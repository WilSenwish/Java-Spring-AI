# 特殊章节独享格式规则（format-special.md）

本章，除标准 QA 章节（chapter-01 ~ 15）外的 6 类页面各有**独享格式体系**，互不通用。编写 / 修改时可据此逐类对照。无论哪类，均遵循 `format-shared.md` 的底层规则（设计令牌、`.nojekyll`、资源按需载入、Mermaid 转义铁律）。

---

## 目录

1. [核心方法论 chapter-core-methodology（M 系列）](#1)
2. [优先级大盘 chapter-overview-priority（ov 组件）](#2)
3. [核心原理速查 chapter-questions-eight-part（epq 组件）](#3)
4. [场景题 chapter-questions-scenario（S 系列场景卡片）](#4)
5. [安全 Checkpoint chapter-server-security-checkpoint（独立单页）](#5)
6. [工程化要点 chapter-engineering-practices（G 系列）](#6)
7. [首页 index.html](#7)

---

## <a id="1"></a>1. 核心方法论 chapter-core-methodology（M 系列）

- **定位**：核心思维方法论，91 张卡片，ID 前缀 `M`（如 `M01.01`），按模块 `M01~M12` 共 12 组分层侧边目录。
- **卡片**：仍用 `.qa-card`，但**不采用标准六层**，改用三层**单向堆叠**：

  | data-layer | 层标题 | 职责 |
  |-----------|--------|------|
  | `insight` | 核心洞察 | 一句话道破的公理 / 视角 |
  | `principle` | 原理映射 | 把公理落到工程化手段 |
  | `application` | 工程表达 | 技术沟通中的表达话术 / 姿态 |

- **难度**：卡片带 `data-difficulty`：架构级 49 / 专家级 23 / 高级开发 3（合计 91）。
- **优先级**：**部分卡片（39/91）以双编码携带**优先级（`data-priority` + 提问行 `priority-p*` 徽标各 31 处），其余 52 卡不带；不计入全站题目优先级口径（92/209/58 = 359）。
- **题目头**：`qa-badge`（M01.01）+ `qa-question`（条目标题 + `difficulty` 视觉标签）；携带优先级的卡片另加 `priority-p*` 徽标。
- **目录**：按模块分组的多段侧边目录；**分组标题必须**为 `<a class="toc-group-title" href="#…">`（禁止 `div`）：
  - 元思维组 ①～⑥ → `#m-group-01`～`#m-group-06`（正文 `.m-subgroup-title` 带同名 `id`）
  - 五大主题 + 附录 → `#hc-section` / `#ha-section` / `#hp-section` / `#sec-section` / `#ir-section` / `#iv-section`
  - 条目锚点仍为 `M##.##`
- **导航**：顶/底 `chapter-nav-top` / `chapter-nav` 内容一致；左 `nav-home`「← 返回目录」、右 `nav-next`「工程化要点 →」；中间 `nav-center` 为「全部章节 → 本章思维导图」（勿与左右重复链工程化）。
- 单条新增规则：`id = M{模块}.{序}`；`insight → principle → application` 三层层序固定。

## <a id="2"></a>2. 优先级大盘 chapter-overview-priority（ov 组件）

- **定位**：知识点大盘与优先级矩阵页，无 `qa-card`，纯 `ov-*` 组件；服务于「按 P0/P1/P2 复习」的导航索引，**向 `questions-*`、`chapter-*` 内页锚点转发**。
- **结构层级**：

  ```
  ov-stats（两行统计；ov-stat-num 顶部 11 项 + 9 子组标题计数 = 全页 20 处；顺序见 `kb-counts.json` → `ov_stat_order`）
  ├─ ov-stats-row ① 题目总数 / 方法论 91 / P0 / P1 / P2
  ├─ ov-stats-row ② 专家级 / 架构级 / 高级开发 / 章节题 / 核心原理 / 场景题
  ├─ ov-group（按优先级 P0/P1/P2）×3
  │    ├─ ov-group-title
  │    └─ ov-group-body
  │         └─ ov-subgroup（子组 = 优先级 × 难度）×9
  │              ├─ ov-subgroup-title (+ ov-stat-num/ov-stat-label)
  │              └─ ov-items
  │                   └─ ov-item ×359
  │                        ├─ ov-num        # 序号
  │                        ├─ ov-title      # 条目名
  │                        └─ ov-badges     # 难度 / 优先级徽标
  ```

- 条目为链接卡片，点击跳转对应题目的站内锚点；改新题 / 更名页面时须同步本页 `ov-item` 的 href 与徽标。

## <a id="3"></a>3. 核心原理速查 chapter-questions-eight-part（epq 组件）

- **定位**：核心原理速查手册，61 条目（`E01~E12` 共 12 组），ID 前缀 `E`（如 `E01.01`）；用独立的 `epq-*` 组件体系，**不用 `qa-card` / `qa-layer`**。
- **TOC**：`toc-group`（分组）+ `toc-group-title`（须为 `<a href="#epq-group-NN">` 可点击，跳到组导读；禁止 `div`）+ `toc-number` 分层锚点。
- **分组导读**：每组（E01~E12）在首题前有 `epq-group-head`（`epq-group-title` + `group-lead`）。`group-lead` 三块：① **本组知识链**（`group-lead-chain`：intro + 分阶段 `ol`，阶段说明写清因果与边界，禁止只剩箭头关键词）② **工程化要点**（`group-lead-points`，约 **7 条**，可执行口径）③ **本组思维模式**（`group-lead-mind`，约 **5 条**命名条目）。页底须有 `chapter-nav`（与顶栏内容一致：返回目录 / 核心方法论 / 全部章节 / 场景题）。
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

- 每条目携带难度 / 优先级徽标（`data-priority` p0 20 / p1 33 / p2 8 = 61 全覆盖）；内容内联代码 `inline-code`、变量 `var` 使用频繁。页面引入 `shared/js/` 需按需（本页通常含 echarts / 表格组件）。

## <a id="4"></a>4. 场景题 chapter-questions-scenario（S 系列场景卡片）

- **定位**：场景设计题集，70 卡，ID 前缀 `S`（如 `S01.01`）。
- **分组导读**：每个 `scenario-group` 在 `group-title` 后插入 `group-lead`（结构与核心原理页一致：本组知识链 intro+`ol` / 工程化要点 / 本组思维模式）；侧栏 `toc-group-title` 须为 `<a href="#group-N">`（禁止 `div`）。
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
- **难度 / 优先级**：卡片带 `data-difficulty`（architect 43 / senior 17 / expert 7）与 `data-priority`（p0 21 / p1 26 / p2 20）。
- 新增场景题：`id = S{组}.{序}`；严格保持上述层序；`扩展补全`可选，其余各层建议齐备。

## <a id="5"></a>5. 安全 Checkpoint chapter-server-security-checkpoint（独立单页）

- **定位**：服务端开发安全自检清单，覆盖 OWASP Top 10:2025；**无 `qa-card`**；顶/底导航与篇章页一致（`chapter-nav-top` / `chapter-nav`：上一篇 / 核心方法论 / 全部章节 / 思维导图 / 返回目录），并**引入 `nav.js`**。
- **布局 / 目录**：与篇章页一致，使用 `page-wrapper` + 左侧 `sidebar-toc`（「本篇目录」）+ `content-main`；禁止正文中置目录或浅蓝 `.toc` / `.doc-toc` 盒子。
- **样式**：仅引入 `assets/design-system.css`，页面内联 `<style>` 仅定义少量独占令牌与正文排版覆盖（如 `--quote-bg`、`--quote-border`、`--th-bg`、`--zebra`），其余取值自全局令牌。
- **内容结构**：传统「文档章节」式，标题层级清晰：
  - `h1`（`<title>` / 页首）→ `h2`(13 个主章节) → `h3`(57 个子节) → `h4`(7)；
  - 表格：`compare-table`（23 张，全部带 `class="compare-table"`）；
  - 勾选清单：`.checklist`（6 份，自检 `☐` 项）；
  - 底部：`.footer-note`。
- 无 `Mermaid` / `ECharts`。CSS 资源引用路径为 `assets/design-system.css`（曾由 `security/` 目录迁入本目录，注意相对路径）。


## <a id="6"></a>6. 工程化要点 chapter-engineering-practices（G 系列）

- **定位**：与方法论并列的工程门禁手册，**24 卡**，ID 前缀 `G`（如 `G01.01`）；**不计入题目总量 365**，计入 `sum_all`。
- **卡片**：与方法论相同三层（`insight` / `principle` / `application`）。
- **分组**：G01～G08 八组（发布回滚、可观测、容量、数据、缓存、调用预算、AI、安全）；每组正文载体为 `<section class="eng-group" id="G0N">`。
- **目录**：侧栏分组标题必须为 `<a class="toc-group-title" href="#G0N">`（禁止 `div`），与组 `id` 一一对应。
- **导图**：`mind-engineering-practices.html`。
- **导航**：顶/底一致；左 `nav-prev`「← 核心方法论」、右 `nav-next`「优先级总览 →」；中间 `nav-center` 为「全部章节 → 本章思维导图」（勿再重复链核心方法论）。

## <a id="7"></a>7. 首页 index.html


- **定位**：全站入口导航页（`java-architect-interview/index.html`）。卡片顺序**允许人工编排**，不以文件名自然序强制重排；Agent 改卡时**保持现有 DOM 顺序**，除非用户明确要求调整位置。
- **当前卡片顺序**（手工编排，改动须同步本条）：
  1. 思维导图站入口（通栏）
  2. 核心方法论（通栏）
  3. 工程化要点（通栏）
  4. 核心原理速查（通栏）
  5. 场景题（通栏）
  6. 优先级总览（通栏）
  7. 第 01～15 篇（网格）
  8. 服务端安全 Checkpoint（通栏）
- **组件**：
  - `chapter-card`：`card-number` + `card-title` + `card-desc` + `card-tags` + `card-footer`
  - `stat-item` / `stat-label` / `stat-number`：全站统计区
  - `tag-cloud` / `trend-section`：知识点标签云与趋势块；**须用 `<details class="… index-fold">` 包裹且默认折叠**（不加 `open`），`<summary>` 内放原 `h2` 标题
- **难度徽标（`card-tags`）约定**：
  - **统一顺序**：有计数时按 **专家 → 架构 → 高级**；某档为 0 则省略该档（不写 `×0`）。
  - **凡可按 `data-difficulty` 实计的卡片均须带 ×N**：篇章 01～15、核心方法论、工程化、核心原理、场景、优先级总览（总览口径 = 篇章+核心原理+场景，合计 365）。
  - **无法实计的卡**（思维导图站入口、安全 Checkpoint 等无 `data-difficulty` 题卡）：只标档位文案，不写 ×N。
  - 数字须与目标页 `data-difficulty` 实计一致；改题难度后同步本页对应卡徽标。
- 每张章节卡片须链接到对应目标页；`card-number / card-title` 应与目标页一致；`card-footer` 题数须与目标页实卡数一致。
- 引用更新规则：任何章节文件改名，须同步根 `index.html` 与本目录 `index.html`（路径写法不同）。

---

## 附：独享体系速查对照

| 页面 | 外壳 | 内容单元 | ID 前缀 | 难度 | 优先级 | nav.js |
|------|------|----------|:---:|:---:|:---:|:---:|
| chapter-01~15（标准） | page-wrapper + sidebar | `qa-card` 六层 | `C##.##` | ✔ | ✔ | ✔ |
| chapter-core-methodology | 同标准外壳 | `qa-card` 三层（insight/principle/application） | `M##.##` | 架构/专家/高级 | 部分(31/75) | ✔ |
| chapter-overview-priority | – | `ov-*` 矩阵 | – | ✔ | ✔ | ✔ |
| chapter-questions-eight-part | – | `epq-*` 问答速查 | `E##.##` | ✔ | ✔ | ✔ |
| chapter-questions-scenario | – | `qa-card` 场景层 | `S##.##` | ✔ | ✔ | ✔ |
| chapter-server-security-checkpoint | page-wrapper + sidebar | 章节式 h2/h3 + compare-table + checklist | – | – | – | ✔ |
| chapter-engineering-practices | page-wrapper + sidebar | `qa-card` 三层（insight/principle/application） | `G##.##` | ✔ | – | ✔ |
| index | – | chapter-card / stat / tag-cloud（`index-fold` 默认折叠） | – | 可计卡带 ×N（专家→架构→高级） | – | ✔ |
