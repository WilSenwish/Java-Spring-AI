---
name: java-kb-expand
description: 当用户提供外部链接（豆包/知乎/CSDN/技术博客等）并询问"内容可补充到哪个篇章/以何种形式补充"，或要求把链接内容入库到 java-architect-interview 知识库时使用。本技能固化"抓取链接→归属判定与覆盖度核查→给出形式候选（确认式）→用户确认后全量同步 7 文件→全量校验"的标准流程，内置双站结构、4 份聚合统计页、data-page-node-id 红线与可复用校验脚本，任何 Agent 均可据此独立完成同样的题库拓展任务。
agent_created: true
---

# Java 工程能力知识库 · 链接拓展流程

## Overview

把一篇外部技术链接（豆包 thread / 知乎 / CSDN / 官方文档等）的内容，按需入库到 `java-architect-interview` 静态 HTML 知识库。流程核心是**先核查覆盖度、再确认形式、后全量同步并校验**，绝不盲目新增重复卡片。

本技能编码了该项目题库的全部结构约定、权威计数口径、红线与坑位，使任意 Agent 无需先验知识即可复现。详细的 HTML 卡片/导图节点模板与聚合页字段名见 `references/conventions.md`；校验脚本见 `scripts/validate_kb.py`。

## 项目结构红线（必读）

题库为**纯静态 HTML 双站**，两站经导航互链：

- **章节站** `java-architect-interview/`：15 个编号篇章页 `chapter-01~15-*.html` + 方法论页 `chapter-core-methodology.html`（M 前缀）+ 工程化要点页 `chapter-engineering-practices.html`（G 前缀）+ 生产踩坑页 `chapter-production-pitfalls.html`（K）+ 安全卡 `nav-server-security-checkpoint.html` + 核心原理页 `chapter-questions-eight-part.html`（E 前缀）+ 场景页 `chapter-questions-scenario.html`（S 前缀）+ 章节导航 `index.html`。
- **导图站** `java-architect-interview-mind/`：对应 `mind-01~15-*.html` + `mind-core-methodology.html` + `mind-engineering-practices.html` + `mind-server-security-checkpoint.html` + 导图导航 `index.html`（18 个导图页，线性链顺序见 `references/conventions.md` §7）。
- **项目根** `Java Spring AI/index.html`：全部题目的扁平全量快照（每题一个 `q-item` li，带难度 + `priority-pX` 徽标）。

题号前缀：方法论页用 **M**，工程化要点页用 **G**，`chapter-01~15` 用 **C**，`E` 核心原理、`S` 场景。卡片三级目录为 `页面篇章 / 分组 / 题号`。

聚合统计页共 **4 份**，任何题目数/优先级的增删改都必须联动（详见 `references/conventions.md` §4）：① 项目根 `index.html`；② `java-architect-interview/index.html`；③ `java-architect-interview-mind/index.html`（题量表达式 `N篇章+N核心原理+N场景`）；④ `nav-overview-priority.html`（`ov-stat-num` 10 项 + 9 子组标题，按**优先级×难度**组织；不含 M/G/K）。

**绝对红线：**
1. **禁止用 `present_files` 预览任何 HTML**（含在预览面板点击链接）。实测预览服务会持有文件并在外部变更时重新序列化、注入 `data-page-node-id` 属性。交付方式只有「绝对路径 + 文字结论」。
2. **禁止重复**：先核查覆盖度，不得新增与现有卡片/场景题重复的题。同源重复内容应补入现有卡（不新增计数）或不入库。
3. **P3 优先级已废除**：`data-priority` 仅 P0/P1/P2 三级。
4. 共享样式集中在 `assets/design-system.css`，优先改共享 CSS，不逐卡内联。
5. **手机小屏强制（MOBILE-MANDATORY）**：全站必须适配 ≤768/≤480；细则 `docs/format-shared.md` §8；`validate_kb` 校验 CSS 标记、viewport、根/导图小屏媒体查询。
6. **主题 / 暗黑模式**：用户页须在 CSS 前引入 `theme-init.js`；令牌换肤见 `docs/format-shared.md` §9；切换器与回顶/去底由 `theme-init.js` 注入。
7. **顶/底章节导航**：仅根 / 章节 `index.html` 无导航；其余页顶栏贴 `body` 首、底栏在脚本前；壳层 `.site-page-nav`；细则 `docs/format-shared.md` §4.2。
8. **HTML Prettier + Mermaid**：改 HTML 后 `npm run format:html`；每个 `<div class="mermaid">` 上一行 `<!-- prettier-ignore -->`；见 `docs/format-shared.md` §10。

权威计数口径（以 `ov-stat-num` 与根 index 全量徽标为权威三源，三者须相等）：
- 总量 = 篇章(深度Q&A) + 核心原理 + 场景
- 优先级 P0 / P1 / P2（求和 = 总量）
- 难度三级：专家级 / 架构级 / 高级开发（求和 = 总量）

<!-- COUNTS:BEGIN 由 scripts/sync_counts.py render 生成，勿手改 -->
- 题目总量 **398** = 篇章 251 + 核心原理 73 + 场景 74
- 优先级 **P0=94 / P1=246 / P2=58**（求和 = 398）
- 难度 **专家 46 / 架构 191 / 高级开发 161**（求和 = 398）
- 方法论 **91 卡**（M01~M12，专篇键 methodology）
- 工程化 **65 卡**（G01~G08，专篇键 engineering）
- 生产踩坑 **64 卡**（K01~K08，专篇键 pitfalls）
- 口径（程序约束）：题目总量 total=篇章+核心原理+场景；M/G/K 为专篇键，不进 total；结构计数见 struct；**禁止 kb-count-local；禁止页面用自然语言声明口径**
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
| P10 | `docs/README.md` | docs/README.md 文件表方法论数 |
| P11 | `docs/README.md` | docs/README.md 难度分布段 |
| P12 | `docs/README.md` | docs/README.md 方法论带优先级数（分子） |
| P13 | `docs/README.md` | docs/README.md 方法论带优先级数（分母） |
| P14 | `docs/format-shared.md` | docs/format-shared.md 分子 |
| P15 | `docs/format-shared.md` | docs/format-shared.md 分母 |
| P16 | `docs/format-special.md` | docs/format-special.md 定位段 |
| P17 | `docs/format-special.md` | docs/format-special.md 难度段合计 |
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
| P103 | `java-architect-interview/index.html` | 章节 index 工程化卡 footer 架构数 |
| P104 | `java-architect-interview/index.html` | 章节 index 工程化卡 footer 高级数 |
| P105 | `java-architect-interview/index.html` | 章节 index 踩坑卡 footer 高级数 |
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
| P221 | `java-architect-interview/index.html` | 升格 local:mind-pages → mind_pages |
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
| P330 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme-count → struct.meth.theme_count_1 |
| P331 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme-count → struct.meth.theme_count_2 |
| P332 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme-count → struct.meth.theme_count_3 |
| P333 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme-count → struct.meth.theme_count_4 |
| P334 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme-count → struct.meth.theme_count_5 |
| P335 | `java-architect-interview/chapter-core-methodology.html` | 升格 local:meth-theme-count → struct.meth.theme_count_6 |
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
<!-- COUNTS:END -->

## Workflow（标准 5 步）

### Step 1 · 抓取链接全文
用 `WebFetch` 抓取链接，prompt 要求完整提取正文、知识点、代码、对比表、结论，并标注涉及的 Java/Spring/微服务/并发/IO/数据库/缓存/消息队列/网络/操作系统/JVM/分布式/架构方向。链接可能 AI 生成、有误差，需结合题库事实判断。

**⚠️ 抓取失败 / 正文为空降级流程（高频：豆包 thread 等多需登录，WebFetch 常只返回标题+日期）：**
- 若 `WebFetch` 仅返回标题/日期、正文为空，或返回"需要登录 / 正文无法获取"：**严禁基于标题臆测正文内容去做覆盖度核查**（会产出虚假结论）。
- 降级动作（按顺序）：
  1. **如实告知用户**正文未获取，并明确这是抓取限制而非内容不存在。
  2. 仅基于**标题关键词**给出「宿主篇章初判」候选（当前实际文件映射：**Spring/Bean/IoC/AOP/事务 → `chapter-05-spring-core.html`（第 05 篇，非数据库！）**；**MySQL 索引/隐式转换/慢SQL/EXPLAIN → `chapter-07-mysql-deep.html`（第 07 篇）**；**缓存/Redis → `chapter-08-redis-cache.html`（第 08 篇）**；MQ → `chapter-06-*.html`（第 06 篇）；**数据库/分库分表/NoSQL/向量 → `chapter-14-databases.html`（第 14 篇）**；微服务/注册发现/配置/限流/灰度 → `chapter-10-*.html`（第 10 篇）；分布式事务/锁/ID → `chapter-09-*.html`（第 09 篇）；JVM/GC → `chapter-12-*.html`（第 12 篇）；网络/epoll/IO/Reactor → `chapter-13-*.html`（第 13 篇）），并**显式标注"未经正文覆盖度核查"**。**⚠️ 历史坑：技能旧版把"数据库→第05篇"已失效，第05篇现为 Spring Core，数据库相关内容在 07（MySQL 深）/14（分库分表/NoSQL），归并前务必 `Grep` 实定位文件名而非套用篇章号。**
  3. **请用户提供链接正文**（粘贴文本 / 导出 md / 截图 OCR），收到后再严格走 Step 2~5。
  4. 收到正文后，先用 `Grep` 在题库内检索标题里的核心术语，定位候选宿主卡并 `Read` 全文做逐点比对（回到标准流程）。

### Step 2 · 归属判定 + 覆盖度核查（不可跳过）
1. 用 `Grep` 在项目内检索链接关键词，定位最匹配的宿主篇章/卡片。
2. **读取候选卡片的完整现有全文**（用 `Read`），逐点比对链接知识点，产出覆盖度核查表：每项标 ✅已覆盖 / 🔴缺口 / 🟡可强化。
3. 判定三种情形：
   - **全新知识点** → 归并到最匹配篇章，可能新增卡。
   - **部分覆盖** → 仅补缺口，不重复已有部分。
   - **同源重复（>80% 已覆盖）** → 不能新开卡（会与现有卡/场景题双重重复），只补实质增量或判定不入库。
   - **多元聚合链接（一个链接含多个主题）** → 逐主题拆开，分别走上面的覆盖度核查；同源重复部分直接排除，缺口部分按价值归并到不同宿主卡（补层/新卡）。常见形态：Nacos+Sentinel+推送范式聚合、epoll+Reactor+IOCP 聚合。⚠️ 若某主题归并到非默认宿主（如"Nacos 版本演进"内容在 `C10.08 配置中心设计` 而非 `C10.01 注册发现`，"Sentinel 版本演进"在 `C10.03 限流熔断` 而非 `C10.02 API 网关`），**必须以 `Grep` 实际定位含该术语的卡片**，勿凭记忆套用卡号（曾因记错 C10.02=C10.03 导致宿主选错）。
   - **比较表第三极不一致 / 桥接题（高频坑，归并判定必查）**：链接若以"Redis/ZK/Etcd 锁对比"为题，而宿主卡（如 `C09.03 分布式锁三种实现对比`）的对比表第三列是「**数据库锁**」而非「**Etcd 锁**」，则 **Etcd 锁是真实缺口**（数据库锁 ≠ Etcd 锁，不能因"都讲三种实现"就判已覆盖，须逐列比对主语）。同理，当链接问"**A 与 B 的联系**"且 A 在某卡、B 在另一卡（如「分布式锁 ↔ 拜占庭容错」：锁在 C09.03、拜占庭在 C09.10），该**桥接视角本身常是缺口**——两卡各自覆盖了 A、B，但没人把"A 用到的共识模型属于 CFT 而非 BFT"这条线连起来。处理：优先以**补层（形式4）**补入较对味的宿主卡（本例 Etcd 锁+Kleppmann 批判入 C09.03、桥接一句入 C09.10），**不要新开卡**（会与两卡强重叠、制造同源重复）；仅当该合成题本身是高频独立知识点、且缺口占比 > 30% 时，才考虑独立新卡。
  - **概念辨析 / 同名主题卡已存在（高频，归并判定必查）**：链接是对某一已存在主题卡的「对话式展开 / 本质辨析」（如「蓝绿/金丝雀/灰度 本质区别」「什么是 X」「A 与 B 到底啥关系」），而题库已有同名/同主题卡（如 `C10.09 灰度发布与蓝绿部署如何设计` 已含四策略对比表 + 全链路灰度 + schema 灰度 + 共享库 pitfall）。处理：**先 `Read` 该卡全文逐点比对**，链接的增量通常是四类——① **操作细节**（如割接流程 停写→数据追平→一键全切→提升主库、写必须全切否则脑裂 split-brain）；② **关系辨析**（如「金丝雀是灰度子集、灰度可能永停 50% 做 A/B 测试业务效果、基于用户 ID 分流的回滚一致性」）；③ **心智模型**（如「环境特指无状态应用实例、数据库独立剥离、有状态 vs 无状态」）；④ **模式枚举**（如「蓝绿中数据库三种模式：独立库+CDC / 共享库+向后兼容 / 数据库蓝绿部署 AWS RDS」）。优先以**补层（形式4）**补入该卡，**勿新开卡**（会与现有卡强重叠、制造同源重复）。宿主速查：发布策略 / 蓝绿 / 金丝雀 / 灰度 / 流量染色 → `C10.09`（其 schema 灰度与 `C11` 的 Expand-Contract 呼应）；概率过滤器 / 布隆 / Counting-BF / 布谷鸟 / Cuckoo → `C08.09`（其已含三者对比表 + 误判率公式 + RedisBloom 基础 + Guava 单机提示，缺口常为① **底层数据结构深挖**：布谷鸟 `buckets[m][b]`、`b=4`、8bit 指纹、partial-key cuckoo hashing 异或公式 `i₂=i₁⊕hash(f)`、可逆、MaxKicks≈50、与普通布谷鸟哈希区别；② **单机 vs 分布式维度**：算法本身全单机内存无原生分布式协议、分布式靠外部存储（RedisBloom `BF.ADD`/`CF.DEL`）、Redis 集群单 key 不跨分片需 hash-tag/业务层多分片——此分片坑为高频真缺口）；概念辨析类链接若题库已有同名卡，一律先比对再补层。**（2026-09-03 实测校验：上列 C08.09 缺口预测与实际 Grep+Read 结果完全吻合——布谷鸟 `buckets[m][b]`/`b=4`/8bit 指纹/异或公式 `i₂=i₁⊕hash(f)` 可逆/MaxKicks≈50/与普通布谷鸟哈希对比/重复插入陷阱，以及单机 vs 分布式心智模型 + Redis 集群单 key 不跨分片 + hash-tag 多分片，全部为真缺口；该卡为 `senior`/`p2` 六层卡，补为第 7 层 `extension`。可放心沿用此速查。）**；隐式类型转换 / 索引失效 / CAST / CONVERT / IN 列表隐式转换 / Navicat 筛选加引号 → `C07.13`（其已含核心规则 + 转换对照表 + EXPLAIN + SHOW WARNINGS + collation 坑 + MyBatis 参数坑，缺口常为① **IN 列表数字常量导致 varchar 列被逐行转数字**（`uid IN(1001,1002)` 失效，改字符串列表）；② **MySQL 8.0 optimizer_trace 搜 `converted` 精准定位**被转换操作数（SHOW WARNINGS 之外的第二手段）；③ **完整转换规则补全**：日期时间列 vs 数字常量（`create_time=20260907` 数字转日期、列不动走索引）、`NULL=NULL` 为 NULL 须用 `IS NULL`；④ **CAST/CONVERT 完整类型清单 + `CONVERT(expr USING charset)` 字符集转码**；⑤ **高频面试五连问串讲**（where str=123 / where int='123' / join varchar×int / IN / 字符集）；⑥ **Navicat 默认加引号 = 工具规避隐式转换的保守策略** + 反例「`id='100'`（int）性能不差」。该卡为 `senior`/`p1` 六层卡，补为第 7 层 `extension`。**（2026-09-07 实测校验：上列 C07.13 缺口预测与实际 Grep+Read 结果完全吻合——IN 列表隐式转换、optimizer_trace `converted` 精准定位、日期数字转日期 + NULL 规则、CAST 完整类型清单 + CONVERT charset、面试五连问、Navicat 加引号，全部为真缺口；补为第 7 层 `extension`，mind-07 节点 body 同步补一句 + 加 `Navicat` 标签。可放心沿用此速查。）**
  - **算法类链接的「单机 vs 分布式维度」缺口（高频，归并判定必查）**：很多算法/数据结构链接（布隆/布谷鸟/跳表/LRU/SkipList/一致性哈希等）会以「单机实现 vs 分布式可用」为卖点展开。题库对应卡通常只零散提一句「单机库（Guava/Caffeine）不共享、集群用 Redis」，**缺系统化的「算法本身全单机内存、无原生分布式协议、分布式靠外部共享存储（RedisBloom/Redisson/Redis 模块）实现」心智模型 + 分布式坑位**（如 RedisBloom 一个过滤器 key 只能落一个分片、不自动跨节点、超大规模需业务层多分片 + hash-tag 强制定 slot）。该维度是高频真实缺口，补层时优先纳入。

### Step 3 · 给出形式候选（确认式，必须等用户选）
不要自行新增。给出归属结论 + 覆盖度表 + 2~4 个形式候选（见下「形式候选定义」），让用户以 `OPT-A / B / C…` 或自由偏好确认。明确每个候选的联动成本（改几个文件、是否动计数）。

### Step 4 · 执行（确认后）
1. **先备份**所有待改文件到 `tmp/`（如 `tmp/kb_<task>_backup/`）。
2. 用 **Python 脚本**（而非 `Edit`）做精确字符串替换并即时断言——`Edit` 对 overview 的大数字 `ov-stat-num` 存在"报成功但未落盘"的 IDE 实时改写竞态，脚本最可靠。脚本须内含断言：替换命中数 = 预期、插入内容存在、`data-page-node-id` 计数 = 0。
   - ⚠️ **防重复插入的断言必须按"卡片区间"判定，不能按文件级计数**：一个章节页通常**已存在多个** `data-layer="extension"` 层（如 chapter-08 有 6 个）。错写成 `assert t.count('data-layer="extension"') == 0` 会直接误报中断。正确写法：先切出目标卡区间再判定，并用「改前计数 +1」校验落盘。
     ```python
     _seg = t[t.index('id="C08.09"'):t.index('id="C08.10"')]
     assert 'data-layer="extension"' not in _seg, "该卡已有 extension 层"
     _before = t.count('data-layer="extension"')
     t2 = t.replace(ANCHOR, REPL, 1)
     assert t2.count('data-layer="extension"') == _before + 1
     ```
   - ⚠️ **关键词断言数要按实际出现次数写**：正文与「高频追问」里常重复同一术语（如 `partial-key cuckoo hashing` 出现 2 次），写 `== 1` 会误失败；先跑一次拿到真实计数再固化。
3. 按 `references/conventions.md` §4 的「7 文件同步清单」落盘；若仅补增量（不新增卡），只改章节页 + 对应 mind 页，4 份聚合页不动。
4. 环境 Python：`/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3`。

### Step 5 · 全量校验 + 记忆
1. 跑 `scripts/validate_kb.py`（会**强制**子进程跑 `sync_counts.py check`）：三权威源一致、**散文计数位 P01–P89 与真源一致**、各文件 `data-page-node-id` 全 0、无 `</spa` 截断、新卡双编码与落位。
2. **散文计数硬约束（2026-09-13 固化，禁止遗漏）**：
   - 页头/来源段里的「本页 N 道 / 234 道深度问答 / 72 道场景…」属于**散文位**，已登记为 `kb-counts.json` → `positions` 的 **P01–P89**（及后续扩展）。
   - **改题数必须**走 `sync_counts.py bump …`（或 bump 后 `apply`），禁止只改 HTML 散文数字。
   - `validate_kb.py` 第 0 步即 `sync_counts check`；任一散文位漂移 → **整次校验 FAIL**。
   - 新增散文数字时：先在 `kb-counts.json` 加 position（pattern 命中恰好 1 处），**同时**给数字套上 `data-kb-pos="Pxx"` 标记（见 `conventions.md` §5.1.4），再 `render` 更新 SKILL/AGENTS/conventions 的 COUNTS 表，最后 `check`。
   - **计数点分级（2026-09-13 全量固化）**：见 `conventions.md` **§5.1.4**。
     - **L0** SSOT：`data-kb-pos`（`kb-counts.json` positions，现 P01–P89）
     - **L1** 聚合 UI：页头/footer/desc/meta/subtitle/map-note/tagline/stat 等，禁止裸「N题|卡|道|组」
     - **L2** 页内结构：`ov-type`/`group-count`/`m-sub-count`/meth-table 等
     - **L3** 正文技术数字：不打标；**LX** Mermaid：节点纯文本 + 旁注锚点
     - `validate_kb`：**0b** 标记齐全，**0c** L1 容器扫描
3. **补层轮次也要做"计数体检"**：即使本轮不改计数，也应跑 `validate_kb.py`。另须覆盖：
   - **① `stat-number` 全部字段**（题目总数 ≠ 合计；合计 = 题数 + 方法论 + 工程化）。
   - **② 散文式数字**（已由 P27+ 与 sync_counts check 覆盖；章节 index `card-desc`/`card-footer` 等若新增散文数字须同步登记 position）。
   - **③ mind 页 summary 编号 ↔ 章节页 qa-card id 逐一对齐**。
2. 刷新 `Java Spring AI/.workbuddy/memory/MEMORY.md` 权威计数（若计数变更）+ 追加 `2026-09-03.md` 等价当日日志（按实际日期）记录入库/补增量。
3. 按红线交付：仅给绝对路径 + 文字结论，绝不预览。

## 形式候选定义（通用，非固定字母）

每轮用 `OPT-A/B/C…` 是用户选择的标签，不全局固定。常用形式：

- **形式1 · 新增篇章题**（`Cxx.xx`，架构级/P1 等）：需全量同步 7 文件（章节页 + 4 聚合 + 2 mind），计数 +1。
- **形式2 · 新增场景题**（`Sxx.xx`，归 `group-N`）：需全量同步 7 文件，计数 +1。
- **形式3 · 新增核心原理题**（`Exx.xx`）：需全量同步 7 文件，计数 +1。
- **形式4 · 补入现有卡**（不新增计数）：把增量作为现有卡的新 `qa-layer`（如 `data-layer="extension"`）+ 对应 mind 节点描述补一句；只改 2 文件，4 聚合页不动。
- **形式5 · 不入库**：判定同源重复、增量微小，仅记录核查结论。

难度/优先级建议：新卡默认 `data-difficulty="architect"` + `data-priority="p1"`（除非内容更偏专家级或高级开发）；双编码必须同步（属性 + 可见徽标）。

## 全量同步必改点（形式1/2/3）

详见 `references/conventions.md` §4。要点速览：

| 文件 | 必改 |
|---|---|
| `chapter-xx-*.html` | meta 题目数 / 难度计数 / 复习分钟 +N；TOC 加条目；导航前插卡片（双编码一致） |
| `nav-overview-priority.html` | 新增 ov-item（**插入位置见 `conventions.md` §5.1.1**：P0→P2 / 专家→架构→高级 / 组内 C→E→S / 题号升序，禁止随意插在同级某卡后）；`ov-stat-num` 共 **10 个**字段须同步 +N（顺序见 `kb-counts.json` → `ov_stat_order`）；对应子组标题与组标题/`ov-nav-cnt`/页头「全站 N 道」+N |
| `Java Spring AI/index.html`（根） | 类型计数 /「全站」仅=total（C+E+S）/ M·G·K 各自统计卡；`dir-count` + `dir-group-count`（须=该组 q-list 长度）+N；新增 q-item li |
| `java-architect-interview/index.html` | stat-number +N（C/E/S 与 M/G/K 分卡）；「全站」仅=total；章节 card-footer +N（**不枚举单题 ID**） |
| `mind-xx-*.html` | 主干范围 `C10.01–C10.N` 扩尾；插 map-card（summary/body/tags）；meta；`map-note` 并入清单 |
| `mind/index.html` | 题量表达式 `N+N+N`；对应卡片 `card-foot`（章节=C 卡数；原理/场景=该 mind `<summary>` 中 E/S 数） |

## 坑位速查（高频踩坑）

- **Edit 大数字竞态**：overview 的 `ov-stat-num` 用 `Edit` 报成功却未落盘，改用 Python 脚本替换。
- **章节导航页不枚举单题 ID**：`java-architect-interview/index.html` 只列章节卡片与统计，不含 `Cxx.xx`/`Sxx.xx` 条目——校验时"落位=False"属预期。
- **9 子组标题按 优先级×难度**（P0/P1/P2 各含 专家级/架构级/高级开发），不是难度×类型；同步前先算真实 9 宫格再对齐「子组标题 + ov-stat-num」两处。
- **overview 新卡落位排序（2026-09-13 硬约束）**：P0→P2 → 专家→架构→高级 → 子组内 **C→E→S** → **题号升序**。详见 `conventions.md` §5.1.1。`validate_kb.py` 校验子组内 `ov-num` 单调；曾因「插在同 priority 某 E 卡后」导致 E10 跑到 E09 前。三类占比见 §5.1.2（**不要求各桶均分**，按内容定级）。
- **全站分组/页头页尾计数（2026-09-13 全站固化）**：见 `conventions.md` §5.1.3。高频坑：① 场景卡插在 `</section>` 外导致 `group-count` 表面正确、结构孤儿；② overview `ov-nav-cnt`/组 h2 与 `ov-stat` 脱节；③ mind `card-foot`/mermaid「章节·原理·场景」未随并入清单更新；④ overview 难度子组未拆 C/E/S `ov-type` 或 `ov-type-count` 漂移。`validate_kb` 3b2/3c + `sync_counts` P47–P62 覆盖导航/组标题/聚合统计；改后必跑 `validate_kb.py`。
- **计数点标记（2026-09-14）**：见 `conventions.md` §5.1.4。新增/移动计数数字必须 `data-kb-pos` + `data-kb-count`（`counts`/`struct`）；**禁止** `kb-count-local`；禁止留下裸数字权威位。
- **计数点分级全量门禁（2026-09-13）**：L0–L2/LX 见 §5.1.4。改题或改聚合文案后必跑 `validate_kb.py`（含 **0c L1 扫描**）。禁止再「发现一处补一处」——新增展示题量必须先定级再落标。
- **overview 类型三级计数（2026-09-13）**：每个难度子组内须有 `ov-type`（篇章/核心原理/场景题）分块；禁止只挂一个「篇章」标题却混入 E/S。`ov-type-count` 必须=块内题数。见 `conventions.md` §5.1.3/§5.1.4；`validate_kb` 3b2。
- **overview `ov-stat-num` 共 11 项全要改**：总量/方法论/P0/P1/P2/专家级/架构级/高级开发/章节题/核心原理/场景题（顺序见 `ov_stat_order`）。最易漏的是「章节题」（篇章数）与「方法论」（紧随总量），漏改会导致 overview 与根 index、章节 index 的计数不一致。另须同步组标题/`ov-nav-cnt`/页头副标题「全站 N 道（篇章+原理+场景）」。
- **禁止全站合计**：跨大篇章/聚合只动 total（C+E+S）；加 M/G/K 只 bump 对应键，**不要**再维护 sum_all（已废除）。
- **mind 导图页数 18 与题量无关**（mind-01~15 + core + engineering + security）；`idx-meta` 五格含方法论/工程化卡数与 `N+N+N`；改题同步对应 `card-foot`。
- **`dir-group-count` / `group-count` / 篇章 `dir-count` 必须等于实际卡片数**；M12 禁止嵌套进「一、高并发」。
- **`</spa` 误判**：截断检测用负向前瞻排除合法 `</span>`（正则 `</spa(?!n>)`）。
- **路径双层**：`Java Spring AI/index.html` 是项目根全量快照，与子目录 `java-architect-interview/index.html` 是不同文件，全局核对须覆盖根那一层。
- **Bash 内置 `grep` 受 `_zshz` 干扰**：交叉验证用 `Grep` 工具或 `git grep`。
- **校验提取正则必须覆盖新编号空间（2026-09-04 实测）**：升层重编号后若用旧模式（如 `M0[1-7]\.\d{2}`）提取 after 集合做多重集断言，会"看不见" M08+ 的新号而误报不一致（替换其实已成功）；after 一律用宽模式 `M\d{2}\.\d{2}`。
- **Mermaid 被格式化压成一行（2026-09-15）**：每个 `<div class="mermaid">` 必须带上一行 `<!-- prettier-ignore -->`；统一用 `npm run format:html`。缺 ignore 时 Prettier 会塌缩图源码，`validate_kb` 会拦。
- **导图 Mermaid 节点未随新增卡补齐（2026-09-15 实测，validate_kb 查不出）**：同步导图时最易「补了 `<summary>` 主题卡、忘了 `<div class="mermaid">` 图节点」。实测新增 4 卡（C11.29/C11.30/G07.09/S12.09）时漏掉该步，致 mind-11 缺 2 节点、mind-engineering-practices 缺 1 节点（mind-12 因惯例带 ID 前缀反而被注意到）。**导图 Mermaid 是「本篇章卡的全量列点」**——章节 +N 张卡，图里必须 +N 个节点，插在交叉卡（E/S）节点之前以对齐原卡序；节点 id 在分支内递增，需插队时把后续 id 顺延（节点 id 不被别处引用，重编安全）。校验用 `scripts/check_mind_mermaid.py`。
- **mind `<summary>` 的 ID 对齐 ≠ 标题对齐（2026-09-15 发现并已修复）**：`validate_kb` 只比对 mind 与章节的 **ID 集合**，两者 ID 集合相同但**标题错位**时不会报错。实测已修 6 处：mind-11 `C11.12/C11.13/C11.14`（导图把「调度」标成 .12、「ES」标成 .13，并有 1 条章节页不存在的幽灵卡「分布式任务调度与搜索整合」→ 现改为 C11.12=API 网关 / C11.13=调度 / C11.14=ES，幽灵卡消除）、mind-12 `C12.16/C12.17`（互换编号）、`C12.22`（原误用 C12.21 的标题「十亿级向量库」，正文实为「Embedding 模型升级迁移」）。**改导图卡编号时，同步改三处**：① `map-body-text` 正文（须与新标题同题）；② Mermaid 节点（mind-11/12 的 C 卡节点不带 ID，须按**内容**改标签；mind-12 的 S 卡节点带 ID）；③ 全站交叉引用「与 Cxx.yy 印证」——实测 mind-11 有 4 处、mind-12 有 4 处引用这些 ID，编号一改即须跟着改。
- **内部编辑字眼会漏进正文（2026-09-15 实测，已纳入硬门禁）**：内容补写轮次留下的占位/批注词（`<strong>再加厚：</strong>`）曾残留在 10 个章节页 / 15 处，**任何校验都拦不住**（`validate_kb` 原无此检查）。已全部清除，并在 `validate_kb.py` 新增 **1f) 内部编辑字眼**检查（`EDITORIAL_WORDS = ["再加厚","补厚","占位段落","待补写"]`，全站须 0）。**教训：替换占位段落时，连包裹它的 `<strong>标签</strong>` 一并处理**，只换正文会留下标签壳。
- **顶底导航位置（2026-09-15）**：顶栏必须是 `body` 第一个壳；底栏在 footer 后、script 前；根/章节 index 无导航。勿再把导航塞进 `content-main` 中部。
- **移动端横向溢出：逐选择器枚举的兜底会漏整类容器（2026-09-15 实测事故）**：共享 CSS 原先只给 `qa-question`/`qa-layer-body`/`chapter-card *`/`epq-question` 等**逐个选择器**加 `overflow-wrap`，结果新增的 `epq-*` 正文容器整类被漏——核心原理页 375px 视口文档溢出 **248px**、**18 处**元素越界（最狠一条 `META-INF/spring/org.springframework…` 长 80 字符、超标 275px）。**修法**：`body` 加一条 `overflow-wrap: anywhere`（可继承属性，一条覆盖全站），**不要再罗列选择器**。裸 `<pre>` 另需兜底：实测 chapter-07 有 8 处未包 `.code-block`（无深色样式也无横滑）溢出 **814px**，已补包裹 + `pre { overflow-x: auto }`。
- **新门禁必须做正向验证（2026-09-15 实测，否则极易恒真）**：本轮 `check("overflow-wrap: anywhere" in css_txt)` 看似合理，但该串在 CSS 里本就有 9 处（属其它选择器规则），删掉 `body` 规则后依然 PASS —— **形同虚设**。规约：① 断言锚定结构而非子串（`re.search(r"^\s*body\s*\{[^}]*overflow-wrap:\s*anywhere", css, re.M)`）；② 每条新门禁跑一次「注入缺陷 → 必须 FAIL（exit≠0）→ 还原并核对 MD5」，脚本范式 `scripts/probe_validate_gate.py`。
- **移动端实测必须用 CDP，`--window-size` 不可用（2026-09-15）**：macOS 上 Chrome 的 `--window-size=375,812` 被最小窗口宽度钳制为 **500 CSS px**（新旧 headless 皆然）；且**文本溢出不改变元素 `getBoundingClientRect()`**，用 rect 判定会全漏。正确姿势：CDP `Emulation.setDeviceMetricsOverride` 设视口 → 以 `scrollWidth > clientWidth` 判溢出 → 向上排除「自身或祖先带 `overflow:auto/scroll/hidden`」的容器（代码块横滑属设计而非缺陷）。可复用：`scripts/check_mobile_overflow.js`（批量、Node 22 原生 WebSocket、零依赖）。
- **列表圆点/数字被甩出卡片：reset 抹掉了 `ul/ol` 默认缩进（2026-09-16 实测）**：共享 CSS 顶部 `* { margin: 0; padding: 0 }` 把 `ul`/`ol` 的 UA 默认 `padding-inline-start`（40px）一并归零，**全站列表缩进完全依赖各自类规则**——凡未匹配到类规则的列表 `padding-left` 即为 0，而 `list-style-position: outside` 的圆点/数字**绘制在内容盒之外**：桌面表现为「列表没有缩进、圆点贴着卡片边缘」，小屏（`.epq-card` 内边距收窄到 `0.9rem`=14.4px）直接越出卡片 2.6px。实测核心原理页 20 处（`.epq-section > ul/ol`）、安全检查页 1 处（`main.content-main > ol`）。**修法**：共享 CSS 加零特异度兜底 `:where(ul, ol) { padding-inline-start: 1.25rem }`；**写成裸选择器 `ul, ol { … }`（特异度 0,0,1）会顶掉 `.epq-kp-list`/`.map-col ul`/`.sidebar-toc ol` 的 `padding: 0`，反成新缺陷**（`validate_kb` 1h 拦此退化）。判定口径：`列表内容盒左边 − 边界容器内容盒左边 < 1.2×li字号 − 0.5px` 即缺陷；`list-style-position: inside` 与 `list-style-type: none` 不参与判定。可复用：`scripts/check_list_indent.js`（全站 44 页 × {1280, 375}，88 次测量）。
- **给 `ul` 写缩进时漏了 `ol`，数字比圆点少缩进（2026-09-16 实测）**：`nav-server-security-checkpoint.html` 的 `.content-main ul { padding-left: 24px }` **只写了 `ul`**，正文的有序列表（威胁建模步骤）于是回落到共享样式的 `1.25rem` 兜底 = 20px，**比同容器的圆点列表少缩进 4px** —— 这就是「数字列表缩进不够」的真身（`chapter-questions-scenario.html` 的 `.reading-guide .guide-body ul { padding-left: 1.2em }` 是同类漏写，方向相反）。**修法**：给这些规则补上 `ol`（`.content-main ul, .content-main ol { … }`）；页内 `<style>` 与共享 CSS 同特异度时**页面样式后加载胜出**，故 `aside.sidebar-toc`（与 `main.content-main` 平级）不受影响。**排查手法**：`tmp/scan_ul_rules.py` 语义扫描「选择器含裸 `ul` 且不含 `ol`、声明含 `padding`」的规则（须同时匹配 `padding:` 简写，否则漏检；`.map-col ul`/`.epq-kp-list ul` 等 `list-style:none` 装饰列表要排除）。**门禁**：`check_list_indent.js` 新增「同容器 `min(ol pl) < max(ul pl) − 0.5`」判定（只比 `boundaryOf` 同一容器，`body` 级不参与）。

- **聚合页徽标结构断裂：漏 `.ov-badges` 包裹 / `q-item` 顶格与未闭合（2026-09-16 实测）**：根因是新增卡片时**只贴徽标、不贴容器**。① overview：难度+优先级徽标漏包 `<span class="ov-badges">` 时，二者成为 `.ov-item` 的直接 flex 子项并继承 `.ov-item { gap: var(--space-sm) }`（大间距），而正常项取 `.ov-badges { gap: 4px }` → 页面上**同列徽标间距时宽时窄**（实测 15 条：C06.15、C07.16、C08.12、C09.17、C10.29/30、C11.26/27/28、C12.33/34/35、C13.14、C14.13、C15.12）；② 根 index：新增题写成**顶格 `<a>`** 且 `<span class="q-tags">` **未闭合**（实测 7 条：C11.28/29/30、S12.08/09、G07.08/09）→ 渲染上徽标错位、层级断开。**修法**：overview 补包裹；index 取上一 `<a>` 行缩进并闭合 `q-tags`。**优先级补齐口径 = 镜像源页**：源页有级则补（C11.28/29/30、S12.08/09 补 `P1`），源页无级则不补只修结构（G/K 块）；**根 index 方法论块（M 卡）整体不加优先级**（长官决策，M 卡优先级只在章节页呈现）。**门禁** `scripts/check_index_badges.py`（正向验证：修复后 PASS / 缺陷版 FAIL 29）。**教训：HTML 结构分析一律按块解析（`<li class="q-item">…</li>`），按行匹配 `class=` 与徽标会因二者不在同一行而全量误报。**

## Resources

- `references/conventions.md` — 完整结构约定：题号前缀、卡片 HTML 模板（`.qa-card`/`.qa-layer` 七层/场景七层）、导图节点模板、4 份聚合页字段名与 `ov-stat-num` 顺序、权威计数示例、导航/小屏/Prettier（§7–§7.2）。
- `scripts/validate_kb.py` — 可复用全量校验：SSOT check、**0b 标记**、**0c L1 聚合 UI 扫描**、**0d 页头难度自证**、overview 排序/类型、三权威源、红线（`data-page-node-id`）、**1f 内部编辑字眼**、**1g 横向溢出兜底**、**1h 列表缩进兜底**、**Mermaid prettier-ignore**、主题/小屏。
- `scripts/check_list_indent.js` — 列表 marker 缩进**实测**（CDP，零依赖）。两重判定：① `markerSpace < 1.2×li字号 − 0.5px`：`markerSpace` = 列表内容盒左边 − 边界容器内容盒左边（边界优先取卡片类 `.epq-card`/`.qa-card`/`details.map-card`，其次取最近有 padding 的块级祖先，**绝不退到 0**，否则 375px 假阳 / 1280px 假阴）；② **同容器内 `min(ol pl) < max(ul pl) − 0.5`** —— 有序列表比无序列表少缩进（给 `ul` 写 padding 漏了 `ol`）。`node check_list_indent.js`（全站 44 页 × {1280, 375}）、`--only <相对路径>`、`--viewport 375`、`--dump`（打印各分组样本）、`--out r.json`。任一判定命中即 exit 1。**注意**：本脚本的度量代码位于 `MEASURE` 模板字符串内，**其注释里禁止出现反引号**（会提前终止模板字符串，报 `SyntaxError: Unexpected identifier`）—— 本轮实测踩过。
- `scripts/probe_list_gate.py` — 1h 门禁的**正向验证**（注入缺陷 → 必须 FAIL）：`1` 删除兜底规则、`2` 兜底退化为裸选择器 `ul, ol { … }`；`--inject` 只注入不校验（便于分步执行，规避前台信号中断）。注入态始终由权威备份构造，还原由调用方命令负责。
- `scripts/check_mobile_overflow.js` — 移动端横向溢出**实测**（CDP + headless Chrome，Node 22 原生 WebSocket，零依赖）。静态审计只能发现风险，不能证明修好；本脚本在真实视口下量 `documentElement.scrollWidth - clientWidth` 与「内容越出卡片」的元素数。`node check_mobile_overflow.js`（内置 8 页 × 320/375/414）、`--path <html>`（单页）、或传 cfg.json。溢出即 exit 1，可直接作门禁。
- `scripts/ensure_mermaid_prettier_ignore.py` — 批量为缺失的 mermaid 节点补 `<!-- prettier-ignore -->`（格式化前可先跑）。
- `scripts/normalize_html_closers.py` — Prettier 后把 `</tag\\n>` 压回同行（保护 kb-count 锚点）。
- `scripts/check_html_format.py` — `npm run format:html:check` 稳态检查。
- `scripts/audit_l1_counts.py` — 只跑 L1 裸计数扫描（改聚合文案后可先跑这支）。
- `scripts/check_mind_mermaid.py` — 导图站不变式校验：每条 map-card（含 `C12.11~15 …` 聚合条目）是否都有对应 Mermaid 图节点；缺失 → exit 1。补这个盲区（`validate_kb` 只查 ID 集合，查不出图节点缺失）。
- `scripts/sync_new_card.py` — 新增卡片的 7 文件同步脚本骨架（参数化），含备份、断言、`data-page-node-id` 守卫；按需填充卡片 HTML 与计数增量。
- `scripts/check_index_badges.py` — 聚合 UI 徽标**结构**校验（零依赖，纯正则）：① `nav-overview-priority.html` 每条 `ov-item` 必须含 `.ov-badges` 包裹（漏包 → 页面上徽标间距时宽时窄）；② 根 `index.html` 不得出现顶格 `<a href="…">`（须与同级 li 同缩进）、不得有未闭合 `<span class="q-tags">`。`python3 check_index_badges.py [项目根]`，PASS → exit 0 / 有缺陷 → exit 1 / 定位失败 → exit 2。**项目根默认自动向上查找**（同时含 `AGENTS.md` 与 `index.html` 的最近祖先，兼容 `.agents` 软链调用）——**不要改回固定层级 `dirname`**，曾因层级写错静默指向 `.workbuddy/` 而报 `FileNotFoundError`。
- `scripts/probe_index_badge_gate.py` — 上条门禁的**正向验证**：用权威备份在 `tmp/` 沙箱构造缺陷版（**不写项目真实文件**，故无需还原）→ 必须 `exit=1` 且命中 29 处；再对当前树跑 → 必须 `exit=0`。双向任一不符即 exit 1，证明门禁非恒真且不误杀。
- `scripts/strip_page_node_id.py` — 红线兜底：清除全站 HTML 的 `data-page-node-id` 属性（预览服务注入污染时用）。`--check` 只读扫描（报告计数与命中文件）、`--fix` 回写；覆盖根 `index.html` + `java-architect-interview/*.html` + `java-architect-interview-mind/*.html`。三步归一：删属性 → 标签内空白归一 → 属性与 `>` 间去空格。**改完勿用预览确认**（会再次注入）。
- 仓库根：`npm run format:html` / `format:html:check`；规范正文见 `docs/format-shared.md` §4.2 / §10。