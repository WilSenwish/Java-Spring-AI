/* Laws-Theories-Principles-and-Patterns/assets/app.js
   提取自 index.html 末尾 <script> 块（原第 563–582 行）。
   职责：
   1) 绑定顶部 toolbar 的「↑ 顶部」按钮 → 平滑回顶；
   2) 绑定顶部 toolbar 的「主题切换」按钮 → 复用 theme-init.js 暴露的 window.kbTheme.cycle()
      （浅→深→系统 三态，单一状态源），并随 kb-theme-change 事件同步按钮文案。
   依赖：theme-init.js（已在 <head> 同步引入，先于本文件注册 window.kbTheme）。 */
(function(){
  var b = document.getElementById('topBtn');
  if (b) b.addEventListener('click', function(){ window.scrollTo({ top:0, behavior:'smooth' }); });

  // 顶部 toolbar 主题切换按钮：与 cppam 保持一致（位置/图标+文字）；
  // 复用 theme-init.js 暴露的 window.kbTheme.cycle()（浅→深→系统 三态，单一状态源）
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
