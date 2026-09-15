#!/usr/bin/env node
/**
 * 移动端横向溢出实测（CDP，零依赖；复用同一 Chrome 实例）
 *
 * 为什么需要它：
 *   1. macOS 上 Chrome 的 --window-size=375 会被最小窗口宽度钳制为 500 CSS px，
 *      新旧 headless 皆然 —— 测不出真实手机视口，必须用 CDP 的
 *      Emulation.setDeviceMetricsOverride。
 *   2. 文本溢出不改变元素的 getBoundingClientRect()，用 rect 判定会全部漏掉；
 *      正确指标是 scrollWidth - clientWidth。
 *   3. 代码块（.code-block / .compare-table 等）自身横滑属设计，不是缺陷 ——
 *      需向上排除「自身或祖先带 overflow:auto|scroll|hidden」的容器。
 *
 * 用法:
 *   node check_mobile_overflow.js                     # 内置默认页 + 320/375/414
 *   node check_mobile_overflow.js cfg.json            # {viewports:[[w,h]], urls:[...]}
 *   node check_mobile_overflow.js --path <html> [w] [h]
 *
 * 退出码: 0 = 全部无横向溢出；1 = 存在溢出（可直接用作门禁）
 */
'use strict';
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME = process.env.CHROME_BIN ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9601 + Math.floor(Math.random() * 300);
const PROFILE = '/tmp/cdp-mobile-overflow-profile-' + PORT;
const ROOT = path.resolve(__dirname, '../../../..');   // 项目根

const MEASURE = `
(function () {
  function nm(el) {
    var c = (el.getAttribute && el.getAttribute('class')) || '';
    return el.tagName.toLowerCase() + (c ? '.' + c.trim().split(/\\s+/).slice(0, 2).join('.') : '');
  }
  function pathOf(el) {
    var parts = [], n = el;
    while (n && n.nodeType === 1 && parts.length < 5) {
      if (n.id) { parts.unshift(nm(n) + '#' + n.id); break; }
      parts.unshift(nm(n));
      n = n.parentElement;
    }
    return parts.join('>');
  }
  function cardOf(el) {
    var n = el;
    while (n && n !== document.body) {
      if (n.classList && (n.classList.contains('epq-card') || n.classList.contains('qa-card') ||
          n.classList.contains('map-card') || n.classList.contains('chapter-card') ||
          n.classList.contains('eng-card') || n.classList.contains('kpit-card'))) {
        return (n.id || '').toString() || nm(n);
      }
      n = n.parentElement;
    }
    return '(无卡片容器)';
  }
  function clipped(el) {
    if (/auto|scroll|hidden|clip/.test(getComputedStyle(el).overflowX)) return true;
    var p = el.parentElement;
    while (p && p !== document.body && p !== document.documentElement) {
      if (/auto|scroll|hidden|clip/.test(getComputedStyle(p).overflowX)) return true;
      p = p.parentElement;
    }
    return false;
  }
  var hard = [], clippedN = 0;
  document.querySelectorAll('body *').forEach(function (el) {
    var s = getComputedStyle(el);
    if (s.display === 'none' || s.display === 'inline') return;
    if (el.clientWidth <= 0) return;
    if (el.scrollWidth - el.clientWidth <= 1) return;
    if (clipped(el)) { clippedN++; return; }
    hard.push(el);
  });
  var set = new Set(hard);
  var culprits = hard.filter(function (el) {
    var kids = el.querySelectorAll('*');
    for (var i = 0; i < kids.length; i++) if (set.has(kids[i])) return false;
    return true;
  });
  var res = culprits.map(function (el) {
    var found = null, n = el;
    while (n && n !== document.body) {
      if (n.classList && (n.classList.contains('epq-card') || n.classList.contains('qa-card') ||
          n.classList.contains('map-card') || n.classList.contains('chapter-card'))) { found = n; break; }
      n = n.parentElement;
    }
    var cr = found ? found.getBoundingClientRect() : null;
    var r = el.getBoundingClientRect();
    var cs = getComputedStyle(el);
    var contentRight = r.left + (parseFloat(cs.borderLeftWidth) || 0) + el.scrollWidth;
    return {
      card: cardOf(el).slice(0, 22),
      over: el.scrollWidth - el.clientWidth,
      escapesCard: cr ? Math.round(contentRight - cr.right) : null,
      tag: pathOf(el),
      txt: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 56)
    };
  }).sort(function (a, b) { return b.over - a.over; });
  var escaping = res.filter(function (x) { return x.escapesCard > 0; });
  var de = document.documentElement;
  return {
    measured: true, vw: de.clientWidth,
    docScrollOver: de.scrollWidth - de.clientWidth,
    hardTotal: res.length, escapingCard: escaping.length, clippedN: clippedN,
    sample: res.slice(0, 10), escapingSample: escaping.slice(0, 10)
  };
})()`;

function toFileUrl(p) {
  return 'file://' + (p.startsWith('/') ? p : path.resolve(ROOT, p)).replace(/ /g, '%20');
}

// ---- 配置 ----
let cfg;
const argv = process.argv.slice(2);
if (argv[0] === '--path') {
  cfg = { viewports: [[parseInt(argv[2] || 375, 10), parseInt(argv[3] || 812, 10)]], urls: [toFileUrl(argv[1])] };
} else if (argv[0]) {
  cfg = JSON.parse(fs.readFileSync(argv[0], 'utf8'));
  cfg.urls = cfg.urls.map((u) => (u.startsWith('file://') ? u : toFileUrl(u)));
} else {
  const pages = [
    'index.html',
    'java-architect-interview/chapter-questions-eight-part.html',
    'java-architect-interview/chapter-05-spring-core.html',
    'java-architect-interview/chapter-07-mysql-deep.html',
    'java-architect-interview/chapter-11-middleware-engineering.html',
    'java-architect-interview/chapter-questions-scenario.html',
    'java-architect-interview/nav-server-security-checkpoint.html',
    'java-architect-interview-mind/mind-05-spring-core.html'
  ];
  cfg = { viewports: [[320, 720], [375, 812], [414, 896]], urls: pages.map(toFileUrl) };
}

const getJSON = (p) => new Promise((res, rej) => {
  const r = http.get({ host: '127.0.0.1', port: PORT, path: p }, (x) => {
    let b = ''; x.on('data', (d) => (b += d));
    x.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(e); } });
  });
  r.on('error', rej); r.setTimeout(2000, () => r.destroy(new Error('timeout')));
});
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  let chrome, ws;
  const out = [];
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
    for (const [w, h] of cfg.viewports) {
      await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 2, mobile: true });
      for (const url of cfg.urls) {
        lastLoad = 0;
        await send('Page.navigate', { url });
        const dl = Date.now() + 15000;
        while (!lastLoad && Date.now() < dl) await sleep(120);
        await sleep(350);
        let rec = { url: decodeURIComponent(url.split('/').pop()), vw: w, ok: false };
        try {
          const r = await send('Runtime.evaluate', { expression: MEASURE, returnByValue: true });
          const v = r.result && r.result.value;
          if (v && v.measured) {
            rec = {
              url: decodeURIComponent(url.split('/').pop()), vw: v.vw, ok: true,
              docOver: v.docScrollOver, n: v.hardTotal, esc: v.escapingCard,
              sc: v.clippedN, sample: v.sample, escSample: v.escapingSample
            };
          }
        } catch (e) { rec.err = String(e.message || e); }
        out.push(rec);
      }
    }
  } catch (e) {
    out.push({ fatal: String(e && e.message || e) });
  } finally {
    try { if (ws) ws.close(); } catch (e) { /* noop */ }
    try { if (chrome) chrome.kill('SIGKILL'); } catch (e) { /* noop */ }
    await sleep(250);
    try { fs.rmSync(PROFILE, { recursive: true, force: true }); } catch (e) { /* noop */ }
  }

  const bad = out.filter((r) => !r.ok || r.docOver > 0 || r.esc > 0);
  for (const r of out) {
    if (!r.ok) { console.log(`ERR  ${r.url || ''}  ${r.fatal || r.err || ''}`); continue; }
    const flag = (r.docOver > 0 || r.esc > 0) ? 'FAIL' : 'PASS';
    console.log(`${flag} ${String(r.vw).padStart(4)}px  ${r.url.padEnd(46)} 文档溢出=${String(r.docOver).padStart(4)}px  越出卡片=${String(r.esc).padStart(3)}  横滑容器=${r.sc}`);
    if (flag === 'FAIL') for (const s of (r.escSample || []).slice(0, 4)) {
      console.log(`        超出 ${s.over}px  ${s.tag}  ${s.txt ? '| ' + s.txt : ''}`);
    }
  }
  console.log(`\n共 ${out.length} 次测量，异常 ${bad.length} 次 → ${bad.length ? 'FAIL' : 'ALL PASS'}`);
  process.exit(bad.length ? 1 : 0);
})();
