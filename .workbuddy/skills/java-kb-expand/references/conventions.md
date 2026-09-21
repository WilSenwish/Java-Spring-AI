# 题库结构约定（java-kb-expand 参考）

本文件编码 `java-architect-interview` 知识库的全部结构约定，供脚本与 Agent 直接取用。

## 1. 题号前缀与三级目录

- 篇章页：`chapter-core-methodology.html` 用 **M**（分组 M01~M16，共 94 卡，如 `M01.02` / `M16.04`；道 M01–M02，法 M03–M07，术 M08–M16 且 M12 在 TOC 收口、R2 仍标法），`chapter-engineering-practices.html` 用 **G**（G01~G08，卡数见 `engineering`，方法论同款三层 insight/principle/application，专篇键），`chapter-01~15` 用 **C**（如 `C10.26`）。
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
  - **仍保留**：M 卡 `data-priority`（74/126）属性，但不呈现。新增 M/G/K 卡（含导航位）时**勿写 `data-difficulty`、勿贴难度徽标**。
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

改题数或挪卡后，下列位必须与正文实际卡数一致（`sync_counts` positions **P01–P102** + `validate_kb` 3b/3b2/3c）：

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
2. **禁止**在聚合 UI 容器留下裸「N 题/卡/道/组」。
3. **禁止**在页面用自然语言声明口径（例如宣称某类卡与 `total` 的包含关系）；口径只写在本规约 + `validate_kb.py` / `sync_counts.py`。
4. **改题后**跑 `sync_counts check` + `validate_kb.py`。
5. overview 类型三级、方法论统计表、Mermaid 旁注：见下补充条。

补充：

- **overview `ov-type`**：每难度子组须拆篇章/核心原理/场景题；`ov-type-count` = 块内题数（`validate_kb` 3b2），键在 `struct`。
- **方法论统计表**：`compare-table`「卡数」列 → `struct.meth.table_*`；表尾合计 → L0（methodology）。
- **Mermaid**：节点纯文本；旁注挂锚点。
- **口径**：`total` = 篇章+核心原理+场景；`methodology` / `engineering` / `pitfalls` 为专篇键；不设全站合计。
### 5.2 项目根 `Java Spring AI/index.html`（全量快照）
- **Hero 统计块**（`.dir-hero` 内两行，共 10 项；改数走 `sync_counts.py`，勿手改）：
  - 首行 `.dir-stats`（4 项，无 `stat-tag`）：编号体系 `6`（`struct.misc.index.site-meta_1`，P108）/ 页面篇章 `20`（`site-meta_2`，P109）/ **思维导图 `19`（`mind_pages`，P37）** / 题目总数 `total`（P36）。
  - 次行 `.dir-stats.dir-stats-sub`（6 项，各带 `stat-tag`）：M 核心方法论 / G 工程化要点 / K 生产踩坑 / C 深度 Q&A / E 核心原理速查 / S 真实场景题。
  - 口径：M/G/K 为专篇键，**各自单独计数，禁止「题数+M+G+K」式合计**；「全站 N 题」仅指 `total`（C+E+S）。禁止 `kb-count-local`。
  - **`mind_pages` 是全站唯一的导图页数键**（19 = 15 篇章导图 + 方法论 + 工程化 + 踩坑 + 安全），三处展示：根 index P37 / 章节导航 index P222 / 导图站 P351；文案一律「思维导图」/「思维导图页」。（章节导航 hero 原有第 7 格 P221，2026-09-16 长官移除其「思维导图」统计卡后该位作废并已从 `positions` 删除。**删展示位必须同步删 position**：残留 position 会让 `sync_counts.py check` 与 `validate_kb.py` 的「kb-count 标记」项双双 FAIL。）
  - 小屏列数（**按块定列，使列数与项数整除**）：≤768px 首行 `.dir-stats` **4 列**（4 项＝1 行）、次行 `.dir-stats-sub` **3 列**（6 项＝2 行）；≤480px 两行统一 **2 列**（4 项＝2 行、6 项＝3 行）。**加计数项须让两行项数各自能被当前列数整除**，否则末行出现半空格子（历史：首行 3 项时 375px 下「题目总数」独占一行、右侧整格留白；首行 4 项而用 3 列时 481~768px 也会「3+1」留白）。
- 每题一个 `<li class="q-item">…，<span class="q-id">ID</span>…，<span class="q-tags"><span class="difficulty">…</span><span class="priority priority-pX">PX</span></span></li>`；新增题须在对应 ID 的 li 后插入。
  - **结构完整性**：`q-tags` 必须闭合、`<a>` 不得顶格（须与同级 li 内缩进一致）。历史新增题曾出现「顶格 `<a>` + `q-tags` 未闭合」（2026-09-16 实测 7 条：C11.28/29/30、S12.08/09 顶格+未闭合，G07.08/09 仅未闭合），渲染上表现为徽标错位、层级断开。门禁 `scripts/check_index_badges.py`（顶格 `<a href=…>` 与未闭合 `q-tags` 均为 FAIL）。
  - **优先级补齐口径**：缺失徽标按**镜像源页**判定——源页有优先级则补（C11.28/29/30、S12.08/09 补 `P1`），源页无优先级则**不补，仅修结构**（G/K 块源页本无优先级，`validate_kb` 亦不强制）。**M/G/K 三类卡一律不呈现等级与优先级徽标**（2026-09-16 长官决策，两次下达：先三专篇页、再三处导航位）——根 index M/G/K 区块 220 条 `.q-tags` 已整块移除，全文口径见 §2 例外条。**长尾提醒**：删徽标会连带**孤立计数位**（本轮 6 个：P74/P75/P76/P103/P104/P105 随章节导航 `card-tags` 一并作废），必须同步从 `kb-counts.json` 的 `positions` 删除并跑 `sync_counts.py render`。
- per-chapter / per-group `dir-count` / `dir-group-count`：**必须等于**紧随其后的 `ul.q-list` 内卡片数；各篇章 `dir-count` 求和 = 篇章总数（见 COUNTS）。
  - **新增卡片四步（漏任一步都会「假绿」，2026-09-20 血泪）**：① 章节页正文卡 + TOC + Mermaid 组图节点；② 对应 mind 导图页（卡 + mindmap 节点 + 列表节点）；③ **根 index 对应 `dir-group` 的 `ul.q-list` 内按序插入 `<li class="q-item">`**——只改 `dir-count` 计数而不补 li，会直接触发 `validate_kb` 的 `[根index dir-count] 计数≠列表` FAIL；同时组的 `dir-group-count` 须 `sync_counts.py bump struct.root.dir_group_N=+1`（否则补 li 后又触发 `[根index dir-group]` FAIL）；④ **把新 ID 登记进 `validate_kb.py` 顶部 `NEW_IDS`（第 85 行「待填：本轮新增/改动题号」，手工维护）——未登记则该卡的「落位 + 双编码」检查被静默跳过、不报错，门禁显示 ALL PASS 实为假绿**。计数一律走 `sync_counts.py bump` 唯一入口，勿手改数字。
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
  - **方法论卡**：`94 卡 · 16 组`（M01~M16）。
  - **工程化卡**：`24 卡 · 8 组`（G01~G08）。
  - **安全手册卡**：`手册 7 章` + 该 mind 页并入的原理/场景数。
- `idx-meta` 题量表达式形如 `篇章+原理+场景`（取值见 COUNTS，勿写死旧数）。

### 5.5 场景 / 核心原理页分组计数
- 场景页正文 `span.group-count`、根 index 场景区 `dir-group-count`，均须等于该组 `S##.##` 实际题数（当前：5/6/5/6/5/6/7/8/5/5/6/8）。
- 核心原理页各组实际题数（当前：4/4/8/8/4/6/10/4/6/6/5/8）；根 index 对应 `dir-group-count` 同步。
- **散文计数位**：页头/来源段「本页 N 道 / 高频核心原理 N 题 / overview 全站 N 道…」等必须登记为 `kb-counts.json` positions（**P01–P102**），改数走 `sync_counts.py bump`；`validate_kb.py` 第 0 步强制 `sync_counts check`，第 0c 步扫描 L1 聚合 UI。
## 6. 权威计数示例（2026-09-03 OPT-A 后固化）

<!-- COUNTS:BEGIN 由 scripts/sync_counts.py render 生成，勿手改 -->
- 题目总量 **400** = 篇章 252 + 核心原理 74 + 场景 74
- 优先级 **P0=94 / P1=248 / P2=58**（求和 = 400）
- 难度 **专家 46 / 架构师 192 / 高级开发 162**（求和 = 400；仅覆盖 C/E/S，M/G/K 不分级）
- 方法论 **137 卡**（M01~M16，专篇键 methodology；**不分难度等级**）
- 工程化 **65 卡**（G01~G08，专篇键 engineering；**不分难度等级**）
- 生产踩坑 **65 卡**（K01~K08，专篇键 pitfalls；**不分难度等级**）
- 口径（程序约束）：题目总量 total=篇章+核心原理+场景；M/G/K 为专篇键，不进 total；结构计数见 struct；**禁止 kb-count-local；禁止页面用自然语言声明口径**
- 方法论细分：带优先级 85/137（2026-09-16 起 M/G/K 不设难度计数）

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
| P223 | `java-architect-interview/index.html` | 升格 local:chap-footer-meta → struct.chap.idx.meta_1 |
| P224 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_1 |
| P225 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_2 |
| P226 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_3 |
| P227 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_4 |
| P228 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_5 |
| P229 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_6 |
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
| P253 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c06.senior |
| P254 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c07.n |
| P255 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c07.expert |
| P256 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c07.architect |
| P257 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c07.senior |
| P258 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c08.n |
| P259 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c08.expert |
| P260 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c08.architect |
| P261 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c08.senior |
| P262 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c09.n |
| P263 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c09.expert |
| P264 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c09.architect |
| P265 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c09.senior |
| P266 | `java-architect-interview/index.html` | 升格 local:chap-desc-local → struct.misc.chap_index.chap-desc-local_1 |
| P267 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c10.n |
| P268 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c10.expert |
| P269 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_7 |
| P270 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_8 |
| P271 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c11.n |
| P272 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c11.expert |
| P273 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c11.architect |
| P274 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_9 |
| P275 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c12.n |
| P276 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c12.expert |
| P277 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c12.architect |
| P278 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c12.senior |
| P279 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c13.n |
| P280 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c13.expert |
| P281 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c13.architect |
| P282 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c13.senior |
| P283 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c14.n |
| P284 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c14.expert |
| P285 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c14.architect |
| P286 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.diff_misc_10 |
| P287 | `java-architect-interview/index.html` | 升格 local:chap-footer → struct.chap.idx.c15.n |
| P288 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c15.expert |
| P289 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c15.architect |
| P290 | `java-architect-interview/index.html` | 升格 local:chap-footer-diff → struct.chap.idx.c15.senior |
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
| P332 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 M16 组头卡数（原键 theme_count_3，2026-09-20 归一为 group_N） |
| P333 | `java-architect-interview/chapter-core-methodology.html` | 方法论页『势』的五个横坐标数（原键 theme_count_4，改为语义单一键） |
| P334 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 M13 卡数（原键 theme_count_5，改为复用 canonical group_13） |
| P335 | `java-architect-interview/chapter-core-methodology.html` | 方法论页『G 组数』对照（原键 theme_count_6，改为复用 canonical engineering_groups） |
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
| P402 | `index.html` | 根 index 方法论 M16 组卡数 |
| P403 | `java-architect-interview/chapter-core-methodology.html` | 方法论页 M13 组头卡数（原缺失：正文自证『已在组头』而组头为空） |
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
