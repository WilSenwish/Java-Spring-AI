# 题库结构约定（java-kb-expand 参考）

本文件编码 `java-architect-interview` 知识库的全部结构约定，供脚本与 Agent 直接取用。

## 1. 题号前缀与三级目录

- 篇章页：`chapter-core-methodology.html` 用 **M**（分组 M01~M11，共 75 卡，如 `M01.06`；2026-09-04 序章 5 块升层重编号：M01~M05=核心哲学/通用核心思维模式/通用方法论/通用架构与工程原则/Java 生态思维，M06~M10=高并发/高可用/高性能/安全/线上问题处理，M11=附录实战表达），`chapter-01~15` 用 **C**（如 `C10.26`）。
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
- 插入新节点后，更新该页顶部 `主干 Cxx.01–Cxx.N` 范围与底部 `map-note`（并入清单，如 `S04.01~06`）。
- `mind/index.html` 题量表达式 `N篇章+N核心原理+N场景`（如 `220+58+67`），随计数变更同步。

## 5. 4 份聚合统计页字段名

### 5.1 `chapter-overview-priority.html`（优先级总览）
- `ov-stat-num` 顺序（**11 个**，校验权威三源；第 8 项为「方法论 75」，勿遗漏）：
  1. 总量（345）
  2. P0（90）
  3. P1（195）
  4. P2（60）
  5. 专家级（44）
  6. 架构级（160）
  7. 高级开发（141）
  8. 方法论（75）
  9. 篇章题数（220）
  10. 核心原理题数（58）
  11. 场景题数（67）
- 9 子组标题：`<h3 class="ov-subgroup-title">专家级 · 10 题</h3>` 格式，按 **优先级×难度** 排列（P0/P1/P2 各含 专家级/架构级/高级开发），求和须各自等于 P0/P1/P2 与难度三级。
- 每个 ov-item：`<div class="ov-item" …><span class="priority priority-pX">…</span><span class="difficulty difficulty-architect">…</span><span class="ov-src">第X篇</span>…</div>`，与章节页卡片一一对应。

### 5.2 项目根 `Java Spring AI/index.html`（全量快照）
- 统计块 `stat-number`：深度Q&A / 核心原理 / 场景 各自计数、合计（= 题数 + 方法论卡片，如 345+75=420）、全站 N 题。
- 每题一个 `<li class="q-item">…，<span class="q-id">ID</span>…，<span class="q-tags"><span class="difficulty">…</span><span class="priority priority-pX">PX</span></span></li>`；新增题须在对应 ID 的 li 后插入。
- per-chapter `dir-count`（各篇章题数），求和须等于篇章总数。

### 5.3 `java-architect-interview/index.html`（章节导航）
- `stat-number`：深度Q&A / 核心原理 / 场景、全站 N 道题目。
- 每篇章 `<div class="chapter-card">…<div class="card-footer">第X篇 · N 题</div></div>`，footer 计数随该篇章题数变更。
- **不枚举单题 ID**（无 `Cxx.xx`/`Sxx.xx` li）——校验时落位=False 属预期。

### 5.4 `java-architect-interview-mind/index.html`（导图导航）
- 题量表达式 `N篇章+N核心原理+N场景`，随计数同步；`mind 页计数 1+15+1` 与题量无关，勿动。

## 6. 权威计数示例（2026-09-03 OPT-A 后固化）

全站 **345** = 篇章 **220** + 核心原理 **58** + 场景 **67**；优先级 P0=**90** / P1=**195** / P2=**60**；难度 专家级 **44** / 架构级 **160** / 高级开发 **141**。统计口径为「篇章 + 核心原理 + 场景」三页，方法论页（75 张 M 卡）与概览页、安全卡页不计入题目数。任何同步后须满足：优先级三项和=总量、难度三项和=总量、类型三项和=总量。

## 7. 双站导航约定（简述）

- 章节页 `.chapter-nav-top`（顶部）+ `.chapter-nav`（底部），四按钮分两组：翻页组（前一篇/后一篇/返回目录，灰底）+ 居中组（全部章节/查看本章思维导图，浅蓝 `nav-mind`）。
- 导图页五按钮：翻页组（前一篇导图 `nav-prev` / 后一篇导图 `nav-next`，带 ←/→ 与具体篇章名）+ 居中组（全部章节/导图总览/本导图对应章节，`nav-mind`）。
- 顶部/底部按钮 `padding`/`font-size`/`gap` 须同步一致，避免高度差。
- 两站共用 `assets/design-system.css`，一处修改惠及全部。
