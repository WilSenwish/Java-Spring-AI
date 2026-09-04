/**
 * Java 工程能力知识库 — 导航交互逻辑
 * 功能：TOC 高亮、返回顶部、阅读进度条
 */
(function () {
  'use strict';

  // ---------- 返回顶部 ----------
  function initBackToTop() {
    var btn = document.createElement('button');
    btn.className = 'back-to-top';
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

  // ---------- TOC 高亮当前题号 ----------
  function initTocHighlight() {
    var tocLinks = document.querySelectorAll('.sidebar-toc a');
    if (tocLinks.length === 0) return;

    var cards = document.querySelectorAll('.qa-card');
    if (cards.length === 0) return;

    function updateActive() {
      var scrollPos = window.scrollY + 120;
      var activeCard = null;

      for (var i = 0; i < cards.length; i++) {
        if (cards[i].offsetTop <= scrollPos) {
          activeCard = cards[i];
        }
      }

      // 按 href 锚点与卡片 id 精确匹配，避免 TOC 链接数与卡片数不一致时按索引错位
      var activeId = activeCard ? activeCard.id : '';

      tocLinks.forEach(function (link) {
        var href = link.getAttribute('href');
        var isActive = href === '#' + activeId;
        if (isActive) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    }

    window.addEventListener('scroll', updateActive);
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

  // ---------- 初始化 ----------
  function init() {
    initBackToTop();
    initReadingProgress();
    initTocHighlight();
    initTableCards();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
