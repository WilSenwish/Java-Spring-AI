/* xinchuang/assets/app.js · 信创研究站交互（零依赖、零外部资源）
 * 职责：
 *  1) 主题三态（浅色 / 深色 / 系统），localStorage 持久化，单一状态源为 html[data-theme]；
 *  2) 顶部工具条：回顶、主题按钮文案同步；
 *  3) 阅读进度（顶栏细条 + 右下浮动环）与回顶 / 去底按钮（DOM 由本文件注入，样式在 base.css）；
 *  4) 页内目录滚动高亮 + 折叠开关；
 *  5) 小屏目录抽屉（左下 FAB + 遮罩 + Esc 关闭）；
 *  6) 站内搜索：读取 assets/search-data.js 的 window.XC_SEARCH，跨页检索章节标题。
 * 说明：本文件刻意使用 ES5 风格字符串拼接，避免模板字符串与构建期转义纠缠。
 */
(function () {
  'use strict';

  /* ---------- 1. 主题 ---------- */
  var KEY = 'xc-theme';
  var LABELS = { light: '☀ 浅色', dark: '☾ 深色', system: '◐ 系统' };
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function readPref() {
    try {
      var v = localStorage.getItem(KEY);
      return (v === 'light' || v === 'dark') ? v : 'system';
    } catch (e) { return 'system'; }
  }
  function effective(pref) {
    if (pref === 'light' || pref === 'dark') return pref;
    return mq && mq.matches ? 'dark' : 'light';
  }
  function apply(pref, fire) {
    var eff = effective(pref);
    document.documentElement.setAttribute('data-theme', eff);
    var btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = LABELS[pref] || LABELS.system;
    if (fire) document.dispatchEvent(new CustomEvent('xc-theme-change', { detail: { pref: pref, effective: eff } }));
  }
  function cycle() {
    var order = ['light', 'dark', 'system'];
    var next = order[(order.indexOf(readPref()) + 1) % order.length];
    try {
      if (next === 'system') localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, next);
    } catch (e) { /* 隐私模式下忽略持久化失败 */ }
    apply(next, true);
  }
  apply(readPref(), false);
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) themeBtn.addEventListener('click', cycle);
  if (mq) {
    var onSys = function () { if (readPref() === 'system') apply('system', true); };
    if (mq.addEventListener) mq.addEventListener('change', onSys);
    else if (mq.addListener) mq.addListener(onSys);
  }

  /* ---------- 2. 工具条回顶 ---------- */
  var topBtn = document.getElementById('topBtn');
  if (topBtn) topBtn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ---------- 3. 阅读进度 / 回顶 / 去底（注入 DOM） ---------- */
  function injectFab(cls, label, svg, onClick) {
    var b = document.createElement('button');
    b.className = cls; b.type = 'button';
    b.setAttribute('aria-label', label); b.setAttribute('title', label);
    b.innerHTML = svg;
    b.addEventListener('click', onClick);
    document.body.appendChild(b);
    return b;
  }
  var bar = document.createElement('div');
  bar.className = 'reading-progress';
  document.body.appendChild(bar);

  var ring = document.createElement('div');
  ring.className = 'reading-progress-fab';
  ring.setAttribute('aria-hidden', 'true');
  ring.innerHTML = '<svg class="reading-progress-fab__svg" viewBox="0 0 40 40">'
    + '<circle class="reading-progress-fab__track" cx="20" cy="20" r="17"></circle>'
    + '<circle class="reading-progress-fab__value" cx="20" cy="20" r="17"></circle></svg>'
    + '<span class="reading-progress-fab__label">0%</span>';
  document.body.appendChild(ring);
  var ringValue = ring.querySelector('.reading-progress-fab__value');
  var ringLabel = ring.querySelector('.reading-progress-fab__label');

  var bottomFab = injectFab('go-to-bottom', '去底部',
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 16l-6-6h4V4h4v6h4l-6 6z"/></svg>',
    function () { window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' }); });
  var topFab = injectFab('back-to-top', '回到顶部',
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 8l6 6h-4v6h-4v-6H6l6-6z"/></svg>',
    function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  var ticking = false;
  function onScrollFrame() {
    ticking = false;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var y = window.scrollY || window.pageYOffset || 0;
    var pct = h > 0 ? Math.max(0, Math.min(100, Math.round(y / h * 100))) : 0;
    bar.style.width = pct + '%';
    ringValue.style.strokeDashoffset = String(106.814 * (1 - pct / 100));
    ringLabel.textContent = pct + '%';
    if (y > 320) { topFab.classList.add('visible'); } else { topFab.classList.remove('visible'); }
    if (h - y > 320) { bottomFab.classList.add('visible'); } else { bottomFab.classList.remove('visible'); }
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScrollFrame); }
  }, { passive: true });
  window.addEventListener('resize', onScrollFrame);
  onScrollFrame();

  /* ---------- 4. 目录：滚动高亮 + 折叠开关 ---------- */
  function initToc() {
    var toc = document.querySelector('nav.toc');
    if (!toc) return;
    var links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
    var pairs = links.map(function (a) {
      return { a: a, el: document.getElementById(a.getAttribute('href').slice(1)) };
    }).filter(function (p) { return p.el; });

    var fold = document.createElement('button');
    fold.type = 'button'; fold.className = 'toc-fold-toggle'; fold.textContent = '目录';
    fold.setAttribute('aria-expanded', 'true');
    var wrap = toc.querySelector('.wrap');
    if (wrap) wrap.insertBefore(fold, wrap.firstChild);
    fold.addEventListener('click', function () {
      var collapsed = toc.classList.toggle('is-collapsed');
      fold.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
    });

    function highlight() {
      var vTop = (window.scrollY || window.pageYOffset || 0) + 160;
      var current = pairs[0];
      for (var i = 0; i < pairs.length; i++) {
        var top = pairs[i].el.getBoundingClientRect().top + (window.scrollY || window.pageYOffset || 0);
        if (top <= vTop) current = pairs[i]; else break;
      }
      pairs.forEach(function (p) { p.a.classList.remove('is-current'); });
      if (current) current.a.classList.add('is-current');
    }
    var tocTick = false;
    window.addEventListener('scroll', function () {
      if (!tocTick) { tocTick = true; window.requestAnimationFrame(function () { tocTick = false; highlight(); }); }
    }, { passive: true });
    highlight();
  }

  /* ---------- 5. 小屏抽屉 ---------- */
  function initDrawer() {
    var toc = document.querySelector('nav.toc');
    if (!toc) return;
    if (!toc.id) toc.id = 'xc-toc';
    var mqSmall = window.matchMedia ? window.matchMedia('(max-width: 1024px)') : null;
    function isSmall() { return mqSmall ? mqSmall.matches : window.innerWidth <= 1024; }

    var fab = document.createElement('button');
    fab.className = 'toc-fab'; fab.type = 'button';
    fab.setAttribute('aria-label', '目录'); fab.setAttribute('title', '目录');
    fab.setAttribute('aria-expanded', 'false'); fab.setAttribute('aria-controls', toc.id);
    fab.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 6h16v2H4V6zm0 5h16v2H4v-2zm0 5h10v2H4v-2z"/></svg>';
    document.body.appendChild(fab);

    var backdrop = document.createElement('button');
    backdrop.className = 'toc-backdrop'; backdrop.type = 'button';
    backdrop.setAttribute('aria-label', '关闭目录');
    document.body.appendChild(backdrop);

    function setOpen(open) {
      if (!isSmall()) open = false;
      document.documentElement.classList.toggle('toc-drawer-open', open);
      fab.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (isSmall()) toc.setAttribute('aria-hidden', open ? 'false' : 'true');
      else toc.removeAttribute('aria-hidden');
    }
    fab.addEventListener('click', function () {
      setOpen(!document.documentElement.classList.contains('toc-drawer-open'));
    });
    backdrop.addEventListener('click', function () { setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.documentElement.classList.contains('toc-drawer-open')) {
        setOpen(false);
        try { fab.focus(); } catch (e2) { /* noop */ }
      }
    });
    toc.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
      if (a && isSmall()) setOpen(false);
    });
    function onResize() {
      if (!isSmall()) { setOpen(false); toc.removeAttribute('aria-hidden'); }
      else if (!document.documentElement.classList.contains('toc-drawer-open')) toc.setAttribute('aria-hidden', 'true');
    }
    onResize();
    if (mqSmall && mqSmall.addEventListener) mqSmall.addEventListener('change', onResize);
    window.addEventListener('resize', onResize);
  }

  /* ---------- 6. 站内搜索 ---------- */
  function initSearch() {
    var input = document.getElementById('siteSearch');
    var box = document.getElementById('searchResults');
    var data = window.XC_SEARCH || [];
    if (!input || !box) return;
    var active = -1, shown = [];

    function close() { box.hidden = true; box.innerHTML = ''; shown = []; active = -1; input.setAttribute('aria-expanded', 'false'); }
    function go(item) {
      if (!item) return;
      window.location.href = item.p + (item.a ? '#' + item.a : '');
      close();
    }
    function paint(list) {
      shown = list; active = -1;
      if (!list.length) {
        box.innerHTML = '<div class="search-empty">没有匹配的章节，试试「口径」「测评」「迁移」</div>';
        box.hidden = false; input.setAttribute('aria-expanded', 'true'); return;
      }
      box.innerHTML = list.map(function (it, i) {
        return '<a class="search-result" data-i="' + i + '" href="' + it.p + (it.a ? '#' + it.a : '') + '">'
          + it.t + '<span class="sr-doc">' + it.d + (it.a ? ' · 章节' : ' · 文档') + '</span></a>';
      }).join('');
      box.hidden = false; input.setAttribute('aria-expanded', 'true');
      Array.prototype.forEach.call(box.querySelectorAll('.search-result'), function (a) {
        a.addEventListener('mousedown', function (e) { e.preventDefault(); go(shown[Number(a.getAttribute('data-i'))]); });
      });
    }
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      if (!q) { close(); return; }
      var hits = [];
      for (var i = 0; i < data.length && hits.length < 8; i++) {
        if (data[i].t.toLowerCase().indexOf(q) !== -1 || data[i].d.toLowerCase().indexOf(q) !== -1) hits.push(data[i]);
      }
      paint(hits);
    });
    input.addEventListener('keydown', function (e) {
      if (box.hidden || !shown.length) {
        if (e.key === 'Escape') close();
        return;
      }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        active = (active + (e.key === 'ArrowDown' ? 1 : -1) + shown.length) % shown.length;
        Array.prototype.forEach.call(box.querySelectorAll('.search-result'), function (a, i) {
          a.classList.toggle('is-active', i === active);
        });
      } else if (e.key === 'Enter') {
        e.preventDefault(); go(shown[active >= 0 ? active : 0]);
      } else if (e.key === 'Escape') { close(); }
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest || !e.target.closest('.search-box')) close();
    });
  }

  function boot() { initToc(); initDrawer(); initSearch(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
