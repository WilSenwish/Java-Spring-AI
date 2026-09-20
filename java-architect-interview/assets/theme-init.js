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
    /* cScale 系列：思维导图分支底色/连线/标签色。
       不显式定义时 Mermaid 会用 base 主题的默认紫蓝调色板（如 #6a5ffb），
       配本主题的深藏青标签色只有 2.54:1（不可读）——必须显式接管。 */
    cScale0: '#dbeafe',
    cScale1: '#fef3c7',
    cScale2: '#dcfce7',
    cScale3: '#ede9fe',
    cScale4: '#fee2e2',
    cScale5: '#cffafe',
    cScale6: '#f3e8ff',
    cScale7: '#fef9c3',
    cScale8: '#d1fae5',
    cScale9: '#ffe4e6',
    cScale10: '#e0e7ff',
    cScale11: '#e2e8f0',
    cScaleInv0: '#2563eb',
    cScaleInv1: '#d97706',
    cScaleInv2: '#059669',
    cScaleInv3: '#7c3aed',
    cScaleInv4: '#dc2626',
    cScaleInv5: '#0891b2',
    cScaleInv6: '#9333ea',
    cScaleInv7: '#ca8a04',
    cScaleInv8: '#10b981',
    cScaleInv9: '#e11d48',
    cScaleInv10: '#4f46e5',
    cScaleInv11: '#64748b',
    /* 思维导图根节点走 git0 / gitBranchLabel0（非 cScale） */
    git0: '#bfdbfe',
    gitBranchLabel0: '#1e3a5f',
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
    /* cScale 系列：深底版分支底色（与浅色同色相，仅降明度、提对比） */
    cScale0: '#1e3a5f',
    cScale1: '#3d3312',
    cScale2: '#14402b',
    cScale3: '#2a2255',
    cScale4: '#4b1a1d',
    cScale5: '#0e3a44',
    cScale6: '#341d4d',
    cScale7: '#3b3708',
    cScale8: '#0f3d33',
    cScale9: '#4a1c24',
    cScale10: '#1e2a5c',
    cScale11: '#26313f',
    cScaleInv0: '#60a5fa',
    cScaleInv1: '#fbbf24',
    cScaleInv2: '#34d399',
    cScaleInv3: '#a78bfa',
    cScaleInv4: '#f87171',
    cScaleInv5: '#22d3ee',
    cScaleInv6: '#c084fc',
    cScaleInv7: '#facc15',
    cScaleInv8: '#34d399',
    cScaleInv9: '#fb7185',
    cScaleInv10: '#818cf8',
    cScaleInv11: '#94a3b8',
    /* 思维导图根节点走 git0 / gitBranchLabel0（非 cScale） */
    git0: '#24406b',
    gitBranchLabel0: '#e2e8f0',
    fontFamily: 'ui-sans-serif, system-ui, sans-serif',
  };

  /* cScaleLabel：分支标签文字色（不定义则回落 labelTextColor） */
  for (var _ci = 0; _ci < 12; _ci++) {
    MERMAID_VARS_LIGHT['cScaleLabel' + _ci] = '#1e3a5f';
    MERMAID_VARS_DARK['cScaleLabel' + _ci] = '#e2e8f0';
  }

  /* ---------- 图表内联配色「深色重着色」 ----------
   * 背景：Mermaid 的 `style X fill:#dbeafe` 指令会被渲染成元素上的内联
   *   fill:#dbeafe !important
   * 样式表里的 !important 压不过内联 !important（实测两种特异性皆败），
   * 只能在渲染完成后改写 style 属性本身。浅色画布若原样保留，会变成
   * 「浅底 + 近白字」，对比度 1.0 —— 文字事实上不可见。
   * 故按「同色相、降明度」映射为深底，浅色文字即可读（对比度 9:1 以上）；
   * 少数饱和实色配白字的节点则压暗明度，保住白字。 */
  var RETINT_ATTR = 'data-kb-orig-style';
  var RETINT_FILL_DARK = {
    '#dbeafe': '#1e3a5f',
    '#fef3c7': '#3d3312',
    '#dcfce7': '#14402b',
    '#d1fae5': '#0f3d33',
    '#fee2e2': '#4b1a1d',
    '#ffe4e6': '#4a1c24',
    '#ede9fe': '#2a2255',
    '#f3e8ff': '#341d4d',
    '#e0e7ff': '#1e2a5c',
    '#f0f3f7': '#232e40',
    '#e2e8f0': '#26313f',
    '#e5e7eb': '#2a323d',
    '#e1f5fe': '#123a47',
    '#fff3e0': '#46301a',
    '#e8f5e9': '#1d3b22',
    '#4a90d9': '#2f5f96',
    '#7b68ee': '#4f3fb0',
    '#ff6b35': '#a5431f',
    '#e74c3c': '#9e2f26',
    '#f39c12': '#8a5a09',
    '#9b59b6': '#6a3a7f',
  };
  var RETINT_STROKE_DARK = {
    '#2563eb': '#60a5fa',
    '#d97706': '#fbbf24',
    '#059669': '#34d399',
    '#dc2626': '#f87171',
    '#7c3aed': '#a78bfa',
    '#e11d48': '#fb7185',
    '#4f46e5': '#818cf8',
    '#6b7280': '#94a3b8',
    '#475569': '#94a3b8',
    '#64748b': '#94a3b8',
    '#9ca3af': '#cbd5e1',
  };
  var RETINT_DECL = /(^|;)\s*(fill|stroke)\s*:\s*(#[0-9a-fA-F]{3,8})\s*(!important)?/g;

  function remapStyle(orig, dark) {
    if (!dark) return orig;
    return orig.replace(RETINT_DECL, function (all, sep, prop, hex, imp) {
      var map = prop.toLowerCase() === 'fill' ? RETINT_FILL_DARK : RETINT_STROKE_DARK;
      var to = map[hex.toLowerCase()];
      if (!to) return all;
      return sep + prop + ':' + to + (imp ? ' !important' : '');
    });
  }

  /** 只在「确实需要改写」时记录原始值，便于换回浅色时还原 */
  function retintMermaidShapes(dark) {
    var nodes = document.querySelectorAll('.mermaid svg [style]');
    Array.prototype.forEach.call(nodes, function (el) {
      var cur = el.getAttribute('style');
      if (!cur || !/fill\s*:|stroke\s*:/.test(cur)) return;
      if (!el.hasAttribute(RETINT_ATTR)) el.setAttribute(RETINT_ATTR, cur);
      var orig = el.getAttribute(RETINT_ATTR);
      var next = remapStyle(orig, dark);
      if (next !== cur) el.setAttribute('style', next);
    });
  }

  function applyMermaidRetint() {
    retintMermaidShapes(resolvedTheme(readPref()) === 'dark');
  }

  var _retintTimer = null;
  function scheduleMermaidRetint() {
    if (_retintTimer) clearTimeout(_retintTimer);
    _retintTimer = setTimeout(function () {
      _retintTimer = null;
      applyMermaidRetint();
    }, 50);
  }

  /** 只监听 childList：Mermaid 插入 <svg> 时触发；本函数自身的 style 改写不会回环触发 */
  var _retintObserver = null;
  function startMermaidRetintWatcher() {
    if (!window.MutationObserver || !document.body || _retintObserver) return;
    _retintObserver = new MutationObserver(function (records) {
      for (var i = 0; i < records.length; i++) {
        var added = records[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var n = added[j];
          if (n.nodeType !== 1) continue;
          if (n.tagName.toLowerCase() === 'svg' || (n.querySelector && n.querySelector('svg'))) {
            scheduleMermaidRetint();
            return;
          }
        }
      }
    });
    _retintObserver.observe(document.body, { childList: true, subtree: true });
  }

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
    scheduleMermaidRetint();
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
    /** 深色下把图表内联浅色重着色为深底；换肤后由 kb-theme-change 自动触发 */
    retint: applyMermaidRetint,
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

  function initScrollJumpButtons() {
    if (!document.body) return;

    function ensureTop() {
      if (document.querySelector('.back-to-top')) return null;
      var btn = document.createElement('button');
      btn.className = 'back-to-top';
      btn.type = 'button';
      btn.innerHTML = '&#8593;';
      btn.setAttribute('aria-label', '返回顶部');
      btn.setAttribute('title', '返回顶部');
      document.body.appendChild(btn);
      btn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
      return btn;
    }

    function ensureBottom() {
      if (document.querySelector('.go-to-bottom')) return null;
      var btn = document.createElement('button');
      btn.className = 'go-to-bottom';
      btn.type = 'button';
      btn.innerHTML = '&#8595;';
      btn.setAttribute('aria-label', '去到底部');
      btn.setAttribute('title', '去到底部');
      document.body.appendChild(btn);
      btn.addEventListener('click', function () {
        window.scrollTo({
          top: document.documentElement.scrollHeight,
          behavior: 'smooth',
        });
      });
      return btn;
    }

    var topBtn = ensureTop() || document.querySelector('.back-to-top');
    var bottomBtn = ensureBottom() || document.querySelector('.go-to-bottom');
    if (!topBtn && !bottomBtn) return;

    function update() {
      var y = window.scrollY || window.pageYOffset || 0;
      var remain =
        document.documentElement.scrollHeight - y - window.innerHeight;
      if (topBtn) {
        if (y > 400) topBtn.classList.add('visible');
        else topBtn.classList.remove('visible');
      }
      if (bottomBtn) {
        if (remain > 400) bottomBtn.classList.add('visible');
        else bottomBtn.classList.remove('visible');
      }
    }

    // 避免与 nav.js 重复绑定：仅当本脚本创建了按钮时绑定；若按钮已存在也绑定一次可见性（用标记防重）
    if (!window.__kbScrollJumpBound) {
      window.__kbScrollJumpBound = true;
      window.addEventListener('scroll', update, { passive: true });
      window.addEventListener('resize', update);
    }
    update();
  }

  function boot() {
    // 尽早缓存源码（须早于各页 mermaid.initialize startOnLoad）
    snapshotMermaidSources();
    if (document.body) {
      initThemeToggle();
      initScrollJumpButtons();
      startMermaidRetintWatcher();
      scheduleMermaidRetint();
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
