/**
 * 主题同步初始化（须在 design-system.css 之前加载，防闪白）
 * localStorage['kb-color-theme'] = light | dark | system
 * - light/dark：写入 html[data-theme]
 * - system：移除 data-theme，交给 CSS prefers-color-scheme
 * 同时注入全站主题切换器；缓存 Mermaid 源码并在换肤时可靠重绘
 */
(function () {
  'use strict';
  var KEY = 'kb-color-theme';
  var MERMAID_SRC = 'data-kb-mermaid-src';
  var _mermaidRefreshTimer = null;

  /* 偏蓝文档风：浅色 / 深色各一套（theme: base + themeVariables） */
  var MERMAID_VARS_LIGHT = {
    darkMode: false,
    background: '#f8fafc',
    primaryColor: '#dbeafe',
    primaryTextColor: '#1e3a5f',
    primaryBorderColor: '#3b82f6',
    secondaryColor: '#eff6ff',
    tertiaryColor: '#f1f5f9',
    lineColor: '#64748b',
    textColor: '#1e293b',
    mainBkg: '#dbeafe',
    nodeBorder: '#3b82f6',
    clusterBkg: '#eff6ff',
    clusterBorder: '#93c5fd',
    titleColor: '#1d4ed8',
    edgeLabelBackground: '#f8fafc',
    actorBkg: '#dbeafe',
    actorBorder: '#3b82f6',
    actorTextColor: '#1e3a5f',
    actorLineColor: '#60a5fa',
    signalColor: '#334155',
    signalTextColor: '#1e293b',
    labelBoxBkgColor: '#eff6ff',
    labelBoxBorderColor: '#93c5fd',
    labelTextColor: '#1e3a5f',
    loopTextColor: '#1e3a5f',
    noteBkgColor: '#fef9c3',
    noteTextColor: '#713f12',
    noteBorderColor: '#facc15',
    activationBkgColor: '#bfdbfe',
    activationBorderColor: '#2563eb',
    sequenceNumberColor: '#ffffff',
    fontFamily: 'ui-sans-serif, system-ui, sans-serif',
  };
  var MERMAID_VARS_DARK = {
    darkMode: true,
    background: '#0f1419',
    primaryColor: '#1e3a5f',
    primaryTextColor: '#e2e8f0',
    primaryBorderColor: '#60a5fa',
    secondaryColor: '#1a2332',
    tertiaryColor: '#152033',
    lineColor: '#94a3b8',
    textColor: '#e2e8f0',
    mainBkg: '#1e3a5f',
    nodeBorder: '#60a5fa',
    clusterBkg: '#152033',
    clusterBorder: '#3b82f6',
    titleColor: '#93c5fd',
    edgeLabelBackground: '#1a2332',
    actorBkg: '#1e3a5f',
    actorBorder: '#60a5fa',
    actorTextColor: '#e2e8f0',
    actorLineColor: '#60a5fa',
    signalColor: '#cbd5e1',
    signalTextColor: '#e2e8f0',
    labelBoxBkgColor: '#1a2332',
    labelBoxBorderColor: '#3b82f6',
    labelTextColor: '#e2e8f0',
    loopTextColor: '#e2e8f0',
    noteBkgColor: '#422006',
    noteTextColor: '#fde68a',
    noteBorderColor: '#fbbf24',
    activationBkgColor: '#1e40af',
    activationBorderColor: '#60a5fa',
    sequenceNumberColor: '#0f1419',
    fontFamily: 'ui-sans-serif, system-ui, sans-serif',
  };

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

  function mermaidConfig(extra) {
    // 页面 initialize 调用时再兜底缓存一次（保证早于 startOnLoad 渲染）
    try {
      snapshotMermaidSources();
    } catch (e0) {}
    var dark = resolvedTheme(readPref()) === 'dark';
    var cfg = {
      startOnLoad: false,
      theme: 'base',
      themeVariables: dark ? MERMAID_VARS_DARK : MERMAID_VARS_LIGHT,
      securityLevel: 'loose',
      flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' },
      sequence: { useMaxWidth: true, mirrorActors: false },
    };
    if (extra && typeof extra === 'object') {
      Object.keys(extra).forEach(function (k) {
        if (k === 'flowchart' || k === 'sequence') {
          cfg[k] = Object.assign({}, cfg[k] || {}, extra[k] || {});
        } else if (k === 'themeVariables') {
          cfg.themeVariables = Object.assign({}, cfg.themeVariables, extra.themeVariables);
        } else {
          cfg[k] = extra[k];
        }
      });
    }
    return cfg;
  }

  /** 在首次渲染前缓存源码；已渲染节点若无缓存则跳过 */
  function snapshotMermaidSources() {
    var nodes = document.querySelectorAll('.mermaid');
    Array.prototype.forEach.call(nodes, function (el) {
      if (el.getAttribute(MERMAID_SRC)) return;
      if (el.getAttribute('data-processed')) return;
      var src = el.textContent;
      if (src && src.replace(/\s+/g, '').length) {
        el.setAttribute(MERMAID_SRC, src);
      }
    });
  }

  function restoreMermaidSources() {
    var nodes = document.querySelectorAll('.mermaid');
    Array.prototype.forEach.call(nodes, function (el) {
      var src = el.getAttribute(MERMAID_SRC);
      if (!src) return;
      el.removeAttribute('data-processed');
      el.removeAttribute('data-mermaid-id');
      el.removeAttribute('data-diagram-type');
      // 清掉上次渲染生成的 id，避免冲突
      if (el.id && String(el.id).indexOf('mermaid') === 0) {
        el.removeAttribute('id');
      }
      el.innerHTML = '';
      el.textContent = src;
    });
  }

  function refreshMermaid() {
    if (!window.mermaid) return;
    snapshotMermaidSources();
    restoreMermaidSources();
    var cfg = mermaidConfig({ startOnLoad: false });
    try {
      window.mermaid.initialize(cfg);
    } catch (e) {}
    try {
      if (typeof window.mermaid.run === 'function') {
        return window.mermaid.run({ querySelector: '.mermaid' });
      }
      if (typeof window.mermaid.init === 'function') {
        window.mermaid.init(undefined, document.querySelectorAll('.mermaid'));
      }
    } catch (e2) {
      /* 失败则下次刷新生效 */
    }
  }

  function scheduleMermaidRefresh() {
    if (_mermaidRefreshTimer) clearTimeout(_mermaidRefreshTimer);
    _mermaidRefreshTimer = setTimeout(function () {
      _mermaidRefreshTimer = null;
      refreshMermaid();
    }, 40);
  }

  window.kbTheme = {
    KEY: KEY,
    readPref: readPref,
    apply: apply,
    resolved: function () {
      return resolvedTheme(readPref());
    },
    /** @deprecated 兼容旧页：统一走 base + 偏蓝变量 */
    mermaidTheme: function () {
      return 'base';
    },
    mermaidConfig: mermaidConfig,
    snapshotMermaid: snapshotMermaidSources,
    refreshMermaid: scheduleMermaidRefresh,
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
      // 只 cycle；重绘统一由 kb-theme-change 触发，避免双重 run 破坏图
      window.kbTheme.cycle();
    });
    document.body.appendChild(btn);
    try {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var onChange = function () {
        if (readPref() !== 'system') return;
        scheduleMermaidRefresh();
      };
      if (mq.addEventListener) mq.addEventListener('change', onChange);
      else if (mq.addListener) mq.addListener(onChange);
    } catch (e3) {}
    document.addEventListener('kb-theme-change', function () {
      paint();
      scheduleMermaidRefresh();
    });
  }

  function boot() {
    // 尽早缓存源码（须早于各页 mermaid.initialize startOnLoad）
    snapshotMermaidSources();
    if (document.body) initThemeToggle();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
