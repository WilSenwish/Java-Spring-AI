# 题库结构约定（java-kb-expand 参考）

本文件编码 `java-architect-interview` 知识库的全部结构约定，供脚本与 Agent 直接取用。

## 1. 题号前缀与三级目录

- 篇章页：`chapter-core-methodology.html` 用 **M**（分组 M01~M17，共 149 卡，如 `M01.02` / `M16.04`；道 M01–M02，法 M03–M07，术 M08–M15，势 M16（11 张势定律），附 M17（4 张表达与对齐）且 M12 在 TOC 收口、R2 仍标法），`chapter-engineering-practices.html` 用 **G**（G01~G08，卡数见 `engineering`，方法论同款三层 insight/principle/application，专篇键），`chapter-01~15` 用 **C**（如 `C10.26`）。
- 核心原理页：`E`（如 `E07.02`）。
- 场景页：`S`（如 `S04.06`），按 `group-N` 归组（微服务架构 / 并发 / 数据库 …）。
- 目录层级：页面篇章 / 分组 / 题号。

## 2. 篇章/核心原理卡片结构（`.qa-card`）

```html
<div class="qa-card" id="C10.26" data-difficulty="architect" data-priority="p1">
  <div class="qa-header">
    <div class="qa-badge">C10.26</div>
    <div class="qa-question">题目标题
      <span class="difficulty difficulty-architect">架构</span>
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

- `data-difficulty` 取值：`expert` / `architect` / `senior`（**仅 C/E/S 使用**；M/G/K 一律不用，见下条）。
- `data-priority` 取值：`p0` / `p1` / `p2`（**P3 已废除**）。
- 双编码一致：卡片 `data-priority="p*"` 属性 **与** 可见徽标 `<span class="priority priority-p*">P*</span>` 必须同步，禁止只改其一。
- **难度文案口径（全站唯一，2026-09-16 长官决策）**：
  - **标签位**一律短表 **专家 / 架构 / 高级**（`difficulty-expert` / `architect` / `senior`）。标签位 = 卡片 `.qa-question` 徽标、章节页头 `chapter-meta` 的 `高级 ×N / 架构 ×N / 专家 ×N`、总览 `.ov-stat-label` 与 `.ov-subgroup-title`、章节导航 `card-tags`、根 index `q-tags`、总览页脚排序说明、`format-shared` §3.1 的「文案」列。
  - **正文**用 **专家 / 架构师 / 高级开发**（称人/角色）；存量正文中把等级当定语用的写法（「架构级理解」「专家级深度」「专家级的技术判断力」，共 8 处）**保留不改、不再新增**。
  - 门禁：`validate_kb.py` **1j**（徽标文案白名单，可带 ` ×N`）。
- **难度配色口径（2026-09-16 晚修订，长官反馈「专家/架构区分度不明显」+「主要是颜色」）**：
  - 三档色相：`senior` = 蓝 `--accent`（`#2563eb`）；`architect` = 紫 `--accent2`（`#7c3aed`）；**`expert` = 青绿 `--diff-expert`**（浅色 `#0f766e` / 深色 `#2dd4bf`）。
  - **改前真因**：`expert` 与 `architect` 的 `color` **同为 `var(--accent2)`**、底色都是 10% 蓝紫浅色，仅边框透明度 0.2 / 0.3 之差 —— 专家等于借用了架构的紫。
  - 专家卡的 `border-left-color` 与 `qa-badge` 底色取 **`--diff-expert-solid`**（浅 `#0f766e` / 深 `#14b8a6`），**原「蓝→紫渐变」已废弃**。两个令牌拆开的原因：徽标底色承白字、胶囊文字是前景色，对比度要求相反，同一值无法兼顾（若用 `#0d9488` 做底色，白字仅 1.86:1）。
  - **色相避让**：难度胶囊与优先级胶囊在 `.qa-question` 内**紧邻同框**，故难度色相必须避开已占用色相 —— 蓝＝高级 + `P2`；紫＝架构 + `callout-deep`；红＝`P0`；琥珀＝`P1` + `callout-pitfall`；翡翠绿＝`callout-tip`。剩余可用即青绿。
  - 落地面：`design-system.css` 三处令牌（`:root` + 两处深色覆盖）+ 两条 `[data-difficulty="expert"]` 规则；全站 1252 枚徽标自动生效。`.layer-tag`（想/做/守）刻意沿用架构紫，**不随本次改动**。
- **`M`（方法论）/ `G`（工程化要点）/ `K`（生产踩坑）三类卡彻底取消难度分级（2026-09-16 长官决策，属性 / 徽标 / 计数三层一并移除）**：
  1. 三个专篇页（`chapter-core-methodology` / `chapter-engineering-practices` / `chapter-production-pitfalls`）的 `.qa-card` **不写 `data-difficulty`**（原 220 处已全清），`.qa-question` 内不写 `<span class="difficulty …">`；
  2. 根 index 的 M/G/K 三个区块共 **220 条 q-item** 连 `.q-tags` 空壳一并去掉（其内只有等级徽标）；章节导航 index 的三张专篇 `chapter-card` **不带 `.card-tags`**（原 M 3 枚 / G 2 枚 / K 1 枚）；
  3. `kb-counts.json` **不再有** `methodology_expert/architect/senior`、`engineering_architect/senior`、`pitfalls_senior` 六个键，**也不再有不变量**「方法论难度三级求和 = methodology」；全局 `counts.expert/architect/senior`（46/191/161 = 398）**只覆盖 C/E/S**。
  - **视觉后果**：`.qa-card[data-difficulty="architect"|"expert"]` 的紫左边框 / 青绿左边框、`.qa-badge` 配色不再命中 → M/G/K 220 张卡统一回落 `.qa-card` 默认蓝色左边框。若日后要给某专篇统一专色，须显式加页面级类，**勿再借难度属性**。
  - **不写**：M 卡 `data-priority`（2026-09-21 废除：属性无 CSS/JS 消费方，纯冗余）。新增 M/G/K 卡（含导航位）时**勿写 `data-difficulty`、勿贴难度徽标**。
  - 门禁：`validate_kb.py` **1k**（三专篇 `data-difficulty` 须 0）。
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

标签：`data-difficulty="senior"`（标签位文案 **高级**），默认 `data-priority="p1"`。定位在初级高开与架构之间：

| | 偏「初级高开」 | **桥接（目标）** | 偏「架构」 |
|---|---|---|---|
| 问题 | 是什么 / API 怎么用 | **怎么落地排查与守边界** | 跨系统取舍 / 多方案权衡 |
| 答案 | 概念 + 示例 | **步骤、信号、参数、失败模式、回滚点** | 组织级/多域决策 |

一句话：高开能独立排障上线，但不必做平台级选型答辩。禁止空泛「要做好监控」；必须有可抄的排查顺序或参数/开关表。**桥接卡禁止薄卡**：除本质问题外，至少含原理映射 + 落地排查（有序步骤）+ 参数/开关或失败模式表，体量应对齐同章常规卡的可执行深度。

### 5.0.2 生产踩坑专篇 K（专篇键 `pitfalls`）

与工程化 G 同级独立计数：

- 前缀 **`K##.##`**；页：`chapter-production-pitfalls.html` / `mind-production-pitfalls.html`
- 计数键 `pitfalls`；**单独计数**，不与 total 加总；**已废除 `sum_all` / 全站合计**
- **不进** overview；不属于 `total` / ≤400 题目预算
- 定位三角：M12=思维，G=门禁，K=事故翻车/识别/止血
- 卡片结构对齐 G（三层 + 事故叙事），不套 C 六层长文
- G/K 可按组扩容（如 G0x.04、K0x.02），扩容只改专篇键与对应 `struct`；同步根 index 分组与 L0 `engineering`/`pitfalls`

### 5.1 `nav-overview-priority.html`（优先级总览）

> 文件名前缀 `nav-`：导航/聚合页，**不是**篇章题宿主。`ov_stat_order` 现为 **10 项**（total/P0–P2/难度三级/C·E·S），**不含** methodology；M/G/K 单独计数、不进 overview 统计条。P37（根合计）与 **sum_all / 全站合计**均已废止；M/G/K 仅各自 L0，不进跨大篇章加总。
- `ov-stat-num` 顺序（**10 个**，校验权威三源；顺序以 `kb-counts.json` 的 `ov_stat_order` 为准；**不含 方法论**——方法论只在专篇页/各 index 呈现，不进本页统计条；取值见 §6 COUNTS 块）：
  1. 总量
  2. P0
  3. P1
  4. P2
  5. 专家
  6. 架构
  7. 高级
  8. 篇章题数
  9. 核心原理题数
  10. 场景题数
  （DOM 实测 `data-kb-ov-i` = 0…9 与上表逐项对应；渲染上 P2 之后换行。）
- 9 子组标题：`<h3 class="ov-subgroup-title">专家 · 10 题</h3>` 格式，按 **优先级×难度** 排列（P0/P1/P2 各含 专家/架构/高级），求和须各自等于 P0/P1/P2 与难度三级；**标题内题数 = 该子组 `ov-item` 实际个数**（易漏）。
- 每个 ov-item：`<a class="ov-item" href="…#ID">…<span class="ov-num">ID</span>…`，与章节页卡片一一对应（仅 C/E/S；M/G 不进 overview）。
  - **难度/优先级徽标必须包在 `<span class="ov-badges">` 内**：`<span class="ov-badges"><span class="difficulty …">…</span><span class="priority priority-pX">PX</span></span>`。漏包裹时两枚徽标直接成为 `.ov-item` 的 flex 子项，取 `.ov-item { gap: var(--space-sm) }`（大间距），而正常项取 `.ov-badges { gap: 4px }` → **页面上同列徽标间距时宽时窄**（2026-09-16 实测 15 条：C06.15、C07.16、C08.12、C09.17、C10.29/30、C11.26/27/28、C12.33/34/35、C13.14、C14.13、C15.12）。门禁 `scripts/check_index_badges.py`。

#### 5.1.1 新卡插入排序（硬约束，2026-09-13 固化）

页面声明顺序：**P0 → P2**，组内 **专家 → 架构 → 高级**，子组内再 **篇章(C) → 核心原理(E) → 场景(S)**，同类内 **题号升序**。

插入算法（禁止「随便插在同优先级某卡后面」）：

1. 定位目标桶：`#group-p{0|1|2}` → 对应难度的 `<h3 class="ov-subgroup-title">`。
2. 在该子组已有 `ov-item` 中，按键 `(类型序 C=0,E=1,S=2, 题号字符串)` **升序**找到第一个「大于新卡」的项，插到其**前面**；若皆更小则插到该子组末尾（场景块之后、下一 `h3` / 子组结束之前）。
3. 同步：子组标题 `· N 题`、组标题 `必考核心|高频重点|进阶补充 · N 题`、顶栏 `ov-nav-cnt`、`ov-stat-num`、页头副标题「全站 N 道…」。
4. **禁止**仅按「同字母前缀相邻」插入（曾把 `E10.06` 插到 `E09.01` 前、把 `E06.06` 插到 `E09.03` 后，破坏题号升序）。
5. `validate_kb.py` 会校验：每个子组内 `ov-num` 序列对上述键单调不减；属性 `priority`/`difficulty` 必须与所在 section/subgroup 一致。

#### 5.1.2 三类占比（观察口径，非强制均分）

全局 C:E:S ≈ 篇章:原理:场景（当前 234:73:72）。**各 P×难度桶不要求三类均分**——P1 专家几乎全是篇章、P2 场景占比偏高属现状。新增时优先按知识点真实优先级/难度归桶，勿为「凑均衡」改级；若某桶长期缺失 E 或 S，可在扩库时优先补该桶缺口，但仍服从内容定级。

#### 5.1.3 全站聚合/分组/页头页尾计数清单（2026-09-13 全站核查固化）

改题数或挪卡后，下列位必须与正文实际卡数一致（**位号清单以 `kb-counts.json` 的 `positions` 为唯一权威**——文档/脚本里**禁止写死位号范围**，写死必然滞后于新增；另见 `validate_kb` 3b/3b2/3c）：

| 层级 | 位置 | 规则 |
|---|---|---|
| SSOT | `kb-counts.json` | 唯一写源；`bump`/`apply`/`check` |
| overview | `ov-stat-num`×10、顶栏 `ov-nav-cnt`、组 `h2 · N 题`、子组 `h3 · N 题`、**类型三级 `ov-type-count`（篇章/核心原理/场景题）**、页头副标题、页脚数据来源 | 与 P0/P1/P2/总量/类型一致；子组 N=该组 ov-item 数；**每个难度子组必须拆成 C/E/S 三个（或有则建）`ov-type` 块，计数=块内题数** |
| 根 index | `stat-number`、`dir-count`、`dir-group-count`、overview tagline | `dir-*` 必须等于紧随 `q-list` 的 `q-item` 数 |
| 章节 index | `stat-number`、篇章 `card-footer N 题`、散文总量 | footer N=该章 C 卡数 |
| 核心原理页 | title/h1/meta「N 题」 | = basics；TOC 各组 li 数=该组 E 卡 |
| 场景页 | 「本页 N 道」、各组 `group-count` | **所有 `Sxx` 卡必须在对应 `#group-N` 的 `<section>` 内**（禁止卡在 `</section>` 与下一组之间）；`group-count`=组内卡数 |
| 导图 index | `N+N+N`、`card-foot` 章节/原理/场景 | 章节=C 卡；原理/场景=`<summary>` 内唯一 E/S 题号数 |
| 导图页 | mermaid 根节点「章节·原理·场景」 | 与上同口径；改并入清单后同步 |

审计脚本（只读）：`tmp/full_site_count_audit.py`。

#### 5.1.4 计数点分级与标记（2026-09-14：废除本地计数）

样式：`assets/design-system.css` → `.kb-count`（虚线下划线）。
改数入口：`sync_counts.py bump/apply`；结构键用 `bump struct.<key>=+1`。

##### 分级

| 级别 | 名称 | 必须打标？ | 典型载体 |
|---|---|---|---|
| **L0** | SSOT 权威位 | **必须** `data-kb-pos="Pxx"` + `data-kb-count` | `kb-counts.json` 的 `counts` / `struct` + `positions`；`bump`/`apply` 写回 |
| **L3** | 正文技术数字 | **不打标** | `qa-card` 正文、算法/JDK/HTTP 版本、对比表序号/年份、压测数据、「第 N 章」标题序号 |
| **LX** | Mermaid 节点 | 节点内**禁止**嵌 span；旁注/`map-note` 挂同值 L0 | `flowchart` 节点标签里的「N 卡」 |

**已废除**：`kb-count-local` / `data-kb-count-local`（旧 L1/L2「本地计数」）。凡页头、footer、desc、meta、overview 分组、场景 `group-count`、方法论表、mind chip 等展示题量/卡量，**一律 L0**，键落入 `counts` 或 `struct`，由 `sync_counts` 统一刷新。

##### 标记写法

| 级别 | 写法 |
|---|---|
| L0 · 全局键 | `<span class="kb-count" data-kb-count="total" data-kb-pos="Pxx">N</span>` |
| L0 · 结构键 | `<span class="kb-count" data-kb-count="struct.chap.idx.c01.n" data-kb-pos="Pxx">N</span>` |
| L0 · ov_series | 同上，另加 `data-kb-ov-i="0..10"`（P07，顺序=`ov_stat_order`） |
| title 特例 | 属性打在 `<title class="kb-count" data-kb-pos="Pxx">`（勿嵌套 span） |

##### 硬约定

1. **新增展示题量/卡量**：必须新增/复用 `kb-counts.json` 键 + `positions` + HTML `data-kb-pos`；**禁止**本地计数。
2. **零裸计数（全域覆盖，含正文）**：展示计数一律受门禁保护——**要么带 `data-kb-pos`，要么在 SSOT 显式豁免**。聚合 UI 容器内不得留裸「N 题/卡/道/组/项」；全域 `inline` 模式（如「M## 名（N）」）命中的数字同样不得裸奔；**通用兜底**按「短块」结构性判据网住白名单外的一切裸计数；**正文聚合（D 段）**再按「数字 ∈ 真值集 V 且紧邻单位词」网住**长正文段落**里的计数。**不允许存在"门禁看不见的计数"**（详见下「计数保护全覆盖」）。
3. **禁止**在页面用自然语言声明口径（例如宣称某类卡与 `total` 的包含关系）；口径只写在本规约 + `validate_kb.py` / `sync_counts.py`。
4. **改题后三件套 + 审计**：`sync_counts check` → `validate_kb.py` → `audit_count_drift.py`（新增 / 重编号卡后**必跑**第三者）。
5. overview 类型三级、方法论统计表、Mermaid 旁注：见下补充条。

补充：

- **overview `ov-type`**：每难度子组须拆篇章/核心原理/场景题；`ov-type-count` = 块内题数（`validate_kb` 3b2），键在 `struct`。
- **方法论统计表**：`compare-table`「卡数」列 → `struct.meth.table_*`；表尾合计 → L0（methodology）。
- **Mermaid**：节点纯文本；旁注挂锚点。
- **口径**：`total` = 篇章+核心原理+场景；`methodology` / `engineering` / `pitfalls` 为专篇键；不设全站合计。

##### 计数保护全覆盖（2026-09-21 长官指令：所有计数必须设门禁保护）

**原则**：页面上的每一个展示计数都必须受门禁保护——**要么带 `data-kb-pos`，要么在 SSOT 显式豁免**。
**不允许存在「门禁看不见的计数」**，**包括埋在长正文段落里的聚合计数**（2026-09-21 长官追加指令）。
反例一：mind 页 `map-col` 的 14 个组数长期是纯文本，原有门禁的容器白名单与「数字+单位词」
两个维度都不匹配 `（16）` 这类括号式写法，直到人工探针才暴露。反例二：mind 势页正文
「M16 单列"势定律"（11 张）」「M17（附，4 张）」与方法论页「本库不是 15 篇平行说明书」——
**长段落**写法绕过了短块兜底，且其中两个数字（11 / 14 以外的）此前**连 SSOT 键都没有**。
该批数字此后已全部升格为 L0 并注册独立 position（新增键 `chapters_pages`）。

**六重门禁（互补，缺一即假绿）**

| 脚本 | 职责 | 单独使用时的盲区 |
|---|---|---|
| `validate_kb.py` 0c 步 `run_l1_container_scan`（=`audit_l1_counts.py`） | **覆盖**：A 聚合容器 / B 全域 inline / **C 通用兜底（短块）** / **D 正文聚合（真值锚定）**，「疑似计数」未受保护即 FAIL | 只知「有没有漏标」，不知「标的值对不对」 |
| `sync_counts.py check` | **一致**：SSOT 键 ↔ DOM 取值逐位一致 | 键与 DOM 同为旧值时全绿 |
| `audit_count_drift.py` | **结构**：全站卡片普查（含重复定义）/ position 已登记 / 全局唯一 / `data-kb-count` 键有效 | 不管「键值是几才对」 |
| `audit_truth_source.py`（= `validate_kb` 0c2 步） | **真值**：按 SSOT `guard.sources` 逐键**独立求值**，与 SSOT 值、DOM 显示值三方比对；真源完备性 + 不变式 | 只覆盖已声明真源的键（未声明者由「未声明真源」检查抓） |
| `audit_prose_exempt.py` | **台账**：D 段全部候选及**豁免归属**逐条可见（**豁免本身不得成为盲区**） | 只读审计，不阻塞；不判对错 |
| `scan_undeclared_counts.py`（= `validate_kb` 0c3 步） | **正向完备**：全站正文每个计数锚点（`data-kb-count` + `data-kb-pos`）必须已在 SSOT `positions` 登记；漏登记即 FAIL | 只知「正文冒出来的数有没有登记」，不核「登记的值对不对」（后者由 0c2 真源管） |

链路：覆盖（有没有漏标）→ 一致（标的值对不对）→ 结构（位有没有登记、有没有重）→
**真值（反向：声明了 ⇒ 必须对）** → **正向（正文有 ⇒ 必须登记）** → 台账（豁免有没有过宽）。

> **反向 vs 正向（2026-09-21 长官指令「把未登记声明的键找出来」）**：
> `audit_truth_source`（0c2）只覆盖**已声明**的键——这是**反向**完备性（每个已登记 position 必须有真源、值必须正确）。
> 但「反向」天生看不见**从未登记**的计数：页面上偷偷加一个 `data-kb-count="X"`，只要 SSOT 里没有 `X`，
> 所有旧门禁都**零覆盖、零校验**（裸奔）。`scan_undeclared_counts`（0c3）补上**正向**完备性：
> 扫描全站正文，**凡是带 `data-kb-count` 锚点的键，都必须能在 SSOT `positions` 查到**；查不到即 FAIL「未登记计数」，
> 逼着任何新计数先 `sync_counts bump --add` 登记、再在 `guard.sources` 声明真源。
> 两道合起来才是**闭合**：声明了 ⇒ 必须对（0c2）；正文有 ⇒ 必须登记（0c3）。只做反向，
> 漏登记的计数永远进不了 SSOT，门禁对它形同虚设。

> **职责收敛（2026-09-21）**：`audit_count_drift.py` 原先自带一套真值推导
> （`guard.layers` / `guard.derived` / `guard.single_source`），与新的真源引擎**逻辑重复**——
> 同一语义两处解读，改一处必分叉。现真值**统一由 `audit_truth_source.py` 承担**，
> `audit_count_drift.py` 只保留结构性校验，并**以子进程方式调用真源引擎**把其 FAIL 并入自身结论。

**通用兜底（C 段，2026-09-21）—— 防「白名单枚举」漏网**

覆盖门禁的 A 段依赖 `containers` **枚举**容器类名，一旦出现**全新样式的容器**就必然漏。故加 C 段：
按 `block_tags` 切块，块「可见文本」长度 ≤ `max_block_chars` 者视为**元数据/标签块**，
其内任何未受 `data-kb-pos` 保护的「数字+单位词」一律 FAIL；长块（正文叙述）天然豁免。
**判据是结构性的（块有多短），不是容器名**，故新增容器样式自动被覆盖。

- 阈值 `max_block_chars = 100`：实测 70 / 100 两档候选集**完全一致**，140 起开始出现正文误报（如「149 测中 90 项更快」「建 200 题评测集」）。**宁可留余量，勿缩小覆盖率**。
- 误报**一律进 `fallback.exempt`**（数据），不改脚本。现有 3 类：`第 N 章`（章节序号引用）、`N 测中`（官方基准测项叙述）、`P0/P1`（优先级文案）。
- 非可见区由 `fallback.mask` 屏蔽：注释 / `script` / `style` / `pre` / `code` / `svg` / `mermaid` 容器 / 标签本身。

**正文聚合计数（D 段，2026-09-21 长官指令「正文也要应管尽严」）—— 真值锚定，非句式枚举**

C 段只覆盖「短元数据块」（可见文本 ≤ `max_block_chars`）；**埋在长正文段落里的聚合计数**
（如「本库不是 15 篇平行说明书」「M16 单列"势定律"（11 张）」）此前完全失管。D 段补上这一段：

判据 = 数字 **∈ 语义真值集合 V** 且后接单位 ∈ `prose.units`，且**未被 `data-kb-pos` span 精确包裹**，
且未命中 `prose.exempt` → FAIL。

- **V = `counts` 全部正整数值 ∪ 所有已注册 position 的键的当前值**（`validate_kb.truth_value_set()`）。
  这是**语义真值锚定**：正文里的数字只有**恰好等于**某个计数键当前值时才可能是本站聚合计数；
  技术叙述中的其他数字（「325 张表」「2000 万行」「8 亿行」）**天然不命中，无需逐一枚举句式**。
  新增计数键后 V 自动扩展，**无需改脚本**。
- **与 C 段的分工**：C 管「短元数据块」，D 管「长正文段落」；判据与豁免各自独立。
- **爆炸半径**（2026-09-21 实测）：零豁免下 D 段候选 **124 处** —— 110 处是「第 N 篇」章节序号引用，
  其余 14 处为技术叙述（B+ 树层数、调用链深度、项测试、核心表、比较阈值等），全部由 `prose.exempt`
  **9 条**正则覆盖，**0 处未豁免**。
- **误报一律进 `prose.exempt`**（**每条须带 `name` 写明理由**），**禁调 `prose.units` / 禁关 `prose.enabled`**。
- **豁免可见性（红线）**：`python3 scripts/audit_prose_exempt.py` 打印**豁免台账**（每条豁免放过哪些位置、
  共几处），用于复核豁免是否过宽 —— **豁免本身是新的盲区来源**，必须可见、可审。
- **边界（须知晓，不是缺陷）**：
  ① 技术叙述数字若**恰好等于**某键值（如 149 ∈ V →「149 项测试」）会命中 → 走 `prose.exempt` 台账豁免；
  ② 正文若写了与**所有**键值都不等的错误数字（如误写「163 张卡」）**不命中** —— 属**内容正确性**范畴，
     由人审负责，非本门禁职责（门禁管「有没有受保护」，不管「写得对不对」）；
  ③ 无单位词的展示位（如 mind index 算式 `1+1+1+15+1` 中的 15）：D 段要求「数字紧邻单位词」，抓不到，
     仍**须注册 position**（例 P433）并由一致性 / 真值链路保障。

**真源完备性（2026-09-21 长官指令「门禁得管写得对不对」）—— 登记了位置点，位上的数就必须有正确性校验**

前三重门禁（覆盖 / 一致 / 结构）**全部是内部自洽**：position ↔ SSOT ↔ DOM 三方对齐，但
**没有一条链路去核对「那个值本身对不对」**。后果是**实测到的真实内容错误长期潜伏**：

| 缺陷 | 事实 | 为何所有旧门禁全绿 |
|---|---|---|
| 根 index 组 1「权威（与章节同构）」显示 16 | 实际列了 **17** 个节点（M01–M17） | DOM 与 SSOT 同为陈旧的 16，`check` 逐位一致；不同链路（`dir_count_1`）也一致 |
| mind 势页正文「（11 张）/（4 张）」 | 键 `meth.group_16/17` 早已存在，但**该文件没注册 position** | 一致检查按 position 的 `file` 过滤，未登记的位不看 |
| 6 篇章节 index 的「高级」计数 | 比正文 `difficulty-senior` 实际数**少 1–3** | 同上：DOM ↔ SSOT 一致，但都错 |
| 核心原理「高级」39 / 场景「架构」49 | 实际 40 / 50 | 同上 |
| SSOT 里 `mind-foot-c_11` 有**两份**（扁平点分键 = 30 ✓ / 嵌套键 = 28 ✗） | 同一逻辑键双写、值不同 | 解析只认扁平键，嵌套那份**谁也看不见** |

**真源规则（`guard.sources.rules`）**——每条 = 「一类键的真值怎么算」的**唯一**声明：

| `type` | 语义 | 关键字段 |
|---|---|---|
| `dom_scan` | 单文件内按块切分，**块内元素数 == 块内声明的计数值**（万能恒等式） | `file` / `block_re` / `end_re` / `count_re` / `key_re` |
| `cards_by_link` | 索引页的链接列表 → 逐个宿主页数元素 | `index_file` / `link_re` / `count_re` 或 `count{...}` / `key_re` |
| `block_count_same_file` | 同一文件内按「第 n 个块」定键（`%02d` 可格式化） | `file` / `block_re` / `next_re` / `count_re` |
| `host_page_cards` | 键 ↔ 宿主页元素数（键名与文件名**都要显式声明**，不靠猜） | `items[{key,file,count_re}]` |
| `dom_count` | 单值 = 某文件内某正则的命中数 | `items[{key,file,count_re}]` |
| `sum` | 分组键求和 == 合计键 | `items[{key,terms,desc}]` |
| `file_count` | 键 = 匹配 glob 的文件数 | `items[{key,glob}]` |
| `page_diff` | 页内难度分布（`prefix` + 宿主页） | `items[{prefix,file}]` |
| `layer_sum` | 层卡数 = Σ 该层 M 组卡数（层归属读 `guard.layers`） | `from:"layers"` |
| `derived` | 结构性派生（`region` 取块 → `count` 计数） | `from:"derived"` |

**不变式（`guard.sources.invariants`）**：分组分项之和 == 合计。分项取**展示值**、合计取**真值**——
若两边都用重算真值就退化成 `truth == truth` 的**恒真空检查**（2026-09-21 probe 用例 C 实测的假绿，
已修正）。同时这条不变式天然能抓「整项缺展示位」（SSOT 里没有该分项键 → 记「缺展示位」）。

**人工锚定（`guard.sources.manual`）**：真源不可自动推导的少数位（站名/slogan 类文案数字、
`shi_axis`、`methodology*`）显式登记 `key_re` + `desc`（**须写明为什么不能自动求值**）。
未登记 `manual` 又无规则覆盖的键 → FAIL「未声明真源」。

**真源引擎的五类 FAIL（全部点名，默认不截断）**

| 关键字 | 含义 |
|---|---|
| `[真源配置]` | 规则 `type` 未实现 / 块找不到 / `region` 命中 ≠ 1 次 |
| `[键路径冲突]` | 同一逻辑键在 SSOT 写了**两份表示**（扁平点分键 + 嵌套键），展平后互相覆盖 |
| `[真源冲突]` | 同一键被多条声明求出**不同值**（双写，须合并为单一声明） |
| `[不变式]` | 分项（展示值）之和 ≠ 合计（真值） |
| `[未声明真源]` / `[声明未生效]` | 键没有任何声明覆盖 / 被规则正则覆盖却求不出真值 |
| `[无展示位]` | 求出了真值却没有已注册 position（「声明了却没人看得见的计数」） |
| `[真值不符]` | SSOT 值 ≠ 真值实测值（**这一条就是「写得对不对」**） |

**新增计数位的真源义务（与「先加 `data-kb-pos`」同级的硬要求）**：
新计数注册 position 后，**必须**能在 `guard.sources` 里被某条规则或 `manual` 覆盖，
否则 0c2 步直接 FAIL「未声明真源」。真源不是卡片数的（层下挂元素数等）走 `derived`。

**禁止的绕开姿势**：① 为让门禁过而改 `guard.sources.rules` 的口径（把真值算成当前值）；
② 把 `[真值不符]` 的内容问题「先改 SSOT 再改 DOM」对齐了事——必须**先查内容真相**（读原文 / 数元素），
再同时改 DOM 与 SSOT（`sync_counts.py bump`）；③ 用嵌套键绕过扁平键（`[键路径冲突]` 会抓）。

**边界（须知晓）**：真源引擎只能核对**已被声明真源**的键；正文里与所有键值都不等的手写数字
（如误写「163 张卡」）仍是**内容正确性**范畴，由人审负责（同 D 段边界②）。

**正向完备性（未登记计数扫描，2026-09-21 长官指令「过滤全站正文，把未登记声明的键找出来」）—— 正文有 ⇒ 必须登记**

反向（0c2 真源）管「已声明的键值对不对」；这道正向（0c3）管「正文冒出来的计数有没有登记」。
`scan_undeclared_counts.py` 扫描全站 HTML + Markdown（排除目录取自 SSOT `guard.exclude`，默认 `tmp/` `node_modules/` `rk/`），抽取形如
`<... data-kb-count="KEY" data-kb-pos="Pnn" ...>VALUE</span>` 的锚点（两种属性先后顺序都支持），
与 SSOT `positions` 的**键集合** + **position 编号集合**比对：

- **未登记键**（`data-kb-count` 的 KEY 不在 `positions` 键集合）→ FAIL「未登记计数」。
  这是门禁的**真正盲区**：该计数无任何覆盖/一致/真值/豁免链路管得到，等于裸奔。
- **未登记编号**（`data-kb-pos` 的 P 编号不在 `positions` 编号集合）→ FAIL「未登记计数」（孤儿锚点）。
- **已登记但正文缺位**（SSOT 有键、全站正文无锚点）→ WARN（不阻塞）：可能是派生/汇总键无需锚点，
  或登记了却没落地，请人工确认（当前仅 `methodology_with_priority` 一条，值为 0，疑似未落地的占位键）。

**产物闭环**：发现未登记键 ⇒ 必须 `sync_counts.py bump --add <key>=<值>` 登记进 `positions`
（新建键加 `--add`），并在 `guard.sources` 声明真源（否则 0c2 步 `[未声明真源]` 会接力 FAIL）。
两步缺一不可，否则门禁对它就零覆盖。

**结构性派生计数（`guard.derived`）—— 真源不是卡片数的那一类**

某些展示计数的真源**不是卡片数**，无法由 `qa-card` 推出。例：`chapter-core-methodology.html`
的 5 个 `layer-count`（道 12 / 法 11 / 术 16 / 器 16 / 势 15 项）实际是各层 `layer-hang` 下挂
`layer-chip` 的**元素个数**（2026-09-21 实测：展示值与 DOM 元素数完全吻合，但此前无任何门禁保护）。
这类计数在 `guard.derived.items` 声明：`region` 取块 → `count` 计数 = 真值，与 SSOT 键值、
已注册 position **三方互证**；且每个派生键**必须**有已注册 position（由真源引擎 `[无展示位]` 把关）。

**配置数据化（红线，2026-09-21）**：门禁脚本内**禁止写死组号区间 / 文件名 / 容器名 / 单位词 / 白名单 / 项目根层级 / 忽略目录**——
写死一个子集就必然遗漏集合外的一切（历史事故：`audit_count_drift.py` 初版写死层边界、只审计 3 个文件、
白名单硬编码单一位号；另有 **9 个脚本硬编码「某用户家目录 + 项目名」的绝对路径**，
换机器 / 换目录即全崩——现统一走 `scripts/_kbroot.py::find_root`，**全脚本唯一实现**）。
忽略目录（`tmp/ node_modules/ rk/`）**统一取自 SSOT `guard.exclude`**，由各扫描脚本运行时 `G.get("exclude") or DEF_EXCLUDE` 读取
（`audit_truth_source` / `audit_count_drift` / `scan_undeclared_counts` 同此一处来源，**杜绝脚本内写死**，
否则 tmp 清理或忽略集调整时脚本与配置脱节、逐渐过时）。
全部配置集中到 SSOT `guard` 块：

| 键 | 用途 | 消费方 |
|---|---|---|
| `guard.coverage.scan` | 扫描范围 glob | `run_l1_container_scan` |
| `guard.coverage.containers` | 聚合 UI 容器（容器内「数字+单位词」必须受保护） | 同上 |
| `guard.coverage.units` | 受管单位词（题 / 卡 / 组 / 道 / 页 / 章 / 张 / **项**） | 同上 |
| `guard.coverage.inline` | 全域通用模式（如「M## 名（N）」括号式组数） | 同上 |
| `guard.coverage.fallback` | **通用兜底**：`max_block_chars` / `block_tags` / `mask` / `exempt` / `exempt_window` —— 短块内裸计数即 FAIL，**不依赖容器枚举** | 同上 |
| `guard.coverage.prose` | **正文聚合计数**：`enabled` / `units` / `mask` / `exempt`（含 `name` 理由）/ `exempt_window` —— 数字 ∈ V 且紧邻单位词、未受 span 包裹即 FAIL，**真值锚定** | 同上 + `audit_prose_exempt` |
| `guard.coverage.exempt` | 豁免正则（按整行匹配则跳过，服务 A/B 段） | 同上 |
| **`guard.sources`** | **真源声明**：`types`（类型说明）/ `rules`（怎么求真值）/ `manual`（人工锚定）/ `invariants`（不变式） | **`audit_truth_source`** |
| `guard.layers` | 层归属 `range` + 合计 `sum_keys`（真值随 `range` 变化 → probe D 用例）；**层展示位须复用 `sum_keys` 内已有键**（道/法/术各 4 键 `meta_1..4`/`theme_1..4`/`appendix_1..4`，势/附**仅** `shi_3`/`fu_3`）——新建未登记的同族键（如 `shi_1`/`fu_1`）会被判「声明未生效」 | `audit_truth_source`（`layer_sum` 规则） |
| `guard.single_source` | 单值键（组数 / 总卡数）来源声明 | 同上（`dom_count` 规则 + `manual`） |
| `guard.derived` | **结构性派生计数**：`key` / `file` / `region` / `count`（真源 = DOM 元素数） | 同上（`derived` 规则） |
| `guard.pos_allow_multi` | 允许多点位白名单 | `audit_count_drift` |
| `guard.exclude` | **全局忽略目录**：`tmp/`、`node_modules/`、**`rk/`** | 全部脚本 |

**`rk/` 全局忽略（2026-09-21 长官指令）**：`rk/` 是软考资料站，**不属于 KB 站群**；
所有扫描 / 门禁 / 审计一律跳过，AI 亦不主动改动其中内容。

**新增或发现受保护场景**：只改 SSOT `guard`（**配置**），**不改脚本**。若某新容器 / 新写法漏保护，
登记进 `guard.coverage`（容器 / inline 模式 / **兜底豁免**）即全域生效；若某新计数的真源不是卡片数，
登记进 `guard.derived` + 注册 position。

**禁止的"绕开姿势"**：① 为让门禁过而把阈值调大 / 把兜底关掉（`fallback.enabled=false`）/
把正文段关掉（`prose.enabled=false`）/ **把真值改写成当前值（`guard.sources` 口径作弊）**；
② 把误报内容直接塞进 `exempt` 而不确认它确实**不是**计数（每条豁免须写 `name` 理由，
并用 `audit_prose_exempt.py` 复核台账）；
③ 新增展示计数却不注册 position（`audit_count_drift` 的「未登记 position」检查会抓，
但**只在它带 `data-kb-pos` 时**才看得见 —— 所以「先加 `data-kb-pos`」是本规约的第一步，不是最后一步）；
④ 注册了 position 却不声明真源（0c2 步 `[未声明真源]` 会抓）；
⑤ 发现 `[真值不符]` 后**只把 SSOT 与 DOM 互相对齐**（两边一起错也还是错）——
必须先读原文 / 数元素查清**内容真相**，再走 `sync_counts.py bump` 修正。

**反向验证（改门禁必跑）**

- `python3 scripts/probe_count_coverage_gate.py` — 覆盖门禁 **6 用例**：A inline 去保护 / B 容器裸计数 /
  **C 白名单外的全新容器样式内裸计数** / **D 短块兜底（layer-count 去保护）** /
  **E 正文长段落「15 篇」去保护** / **F 长正文注入全新裸计数（400 道 / 149 张）**
- `python3 scripts/probe_count_drift_gate.py` — 漂移审计 8 用例：键值漂移 / position 未登记 / position 重复 /
  数据驱动（改 `guard.layers` range）/ **derived 真源漂移** / **derived 独占检出（多插 chip）** /
  **derived region 失效** / **derived 无展示位**
- `python3 scripts/probe_truth_gate.py` — 真源门禁 **6 用例**：A **值错但四处自洽**
  （同时改 DOM + SSOT，`sync_counts check` 依然 425/425 全绿 → **只有真源审计能发现**，本门禁存在的唯一理由）/
  B 未声明真源 / C 不变式破损 / D 键路径冲突（扁平 + 嵌套双写） / E 真源配置写错 / F 声明未生效
- `python3 scripts/probe_undeclared_gate.py` — 未登记计数门禁 **2 轮**：轮 1 在根 index.html 正文
  **就地注入一个未登记键**（用已登记的 P01 编号、隔离「键未登记」路径）→ 断言 scan 脚本 FAIL 且命中该键；
  轮 2 还原后再跑 → 断言 PASS（无误杀）。**自包含**（从当前文件派生注入态，不依赖 tmp 历史快照）；
  `try/finally` 保证根 index.html **字节级还原**；夹具/环境缺失退 3。
- `python3 scripts/audit_prose_exempt.py` — **豁免台账**（只读，非 probe）：列出 D 段全部候选与豁免归属，
  「未被豁免」应为 0 处。改 `prose.exempt` 后必看。

**徽标结构 / 小屏留白 / 页内对齐门禁（check_index_badges.py，2026-09-16）—— 聚合 UI 的「视觉合规」层**

与「计数对不对」互补的另一类门禁：根 index + overview 的**徽标结构**（聚合 UI 分类计数徽标是否成组、
是否缺 `margin-left:auto`）、**小屏留白**（`.dir-group`/`.q-list`/`.q-item` 在 768/480 断点下的内缩是否单层化）、
**页内对齐**（桌面 `.dir-group` 横向间距是否统一）三项不得退化。对应 `validate_kb` 的「聚合 UI 禁裸数字」同族，
但校验的是**视觉结构**而非数字本身。

- 入口：`scripts/check_index_badges.py`（**独立运行** `python3 check_index_badges.py <项目根>`；
  `validate_kb.py` 未直接调用它，但其内联的 `[小屏]`/`[列表]` 检查与本门禁互补——二者口径须一致）。
- 正向验证：`scripts/probe_index_badge_gate.py` —— **自包含**（2026-09-21 改写，摆脱对 tmp/ 历史快照的依赖）：
  从当前项目的 `index.html` + `nav-overview-priority.html` 复制进**系统临时沙箱**，分别注入三类缺陷
  （删 `.dir-container` 规则→留白、删 `.dir-count` 规则→对齐、剥 `ov-badges` 包裹→徽标），
  断言门禁 FAIL 且命中该类签名串，最后跑干净树断言 PASS；沙箱用完即清，**不碰项目真实文件、不依赖 tmp/**。
  与 `probe_truth_gate` / `probe_undeclared_gate` 同构（从当前文件派生注入态）。
- **关联落位（长官指令「有价值的脚本得落 skills」）**：`check_index_badges.py` 与 `probe_index_badge_gate.py`
  均已在 `.workbuddy/skills/java-kb-expand/scripts/`；本段即其「关联文档」，补齐此前漏写的说明。

注入必须 FAIL、还原必须 PASS，否则门禁是「假绿」。
C/D/E/F 用例是「兜底与正文段不可被关掉」的证据；probe_truth_gate 的 A / probe_count_drift_gate 的 D、F
是「真值与数据驱动不可被绕过」的证据——谁改回枚举或写死口径，probe 立即变红。

**验证脚本自身的纪律（2026-09-21 事故后固化）**

- **还原一律走 `try/finally`**：`probe_diff_label_gate.py` 曾因「锚点不存在」直接 `return 1`，
  绕过轮 5 的还原，把 `chapter-01` 一枚徽标留成「高级开发」，随后 `validate_kb` FAIL ——
  **会污染被测对象的验证脚本，其结论不可信**。
- **注入锚点动态取，不写死文本**（用当前文件里真实存在的结构定位）。
- **不依赖 `tmp/` 历史夹具**：夹具随沙箱清理即消失，脚本会抛 `FileNotFoundError`，
  被误读成「门禁失效」。注入态一律**从当前文件派生**；确需夹具而缺失时，
  以**退出码 3** 明确报「夹具缺失待重建」，**不得**抛异常、**不得**静默退出 0。
- 退出码约定：`0` 通过 / `1` 门禁失效 / `2` 定位失败 / `3` 环境缺失（当前 `probe_index_badge_gate.py`
  已自包含，正常跑为 `0`；仅当 `index.html` 或 `nav-overview-priority.html` 缺失才退 `3`）。
### 5.2 项目根 `Java Spring AI/index.html`（全量快照）
- **Hero 统计块**（`.dir-hero` 内两行，共 10 项；改数走 `sync_counts.py`，勿手改）：
  - 首行 `.dir-stats`（4 项，无 `stat-tag`）：编号体系 `6`（`struct.misc.index.site-meta_1`，P108）/ 页面篇章 `20`（`site-meta_2`，P109）/ **思维导图 `19`（`mind_pages`，P37）** / 题目总数 `total`（P36）。
  - 次行 `.dir-stats.dir-stats-sub`（6 项，各带 `stat-tag`）：M 核心方法论 / G 工程化要点 / K 生产踩坑 / C 深度 Q&A / E 核心原理速查 / S 真实场景题。
  - 口径：M/G/K 为专篇键，**各自单独计数，禁止「题数+M+G+K」式合计**；「全站 N 题」仅指 `total`（C+E+S）。禁止 `kb-count-local`。
  - **`mind_pages` 是全站唯一的导图页数键**（19 = 15 篇章导图 + 方法论 + 工程化 + 踩坑 + 安全），三处展示：根 index P37 / 章节导航 index P222 / 导图站 P351；文案一律「思维导图」/「思维导图页」。（章节导航 hero 原有第 7 格 P221，2026-09-16 长官移除其「思维导图」统计卡后该位作废并已从 `positions` 删除。**删展示位必须同步删 position**：残留 position 会让 `sync_counts.py check` 与 `validate_kb.py` 的「kb-count 标记」项双双 FAIL。）
  - **`chapters_pages` = 篇章页数**（**15** = `第 01 篇`~`第 15 篇`，2026-09-21 新建键）：与 `counts.chapters`（**252** = 篇章**题数**）**语义不同，切勿混用**。此前「15 篇 / 15 篇章 / 15 章」在全站 **5 处**副标题与正文中是**裸数字、且 SSOT 里连键都没有**（2026-09-21 由正文聚合门禁 D 段探针暴露）。展示位 **P429–P433**：章节 index 方法论卡 footer / overview 页头副标题 / overview 页脚 / mind index 副标题 / 方法论页正文；另有 mind index 的**算式位** `1+1+1+15+1`（P433，无单位词，由 `sync_counts check` 与 `audit_count_drift` 保障）。
  - **`site-meta_2` = 页面篇章 20**（页面口径，含非篇章页），与 `chapters_pages`（15 篇）/ `chapters`（252 题）三者**互不相同**，勿互相换算。
  - 小屏列数（**按块定列，使列数与项数整除**）：≤768px 首行 `.dir-stats` **4 列**（4 项＝1 行）、次行 `.dir-stats-sub` **3 列**（6 项＝2 行）；≤480px 两行统一 **2 列**（4 项＝2 行、6 项＝3 行）。**加计数项须让两行项数各自能被当前列数整除**，否则末行出现半空格子（历史：首行 3 项时 375px 下「题目总数」独占一行、右侧整格留白；首行 4 项而用 3 列时 481~768px 也会「3+1」留白）。
- 每题一个 `<li class="q-item">…，<span class="q-id">ID</span>…，<span class="q-tags"><span class="difficulty">…</span><span class="priority priority-pX">PX</span></span></li>`；新增题须在对应 ID 的 li 后插入。
  - **结构完整性**：`q-tags` 必须闭合、`<a>` 不得顶格（须与同级 li 内缩进一致）。历史新增题曾出现「顶格 `<a>` + `q-tags` 未闭合」（2026-09-16 实测 7 条：C11.28/29/30、S12.08/09 顶格+未闭合，G07.08/09 仅未闭合），渲染上表现为徽标错位、层级断开。门禁 `scripts/check_index_badges.py`（顶格 `<a href=…>` 与未闭合 `q-tags` 均为 FAIL）。
  - **优先级补齐口径**：缺失徽标按**镜像源页**判定——源页有优先级则补（C11.28/29/30、S12.08/09 补 `P1`），源页无优先级则**不补，仅修结构**（G/K 块源页本无优先级，`validate_kb` 亦不强制）。**M/G/K 三类卡一律不呈现等级与优先级徽标**（2026-09-16 长官决策，两次下达：先三专篇页、再三处导航位）——根 index M/G/K 区块 220 条 `.q-tags` 已整块移除，全文口径见 §2 例外条。**长尾提醒**：删徽标会连带**孤立计数位**（本轮 6 个：P74/P75/P76/P103/P104/P105 随章节导航 `card-tags` 一并作废），必须同步从 `kb-counts.json` 的 `positions` 删除并跑 `sync_counts.py render`。
- per-chapter / per-group `dir-count` / `dir-group-count`：**必须等于**紧随其后的 `ul.q-list` 内卡片数；各篇章 `dir-count` 求和 = 篇章总数（见 COUNTS）。
  - **新增卡片八步（漏任一步都会「假绿」，2026-09-20 / 2026-09-21 血泪）**：① 章节页正文卡 + TOC + Mermaid 组图节点；② 对应 mind 导图页（卡 + mindmap 节点 + 列表节点）；③ **根 index 对应 `dir-group` 的 `ul.q-list` 内按序插入 `<li class="q-item">`**——只改 `dir-count` 计数而不补 li，会直接触发 `validate_kb` 的 `[根index dir-count] 计数≠列表` FAIL；同时组的 `dir-group-count` 须 `sync_counts.py bump struct.root.dir_group_N=+1`（否则补 li 后又触发 `[根index dir-group]` FAIL）；④ **把新 ID 登记进 `validate_kb.py` 顶部 `NEW_IDS`（第 85 行「待填：本轮新增/改动题号」，手工维护）——未登记则该卡的「落位 + 双编码」检查被静默跳过、不报错，门禁显示 ALL PASS 实为假绿**。计数一律走 `sync_counts.py bump` 唯一入口，勿手改数字。 ⑤ **跑一次独立反向审计 `scripts/audit_count_drift.py`**——`sync_counts.py check` 只比对「键 ↔ DOM」的**逐位一致性**，查不出两类缺陷：**(a) 键值本身漂移**（键与 DOM 同为旧值，check 全绿却 ≠ 真实卡数；2026-09-21 实测 10 处：`meta_1/2/4` 22→29、`theme_1/2/4` 45→50、`table_1/2/3` 15/7/3→16/13/7、`meth-groups_1` 与 `mind-foot-meta_1` 16→17）；**(b) `data-kb-pos` 跨文件重复**（check 按 position 的 `file` 字段过滤，重复位在**非登记文件**里完全不校验；2026-09-21 实测 mind 页误复用章节页 `P405`/`P404`）。脚本**完全数据驱动**（层归属 / 单值键 / 白名单 / 排除目录全读 SSOT `guard`，宿主页自动识别，**不写死任何组号与文件名**），以「宿主页实际 `qa-card` 数 → SSOT 键 → DOM 取值 → position 全局唯一且全部已登记」四条独立链路互证；另含「未登记 position」「无效 `data-kb-count` 键」「卡片重复定义」三项全局反向检查。有漂移即 exit 1 并给出 `bump` 命令。 ⑥ **改完门禁必跑两个 probe**：`scripts/probe_count_coverage_gate.py`（覆盖门禁 **6 用例**，含「白名单外全新容器样式」「短块兜底」「正文长段落去保护」「长正文注入新裸计数」）与 `scripts/probe_count_drift_gate.py`（漂移审计 **8 用例**，含 4 类 `guard.derived` 注入）——注入缺陷必须 FAIL、还原必须 PASS，否则为「假绿」；改 `prose.exempt` 后另跑 `scripts/audit_prose_exempt.py` 复核**豁免台账**。
 ⑦ **若新计数的真源不是卡片数**（如某层下挂元素个数）：须在 SSOT `guard.derived.items` 声明 `region` + `count`，并注册 position；否则 `audit_count_drift` 报「没有对应的已注册 position」。
 ⑧ **正文里的聚合计数同样受管**（2026-09-21 长官指令）：页头 / 正文段落 / 旁注等**任何位置**，数字 ∈ V 且紧邻单位词即须带 `data-kb-pos`，否则 D 段 FAIL（实测历史漏网：mind 势页「（11 张）」「（4 张）」、方法论页「本库不是 15 篇平行说明书」）。新增「此前**无键**」的展示计数（如篇章页数）用 `sync_counts.py bump --add <key>=<N>` 建键（`--add` 是新建键的唯一入口；不带 `--add` 时键名拼错仍会报错），再注册 position。
- 方法论目录结构（平级 `dir-group`，禁止嵌套）：序章①~⑤ → **⑥ 生产与领域思维速查（M12，16 卡）** → 一~五主题（M06~M10）→ 附录（M11）。**禁止**把 M12 嵌进「一、高并发」。
- **小屏（≤768px）横向 gutter 归一口径（2026-09-16 固化）**：全页横向留白**唯一来源 = `.dir-container` 的 `12px`**，与 `.dir-hero` / `.dir-legend` / `.dir-toolbar` 一致。`.dir-section` **不得**再叠加留边——既要清掉页面内联的 `margin-left/right: 12px`，也要显式覆盖**共享 `design-system.css` 的 `.dir-toolbar,.dir-legend,.dir-section,.dir-stats { padding-left/right: max(12px, env(safe-area-inset-*)) }`**（该规则位于共享表的 ≤768 段，页面 `<style>` 后加载，同特异度下页面胜出，故须写 `padding-left: 0` 显式归零）。列表横向内缩由 **`.dir-body` 单层**承担 `4px`（桌面为 `--dir-pad-panel` = 1rem）——`.dir-group` / `.q-list` 横向必须为 `0`，`.q-item` **仅左侧**为 `0`（右侧内缩有意保留，hover 背景不贴死行尾）。**内缩层必须唯一**：曾把内缩放在 `.dir-group` 上，导致「有分组」与「无分组」（深度 Q&A 15 篇章）两类区块分叉 —— 题号左缘 1px vs 17px，视觉上像两个页面。
  - 修复前每侧累计 **68px**（容器 24 + section margin 12 + 共享 CSS padding 12 + 边框 1 + 8+8+8），375px 下列表可用宽仅 **229px（视口 61%）**，页高 62066px；修复后每侧 **25px**、可用宽 **325px（87%）**、页高 52570px（展开态 −15.3%）。复测/回归用 `scripts/probe_root_index_whitespace.js`。
  - 附带修掉两个被 `overflow: hidden` 掩盖的缺陷：`.dir-header` 的 `.dir-count` 计数胶囊在 303px 内容宽下溢出 section 被裁切（`check_mobile_overflow.js` 会因祖先 `overflow:hidden` 计入「横滑容器」而不报 —— **溢出只有宽度实测 + 截图肉眼可见**）；折叠态页高 3413 → 2692px（−21%）。
- **`q-tags` 缩进口径**：标签行左缘须对齐**题号列宽 + `.q-item a` 的 gap**（gap 现为 `--dir-gap-sm` = 0.5rem）。≤768px `padding-left: 5rem`（q-id 4.5rem + 0.5rem）；≤480px q-id 收窄为 3.8rem，故须同步改 `4.3rem`（曾写 `0`，与 ≤768 断点口径不一致 → 标签错位）。**改 `a` 的 gap 必须同步改这两处**。
- **页内风格 token 层（2026-09-16 归一化）**：页面 `<style>` 顶部声明 `:root { --dir-* }`，把发散的取值收口到有限档位（原字号 **12 档** / 圆角 7 档 / 横向 padding 7 档 / gap 4 档，其中 4 档字号挤在 10.88~12.8px、差 ≤0.48px 肉眼不可辨）。改页内样式**一律引用 token，不得再写裸值**；门禁会先把 `var(--dir-*)` 解析为实际值再比对，token 被删/改名即 FAIL（不静默放行）。
  - **字号 7 档**：`--dir-fs-2xs` 0.7rem（徽标 / 分组计数 / 小屏辅助）· `-xs` 0.8rem（说明 / 等宽编号 / 分隔标题 / 图例）· `-sm` 0.85rem（题目 / 按钮 / 分组标题 / 折叠箭头）· `-md` 0.95rem（面板标题 / 副标题）· `-lg` 1.15rem（次级统计数字）· `-xl` 1.8rem（主统计数字）· `-2xl` 2rem（页主标题）。**响应式字号不进阶梯**：小屏 h1 `clamp(1.25rem,5vw,1.65rem)`、≤480 的 1.2rem、小屏统计数字 1.25rem。
  - **布局 / 内距 / 圆角 / 色彩**：`--dir-maxw` 1100px · `--dir-gutter` 1.5rem（桌面）· `--dir-gutter-sm` 12px（小屏）；内距 3 档 `--dir-pad-chip` 6px（徽标 / 行内 code）· `-item` 8px（列表项 / 计数胶囊 / 分组）· `-panel` 1rem（面板头 / 分组头 / 按钮）；间距 `--dir-gap-xs` 4px · `-sm` 0.5rem · `--dir-stats-gap` 2rem · `-sub` 1.6rem；圆角沿用共享 `--radius-sm/md`，另加 `--dir-radius-pill` 20px；色彩 `--dir-ink-on-tag` / `--dir-tag-g`（G 卡专色，其余 5 个 tag 走共享 token）/ `--dir-hover`（三处 hover 底色的唯一来源）。
- **页内对齐口径（2026-09-16 固化，实测驱动）**：
  - **左侧内容线**：`.q-list` 与 `.q-item` 的**左侧**内缩必须为 `0`，使题号列与分组标题左缘共线（改前桌面 107 vs 91、小屏 25 vs 17，各差 16/8px）。**只约束左侧**——右侧必须保留内缩，否则 hover 背景贴死行尾。
  - **右侧计数线**：`.dir-group-title` 须 `display:flex` + `justify-content:space-between`，使 55 处分组计数与 21 处章节计数胶囊落在同一条右缘垂直线（桌面 1109 / 小屏 358）。改前分组计数以 `margin-left:0.5rem` 紧邻标题文本、章节行却靠 `tagline{flex:1}` 推到行尾 —— 同一语义两种位置策略。
  - **小屏面板头换行**：`.dir-header` 须 `flex-wrap:wrap`，配合 `.dir-title{flex:1 1 auto}`、`.dir-count{order:2}`、`.dir-header .tagline{order:3;flex:1 1 100%}` —— 首行＝箭头+标题+计数胶囊（右缘对齐），tagline 独占第二行。不换行时 tagline 仅剩 ~50px 可用宽，中文逐字换行成竖排（实测「先建世界观」被拆成 5 行）。
  - **列表内缩单层化**：横向内缩**只允许 `.dir-body` 一层**（桌面 `var(--dir-pad-panel)` / 小屏 4px），`.dir-group` 桌面与小屏横向必须为 `0`。页内 24 个 section 分两类：**有分组**（导图/序章/原理/场景，`q-list` 在 `.dir-group` 内）与**无分组**（深度 Q&A 15 篇章，`q-list` 直接挂 `.dir-body`）—— 内缩若挂在 `.dir-group` 上，无分组区块就失去该层，题号左缘退化为紧贴 section 边框（实测 **1px vs 17px**）。修复后两类一致：桌面 **17px** / 小屏 **5px**。
  - **计数胶囊位置**：`.dir-count` 必须 `margin-left:auto` —— 位置**不可**依赖 `.tagline{flex:1}` 撑开。15 个 C 篇章的 header 无 tagline，胶囊会紧贴标题右侧（实测桌面右缘 **294px** vs 行尾 1035px）；小屏因 `.dir-title{flex:1 1 auto}` 恰好推开，**掩盖了该缺陷**（成因即「小屏统一、大屏不统一」）。修复后 24 个 section 的计数右缘取值集合 = `{1035}`（桌面）/ `{346}`（小屏）。

### 5.3 `java-architect-interview/index.html`（章节导航）
- **三张专篇 `chapter-card` 不带 `.card-tags`**（M/G/K 无等级徽标，2026-09-16；`card-footer` 只留组数/卡数/ID 前缀的计数行）。其余章节卡（C01–15 / 核心原理 / 场景 / 优先级总览）保留 `card-tags`，顺序 **专家 → 架构 → 高级**，某档为 0 则省略；数字须与目标页 `data-difficulty` 实计一致。
- **Hero `.meta-stats` 固定 6 格**（顺序）：核心方法论（`methodology`，P03）/ 工程化要点（`engineering`，P24）/ 生产踩坑（`pitfalls`，P91）/ 深度 Q&A（`chapters`，P55）/ 核心原理速查（`basics`，P39）/ 真实场景题（`scenarios`，P56），各自计数；「全站 N 道」= `total`（仅 C+E+S）。
  - **增删格子必须同步 `design-system.css` 的列数**（`.index-hero .meta-stats` 只在 §5.3 这一页出现）：桌面 `repeat(6)`（6 项＝1 行）、≤1024 / ≤768 / ≤480 均 `repeat(3)`（6 项＝3+3 两整行）。**任何断点的列数都须整除项数**，否则末行留半空格子（与 §5.2 根 index 同口径）。
  - **2026-09-16 长官移除原第 1 格「思维导图」（`mind_pages`，P221）**：DOM 删 4 行 + 桌面列数 7→6，P221 已从 `kb-counts.json` 的 `positions` 删除（口径见 §5.2 `mind_pages` 条）。
- 每篇章 `<div class="chapter-card">…<div class="card-footer"><span>N 题</span>…</div></div>`，`N` = 该章 `C##.##` 卡片数（与根 index `dir-count` 一致）。
- **不枚举单题 ID**（无 `Cxx.xx`/`Sxx.xx` li）——校验时落位=False 属预期。

### 5.4 `java-architect-interview-mind/index.html`（导图导航）
- 顶部 `idx-meta` 固定 **5** 格（`.idx-meta` 五列；窄屏两列）：
  1. `1+1+1+15+1` — 方法论 + 工程化 + 踩坑 + 篇章 + 服务端安全手册
  2. `21` — 思维导图页（主链 19 + R2/R3 视角；`mind_pages`）
  3. 方法论卡片数（`methodology`，P08）
  4. 工程化要点卡片数（`engineering`，P26）
  5. 生产踩坑卡片数（`pitfalls`，P93）
  6. `N+N+N` — Q&A · 原理 · 场景（取值见 COUNTS / P57–P59）
- 每张卡片底部 `card-foot` 计数口径（改题后必须同步）：
  - **篇章卡 mind-01~15**：`章节 N` = 对应 `chapter-NN` 的 C 卡数；`原理 N` / `场景 N` = 该 mind 页 `<summary>` 中实际列出的 E / S 卡数（无则省略该 chip）。
  - **方法论卡**：`149 卡 · 17 组`（M01~M17）。
  - **工程化卡**：`65 卡 · 8 组`（G01~G08）。
  - **安全手册卡**：`手册 7 章` + 该 mind 页并入的原理/场景数。
- `idx-meta` 题量表达式形如 `篇章+原理+场景`（取值见 COUNTS，勿写死旧数）。

### 5.5 场景 / 核心原理页分组计数
- 场景页正文 `span.group-count`、根 index 场景区 `dir-group-count`，均须等于该组 `S##.##` 实际题数（当前：5/6/5/6/5/6/7/8/5/5/6/8）。
- 核心原理页各组实际题数（当前：4/4/8/8/4/6/10/4/6/6/5/8）；根 index 对应 `dir-group-count` 同步。
- **散文计数位**：页头/来源段「本页 N 道 / 高频核心原理 N 题 / overview 全站 N 道…」等必须登记为 `kb-counts.json` positions（**位号以 SSOT 为唯一权威，勿写死范围**），改数走 `sync_counts.py bump`；`validate_kb.py` 第 0 步强制 `sync_counts check`，第 0c 步扫描 L1 聚合 UI。
## 6. 权威计数示例（2026-09-03 OPT-A 后固化）

<!-- COUNTS:BEGIN 由 scripts/sync_counts.py render 生成，勿手改 -->
- 题目总量 **400** = 篇章 252 + 核心原理 74 + 场景 74
- 优先级 **P0=94 / P1=248 / P2=58**（求和 = 400）
- 难度 **专家 46 / 架构师 192 / 高级开发 162**（求和 = 400；仅覆盖 C/E/S，M/G/K 不分级）
- 方法论 **149 卡**（M01~M17：道 M01–M02 / 法 M03–M07 / 术 M08–M15 / 势 M16 / 附 M17，专篇键 methodology；**不分难度等级**）
- 工程化 **65 卡**（G01~G08，专篇键 engineering；**不分难度等级**）
- 生产踩坑 **65 卡**（K01~K08，专篇键 pitfalls；**不分难度等级**）
- 口径（程序约束）：题目总量 total=篇章+核心原理+场景；M/G/K 为专篇键，不进 total；结构计数见 struct；**禁止 kb-count-local；禁止页面用自然语言声明口径**
- 方法论细分：带优先级 0/149（2026-09-16 起 M/G/K 不设难度计数）

计数位（改数须全部同步，由 sync_counts.py check 自动核查）：

| 编号 | 载体 | 说明 |
|---|---|---|
| P01 | `index.html` | 根 index 方法论统计卡 |
| P02 | `index.html` | 根 index 方法论分组题数 |
| P03 | `java-architect-interview/index.html` | 章节 index 方法论统计卡 |
| P04 | `java-architect-interview/index.html` | 章节 index card-footer 方法论数 |
| P05 | `java-architect-interview/index.html` | 章节 index card-footer 篇章题数 |
| P06 | `java-architect-interview/chapter-core-methodology.html` | 方法论页页头副标题卡数 |
| P07 | `java-architect-interview/nav-overview-priority.html` | overview ov-stat-num 10 项（顺序见 ov_stat_order；不含方法论） |
| P08 | `java-architect-interview-mind/index.html` | mind index idx-meta 方法论卡片 |
| P09 | `java-architect-interview-mind/mind-core-methodology.html` | mind-core-methodology 尾注 |
| P10 | `docs/README.md` | docs/README.md 文件表方法论数 |
| P11 | `docs/README.md` | docs/README.md 难度口径段 |
| P12 | `docs/README.md` | docs/README.md 方法论带优先级数（分子） |
| P13 | `docs/README.md` | docs/README.md 方法论带优先级数（分母） |
| P14 | `docs/format-shared.md` | docs/format-shared.md 分子 |
| P15 | `docs/format-shared.md` | docs/format-shared.md 分母 |
| P16 | `docs/format-special.md` | docs/format-special.md 定位段 |
| P17 | `docs/format-special.md` | docs/format-special.md 专篇合计段 |
| P18 | `docs/format-special.md` | docs/format-special.md ov-stats 段 |
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
| P33 | `java-architect-interview/chapter-questions-eight-part.html` | 核心原理页 meta 题目数 |
| P34 | `java-architect-interview/index.html` | 章节 index 核心原理卡标题 |
| P35 | `index.html` | 根 index 核心原理 dir-count |
| P36 | `index.html` | 根 index 题目总数 |
| P37 | `index.html` | 根 index 思维导图页数统计卡 |
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
| P77 | `java-architect-interview-mind/mind-engineering-practices.html` | mind 工程化页副标题卡数 |
| P78 | `java-architect-interview-mind/mind-engineering-practices.html` | mind 工程化页尾注卡数 |
| P79 | `java-architect-interview-mind/mind-engineering-practices.html` | mind 工程化页尾注题目总量 |
| P80 | `java-architect-interview-mind/mind-engineering-practices.html` | mind 工程化页尾注方法论卡数 |
| P82 | `java-architect-interview/chapter-engineering-practices.html` | 工程化页 meta 题目总量（C+E+S）参照 |
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
| P98 | `java-architect-interview/chapter-production-pitfalls.html` | 踩坑页 meta 题目总量（C+E+S）参照 |
| P99 | `java-architect-interview-mind/mind-production-pitfalls.html` | mind 踩坑页副标题卡数 |
| P100 | `java-architect-interview-mind/mind-production-pitfalls.html` | mind 踩坑页尾注卡数 |
| P102 | `java-architect-interview/index.html` | 章节 index 踩坑卡 desc 卡数 |
| P106 | `java-architect-interview/index.html` | 章节 index 工程化卡 footer 组数 |
| P107 | `java-architect-interview/index.html` | 章节 index 踩坑卡 footer 组数 |
| P108 | `index.html` | 升格 local:site-meta → struct.misc.index.site-meta_1 |
| P109 | `index.html` | 升格 local:site-meta → struct.misc.index.site-meta_2 |
| P110 | `index.html` | 升格 local:dir-count → struct.root.dir_count_1 |
| P111 | `index.html` | 升格 local:dir-group → struct.root.dir_group_1 |
| P112 | `index.html` | 升格 local:dir-group → struct.root.dir_group_2 |
| P113 | `index.html` | 升格 local:dir-group → struct.root.dir_group_3 |
| P114 | `index.html` | 升格 local:dir-group → struct.root.dir_group_4 |
| P115 | `index.html` | 升格 local:dir-group → struct.root.dir_group_5 |
| P116 | `index.html` | 升格 local:dir-group → struct.root.dir_group_6 |
| P117 | `index.html` | 升格 local:dir-group → struct.root.dir_group_7 |
| P118 | `index.html` | 升格 local:dir-group → struct.root.dir_group_8 |
| P119 | `index.html` | 升格 local:dir-group → struct.root.dir_group_9 |
| P120 | `index.html` | 升格 local:dir-group → struct.root.dir_group_10 |
| P121 | `index.html` | 升格 local:dir-group → struct.root.dir_group_11 |
| P122 | `index.html` | 升格 local:dir-group → struct.root.dir_group_12 |
| P123 | `index.html` | 升格 local:dir-group → struct.root.dir_group_13 |
| P124 | `index.html` | 升格 local:dir-group → struct.root.dir_group_14 |
| P125 | `index.html` | 升格 local:dir-group → struct.root.dir_group_15 |
| P126 | `index.html` | 升格 local:dir-count → struct.root.dir_count_2 |
| P127 | `index.html` | 升格 local:dir-group → struct.root.dir_group_16 |
| P128 | `index.html` | 升格 local:dir-group → struct.root.dir_group_17 |
| P129 | `index.html` | 升格 local:dir-group → struct.root.dir_group_18 |
| P130 | `index.html` | 升格 local:dir-group → struct.root.dir_group_19 |
| P131 | `index.html` | 升格 local:dir-group → struct.root.dir_group_20 |
| P132 | `index.html` | 升格 local:dir-group → struct.root.dir_group_21 |
| P133 | `index.html` | 升格 local:dir-group → struct.root.dir_group_22 |
| P134 | `index.html` | 升格 local:dir-group → struct.root.dir_group_23 |
| P135 | `index.html` | 升格 local:dir-count → struct.root.dir_count_3 |
| P136 | `index.html` | 升格 local:dir-group → struct.root.dir_group_24 |
| P137 | `index.html` | 升格 local:dir-group → struct.root.dir_group_25 |
| P138 | `index.html` | 升格 local:dir-group → struct.root.dir_group_26 |
| P139 | `index.html` | 升格 local:dir-group → struct.root.dir_group_27 |
| P140 | `index.html` | 升格 local:dir-group → struct.root.dir_group_28 |
| P141 | `index.html` | 升格 local:dir-group → struct.root.dir_group_29 |
| P142 | `index.html` | 升格 local:dir-group → struct.root.dir_group_30 |
| P143 | `index.html` | 升格 local:dir-group → struct.root.dir_group_31 |
| P144 | `index.html` | 升格 local:dir-group → struct.root.dir_group_32 |
| P145 | `index.html` | 升格 local:dir-group → struct.root.dir_group_33 |
| P146 | `index.html` | 升格 local:dir-group → struct.root.dir_group_34 |
| P147 | `index.html` | 升格 local:dir-group → struct.root.dir_group_35 |
| P148 | `index.html` | 升格 local:dir-group → struct.root.dir_group_36 |
| P149 | `index.html` | 升格 local:dir-group → struct.root.dir_group_37 |
| P150 | `index.html` | 升格 local:dir-group → struct.root.dir_group_38 |
| P151 | `index.html` | 升格 local:dir-group → struct.root.dir_group_39 |
| P152 | `index.html` | 升格 local:dir-group → struct.root.dir_group_40 |
| P153 | `index.html` | 升格 local:dir-group → struct.root.dir_group_41 |
| P154 | `index.html` | 升格 local:dir-group → struct.root.dir_group_42 |
| P155 | `index.html` | 升格 local:dir-group → struct.root.dir_group_43 |
| P156 | `index.html` | 升格 local:dir-count → struct.root.dir_count_4 |
| P157 | `index.html` | 升格 local:dir-group → struct.root.dir_group_44 |
| P158 | `index.html` | 升格 local:dir-group → struct.root.dir_group_45 |
| P159 | `index.html` | 升格 local:dir-group → struct.root.dir_group_46 |
| P160 | `index.html` | 升格 local:dir-group → struct.root.dir_group_47 |
| P161 | `index.html` | 升格 local:dir-group → struct.root.dir_group_48 |
| P162 | `index.html` | 升格 local:dir-group → struct.root.dir_group_49 |
| P163 | `index.html` | 升格 local:dir-group → struct.root.dir_group_50 |
| P164 | `index.html` | 升格 local:dir-group → struct.root.dir_group_51 |
| P165 | `index.html` | 升格 local:dir-group → struct.root.dir_group_52 |
| P166 | `index.html` | 升格 local:dir-group → struct.root.dir_group_53 |
| P167 | `index.html` | 升格 local:dir-group → struct.root.dir_group_54 |
| P168 | `index.html` | 升格 local:dir-group → struct.root.dir_group_55 |
| P169 | `index.html` | 升格 local:dir-count → struct.root.dir_count_5 |
| P170 | `index.html` | 升格 local:dir-count → struct.root.dir_count_6 |
| P171 | `index.html` | 升格 local:dir-count → struct.root.dir_count_7 |
| P172 | `index.html` | 升格 local:dir-count → struct.root.dir_count_8 |
| P173 | `index.html` | 升格 local:dir-count → struct.root.dir_count_9 |
| P174 | `index.html` | 升格 local:dir-count → struct.root.dir_count_10 |
| P175 | `index.html` | 升格 local:dir-count → struct.root.dir_count_11 |
| P176 | `index.html` | 升格 local:dir-count → struct.root.dir_count_12 |
| P177 | `index.html` | 升格 local:dir-count → struct.root.dir_count_13 |
| P178 | `index.html` | 升格 local:dir-count → struct.root.dir_count_14 |
| P179 | `index.html` | 升格 local:dir-count → struct.root.dir_count_15 |
| P180 | `index.html` | 升格 local:dir-count → struct.root.dir_count_16 |
| P181 | `index.html` | 升格 local:dir-count → struct.root.dir_count_17 |
| P182 | `index.html` | 升格 local:dir-count → struct.root.dir_count_18 |
| P183 | `index.html` | 升格 local:dir-count → struct.root.dir_count_19 |
| P184 | `index.html` | 升格 local:site-meta → struct.misc.index.site-meta_3 |
| P185 | `index.html` | 升格 local:site-meta → struct.misc.index.site-meta_4 |
| P186 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-subgroup → struct.ov.subgroup_1 |
| P187 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_1 |
| P188 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_2 |
| P189 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_3 |
| P190 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-subgroup → struct.ov.subgroup_2 |
| P191 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_4 |
| P192 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_5 |
| P193 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_6 |
| P194 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-subgroup → struct.ov.subgroup_3 |
| P195 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_7 |
| P196 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_8 |
| P197 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_9 |
| P198 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-subgroup → struct.ov.subgroup_4 |
| P199 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_10 |
| P200 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_11 |
| P201 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_12 |
| P202 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-subgroup → struct.ov.subgroup_5 |
| P203 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_13 |
| P204 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_14 |
| P205 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_15 |
| P206 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-subgroup → struct.ov.subgroup_6 |
| P207 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_16 |
| P208 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_17 |
| P209 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_18 |
| P210 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-subgroup → struct.ov.subgroup_7 |
| P211 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_19 |
| P212 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_20 |
| P213 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-subgroup → struct.ov.subgroup_8 |
| P214 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_21 |
| P215 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_22 |
| P216 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_23 |
| P217 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-subgroup → struct.ov.subgroup_9 |
| P218 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_24 |
| P219 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_25 |
| P220 | `java-architect-interview/nav-overview-priority.html` | 升格 local:ov-type → struct.ov.type_26 |
| P222 | `java-architect-interview/index.html` | 升格 local:mind-pages → mind_pages |
| P223 | `java-architect-interview/index.html` | 升格 local:chap-footer-meta → struct.chap.idx.meta_1（2026-09-21 真值修正 16→17） |
| P224 | `java-architect-interview/index.html` | 章节索引页「核心原理」卡「专家」数 → chapter-questions-eight-part.html 内 difficulty-expert 数 |
| P225 | `java-architect-interview/index.html` | 章节索引页「核心原理」卡「架构」数 → 该页内 difficulty-architect 数 |
| P226 | `java-architect-interview/index.html` | 章节索引页「核心原理」卡「高级」数 → 该页内 difficulty-senior 数（2026-09-21 真值修正 39→40） |
| P227 | `java-architect-interview/index.html` | 章节索引页「场景」卡「专家」数 → chapter-questions-scenario.html 内 difficulty-expert 数 |
| P228 | `java-architect-interview/index.html` | 章节索引页「场景」卡「架构」数 → 该页内 difficulty-architect 数（2026-09-21 真值修正 49→50） |
| P229 | `java-architect-interview/index.html` | 章节索引页「场景」卡「高级」数 → 该页内 difficulty-senior 数 |
| P230 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c01.n |
| P231 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c01.expert |
| P232 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c01.architect |
| P233 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c01.senior |
| P234 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c02.n |
| P235 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c02.expert |
| P236 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c02.architect |
| P237 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c02.senior |
| P238 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c03.n |
| P239 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c03.expert |
| P240 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c03.architect |
| P241 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c03.senior |
| P242 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c04.n |
| P243 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c04.expert |
| P244 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c04.architect |
| P245 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c04.senior |
| P246 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c05.n |
| P247 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c05.expert |
| P248 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c05.architect |
| P249 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c05.senior |
| P250 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c06.n |
| P251 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c06.expert |
| P252 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c06.architect |
| P253 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c06.senior（2026-09-21 真值修正 8→9） |
| P254 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c07.n |
| P255 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c07.expert |
| P256 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c07.architect |
| P257 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c07.senior（2026-09-21 真值修正 10→11） |
| P258 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c08.n |
| P259 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c08.expert |
| P260 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c08.architect |
| P261 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c08.senior（2026-09-21 真值修正 7→8） |
| P262 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c09.n |
| P263 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c09.expert |
| P264 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c09.architect |
| P265 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c09.senior |
| P266 | `java-architect-interview/index.html` | 升格 local:chap-desc-local → struct.misc.chap_index.chap-desc-local_1 |
| P267 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c10.n |
| P268 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c10.expert |
| P269 | `java-architect-interview/index.html` | 章节索引页第 10 篇「架构」数 → chapter-10-microservice-cloud.html 内 difficulty-architect 数 |
| P270 | `java-architect-interview/index.html` | 章节索引页第 10 篇「高级」数 → 该篇内 difficulty-senior 数（2026-09-21 真值修正 7→9） |
| P271 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c11.n |
| P272 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c11.expert |
| P273 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c11.architect |
| P274 | `java-architect-interview/index.html` | 章节索引页第 11 篇「高级」数 → chapter-11-middleware-engineering.html 内 difficulty-senior 数（2026-09-21 真值修正 7→10） |
| P275 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c12.n |
| P276 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c12.expert |
| P277 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c12.architect |
| P278 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c12.senior（2026-09-21 真值修正 1→4） |
| P279 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c13.n |
| P280 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c13.expert |
| P281 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c13.architect |
| P282 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c13.senior（2026-09-21 真值修正 4→5） |
| P283 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c14.n |
| P284 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c14.expert |
| P285 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c14.architect |
| P286 | `java-architect-interview/index.html` | 章节索引页第 14 篇「高级」数 → chapter-14-databases.html 内 difficulty-senior 数（2026-09-21 真值修正 3→4） |
| P287 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c15.n |
| P288 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c15.expert |
| P289 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c15.architect |
| P290 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c15.senior（2026-09-21 真值修正 3→4） |
| P291 | `java-architect-interview/index.html` | 升格 local:chap-footer-meta → struct.chap.idx.meta_2 |
| P292 | `java-architect-interview/chapter-engineering-practices.html` | 升格 local:eng-groups → engineering_groups |
| P293 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-meta → struct.meth.meta_1 |
| P294 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme → struct.meth.theme_1 |
| P295 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-appendix → struct.meth.appendix_1 |
| P296 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-groups → struct.misc.chap_chapter_core_methodology.meth-groups_1 |
| P297 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-meta → struct.meth.meta_2 |
| P298 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme → struct.meth.theme_2 |
| P299 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-appendix → struct.meth.appendix_2 |
| P300 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_1 |
| P301 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_2 |
| P302 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_3 |
| P303 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_4 |
| P304 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_5 |
| P305 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_6 |
| P306 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_7 |
| P307 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_8 |
| P308 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_9 |
| P309 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_10 |
| P310 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_11 |
| P311 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-table → struct.meth.table_12 |
| P312 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-meta → struct.meth.meta_3 |
| P313 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme → struct.meth.theme_3 |
| P314 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-appendix → struct.meth.appendix_3 |
| P315 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-meta → struct.meth.meta_4 |
| P316 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme → struct.meth.theme_4 |
| P317 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-appendix → struct.meth.appendix_4 |
| P318 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_1 |
| P319 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_2 |
| P320 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_3 |
| P321 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_4 |
| P322 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_5 |
| P323 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_6 |
| P324 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_7 |
| P325 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_8 |
| P326 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_9 |
| P327 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_10 |
| P328 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_11 |
| P329 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_12 |
| P330 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 M14 组头卡数（原键 theme_count_1，2026-09-20 归一为 group_N） |
| P331 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 M15 组头卡数（原键 theme_count_2，2026-09-20 归一为 group_N） |
| P332 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 M16（势定律）组头卡数（原键 theme_count_3，2026-09-20 归一为 group_N） |
| P333 | `java-architect-interview/chapter-core-methodology.html` | 方法论页『势』的五个横坐标数（原键 theme_count_4，改为语义单一键） |
| P334 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 M13 卡数（原键 theme_count_5，改为复用 canonical group_13） |
| P335 | `java-architect-interview/chapter-core-methodology.html` | 方法论页『G 组数』对照（与工程化页同源 canonical 键 engineering_groups；2026-09-21 统一键形） |
| P336 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_1 |
| P337 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_2 |
| P338 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_3 |
| P339 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_4 |
| P340 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_5 |
| P341 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_6 |
| P342 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_7 |
| P343 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_8 |
| P344 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_9 |
| P345 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_10 |
| P346 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_11 |
| P347 | `java-architect-interview/chapter-questions-scenario.html` | 升格 local:group-count → struct.scenario.group_12 |
| P348 | `java-architect-interview/chapter-production-pitfalls.html` | 踩坑页 meta 组数（pitfalls_groups） |
| P349 | `java-architect-interview-mind/mind-01-jvm-memory-classloading.html` | 升格 local:mind-note-local → struct.mind.mind-01-jvm-memory-classloading.mind-note-local_1 |
| P350 | `java-architect-interview-mind/mind-01-jvm-memory-classloading.html` | 升格 local:mind-note-local → struct.mind.mind-01-jvm-memory-classloading.mind-note-local_2 |
| P351 | `java-architect-interview-mind/index.html` | 升格 local:mind-pages → mind_pages |
| P352 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-meta → struct.mind.idx.mind-foot-meta_1 |
| P353 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-meta → struct.mind.idx.mind-foot-meta_2 |
| P354 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-meta → struct.mind.idx.mind-foot-meta_3 |
| P355 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_1 |
| P356 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_1 |
| P357 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_2 |
| P358 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_2 |
| P359 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_1 |
| P360 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_3 |
| P361 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_3 |
| P362 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_4 |
| P363 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_4 |
| P364 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_2 |
| P365 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_5 |
| P366 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_5 |
| P367 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_6 |
| P368 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_6 |
| P369 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_3 |
| P370 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_7 |
| P371 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_7 |
| P372 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_4 |
| P373 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_8 |
| P374 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_8 |
| P375 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_5 |
| P376 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_9 |
| P377 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_9 |
| P378 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_6 |
| P379 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_10 |
| P380 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_10 |
| P381 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_7 |
| P382 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_11 |
| P383 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_11 |
| P384 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_8 |
| P385 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_12 |
| P386 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_12 |
| P387 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_9 |
| P388 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_13 |
| P389 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_13 |
| P390 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_10 |
| P391 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_14 |
| P392 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_11 |
| P393 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-c → struct.mind.idx.mind-foot-c_15 |
| P394 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-meta → struct.mind.idx.mind-foot-meta_4 |
| P395 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-e → struct.mind.idx.mind-foot-e_14 |
| P396 | `java-architect-interview-mind/index.html` | 升格 local:mind-foot-s → struct.mind.idx.mind-foot-s_12 |
| P397 | `java-architect-interview-mind/mind-server-security-checkpoint.html` | 升格 local:mind-note-local → struct.mind.mind-server-security-checkpoint.mind-note-local_1 |
| P398 | `java-architect-interview-mind/mind-core-methodology.html` | 升格 local:meth-group-count → struct.meth.group_13 |
| P399 | `index.html` | 根 index 方法论 M13 组卡数 |
| P400 | `index.html` | 根 index 方法论 M14 组卡数 |
| P401 | `index.html` | 根 index 方法论 M15 组卡数 |
| P402 | `index.html` | 根 index 方法论 M16(势) 组卡数 |
| P407 | `index.html` | 根 index 方法论 M17(附) 组卡数 |
| P404 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 附(M17) 卡数 |
| P405 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 势(M16) 卡数 |
| P406 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 M17 组头卡数 |
| P403 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 M13 组头卡数（原缺失：正文自证『已在组头』而组头为空） |
| P408 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 M16 势定律组数（原误复用章节页 P405，2026-09-21 独立注册） |
| P409 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 M17 表达与对齐组数（原误复用章节页 P404，2026-09-21 独立注册） |
| P410 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M1 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P411 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M2 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P412 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M3 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P413 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M4 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P414 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M5 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P415 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M6 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P416 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M7 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P417 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M8 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P418 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M9 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P419 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M10 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P420 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M11 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P421 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M12 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P422 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M14 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P423 | `java-architect-interview-mind/mind-core-methodology.html` | mind 导图页 map-col M15 组数（2026-09-21 由纯文本升格为受保护计数位） |
| P424 | `java-architect-interview/chapter-core-methodology.html` | chapter-core-methodology 道层 layer-hang 下挂 chip 数（2026-09-21 由纯文本升格为受保护计数位） |
| P425 | `java-architect-interview/chapter-core-methodology.html` | chapter-core-methodology 法层 layer-hang 下挂 chip 数（2026-09-21 由纯文本升格为受保护计数位） |
| P426 | `java-architect-interview/chapter-core-methodology.html` | chapter-core-methodology 术层 layer-hang 下挂 chip 数（2026-09-21 由纯文本升格为受保护计数位） |
| P427 | `java-architect-interview/chapter-core-methodology.html` | chapter-core-methodology 器层 layer-hang 下挂 chip 数（2026-09-21 由纯文本升格为受保护计数位） |
| P428 | `java-architect-interview/chapter-core-methodology.html` | chapter-core-methodology 势层 layer-hang 下挂 chip 数（2026-09-21 由纯文本升格为受保护计数位） |
| P429 | `java-architect-interview/index.html` | 章节 index 方法论卡 footer「15 篇」篇章页数（2026-09-21 由正文裸数字升格） |
| P430 | `java-architect-interview/nav-overview-priority.html` | overview 页头副标题「15 篇章」篇章页数（2026-09-21 升格） |
| P431 | `java-architect-interview/nav-overview-priority.html` | overview 页脚「15 章深度 Q&A」篇章页数（2026-09-21 升格） |
| P432 | `java-architect-interview-mind/index.html` | mind index 副标题「15 篇知识篇章」篇章页数（2026-09-21 升格） |
| P433 | `java-architect-interview-mind/index.html` | mind index idx-meta 算式「1+1+1+15+1」中的篇章项（2026-09-21 升格；无单位词，由一致性链路保障） |
| P434 | `java-architect-interview/chapter-core-methodology.html` | 方法论页正文「本库不是 15 篇平行说明书」篇章页数（2026-09-21 升格） |
| P435 | `java-architect-interview-mind/mind-core-methodology-dao-fa-shu.html` | mind 势页正文「M16 单列势定律（11 张）」组卡数（2026-09-21 升格；同键既有位 P332 在 chapter-core-methodology） |
| P436 | `java-architect-interview-mind/mind-core-methodology-dao-fa-shu.html` | mind 势页正文「M17 表达与对齐（4 张）」组卡数（2026-09-21 升格；同键既有位 P406） |
| P437 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 chapter-meta 势卡数 |
| P438 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 chapter-meta 附卡数 |
| P439 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 十七组卡数表 M13 |
| P440 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 十七组卡数表 M14 |
| P441 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 十七组卡数表 M15 |
| P442 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 十七组卡数表 M16 |
<!-- COUNTS:END -->

## 7. 双站导航约定（简述）

- **放置（硬约束，与 `docs/format-shared.md` §4.2 一致）**：
  - 有导航页：`body` 首子块 = `<div class="site-page-nav site-page-nav--top">` → `<nav class="chapter-nav-top">`；正文与 `<footer>`（若有）之后、**所有** `<script>` 之前 = `site-page-nav--bottom` → `chapter-nav`。
  - **无导航页**：仅根 `index.html`、章节站 `java-architect-interview/index.html`；导图 `index.html` 与其余内容页均须有顶底导航。
  - 壳层 `.site-page-nav--top/--bottom` 上下 `padding` 对称；首屏 hero（`.map-hero` / `.ov-hero`）勿再叠加大 `padding-top`。
- 章节页 `.chapter-nav-top`（顶部）+ `.chapter-nav`（底部），**顶底内侧 HTML 必须一致**。三槽结构：
  - 左：翻页 `nav-prev`（← 上一篇）或 `nav-home`（← 返回目录）
  - 中：`nav-center` 内 `nav-mind`（篇章页固定顺序：核心方法论 → 全部章节 → 本章思维导图）
  - 右：`nav-next`（下一篇 →）或收束用 `nav-home`（返回目录 →）
- **章节站阅读链路**：`核心方法论 → 工程化要点 → 生产踩坑 → C01…C15 → 服务端安全 → 核心原理速查 → 高频场景题`；导图站同序 `mind-*`。
- 箭头统一字面量 `←` / `→`；回目录文案统一「返回目录」（禁止「返回首页」）；左右已链过的目标勿在 `nav-center` 重复。
- **侧栏分组标题**：凡带 `toc-group` 的页面，`toc-group-title` 必须是 `<a href="#…">`（禁止 `div`）；`nav.js` 会在条目高亮时同步给同组 `a.toc-group-title` 加 `.active`。锚点约定见 `docs/format-shared.md` §4.1。
- 导图页居中组：全部章节 / 导图总览 / 本导图对应章节（`nav-mind`）；首篇左已是导图总览时，居中去掉「导图总览」。
- 顶部/底部按钮 `padding`/`font-size`/`gap` 须同步一致，避免高度差。
- 两站共用 `java-architect-interview/assets/design-system.css`、`theme-init.js` 与 `nav.js`，一处修改惠及全部。

## 7.1 手机小屏强制（MOBILE-MANDATORY）

与 `AGENTS.md` 硬红线第 6 条、`docs/format-shared.md` §8 同级：

- 全站页面必须适配 ≤768px（主）与 ≤480px（极小屏）；必须含 viewport。
- 共享基线在 `assets/design-system.css` 的 `MOBILE-MANDATORY` 段；页面内联桌面布局必须自带 `@media` 覆盖。
- `validate_kb.py` 检查：CSS 标记、根/导图 index、导图页媒体查询、全站 viewport。

## 7.2 HTML 格式化与 Mermaid（Prettier）

与 `docs/format-shared.md` §10 同级：

- 44 个用户可见 HTML 用仓库根 `npm run format:html`（Prettier 3 + `normalize_html_closers.py`）统一格式；配置见 `.prettierrc.json`（`printWidth: 10000`）。
- **每个** `<div class="mermaid">` 上一行必须 `<!-- prettier-ignore -->`，禁止格式化塌缩图源码；缺省可跑 `ensure_mermaid_prettier_ignore.py`。
- 新增/改图后：加 ignore → `npm run format:html` → `npm run format:html:check` → `validate_kb.py`（含 ignore / 换行 / 导航壳检查）。
- 主题切换器与回顶/去底由 `theme-init.js` 注入（非手写第二套）。
- 顶底导航壳 / 阅读链路见 §7；小屏见 §7.1。

## 8. 章节站首页（`java-architect-interview/index.html`）

- **卡片顺序人工编排**：勿按文件名自动重排；现序为 导图 → 方法论 → 工程化 → 核心原理 → 场景 → 优先级总览 → ch01～15 → 安全。细则见 `docs/format-special.md` §7。
- **难度徽标**：可按目标页 `data-difficulty` 实计的卡片均写 **专家 → 架构 → 高级** 的 `×N`（0 档省略）；导图入口 / 安全等无难度题卡的只标档位。详见 `docs/format-special.md` §7。
- **技术栈全景 / 最新技术趋势**：`<details class="tag-cloud|trend-section index-fold">`，**默认折叠**（不加 `open`）。
