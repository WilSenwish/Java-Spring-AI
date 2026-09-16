#!/usr/bin/env node
/**
 * 列表 marker 缩进实测（CDP，零依赖）—— 门禁级检查
 *
 * 为什么需要它：
 *   design-system.css 顶部的 reset（`* { margin:0; padding:0 }`）抹掉了 ul/ol 的
 *   UA 默认 `padding-inline-start`（40px）。全站列表缩进因此完全依赖各自的类规则；
 *   凡未匹配到类规则的列表 padding-left 即为 0，而 `list-style-position: outside`
 *   的圆点/数字是绘制在内容盒之外的 —— 会被甩进卡片内边距区：
 *     · 桌面：列表没有缩进、圆点贴着卡片边缘（视觉上「缩进不对」）
 *     · 小屏：卡片内边距收窄到 0.9rem(14.4px)，marker 直接越出卡片
 *   （2026-09-16 实测：核心原理页 20 处、安全检查页 1 处；修复见共享 CSS 的
 *   零特异度兜底 `:where(ul, ol) { padding-inline-start: 1.25rem }`）
 *
 * 判定：markerSpace = 列表内容盒左边 − 边界容器内容盒左边
 *      need        ≈ 1.2 × li 字号（marker 宽 + 与文本的间隙），带 0.5px 亚像素容差
 *      markerSpace < need − 0.5 → SUSPECT
 *      `list-style-position: inside` 与 `list-style-type: none` 的列表不参与判定
 *      （marker 在内容流内 / 无 marker）。
 *
 * 另判定（2026-09-16 补）：同一容器内「有 marker 的 ol」与「有 marker 的 ul」
 *      padding-inline-start 必须一致 —— min(ol pl) < max(ul pl) − 0.5 → MISMATCH。
 *      根因：多处 CSS 只给 ul 写了缩进（如 nav-server-security-checkpoint 的
 *      `.content-main ul{padding-left:24px}`），ol 回落到共享样式 1.25rem 兜底，
 *      数字比圆点少缩进 4px。**给 ul 加规则时务必同步写 ol。**
 *
 * 用法:
 *   node check_list_indent.js                     # 全站 44 页 × {1280, 375}
 *   node check_list_indent.js --viewport 375      # 指定视口
 *   node check_list_indent.js --only <相对路径>    # 指定单页
 *   node check_list_indent.js --dump              # 打印各分组样本（定位容器用）
 *   node check_list_indent.js --out r.json        # 结果落 JSON
 *
 * 退出码: 0 = 全站列表缩进正常；1 = 存在 marker 空间不足的列表
 */
'use strict';
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME = process.env.CHROME_BIN ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9901 + Math.floor(Math.random() * 300);
const PROFILE = '/tmp/cdp-list-indent-' + PORT;
const ROOT = path.resolve(__dirname, '../../../..');   // 项目根

function allPages() {
  const out = [];
  for (const dir of ['java-architect-interview', 'java-architect-interview-mind']) {
    const d = path.join(ROOT, dir);
    if (!fs.existsSync(d)) continue;
    for (const f of fs.readdirSync(d)) if (f.endsWith('.html')) out.push(dir + '/' + f);
  }
  if (fs.existsSync(path.join(ROOT, 'index.html'))) out.push('index.html');
  return out.sort();
}

const MEASURE = `
(function () {
  function nm(el) {
    var c = (el.getAttribute && el.getAttribute('class')) || '';
    return el.tagName.toLowerCase() + (c ? '.' + c.trim().split(/\\s+/).slice(0, 3).join('.') : '');
  }
  function pathOf(el) {
    var parts = [], n = el;
    while (n && n.nodeType === 1 && parts.length < 4) {
      if (n.id) { parts.unshift(nm(n) + '#' + n.id); break; }
      parts.unshift(nm(n));
      n = n.parentElement;
    }
    return parts.join('>');
  }
  var CARDCLS = ['epq-card','qa-card','map-card','chapter-card','eng-card','kpit-card',
                 'group-lead-block','epq-section','lead-block','card','map-col','chapter-lead'];
  function cardOf(el) {
    var n = el.parentElement;
    while (n && n !== document.body) {
      for (var i = 0; i < CARDCLS.length; i++) if (n.classList && n.classList.contains(CARDCLS[i])) return n;
      n = n.parentElement;
    }
    return null;
  }
  /* 边界容器：优先卡片类；否则退到最近「有内边距的块级祖先」；再退到 main。
     绝不用 0（视口左边距不是可用空间，会造成 375px 假阳 / 1280px 假阴）。 */
  function boundaryOf(el) {
    var c = cardOf(el);
    if (c) return c;
    var n = el.parentElement;
    while (n && n !== document.body) {
      var s = getComputedStyle(n);
      if (s.display !== 'inline' && ((parseFloat(s.paddingLeft) || 0) > 1 ||
          (parseFloat(s.borderLeftWidth) || 0) > 0)) return n;
      n = n.parentElement;
    }
    return document.querySelector('main.content-main') || document.querySelector('main') || document.body;
  }
  var out = [];
  var cardRefs = [];
  document.querySelectorAll('ul,ol').forEach(function (ul) {
    var s = getComputedStyle(ul);
    if (s.display === 'none') return;
    var r = ul.getBoundingClientRect();
    if (r.width <= 0) return;
    var card = boundaryOf(ul);
    var cr = card.getBoundingClientRect();
    var ccs = getComputedStyle(card);
    var cardContentLeft = cr.left + (parseFloat(ccs.borderLeftWidth) || 0) + (parseFloat(ccs.paddingLeft) || 0);
    var pl = parseFloat(s.paddingLeft) || 0;
    var ml = parseFloat(s.marginLeft) || 0;
    var contentLeft = r.left + pl + (parseFloat(s.borderLeftWidth) || 0);
    var li = ul.querySelector(':scope > li');
    var lf = li ? (parseFloat(getComputedStyle(li).fontSize) || 16) : 16;
    var lpos = li ? getComputedStyle(li).listStylePosition : s.listStylePosition;
    var need = (s.listStyleType === 'none' ? 0 : 1.2 * lf);
    var markerSpace = (s.listStyleType === 'none' || lpos === 'inside') ? Infinity : (contentLeft - cardContentLeft);
    var rec = {
      card: card ? (card.id || nm(card)).slice(0, 26) : '(no-card)',
      sel: pathOf(ul).slice(0, 46),
      tag: ul.tagName.toLowerCase(),
      type: s.listStyleType,
      pos: lpos,
      pl: Math.round(pl * 10) / 10,
      ml: Math.round(ml * 10) / 10,
      gap: Math.round((r.left - cardContentLeft) * 10) / 10,
      space: markerSpace === Infinity ? null : Math.round(markerSpace * 10) / 10,
      need: Math.round(need),
      li: Math.round(lf * 10) / 10,
      suspect: markerSpace !== Infinity && markerSpace < need - 0.5,
      txt: (ul.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 42)
    };
    out.push(rec);
    cardRefs.push({ el: card, rec: rec });
  });
  /* 同容器（含 marker 的）有序列表与无序列表缩进必须一致：
     实测 nav-server-security-checkpoint 的 .content-main ul{padding-left:24px} 漏了 ol，
     导致正文数字列表回落到 1.25rem 兜底，比圆点少缩进 4px（2026-09-16 修复）。
     只比较同一 boundaryOf 容器，避免跨区块误判；body 级容器不参与（粒度太粗）。 */
  var cardMap = new Map();
  cardRefs.forEach(function (x) {
    if (!x.el || x.el === document.body) return;
    if (x.rec.type === 'none' || x.rec.pos === 'inside') return;
    var e = cardMap.get(x.el);
    if (!e) { e = { name: x.rec.card, ul: [], ol: [] }; cardMap.set(x.el, e); }
    (x.rec.tag === 'ol' ? e.ol : e.ul).push(x.rec.pl);
  });
  var mismatch = [];
  cardMap.forEach(function (e) {
    if (!e.ul.length || !e.ol.length) return;
    var maxUl = Math.max.apply(null, e.ul);
    var minOl = Math.min.apply(null, e.ol);
    if (minOl < maxUl - 0.5) mismatch.push({ card: e.name, ulPl: maxUl, olPl: minOl });
  });
  var sus = out.filter(function (o) { return o.suspect; });
  var samples = {};
  out.forEach(function (o) {
    var k = o.type + '@pl=' + o.pl;
    (samples[k] = samples[k] || []).length < 3 &&
      samples[k].push(o.card + ' :: ' + o.sel + ' [liPos=' + o.pos + ' space=' + o.space + ' need=' + o.need + ']');
  });
  return {
    measured: true, vw: document.documentElement.clientWidth,
    total: out.length, suspect: sus.length, mismatch: mismatch.slice(0, 12),
    byPl: out.reduce(function (a, o) { var k = o.type + '@pl=' + o.pl; a[k] = (a[k] || 0) + 1; return a; }, {}),
    samples: samples, sus: sus.slice(0, 60)
  };
})()`;

const getJSON = (p) => new Promise((res, rej) => {
  const r = http.get({ host: '127.0.0.1', port: PORT, path: p }, (x) => {
    let b = ''; x.on('data', (d) => (b += d));
    x.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(e); } });
  });
  r.on('error', rej); r.setTimeout(2000, () => r.destroy(new Error('timeout')));
});
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const toFileUrl = (p) => 'file://' + path.resolve(ROOT, p).replace(/ /g, '%20');

(async () => {
  const argv = process.argv.slice(2);
  const outIdx = argv.indexOf('--out');
  const onlyArg = argv.indexOf('--only');
  const vpArg = argv.indexOf('--viewport');
  const viewports = vpArg >= 0 ? [[parseInt(argv[vpArg + 1], 10), 812]] : [[1280, 900], [375, 812]];
  const runPages = onlyArg >= 0 ? [argv[onlyArg + 1]] : allPages();

  const results = [];
  let chrome, ws;
  try {
    chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
      '--remote-debugging-port=' + PORT, '--user-data-dir=' + PROFILE, 'about:blank'], { stdio: 'ignore' });
    let targets = null;
    for (let i = 0; i < 60; i++) {
      try { targets = await getJSON('/json/list'); if (targets && targets.length) break; } catch (e) { /* retry */ }
      await sleep(250);
    }
    if (!targets || !targets.length) throw new Error('CDP 未就绪（Chrome 未启动）');
    const page = targets.find((t) => t.type === 'page') || targets[0];
    ws = new WebSocket(page.webSocketDebuggerUrl);
    await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
    let id = 0; const pending = new Map(); let lastLoad = 0;
    ws.addEventListener('message', (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && pending.has(m.id)) {
        const { res, rej } = pending.get(m.id); pending.delete(m.id);
        m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
      } else if (m.method === 'Page.loadEventFired') { lastLoad = Date.now(); }
    });
    const send = (method, params) => new Promise((res, rej) => {
      const i = ++id; pending.set(i, { res, rej });
      ws.send(JSON.stringify({ id: i, method, params: params || {} }));
    });
    await send('Page.enable');
    for (const [w, h] of viewports) {
      await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 2, mobile: w < 700 });
      for (const p of runPages) {
        lastLoad = 0;
        await send('Page.navigate', { url: toFileUrl(p) });
        const dl = Date.now() + 15000;
        while (!lastLoad && Date.now() < dl) await sleep(120);
        await sleep(300);
        const rec = { page: p.split('/').pop(), vw: w };
        try {
          const r = await send('Runtime.evaluate', { expression: MEASURE, returnByValue: true });
          Object.assign(rec, (r.result && r.result.value) || { err: 'no-value' });
        } catch (e) { rec.err = String(e.message || e); }
        results.push(rec);
      }
    }
  } catch (e) {
    console.log('FATAL ' + (e && e.message));
  } finally {
    try { if (ws) ws.close(); } catch (e) { /* noop */ }
    try { if (chrome) chrome.kill('SIGKILL'); } catch (e) { /* noop */ }
    await sleep(200);
    try { fs.rmSync(PROFILE, { recursive: true, force: true }); } catch (e) { /* noop */ }
  }

  if (outIdx >= 0) fs.writeFileSync(path.resolve(ROOT, argv[outIdx + 1]), JSON.stringify(results, null, 1));
  let bad = 0;
  for (const r of results) {
    if (r.err) { console.log(`ERR  ${r.page} @${r.vw}  ${r.err}`); bad++; continue; }
    const mis = r.mismatch || [];
    const isBad = r.suspect > 0 || mis.length > 0;
    if (isBad) bad++;
    console.log(`${isBad ? 'FAIL' : 'PASS'} ${String(r.vw).padStart(4)}px  ${r.page.padEnd(46)} 列表=${String(r.total).padStart(3)} 嫌疑=${String(r.suspect).padStart(2)} 缩进不一致=${String(mis.length).padStart(2)}  ${JSON.stringify(r.byPl)}`);
    if (r.suspect > 0) for (const s of r.sus) {
      console.log(`         ${s.card} | ${s.sel}`);
      console.log(`           type=${s.type} pos=${s.pos} pl=${s.pl} 可用=${s.space}px 需=${s.need}px | ${s.txt}`);
    }
    for (const m of mis) {
      console.log(`         [缩进不一致] ${m.card}：ol pl=${m.olPl} < ul pl=${m.ulPl}（数字比圆点少缩进 ${(m.ulPl - m.olPl).toFixed(1)}px）`);
    }
  }
  if (argv.includes('--dump')) {
    console.log('\n--- 分组样本（每类最多 3 条）---');
    for (const r of results) {
      if (!r.samples) continue;
      console.log(`  ${r.page} @${r.vw}`);
      for (const [k, v] of Object.entries(r.samples)) console.log(`    ${k}  ->  ${v[0]}`);
    }
  }
  const total = results.reduce((a, r) => a + (r.suspect || 0), 0);
  const totalMis = results.reduce((a, r) => a + ((r.mismatch || []).length), 0);
  console.log(`\n共 ${results.length} 次测量，marker 缩进不足 ${total} 处、ol/ul 缩进不一致 ${totalMis} 处 → ${bad ? 'FAIL' : 'ALL PASS'}`);
  process.exit(bad ? 1 : 0);
})();
