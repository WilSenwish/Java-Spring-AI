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
    <link rel="stylesheet" href="assets/design-system.css">   <!-- 首个资源 -->
  </head>
  <body>
    <div class="page-wrapper">   <!-- 或 body 直接承载 -->
      … 页面内容 …
    </div>
    【脚本按需写在 </body> 前】
  </body>
  </html>
  ```
- 任何新页都必须引入 `assets/design-system.css`，不得另起一整套全局样式；页面特有样式以内联 `<style>` 覆盖。

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

| 类名 | 文案 | 取值（属性） |
|------|------|------|
| `difficulty-senior` | 高级开发 | `senior` |
| `difficulty-expert` | 专家级 | `expert` |
| `difficulty-architect`| 架构级 | `architect` |

- 卡片根节点用 `data-difficulty="senior|expert|architect"` 记录机器可读；提问行内叠加 `<span class="difficulty difficulty-xxx">文案</span>` 作视觉标签。

### 3.2 优先级 `priority-p*`

| 类名 | 文案 | 说明 |
|------|------|------|
| `priority-p0` | P0 | 致命 / 必考 |
| `priority-p1` | P1 | 高频 |
| `priority-p2` | P2 | 中频 |

- 携带优先级：标准 QA、核心原理速查、场景题（条目级全覆盖，合计 92/209/58 = 359）；优先级大盘以 `ov-item` 徽标呈现；方法论仅部分卡片（<span class="kb-count" data-kb-count="methodology_with_priority" data-kb-pos="P14">45</span>/<span class="kb-count" data-kb-count="methodology" data-kb-pos="P15">91</span>）携带；安全手册不携带。
- 属性侧：卡片用 `data-priority="p0|p1|p2"`；提问行叠加 `<span class="priority priority-p0">P0</span>`。

## 4. 资源按需载入规则

- `assets/nav.js`：全站导航交互脚本，**所有页面（含安全手册单页）均引入**；职责含：
  1. **侧栏 TOC 滚动高亮**：按 `a[href^="#"]` 解析目标，兼容卡片 / 分组锚点 / 章节 `h2`；当前高亮条目所属 `.toc-group` 内的 `a.toc-group-title` **同步加 `.active`**（分组标题高亮同步）。
  2. 返回顶部、阅读进度条。
  3. **表格纵向卡片化**（≤640px 时 `initTableCards()` 为结构规整的表注入 `td[data-label]` 并加 `table-cards` 类；含 `colspan/rowspan` 的表自动跳过）。
- `shared/js/mermaid.min.js`：仅在页面含 Mermaid 图时引入，并配套初始化；无图的页面不得引入。
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

- **顶底内容必须一致**：`.chapter-nav-top` 与 `.chapter-nav` 的内侧 HTML（链接集合与文案）须相同，仅外层 class 不同。
- **箭头**：统一字面量 `←` / `→`（禁止底栏用 `&#8592;` / `&#8594;`、顶栏用字面量的混用）；思维导图外链箭头仍用 `&#8599;`。
- **回目录文案**：统一「返回目录」（禁止「返回首页」）。
- **结构**（三槽）：
  - 左：`nav-prev`（上一篇）或首页首篇 / 特殊页用 `nav-home`（`← 返回目录`）
  - 中：`nav-center` 内 `nav-mind` 链接；篇章页顺序固定为 **核心方法论 → 全部章节 → 本章思维导图**
  - 右：`nav-next`（下一篇）或末篇 / 收束页用 `nav-home`（`返回目录 →`）
- **去重**：若左侧 `nav-prev` 已指向某页，中间 `nav-center` **不得再重复**同一目标（方法论 / 工程化互链页尤须注意）。

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

### 8.4 验收清单（改样式必过）

- [ ] ≤768px 无整页横向滚动（代码块/表允许组件内横滑）
- [ ] 标题与长摘要可断词，不撑破卡片
- [ ] 统计条/元信息为网格或可换行，不挤成单行溢出
- [ ] 卡片 footer（题量 + 难度徽标）小屏可换行或上下堆叠
- [ ] 顶/底 `chapter-nav` 可点、可辨（沿用既有 900/768/480 规则）
- [ ] Mermaid 容器可横滑，不撑破版心
- [ ] 未用预览服务打开 HTML 做视觉确认（避免 `data-page-node-id` 注入）；交付写清改动文件绝对路径与适配结论

### 8.5 校验

`validate_kb.py` 会检查：全站 HTML 含 viewport；`design-system.css` 含 `MOBILE-MANDATORY`；根 index / 导图 index / 导图页含小屏 `@media`。
