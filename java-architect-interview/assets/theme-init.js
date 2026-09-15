/**
 * 主题同步初始化（须在 design-system.css 之前加载，防闪白）
 * localStorage['kb-color-theme'] = light | dark | system
 * - light/dark：写入 html[data-theme]
 * - system：移除 data-theme，交给 CSS prefers-color-scheme
 * 同时注入全站主题切换器（不依赖 nav.js，保证根 index / 导图页也可切换）
 */
(function () {
  'use strict';
  var KEY = 'kb-color-theme';
  function systemDark() {
    try {
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    } catch (e) {
      return false;
    }
  }
  function readPref() {
    try {
      var v = localStorage.getItem(KEY);
      if (v === 'light' || v === 'dark' || v === 'system') return v;
    } catch (e) {}
    return 'system';
  }
  function apply(pref) {
    var root = document.documentElement;
    if (pref === 'light' || pref === 'dark') {
      root.setAttribute('data-theme', pref);
    } else {
      root.removeAttribute('data-theme');
    }
    root.setAttribute('data-theme-pref', pref);
  }
  function resolvedTheme(pref) {
    if (pref === 'light' || pref === 'dark') return pref;
    return systemDark() ? 'dark' : 'light';
  }
  function refreshMermaid(resolved) {
    if (!window.mermaid) return;
    var theme = resolved === 'dark' ? 'dark' : 'neutral';
    try {
      window.mermaid.initialize({
        startOnLoad: false,
        theme: theme,
        securityLevel: 'loose',
        flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' },
      });
    } catch (e) {}
    var nodes = document.querySelectorAll('.mermaid');
    if (!nodes.length) return;
    Array.prototype.forEach.call(nodes, function (el) {
      if (el.getAttribute('data-processed')) {
        el.removeAttribute('data-processed');
      }
    });
    try {
      if (typeof window.mermaid.run === 'function') {
        window.mermaid.run({ querySelector: '.mermaid' });
      } else if (typeof window.mermaid.init === 'function') {
        window.mermaid.init(undefined, nodes);
      }
    } catch (e2) {
      /* 重绘失败则下次刷新生效 */
    }
  }
  window.kbTheme = {
    KEY: KEY,
    readPref: readPref,
    apply: apply,
    resolved: function () {
      return resolvedTheme(readPref());
    },
    mermaidTheme: function () {
      return resolvedTheme(readPref()) === 'dark' ? 'dark' : 'neutral';
    },
    cycle: function () {
      var cur = readPref();
      var next = cur === 'light' ? 'dark' : cur === 'dark' ? 'system' : 'light';
      try {
        localStorage.setItem(KEY, next);
      } catch (e) {}
      apply(next);
      try {
        document.dispatchEvent(
          new CustomEvent('kb-theme-change', {
            detail: { pref: next, resolved: resolvedTheme(next) },
          })
        );
      } catch (e2) {}
      return next;
    },
  };
  apply(readPref());

  function initThemeToggle() {
    if (document.querySelector('.theme-toggle')) return;
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
      var pref = readPref();
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
      refreshMermaid(resolvedTheme(readPref()));
    });
    document.body.appendChild(btn);
    try {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var onChange = function () {
        if (readPref() !== 'system') return;
        refreshMermaid(resolvedTheme('system'));
      };
      if (mq.addEventListener) mq.addEventListener('change', onChange);
      else if (mq.addListener) mq.addListener(onChange);
    } catch (e3) {}
    document.addEventListener('kb-theme-change', function (ev) {
      paint();
      if (ev && ev.detail) refreshMermaid(ev.detail.resolved);
    });
  }

  function bootToggle() {
    if (!document.body) return;
    initThemeToggle();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootToggle);
  } else {
    bootToggle();
  }
})();
