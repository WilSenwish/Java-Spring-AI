# 特殊章节独享格式规则（format-special.md）

本章，除标准 QA 章节（chapter-01 ~ 15）外的 6 类页面各有**独享格式体系**，互不通用。编写 / 修改时可据此逐类对照。无论哪类，均遵循 `format-shared.md` 的底层规则（设计令牌、`.nojekyll`、资源按需载入、Mermaid 转义铁律）。

---

## 目录

1. [核心方法论 chapter-core-methodology（M 系列）](#1)
2. [优先级大盘 chapter-overview-priority（ov 组件）](#2)
3. [八股速查 chapter-questions-eight-part（epq 组件）](#3)
4. [场景题 chapter-questions-scenario（S 系列场景卡片）](#4)
5. [安全 Checkpoint chapter-server-security-checkpoint（独立单页）](#5)
6. [首页 index.html](#6)

---

## <a id="1"></a>1. 核心方法论 chapter-core-methodology（M 系列）

- **定位**：核心思维方法论，48 张卡片，ID 前缀 `M`（如 `M01.01`）。
- **卡片**：仍用 `.qa-card`，但**不采用标准六层**，改用三层**单向堆叠**：

  | data-layer | 层标题 | 职责 |
  |-----------|--------|------|
  | `insight` | 核心洞察 | 一句话道破的公理 / 视角 |
  | `principle` | 原理映射 | 把公理落到工程化手段 |
  | `application` | 工程表达 | 技术沟通中的表达话术 / 姿态 |

- **难度**：卡片仅带 `data-difficulty`，取值仅 `architect`（架构级，33）与 `expert`（专家级，15）；**无优先级标签、也无 `data-priority`**。
- **题目头**：`qa-badge`（M01.01）+ `qa-question`（条目标题 + `difficulty` 视觉标签），无 priority 标签。
- **目录**：按模块（M01~M11）分组的多段侧边目录，各模块一组锚点 `M##.##`。
- 单条新增规则：`id = M{模块}.{序}`；`insight → principle → application` 三层层序固定。

## <a id="2"></a>2. 优先级大盘 chapter-overview-priority（ov 组件）

- **定位**：知识点大盘与优先级矩阵页，无 `qa-card`，纯 `ov-*` 组件；服务于「按 P0/P1/P2 复习」的导航索引，**向 `questions-*`、`chapter-*` 内页锚点转发**。
- **结构层级**：

  ```
  ov-stats-row            # 顶部统计行（如 P0/P1/P2 计数），页首
  ├─ ov-group（四大知识组）×4
  │    ├─ ov-group-title
  │    └─ ov-group-body
  │         └─ ov-subgroup（子主题组）×11
  │              ├─ ov-subgroup-title (+ ov-stat-num/ov-stat-label)
  │              └─ ov-items
  │                   └─ ov-item ×321
  │                        ├─ ov-num        # 序号
  │                        ├─ ov-title      # 条目名
  │                        └─ ov-badges     # 难度 / 优先级徽标
  ```

- 条目为链接卡片，点击跳转对应题目的站内锚点；改新题 / 更名页面时须同步本页 `ov-item` 的 href 与徽标。

## <a id="3"></a>3. 八股速查 chapter-questions-eight-part（epq 组件）

- **定位**：八股文速查手册，50 条目，ID 前缀 `E`（如 `E01.01`）；用独立的 `epq-*` 组件体系，**不用 `qa-card` / `qa-layer`**。
- **TOC**：`toc-group`（分组）+ `toc-group-title` + `toc-number` 分层锚点。
- **条目**：

  ```
  epq-section
  ├─ epq-header
  │    ├─ epq-badge         # E##.##
  │    ├─ epq-question      # 题干
  │    └─ epq-tags          # epq-tag 标签组
  ├─ 正文区
  │    ├─ .q / .a  问答块
  │    ├─ epq-section-title（子小节标题）
  │    ├─ epq-kp-list       关键点列表
  │    └─ epq-fu-list       延伸追问列表
  ```

- 携带难度 / 优先级徽标（`priority-p*` 54 处）；内容内联代码 `inline-code`、变量 `var` 使用频繁。页面引入 `shared/js/` 需按需（本页通常含 echarts / 表格组件）。

## <a id="4"></a>4. 场景题 chapter-questions-scenario（S 系列场景卡片）

- **定位**：场景设计题集，65 卡，ID 前缀 `S`（如 `S01.01`）。
- **卡片**：复用 `.qa-card` 外壳，但卡片内层为**场景专属序列**（非标准六层），顺序如下：

  | data-layer 对应 | 层标题 | 职责 |
  |-----------|--------|------|
  | (scenario) | 场景背景 | 业务 / 系统场景铺垫 |
  | (challenge) | 核心挑战 | 场景中真正的难点 |
  | (principle) | 分析框架 | 破题的思维框架 |
  | (practice ×2) | 解决方案 / 关键代码 | 落地方案 + 关键实现（拆为两层） |
  | (deep) | 深度追问 | 追问与边界 |
  | (pitfall) | 常见陷阱 | 易失分点 |
  | (extension) | 扩展补全 | 可选延伸 |

- **分层特征**：`practice` 通常一题出现**两层**（`解决方案` + `关键代码`），故全页 `qa-layer-title` 总量明显高于卡片数；`数据层` 标签存在 `scenario / challenge / deep / pitfall / principle / practice / extension` 的组合。
- **难度 / 优先级**：卡片带 `data-difficulty`（architect 41 / senior 17 / expert 7）与 `data-priority`。
- 新增场景题：`id = S{组}.{序}`；严格保持上述层序；`扩展补全`可选，其余各层建议齐备。

## <a id="5"></a>5. 安全 Checkpoint chapter-server-security-checkpoint（独立单页）

- **定位**：服务端开发安全自检清单，覆盖 OWASP Top 10:2025；**完全独立于导航体系**——不引入 `nav.js`、无侧栏 TOC、无 `chapter-nav-top`、无 `qa-card`。
- **样式**：仅引入 `assets/design-system.css`，页面内联 `<style>` 仅定义少量独占令牌覆盖（如 `--quote-bg`、`--quote-border`、`--th-bg`、`--zebra`、`--accent-soft`），其余取值自全局令牌。
- **内容结构**：传统「文档章节」式，标题层级清晰：
  - `h1`（`<title>` / 页首）→ `h2`(13 个主章节) → `h3`(57 个子节) → `h4`(7)；
  - 表格：`table-wrap > table`（23 张）；
  - 勾选清单：`.checklist`（6 份，自检 `☐` 项）；
  - 底部：`.footer-note`。
- 无 `Mermaid` / `ECharts`。CSS 资源引用路径为 `assets/design-system.css`（曾由 `security/` 目录迁入本目录，注意相对路径）。

## <a id="6"></a>6. 首页 index.html

- **定位**：全站入口导航页。
- **组件**：
  - `chapter-card`（20 张章节卡片）：`card-number` + `card-title` + `card-desc` + `card-tags` + `card-footer`；
  - `stat-item` / `stat-label` / `stat-number`：全站统计区；
  - `tag` / `tag-cat` / `tag-cloud` / `trend-section`：知识点标签云与趋势块。
- 每张章节卡片须链接到对应 `chapter-*.html`，卡片上的 `card-number / card-title / 难度` 应与目标章节页 `chapter-header` 一致。
- 引用更新规则：任何章节文件改名，须同步 `../../index.html` 与 `../index.html`（两者路径写法不同：前者为页面级相对路径）。

---

## 附：独享体系速查对照

| 页面 | 外壳 | 内容单元 | ID 前缀 | 难度 | 优先级 | nav.js |
|------|------|----------|:---:|:---:|:---:|:---:|
| chapter-01~15（标准） | page-wrapper + sidebar | `qa-card` 六层 | `C##.##` | ✔ | ✔ | ✔ |
| chapter-core-methodology | 同标准外壳 | `qa-card` 三层（insight/principle/application） | `M##.##` | 仅架构/专家 | ✘ | ✔ |
| chapter-overview-priority | – | `ov-*` 矩阵 | – | ✔ | ✔ | ✔ |
| chapter-questions-eight-part | – | `epq-*` 问答速查 | `E##.##` | ✔ | ✔ | ✔ |
| chapter-questions-scenario | – | `qa-card` 场景层 | `S##.##` | ✔ | ✔ | ✔ |
| chapter-server-security-checkpoint | 独立单页 | 章节式 h2/h3 + 表格 + checklist | – | – | – | ✘ |
| index | – | chapter-card / stat / tag-cloud | – | – | – | ✔ |