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
| `priority-p3` | P3 | 低频延伸 |

- 携带优先级：标准 QA、优先级大盘、八股速查、场景题；**方法论（M系列）与安全手册不携带**优先级标签。
- 属性侧：卡片用 `data-priority="p0|p1|p2"`；提问行叠加 `<span class="priority priority-p0">P0</span>`。

## 4. 资源按需载入规则

- `assets/nav.js`：全站导航交互脚本，**除了安全手册单页外，其余页面均引入**。
- `shared/js/mermaid.min.js`：仅在页面含 Mermaid 图时引入，并配套初始化；无图的页面不得引入。
- `shared/js/echarts.min.js`：仅在含 ECharts 图表时引入。
- 字体：`shared/fonts/`（WorkSans、JetBrainsMono），仅在有需要时通过 `@font-face` 引用。

## 5. 通用内容元素

- 行内代码：`<code class="inline-code">…</code>`。
- 表格：常用 `<div class="table-wrap"><table>…</table></div>` 包裹，便于横滚。
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
| `E##.##` | 八股速查条目 | `E01.01` | chapter-questions-eight-part |
| `S##.##` | 场景题条目 | `S01.01` | chapter-questions-scenario |

约定：前缀字母 >= 该页内容类型；两位数字为「主题组 . 题序」。首页与大盘、安全手册按章节锚点 `href="#其题号"` 引用。
锚点入口均以 `#ID` 形式被 `../../index.html`、`chapter-overview-priority.html` 等转发。

## 7. 通用注意事项（历史踩坑沉淀）

- **嵌套模板语法**：站内 HTML 若内嵌 JSON 对象，必须以合法 JSON 书写（`"answer": …`），不要残留 `{{}}` —— `.nojekyll` 已存在以防模板解析，但内容本身也要合规。
- **Mermaid 文本转义铁律**（仅在含 Mermaid 的页适用）：
  - 节点标签含 `数字.` 时用中文顿号 `1、` 代替 `1.`，防 `Unsupported markdown: list`。
  - 标签含半角括号 `()` 时改用全角 `（）`，防 `Syntax error in text`。
  - 填充色必须用 6 位十六进制（`#fee2e2`），禁用 `#fee`。
  - 含 `#` 的文本需移除或转义。
  - Timeline 条目用冒号 `:` 分隔，勿用 `<br/>`。
- **无图表页**：不写 mermaid 引入与初始化代码，避免多余网络开销。
- **改文件名后的同步**：凡改名为 `chapter-*` 的文件，需同步更新 `../../index.html`、`../index.html`、`chapter-overview-priority.html` 内的引用 href（曾发生安全手册从 `security/` 移入本目录并更名）。