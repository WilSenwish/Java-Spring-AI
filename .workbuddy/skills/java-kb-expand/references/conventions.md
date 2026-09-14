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


### 5.0.1 高级开发「桥接」口径（计入题目总量）

标签：`data-difficulty="senior"`，默认 `data-priority="p1"`。定位在初级高开与架构之间：

| | 偏「初级高开」 | **桥接（目标）** | 偏「架构」 |
|---|---|---|---|
| 问题 | 是什么 / API 怎么用 | **怎么落地排查与守边界** | 跨系统取舍 / 多方案权衡 |
| 答案 | 概念 + 示例 | **步骤、信号、参数、失败模式、回滚点** | 组织级/多域决策 |

一句话：高开能独立排障上线，但不必做平台级选型答辩。禁止空泛「要做好监控」；必须有可抄的排查顺序或参数/开关表。**桥接卡禁止薄卡**：除本质问题外，至少含原理映射 + 落地排查（有序步骤）+ 参数/开关或失败模式表，体量应对齐同章常规卡的可执行深度。

### 5.0.2 生产踩坑专篇 K（不计入题目总量）

与工程化 G 同级独立计数：

- 前缀 **`K##.##`**；页：`chapter-production-pitfalls.html` / `mind-production-pitfalls.html`
- 计数键 `pitfalls`；**单独计数**，不与 total 加总；**已废除 `sum_all` / 全站合计**
- **不进** overview；不计入 ≤400 题目预算
- 定位三角：M12=思维，G=门禁，K=事故翻车/识别/止血
- 卡片结构对齐 G（三层 + 事故叙事），不套 C 六层长文
- G/K 可按组扩容（如 G0x.04、K0x.02），**不计入** total/≤400；扩容后同步根 index 分组 `dir-group-count` 与 L0 `engineering`/`pitfalls`

### 5.1 `nav-overview-priority.html`（优先级总览）

> 文件名前缀 `nav-`：导航/聚合页，**不是**篇章题宿主。`ov_stat_order` 现为 **10 项**（total/P0–P2/难度三级/C·E·S），**不含** methodology；M/G/K 单独计数、不进 overview 统计条。P37（根合计）与 **sum_all / 全站合计**均已废止；M/G/K 仅各自 L0，不进跨大篇章加总。
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
- 9 子组标题：`<h3 class="ov-subgroup-title">专家级 · 10 题</h3>` 格式，按 **优先级×难度** 排列（P0/P1/P2 各含 专家级/架构级/高级开发），求和须各自等于 P0/P1/P2 与难度三级；**标题内题数 = 该子组 `ov-item` 实际个数**（易漏）。
- 每个 ov-item：`<a class="ov-item" href="…#ID">…<span class="ov-num">ID</span>…`，与章节页卡片一一对应（仅 C/E/S；M/G 不进 overview）。

#### 5.1.1 新卡插入排序（硬约束，2026-09-13 固化）

页面声明顺序：**P0 → P2**，组内 **专家级 → 架构级 → 高级开发**，子组内再 **篇章(C) → 核心原理(E) → 场景(S)**，同类内 **题号升序**。

插入算法（禁止「随便插在同优先级某卡后面」）：

1. 定位目标桶：`#group-p{0|1|2}` → 对应难度的 `<h3 class="ov-subgroup-title">`。
2. 在该子组已有 `ov-item` 中，按键 `(类型序 C=0,E=1,S=2, 题号字符串)` **升序**找到第一个「大于新卡」的项，插到其**前面**；若皆更小则插到该子组末尾（场景块之后、下一 `h3` / 子组结束之前）。
3. 同步：子组标题 `· N 题`、组标题 `必考核心|高频重点|进阶补充 · N 题`、顶栏 `ov-nav-cnt`、`ov-stat-num`、页头副标题「全站 N 道…」。
4. **禁止**仅按「同字母前缀相邻」插入（曾把 `E10.06` 插到 `E09.01` 前、把 `E06.06` 插到 `E09.03` 后，破坏题号升序）。
5. `validate_kb.py` 会校验：每个子组内 `ov-num` 序列对上述键单调不减；属性 `priority`/`difficulty` 必须与所在 section/subgroup 一致。

#### 5.1.2 三类占比（观察口径，非强制均分）

全局 C:E:S ≈ 篇章:原理:场景（当前 234:73:72）。**各 P×难度桶不要求三类均分**——P1 专家级几乎全是篇章、P2 场景占比偏高属现状。新增时优先按知识点真实优先级/难度归桶，勿为「凑均衡」改级；若某桶长期缺失 E 或 S，可在扩库时优先补该桶缺口，但仍服从内容定级。

#### 5.1.3 全站聚合/分组/页头页尾计数清单（2026-09-13 全站核查固化）

改题数或挪卡后，下列位必须与正文实际卡数一致（`sync_counts` positions **P01–P102** + `validate_kb` 3b/3b2/3c）：

| 层级 | 位置 | 规则 |
|---|---|---|
| SSOT | `kb-counts.json` | 唯一写源；`bump`/`apply`/`check` |
| overview | `ov-stat-num`×11、顶栏 `ov-nav-cnt`、组 `h2 · N 题`、子组 `h3 · N 题`、**类型三级 `ov-type-count`（篇章/核心原理/场景题）**、页头副标题、页脚数据来源 | 与 P0/P1/P2/总量/类型一致；子组 N=该组 ov-item 数；**每个难度子组必须拆成 C/E/S 三个（或有则建）`ov-type` 块，计数=块内题数** |
| 根 index | `stat-number`、`dir-count`、`dir-group-count`、overview tagline | `dir-*` 必须等于紧随 `q-list` 的 `q-item` 数 |
| 章节 index | `stat-number`、篇章 `card-footer N 题`、散文总量 | footer N=该章 C 卡数 |
| 核心原理页 | title/h1/meta「N 题」 | = basics；TOC 各组 li 数=该组 E 卡 |
| 场景页 | 「本页 N 道」、各组 `group-count` | **所有 `Sxx` 卡必须在对应 `#group-N` 的 `<section>` 内**（禁止卡在 `</section>` 与下一组之间）；`group-count`=组内卡数 |
| 导图 index | `N+N+N`、`card-foot` 章节/原理/场景 | 章节=C 卡；原理/场景=`<summary>` 内唯一 E/S 题号数 |
| 导图页 | mermaid 根节点「章节·原理·场景」 | 与上同口径；改并入清单后同步 |

审计脚本（只读）：`java-architect-interview/tmp/full_site_count_audit.py`。

#### 5.1.4 计数点分级与标记（2026-09-13 全量固化，禁止再漏）

样式：`assets/design-system.css` → `.kb-count`（虚线下划线）。改数入口仍是 `sync_counts.py bump/apply`。

##### 分级（先定级再决定是否打标）

| 级别 | 名称 | 必须打标？ | 典型载体 |
|---|---|---|---|
| **L0** | SSOT 权威位 | **必须** `data-kb-pos="Pxx"` | `kb-counts.json` → `positions`（当前 P01–P102）；`bump` 写回这些位 |
| **L1** | 聚合 UI | **必须** `kb-count` 或 `kb-count-local` | 页头/副标题/`chapter-meta`、`stat-number`、`ov-*`、`dir-*`/`group-count`、`card-footer`/`card-foot`/`card-desc` 中的题量·卡量、`map-note`/`subtitle`/`tagline`、统计表「卡数」列与合计、mind `idx-meta` |
| **L2** | 页内结构计数 | **必须** local（或已由 L0 覆盖） | overview `ov-type-count`、场景 `group-count`、方法论 `m-sub-count`/meth-table、mind `chip` 章节·原理·场景 |
| **L3** | 正文技术数字 | **不打标** | `qa-card` 正文、算法/JDK/HTTP 版本、对比表序号/年份、压测数据、「第 N 章」标题序号 |
| **LX** | Mermaid 节点 | 节点内**禁止**嵌 span；旁注/caption/`map-note` 挂同值 L0/L1 锚点 | `flowchart` 节点标签里的「N 卡」 |

##### 标记写法

| 级别 | 写法 |
|---|---|
| L0 | `<span class="kb-count" data-kb-count="{key}" data-kb-pos="Pxx">N</span>`；title 特例：属性打在 `<title class="kb-count" data-kb-pos="Pxx">`（勿嵌套 span，现 P31） |
| L0 · ov_series | 同上，另加 `data-kb-ov-i="0..10"`（P07，顺序=`ov_stat_order`） |
| L1/L2 | `<span class="kb-count kb-count-local" data-kb-count-local="{kind}">N</span>`；若该数字已是 L0 键则优先 L0 |

`data-kb-count-local` 常用 kind：`dir-count` / `dir-group` / `group-count` / `ov-subgroup` / `ov-type` / `chap-footer` / `chap-footer-diff` / `chap-footer-meta` / `mind-foot-c|e|s` / `mind-pages` / `meth-table` / `meth-group-count` / `site-meta` / `mind-note-local` 等。

##### 硬约定

1. **新增展示题量/卡量的数字**：先定级 → L0 则加 position + 标记；L1/L2 则至少 local；L3/LX 按上表。
2. **禁止**在 L1 容器里留下裸「N 题/卡/道/组」。
3. **改题后**跑 `sync_counts check`（覆盖全部 L0）+ `validate_kb.py`（0b 标记 + **0c L1 容器扫描** + 3b2/3c）。
4. 全量 L1 审计（只读）：可复用本轮脚本思路；临时报告 `java-architect-interview/tmp/kb_count_full_audit.json`。
5. overview 类型三级、方法论统计表、Mermaid 旁注：见下补充条。

补充：

- **overview `ov-type`**：每难度子组须拆篇章/核心原理/场景题；`ov-type-count` = 块内题数（`validate_kb` 3b2）。
- **方法论统计表**：`compare-table`「卡数」列 → `meth-table`；表尾合计 → L0（methodology）。
- **Mermaid**：节点纯文本；旁注挂锚点。

### 5.2 项目根 `Java Spring AI/index.html`（全量快照）
- 统计块 `stat-number`：深度Q&A / 核心原理 / 场景（跨大篇章口径=total）与方法论 / 工程化 / 踩坑**各自单独计数**；禁止「题数+M+G+K」式合计；「全站 N 题」仅指 total（C+E+S）。
- 每题一个 `<li class="q-item">…，<span class="q-id">ID</span>…，<span class="q-tags"><span class="difficulty">…</span><span class="priority priority-pX">PX</span></span></li>`；新增题须在对应 ID 的 li 后插入。
- per-chapter / per-group `dir-count` / `dir-group-count`：**必须等于**紧随其后的 `ul.q-list` 内卡片数；各篇章 `dir-count` 求和 = 篇章总数（见 COUNTS）。
- 方法论目录结构（平级 `dir-group`，禁止嵌套）：序章①~⑤ → **⑥ 生产与领域思维速查（M12，16 卡）** → 一~五主题（M06~M10）→ 附录（M11）。**禁止**把 M12 嵌进「一、高并发」。

### 5.3 `java-architect-interview/index.html`（章节导航）
- `stat-number`：深度Q&A / 核心原理 / 场景 / 方法论 / 工程化 / 踩坑各自计数；「全站 N 道」= total（仅 C+E+S）。
- 每篇章 `<div class="chapter-card">…<div class="card-footer"><span>N 题</span>…</div></div>`，`N` = 该章 `C##.##` 卡片数（与根 index `dir-count` 一致）。
- **不枚举单题 ID**（无 `Cxx.xx`/`Sxx.xx` li）——校验时落位=False 属预期。

### 5.4 `java-architect-interview-mind/index.html`（导图导航）
- 顶部 `idx-meta` 固定 **5** 格（`.idx-meta` 五列；窄屏两列）：
  1. `1+1+1+15+1` — 方法论 + 工程化 + 踩坑 + 篇章 + 服务端安全手册
  2. `19` — 思维导图页（+ mind-production-pitfalls）
  3. 方法论卡片数（`methodology`，P08）
  4. 工程化要点卡片数（`engineering`，P26）
  5. 生产踩坑卡片数（`pitfalls`，P93）
  6. `N+N+N` — Q&A · 原理 · 场景（取值见 COUNTS / P57–P59）
- 每张卡片底部 `card-foot` 计数口径（改题后必须同步）：
  - **篇章卡 mind-01~15**：`章节 N` = 对应 `chapter-NN` 的 C 卡数；`原理 N` / `场景 N` = 该 mind 页 `<summary>` 中实际列出的 E / S 卡数（无则省略该 chip）。
  - **方法论卡**：`91 卡 · 12 组`（M01~M12）。
  - **工程化卡**：`24 卡 · 8 组`（G01~G08）。
  - **安全手册卡**：`手册 7 章` + 该 mind 页并入的原理/场景数。
- `idx-meta` 题量表达式形如 `篇章+原理+场景`（取值见 COUNTS，勿写死旧数）。

### 5.5 场景 / 核心原理页分组计数
- 场景页正文 `span.group-count`、根 index 场景区 `dir-group-count`，均须等于该组 `S##.##` 实际题数（当前：5/6/5/6/5/6/7/8/5/5/6/8）。
- 核心原理页各组实际题数（当前：4/4/8/8/4/6/10/4/6/6/5/8）；根 index 对应 `dir-group-count` 同步。
- **散文计数位**：页头/来源段「本页 N 道 / 高频核心原理 N 题 / overview 全站 N 道…」等必须登记为 `kb-counts.json` positions（**P01–P102**），改数走 `sync_counts.py bump`；`validate_kb.py` 第 0 步强制 `sync_counts check`，第 0c 步扫描 L1 聚合 UI。
## 6. 权威计数示例（2026-09-03 OPT-A 后固化）

<!-- COUNTS:BEGIN 由 scripts/sync_counts.py render 生成，勿手改 -->
- 题目总量 **395** = 篇章 249 + 核心原理 73 + 场景 73
- 优先级 **P0=94 / P1=243 / P2=58**（求和 = 395）
- 难度 **专家 46 / 架构 188 / 高级开发 161**（求和 = 395）
- 方法论 **91 卡**（M01~M12），不计入 395
- 工程化 **64 卡**（G01~G08），单独计数，不计入 395
- 生产踩坑 **64 卡**（K01~K08），单独计数，不计入 395
- 口径：跨大篇章/聚合分组仅计「篇章+核心原理+场景」；M/G/K 各自单独计数；**不设全站合计**
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
| P07 | `java-architect-interview/nav-overview-priority.html` | overview ov-stat-num 11 项（顺序见 ov_stat_order） |
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
| P19 | `java-architect-interview/nav-overview-priority.html` | overview 页脚 篇章题数 |
| P20 | `java-architect-interview/nav-overview-priority.html` | overview 页脚 核心原理数 |
| P21 | `java-architect-interview/nav-overview-priority.html` | overview 页脚 场景题数 |
| P22 | `java-architect-interview/nav-overview-priority.html` | overview 页脚 题目总量 |
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
| P38 | `index.html` | 根 index 核心原理统计 |
| P39 | `java-architect-interview/index.html` | 章节 index 核心原理统计卡 |
| P40 | `java-architect-interview/index.html` | 章节 index 工程化卡散文总量 |
| P41 | `java-architect-interview/index.html` | 章节 index overview 卡散文总量 |
| P42 | `index.html` | 根 index overview 区 tagline |
| P43 | `java-architect-interview/nav-overview-priority.html` | overview 页头副标题题目总量（防漂移） |
| P44 | `java-architect-interview/nav-overview-priority.html` | overview 页头副标题篇章数 |
| P45 | `java-architect-interview/nav-overview-priority.html` | overview 页头副标题核心原理数 |
| P46 | `java-architect-interview/nav-overview-priority.html` | overview 页头副标题场景题数 |
| P47 | `java-architect-interview/nav-overview-priority.html` | overview 顶栏导航 P0 题数 |
| P48 | `java-architect-interview/nav-overview-priority.html` | overview 顶栏导航 P1 题数 |
| P49 | `java-architect-interview/nav-overview-priority.html` | overview 顶栏导航 P2 题数 |
| P50 | `java-architect-interview/nav-overview-priority.html` | overview P0 组标题题数 |
| P51 | `java-architect-interview/nav-overview-priority.html` | overview P1 组标题题数 |
| P52 | `java-architect-interview/nav-overview-priority.html` | overview P2 组标题题数 |
| P53 | `index.html` | 根 index 深度 Q&A 统计 |
| P54 | `index.html` | 根 index 场景题统计 |
| P55 | `java-architect-interview/index.html` | 章节 index 深度 Q&A 统计 |
| P56 | `java-architect-interview/index.html` | 章节 index 场景题统计 |
| P57 | `java-architect-interview-mind/index.html` | mind index 题量表达式篇章 |
| P58 | `java-architect-interview-mind/index.html` | mind index 题量表达式核心原理 |
| P59 | `java-architect-interview-mind/index.html` | mind index 题量表达式场景 |
| P60 | `java-architect-interview/chapter-core-methodology.html` | 方法论页副标题篇章题数 |
| P61 | `java-architect-interview/chapter-core-methodology.html` | 方法论页正文篇章题数 |
| P62 | `java-architect-interview/chapter-engineering-practices.html` | 工程化页副标题卡数 |
| P63 | `java-architect-interview/index.html` | 章节 index 工程化卡 footer 卡数 |
| P64 | `java-architect-interview/index.html` | 章节 index overview 卡 footer 题数 |
| P65 | `java-architect-interview/index.html` | 章节 index overview 卡 footer 专家数 |
| P66 | `java-architect-interview/index.html` | 章节 index overview 卡 footer 架构数 |
| P67 | `java-architect-interview/index.html` | 章节 index overview 卡 footer 高级数 |
| P68 | `java-architect-interview/index.html` | 章节 index 场景卡 desc 题数 |
| P69 | `java-architect-interview/index.html` | 章节 index 核心原理卡 footer 题数 |
| P70 | `java-architect-interview/index.html` | 章节 index 场景卡 footer 题数 |
| P71 | `java-architect-interview-mind/index.html` | mind index 方法论卡 footer 卡数 |
| P72 | `java-architect-interview-mind/index.html` | mind index 工程化卡 footer 卡数 |
| P73 | `java-architect-interview-mind/index.html` | mind index 工程化卡 desc 卡数 |
| P74 | `java-architect-interview/index.html` | 章节 index 方法论卡 footer 专家数 |
| P75 | `java-architect-interview/index.html` | 章节 index 方法论卡 footer 架构数 |
| P76 | `java-architect-interview/index.html` | 章节 index 方法论卡 footer 高级数 |
| P77 | `java-architect-interview-mind/mind-engineering-practices.html` | mind 工程化页副标题卡数 |
| P78 | `java-architect-interview-mind/mind-engineering-practices.html` | mind 工程化页尾注卡数 |
| P79 | `java-architect-interview-mind/mind-engineering-practices.html` | mind 工程化页尾注题目总量 |
| P80 | `java-architect-interview-mind/mind-engineering-practices.html` | mind 工程化页尾注方法论卡数 |
| P82 | `java-architect-interview/chapter-engineering-practices.html` | 工程化页 meta 不计入题目总量 |
| P83 | `java-architect-interview-mind/mind-engineering-practices.html` | mind 工程化页 Mermaid 旁注卡数 |
| P84 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 meta 合计卡数 |
| P85 | `java-architect-interview/chapter-core-methodology.html` | 方法论页统计表合计卡数 |
| P86 | `java-architect-interview/index.html` | 章节 index 方法论卡 desc 篇章题数 |
| P87 | `java-architect-interview/index.html` | 章节 index 工程化卡 desc 卡数 |
| P88 | `java-architect-interview/chapter-questions-scenario.html` | 场景页副标题题数 |
| P89 | `java-architect-interview-mind/mind-01-jvm-memory-classloading.html` | mind-01 尾注核心原理总量 |
| P90 | `index.html` | 根 index 踩坑统计卡 |
| P91 | `java-architect-interview/index.html` | 章节 index 踩坑统计卡 |
| P92 | `java-architect-interview/chapter-production-pitfalls.html` | 踩坑页页头 meta 卡数 |
| P93 | `java-architect-interview-mind/index.html` | mind index idx-meta 踩坑卡片 |
| P94 | `java-architect-interview/chapter-production-pitfalls.html` | 踩坑页副标题卡数 |
| P95 | `java-architect-interview/index.html` | 章节 index 踩坑卡 footer 卡数 |
| P96 | `java-architect-interview-mind/index.html` | mind index 踩坑卡 footer 卡数 |
| P97 | `java-architect-interview-mind/index.html` | mind index 踩坑卡 desc 卡数 |
| P98 | `java-architect-interview/chapter-production-pitfalls.html` | 踩坑页 meta 不计入题目总量 |
| P99 | `java-architect-interview-mind/mind-production-pitfalls.html` | mind 踩坑页副标题卡数 |
| P100 | `java-architect-interview-mind/mind-production-pitfalls.html` | mind 踩坑页尾注卡数 |
| P102 | `java-architect-interview/index.html` | 章节 index 踩坑卡 desc 卡数 |
| P103 | `java-architect-interview/index.html` | 章节 index 工程化卡 footer 架构数 |
| P104 | `java-architect-interview/index.html` | 章节 index 工程化卡 footer 高级数 |
| P105 | `java-architect-interview/index.html` | 章节 index 踩坑卡 footer 高级数 |
| P106 | `java-architect-interview/index.html` | 章节 index 工程化卡 footer 组数 |
| P107 | `java-architect-interview/index.html` | 章节 index 踩坑卡 footer 组数 |
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
