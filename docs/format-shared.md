# 全站共用格式规则（format-shared.md）

适用对象：`..` 下**所有**页面。标准章节卡片体系见 `format-std-qa.md`，特殊章节独享体系见 `format-special.md`。

---

## 1. 文件与页面骨架

- 单文件自包含：结构 + 内容 + 页面内联样式，全部在一个 `.html` 中；仓库内 `.nojekyll` 确保 GitHub Pages 不将其当作 Liquid 模板解析。
- 固定骨架顺序：
  ```
  <!DOCTYPE html>
  <html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>…</title>
    <script src="assets/theme-init.js"></script>              <!-- 须在 CSS 前，防闪白 -->
    <link rel="stylesheet" href="assets/design-system.css">   <!-- 设计令牌 -->
  </head>
  <body>
    <!-- 有章节导航的页面：顶栏必须是 body 内第一个可见块 -->
    <div class="site-page-nav site-page-nav--top">
      <nav class="chapter-nav-top">…</nav>
    </div>
    <div class="page-wrapper">   <!-- 或 body 直接承载（导图/总览等） -->
      … 页面内容 …
    </div>
    <!-- 底栏在正文/footer 之后、所有 <script> 之前 -->
    <div class="site-page-nav site-page-nav--bottom">
      <nav class="chapter-nav">…</nav>
    </div>
    【脚本按需写在 </body> 前】
  </body>
  </html>
  ```
  例外：根 `index.html`、章节站 `java-architect-interview/index.html` **不**放顶/底章节导航。
- 任何新页都必须引入 `assets/theme-init.js`（在 CSS 前）与 `assets/design-system.css`，不得另起一整套全局样式；页面特有样式以内联 `<style>` 覆盖。相对路径：根 `index.html` → `java-architect-interview/assets/…`；章节站 → `assets/…`；导图站 → `../java-architect-interview/assets/…`。

## 2. 设计系统 · 设计令牌（CSS 变量）

`assets/design-system.css` 是唯一设计系统来源，全部以 CSS 自定义属性定义语义令牌，页面一律引用令牌而非魔法值。

| 令牌 | 语义 | 令牌 | 语义 |
|------|------|------|------|
| `--bg` / `--bg2` | 页面背景 / 次级背景 | `--ink` | 主文字色 |
| `--accent` / `--accent2` | 主强调 / 次强调色 | `--muted` | 弱化文字 |
| `--danger` | 危险 / 错误 / P0 | `--success` | 成功 / P2 |
| `--warn` | 警告 / P1 | `--rule` | 分割线 / 边框 |
| `--code-bg` / `--code-ink` | 代码背景 / 代码文字 | `--font-body` / `--font-mono` | 正文字体 / 等宽字体 |
| `--body-size` / `--line-height` | 正文字号 / 行高 | `--max-width` | 内容最大宽度 |
| `--radius-sm/md/lg` | 圆角 | `--shadow-sm/md` | 阴影 |
| `--space-xs/sm/md/lg/xl` | 间距刻度 | | |

> 安全手册页曾用 `--quote-bg`、`--th-bg` 等仅页面内联变量扩充，不影响全局令牌。

## 3. 标签体系（全站通用）

难度与优先级以「元素属性承载数据 + 视觉标签呈现」双通道表达：

### 3.1 难度 `difficulty-*`

| 类名 | 文案（标签位） | 取值（属性） |
|------|------|------|
| `difficulty-senior` | 高级 | `senior` |
| `difficulty-expert` | 专家 | `expert` |
| `difficulty-architect`| 架构 | `architect` |

- 卡片根节点用 `data-difficulty="senior|expert|architect"` 记录机器可读；提问行内叠加 `<span class="difficulty difficulty-xxx">文案</span>` 作视觉标签。
  - **口径（2026-09-16 长官决策）**：**标签位**一律短表 **专家 / 架构 / 高级**（徽标、章节页头 `chapter-meta` 的 `高级 ×N / 架构 ×N / 专家 ×N`、总览 `.ov-stat-label` / `.ov-subgroup-title`、各导航页 `card-tags` / `q-tags`、页脚排序说明）；**正文**用 **专家 / 架构师 / 高级开发**。存量正文中把等级当定语的写法（「架构级理解」「专家级深度」等 8 处）保留、不再新增。门禁 `validate_kb.py` 1j。
  - **`M` / `G` / `K` 三专篇彻底取消难度分级（同日决策）**：不写 `data-difficulty`、不呈现难度徽标、`kb-counts.json` 无对应难度键与不变式；`counts.expert/architect/senior`（46/191/161 = 398）**只覆盖 C/E/S**。细则见 `conventions.md` §2。
  - **优先级例外**：`M`（方法论）/ `G`（工程化要点）/ `K`（生产踩坑）三类卡**不呈现优先级徽标**；三处载体同步：专篇页 `.qa-question`、根 index 的 M/G/K 区块（220 条 q-item，连 `.q-tags` 壳一并去掉）、章节导航 index 的三张专篇 `chapter-card`（无 `.card-tags`）。
  - **配色（2026-09-16 晚修订，长官反馈「专家/架构区分度不明显」）**：`senior` = 蓝 `--accent`、`architect` = 紫 `--accent2`、`expert` = **青绿 `--diff-expert`**（浅色 `#0f766e` / 深色 `#2dd4bf`）。**改前** `expert` 与 `architect` 的文字色**同为 `var(--accent2)`**、底色都是 10% 蓝紫浅色，只有边框透明度 0.2/0.3 的微差，等于专家借用了架构的紫 —— 这是「区分度不明显」的真因。专家卡的左边框与 `qa-badge` 底色改用 `--diff-expert-solid`（浅 `#0f766e` / 深 `#14b8a6`），**原「蓝→紫渐变」已废弃**；两个令牌拆开的原因：徽标底色承白字、胶囊文字是前景色，对比度要求相反，同值无法兼顾。
  - **难度色相须避开优先级色相**（二者在 `.qa-question` 内紧邻同框）：蓝＝高级 + `P2`；紫＝架构 + `callout-deep`；红＝`P0`；琥珀＝`P1` + `callout-pitfall`；翡翠绿＝`callout-tip`。可用余量只剩青绿。`.layer-tag`（想/做/守）刻意沿用架构紫，**不随难度配色改动**。

### 3.2 优先级 `priority-p*`

| 类名 | 文案 | 说明 |
|------|------|------|
| `priority-p0` | P0 | 致命 / 必考 |
| `priority-p1` | P1 | 高频 |
| `priority-p2` | P2 | 中频 |

- 携带优先级（属性侧）：标准 QA、核心原理速查、场景题（条目级全覆盖，合计 92/209/58 = 359）；优先级大盘以 `ov-item` 徽标呈现；方法论仅部分卡片（<span class="kb-count" data-kb-count="methodology_with_priority" data-kb-pos="P14">45</span>/<span class="kb-count" data-kb-count="methodology" data-kb-pos="P15">97</span>）携带；安全手册不携带。**可见徽标侧：M/G/K 一律不呈现优先级徽标**（2026-09-16 长官决策，见 §3.1）；该三处原计数位 P74/P75/P76/P103/P104/P105 已随之作废删除。**注意与难度的差别**：难度是「属性 + 键 + 徽标」三层全删，优先级只删徽标、属性保留。
- 属性侧：卡片用 `data-priority="p0|p1|p2"`；提问行叠加 `<span class="priority priority-p0">P0</span>`（**M/G/K 三类卡只写属性、不叠加可见徽标**）。

### 3.3 导图分层标签 `layer-tag`（**非难度**）

根 index 的导图节点（T01~T48）用「想 / 做 / 守」标注所在分层（对应导图三组：① 思维模式（道）② 方法论（法）③ 原则（术））。

```html
<span class="q-tags"><span class="layer-tag">想</span></span>
```

- 类定义在 `design-system.css`（视觉与 `.difficulty` + `.difficulty-architect` 完全一致）；根 index 页内另有 `.q-tags .layer-tag` 尺寸覆盖（引用 `--dir-fs-2xs` / `--dir-pad-chip`）。
- **禁止再用 `difficulty difficulty-architect` 承载这类非难度标签**（2026-09-16 整改）：既违反「difficulty 类只放难度」口径，也会让按类名做文案归一/门禁的脚本把「想」误改成「架构」。门禁 `validate_kb.py` 1j。

## 4. 资源按需载入规则

- `assets/theme-init.js`：主题同步初始化 + **全站主题切换器** + **返回顶部 / 去到底部**（见 §9）；**所有用户可见 HTML 均须在 `design-system.css` 之前引入**。
- `assets/nav.js`：全站导航交互脚本（章节站均引入；导图/根 index 可依赖 `theme-init.js` 的浮动控件）；职责含：
  1. **侧栏 TOC 滚动高亮**：按 `a[href^="#"]` 解析目标，兼容卡片 / 分组锚点 / 章节 `h2`；当前高亮条目所属 `.toc-group` 内的 `a.toc-group-title` **同步加 `.active`**（分组标题高亮同步）。
  2. 阅读进度条；主题切换 / 回顶 / 去底由 `theme-init.js` 负责（本脚本仅兜底防漏）。
  3. **表格纵向卡片化**（≤640px 时 `initTableCards()` 为结构规整的表注入 `td[data-label]` 并加 `table-cards` 类；含 `colspan/rowspan` 的表自动跳过）。
- `shared/js/mermaid.min.js`：仅在页面含 Mermaid 图时引入，并配套初始化；无图的页面不得引入。初始化须用 `mermaid.initialize((window.kbTheme && window.kbTheme.mermaidConfig({ startOnLoad: true })) || {…})`（偏蓝 `base` 主题）；禁止写死 `"neutral"` / `"default"`。换肤重绘由 `theme-init.js` 缓存 `data-kb-mermaid-src` 后 `mermaid.run`，勿在页面重复监听重绘。**每个** `<div class="mermaid">` 的上一行必须是 `<!-- prettier-ignore -->`（防止 HTML 格式化把图源码压成一行）；见 §10。
- `shared/js/echarts.min.js`：仅在含 ECharts 图表时引入。
- 字体：`shared/fonts/`（WorkSans、JetBrainsMono），仅在有需要时通过 `@font-face` 引用。

### 4.1 侧栏分组标题（`toc-group-title`）

- **必须**写成可点击锚点：`<a class="toc-group-title" href="#…">…</a>`。**禁止** `<div class="toc-group-title">`（`nav.js` 只高亮带 `href="#id"` 的链接，div 无法参与高亮同步）。
- 目标锚点须在正文存在对应 `id`（组导读 / `section` / `m-subgroup-title` 等），并建议带 `scroll-margin-top`（`design-system.css` 已覆盖 `.epq-group-head` / `.scenario-group` / `.eng-group` / `.m-subgroup-title[id]` / `.dimension-section[id]`）。
- 有分组的页面一览：

  | 页面 | 分组标题 `href` 目标 | 正文锚点载体 |
  |------|----------------------|--------------|
  | 核心原理八篇 | `#epq-group-NN` | `.epq-group-head` |
  | 场景题 | `#group-N` | `.scenario-group` |
  | 核心方法论 | `#m-group-01~06` / `#hc-section` 等 | `.m-subgroup-title[id]` / `.dimension-section[id]` |
  | 工程化要点 | `#G01`～`#G08` | `.eng-group` |

### 4.2 顶 / 底章节导航（`chapter-nav-top` / `chapter-nav`）

- **放置（硬约束）**：
  - 顶栏：`body` 内**第一个**子块，外包 `<div class="site-page-nav site-page-nav--top">`。
  - 底栏：正文与 `<footer>`（若有）之后、**所有** `<script>` 之前，外包 `<div class="site-page-nav site-page-nav--bottom">`。
  - **无导航页**：仅根 `index.html`、章节站 `java-architect-interview/index.html`；导图 `index.html` 与其余内容页均须有顶底导航。
- **顶底内容必须一致**：`.chapter-nav-top` 与 `.chapter-nav` 的内侧 HTML（链接集合与文案）须相同，仅外层 class 不同。
- **顶底高度与间距对称**：壳层 `.site-page-nav--top` / `--bottom` 使用相同的上下 `padding`；内层导航条相同 `min-height` / `padding`；**内容 ↔ 导航块**的间隔只由壳层承担（正文首屏如 `.map-hero` / `.ov-hero` 勿再叠加大 `padding-top`）。样式以 `assets/design-system.css` 为准，小屏断点亦须对称。
- **箭头**：统一字面量 `←` / `→`（禁止 `&#8592;` / `&#8594;`）；思维导图外链箭头仍用 `&#8599;`。
- **回目录文案**：统一「返回目录」（禁止「返回首页」）；导图站首/末用「导图总览」/「返回导图总览」。
- **结构**（三槽）：
  - 左：`nav-prev`（上一篇）或首篇 `nav-home`
  - 中：`nav-center` 内 `nav-mind` 快捷链（见下）
  - 右：`nav-next`（下一篇）或末篇 `nav-home`
- **去重**：若左侧已指向某 URL，中间 `nav-center` **不得再重复**同一目标。
- **章节站阅读链路**（上一/下一）：  
  `核心方法论 → 工程化要点 → 生产踩坑 → C01…C15 → 服务端安全 → 核心原理速查 → 高频场景题`  
  首篇左「返回目录」、末篇右「返回目录」。**`nav-overview-priority.html` 使用标准三槽顶底导航**（左返回目录；中：核心方法论 / 核心原理 / 场景；右进 C01），顶底同文，外包 `.site-page-nav`。
- **篇章页居中组**（C01–C15 / 安全）：**核心方法论 → 全部章节 → 本章思维导图**；方法论页居中仅「本章思维导图」（左已是返回目录）；工程化/踩坑居中为「全部章节 + 本章思维导图」；核心原理/场景无导图链。
- **导图站阅读链路**：与章节站同序的 `mind-*`；居中组为 **全部章节 → 导图总览 → 本导图对应的章节**（首篇左已是导图总览时，居中去掉「导图总览」）。
- **小屏**：≤900px 左右槽各半行、居中整行；≤768px 按钮固定行高 + 省略号，禁止顶底栏因换行导致高度不一致。

## 5. 通用内容元素

- 行内代码：`<code class="inline-code">…</code>`。
- 表格：统一使用 `.compare-table` 体系——标准写法 `<table class="compare-table">`，或 `<div class="compare-table"><table>…</table></div>` 包裹写法（两写法均被样式与卡片化脚本覆盖）。**禁止裸 `<table>`**。小屏（≤768px）呈带边框圆角面板 + 横滑，≤640px 由 nav.js 纵向卡片化。
- 提示块 / callout：带高亮标题的容器（标准章多用 `callout-title`），承载注意 / 提醒语义。
- 代码块 / 列表、`<strong>` 重点强调等遵循朴素 HTML；语义用类而非内联样式表达。

## 6. 文件与 ID 命名规范

### 6.1 文件命名

```
chapter-{NN}-{topic-slug}.html     # 标准 QA 章节（NN=01..15 编号）
chapter-{topic-name}.html          # 特殊章节（core-methodology / overview-priority / questions-* / server-security-checkpoint）
index.html                         # 首页
```

### 6.2 锚点 ID 前缀语义（跨章节唯一约定）

| 前缀 | 含义 | 示例 | 所在文件 |
|------|------|------|----------|
| `C##.##` | 标准 QA 题号（Chapter.编号） | `C01.01` | chapter-01 ~ 15 |
| `M##.##` | 核心方法论条目 | `M01.01` | chapter-core-methodology |
| `G##.##` | 工程化要点条目 | `G01.01` | chapter-engineering-practices |
| `E##.##` | 核心原理速查条目 | `E01.01` | chapter-questions-eight-part |
| `S##.##` | 场景题条目 | `S01.01` | chapter-questions-scenario |

约定：前缀字母 >= 该页内容类型；两位数字为「主题组 . 题序」。首页与大盘、安全手册按章节锚点 `href="#其题号"` 引用。
锚点入口均以 `#ID` 形式被 `../../index.html`、`nav-overview-priority.html` 等转发。

## 7. 通用注意事项（历史踩坑沉淀）

- **嵌套模板语法**：站内 HTML 若内嵌 JSON 对象，必须以合法 JSON 书写（`"answer": …`），不要残留 `{{}}` —— `.nojekyll` 已存在以防模板解析，但内容本身也要合规。
- **Mermaid 文本转义铁律**（仅在含 Mermaid 的页适用）：
  - 节点标签含 `数字.` 时用中文顿号 `1、` 代替 `1.`，防 `Unsupported markdown: list`。
  - 标签含半角括号 `()` 时改用全角 `（）`，防 `Syntax error in text`。
  - 填充色必须用 6 位十六进制（`#fee2e2`），禁用 `#fee`。
  - 含 `#` 的文本需移除或转义。
  - Timeline 条目用冒号 `:` 分隔，勿用 `<br/>`。
- **无图表页**：不写 mermaid 引入与初始化代码，避免多余网络开销。
- **代码块内尖括号必须转义**：`<pre><code>` 仅保留空白/换行，**不禁用标签解析**——Java 泛型 `Map<T,S>`、lambda `->`、比较符等必须写成 `&lt;` / `&gt;`，否则 `<String` 被当作标签起始导致渲染错乱（chapter-07 曾踩坑）。
- **命令占位符转义**：`<pid>` 之类占位符必须写 `&lt;pid&gt;`，否则被浏览器当作未知标签、"pid" 文本被吞（mind-02 曾踩坑）。
- **顶层 div 必须平衡**：`qa-card` 的关闭 `</div>` 缺失会让后续所有卡片嵌套进该卡、并"偷走" `page-wrapper` 的关闭标签（chapter-09 曾踩坑）；改卡后应复核整页 div 深度为 0。
- **改文件名后的同步**：凡改名为 `chapter-*` 的文件，需同步更新 `../../index.html`、`../index.html`、`nav-overview-priority.html` 内的引用 href（曾发生安全手册从 `security/` 移入本目录并更名）。
- **侧栏分组标题禁止用 div**：`<div class="toc-group-title">` 无法被 `nav.js` 高亮；必须用 `<a class="toc-group-title" href="#…">`，且正文有对应 `id`（方法论 / 工程化曾踩坑）。
- **顶底导航须同文**：改 `chapter-nav-top` 时同步 `chapter-nav`；箭头与「返回目录」文案见 §4.2。
- **权威/结构计数点标记**：展示题量/卡量一律 L0（`.kb-count` + `data-kb-pos` + `data-kb-count`，键在 `kb-counts.json` 的 `counts`/`struct`）；样式在 `assets/design-system.css`；细则见 skills `conventions.md` **§5.1.4**。禁止聚合 UI 留裸数字；禁止 `kb-count-local`。
- **禁止写死日历年的营销/考察语气**：用户可见文案（副标题、开篇、卡片摘要、题干、导图注）勿写「2026 工程能力要求 / 2026 技术趋势 / 2026 高频 / 2026 选型」等会随年份过期的表述，改用「最新 / 当前 / 近年」。**例外**：技术演进迭代、产品版本、标准发布日、证据复核日、示例日期、页脚「最后更新」、changelog 日期可保留具体年月日。

## 8. 手机小屏强制规范（MOBILE-MANDATORY）

> **强制要求**（与 `AGENTS.md` 硬红线第 6 条同级）：全站内容样式必须针对手机小屏优化。新增/改版页面未做小屏适配视为未完成交付。

### 8.1 适用范围

- 根目录 `index.html`
- 章节站全部页面（`java-architect-interview/**/*.html`，含 index / chapter-* / nav-*）
- 导图站全部页面（`java-architect-interview-mind/**/*.html`）
- 共享样式：`assets/design-system.css`（导图站相对路径引用同一文件）

### 8.2 断点约定

| 断点 | 用途 |
|------|------|
| ≤900px | 章节顶/底导航分组换行；章节 index 卡片网格改单列 |
| ≤768px | **手机主断点**：字号/间距/页脚堆叠/统计条网格化/长文断词 |
| ≤640px | `.compare-table` 纵向卡片化（`nav.js` `initTableCards`） |
| ≤480px | 极小屏：进一步压缩标题、统计列数、导航按钮 |

所有页面必须含：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 8.3 实现归属

1. **共享基线**：写在 `assets/design-system.css`，段注释标记为 `MOBILE-MANDATORY`（禁止删除该标记）。覆盖 `page-wrapper` / `chapter-*` / `qa-*` / `code-block` / `chapter-grid` / `index-hero`，并对导图/根目录常见类（`map-*` / `idx-*` / `dir-*` / `epq-*`）提供小屏兜底。
2. **页面内联样式**：若在 `<style>` 里写了桌面专用布局（如 `grid-template-columns: repeat(3, 1fr)`、固定 `minmax(320px,…)`、大字号 hero），**同一文件必须**提供对应 `@media (max-width: 768px)`（建议再补 `480px`）覆盖；否则桌面规则会压过共享 CSS（同特异度、页面样式后加载）。
3. **禁止**：固定宽表格/代码块不横滑；卡片页脚与标签不换行导致横向溢出；仅桌面 `hover` 位移作为唯一可发现性（触控设备须可直接点击）。
4. **长 token 换行兜底（2026-09-15 补，实测事故）**：`body` 必须声明 `overflow-wrap: anywhere`——它是可继承属性，一条声明覆盖全站所有文本容器。缺此声明时，`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`、`-Djdk.tracePinnedThreads=full|short` 这类长英文标识符/路径/方法签名不换行，横向撑破卡片：实测 375px 视口下核心原理页（`chapter-questions-eight-part.html`）文档溢出 **248px**、**18 处**元素越界（`@media` 内的逐选择器兜底不可靠，`.epq-kp-list li` / `.epq-fu-list li` / `ol>li` / `.callout p` 全被漏掉）。
   裸 `<pre>`（未被 `.code-block` 包裹）另需 `pre { overflow-x: auto }` 兜底：实测 chapter-07 有 8 处裸 pre 溢出 **814px**。
   > 注意：**逐选择器枚举的兜底方式本身是缺陷来源**——共享 CSS 原先只覆盖 `qa-*` / `epq-question` / `chapter-card *`，新增的 `epq-*` 正文容器整类被漏。优先用可继承的全局兜底而非罗列选择器。
5. **列表 marker 缩进兜底（2026-09-16 补，实测事故）**：`design-system.css` 必须保留零特异度兜底
   `:where(ul, ol) { padding-inline-start: 1.25rem }`。顶部 reset（`* { margin: 0; padding: 0 }`）抹掉了
   `ul` / `ol` 的 UA 默认 `padding-inline-start`（40px），全站列表缩进因此完全依赖各自的类规则；
   凡未匹配到类规则的列表 `padding-left` 即为 0，而 `list-style-position: outside` 的圆点/数字是
   **绘制在内容盒之外**的——会被甩进卡片内边距区：桌面表现为「列表没有缩进、圆点贴着卡片边缘」，
   小屏（卡片内边距收窄到 `0.9rem` = 14.4px）直接越出卡片。实测核心原理页 20 处
   （`.epq-section > ul/ol`）、安全检查页 1 处（`main.content-main > ol`）。
   > 必须用 `:where()` 把特异度压到 0，这样任何带类名的列表规则（`.epq-kp-list { padding: 0 }`、
   > `.map-col ul { padding: 0 }`、`.sidebar-toc ol { padding: 0 }`、`.guide-body ul { padding-left: 1.2em }`）
   > 都能覆盖它。**写成裸选择器 `ul, ol { … }`（特异度 0,0,1）会顶掉这些自定义列表的排版**，
   > 反而制造新缺陷——`validate_kb` 项 1h 会拦这一退化。
6. **有序列表缩进必须与无序列表同步（2026-09-16 补，实测事故）**：给 `ul` 写 `padding-left` 时，
   **同一容器的 `ol` 必须同步**。多处 CSS 只写了 `ul` —— `nav-server-security-checkpoint.html` 的
   `.content-main ul { padding-left: 24px }`、`chapter-questions-scenario.html` 的
   `.reading-guide .guide-body ul { padding-left: 1.2em }`；`ol` 于是回落到共享样式的 `1.25rem`
   兜底，**数字比同容器的圆点少缩进 4px**（实测安全检查页正文数字列表 pl=20 vs 圆点 pl=24）。
   另注意 `footer .sources ol` / `.qa-layer-body ul, ol` 用的是 `1.2rem`，与兜底的 `1.25rem` 不同值。
   `check_list_indent.js` 按「同容器内 `min(ol pl) < max(ul pl) − 0.5`」拦截。
   > `list-style: none` 的自定义装饰列表（`.map-col ul` / `.epq-kp-list ul` / `.sidebar-toc ol`）
   > 不参与该判定。
7. **横向留白只能有一个来源（2026-09-16 补，实测事故）**：一个页面内，**同一断点下的横向 gutter 必须来自单一容器**，
   下游容器不得各自再加边距——**尤其要留意共享 `design-system.css` 已在 ≤768 段为 `.dir-toolbar,.dir-legend,.dir-section,.dir-stats`
   统一写了 `padding-left/right: max(12px, env(safe-area-inset-*))`**，页面内联样式若再给 `.dir-section` 加 `margin: 0 12px`、
   且 `.dir-container` 保持桌面 `1.5rem`，就会叠加成每侧 68px（根 index 实测：24+12+12+1+8+8+8）。
   - 量化口径：**列表可用宽 / 视口宽**。根 index 修复前 375px 下为 229/375 = **61%**，修复后 325/375 = **87%**。
   - 判定阈值建议：可读内容的**可用宽不得低于视口的 78%**（375px 下 ≈ 292px）；低于此值即为留白超标。
   - 对齐口径：标签行（`.q-tags`）等「第二行内容」的缩进必须用**题号列宽 + gap** 推导，跨断点同步改，
     否则窄断点会与宽断点错位（根 index 曾在 ≤480px 写 `padding-left: 0`，而 ≤768px 为 `5.1rem`）。
   - 附带效应：`.dir-section { overflow: hidden }` 会把「子元素撑破容器」**裁掉而非报错**，
     `check_mobile_overflow.js` 也会因祖先 `overflow:hidden` 计入「横滑容器」而放行 ——
     **这类缺陷只有「宽度实测 + 截图肉眼」才能发现**，不要只信溢出脚本的 PASS。
   > 复测脚本：`scripts/probe_root_index_whitespace.js`（打印各容器 padding/margin、逐级 left 留白、列表可用宽、页高）。

8. **横向内缩只能有一层，且不得被部分分支绕过（2026-09-16 补，实测事故）**：与第 7 条同族 —— gutter 之外，
   内容自身的横向**内缩也必须由单一容器承担**。根 index 提供了完整反例：其 section 分两类，
   **有分组**（`q-list` 在 `.dir-group` 内）与**无分组**（`q-list` 直接挂 `.dir-body`）——
   内缩若写在 `.dir-group` 上，无分组分支就整体失去该层，题号左缘退化成紧贴卡片边框
   （桌面实测 **1px vs 有分组的 17px**；小屏仅差 4px，正是因此被忽略了两轮）。
   - **位置/间距不要实现为「相邻元素恰好撑开」**：如把计数胶囊位置交给兄弟节点 `.tagline{flex:1}` 推挤，
     则**没有该兄弟的分支必然退化**（根 index 15 个无 tagline 的篇章里，胶囊紧贴标题，右缘 294px vs 行尾 1035px）。
     位置要有**自有属性**（`margin-left:auto`、固定 padding）。
   - 量测要求：**按取值集合验收，不抽样单个元素**。根 index 全 24 个 section 的题号左缘集合须为 `{17}`（桌面）/ `{5}`（小屏），
     计数胶囊右缘集合须为 `{1035}` / `{346}`；出现两个以上取值即说明有分支未覆盖。
   > 复测脚本：`scripts/probe_section_style.js`（逐 section 导出结构与计算样式，按「有无 `.dir-group`」分类比对）。

### 8.4 验收清单（改样式必过）

- [ ] ≤768px 无整页横向滚动（代码块/表允许组件内横滑）
- [ ] 长英文 token（包名/路径/方法签名/命令行参数）可断行，不撑破卡片
- [ ] 代码块统一 `<div class="code-block"><pre><code>…</code></pre></div>` 包裹；裸 `<pre>` 无深色样式也无横滑，属缺陷
- [ ] 列表 marker（圆点/数字）落在内容区内：既未压到卡片内边距、更未越出卡片；列表内容相对正文有明显缩进层次
- [ ] 同一容器内**有序列表与无序列表的缩进一致**：给 `ul` 写 `padding-left` 时同步写 `ol`（否则数字回落到 `1.25rem` 兜底，比圆点少缩进 4px）
- [ ] **横向内缩单层且全分支一致**：内缩由单一容器提供；**按取值集合**核对同语义元素（逐区块导出几何，只允许一个取值）；位置类样式不得依赖兄弟元素的 `flex` 撑开
- [ ] **横向留白单一来源**：同断点下 gutter 只由一处容器提供；可读内容可用宽 ≥ 视口 78%（375px 下 ≥ 292px）；不用截图肉眼确认过 `.dir-section` 这类 `overflow:hidden` 容器内是否有被裁掉的子元素
- [ ] 标题与长摘要可断词，不撑破卡片
- [ ] 统计条/元信息为网格或可换行，不挤成单行溢出
- [ ] 卡片 footer（题量 + 难度徽标）小屏可换行或上下堆叠
- [ ] 顶/底 `chapter-nav` 可点、可辨（沿用既有 900/768/480 规则）
- [ ] Mermaid 容器可横滑，不撑破版心
- [ ] 未用预览服务打开 HTML 做视觉确认（避免 `data-page-node-id` 注入）；交付写清改动文件绝对路径与适配结论

> **实测建议**：静态审计（扫描超阈值长 token）只能发现风险，不能证明修复有效。用 headless 浏览器在真实视口下量 `documentElement.scrollWidth - clientWidth` 与「内容越出卡片」的元素数，才是可交付的证据。macOS 上 Chrome 的 `--window-size` 被最小窗口宽度钳制为 500 CSS px，须用 CDP `Emulation.setDeviceMetricsOverride` 精确模拟 375/414（脚本见 `tmp/cdp_measure_batch.js`，可复用）。

### 8.5 校验

`validate_kb.py` 会检查：全站 HTML 含 viewport；`design-system.css` 含 `MOBILE-MANDATORY`；根 index / 导图 index / 导图页含小屏 `@media`；**校验项 1g**——`design-system.css` 的 `body` 规则含 `overflow-wrap: anywhere`、含裸 `pre { overflow-x: auto }`，且全站不存在未被 `.code-block` 包裹的裸 `<pre>`；**校验项 1h**——`design-system.css` 含零特异度列表缩进兜底 `:where(ul, ol) { padding-inline-start: … }`，且该兜底未退化为裸选择器 `ul, ol { … }`。

实测脚本（`.workbuddy/skills/java-kb-expand/scripts/`）：

| 脚本 | 用途 | 判定 |
|---|---|---|
| `check_mobile_overflow.js` | 横向溢出（文档级 + 越出卡片） | `scrollWidth - clientWidth`，溢出即 exit 1 |
| `check_list_indent.js` | 列表 marker 缩进 + 同容器 ol/ul 缩进一致性（全站 44 页 × {1280, 375}） | 可用空间 < 1.2×字号，或 `min(ol pl) < max(ul pl) − 0.5`，即 exit 1 |
| `probe_list_gate.py` | 1h 门禁的正向验证（注入缺陷 → 必须 FAIL） | 两轮注入，`--inject` 支持分步 |

### 8.6 门禁编写规约（新增 `validate_kb` 断言必守）

- **锚定结构，禁用子串 `in`**：断言必须匹配带上下文的真实规则，例如判定 CSS 兜底用
  `re.search(r"^\s*body\s*\{[^}]*overflow-wrap:\s*anywhere", css, re.M)`，
  **禁止**写成 `"overflow-wrap" in css` 这类子串判定——CSS/HTML 里同名串（`body` / `pre` / `ul` / `ol` 等）随处可见，
  子串命中恒真，无法验证规则是否真在、是否退化。
- **每条新门禁须正向验证**：注入对应缺陷 → 断言必须 FAIL → 还原文件并核 MD5 确认无误伤。
  范式脚本：`scripts/probe_validate_gate.py`（通用两步注入）/ `scripts/probe_list_gate.py`（1h 专项，支持 `--inject` 分步）/ `scripts/probe_index_badge_gate.py`（聚合徽标结构，沙箱双向验证、不写真实文件）。
- **脚本定位项目根禁止写死层级**：校验/探针脚本若需项目根，须**向上查找特征文件**（同时含 `AGENTS.md` 与 `index.html` 的最近祖先），而非 `dirname(__file__)` 叠加固定层数——本技能可经 `.agents/skills/java-kb-expand` 软链调用，层级一变即静默指错目录（曾指到 `.workbuddy/` 并报 `FileNotFoundError`，看似「门禁通过」实则未执行到判定）。
- **只比结构特征，不比展示文本**：跨文件一致性（如 mind 与章节）只比对 **ID 集合**，标题/措辞错位不报错；
  避免门禁因文案微调而误杀，也避免文案漂移漏报结构问题。

## 9. 主题 / 暗黑模式

全站浅色 / 深色 / 跟随系统三态，以 CSS 变量换肤为唯一入口。

| 项 | 约定 |
|---|---|
| 机制 | `html[data-theme="light\|dark"]` 覆盖 `design-system.css` 令牌；未强制时跟 `prefers-color-scheme` |
| 默认 | `system` |
| 持久化 | `localStorage['kb-color-theme']` = `light` \| `dark` \| `system` |
| 防闪白 | `<head>` 在 CSS **之前**引入 `assets/theme-init.js` |
| 切换 UI | 由 `theme-init.js` 注入 `.theme-toggle`（浅色 → 深色 → 跟随系统）以及 `.back-to-top` / `.go-to-bottom` 成对浮动按钮；`nav.js` 仅兜底防漏；页面**不得**手写第二套 |
| Mermaid | `mermaid.initialize(kbTheme.mermaidConfig({ startOnLoad: true }))`（偏蓝 `base` + themeVariables）；换肤时 `theme-init.js` 用 `data-kb-mermaid-src` 还原源码再 `mermaid.run` |

硬约束：

1. **令牌只写 CSS 变量**：新增样式优先 `var(--bg)` / `var(--ink)` / `var(--accent)` 等；禁止新增仅适配浅色的裸 hex 作为页面主色（装饰性章节色条、accent 底上的 `#fff` 文字可例外）。
2. **深色令牌块**：`design-system.css` 须含 `html[data-theme="dark"]` 与 `@media (prefers-color-scheme: dark)` 下 `html:not([data-theme="light"])` 同套令牌。
3. **不改** `docs/facts/`；不重写 Mermaid 图内数百处 `fill:#dbeafe`（默认偏蓝主题变量已覆盖无内联 fill 的节点）。

`validate_kb.py` 会检查：站点 HTML 含 `theme-init.js`；`design-system.css` 含 `data-theme="dark"` 令牌块。

## 10. HTML 格式化（Prettier）与 Mermaid 保护

站点无构建步骤，但仍用 **Prettier 3** 统一 44 个用户可见 HTML 的缩进与标签换行（根 `index.html` + 章节站 `*.html` + 导图站 `*.html`）。`docs/facts/`、备份目录、压缩资源不在格式化范围。

| 项 | 约定 |
|---|---|
| 配置 | 仓库根 `.prettierrc.json` / `.prettierignore` / `package.json`（仅 `prettier` devDependency） |
| 命令 | `npm run format:html`（Prettier 写入 + 闭合标签归一） / `npm run format:html:check`（稳态检查） |
| 关键选项 | `printWidth: 10000`（避免 `</span>` 被拆行破坏计数锚点）、`htmlWhitespaceSensitivity: "css"`、`embeddedLanguageFormatting: "off"`、`endOfLine: "lf"` |
| 后处理 | `scripts/normalize_html_closers.py`：把 Prettier 偶发产出的 `</tag\\n>` 压回 `</tag>`（kb-count / `validate_kb` 依赖同行闭合） |
| Mermaid | 每个 `<div class="mermaid">` **正上方**一行 `<!-- prettier-ignore -->`；忽略该节点整棵子树，图源码保持多行 |
| 新增图 | 插入 mermaid 容器时同步加 ignore（或跑 `ensure_mermaid_prettier_ignore.py`）；再 `format:html` → `validate_kb.py` |
| 语法 | Prettier 遇非法 HTML（未闭合 / 嵌套错误的 `p`/`a` 等）会失败——先修标签再格式化 |

标准写法：

```html
<div class="mermaid-container">
  <!-- prettier-ignore -->
  <div class="mermaid">
graph TD
    A --> B
  </div>
</div>
```

历史坑：无 ignore 时格式化曾把图压成单行，需用 `docs/fix_mermaid.py` 一类脚本从 git 旧版还原；**现行流程以 ignore + Prettier 为准，禁止再裸跑会改写 mermaid 文本节点的格式化器**。

`validate_kb.py` 会检查：凡含 `class="mermaid"` 的站点 HTML，每个图节点上一行均为 `prettier-ignore`；图内换行数 ≥ 2（未塌缩）。
