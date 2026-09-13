# 题库结构约定（java-kb-expand 参考）

本文件编码 `java-architect-interview` 知识库的全部结构约定，供脚本与 Agent 直接取用。

## 1. 题号前缀与三级目录

- 篇章页：`chapter-core-methodology.html` 用 **M**（分组 M01~M12，共 91 卡，如 `M01.06` / `M12.01`；序章：M01~M05=核心哲学/通用核心思维模式/通用方法论/通用架构与工程原则/Java 生态思维，M12=生产与领域思维速查，M06~M10=高并发/高可用/高性能/安全/线上问题处理，M11=附录实战表达），`chapter-engineering-practices.html` 用 **G**（G01~G08，共 24 卡，方法论同款三层 insight/principle/application，不计入题目总量），`chapter-01~15` 用 **C**（如 `C10.26`）。
- 核心原理页：`E`（如 `E07.02`）。
- 场景页：`S`（如 `S04.06`），按 `group-N` 归组（微服务架构 / 并发 / 数据库 …）。
- 目录层级：页面篇章 / 分组 / 题号。

## 2. 篇章/核心原理卡片结构（`.qa-card`）

```html
<div class="qa-card" id="C10.26" data-difficulty="architect" data-priority="p1">
  <div class="qa-header">
    <div class="qa-badge">C10.26</div>
    <div class="qa-question">题目标题
      <span class="difficulty difficulty-architect">架构级</span>
      <span class="priority priority-p1">P1</span>
    </div>
  </div>
  <div class="qa-layer" data-layer="essence"><div class="qa-layer-title">本质问题</div><div class="qa-layer-body">…</div></div>
  <div class="qa-layer" data-layer="principle">…</div>
  <div class="qa-layer" data-layer="practice">…</div>
  <div class="qa-layer" data-layer="deep">…</div>
  <!-- 可选扩展层 -->
  <div class="qa-layer" data-layer="extension">…</div>
</div>
```

- `data-difficulty` 取值：`expert`（专家级）/ `architect`（架构级）/ `senior`（高级开发）。
- `data-priority` 取值：`p0` / `p1` / `p2`（**P3 已废除**）。
- 双编码一致：卡片 `data-priority="p*"` 属性 **与** 可见徽标 `<span class="priority priority-p*">P*</span>` 必须同步，禁止只改其一。
- `qa-layer` 合法 `data-layer` 取值（在 `assets/design-system.css`）：`essence` / `evolution` / `principle` / `practice` / `deep` / `pitfall` / `extension` / `production` / `scenario` / `evaluation` / `insight` / `application` / `challenge`。
- 常用组件类：`compare-table`（对比表）、`code-block`/`pre>/code`（代码）、`callout callout-pitfall`（警示）、`inline-code`。

## 3. 场景题结构（`scenario-group` / `qa-layer`）

场景页按 `group-N` 分组的 `<section class="scenario-group" id="group-N">`，组内每题为 `.qa-card`（id=`Sxx.xx`）。标准七层：
`scenario` / `challenge` / `principle` / `practice` / `deep` / `pitfall` / `insight`。插入新场景题时定位「下一组」的 `<section class="scenario-group" id="group-N+1">` 锚点（注意该标签在列 0 常无缩进）。

## 4. 导图节点结构（`mind-xx-*.html`）

```html
<details class="map-card">
  <summary>C10.26 标题</summary>
  <div class="map-body-text">一句话要点描述</div>
  <div class="map-tags"><span class="map-tag t-c">章节</span><span class="map-tag t-c">配置热刷新</span></div>
</details>
```
- `map-tag` 类别：`t-c`（章节）/ `t-e`（核心原理）/ `t-s`（场景）。
- 插入新节点后，更新该页顶部 `主干 Cxx.01–Cxx.N` 范围与底部 `map-note`（并入清单，如 `S04.01~06`），并同步 `mind/index.html` 对应卡片 `card-foot`（见 §5.4）。
- `mind/index.html` 顶部 `idx-meta`（5 格，随计数同步）：① 组成 `1+1+15+1`（方法论+工程化+篇章+安全）② 导图页数 **18** ③ 方法论卡数 ④ 工程化卡数 ⑤ 题量 `N篇章+N核心原理+N场景`（如 `229+64+72`）。

## 5. 4 份聚合统计页字段名

### 5.1 `chapter-overview-priority.html`（优先级总览）
- `ov-stat-num` 顺序（**11 个**，校验权威三源；顺序以 `kb-counts.json` 的 `ov_stat_order` 为准；**方法论紧随总量**，勿遗漏；取值见 §6 COUNTS 块）：
  1. 总量
  2. 方法论
  3. P0
  4. P1
  5. P2
  6. 专家级
  7. 架构级
  8. 高级开发
  9. 篇章题数
  10. 核心原理题数
  11. 场景题数
- 9 子组标题：`<h3 class="ov-subgroup-title">专家级 · 10 题</h3>` 格式，按 **优先级×难度** 排列（P0/P1/P2 各含 专家级/架构级/高级开发），求和须各自等于 P0/P1/P2 与难度三级。
- 每个 ov-item：`<div class="ov-item" …><span class="priority priority-pX">…</span><span class="difficulty difficulty-architect">…</span><span class="ov-src">第X篇</span>…</div>`，与章节页卡片一一对应。

### 5.2 项目根 `Java Spring AI/index.html`（全量快照）
- 统计块 `stat-number`：深度Q&A / 核心原理 / 场景 / 方法论 / 工程化各自计数、合计（= 题数 + 方法论 + 工程化，如 365+91+24=480）、全站 N 题。
- 每题一个 `<li class="q-item">…，<span class="q-id">ID</span>…，<span class="q-tags"><span class="difficulty">…</span><span class="priority priority-pX">PX</span></span></li>`；新增题须在对应 ID 的 li 后插入。
- per-chapter / per-group `dir-count` / `dir-group-count`：**必须等于**紧随其后的 `ul.q-list` 内卡片数；各篇章 `dir-count` 求和 = 篇章总数（229）。
- 方法论目录结构（平级 `dir-group`，禁止嵌套）：序章①~⑤ → **⑥ 生产与领域思维速查（M12，16 卡）** → 一~五主题（M06~M10）→ 附录（M11）。**禁止**把 M12 嵌进「一、高并发」。

### 5.3 `java-architect-interview/index.html`（章节导航）
- `stat-number`：深度Q&A / 核心原理 / 场景 / 方法论 / 工程化、全站 N 道题目。
- 每篇章 `<div class="chapter-card">…<div class="card-footer"><span>N 题</span>…</div></div>`，`N` = 该章 `C##.##` 卡片数（与根 index `dir-count` 一致）。
- **不枚举单题 ID**（无 `Cxx.xx`/`Sxx.xx` li）——校验时落位=False 属预期。

### 5.4 `java-architect-interview-mind/index.html`（导图导航）
- 顶部 `idx-meta` 固定 **5** 格（`.idx-meta` 五列；窄屏两列）：
  1. `1+1+15+1` — 方法论 + 工程化要点 + 篇章 + 服务端安全手册
  2. `18` — 思维导图页（mind-01~15 + mind-core + mind-engineering + mind-security）
  3. 方法论卡片数（`methodology`，P08）
  4. 工程化要点卡片数（`engineering`，P26）
  5. `N+N+N` — Q&A · 原理 · 场景（如 `229+64+72`）
- 每张卡片底部 `card-foot` 计数口径（改题后必须同步）：
  - **篇章卡 mind-01~15**：`章节 N` = 对应 `chapter-NN` 的 C 卡数；`原理 N` / `场景 N` = 该 mind 页 `<summary>` 中实际列出的 E / S 卡数（无则省略该 chip）。
  - **方法论卡**：`91 卡 · 12 组`（M01~M12）。
  - **工程化卡**：`24 卡 · 8 组`（G01~G08）。
  - **安全手册卡**：`手册 7 章` + 该 mind 页并入的原理/场景数。

### 5.5 场景 / 核心原理页分组计数
- 场景页正文 `span.group-count`、根 index 场景区 `dir-group-count`，均须等于该组 `S##.##` 实际题数（当前：5/6/5/6/5/6/7/8/5/5/6/8）。
- 核心原理页各组实际题数（当前：4/4/8/8/4/6/10/4/6/6/5/8）；根 index 对应 `dir-group-count` 同步。
- **散文计数位**：页头/来源段「本页 N 道 / 高频核心原理 N 题」等必须登记为 `kb-counts.json` positions（含 P27–P42），改数走 `sync_counts.py bump`；`validate_kb.py` 第 0 步强制 `sync_counts check`。
## 6. 权威计数示例（2026-09-03 OPT-A 后固化）

<!-- COUNTS:BEGIN 由 scripts/sync_counts.py render 生成，勿手改 -->
- 题目总量 **379** = 篇章 234 + 核心原理 73 + 场景 72
- 优先级 **P0=94 / P1=227 / P2=58**（求和 = 379）
- 难度 **专家 46 / 架构 187 / 高级开发 146**（求和 = 379）
- 方法论 **91 卡**（M01~M12），不计入 379
- 工程化 **24 卡**（G01~G08），不计入 379；全站合计 **494** = 题目 + 方法论 + 工程化
- 方法论细分：带优先级 45/91；难度 专家 26 / 架构 61 / 高级开发 4

计数位（改数须全部同步，由 sync_counts.py check 自动核查）：

| 编号 | 载体 | 说明 |
|---|---|---|
| P01 | `index.html` | 根 index 方法论统计卡 |
| P02 | `index.html` | 根 index 方法论分组题数 |
| P03 | `java-architect-interview/index.html` | 章节 index 方法论统计卡 |
| P04 | `java-architect-interview/index.html` | 章节 index card-footer 方法论数 |
| P05 | `java-architect-interview/index.html` | 章节 index card-footer 篇章题数 |
| P06 | `java-architect-interview/chapter-core-methodology.html` | 方法论页页头副标题卡数 |
| P07 | `java-architect-interview/chapter-overview-priority.html` | overview ov-stat-num 11 项（顺序见 ov_stat_order） |
| P08 | `java-architect-interview-mind/index.html` | mind index idx-meta 方法论卡片 |
| P09 | `java-architect-interview-mind/mind-core-methodology.html` | mind-core-methodology 尾注 |
| P10 | `java-architect-interview/docs/README.md` | docs/README.md 文件表方法论数 |
| P11 | `java-architect-interview/docs/README.md` | docs/README.md 难度分布段 |
| P12 | `java-architect-interview/docs/README.md` | docs/README.md 方法论带优先级数（分子） |
| P13 | `java-architect-interview/docs/README.md` | docs/README.md 方法论带优先级数（分母） |
| P14 | `java-architect-interview/docs/format-shared.md` | docs/format-shared.md 分子 |
| P15 | `java-architect-interview/docs/format-shared.md` | docs/format-shared.md 分母 |
| P16 | `java-architect-interview/docs/format-special.md` | docs/format-special.md 定位段 |
| P17 | `java-architect-interview/docs/format-special.md` | docs/format-special.md 难度段合计 |
| P18 | `java-architect-interview/docs/format-special.md` | docs/format-special.md ov-stats 段 |
| P19 | `java-architect-interview/chapter-overview-priority.html` | overview 页脚 篇章题数 |
| P20 | `java-architect-interview/chapter-overview-priority.html` | overview 页脚 核心原理数 |
| P21 | `java-architect-interview/chapter-overview-priority.html` | overview 页脚 场景题数 |
| P22 | `java-architect-interview/chapter-overview-priority.html` | overview 页脚 题目总量 |
| P23 | `index.html` | 根 index 工程化统计卡 |
| P24 | `java-architect-interview/index.html` | 章节 index 工程化统计卡 |
| P25 | `java-architect-interview/chapter-engineering-practices.html` | 工程化页页头 meta 卡数 |
| P26 | `java-architect-interview-mind/index.html` | mind index idx-meta 工程化要点卡片 |
| P27 | `java-architect-interview/chapter-questions-scenario.html` | 场景页开篇散文题数（防漂移） |
| P28 | `java-architect-interview/chapter-core-methodology.html` | 方法论页来源段篇章题数 |
| P29 | `java-architect-interview/chapter-core-methodology.html` | 方法论页来源段场景题数 |
| P30 | `java-architect-interview/chapter-core-methodology.html` | 方法论页来源段核心原理数 |
| P31 | `java-architect-interview/chapter-questions-eight-part.html` | 核心原理页 title 散文题数 |
| P32 | `java-architect-interview/chapter-questions-eight-part.html` | 核心原理页 h1 题数 |
| P33 | `java-architect-interview/chapter-questions-eight-part.html` | 核心原理页 meta 题目数 |
| P34 | `java-architect-interview/index.html` | 章节 index 核心原理卡标题 |
| P35 | `index.html` | 根 index 核心原理 dir-count |
| P36 | `index.html` | 根 index 题目总数 |
| P37 | `index.html` | 根 index 合计 |
| P38 | `index.html` | 根 index 核心原理统计 |
| P39 | `java-architect-interview/index.html` | 章节 index 核心原理统计卡 |
| P40 | `java-architect-interview/index.html` | 章节 index 工程化卡散文总量 |
| P41 | `java-architect-interview/index.html` | 章节 index overview 卡散文总量 |
| P42 | `index.html` | 根 index overview 区 tagline |
<!-- COUNTS:END -->

## 7. 双站导航约定（简述）

- 章节页 `.chapter-nav-top`（顶部）+ `.chapter-nav`（底部），**顶底内侧 HTML 必须一致**。三槽结构：
  - 左：翻页 `nav-prev`（← 上一篇）或 `nav-home`（← 返回目录）
  - 中：`nav-center` 内 `nav-mind`（篇章页固定顺序：核心方法论 → 全部章节 → 本章思维导图）
  - 右：`nav-next`（下一篇 →）或收束用 `nav-home`（返回目录 →）
- 箭头统一字面量 `←` / `→`；回目录文案统一「返回目录」（禁止「返回首页」）；左右已链过的目标勿在 `nav-center` 重复。
- **侧栏分组标题**：凡带 `toc-group` 的页面，`toc-group-title` 必须是 `<a href="#…">`（禁止 `div`）；`nav.js` 会在条目高亮时同步给同组 `a.toc-group-title` 加 `.active`。锚点约定见 `docs/format-shared.md` §4.1。
- 导图页五按钮：翻页组（前一篇导图 `nav-prev` / 后一篇导图 `nav-next`，带 ←/→ 与具体篇章名）+ 居中组（全部章节/导图总览/本导图对应章节，`nav-mind`）。
- 顶部/底部按钮 `padding`/`font-size`/`gap` 须同步一致，避免高度差。
- 两站共用 `java-architect-interview/assets/design-system.css` 与 `nav.js`，一处修改惠及全部。

## 8. 章节站首页（`java-architect-interview/index.html`）

- **卡片顺序人工编排**：勿按文件名自动重排；现序为 导图 → 方法论 → 工程化 → 核心原理 → 场景 → 优先级总览 → ch01～15 → 安全。细则见 `docs/format-special.md` §7。
- **难度徽标**：可按目标页 `data-difficulty` 实计的卡片均写 **专家 → 架构 → 高级** 的 `×N`（0 档省略）；导图入口 / 安全等无难度题卡的只标档位。详见 `docs/format-special.md` §7。
- **技术栈全景 / 2026 技术趋势**：`<details class="tag-cloud|trend-section index-fold">`，**默认折叠**（不加 `open`）。
