#!/usr/bin/env node
/**
 * 根 index「篇章列表 vs 前序列表」样式分类实测（CDP，零依赖）
 *
 * 目的：把页内**全部** .dir-section 的结构特征 + 计算样式导出，按「是否含 .dir-group」
 * 分类对比，量化两类区块在边框 / 头部底色 / 内缩 / 题号左缘上的差异。
 *
 * 用法: node probe_section_style.js [1200]
 */
'use strict';
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME = process.env.CHROME_BIN ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9900 + Math.floor(Math.random() * 80);
const PROFILE = '/tmp/cdp-secstyle-' + PORT;
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

const MEASURE = `
(function () {
  var cs = function (el) { return getComputedStyle(el); };
  var r1 = function (x) { return Math.round(x * 10) / 10; };
  var out = [];
  var secs = document.querySelectorAll('.dir-section');
  for (var i = 0; i < secs.length; i++) {
    var s = secs[i];
    var sr = s.getBoundingClientRect();
    var h = s.querySelector('.dir-header');
    var hr = h ? h.getBoundingClientRect() : null;
    var hs = h ? cs(h) : null;
    var firstItem = s.querySelector('.q-item');
    var is = firstItem ? cs(firstItem) : null;
    var ir = firstItem ? firstItem.getBoundingClientRect() : null;
    var qid = s.querySelector('.q-id');
    var qr = qid ? qid.getBoundingClientRect() : null;
    var qidS = qid ? cs(qid) : null;
    var ql = s.querySelector('.q-list');
    var qls = ql ? cs(ql) : null;
    var gt = s.querySelector('.dir-group-title');
    var gr = gt ? gt.getBoundingClientRect() : null;
    var body = s.querySelector('.dir-body');
    var bs = body ? cs(body) : null;
    var grp = s.querySelector('.dir-group');
    var gs = grp ? cs(grp) : null;
    var title = s.querySelector('.dir-title');
    var tr = title ? title.getBoundingClientRect() : null;
    var count = s.querySelector('.dir-count');
    var cr = count ? count.getBoundingClientRect() : null;
    var cntS = count ? cs(count) : null;
    out.push({
      idx: i,
      title: title ? title.textContent.trim().slice(0, 26) : '(无标题)',
      hasGroup: !!grp,
      hasTagline: !!s.querySelector('.tagline'),
      groups: s.querySelectorAll('.dir-group').length,
      items: s.querySelectorAll('.q-item').length,
      secLeft: r1(sr.left), secRight: r1(sr.right), secTop: r1(sr.top + window.scrollY),
      borderW: cs(s).borderLeftWidth, borderColor: cs(s).borderLeftColor,
      radius: cs(s).borderTopLeftRadius, secBg: cs(s).backgroundColor,
      headerBg: hs ? hs.backgroundColor : null,
      headerPadLeft: hs ? hs.paddingLeft : null,
      headerPadRight: hs ? hs.paddingRight : null,
      bodyPadLeft: bs ? bs.paddingLeft : null,
      groupPadLeft: gs ? gs.paddingLeft : null,
      qListPadLeft: qls ? qls.paddingLeft : null,
      itemPadLeft: is ? is.paddingLeft : null,
      itemPadRight: is ? is.paddingRight : null,
      titleLeftRel: tr ? r1(tr.left - sr.left) : null,
      qidLeftRel: qr ? r1(qr.left - sr.left) : null,
      qidW: qidS ? qidS.width : null,
      qidColor: qidS ? qidS.color : null,
      qidDecoration: qidS ? (qidS.textDecorationLine || qidS.textDecoration) : null,
      titleDecoration: title ? cs(title).textDecorationLine : null,
      groupTitleLeftRel: gr ? r1(gr.left - sr.left) : null,
      groupTitleColor: gt ? cs(gt).color : null,
      countLeftRel: cr ? r1(cr.left - sr.left) : null,
      countRightRel: cr ? r1(cr.right - sr.left) : null,
      countBg: cntS ? cntS.backgroundColor : null,
      countBorder: cntS ? cntS.borderTopWidth + ' ' + cntS.borderTopColor : null,
      countRadius: cntS ? cntS.borderTopLeftRadius : null,
      groupCountStyle: gt ? (function () {
        var gc = s.querySelector('.dir-group-count');
        if (!gc) return null;
        var g = cs(gc);
        var gr2 = gc.getBoundingClientRect();
        return { bg: g.backgroundColor, border: g.borderTopWidth + ' ' + g.borderTopColor,
                 radius: g.borderTopLeftRadius, rightRel: r1(gr2.right - sr.left), color: g.color };
      })() : null
    });
  }
  return { vw: window.innerWidth, docH: document.documentElement.scrollHeight, secs: out };
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
  const vps = (args.find((a) => /^[\d,]+$/.test(a)) || '1200').split(',').map((n) => parseInt(n, 10));
  const urlArg = args.includes('--url') ? args[args.indexOf('--url') + 1] : null;
  const URL = urlArg ? 'file://' + path.resolve(urlArg) : 'file://' + path.join(ROOT, 'index.html');
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
    for (const w of vps) {
      await send('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 768 });
      lastLoad = 0;
      await send('Page.navigate', { url: URL });
      const dl = Date.now() + 15000;
      while (!lastLoad && Date.now() < dl) await sleep(120);
      await sleep(400);
      await send('Runtime.evaluate', { expression:
        "Array.prototype.forEach.call(document.querySelectorAll('.dir-section'), function(s){ s.classList.add('expanded'); })" });
      await sleep(600);
      const r = await send('Runtime.evaluate', { expression: MEASURE, returnByValue: true });
      console.log('===== 视口 ' + w + ' =====');
      console.log(JSON.stringify(r.result.value));
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
