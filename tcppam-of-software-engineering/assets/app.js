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
