/**
 * Java 架构师面试问答 — 导航交互逻辑
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

  // ---------- 初始化 ----------
  function init() {
    initBackToTop();
    initReadingProgress();
    initTocHighlight();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
