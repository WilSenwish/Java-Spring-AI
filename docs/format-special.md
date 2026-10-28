# 特殊章节独享格式规则（format-special.md）

本章，除标准 QA 章节（chapter-01 ~ 15）外的特殊页 / `nav-*` 聚合页各有**独享格式体系**，互不通用。编写 / 修改时可据此逐类对照。无论哪类，均遵循 `format-shared.md` 的底层规则（设计令牌、`.nojekyll`、资源按需载入、Mermaid 转义铁律）。卡数一律以 SSOT `docs/kb-counts.json` 为准，本文尽量用 `data-kb-count` 位或「以宿主页实计为准」表述。

---

## 目录

1. [核心方法论 chapter-core-methodology（M 系列）](#1)
2. [优先级大盘 nav-overview-priority（ov 组件）](#2)
3. [核心原理速查 chapter-questions-eight-part（epq 组件）](#3)
4. [场景题 chapter-questions-scenario（S 系列场景卡片）](#4)
5. [安全 Checkpoint nav-server-security-checkpoint（独立单页）](#5)
6. [工程化要点 chapter-engineering-practices（G 系列）](#6)
7. [首页 index.html](#7)
8. [生产踩坑 / AI 纵深 / 垂直领域 / 速查清单](#8)

---

## <a id="1"></a>1. 核心方法论 chapter-core-methodology（M 系列）

- **定位**：全库框。C/E/S 是领域细枝，G 是门禁化的器，K 是器失效的反例；本篇提供可挂载的道/法/术/势（器**不单列** Module）。势已独立为 **M16 维度**（势定律 11 卡）。开篇含五层定义、同一词跨层三例（`#hang-cross`）与四种错位（`#hang-misalign`）；**不再维护**全库挂网总表（`#hang-master`）、组级 `.mod-hang` 五列下挂、图 0d 层带（`.layer-hang`）——导航以侧栏 TOC / 卡号锚点 / 开篇竖切为准（2026-10-27 清除）。<span class="kb-count" data-kb-count="methodology" data-kb-pos="P16">145</span> 张卡片，ID 前缀 `M`（如 `M01.01`），按模块 **`M01~M16` 共 16 组**分层侧边目录。
- **卡片**：仍用 `.qa-card`，但**不采用标准六层**，改用三层**单向堆叠**：

  | data-layer | 层标题 | 职责 |
  |-----------|--------|------|
  | `insight` | 核心洞察 | 一句话道破的公理 / 视角 |
  | `principle` | 原理映射 | 把公理落到工程化手段 |
  | `application` | 工程表达 | 技术沟通中的表达话术 / 姿态 |

- **难度**：**不适用 —— M 卡不分难度等级**（2026-09-16 长官决策：移除 `data-difficulty`、难度计数键与「方法论难度三级求和」不变式）。本篇合计 <span class="kb-count" data-kb-count="methodology" data-kb-pos="P17">145</span> 卡。
- **优先级**：**属性侧**仅部分卡片携带 `data-priority`（分子/分母以 SSOT 键 `methodology_with_priority` / `methodology` 为准，**勿写死**；展示位在 `format-shared.md` §3.2）；**可见徽标侧不呈现**（同日决策：M/G/K 去等级与优先级徽标）。不属于全站题目优先级口径（P0/P1/P2 统计进入 `total` 的 C+A+E+S+D）。
- **题目头**：`qa-badge`（M01.01）+ `qa-question`（条目标题，**不带难度/优先级徽标**）。
- **目录**：按模块分组的多段侧边目录；**分组标题必须**为 `<a class="toc-group-title" href="#…">`（禁止 `div`）：
  - 十六组 → `#m-group-01`～`#m-group-16`（与 Module 编号一致）
  - 条目锚点仍为 `M##.##`
- **导航**：顶/底 `chapter-nav-top` / `chapter-nav` 内容一致；左 `nav-home`「← 返回目录」、右 `nav-next`「工程化要点 →」；中间 `nav-center` 为「全部章节」（勿与左右重复链工程化）。
- 单条新增规则：`id = M{模块}.{序}`；`insight → principle → application` 三层层序固定。

## <a id="2"></a>2. 优先级大盘 nav-overview-priority（ov 组件）

- **定位**：知识点大盘与优先级矩阵页，无 `qa-card`，纯 `ov-*` 组件；服务于「按 P0/P1/P2 复习」的导航索引，**向 C/E/S/A/D 宿主页锚点转发**（M/G/K 不进本页）。文件名前缀 `nav-` = 非篇章题宿主。
- **结构层级**：

  ```
  ov-stats（ov-stat-num 顶部项数 = len(ov_stat_order)，当前 12；顺序见 `kb-counts.json` → `ov_stat_order`）
  ├─ 总量 / P0 / P1 / P2 / 专家 / 架构 / 高级
  ├─ 篇章C / AI纵深A / 核心原理E / 场景S / 垂直领域D
  ├─ （方法论 <span class="kb-count" data-kb-count="methodology" data-kb-pos="P18">145</span> 卡不在本页统计条，只在专篇页与各 index 呈现）
  ├─ ov-group（按优先级 P0/P1/P2）×3
  │    ├─ ov-group-title
  │    └─ ov-group-body
  │         └─ ov-subgroup（子组 = 优先级 × 难度）×9
  │              ├─ ov-subgroup-title (+ ov-stat-num/ov-stat-label)
  │              └─ ov-items
  │                   └─ ov-item × total（C+A+E+S+D 全覆盖）
  │                        ├─ ov-num        # 题号
  │                        ├─ ov-title      # 条目名
  │                        └─ ov-badges     # 难度 / 优先级徽标（**必须包裹**）
  ```

- 条目为链接卡片，点击跳转对应题目的站内锚点；改新题 / 更名页面时须同步本页 `ov-item` 的 href 与徽标。
- **插入排序**：P0→P2 / 组内专家→架构→高级 / 子组内类型序以 `validate_kb` 与 `conventions.md` §5.1.1 为准（含 A/D）。
- **`.ov-badges` 是硬结构**：难度徽标 + 优先级徽标须同处一个 `.ov-badges` 内（`.ov-badges { gap: 4px }`）；直接挂在 `.ov-item` 下会继承 `.ov-item { gap: var(--space-sm) }`，出现「同列徽标间距时宽时窄」。结构校验：`scripts/check_index_badges.py`。

## <a id="3"></a>3. 核心原理速查 chapter-questions-eight-part（epq 组件）

- **定位**：核心原理速查手册，卡数 = SSOT `basics`（当前页 `E01~E12` 共 12 组），ID 前缀 `E`（如 `E01.01`）；用独立的 `epq-*` 组件体系，**不用 `qa-card` / `qa-layer`**。
- **TOC**：`toc-group`（分组）+ `toc-group-title`（须为 `<a href="#epq-group-NN">` 可点击，跳到组导读；禁止 `div`）+ `toc-number` 分层锚点。
- **分组导读**：每组（E01~E12）在首题前有 `epq-group-head`（`epq-group-title` + `group-lead`）。`group-lead` 三块：① **本组知识链**（`group-lead-chain`：intro + 分阶段 `ol`，阶段说明写清因果与边界，禁止只剩箭头关键词）② **工程化要点**（`group-lead-points`，约 **7 条**，可执行口径）③ **本组思维模式**（`group-lead-mind`，约 **5 条**命名条目）。页底须有 `chapter-nav`（与顶栏内容一致）。
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

- 每条目携带难度 / 优先级徽标（全覆盖；分布以宿主页 `data-*` 实计与 SSOT 为准）。页面引入 `shared/js/` 需按需。

## <a id="4"></a>4. 场景题 chapter-questions-scenario（S 系列场景卡片）

- **定位**：场景设计题集，卡数 = SSOT `scenarios`，ID 前缀 `S`（如 `S01.01`）。
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
- **难度 / 优先级**：卡片带 `data-difficulty` 与 `data-priority`；分布以宿主页实计与 SSOT 为准，**勿在规范文写死分档数字**。
- 新增场景题：`id = S{组}.{序}`；严格保持上述层序；`扩展补全`可选，其余各层建议齐备。

## <a id="5"></a>5. 安全 Checkpoint nav-server-security-checkpoint（独立单页）

- **定位**：服务端开发安全自检清单，覆盖 OWASP Top 10:2025；**无 `qa-card`**；顶/底导航与篇章页一致（`chapter-nav-top` / `chapter-nav`：上一篇 / 核心方法论 / 全部章节 / 返回目录），并**引入 `nav.js`**。
- **布局 / 目录**：与篇章页一致，使用 `page-wrapper` + 左侧 `sidebar-toc`（「本篇目录」）+ `content-main`；禁止正文中置目录或浅蓝 `.toc` / `.doc-toc` 盒子。
- **样式**：仅引入 `assets/design-system.css`，页面内联 `<style>` 仅定义少量独占令牌与正文排版覆盖（如 `--quote-bg`、`--quote-border`、`--th-bg`、`--zebra`），其余取值自全局令牌。
- **内容结构**：传统「文档章节」式，标题层级清晰：
  - `h1`（`<title>` / 页首）→ `h2`(13 个主章节) → `h3`(57 个子节) → `h4`(7)；
  - 表格：`compare-table`（23 张，全部带 `class="compare-table"`）；
  - 勾选清单：`.checklist`（6 份，自检 `☐` 项）；
  - 底部：`.footer-note`。
- 无 `Mermaid` / `ECharts`。CSS 资源引用路径为 `assets/design-system.css`（曾由 `security/` 目录迁入本目录，注意相对路径）。


## <a id="6"></a>6. 工程化要点 chapter-engineering-practices（G 系列）

- **定位**：与方法论并列的工程门禁手册，卡数以 `kb-counts.json` → `engineering` 为准，ID 前缀 `G`（如 `G01.01`）；题目总量口径 = `total`（C+A+E+S+D）；工程化为专篇键，不设全站合计。
- **卡片**：与方法论相同三层（`insight` / `principle` / `application`）。
- **分组**：G01～G08 八组（发布回滚、可观测、容量、数据、缓存、调用预算、AI、安全）；每组正文载体为 `<section class="eng-group" id="G0N">`。
- **目录**：侧栏分组标题必须为 `<a class="toc-group-title" href="#G0N">`（禁止 `div`），与组 `id` 一一对应。
- **导航**：顶/底一致；左 `nav-prev`「← 核心方法论」、右 `nav-next`「优先级总览 →」；中间 `nav-center` 为「全部章节」（勿再重复链核心方法论）。

## <a id="7"></a>7. 首页 index.html


- **定位**：章节站入口导航页（`java-architect-interview/index.html`）。卡片顺序**允许人工编排**，不以文件名自然序强制重排；Agent 改卡时**保持现有 DOM 顺序**，除非用户明确要求调整位置。
- **当前卡片顺序**（手工编排，改动须同步本条；以页面 DOM 为准）：
  1. 全站题目优先级排序总览（`nav-overview-priority`）
  2. 知识点速查手册（`nav-overview-quick-list`）
  3. 核心方法论（通栏）
  4. 第 01～15 篇（网格）
  5. 高频核心原理 / 高频真实场景题
  6. AI 工程纵深
  7. 工程化要点 / 生产踩坑
  8. 垂直领域
  9. 服务端安全 Checkpoint
- **Hero `.meta-stats`**：多格统计（方法论 / 深度 Q&A / 核心原理 / 场景 / AI 纵深 / 工程化 / 踩坑 / 垂直领域等），键与 `data-kb-pos` 以 SSOT `positions` 为准。
- **组件**：
  - `chapter-card`：`card-number` + `card-title` + `card-desc` + `card-tags` + `card-footer`；**M/G/K 三张专篇卡不带 `card-tags`**
  - `stat-item` / `stat-label` / `stat-number`：统计区
  - `tag-cloud` / `trend-section`：须用 `<details class="… index-fold">` 包裹且默认折叠
- **难度徽标（`card-tags`）约定**：
  - **统一顺序**：有计数时按 **专家 → 架构 → 高级**；某档为 0 则省略。
  - **凡可按 `data-difficulty` 实计的卡片均须带 ×N**：篇章 01～15、核心原理、场景、AI 纵深、垂直领域、优先级总览（总览口径 = `total`）。**M/G/K 不写 `card-tags`**。
  - **无法实计的卡**（安全 Checkpoint 等）：只标档位文案，不写 ×N。
- 引用更新规则：任何章节文件改名，须同步根 `index.html` 与本目录 `index.html`、`nav-overview-*.html`。

## <a id="8"></a>8. 生产踩坑 / AI 纵深 / 垂直领域 / 速查清单

- **生产踩坑 `chapter-production-pitfalls.html`（K）**：与工程化同款三层卡（insight/principle/application）；G01～G08 对位的 K01～K08；专篇键 `pitfalls`，不进 `total`；侧栏组锚 `#K01`～`#K08`。
- **AI 工程纵深 `chapter-question-ai-engineering-deep.html`（A）**：独立轴，ID `A##.##`，组锚 `#a-group-NN`（A01–A26）；进 `total`（键 `ai_engineering_deep`）；须带难度/优先级；落位 overview。
- **垂直领域 `chapter-questions-domain.html`（D）**：ID `D##.##`，组锚 `#group-N`；进 `total`（键 `domain_questions`）；卡片变体接近场景轴；须带难度/优先级。
- **速查清单 `nav-overview-quick-list.html`**：`nav-` 聚合页，按知识点清单导航，转发宿主锚点；无独立题号体系。

---

## 附：独享体系速查对照

| 页面 | 外壳 | 内容单元 | ID 前缀 | 难度 | 优先级 | nav.js |
|------|------|----------|:---:|:---:|:---:|:---:|
| chapter-01~15（标准） | page-wrapper + sidebar | `qa-card` 六层 | `C##.##` | ✔ | ✔ | ✔ |
| chapter-core-methodology | 同标准外壳 | `qa-card` 三层 | `M##.##` | 不呈现 | 不呈现 | ✔ |
| chapter-engineering-practices | 同标准外壳 | `qa-card` 三层 | `G##.##` | 不呈现 | 不呈现 | ✔ |
| chapter-production-pitfalls | 同标准外壳 | `qa-card` 三层 | `K##.##` | 不呈现 | 不呈现 | ✔ |
| chapter-questions-eight-part | – | `epq-*` | `E##.##` | ✔ | ✔ | ✔ |
| chapter-questions-scenario | – | `qa-card` 场景层 | `S##.##` | ✔ | ✔ | ✔ |
| chapter-question-ai-engineering-deep | – | 纵深卡 / epq 组头 | `A##.##` | ✔ | ✔ | ✔ |
| chapter-questions-domain | – | 领域卡 | `D##.##` | ✔ | ✔ | ✔ |
| nav-overview-priority | – | `ov-*` 矩阵 | – | ✔ | ✔ | ✔ |
| nav-overview-quick-list | – | 速查清单 | – | – | – | ✔ |
| nav-server-security-checkpoint | page-wrapper + sidebar | h2/h3 + compare-table + checklist | – | – | – | ✔ |
| index | – | chapter-card / meta-stats / index-fold | – | 可计卡带 ×N | – | ✔ |

（「不呈现」= 页面不显示难度/优先级徽标；M/G/K 三行同一口径。）
