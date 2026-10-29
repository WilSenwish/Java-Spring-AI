/**
 * 主题同步初始化（须在 design-system.css 之前加载，防闪白）
 * localStorage['kb-color-theme'] = light | dark | system
 * - light/dark：写入 html[data-theme]
 * - system：移除 data-theme，交给 CSS prefers-color-scheme
 * 同时注入全站主题切换器、左下「听本页」、搜索（无顶栏为右上按钮，有 .toolbar 则为顶栏搜索框）；缓存 Mermaid 源码并在换肤时可靠重绘
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
    /* 2026-10-24：D 篇 R4 导图页扩至十二域，新增四色对应浅底（青/酸橙/品红/橙 100） */
    '#cffafe': '#164e63',
    '#ecfccb': '#2a3a10',
    '#fae8ff': '#4a1d52',
    '#ffedd5': '#4a2c12',
    /* 2026-10-27：A 篇 AI 工程纵深导图页新增三色（青绿浅底/白底/青绿描边） */
    '#ccfbf1': '#0f3d38',
    '#ffffff': '#26313f',
  };
  var RETINT_STROKE_DARK = {
    '#2563eb': '#60a5fa',
    '#d97706': '#fbbf24',
    '#059669': '#34d399',
    '#dc2626': '#f87171',
    /* 2026-10-24：D 篇 R4 导图页「风控与合规」域描边（红 700），与 dc2626 同色相族 */
    '#b91c1c': '#f87171',
    '#7c3aed': '#a78bfa',
    '#e11d48': '#fb7185',
    '#4f46e5': '#818cf8',
    /* 2026-10-24：D 篇 R4 导图页扩至十二域，新增四色（青/酸橙/品红/橙） */
    '#0e7490': '#22d3ee',
    '#4d7c0f': '#a3e635',
    '#c026d3': '#e879f9',
    '#ea580c': '#fb923c',
    /* 2026-10-27：A 篇导图页青绿描边 */
    '#0f766e': '#2dd4bf',
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
      light: { icon: '☀', name: '浅色' },
      dark: { icon: '☾', name: '深色' },
      system: { icon: '◐', name: '跟随系统' },
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
        '</span>';
      btn.setAttribute('title', '主题：' + meta.name + '（点击切换）');
      btn.setAttribute('aria-label', '切换颜色主题（当前：' + meta.name + '）');
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

  /* 阅读进度（方案 A）：顶栏细条次要 + 浮动环主反馈（叠在主题切换上方） */
  var RP_CIRC = 2 * Math.PI * 17; /* 与 CSS stroke-dasharray 同步 */
  function initReadingProgress() {
    if (!document.body) return;

    var bar = document.querySelector('.reading-progress');
    if (!bar) {
      bar = document.createElement('div');
      bar.className = 'reading-progress';
      bar.style.width = '0%';
      bar.setAttribute('aria-hidden', 'true');
      document.body.appendChild(bar);
    }

    var fab = document.querySelector('.reading-progress-fab');
    if (!fab) {
      fab = document.createElement('div');
      fab.className = 'reading-progress-fab';
      fab.setAttribute('role', 'progressbar');
      fab.setAttribute('aria-label', '阅读进度');
      fab.setAttribute('aria-valuemin', '0');
      fab.setAttribute('aria-valuemax', '100');
      fab.setAttribute('aria-valuenow', '0');
      fab.innerHTML =
        '<svg class="reading-progress-fab__svg" viewBox="0 0 44 44" aria-hidden="true">' +
        '<circle class="reading-progress-fab__track" cx="22" cy="22" r="17"></circle>' +
        '<circle class="reading-progress-fab__value" cx="22" cy="22" r="17"></circle>' +
        '</svg>' +
        '<span class="reading-progress-fab__label" aria-hidden="true">0%</span>';
      document.body.appendChild(fab);
    }
    var valueEl = fab.querySelector('.reading-progress-fab__value');
    var labelEl = fab.querySelector('.reading-progress-fab__label');
    var raf = 0;
    function paint() {
      raf = 0;
      var docHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      var y = window.scrollY || window.pageYOffset || 0;
      var pct = docHeight > 0 ? Math.min(100, Math.max(0, (y / docHeight) * 100)) : 0;
      var rounded = Math.round(pct);
      bar.style.width = pct + '%';
      if (valueEl) {
        valueEl.style.strokeDasharray = String(RP_CIRC);
        valueEl.style.strokeDashoffset = String(RP_CIRC * (1 - pct / 100));
      }
      if (labelEl) labelEl.textContent = rounded + '%';
      fab.setAttribute('aria-valuenow', String(rounded));
      fab.setAttribute('title', '阅读进度 ' + rounded + '%');
    }
    function onScroll() {
      if (raf) return;
      raf = window.requestAnimationFrame(paint);
    }
    if (!window.__kbReadingProgressBound) {
      window.__kbReadingProgressBound = true;
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll);
    }
    paint();
  }

  function initScrollJumpButtons() {
    if (!document.body) return;

    function ensureTop() {
      if (document.querySelector('.back-to-top')) return null;
      var btn = document.createElement('button');
      btn.className = 'back-to-top';
      btn.type = 'button';
      /* 顶杠 + 实心三角：比细箭头 ↑ 更饱满 */
      btn.innerHTML =
        '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
        '<path fill="currentColor" d="M5 4h14v2.5H5V4zm7 4.2L19 18H5l7-9.8z"/>' +
        '</svg>';
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
      btn.innerHTML =
        '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
        '<path fill="currentColor" d="M5 17.5h14V20H5v-2.5zM12 15.8L5 6h14l-7 9.8z"/>' +
        '</svg>';
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

  /* 小屏本篇目录：左下 FAB + 复用 .sidebar-toc 左侧抽屉（≤1024） */
  function initMobileTocDrawer() {
    if (!document.body) return;
    var sidebar = document.querySelector('.sidebar-toc');
    if (!sidebar) return;
    if (window.__kbTocDrawerBound) return;
    window.__kbTocDrawerBound = true;

    var mq = null;
    try {
      mq = window.matchMedia('(max-width: 1024px)');
    } catch (e0) {
      mq = null;
    }

    function isMobile() {
      return mq ? mq.matches : window.innerWidth <= 1024;
    }

    var fab = document.querySelector('.toc-fab');
    if (!fab) {
      fab = document.createElement('button');
      fab.className = 'toc-fab';
      fab.type = 'button';
      fab.setAttribute('aria-label', '本篇目录');
      fab.setAttribute('title', '本篇目录');
      fab.setAttribute('aria-expanded', 'false');
      fab.setAttribute('aria-controls', 'kb-sidebar-toc');
      fab.innerHTML =
        '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
        '<path fill="currentColor" d="M4 6h16v2H4V6zm0 5h16v2H4v-2zm0 5h10v2H4v-2z"/>' +
        '</svg>';
      document.body.appendChild(fab);
    }

    if (!sidebar.id) sidebar.id = 'kb-sidebar-toc';

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
      if (isMobile()) {
        sidebar.setAttribute('aria-hidden', open ? 'false' : 'true');
      } else {
        sidebar.removeAttribute('aria-hidden');
      }
      if (open) {
        syncExpandedFromActive();
        var active = sidebar.querySelector('a.active');
        if (active) {
          try {
            active.scrollIntoView({ block: 'nearest', inline: 'nearest' });
          } catch (e1) {}
        }
      } else if (isMobile()) {
        try {
          fab.focus();
        } catch (e2) {}
      }
    }

    function toggle() {
      setOpen(!document.documentElement.classList.contains('toc-drawer-open'));
    }

    function syncExpandedFromActive() {
      if (!isMobile()) return;
      var groups = sidebar.querySelectorAll('.toc-group');
      if (!groups.length) return;
      var activeLink = sidebar.querySelector('a.active:not(.toc-group-title)');
      var activeGroup = activeLink ? activeLink.closest('.toc-group') : null;
      if (!activeGroup) {
        var activeTitle = sidebar.querySelector('a.toc-group-title.active');
        activeGroup = activeTitle ? activeTitle.closest('.toc-group') : null;
      }
      Array.prototype.forEach.call(groups, function (g) {
        if (g === activeGroup) g.classList.add('is-expanded');
        else g.classList.remove('is-expanded');
      });
      if (!activeGroup && groups[0]) {
        /* 无高亮时展开第一组，避免空白抽屉 */
        groups[0].classList.add('is-expanded');
      }
    }

    fab.addEventListener('click', function (e) {
      e.preventDefault();
      toggle();
    });
    backdrop.addEventListener('click', function () {
      setOpen(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      if (!document.documentElement.classList.contains('toc-drawer-open')) return;
      setOpen(false);
      try {
        fab.focus();
      } catch (e3) {}
    });

    /* 条目点击：关抽屉；分组标题：收起时先展开，已展开则跳转并关闭 */
    sidebar.addEventListener('click', function (e) {
      if (!isMobile()) return;
      var groupTitle = e.target.closest('a.toc-group-title');
      if (groupTitle) {
        var group = groupTitle.closest('.toc-group');
        if (group && !group.classList.contains('is-expanded')) {
          e.preventDefault();
          Array.prototype.forEach.call(
            sidebar.querySelectorAll('.toc-group.is-expanded'),
            function (g) {
              g.classList.remove('is-expanded');
            }
          );
          group.classList.add('is-expanded');
          return;
        }
        setOpen(false);
        return;
      }
      var link = e.target.closest('a[href^="#"]');
      if (link && sidebar.contains(link)) {
        setOpen(false);
      }
    });

    function onViewportChange() {
      if (!isMobile()) {
        setOpen(false);
        sidebar.removeAttribute('aria-hidden');
        Array.prototype.forEach.call(
          sidebar.querySelectorAll('.toc-group.is-expanded'),
          function (g) {
            g.classList.remove('is-expanded');
          }
        );
      } else if (
        !document.documentElement.classList.contains('toc-drawer-open')
      ) {
        sidebar.setAttribute('aria-hidden', 'true');
      }
    }
    /* 初始：小屏抽屉关闭时对读屏隐藏侧栏 */
    onViewportChange();
    if (mq) {
      if (mq.addEventListener) mq.addEventListener('change', onViewportChange);
      else if (mq.addListener) mq.addListener(onViewportChange);
    }
    window.addEventListener('resize', onViewportChange);

    window.kbToc = {
      open: function () {
        setOpen(true);
      },
      close: function () {
        setOpen(false);
      },
      syncExpandedFromActive: syncExpandedFromActive,
    };
  }

  /* 听本页：系统语音。样式随脚本注入（子站不加载 design-system.css）。
     浏览器禁止无手势自动出声，故默认关闭；用户点一次后记住，下次开页再尝试续读。 */
  function initPageListen() {
    if (window.__kbPageListenBound) return;
    if (!document.body || !window.speechSynthesis || typeof window.SpeechSynthesisUtterance !== 'function') return;
    var rough = (document.body.textContent || '').replace(/\s+/g, '');
    if (rough.length < 80) return;
    window.__kbPageListenBound = true;

    var AUTO_KEY = 'kb-listen-auto';
    var RATE_KEY = 'kb-listen-rate';
    var RATES = [0.85, 1, 1.15, 1.3];
    var MAX_CHUNK = 64;
    var SKIP =
      'script,style,svg,noscript,pre,.code-block,.mermaid,.mermaid-container,' +
      'nav,.sidebar-toc,.chapter-nav,.chapter-nav-top,.site-page-nav,.toolbar,.toc,' +
      '.kb-listen,.theme-toggle,.back-to-top,.go-to-bottom,.reading-progress,' +
      '.reading-progress-fab,.toc-fab,.toc-backdrop,[aria-hidden="true"]';

    var state = 'idle';
    var queue = [];
    var cursor = 0;
    var retries = 0;
    var gen = 0;
    var utteranceOpen = false;
    var spokeAt = 0;
    var suppressWatchUntil = 0;
    var currentEl = null;
    var rate = readRate();
    var cachedVoice = null;
    var chunkWatchdog = 0;
    var primed = false;
    var warnedNoVoice = false;
    var listenHintEl = null;
    var isChromium = (typeof window.chrome !== 'undefined');
    var reduceMotion = false;
    try {
      reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (eMotion) {}

    if (!document.getElementById('kb-listen-style')) {
      var style = document.createElement('style');
      style.id = 'kb-listen-style';
      style.textContent =
        '.kb-listen{position:fixed;z-index:1000;left:max(30px,env(safe-area-inset-left));bottom:30px;' +
        'display:flex;flex-direction:column;align-items:flex-start;gap:8px;' +
        'max-width:calc(100vw - 24px);pointer-events:none}' +
        '.kb-listen__btn,.kb-listen__rate,.kb-listen__stop,.kb-listen__toggle{pointer-events:auto;touch-action:manipulation;' +
        '-webkit-tap-highlight-color:transparent;font-family:inherit;cursor:pointer;' +
        'background:var(--bg2,#fff);color:var(--ink,var(--text,#1e293b));' +
        'border:1px solid var(--rule,var(--line,#e2e8f0));' +
        'box-shadow:var(--shadow-md,0 4px 12px rgba(15,23,42,.12))}' +
        '.kb-listen__btn{width:44px;height:44px;padding:0;border-radius:50%;display:flex;align-items:center;' +
        'justify-content:center;line-height:1}' +
        '.kb-listen__btn svg{width:22px;height:22px;display:block}' +
        '.kb-listen__btn:hover,.kb-listen__rate:hover,.kb-listen__stop:hover,.kb-listen__toggle:hover{border-color:var(--accent,#2563eb);color:var(--accent,#2563eb)}' +
        '.kb-listen__btn:focus-visible,.kb-listen__rate:focus-visible,.kb-listen__stop:focus-visible,.kb-listen__toggle:focus-visible{' +
        'outline:2px solid var(--accent,#2563eb);outline-offset:2px}' +
        '.kb-listen__btn[aria-pressed="true"],.kb-listen__btn.is-armed{border-color:var(--accent,#2563eb);color:var(--accent,#2563eb)}' +
        '.kb-listen__panel{display:flex;flex-wrap:wrap;gap:6px;max-width:calc(100vw - 32px)}' +
        '.kb-listen__panel[hidden]{display:none !important}' +
        '.kb-listen__rate,.kb-listen__stop,.kb-listen__toggle{min-height:36px;padding:0 10px;border-radius:999px;font-size:12px;font-weight:600}' +
        '.kb-listening{box-shadow:inset 4px 0 0 var(--accent,#2563eb)}' +
        '@media (max-width:480px){.kb-listen{left:max(16px,env(safe-area-inset-left));bottom:24px}}' +
        '@media print{.kb-listen{display:none !important}.kb-listening{box-shadow:none !important}}' +
        '.kb-listen__hint{position:absolute;bottom:56px;left:0;max-width:260px;padding:8px 12px;' +
        'border-radius:10px;font-size:12px;line-height:1.5;' +
        'background:var(--bg2,#fff);color:var(--ink,var(--text,#1e293b));' +
        'border:1px solid var(--rule,var(--line,#e2e8f0));' +
        'box-shadow:var(--shadow-md,0 4px 12px rgba(15,23,42,.12));pointer-events:none;white-space:normal}' +
        '.kb-listen__hint[hidden]{display:none !important}';
      document.head.appendChild(style);
    }

    var ICON_SPEAKER =
      '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path fill="currentColor" d="M3 8.5h4.2L14 3.5v17L7.2 15.5H3v-7z"/>' +
      '<path fill="currentColor" d="M17.34 8.02a5.2 5.2 0 0 1 0 7.96l-1.67-1.99a2.6 2.6 0 0 0 0-3.98l1.67-1.99z"/>' +
      '<path fill="currentColor" d="M19.4 5.57a8.4 8.4 0 0 1 0 12.86l-1.54-1.83a6 6 0 0 0 0-9.2l1.54-1.83z"/>' +
      '</svg>';
    var ICON_PAUSE =
      '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path fill="currentColor" d="M6 5h4v14H6V5zm8 0h4v14h-4V5z"/>' +
      '</svg>';
    var ICON_PLAY =
      '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path fill="currentColor" d="M8 5v14l11-7L8 5z"/>' +
      '</svg>';

    var root = document.createElement('div');
    root.className = 'kb-listen';
    var panel = document.createElement('div');
    panel.className = 'kb-listen__panel';
    panel.hidden = true;
    var toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'kb-listen__toggle';
    toggleBtn.textContent = '暂停';
    var rateBtn = document.createElement('button');
    rateBtn.type = 'button';
    rateBtn.className = 'kb-listen__rate';
    var stopBtn = document.createElement('button');
    stopBtn.type = 'button';
    stopBtn.className = 'kb-listen__stop';
    stopBtn.textContent = '停止';
    stopBtn.setAttribute('aria-label', '停止朗读');
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'kb-listen__btn';
    btn.setAttribute('aria-pressed', 'false');
    panel.appendChild(toggleBtn);
    panel.appendChild(rateBtn);
    panel.appendChild(stopBtn);
    root.appendChild(panel);
    root.appendChild(btn);
    document.body.appendChild(root);

    function readRate() {
      try {
        var n = parseFloat(localStorage.getItem(RATE_KEY));
        for (var i = 0; i < RATES.length; i++) {
          if (Math.abs(RATES[i] - n) < 0.01) return RATES[i];
        }
      } catch (eRate) {}
      return 1;
    }

    function rateLabel(n) {
      if (Math.abs(n - 1) < 0.01) return '1×';
      return String(n) + '×';
    }

    function showListenHint(msg) {
      if (!listenHintEl) {
        listenHintEl = document.createElement('div');
        listenHintEl.className = 'kb-listen__hint';
        if (root) root.appendChild(listenHintEl);
      }
      listenHintEl.textContent = msg;
      listenHintEl.hidden = false;
      try {
        window.clearTimeout(listenHintEl.__t);
        listenHintEl.__t = window.setTimeout(function () {
          if (listenHintEl) listenHintEl.hidden = true;
        }, 6000);
      } catch (e) {}
    }

    function primeOnce() {
      if (primed) return;
      primed = true;
      try {
        var p = new window.SpeechSynthesisUtterance(' ');
        p.volume = 0;
        p.lang = 'zh-CN';
        window.speechSynthesis.speak(p);
      } catch (e) {}
    }

    function autoOn() {
      try {
        return localStorage.getItem(AUTO_KEY) === '1';
      } catch (eAuto) {
        return false;
      }
    }

    function setAuto(on) {
      try {
        localStorage.setItem(AUTO_KEY, on ? '1' : '0');
      } catch (eSet) {}
    }

    var hiddenMemo = typeof WeakMap === 'function' ? new WeakMap() : null;
    function isHidden(el) {
      if (!el) return false;
      if (hiddenMemo && hiddenMemo.has(el)) return hiddenMemo.get(el);
      var chain = [];
      var cur = el;
      var hidden = false;
      while (cur && cur !== document.documentElement) {
        if (hiddenMemo && hiddenMemo.has(cur)) {
          hidden = hiddenMemo.get(cur);
          break;
        }
        chain.push(cur);
        try {
          var st = window.getComputedStyle(cur);
          if (st.display === 'none' || st.visibility === 'hidden') {
            hidden = true;
            break;
          }
        } catch (eHide) {
          break;
        }
        cur = cur.parentElement;
      }
      if (hiddenMemo) {
        for (var i = 0; i < chain.length; i++) hiddenMemo.set(chain[i], hidden);
      }
      return hidden;
    }

    function textOf(el) {
      if (!el || !document.createTreeWalker) return '';
      var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
        acceptNode: function (node) {
          var p = node.parentElement;
          if (!p || (p.closest && p.closest(SKIP))) return NodeFilter.FILTER_REJECT;
          if (isHidden(p)) return NodeFilter.FILTER_REJECT;
          if (!node.nodeValue || !/\S/.test(node.nodeValue)) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        },
      });
      var parts = [];
      var n;
      while ((n = walker.nextNode())) {
        parts.push(n.nodeValue.replace(/\s+/g, ' ').trim());
      }
      return parts.join(' ').replace(/\s+/g, ' ').trim();
    }

    function speakableChunks(text) {
      var out = [];
      var buf = '';
      function flush() {
        var t = buf.replace(/\s+/g, ' ').trim();
        buf = '';
        if (t && /[\u4e00-\u9fffA-Za-z0-9]/.test(t)) out.push(t);
      }
      var breaks = '。！？；!?\n';
      for (var i = 0; i < text.length; i++) {
        buf += text.charAt(i);
        if (breaks.indexOf(text.charAt(i)) >= 0 || buf.length >= MAX_CHUNK) flush();
      }
      flush();
      return out;
    }

    function collectUnits() {
      var cards = document.querySelectorAll('.qa-card');
      if (cards.length) {
        var cardUnits = [];
        var header = document.querySelector('.chapter-header');
        if (header) cardUnits.push(header);
        for (var i = 0; i < cards.length; i++) cardUnits.push(cards[i]);
        return cardUnits;
      }
      var sections = document.querySelectorAll('section');
      var units = [];
      for (var j = 0; j < sections.length; j++) {
        var s = sections[j];
        if (s.closest && s.closest('nav,.sidebar-toc,.toc,.toolbar')) continue;
        if (s.parentElement && s.parentElement.closest && s.parentElement.closest('section')) continue;
        units.push(s);
      }
      if (!units.length) {
        var main = document.querySelector('main, .content-main, .page-wrapper');
        if (main) units.push(main);
      }
      return units;
    }

    function buildQueue() {
      var units = collectUnits();
      var q = [];
      for (var i = 0; i < units.length; i++) {
        var el = units[i];
        if (isHidden(el)) continue;
        var parts = speakableChunks(textOf(el));
        for (var j = 0; j < parts.length; j++) q.push({ text: parts[j], el: el });
      }
      return q;
    }

    function highlight(el) {
      if (currentEl === el) return;
      if (currentEl) currentEl.classList.remove('kb-listening');
      currentEl = el;
      if (!el) return;
      el.classList.add('kb-listening');
      var rect = el.getBoundingClientRect();
      var vh = window.innerHeight || 0;
      if (rect.top >= 0 && rect.bottom <= vh) return;
      try {
        el.scrollIntoView({ block: 'nearest', behavior: reduceMotion ? 'auto' : 'smooth' });
      } catch (eScroll) {
        el.scrollIntoView(true);
      }
    }

    function refreshVoice() {
      cachedVoice = null;
      var voices = [];
      try {
        voices = window.speechSynthesis.getVoices() || [];
      } catch (eVoices) {
        voices = [];
      }
      var best = null;
      var bestScore = -1;
      for (var i = 0; i < voices.length; i++) {
        var lang = (voices[i].lang || '').replace(/_/g, '-').toLowerCase();
        if (lang.indexOf('zh') !== 0) continue;
        var name = (voices[i].name || '').toLowerCase();
        var score = 10;
        if (lang.indexOf('zh-cn') === 0 || lang.indexOf('zh-hans') === 0) score = 50;
        else if (lang === 'zh') score = 30;
        if (voices[i].localService) score += 5;
        if (/tingting|ting-ting|xiaoxiao|xiaoyi|yaoyao|huihui|yunxi|婷婷/.test(name)) score += 8;
        if (score > bestScore) {
          bestScore = score;
          best = voices[i];
        }
      }
      cachedVoice = best;
      if (!warnedNoVoice && voices.length && !best) {
        warnedNoVoice = true;
        showListenHint('本机未安装中文语音：设置 → 辅助功能 → 朗读内容 → 嗓音，下载“中文(中国)”后可正常朗读');
      }
    }

    function paint() {
      var playing = state === 'playing';
      var paused = state === 'paused';
      btn.setAttribute('aria-pressed', playing ? 'true' : 'false');
      var label = '听本页';
      var icon = ICON_SPEAKER;
      if (playing) {
        label = '暂停朗读';
        icon = ICON_PAUSE;
      } else if (paused) {
        label = '继续朗读';
        icon = ICON_PLAY;
      } else if (btn.classList.contains('is-armed')) {
        label = '继续听本页';
      }
      btn.setAttribute('aria-label', label);
      btn.setAttribute('title', label);
      btn.innerHTML = icon;
      panel.hidden = !(playing || paused);
      toggleBtn.textContent = paused ? '继续' : '暂停';
      toggleBtn.setAttribute('aria-label', paused ? '继续朗读' : '暂停朗读');
      toggleBtn.setAttribute('title', toggleBtn.getAttribute('aria-label'));
      var rl = rateLabel(rate);
      rateBtn.textContent = rl;
      rateBtn.setAttribute('aria-label', '语速 ' + rl + '，点击切换');
      rateBtn.setAttribute('title', rateBtn.getAttribute('aria-label'));
    }

    function finish() {
      state = 'idle';
      window.clearTimeout(chunkWatchdog);
      utteranceOpen = false;
      cursor = 0;
      retries = 0;
      highlight(null);
      paint();
    }

    function stop(user) {
      gen++;
      window.clearTimeout(chunkWatchdog);
      state = 'idle';
      utteranceOpen = false;
      cursor = 0;
      retries = 0;
      try {
        window.speechSynthesis.cancel();
      } catch (eCancel) {}
      highlight(null);
      if (user) {
        setAuto(false);
        btn.classList.remove('is-armed');
      }
      paint();
    }

    function armBlocked() {
      stop(false);
      if (autoOn()) btn.classList.add('is-armed');
      showListenHint('浏览器未允许自动朗读，点左下角“听本页”按钮即可开始');
      paint();
    }

    function speakNext() {
      if (state !== 'playing') return;
      if (cursor >= queue.length) {
        finish();
        return;
      }
      var token = ++gen;
      var item = queue[cursor];
      highlight(item.el);
      refreshVoice();
      var u = new window.SpeechSynthesisUtterance(item.text);
      u.lang = 'zh-CN';
      u.rate = rate;
      if (cachedVoice) u.voice = cachedVoice;
      utteranceOpen = true;
      spokeAt = Date.now();
      u.onend = function () {
        if (token !== gen) return;
        utteranceOpen = false;
        retries = 0;
        cursor++;
        if (state === 'playing') speakNext();
      };
      u.onerror = function (ev) {
        if (token !== gen) return;
        utteranceOpen = false;
        var err = (ev && ev.error) || '';
        if (err === 'not-allowed') {
          armBlocked();
          return;
        }
        if (err === 'interrupted' || err === 'canceled' || err === 'cancelled') return;
        retries = 0;
        cursor++;
        if (state === 'playing') speakNext();
      };
      try {
        window.speechSynthesis.speak(u);
        armWatchdog(token, item.text.length);
      } catch (eSpeak) {
        utteranceOpen = false;
        armBlocked();
      }
    }

    function armWatchdog(token, textLen, startAt) {
      window.clearTimeout(chunkWatchdog);
      var ms = Math.max(12000, (textLen * 340) / rate + 6000);
      if (!startAt) startAt = Date.now();
      chunkWatchdog = window.setTimeout(function () {
        if (token !== gen || state !== 'playing' || !utteranceOpen) return;
        if (Date.now() - startAt < ms) {
          armWatchdog(token, textLen, startAt);
          return;
        }
        // iOS 27: onend 可能永不触发，队列冻结；强制 cancel 并推进下一段。
        utteranceOpen = false;
        try { window.speechSynthesis.cancel(); } catch (eCancel) {}
        cursor++;
        retries = 0;
        speakNext();
      }, ms);
    }

    function start(manual) {
      primeOnce();
      queue = buildQueue();
      if (!queue.length) return;
      cursor = indexForStart(manual);
      retries = 0;
      state = 'playing';
      setAuto(true);
      btn.classList.remove('is-armed');
      paint();
      speakNext();
    }

    function indexForStart(manual) {
      var hash = '';
      try {
        hash = decodeURIComponent((location.hash || '').replace(/^#/, ''));
      } catch (eHash) {
        hash = (location.hash || '').replace(/^#/, '');
      }
      if (hash) {
        var target = document.getElementById(hash);
        if (target) {
          for (var i = 0; i < queue.length; i++) {
            if (queue[i].el === target || (queue[i].el.contains && queue[i].el.contains(target))) return i;
          }
        }
      }
      if (!manual) return 0;
      var y = window.scrollY || window.pageYOffset || 0;
      if (y < 80) return 0;
      var anchor = (window.innerHeight || 0) * 0.3;
      for (var j = 0; j < queue.length; j++) {
        if (queue[j].el.getBoundingClientRect().bottom > anchor) return j;
      }
      return 0;
    }

    function whenVoices(cb) {
      refreshVoice();
      var existing = [];
      try {
        existing = window.speechSynthesis.getVoices() || [];
      } catch (eExist) {}
      if (cachedVoice || existing.length) {
        cb();
        return;
      }
      var done = false;
      function finish() {
        if (done) return;
        done = true;
        refreshVoice();
        cb();
      }
      try {
        window.speechSynthesis.addEventListener('voiceschanged', finish);
      } catch (eBind) {}
      window.setTimeout(finish, 800);
    }

    function maybeAuto() {
      if (!autoOn()) return;
      if (reduceMotion || document.hidden) {
        btn.classList.add('is-armed');
        paint();
        return;
      }
      whenVoices(function () {
        if (state !== 'idle') return;
        start(false);
        window.setTimeout(function () {
          if (state === 'playing' && !window.speechSynthesis.speaking && !window.speechSynthesis.pending) {
            armBlocked();
          }
        }, 700);
      });
    }

    function pausePlayback() {
      if (state !== 'playing') return;
      state = 'paused';
      gen++;
      window.clearTimeout(chunkWatchdog);
      utteranceOpen = false;
      try {
        window.speechSynthesis.cancel();
      } catch (ePause) {}
      paint();
    }

    function resumePlayback() {
      if (state !== 'paused') return;
      state = 'playing';
      paint();
      speakNext();
    }

    function onToggle() {
      if (state === 'playing') pausePlayback();
      else if (state === 'paused') resumePlayback();
      else start(true);
    }

    btn.addEventListener('click', onToggle);
    toggleBtn.addEventListener('click', function () {
      if (state === 'playing') pausePlayback();
      else if (state === 'paused') resumePlayback();
    });

    rateBtn.addEventListener('click', function () {
      var i = 0;
      for (; i < RATES.length; i++) {
        if (Math.abs(RATES[i] - rate) < 0.01) break;
      }
      rate = RATES[(i + 1) % RATES.length];
      try {
        localStorage.setItem(RATE_KEY, String(rate));
      } catch (eStore) {}
      paint();
    });

    stopBtn.addEventListener('click', function () {
      stop(true);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      if (document.documentElement.classList.contains('toc-drawer-open')) return;
      if (state === 'idle') return;
      stop(true);
    });

    window.addEventListener('pagehide', function () {
      stop(false);
    });

    window.addEventListener('pageshow', function (e) {
      if (!e.persisted || state !== 'idle') return;
      maybeAuto();
    });

    try {
      window.speechSynthesis.addEventListener('voiceschanged', refreshVoice);
    } catch (eVoiceBind) {}
    refreshVoice();

    var spokenMs = 0;
    window.setInterval(function () {
      if (!isChromium) return; // Safari/iOS: 程序化 pause/resume 会弄坏 TTS，跳过
      if (state !== 'playing' || !window.speechSynthesis.speaking || window.speechSynthesis.paused) {
        if (state !== 'playing') spokenMs = 0;
        return;
      }
      spokenMs += 1000;
      if (spokenMs < 10000) return;
      spokenMs = 0;
      suppressWatchUntil = Date.now() + 1000;
      try {
        window.speechSynthesis.pause();
        window.speechSynthesis.resume();
      } catch (eKeep) {}
    }, 1000);

    window.setInterval(function () {
      if (state !== 'playing') return;
      if (Date.now() < suppressWatchUntil) return;
      if (window.speechSynthesis.paused && Date.now() - spokeAt > 1200) {
        try {
          window.speechSynthesis.resume();
        } catch (eUnstick) {}
      }
      if (!utteranceOpen) return;
      if (window.speechSynthesis.speaking || window.speechSynthesis.pending) return;
      if (Date.now() - spokeAt < 800) return;
      utteranceOpen = false;
      retries++;
      if (retries > 1) {
        retries = 0;
        cursor++;
      }
      speakNext();
    }, 500);

    paint();
    maybeAuto();
  }

  /* 全站搜索：索引在首次打开时拉取。样式随脚本注入。 */
  function initPageSearch() {
    if (window.__kbSearchBound) return;
    if (!document.body) return;
    window.__kbSearchBound = true;

    if (!document.getElementById('kb-search-style')) {
      var style = document.createElement('style');
      style.id = 'kb-search-style';
      style.textContent =
        '.kb-search-btn{width:44px;height:44px;padding:0;border-radius:50%;display:flex;align-items:center;' +
        'justify-content:center;line-height:1;cursor:pointer;font-family:inherit;font-size:13px;font-weight:600;' +
        'background:var(--bg2,#fff);color:var(--ink,var(--text,#1e293b));' +
        'border:1px solid var(--rule,var(--line,#e2e8f0));' +
        'box-shadow:var(--shadow-md,0 4px 12px rgba(15,23,42,.12));' +
        'touch-action:manipulation;-webkit-tap-highlight-color:transparent}' +
        '.kb-search-btn svg{width:20px;height:20px;display:block}' +
        '.kb-search-btn:hover,.kb-search-btn[aria-expanded="true"]{border-color:var(--accent,#2563eb);color:var(--accent,#2563eb)}' +
        '.kb-search-btn:focus-visible{outline:2px solid var(--accent,#2563eb);outline-offset:2px}' +
        '.kb-search-btn--fixed{position:fixed;z-index:1000;top:max(10px,env(safe-area-inset-top));' +
        'right:max(16px,env(safe-area-inset-right))}' +
        '.kb-search-btn--bar{position:static;width:auto;min-height:44px;height:auto;padding:0 12px;border-radius:999px;' +
        'box-shadow:none}' +
        '.kb-search{position:fixed;inset:0;z-index:1200;display:flex;align-items:flex-start;justify-content:center;' +
        'padding:12px;padding-top:max(12px,env(safe-area-inset-top))}' +
        '.kb-search[hidden]{display:none !important}' +
        '.kb-search.kb-search--dock{position:static;inset:auto;z-index:auto;display:block;padding:0;background:transparent}' +
        '.kb-search.kb-search--dock[hidden]{display:none !important}' +
        '.kb-search.kb-search--dock .kb-search__panel{position:fixed;z-index:1200;max-height:min(60vh,420px);' +
        'width:min(420px,calc(100vw - 16px))}' +
        '.toolbar .kb-search-inline{flex:1 1 180px;min-width:0;max-width:280px;height:36px;margin:0;padding:0 12px;' +
        'border-radius:999px;border:1px solid var(--border-strong,var(--line,#cdd5e0));' +
        'background:var(--bg,#fff);color:var(--text,var(--ink,#1e293b));font-family:inherit;font-size:16px;' +
        'line-height:36px;outline:none;box-shadow:none}' +
        '.toolbar .kb-search-inline:focus{border-color:var(--accent,#2563eb)}' +
        '@media (max-width:720px){.toolbar:has(.kb-search-inline){flex-wrap:wrap;row-gap:8px}' +
        '.toolbar:has(.kb-search-inline) .brand{flex:1 1 auto}' +
        '.toolbar:has(.kb-search-inline) .tools{margin-left:auto}' +
        '.toolbar .kb-search-inline{flex:1 1 100%;max-width:none;order:3}}' +
        '.kb-search__backdrop{position:absolute;inset:0;border:0;padding:0;margin:0;cursor:pointer;' +
        'background:rgba(15,23,42,.45)}' +
        '.kb-search__panel{position:relative;z-index:1;width:min(640px,100%);max-height:calc(100vh - 24px);' +
        'max-height:calc(100dvh - 24px);display:flex;flex-direction:column;overflow:hidden;' +
        'background:var(--bg,#fff);color:var(--ink,var(--text,#1e293b));' +
        'border:1px solid var(--rule,var(--line,#e2e8f0));border-radius:12px;' +
        'box-shadow:var(--shadow-md,0 8px 24px rgba(15,23,42,.16))}' +
        '.kb-search__bar{display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--rule,var(--line,#e2e8f0))}' +
        '.kb-search__input{flex:1;min-width:0;border:0;background:transparent;color:inherit;font-family:inherit;' +
        'font-size:16px;line-height:1.4;padding:12px 14px;outline:none}' +
        '.kb-search__close{flex:none;margin-right:8px;min-height:36px;padding:0 10px;border-radius:999px;cursor:pointer;' +
        'font-family:inherit;font-size:13px;font-weight:600;background:var(--bg2,#f0f3f7);' +
        'color:inherit;border:1px solid var(--rule,var(--line,#e2e8f0))}' +
        '.kb-search__status{padding:8px 14px;font-size:12px;color:var(--muted,var(--dim,#64748b))}' +
        '.kb-search__results{overflow:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}' +
        '.kb-search__hit{display:block;padding:10px 14px;text-decoration:none;color:inherit;' +
        'border-top:1px solid var(--rule,var(--line,#e2e8f0))}' +
        '.kb-search__hit:hover,.kb-search__hit:focus-visible{background:var(--bg2,#f0f3f7)}' +
        '.kb-search__site{display:block;font-size:12px;color:var(--muted,var(--dim,#64748b));margin-bottom:2px}' +
        '.kb-search__title,.kb-search__snip{display:block;overflow-wrap:anywhere}' +
        '.kb-search__title{font-weight:600}' +
        '.kb-search__snip{margin-top:4px;font-size:13px;color:var(--muted,var(--dim,#64748b))}' +
        '.kb-search mark{background:transparent;color:var(--accent,#2563eb);font-weight:700}' +
        'html.kb-search-open,html.kb-search-open body{overflow:hidden}' +
        '@media (max-width:768px){.kb-search{padding-left:12px;padding-right:12px}.kb-search__panel{width:100%}}' +
        '@media print{.kb-search,.kb-search-btn,.kb-search-inline{display:none !important}}';
      document.head.appendChild(style);
    }

    var ICON =
      '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 5 1.5-1.5-5-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>' +
      '</svg>';

    var toolbar = document.querySelector('.toolbar');
    var tools = toolbar ? toolbar.querySelector('.tools') : null;
    var inline = !!(toolbar && tools);
    var openBtn = null;
    var input = document.createElement('input');
    input.className = 'kb-search__input';
    input.type = 'search';
    input.placeholder = inline ? '搜索' : '搜索标题和正文';
    input.setAttribute('autocomplete', 'off');
    input.setAttribute('enterkeyhint', 'search');
    input.setAttribute('aria-label', '搜索标题和正文');
    if (inline) {
      input.classList.add('kb-search-inline');
      input.setAttribute('aria-controls', 'kb-search-dialog');
      input.setAttribute('aria-expanded', 'false');
      toolbar.insertBefore(input, tools);
    } else {
      openBtn = document.createElement('button');
      openBtn.type = 'button';
      openBtn.className = 'kb-search-btn kb-search-btn--fixed';
      openBtn.setAttribute('aria-label', '搜索');
      openBtn.setAttribute('title', '搜索');
      openBtn.setAttribute('aria-expanded', 'false');
      openBtn.setAttribute('aria-controls', 'kb-search-dialog');
      openBtn.innerHTML = ICON;
      document.body.appendChild(openBtn);
    }

    var root = document.createElement('div');
    root.className = inline ? 'kb-search kb-search--dock' : 'kb-search';
    root.hidden = true;
    var backdrop = null;
    var panel = document.createElement('div');
    panel.className = 'kb-search__panel';
    panel.id = 'kb-search-dialog';
    panel.setAttribute('role', 'dialog');
    if (!inline) panel.setAttribute('aria-modal', 'true');
    panel.setAttribute('aria-label', '搜索');
    var closeBtn = null;
    var status = document.createElement('div');
    status.className = 'kb-search__status';
    status.setAttribute('aria-live', 'polite');
    var results = document.createElement('div');
    results.className = 'kb-search__results';
    if (!inline) {
      backdrop = document.createElement('button');
      backdrop.type = 'button';
      backdrop.className = 'kb-search__backdrop';
      backdrop.setAttribute('aria-label', '关闭搜索');
      var bar = document.createElement('div');
      bar.className = 'kb-search__bar';
      closeBtn = document.createElement('button');
      closeBtn.type = 'button';
      closeBtn.className = 'kb-search__close';
      closeBtn.textContent = '关闭';
      bar.appendChild(input);
      bar.appendChild(closeBtn);
      panel.appendChild(bar);
      root.appendChild(backdrop);
    }
    panel.appendChild(status);
    panel.appendChild(results);
    root.appendChild(panel);
    document.body.appendChild(root);

    var records = null;
    var loading = null;
    var timer = 0;
    var opened = false;

    function siteRoot() {
      var nodes = document.getElementsByTagName('script');
      var mark = 'java-architect-interview/assets/theme-init.js';
      for (var i = 0; i < nodes.length; i++) {
        var src = nodes[i].src || '';
        var at = src.indexOf(mark);
        if (at >= 0) return src.slice(0, at);
      }
      return '';
    }

    function escapeHtml(s) {
      return String(s).replace(/[&<>"']/g, function (ch) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch];
      });
    }

    function markAll(raw, parts) {
      var esc = escapeHtml(raw);
      var alts = [];
      for (var i = 0; i < parts.length; i++) {
        var piece = escapeHtml(parts[i]).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        if (piece) alts.push(piece);
      }
      if (!alts.length) return esc;
      return esc.replace(new RegExp('(' + alts.join('|') + ')', 'ig'), '<mark>$1</mark>');
    }

    function snippet(rec, parts) {
      var raw = rec.text || '';
      var lower = raw.toLowerCase();
      var at = -1;
      var hit = parts[0] || '';
      for (var i = 0; i < parts.length; i++) {
        var j = lower.indexOf(parts[i].toLowerCase());
        if (j >= 0 && (at < 0 || j < at)) {
          at = j;
          hit = parts[i];
        }
      }
      if (at < 0) raw = rec.title || '';
      if (at < 0) at = raw.toLowerCase().indexOf(String(hit).toLowerCase());
      if (at < 0) return markAll((rec.title || '').slice(0, 80), parts);
      var start = Math.max(0, at - 40);
      var end = Math.min(raw.length, at + String(hit).length + 40);
      var slice = (start > 0 ? '…' : '') + raw.slice(start, end) + (end < raw.length ? '…' : '');
      return markAll(slice, parts);
    }

    function queryParts(q) {
      return q.trim().split(/\s+/).filter(function (part) {
        return part.length > 0;
      });
    }

    function search(q) {
      var parts = queryParts(q);
      if (!parts.length || !records) return [];
      var hits = [];
      for (var i = 0; i < records.length; i++) {
        var rec = records[i];
        var title = (rec.title || '').toLowerCase();
        var text = (rec.text || '').toLowerCase();
        var ok = true;
        var titleHit = true;
        var pos = 1e9;
        for (var p = 0; p < parts.length; p++) {
          var part = parts[p].toLowerCase();
          var inTitle = title.indexOf(part);
          var inText = text.indexOf(part);
          if (inTitle < 0 && inText < 0) {
            ok = false;
            break;
          }
          if (inTitle < 0) titleHit = false;
          var at = inTitle >= 0 ? inTitle : inText;
          if (at < pos) pos = at;
        }
        if (ok) hits.push({ rec: rec, titleHit: titleHit, pos: pos });
      }
      hits.sort(function (a, b) {
        if (a.titleHit !== b.titleHit) return a.titleHit ? -1 : 1;
        if (a.pos !== b.pos) return a.pos - b.pos;
        return a.rec.title < b.rec.title ? -1 : 1;
      });
      return hits.slice(0, 40);
    }

    function render() {
      var q = input.value;
      var parts = queryParts(q);
      results.textContent = '';
      if (!parts.length) {
        status.textContent = records ? (inline ? '输入关键词' : '') : status.textContent;
        return;
      }
      if (!records) return;
      var hits = search(q);
      status.textContent = hits.length ? hits.length + ' 条' : '没有匹配';
      var base = siteRoot();
      for (var i = 0; i < hits.length; i++) {
        var rec = hits[i].rec;
        var a = document.createElement('a');
        a.className = 'kb-search__hit';
        a.href = base + rec.url;
        var site = document.createElement('span');
        site.className = 'kb-search__site';
        site.textContent = rec.site || '';
        var title = document.createElement('span');
        title.className = 'kb-search__title';
        title.innerHTML = markAll(rec.title || rec.url, parts);
        var snip = document.createElement('span');
        snip.className = 'kb-search__snip';
        snip.innerHTML = snippet(rec, parts);
        a.appendChild(site);
        a.appendChild(title);
        a.appendChild(snip);
        results.appendChild(a);
      }
    }

    function ensureIndex() {
      if (records || loading) return loading || Promise.resolve(records);
      status.textContent = '正在加载索引';
      loading = fetch(siteRoot() + 'docs/search-index.json')
        .then(function (res) {
          if (!res.ok) throw new Error('status ' + res.status);
          return res.json();
        })
        .then(function (data) {
          records = (data && data.records) || [];
          status.textContent = '';
          render();
          return records;
        })
        .catch(function () {
          loading = null;
          status.textContent = '索引加载失败';
        });
      return loading;
    }

    function placeDock() {
      if (!inline) return;
      var rect = input.getBoundingClientRect();
      var width = Math.min(420, window.innerWidth - 16);
      var left = Math.max(8, Math.min(rect.left, window.innerWidth - 8 - width));
      panel.style.top = Math.round(rect.bottom + 6) + 'px';
      panel.style.left = Math.round(left) + 'px';
      panel.style.width = Math.round(width) + 'px';
    }

    function setOpen(next) {
      opened = next;
      root.hidden = !next;
      var expanded = next ? 'true' : 'false';
      if (openBtn) openBtn.setAttribute('aria-expanded', expanded);
      if (inline) input.setAttribute('aria-expanded', expanded);
      if (!inline) document.documentElement.classList.toggle('kb-search-open', next);
      if (next) {
        placeDock();
        ensureIndex();
        if (!inline) {
          try {
            input.focus();
          } catch (eFocus) {}
        }
      }
    }

    if (openBtn) {
      openBtn.addEventListener('click', function () {
        setOpen(!opened);
      });
    }
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        setOpen(false);
        try {
          openBtn.focus();
        } catch (eBack) {}
      });
    }
    if (backdrop) {
      backdrop.addEventListener('click', function () {
        setOpen(false);
      });
    }
    input.addEventListener('input', function () {
      if (inline) setOpen(true);
      window.clearTimeout(timer);
      timer = window.setTimeout(render, 120);
    });
    input.addEventListener('search', function () {
      if (inline) setOpen(true);
      render();
    });
    if (inline) {
      input.addEventListener('focus', function () {
        setOpen(true);
      });
      document.addEventListener('pointerdown', function (e) {
        if (!opened) return;
        if (e.target === input || panel.contains(e.target)) return;
        setOpen(false);
      });
      window.addEventListener('resize', function () {
        if (opened) placeDock();
      });
      window.addEventListener(
        'scroll',
        function () {
          if (opened) placeDock();
        },
        { passive: true }
      );
    }
    document.addEventListener(
      'keydown',
      function (e) {
        if (e.key === 'Escape' && opened) {
          e.preventDefault();
          e.stopPropagation();
          setOpen(false);
          if (openBtn) {
            try {
              openBtn.focus();
            } catch (eEsc) {}
          }
          return;
        }
        if (e.key !== '/' || e.metaKey || e.ctrlKey || e.altKey || opened) return;
        var target = e.target;
        if (!target) return;
        var tag = target.tagName;
        if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || target.isContentEditable) return;
        e.preventDefault();
        if (inline) {
          try {
            input.focus();
          } catch (eSlash) {}
        }
        setOpen(true);
      },
      true
    );
  }

  function boot() {
    // 尽早缓存源码（须早于各页 mermaid.initialize startOnLoad）
    snapshotMermaidSources();
    if (document.body) {
      initThemeToggle();
      initReadingProgress();
      initScrollJumpButtons();
      initPageListen();
      initPageSearch();
      initMobileTocDrawer();
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
