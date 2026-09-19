/* =========================================================================
   软件工程的核心哲学原理与方法论 · 终篇
   交互与图表组件（原生 JS，无外部依赖）
   资源文件：app.js  |  配套 style.css
   ========================================================================= */
(function () {
  "use strict";

  /* ---------- 主题切换（明/暗） ---------- */
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem("tcppam-theme"); } catch (e) {}
  if (saved) root.setAttribute("data-theme", saved);
  else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    root.setAttribute("data-theme", "dark");
  }
  function toggleTheme() {
    var cur = root.getAttribute("data-theme") === "dark" ? "dark" : "light";
    var next = cur === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("tcppam-theme", next); } catch (e) {}
    var b = document.getElementById("themeBtn");
    if (b) b.textContent = next === "dark" ? "☀ 浅色" : "🌙 深色";
  }
  var tb = document.getElementById("themeBtn");
  if (tb) { tb.textContent = (root.getAttribute("data-theme") === "dark") ? "☀ 浅色" : "🌙 深色"; tb.addEventListener("click", toggleTheme); }
  var top = document.getElementById("topBtn");
  if (top) top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

  /* ---------- Tabs（五种思路切换） ---------- */
  var tabEls = document.querySelectorAll(".tab");
  tabEls.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var group = tab.getAttribute("data-group");
      var target = tab.getAttribute("data-target");
      document.querySelectorAll('.tab[data-group="' + group + '"]').forEach(function (t) { t.classList.remove("active"); });
      document.querySelectorAll('.panel[data-group="' + group + '"]').forEach(function (p) { p.classList.remove("active"); });
      tab.classList.add("active");
      var panel = document.querySelector('.panel[data-group="' + group + '"][data-panel="' + target + '"]');
      if (panel) panel.classList.add("active");
    });
  });

  /* ---------- 数据 ---------- */
  var IDEA_COLORS = {
    i1: "#2563eb", i2: "#7c3aed", i3: "#059669", i4: "#d97706", i5: "#db2777"
  };
  // 雷达：五思路 × 五维度（1-5 分，仅示意性相对强度）
  var RADAR_AXES = ["抽象深度", "场景广度", "组织维度", "落地实操", "哲学深度"];
  var RADAR_SERIES = [
    { key: "i1", name: "思路一·全息张量", v: [5, 5, 4, 4, 4] },
    { key: "i2", name: "思路二·立体能力", v: [4, 5, 5, 5, 3] },
    { key: "i3", name: "思路三·定律归族", v: [5, 3, 4, 4, 5] },
    { key: "i4", name: "思路四·本体五层", v: [5, 4, 3, 4, 3] },
    { key: "i5", name: "思路五·认知坐标系", v: [5, 5, 5, 3, 5] }
  ];
  // 热力：五思路 × 五层 覆盖深度（0-4）
  var HEAT_ROWS = [
    { key: "i1", name: "思路一·全息张量", v: [4, 5, 4, 3, 5] },
    { key: "i2", name: "思路二·立体能力", v: [4, 5, 4, 3, 4] },
    { key: "i3", name: "思路三·定律归族", v: [5, 4, 3, 2, 3] },
    { key: "i4", name: "思路四·本体五层", v: [5, 4, 4, 3, 3] },
    { key: "i5", name: "思路五·认知坐标系", v: [5, 4, 4, 3, 4] }
  ];
  var HEAT_COLS = ["道", "法", "术", "器", "势"];

  /* ---------- 雷达图渲染 ---------- */
  function renderRadar() {
    var svg = document.getElementById("radar");
    if (!svg) return;
    var cx = 175, cy = 175, maxR = 132, n = RADAR_AXES.length, levels = 5;
    var ns = "http://www.w3.org/2000/svg";
    function pt(i, r) {
      var ang = (-90 + i * (360 / n)) * Math.PI / 180;
      return [cx + r * Math.cos(ang), cy + r * Math.sin(ang)];
    }
    var html = "";
    // 网格环
    for (var L = 1; L <= levels; L++) {
      var rr = maxR * L / levels;
      var pts = [];
      for (var i = 0; i < n; i++) { var p = pt(i, rr); pts.push(p[0].toFixed(1) + "," + p[1].toFixed(1)); }
      html += '<polygon class="radar-grid" points="' + pts.join(" ") + '"/>';
    }
    // 轴线 + 标签
    for (var j = 0; j < n; j++) {
      var e = pt(j, maxR);
      html += '<line class="radar-axis" x1="' + cx + '" y1="' + cy + '" x2="' + e[0].toFixed(1) + '" y2="' + e[1].toFixed(1) + '"/>';
      var lp = pt(j, maxR + 22);
      var anchor = j === 0 ? "middle" : (Math.cos((-90 + j * 72) * Math.PI / 180) > 0.2 ? "start" : (Math.cos((-90 + j * 72) * Math.PI / 180) < -0.2 ? "end" : "middle"));
      html += '<text class="radar-label" x="' + lp[0].toFixed(1) + '" y="' + (lp[1] + 4).toFixed(1) + '" text-anchor="' + anchor + '">' + RADAR_AXES[j] + "</text>";
    }
    // 数据多边形
    RADAR_SERIES.forEach(function (s) {
      var pts = [];
      for (var k = 0; k < n; k++) { var p = pt(k, maxR * s.v[k] / levels); pts.push(p[0].toFixed(1) + "," + p[1].toFixed(1)); }
      html += '<polygon class="radar-poly" points="' + pts.join(" ") + '" fill="' + IDEA_COLORS[s.key] + '" stroke="' + IDEA_COLORS[s.key] + '"/>';
      for (var m = 0; m < n; m++) { var pp = pt(m, maxR * s.v[m] / levels); html += '<circle cx="' + pp[0].toFixed(1) + '" cy="' + pp[1].toFixed(1) + '" r="2.6" fill="' + IDEA_COLORS[s.key] + '"/>'; }
    });
    svg.setAttribute("viewBox", "0 0 350 350");
    svg.innerHTML = html;
    // 图例
    var leg = document.getElementById("radarLegend");
    if (leg) {
      leg.innerHTML = RADAR_SERIES.map(function (s) {
        return '<span><i style="background:' + IDEA_COLORS[s.key] + '"></i>' + s.name + "</span>";
      }).join("");
    }
  }

  /* ---------- 热力矩阵渲染 ---------- */
  function renderHeat() {
    var box = document.getElementById("heatMatrix");
    if (!box) return;
    var t = '<table class="heat"><thead><tr><th>思路 ＼ 层</th>';
    HEAT_COLS.forEach(function (c) { t += "<th>" + c + "</th>"; });
    t += "</tr></thead><tbody>";
    HEAT_ROWS.forEach(function (r) {
      t += '<tr><td class="lab">' + r.name + "</td>";
      r.v.forEach(function (val) { t += '<td class="h' + val + '">' + val + "</td>"; });
      t += "</tr>";
    });
    t += "</tbody></table>";
    box.innerHTML = t;
  }

  renderRadar();
  renderHeat();

  /* ---------- 挂载图渲染（原生 SVG：纤细线条 + 随线旋转箭头） ---------- */
  var NS = "http://www.w3.org/2000/svg";
  function svgEl(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }
  var MOUNT_LAYERS = [
    { label: "道", sub: "元约束 · 价值观 · 守恒律", color: "#9b7fd1" },
    { label: "法", sub: "原则 · 规范 · 禁法", color: "#d98a3a" },
    { label: "术", sub: "招式 · 模式 · 反模式", color: "#5a8fd6" },
    { label: "器", sub: "语言 · 框架 · 平台", color: "#3aa0a0" }
  ];
  // 图二：五层全量结构（势环绕，双向细曲线，箭头沿各自切线精确旋转）
  function MountDiagram(svg) {
    var uid = svg.id;
    var W = 560, top = 40, h = 64, gap = 40, x = (W - 240) / 2;
    var defs = svgEl("defs", {});
    // 箭头尖朝 +x：orient:auto 将 marker 的 +x 轴对齐路径切线，箭头即沿切线方向旋转
    defs.appendChild(svgEl("marker", { id: uid + "Down", markerWidth: 9, markerHeight: 9, refX: 7.5, refY: 4, orient: "auto", markerUnits: "userSpaceOnUse" })
      .appendChild(svgEl("path", { d: "M0,0 L0,8 L8,4 Z", fill: "#94a3b8" })).parentNode);
    defs.appendChild(svgEl("marker", { id: uid + "Up", markerWidth: 9, markerHeight: 9, refX: 7.5, refY: 4, orient: "auto", markerUnits: "userSpaceOnUse" })
      .appendChild(svgEl("path", { d: "M0,0 L0,8 L8,4 Z", fill: "#4ea1ff" })).parentNode);
    svg.appendChild(defs);
    svg.appendChild(svgEl("rect", { x: 30, y: 14, width: W - 60, height: top + MOUNT_LAYERS.length * (h + gap) - 6, rx: 14, fill: "none", stroke: "#e0556b", "stroke-width": 1.5, "stroke-dasharray": "6 5" }));
    var shiLbl = svgEl("text", { x: W / 2, y: 30, "text-anchor": "middle", fill: "#e0556b", "font-size": 12, "font-weight": 700 });
    shiLbl.textContent = "势 · 横贯全局（时机·环境·趋势）";
    svg.appendChild(shiLbl);
    MOUNT_LAYERS.forEach(function (L, i) {
      var y = top + i * (h + gap);
      svg.appendChild(svgEl("rect", { x: x, y: y, width: 240, height: h, rx: 9, fill: L.color, filter: "drop-shadow(0 4px 10px rgba(0,0,0,.22))" }));
      var t = svgEl("text", { x: W / 2, y: y + 27, "text-anchor": "middle", fill: "#fff", "font-size": 16, "font-weight": 700 });
      t.textContent = L.label; svg.appendChild(t);
      var s = svgEl("text", { x: W / 2, y: y + 47, "text-anchor": "middle", fill: "rgba(255,255,255,.92)", "font-size": 11 });
      s.textContent = L.sub; svg.appendChild(s);
      if (i < MOUNT_LAYERS.length - 1) {
        var y1 = y + h, y2 = top + (i + 1) * (h + gap);
        // 左曲线（灰实·下行依据）：从中块下沿外凸至 x≈122.5
        svg.appendChild(svgEl("path", { d: "M" + (x + 60) + " " + y1 + " C " + (x - 70) + " " + (y1 + 18) + "," + (x - 70) + " " + (y2 - 18) + "," + (x + 60) + " " + y2, fill: "none", stroke: "#94a3b8", "stroke-width": 1.6, "stroke-linecap": "round", "marker-end": "url(#" + uid + "Down)" }));
        // 右曲线（蓝虚·上行体现）：从下层外凸回收至中块上沿
        svg.appendChild(svgEl("path", { d: "M" + (x + 180) + " " + y2 + " C " + (x + 310) + " " + (y2 - 18) + "," + (x + 310) + " " + (y1 + 18) + "," + (x + 180) + " " + y1, fill: "none", stroke: "#4ea1ff", "stroke-width": 1.6, "stroke-dasharray": "4 4", "stroke-linecap": "round", "marker-end": "url(#" + uid + "Up)" }));
        // 连线中点注释：紧贴曲线、白描边衬底，表达关联关系
        var my = (y1 + y2) / 2;
        var lblL = svgEl("text", { x: x - 37.5, y: my + 4, "text-anchor": "middle", fill: "#94a3b8", "font-size": 11, "font-weight": 600, stroke: "#fff", "stroke-width": 3, "paint-order": "stroke" });
        lblL.textContent = "依据"; svg.appendChild(lblL);
        var lblR = svgEl("text", { x: x + 277.5, y: my + 4, "text-anchor": "middle", fill: "#4ea1ff", "font-size": 11, "font-weight": 600, stroke: "#fff", "stroke-width": 3, "paint-order": "stroke" });
        lblR.textContent = "体现"; svg.appendChild(lblR);
      }
    });
  }
  // 图一：落地链（竖向细线 + 动词贴线中点 + 底部势带）
  function renderChain(svg) {
    var uid = svg.id;
    var W = 560, top = 40, h = 60, gap = 44, x = (W - 240) / 2;
    var verbs = ["落地为", "填充为", "固化为", null];
    var subs = [
      "元约束 · 价值观 · 守恒律",
      "原则 · 规范 · 禁法（挂于 道）",
      "招式 · 模式 · 反模式（挂于 法）",
      "语言 · 框架 · 平台（挂于 术）"
    ];
    var defs = svgEl("defs", {});
    defs.appendChild(svgEl("marker", { id: uid + "Down", markerWidth: 9, markerHeight: 9, refX: 7.5, refY: 4, orient: "auto", markerUnits: "userSpaceOnUse" })
      .appendChild(svgEl("path", { d: "M0,0 L0,8 L8,4 Z", fill: "#94a3b8" })).parentNode);
    svg.appendChild(defs);
    MOUNT_LAYERS.forEach(function (L, i) {
      var y = top + i * (h + gap);
      svg.appendChild(svgEl("rect", { x: x, y: y, width: 240, height: h, rx: 9, fill: L.color, filter: "drop-shadow(0 4px 10px rgba(0,0,0,.22))" }));
      var t = svgEl("text", { x: W / 2, y: y + 26, "text-anchor": "middle", fill: "#fff", "font-size": 16, "font-weight": 700 });
      t.textContent = L.label; svg.appendChild(t);
      var s = svgEl("text", { x: W / 2, y: y + 45, "text-anchor": "middle", fill: "rgba(255,255,255,.92)", "font-size": 11 });
      s.textContent = subs[i]; svg.appendChild(s);
      if (i < MOUNT_LAYERS.length - 1) {
        var y1 = y + h, y2 = top + (i + 1) * (h + gap);
        var midY = (y1 + y2) / 2;
        // 竖向细线（中线 280）贴块中心
        svg.appendChild(svgEl("line", { x1: W / 2, y1: y1 + 4, x2: W / 2, y2: y2 - 4, stroke: "#94a3b8", "stroke-width": 1.6, "stroke-linecap": "round", "marker-end": "url(#" + uid + "Down)" }));
        // 动词贴线右侧 12px，表达「上层 动词 下层」的挂载落地关系
        var vt = svgEl("text", { x: W / 2 + 12, y: midY + 4, "text-anchor": "start", fill: L.color, "font-size": 12, "font-weight": 700, stroke: "#fff", "stroke-width": 3, "paint-order": "stroke" });
        vt.textContent = verbs[i]; svg.appendChild(vt);
      }
    });
    var by = top + 4 * (h + gap) - 2;
    svg.appendChild(svgEl("rect", { x: 140, y: by, width: 280, height: 42, rx: 12, fill: "none", stroke: "#e0556b", "stroke-width": 1.5, "stroke-dasharray": "6 5" }));
    var sl = svgEl("text", { x: W / 2, y: by + 18, "text-anchor": "middle", fill: "#e0556b", "font-size": 12, "font-weight": 700 });
    sl.textContent = "势 · 横贯全程"; svg.appendChild(sl);
    var sl2 = svgEl("text", { x: W / 2, y: by + 34, "text-anchor": "middle", fill: "rgba(224,85,107,.9)", "font-size": 10.5 });
    sl2.textContent = "时机 · 组织 · 规模 · 周期"; svg.appendChild(sl2);
  }
  MountDiagram(document.getElementById("mountFive"));
  renderChain(document.getElementById("mountChain"));

  /* ---------- 滚动渐显 ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }
})();
