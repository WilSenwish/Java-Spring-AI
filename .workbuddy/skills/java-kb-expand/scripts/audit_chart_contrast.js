#!/usr/bin/env node
/**
 * 图表可读性审计（深色 / 浅色均可）——CDP + headless Chrome，零依赖
 *
 * 为什么需要它：
 *   Mermaid 的 `style X fill:#dbeafe` 会渲染成元素上的内联 `fill:#dbeafe !important`；
 *   样式表里的 !important **压不过**内联 !important，所以「深色下节点是否可读」
 *   无法靠静态检查或肉眼看源码判定 —— 只有把页面真渲染出来量对比度才知道。
 *
 * 判定：图内文字 vs「按绘制顺序回溯到的真实底色」的 WCAG 对比度。
 *   <3 = 不可读（浅底浅字，实测会到 1.0）；<4.5 = 不达 AA。
 *
 * 用法:
 *   node audit_chart_contrast.js dark                      # 全站深色（两个站目录）
 *   node audit_chart_contrast.js light --json out.json     # 浅色 + 落盘原始结果
 *   node audit_chart_contrast.js dark --dirs java-architect-interview/chapter-05-spring-core.html
 *   node audit_chart_contrast.js dark --limit 5
 * 退出码: 0 = 无 <3 的节点；1 = 存在不可读节点
 *
 * 注意（实现坑，勿回退）：
 *   ① 底色必须「按绘制顺序」回溯到**文字之前最近的、可见且非零面积的形状** ——
 *      Mermaid 在 `g.label` 下放了一个 0 面积空 `rect`（默认 black），按「祖先链第一个 fill」取会取到它，
 *      假阴（误判为高对比）。
 *   ② `elementsFromPoint` 对视口外元素返回空，不可作为主路径。
 *   ③ 含子 `tspan` 的父 `text` 必须跳过（其 fill 是 `actorBkg`，真正字形色在 `tspan` 上），否则假阳。
 */
'use strict';
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME = process.env.CHROME_BIN ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9901 + Math.floor(Math.random() * 300);
const PROFILE = '/tmp/cdp-dark-audit-' + PORT;
function findRoot(start) {
  let d = start;
  while (d !== path.dirname(d)) {
    if (fs.existsSync(path.join(d, 'AGENTS.md')) && fs.existsSync(path.join(d, 'index.html'))) return d;
    d = path.dirname(d);
  }
  return start;
}
// 项目根：向上查找同时含 AGENTS.md 与 index.html 的最近祖先（本技能可经软链调用，禁用固定层级）
const ROOT = findRoot(__dirname);

const MEASURE = `
(function () {
  function lum(c) {
    var m = String(c).match(/rgba?\\(([^)]+)\\)/);
    if (!m) return null;
    var p = m[1].split(',').map(parseFloat);
    if (p.length > 3 && p[3] === 0) return null;
    var f = p.slice(0, 3).map(function (v) {
      v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2];
  }
  function ratio(a, b) {
    var la = lum(a), lb = lum(b);
    if (la === null || lb === null) return null;
    return Math.round(((Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05)) * 100) / 100;
  }
  var SHAPE = /^(rect|circle|ellipse|polygon|path)$/;
  /** 绘制顺序回溯：取该文字「之前」最近的、真正可见的形状填充色作为底 */
  function bgBehind(el) {
    var host = el.closest('.mermaid-container');
    var n = el, guard = 0;
    while (n && n !== document.body && guard++ < 16) {
      var p = n.parentElement;
      if (!p) break;
      var cands = [];
      if (SHAPE.test(p.tagName.toLowerCase())) cands.push(p);
      var kids = p.children;
      for (var i = 0; i < kids.length; i++) {
        if (kids[i] === n) break;
        if (SHAPE.test(kids[i].tagName.toLowerCase())) cands.push(kids[i]);
      }
      for (var j = cands.length - 1; j >= 0; j--) {
        var cs = getComputedStyle(cands[j]);
        var f = cs.fill;
        if (!f || f === 'none') continue;
        if (lum(f) === null) continue;                       // alpha=0 透明
        var r = cands[j].getBoundingClientRect();
        if (r.width < 2 || r.height < 2) continue;            // 0 面积占位 rect（mermaid 的 g.label > rect）
        return f;
      }
      n = p;
      if (n === host) break;
    }
    return host ? getComputedStyle(host).backgroundColor : getComputedStyle(document.body).backgroundColor;
  }
  function collectTextEls(c) {
    var out = [];
    c.querySelectorAll('svg text, foreignObject span, .nodeLabel, .cluster-label span, .messageText, .loopText, .noteText, .actor').forEach(function (el) {
      if (el.tagName.toLowerCase() === 'text' && el.querySelector('tspan')) return; // 字色在 tspan 上
      out.push(el);
    });
    return out;
  }
  var rows = [], hist = {};
  document.querySelectorAll('.mermaid-container').forEach(function (c, ci) {
    collectTextEls(c).forEach(function (el) {
      var txt = (el.textContent || '').replace(/\\s+/g, ' ').trim();
      if (!txt) return;
      var cs = getComputedStyle(el);
      var isSvgText = /^(text|tspan)$/.test(el.tagName.toLowerCase());
      var fg = isSvgText ? cs.fill : cs.color;
      var bg = bgBehind(el);
      var rt = ratio(fg, bg);
      if (rt === null) return;
      var inlineShape = '';
      var g = el.closest('g.node') || el.closest('g.cluster');
      if (g) {
        var sh = g.querySelector('rect,circle,ellipse,polygon,path');
        if (sh) inlineShape = (sh.getAttribute('style') || '').replace(/\\s+/g, ' ');
      } else {
        var sh2 = el.parentElement && el.parentElement.querySelector('rect,circle,ellipse,polygon,path');
        if (sh2) inlineShape = (sh2.getAttribute('style') || '').replace(/\\s+/g, ' ');
      }
      rows.push({ fig: ci, txt: txt.slice(0, 20), fg: fg, bg: bg, r: rt, inline: inlineShape.slice(0, 58) });
      if (inlineShape && /fill\\s*:/.test(inlineShape)) hist[inlineShape] = (hist[inlineShape] || 0) + 1;
    });
  });
  var bad3 = rows.filter(function (x) { return x.r < 3; });
  var bad45 = rows.filter(function (x) { return x.r < 4.5 && x.r >= 3; });
  return {
    ok: true,
    theme: document.documentElement.getAttribute('data-theme') || '(none)',
    bodyBg: getComputedStyle(document.body).backgroundColor,
    containers: document.querySelectorAll('.mermaid-container').length,
    svgRendered: document.querySelectorAll('.mermaid svg').length,
    labels: rows.length,
    bad3: bad3.length, bad45: bad45.length,
    inlineHist: hist,
    worst: bad3.sort(function (a, b) { return a.r - b.r; }).slice(0, 10),
    mid: bad45.slice(0, 6)
  };
})()`;

const toFileUrl = (p) => 'file://' + path.resolve(ROOT, p).replace(/ /g, '%20');
const getJSON = (p) => new Promise((res, rej) => {
  const r = http.get({ host: '127.0.0.1', port: PORT, path: p }, (x) => {
    let b = ''; x.on('data', (d) => (b += d));
    x.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(e); } });
  });
  r.on('error', rej); r.setTimeout(2000, () => r.destroy(new Error('timeout')));
});
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function collectPages(dirs) {
  const out = [];
  for (const d of dirs) {
    const abs = path.resolve(ROOT, d);
    if (!fs.existsSync(abs)) continue;
    if (fs.statSync(abs).isFile()) { out.push(d); continue; }
    for (const f of fs.readdirSync(abs)) {
      if (f.endsWith('.html')) out.push(path.join(d, f));
    }
  }
  return out.sort();
}

(async () => {
  const argv = process.argv.slice(2);
  const mode = argv[0] || 'dark';
  let dirs = ['java-architect-interview', 'java-architect-interview-mind'];
  let limit = 0, jsonOut = null;
  for (let i = 1; i < argv.length; i++) {
    if (argv[i] === '--dirs') dirs = argv[++i].split(',');
    else if (argv[i] === '--limit') limit = parseInt(argv[++i], 10);
    else if (argv[i] === '--json') jsonOut = argv[++i];
  }
  let pages = collectPages(dirs);
  if (limit) pages = pages.slice(0, limit);

  let chrome, ws;
  const results = [];
  try {
    chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
      '--allow-file-access-from-files',
      '--remote-debugging-port=' + PORT, '--user-data-dir=' + PROFILE, 'about:blank'], { stdio: 'ignore' });
    let targets = null;
    for (let i = 0; i < 60; i++) {
      try { targets = await getJSON('/json/list'); if (targets && targets.length) break; } catch (e) { }
      await sleep(250);
    }
    if (!targets || !targets.length) throw new Error('CDP 未就绪');
    const t = targets.find((x) => x.type === 'page') || targets[0];
    ws = new WebSocket(t.webSocketDebuggerUrl);
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
    await send('Emulation.setDeviceMetricsOverride', { width: 1400, height: 1000, deviceScaleFactor: 1, mobile: false });
    await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: mode }] });

    for (const p of pages) {
      lastLoad = 0;
      await send('Page.navigate', { url: toFileUrl(p) });
      const dl = Date.now() + 25000;
      while (!lastLoad && Date.now() < dl) await sleep(100);
      await sleep(1600);
      try {
        const r = await send('Runtime.evaluate', { expression: MEASURE, returnByValue: true });
        const v = r.result && r.result.value;
        if (v && v.ok) { v.page = path.basename(p); v.dir = p.startsWith('java-architect-interview-mind') ? 'mind' : 'chap'; results.push(v); }
        else results.push({ page: path.basename(p), err: 'no-measure' });
      } catch (e) { results.push({ page: path.basename(p), err: String(e.message || e).slice(0, 120) }); }
    }
  } catch (e) {
    console.log('FATAL: ' + (e && e.message || e));
    process.exit(2);
  } finally {
    try { if (ws) ws.close(); } catch (e) { }
    try { if (chrome) chrome.kill('SIGKILL'); } catch (e) { }
    await sleep(200);
    try { fs.rmSync(PROFILE, { recursive: true, force: true }); } catch (e) { }
  }

  const withFigs = results.filter((r) => !r.err);
  const totBad3 = withFigs.reduce((a, r) => a + r.bad3, 0);
  const totBad45 = withFigs.reduce((a, r) => a + r.bad45, 0);
  const totLabels = withFigs.reduce((a, r) => a + r.labels, 0);
  console.log(`模式=${mode}  页面=${results.length}  有图页=${withFigs.length}  图容器=${withFigs.reduce((a, r) => a + r.containers, 0)}  已渲染SVG=${withFigs.reduce((a, r) => a + r.svgRendered, 0)}`);
  console.log(`文字样本=${totLabels}  对比度<3（不可读）=${totBad3}  <4.5（不达AA）=${totBad45}\n`);
  console.log('--- 逐页（仅列出有问题的）---');
  withFigs.filter((r) => r.bad3 > 0 || r.bad45 > 0)
    .sort((a, b) => b.bad3 - a.bad3)
    .forEach((r) => console.log(`${String(r.bad3).padStart(4)}  <3 | ${String(r.bad45).padStart(3)} mid | ${r.page}`));
  const errs = results.filter((r) => r.err);
  if (errs.length) { console.log('\n--- 未能测量 ---'); errs.forEach((e) => console.log('  ' + e.page + '  ' + e.err)); }

  const allWorst = [];
  withFigs.forEach((r) => (r.worst || []).forEach((w) => allWorst.push(Object.assign({ page: r.page }, w))));
  allWorst.sort((a, b) => a.r - b.r);
  console.log('\n--- 全站最差 12 例 ---');
  allWorst.slice(0, 12).forEach((w) => console.log(`  ${String(w.r).padStart(5)} | ${w.page} fig${w.fig} | "${w.txt}" fg=${w.fg} bg=${w.bg} | ${w.inline}`));
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(results, null, 1), 'utf8');
  process.exit(totBad3 > 0 ? 1 : 0);
})();
