/**
 * Java 工程能力知识库 — 导航交互逻辑
 * 功能：TOC 高亮、返回顶部/去到底部（兜底）、阅读进度条
 */
(function () {
  'use strict';

  // ---------- 返回顶部（由 theme-init.js 全站注入；此处兜底） ----------
  function initBackToTop() {
    if (document.querySelector('.back-to-top')) return;
    var btn = document.createElement('button');
    btn.className = 'back-to-top';
    btn.type = 'button';
    btn.innerHTML = '&#8593;';
    btn.setAttribute('aria-label', '返回顶部');
    document.body.appendChild(btn);

    window.addEventListener('scroll', function () {
      if (window.scrollY > 400) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    });

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ---------- 去到底部（由 theme-init.js 全站注入；此处兜底） ----------
  function initGoToBottom() {
    if (document.querySelector('.go-to-bottom')) return;
    var btn = document.createElement('button');
    btn.className = 'go-to-bottom';
    btn.type = 'button';
    btn.innerHTML = '&#8595;';
    btn.setAttribute('aria-label', '去到底部');
    document.body.appendChild(btn);

    function update() {
      var remain =
        document.documentElement.scrollHeight - window.scrollY - window.innerHeight;
      if (remain > 400) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }
    window.addEventListener('scroll', update);
    window.addEventListener('resize', update);
    update();

    btn.addEventListener('click', function () {
      window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: 'smooth',
      });
    });
  }

  // ---------- 阅读进度条 ----------
  function initReadingProgress() {
    var bar = document.createElement('div');
    bar.className = 'reading-progress';
    bar.style.width = '0%';
    document.body.appendChild(bar);

    window.addEventListener('scroll', function () {
      var scrollTop = window.scrollY;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      var progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      bar.style.width = progress + '%';
    });
  }

  // ---------- TOC 高亮当前条目（卡片 / 分组 / 章节标题） ----------
  function initTocHighlight() {
    var tocLinks = Array.prototype.slice.call(
      document.querySelectorAll('.sidebar-toc a[href^="#"]')
    );
    if (tocLinks.length === 0) return;

    // 以侧栏 href 为准解析目标，兼容 qa-card、epq 分组、安全手册 h2 等
    var targets = [];
    var seen = {};
    tocLinks.forEach(function (link) {
      var href = link.getAttribute('href') || '';
      if (href.length < 2) return;
      var id = href.slice(1);
      if (seen[id]) return;
      var el = document.getElementById(id);
      if (!el) return;
      seen[id] = true;
      targets.push({ id: id, el: el, link: link });
    });
    if (targets.length === 0) return;

    targets.sort(function (a, b) {
      if (a.el.compareDocumentPosition(b.el) & Node.DOCUMENT_POSITION_FOLLOWING) {
        return -1;
      }
      return 1;
    });

    var sidebar = document.querySelector('.sidebar-toc');
    var ticking = false;

    function updateActive() {
      var scrollPos = window.scrollY + 120;
      var active = null;

      for (var i = 0; i < targets.length; i++) {
        var top =
          targets[i].el.getBoundingClientRect().top + window.scrollY;
        if (top <= scrollPos) {
          active = targets[i];
        }
      }

      tocLinks.forEach(function (link) {
        link.classList.remove('active');
      });

      if (active) {
        active.link.classList.add('active');
        // 分组标题同步高亮：当前条目所属 toc-group 的标题一并 active
        var group = active.link.closest('.toc-group');
        if (group) {
          var groupTitle = group.querySelector('a.toc-group-title');
          if (groupTitle) {
            groupTitle.classList.add('active');
          }
        }
        // 侧栏内跟随，避免长目录下高亮项滚出可视区
        if (sidebar) {
          var linkRect = active.link.getBoundingClientRect();
          var sideRect = sidebar.getBoundingClientRect();
          if (
            linkRect.top < sideRect.top + 8 ||
            linkRect.bottom > sideRect.bottom - 8
          ) {
            active.link.scrollIntoView({ block: 'nearest', inline: 'nearest' });
          }
        }
      }
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        updateActive();
        ticking = false;
      });
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    updateActive();
  }

  // ---------- 小屏表格纵向卡片化：注入列名 data-label ----------
  // 仅处理结构规整的 compare-table（行列数齐整、无合并单元格）；
  // 不规则表格跳过，由 CSS 兜底保持横向滚动面板。
  function initTableCards() {
    // 兼容两种写法：<table class="compare-table"> 与 <div class="compare-table"><table>
    var holders = document.querySelectorAll('.compare-table');
    if (holders.length === 0) return;

    var tables = [];
    for (var i = 0; i < holders.length; i++) {
      tables.push(holders[i].tagName === 'TABLE' ? holders[i] : holders[i].querySelector('table'));
    }
    tables = tables.filter(Boolean);
    if (tables.length === 0) return;

    for (var i = 0; i < tables.length; i++) {
      var tbl = tables[i];
      var headCells = tbl.querySelectorAll('thead th');
      var bodyRows = tbl.querySelectorAll('tbody tr');
      if (headCells.length === 0 || bodyRows.length === 0) continue;

      // 结构规整性校验：每行的单元格数与表头一致，且全部为 td（排除 colspan/rowspan/行头 th）
      var regular = true;
      for (var r = 0; r < bodyRows.length && regular; r++) {
        var cells = bodyRows[r].children;
        if (cells.length !== headCells.length) { regular = false; break; }
        for (var c = 0; c < cells.length; c++) {
          if (cells[c].tagName !== 'TD') { regular = false; break; }
        }
      }
      if (!regular) continue;

      // 注入列名并标记卡片化
      for (var r2 = 0; r2 < bodyRows.length; r2++) {
        var cells2 = bodyRows[r2].children;
        for (var c2 = 0; c2 < cells2.length; c2++) {
          cells2[c2].setAttribute('data-label', headCells[c2].textContent.trim());
        }
      }
      tbl.classList.add('table-cards');
    }
  }

  // ---------- 主题切换（由 theme-init.js 注入；此处仅兜底） ----------
  function initThemeToggle() {
    if (document.querySelector('.theme-toggle')) return;
    if (!window.kbTheme || typeof window.kbTheme.cycle !== 'function') return;

    var LABELS = {
      light: { icon: '☀', text: '浅色' },
      dark: { icon: '☾', text: '深色' },
      system: { icon: '◐', text: '系统' },
    };

    var btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.type = 'button';
    btn.setAttribute('aria-label', '切换颜色主题');

    function paint() {
      var pref = window.kbTheme.readPref();
      var meta = LABELS[pref] || LABELS.system;
      btn.innerHTML =
        '<span class="theme-toggle-icon" aria-hidden="true">' +
        meta.icon +
        '</span><span>' +
        meta.text +
        '</span>';
      btn.setAttribute('title', '主题：' + meta.text + '（点击切换）');
      btn.setAttribute('data-theme-pref', pref);
    }

    paint();
    btn.addEventListener('click', function () {
      window.kbTheme.cycle();
      paint();
    });
    document.body.appendChild(btn);
    document.addEventListener('kb-theme-change', paint);
  }

  // ---------- 初始化 ----------
  function init() {
    initBackToTop();
    initGoToBottom();
    initReadingProgress();
    initThemeToggle();
    initTocHighlight();
    initTableCards();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
