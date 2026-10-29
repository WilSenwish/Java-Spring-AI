/* java-design-patterns-principles/assets/app.js
   复用自 Software-Engineering-Laws-Theories-Principles-and-Patterns/assets/app.js（长官要求「导航参考 Laws」）。
   职责：
   1) 绑定顶部 toolbar 的「↑ 顶部」按钮 → 平滑回顶；
   2) 绑定顶部 toolbar 的「主题切换」按钮 → 复用 theme-init.js 暴露的 window.kbTheme.cycle()
      （浅→深→系统 三态，单一状态源），并随 kb-theme-change 事件同步按钮文案。
   依赖：theme-init.js（已在 <head> 同步引入，先于本文件注册 window.kbTheme）。 */
(function(){
  var b = document.getElementById('topBtn');
  if (b) b.addEventListener('click', function(){ window.scrollTo({ top:0, behavior:'smooth' }); });

  // 顶部 toolbar 主题切换按钮：图标+文字，复用 window.kbTheme.cycle()（浅→深→系统 三态，单一状态源）
  var tbtn = document.getElementById('themeBtn');
  var LABELS = { light:{i:'☀',t:'浅色'}, dark:{i:'☾',t:'深色'}, system:{i:'◐',t:'系统'} };
  function paintThemeBtn(){
    if (!tbtn || !window.kbTheme) return;
    var pref = window.kbTheme.readPref();
    var m = LABELS[pref] || LABELS.system;
    tbtn.innerHTML = m.i + ' ' + m.t;
  }
  if (tbtn) {
    tbtn.addEventListener('click', function(){ if (window.kbTheme) window.kbTheme.cycle(); });
    paintThemeBtn();
    document.addEventListener('kb-theme-change', paintThemeBtn);
  }
})();

/* ---------- 目录增强：滚动高亮当前章节 + 折叠/展开（适配扁平目录） ---------- */
(function () {
  function initTocEnhancements() {
    if (!document.body) return;
    var toc = document.querySelector('nav.toc');
    if (!toc || window.__satTocEnhBound) return;
    window.__satTocEnhBound = true;

    var isCore = !!toc.querySelector('ol');
    var links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
    if (!links.length) return;

    var pairs = links.map(function (a) {
      var id = a.getAttribute('href').slice(1);
      return { a: a, target: id ? document.getElementById(id) : null };
    }).filter(function (p) { return p.target; });
    if (!pairs.length) return;

    /* ---- 折叠 / 展开 ---- */
    var toggle = isCore ? toc.querySelector('h3') : null;
    if (!toggle) {
      toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'toc-fold-toggle';
      toggle.textContent = '目录';
      var w = toc.querySelector('.wrap');
      if (w) w.insertBefore(toggle, w.firstChild);
    }
    if (toggle) {
      toggle.classList.add('toc-fold-toggle');
      if (isCore) toggle.setAttribute('role', 'button');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.addEventListener('click', function (e) {
        e.preventDefault();
        var collapsed = toc.classList.toggle('is-collapsed');
        toggle.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
      });
    }
    /* 点击目录条目跳转后展开（移动端抽屉关闭 + 折叠展开，便于看到落点） */
    toc.addEventListener('click', function (e) {
      var link = e.target.closest('a[href^="#"]');
      if (!link || link === toggle || !toc.contains(link)) return;
      toc.classList.remove('is-collapsed');
      if (toggle) toggle.setAttribute('aria-expanded', 'true');
    });

    /* ---- 滚动高亮（scroll-spy） ---- */
    var ticking = false;
    function update() {
      ticking = false;
      var vTop = (window.scrollY || window.pageYOffset || 0) + 140;
      var current = pairs[0];
      for (var i = 0; i < pairs.length; i++) {
        var docTop = pairs[i].target.getBoundingClientRect().top +
                     (window.scrollY || window.pageYOffset || 0);
        if (docTop <= vTop) current = pairs[i]; else break;
      }
      if (!current) current = pairs[0];
      pairs.forEach(function (p) { p.a.classList.remove('is-current'); });
      current.a.classList.add('is-current');
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTocEnhancements);
  } else {
    initTocEnhancements();
  }
})();

/* ---------- 小屏目录抽屉（与 java-architect-interview 同机制：左下 FAB + 左侧抽屉） ---------- */
(function () {
  function initMobileTocDrawer() {
    if (!document.body) return;
    var toc = document.querySelector('nav.toc') || document.querySelector('.sidebar-toc');
    if (!toc) return;
    if (window.__satTocDrawerBound) return;
    window.__satTocDrawerBound = true;

    var mq = null;
    try { mq = window.matchMedia('(max-width: 1024px)'); } catch (e0) { mq = null; }
    function isMobile() { return mq ? mq.matches : window.innerWidth <= 1024; }

    var fab = document.querySelector('.toc-fab');
    if (!fab) {
      fab = document.createElement('button');
      fab.className = 'toc-fab';
      fab.type = 'button';
      fab.setAttribute('aria-label', '目录');
      fab.setAttribute('title', '目录');
      fab.setAttribute('aria-expanded', 'false');
      fab.setAttribute('aria-controls', 'sat-toc');
      fab.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M4 6h16v2H4V6zm0 5h16v2H4v-2zm0 5h10v2H4v-2z"/></svg>';
      document.body.appendChild(fab);
    }
    if (!toc.id) toc.id = 'sat-toc';

    var backdrop = document.querySelector('.toc-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('button');
      backdrop.className = 'toc-backdrop';
      backdrop.type = 'button';
      backdrop.setAttribute('aria-label', '关闭目录');
      document.body.appendChild(backdrop);
    }

    function setOpen(open) {
      if (!isMobile()) open = false;
      document.documentElement.classList.toggle('toc-drawer-open', open);
      fab.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (isMobile()) toc.setAttribute('aria-hidden', open ? 'false' : 'true');
      else toc.removeAttribute('aria-hidden');
    }
    function toggle() {
      setOpen(!document.documentElement.classList.contains('toc-drawer-open'));
    }

    fab.addEventListener('click', function (e) { e.preventDefault(); toggle(); });
    backdrop.addEventListener('click', function () { setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      if (!document.documentElement.classList.contains('toc-drawer-open')) return;
      setOpen(false);
      try { fab.focus(); } catch (e3) {}
    });
    toc.addEventListener('click', function (e) {
      if (!isMobile()) return;
      var link = e.target.closest('a[href^="#"]');
      if (link && toc.contains(link)) setOpen(false);
    });
    function onViewportChange() {
      if (!isMobile()) {
        setOpen(false);
        toc.removeAttribute('aria-hidden');
      } else if (!document.documentElement.classList.contains('toc-drawer-open')) {
        toc.setAttribute('aria-hidden', 'true');
      }
    }
    onViewportChange();
    if (mq) {
      if (mq.addEventListener) mq.addEventListener('change', onViewportChange);
      else if (mq.addListener) mq.addListener(onViewportChange);
    }
    window.addEventListener('resize', onViewportChange);
  }
  initMobileTocDrawer();
})();
