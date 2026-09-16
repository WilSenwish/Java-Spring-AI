#!/usr/bin/env node
/**
 * 根 index 小屏留白实测（CDP，零依赖）
 *
 * 目的：量化「小屏空白占比大」到底来自哪里 —— 横向（容器 padding + section margin
 * 吃掉的可用宽度），还是纵向（hero/分隔标题等块级留白）。
 *
 * 用法:
 *   node probe_root_index_whitespace.js                 # 375 视口，打印 JSON
 *   node probe_root_index_whitespace.js 375,414,320     # 指定多视口
 *   node probe_root_index_whitespace.js 375 --shot      # 额外保存全页截图到 tmp/shots/
 */
'use strict';
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME = process.env.CHROME_BIN ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9701 + Math.floor(Math.random() * 200);
const PROFILE = '/tmp/cdp-whitespace-' + PORT;
const ROOT = (function () {
  // 向上查找项目根（同时含 AGENTS.md 与 index.html 的最近祖先）——
  // 本脚本位于技能 scripts/ 目录，__dirname/.. 不再等于项目根，禁止写死层级。
  let d = path.resolve(__dirname);
  for (let i = 0; i < 8; i++) {
    if (fs.existsSync(path.join(d, 'AGENTS.md')) && fs.existsSync(path.join(d, 'index.html'))) return d;
    const p = path.dirname(d);
    if (p === d) break;
    d = p;
  }
  return path.resolve(__dirname, '..');
})();
const SHOTS = path.join(ROOT, 'tmp/shots');

const MEASURE = `
(function () {
  function box(sel) {
    var el = document.querySelector(sel);
    if (!el) return null;
    var r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return {
      sel: sel,
      w: Math.round(r.width), h: Math.round(r.height),
      left: Math.round(r.left), right: Math.round(window.innerWidth - r.right),
      pl: s.paddingLeft, pr: s.paddingRight, pt: s.paddingTop, pb: s.paddingBottom,
      ml: s.marginLeft, mr: s.marginRight, mt: s.marginTop, mb: s.marginBottom
    };
  }
  // 纵向：相邻大块之间的实际空隙
  var blocks = ['.dir-hero', '.dir-legend', '.dir-toolbar', '.dir-container'];
  var gaps = [];
  for (var i = 0; i + 1 < blocks.length; i++) {
    var a = document.querySelector(blocks[i]), b = document.querySelector(blocks[i + 1]);
    if (!a || !b) continue;
    gaps.push({ between: blocks[i] + ' → ' + blocks[i + 1],
      gap: Math.round(b.getBoundingClientRect().top - a.getBoundingClientRect().bottom) });
  }
  // 统计块内部：每个 stat-item 的实际尺寸与网格列数
  var stats = document.querySelector('.dir-stats');
  var sub = document.querySelector('.dir-stats-sub');
  var gs = stats ? getComputedStyle(stats) : null;
  // 列表可用宽度损失：q-item 内容盒 vs 视口
  var qi = document.querySelector('.q-item a');
  var qt = document.querySelector('.q-tags');
  var avail = qi ? Math.round(qi.getBoundingClientRect().width) : null;
  return {
    vw: window.innerWidth,
    docH: document.documentElement.scrollHeight,
    boxes: blocks.concat(['.dir-stats', '.dir-stats-sub', '.dir-section', '.dir-group', '.q-list', '.q-item', '.q-item a', '.q-tags', '.stat-tag'])
      .map(box),
    gaps: gaps,
    statsCols: gs ? gs.gridTemplateColumns : (stats ? getComputedStyle(stats).display : null),
    statsItems: document.querySelectorAll('.dir-stats .stat-item').length,
    subItems: sub ? sub.querySelectorAll('.stat-item').length : 0,
    listAvail: avail,
    listAvailPct: avail ? Math.round(100 * avail / window.innerWidth) : null,
    qTagsPaddingLeft: qt ? getComputedStyle(qt).paddingLeft : null,
    sections: document.querySelectorAll('.dir-section').length,
    expanded: document.querySelectorAll('.dir-section.expanded').length
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

(async () => {
  const args = process.argv.slice(2);
  const shot = args.includes('--shot');
  const vps = (args.find((a) => /^[\d,]+$/.test(a)) || '375').split(',').map((n) => parseInt(n, 10));
  // --url <file>      指定被测 HTML（默认项目根 index.html）
  // --expand N        仅展开前 N 个折叠面板（0 = 全不展开）
  // --shot-section    截图裁剪到第一个 .dir-section 的盒，高 ≤ 900 CSS px（同口径对照用）
  const urlArg = args.indexOf('--url');
  const expandArg = args.indexOf('--expand');
  const expandN = expandArg >= 0 ? parseInt(args[expandArg + 1], 10) : null;
  const shotSection = args.includes('--shot-section');
  const clipSel = args.includes('--clip') ? args[args.indexOf('--clip') + 1] : '.dir-section';
  const tag = args.includes('--tag') ? args[args.indexOf('--tag') + 1] : '';
  const padTop = args.includes('--pad-top') ? parseInt(args[args.indexOf('--pad-top') + 1], 10) : 8;
  const maxH = args.includes('--height') ? parseInt(args[args.indexOf('--height') + 1], 10) : 900;
  const URL = 'file://' + (urlArg >= 0 ? path.resolve(args[urlArg + 1]) : path.join(ROOT, 'index.html'));
  let chrome, ws;
  try {
    chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
      '--remote-debugging-port=' + PORT, '--user-data-dir=' + PROFILE, 'about:blank'], { stdio: 'ignore' });
    let targets = null;
    for (let i = 0; i < 60; i++) {
      try { targets = await getJSON('/json/list'); if (targets && targets.length) break; } catch (e) { /* retry */ }
      await sleep(250);
    }
    if (!targets || !targets.length) throw new Error('CDP 未就绪');
    const page = targets.find((t) => t.type === 'page') || targets[0];
    ws = new WebSocket(page.webSocketDebuggerUrl);
    await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
    let id = 0; const pending = new Map(); let lastLoad = 0;
    ws.addEventListener('message', (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && pending.has(m.id)) {
        const { res, rej } = pending.get(m.id); pending.delete(m.id);
        m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
      } else if (m.method === 'Page.loadEventFired') lastLoad = Date.now();
    });
    const send = (method, params) => new Promise((res, rej) => {
      const i = ++id; pending.set(i, { res, rej });
      ws.send(JSON.stringify({ id: i, method, params: params || {} }));
    });
    await send('Page.enable');
    if (shot) fs.mkdirSync(SHOTS, { recursive: true });
    for (const w of vps) {
      await send('Emulation.setDeviceMetricsOverride', { width: w, height: 812, deviceScaleFactor: 2, mobile: true });
      lastLoad = 0;
      await send('Page.navigate', { url: URL });
      const dl = Date.now() + 15000;
      while (!lastLoad && Date.now() < dl) await sleep(120);
      await sleep(400);
      if (expandN) {
        await send('Runtime.evaluate', { expression:
          "Array.prototype.slice.call(document.querySelectorAll('.dir-section'),0," + expandN +
          ").forEach(function(s){var b=s.querySelector('.dir-body'); if(b) s.classList.add('expanded');})" });
        await sleep(300);
      }
      if (shotSection) {
        fs.mkdirSync(SHOTS, { recursive: true });
        const bb = await send('Runtime.evaluate', { returnByValue: true, expression:
          "(function(){var s=document.querySelector('" + clipSel + "');var r=s.getBoundingClientRect();" +
          "var y=Math.max(0,Math.round(r.top+window.scrollY-" + padTop + "));" +
          "return {x:0,y:y,width:window.innerWidth,height:Math.min(" + maxH + ",Math.round(r.height+" + padTop + "+8))};})()" });
        const capS = await send('Page.captureScreenshot',
          { format: 'png', clip: Object.assign({ scale: 1 }, bb.result.value), captureBeyondViewport: true });
        const fS = path.join(SHOTS, 'root-index-section' + (tag ? '-' + tag : '') + '-' + w + '.png');
        fs.writeFileSync(fS, Buffer.from(capS.data, 'base64'));
        console.log('区块截图 ->', fS, JSON.stringify(bb.result.value));
      }
      const r = await send('Runtime.evaluate', { expression: MEASURE, returnByValue: true });
      console.log('===== 视口 ' + w + ' =====');
      console.log(JSON.stringify(r.result.value, null, 2));
      if (args.includes('--expanded')) {
        await send('Runtime.evaluate', { expression: "document.getElementById('expand-all').click()" });
        await sleep(300);
        const r2 = await send('Runtime.evaluate', { expression: MEASURE, returnByValue: true });
        console.log('===== 视口 ' + w + '（全部展开）=====');
        console.log(JSON.stringify(r2.result.value, null, 2));
      }
      if (shot) {
        // 护栏：全页截图会按整页高度分配位图，根 index 展开态可达 6 万 px（×DSF 2 → 数十 GB），
        // 会直接挂死 Chrome。超过 12000px 时退化为「仅视口截图」并提示。
        const h = r.result.value.docH;
        const beyond = h <= 12000;
        if (!beyond) console.log('页面高 ' + h + 'px，超护栏，改截视口首屏（需要全页请用过 --expanded 关闭）');
        const cap = await send('Page.captureScreenshot',
          { format: 'png', captureBeyondViewport: beyond });
        const f = path.join(SHOTS, 'root-index-' + w + (beyond ? '' : '-viewport') + '.png');
        fs.writeFileSync(f, Buffer.from(cap.data, 'base64'));
        console.log('截图 ->', f);
      }
    }
  } catch (e) {
    console.error('FATAL', e && e.message);
    process.exitCode = 1;
  } finally {
    try { if (ws) ws.close(); } catch (e) { /* noop */ }
    try { if (chrome) chrome.kill('SIGKILL'); } catch (e) { /* noop */ }
    await sleep(200);
    try { fs.rmSync(PROFILE, { recursive: true, force: true }); } catch (e) { /* noop */ }
  }
})();
