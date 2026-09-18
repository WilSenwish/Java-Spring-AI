# AGENTS.md — 项目常驻规则（Codex / Cursor / 所有支持 AGENTS.md 的 Agent 通用）

本文件是**精简版硬约束**。完整约定见 `.workbuddy/memory/MEMORY.md`（WorkBuddy 专用，其他工具可不读）。
详细格式规范见 `docs/`（README / format-shared / format-std-qa / format-special）。

## 1. 项目是什么

《Java 专家 · 架构师 · 高级开发 工程能力知识库》——**纯静态 HTML 站点**（GitHub Pages 发布），无后端、无构建步骤。

- `index.html`：站点总目录（聚合统计页，三权威源之一）
- `java-architect-interview/`：章节站。方法论页 `chapter-core-methodology.html`、工程化要点页 `chapter-engineering-practices.html`、生产踩坑页 `chapter-production-pitfalls.html`、`chapter-01~15-*`、`chapter-questions-eight-part.html`（核心原理）、`chapter-questions-scenario.html`（场景）、`nav-server-security-checkpoint.html`、`nav-overview-priority.html`（导航聚合页；前缀 nav- 表示非篇章题）
- `java-architect-interview-mind/`：导图站，21 个 `mind-*.html`（19 主链 + R2/R3 视角），与章节页互链
- 共享资源：`java-architect-interview/assets/design-system.css`、`java-architect-interview/assets/theme-init.js`、`java-architect-interview/assets/nav.js`（导图站相对路径引用同套文件）

**卡片编号**：`M##.##`（方法论，M01~M16 共 94 卡）/ `G##.##`（工程化，G01~G08 共 64 卡）/ `K##.##`（踩坑，K01~K08 共 64 卡）/ `C##.##`（篇章 249）/ `E##.##`（核心原理 73）/ `S##.##`（场景 73）。

## 2. 硬红线（违反即返工）

1. **禁止预览/打开任何 HTML 做可视化确认**。预览服务会持有文件并回写注入 `data-page-node-id` 属性（历史上单文件被注入 6517 处）。交付方式：**绝对路径 + 文字结论**。
2. **`data-page-node-id` 全站必须为 0**。改动后必须扫描确认（46 个 HTML 文件）。
3. **禁用词**：`面试`、`面试官`、`八股`。全站已清除，新增内容一律不得出现。
   术语映射：面试→知识点/技术沟通；面试题→知识点；八股→核心原理；层名「面试应用」→「工程表达」（`data-layer="application"` 英文值不动）。
4. **`docs/facts/` 只读**：下载的官方参考文档归档，不在任何修改范围内。
5. **同文件多处修改禁止并行编辑**（会静默丢更新）；须串行修改或整文件重写后重新校验。
6. **全站手机小屏样式强制优化**（违反即返工）：所有对用户可见的页面必须在 ≤768px（及 ≤480px 极小屏）下可读、可点、无横向撑破；共享样式以 `assets/design-system.css` 的 `MOBILE-MANDATORY` 段为准，页面内联桌面规则必须自带对应 `@media` 覆盖。细则见 `docs/format-shared.md` §8。交付仍遵守红线 1（禁止预览注入），用绝对路径 + 文字结论说明适配点。
   - **列表缩进兜底不得删改**：共享 CSS 的零特异度 `:where(ul, ol) { padding-inline-start: 1.25rem }` 必须保留，且**不得退化为裸选择器 `ul, ol { … }`**。原因是顶部 reset（`* { margin: 0; padding: 0 }`）把 `ul`/`ol` 的 UA 默认缩进一并归零，凡未匹配到类规则的列表 `padding-left` 即为 0，而 `list-style-position: outside` 的圆点/数字绘制在内容盒之外 —— 桌面「列表无缩进、圆点贴卡片边缘」，小屏直接越出卡片（实测核心原理页 20 处、安全检查页 1 处）。校验：`validate_kb` 项 **1h** + `scripts/check_list_indent.js`。
7. **主题 / 暗黑模式**：新页须在 CSS 前引入 `theme-init.js`；换肤只改 CSS 变量；切换器与回顶/去底由 `theme-init.js` 注入。细则见 `docs/format-shared.md` §9。
8. **顶/底章节导航**：仅根 `index.html` 与章节站 `index.html` 无导航；其余页顶栏为 `body` 首块（`.site-page-nav--top`），底栏在脚本前（`.site-page-nav--bottom`），顶底同文、壳层间距对称。细则见 `format-shared.md` §4.2。
9. **HTML Prettier + Mermaid**：用户可见 HTML 用 `npm run format:html`；每个 `<div class="mermaid">` 上一行必须 `<!-- prettier-ignore -->`。细则见 `format-shared.md` §10。

## 3. 权威计数（单一真源驱动）

**真源**：`docs/kb-counts.json`（唯一写源，勿在别处手改数字）。
**改数唯一入口**：`python3 .workbuddy/skills/java-kb-expand/scripts/sync_counts.py bump 键=增量`
（例：`bump methodology=+1 total=+1`；随后自动写回全部计数位并复核。只读核对用 `check`。）
**计数点标记**：每个展示题量/卡量须带 `data-kb-pos="Pxx"` + `data-kb-count`（全局键或 `struct.*`）；`<title>` 用属性打标。**禁止** `kb-count-local`。分级见 `conventions.md` §5.1.4；`validate_kb` 扫描聚合 UI 裸数字。

统计口径（易错）：跨大篇章/聚合分组**只算「篇章 + 核心原理 + 场景」**（= `total`）；方法论 / 工程化 / 踩坑为**专篇键**，**不设全站合计**（已废除 `sum_all`）。概览页、安全卡页的题量口径亦为 `total`，不含 M/G/K。
全文件扫到 C+E+S+M+G+K 张卡属正常，勿把分域加总当成对外「全站合计」。卡片优先级**双编码**：`data-priority="p*"` + 可见徽标
`<span class="priority priority-p*">P*</span>`，改级两处同步。
分组/篇章可见计数（`dir-count` / `dir-group-count` / `group-count` / mind `card-foot`）须与实际卡片数一致；细则见 `docs/` 与 `.workbuddy/skills/java-kb-expand/references/conventions.md` §5。

<!-- COUNTS:BEGIN 由 scripts/sync_counts.py render 生成，勿手改 -->
- 题目总量 **398** = 篇章 251 + 核心原理 73 + 场景 74
- 优先级 **P0=94 / P1=246 / P2=58**（求和 = 398）
- 难度 **专家 46 / 架构师 191 / 高级开发 161**（求和 = 398；仅覆盖 C/E/S，M/G/K 不分级）
- 方法论 **127 卡**（M01~M16，专篇键 methodology；**不分难度等级**）
- 工程化 **65 卡**（G01~G08，专篇键 engineering；**不分难度等级**）
- 生产踩坑 **64 卡**（K01~K08，专篇键 pitfalls；**不分难度等级**）
- 口径（程序约束）：题目总量 total=篇章+核心原理+场景；M/G/K 为专篇键，不进 total；结构计数见 struct；**禁止 kb-count-local；禁止页面用自然语言声明口径**
- 方法论细分：带优先级 75/127（2026-09-16 起 M/G/K 不设难度计数）

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
| P31 | `java-architect-interview/chapter-questions-eight-part.html` | 核心原理页 title 散文题数 |
| P32 | `java-architect-interview/chapter-questions-eight-part.html` | 核心原理页 h1 题数 |
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
| P399 | `index.html` | 根 index 方法论 M13 组卡数 |
| P400 | `index.html` | 根 index 方法论 M14 组卡数 |
| P401 | `index.html` | 根 index 方法论 M15 组卡数 |
| P402 | `index.html` | 根 index 方法论 M16 组卡数 |
<!-- COUNTS:END -->
## 4. 常用操作约定

- **改 HTML 前先备份**到 `tmp/`（已 gitignore）；脚本也写在这里，用绝对路径、不依赖记忆数字。
- **统计/校验脚本**：先写入 `tmp/` 再执行（Bash 内联长脚本可能被安全策略拦截）。
- **Python**：`/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3`。
- **Bash 内置 `grep` 受 `_zshz` 干扰会误返空**，交叉验证请用其他方式。
- 改题库后必须跑全量校验：`.workbuddy/skills/java-kb-expand/scripts/validate_kb.py`（校验红线 + 三权威源一致性）。

## 5. 可用 Skill

- **`java-kb-expand`**（`.agents/skills/java-kb-expand/`，软链到 `.workbuddy/skills/java-kb-expand/`）：用户提供外部链接并要求入库时使用。固化「抓取链接 → 归属判定与覆盖度核查 → 确认式给候选 → 带备份脚本全量同步 → 全量校验」五步流程。

> 约定：**链接入库必须走确认式**——先给覆盖度核查表与 OPT 候选，用户确认后才改文件。
