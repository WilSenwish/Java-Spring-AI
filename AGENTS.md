# AGENTS.md — 项目常驻规则（Codex / Cursor / 所有支持 AGENTS.md 的 Agent 通用）

本文件是**精简版硬约束**。完整约定见 `.workbuddy/memory/MEMORY.md`（WorkBuddy 专用，其他工具可不读）。
详细格式规范见 `java-architect-interview/docs/`（README / format-shared / format-std-qa / format-special）。

## 1. 项目是什么

《Java 专家 · 架构师 · 高级开发 工程能力知识库》——**纯静态 HTML 站点**（GitHub Pages 发布），无后端、无构建步骤。

- `index.html`：站点总目录（聚合统计页，三权威源之一）
- `java-architect-interview/`：章节站。方法论页 `chapter-core-methodology.html`、工程化要点页 `chapter-engineering-practices.html`、`chapter-01~15-*`、`chapter-questions-eight-part.html`（核心原理）、`chapter-questions-scenario.html`（场景）、`chapter-server-security-checkpoint.html`、`chapter-overview-priority.html`（聚合页）
- `java-architect-interview-mind/`：导图站，18 个 `mind-*.html`，与章节页一一对应互链
- 共享资源：`assets/design-system.css`、`shared/js/nav.js`

**卡片编号**：`M##.##`（方法论，M01~M12 共 91 卡）/ `G##.##`（工程化，G01~G08 共 24 卡）/ `C##.##`（篇章 229）/ `E##.##`（核心原理 64）/ `S##.##`（场景 72）。

## 2. 硬红线（违反即返工）

1. **禁止预览/打开任何 HTML 做可视化确认**。预览服务会持有文件并回写注入 `data-page-node-id` 属性（历史上单文件被注入 6517 处）。交付方式：**绝对路径 + 文字结论**。
2. **`data-page-node-id` 全站必须为 0**。改动后必须扫描确认（42 个 HTML 文件）。
3. **禁用词**：`面试`、`面试官`、`八股`。全站已清除，新增内容一律不得出现。
   术语映射：面试→知识点/技术沟通；面试题→知识点；八股→核心原理；层名「面试应用」→「工程表达」（`data-layer="application"` 英文值不动）。
4. **`java-architect-interview/docs/facts/` 只读**：下载的官方参考文档归档，不在任何修改范围内。
5. **同文件多处修改禁止并行编辑**（会静默丢更新）；须串行修改或整文件重写后重新校验。

## 3. 权威计数（单一真源驱动）

**真源**：`java-architect-interview/docs/kb-counts.json`（唯一写源，勿在别处手改数字）。
**改数唯一入口**：`python3 .workbuddy/skills/java-kb-expand/scripts/sync_counts.py bump 键=增量`
（例：`bump methodology=+1 total=+1`；随后自动写回全部计数位并复核。只读核对用 `check`。）

统计口径（易错）：题目统计**只算「篇章 + 核心原理 + 场景」三页**；方法论页、工程化要点页、概览页、安全卡页**不计入**。
全文件扫描得 480（365+91+24）属正常，勿误判。卡片优先级**双编码**：`data-priority="p*"` + 可见徽标
`<span class="priority priority-p*">P*</span>`，改级两处同步。

<!-- COUNTS:BEGIN 由 scripts/sync_counts.py render 生成，勿手改 -->
- 题目总量 **365** = 篇章 229 + 核心原理 64 + 场景 72
- 优先级 **P0=92 / P1=217 / P2=56**（求和 = 365）
- 难度 **专家 46 / 架构 178 / 高级开发 141**（求和 = 365）
- 方法论 **91 卡**（M01~M12），不计入 365
- 工程化 **24 卡**（G01~G08），不计入 365；全站合计 **480** = 题目 + 方法论 + 工程化
- 方法论细分：带优先级 45/91；难度 专家 26 / 架构 61 / 高级开发 4

计数位（改数须全部同步，由 sync_counts.py check 自动核查）：

| 编号 | 载体 | 说明 |
|---|---|---|
| P01 | `index.html` | 根 index 方法论统计卡 |
| P02 | `index.html` | 根 index 方法论分组题数 |
| P03 | `java-architect-interview/index.html` | 章节 index 方法论统计卡 |
| P04 | `java-architect-interview/index.html` | 章节 index card-footer 方法论数 |
| P05 | `java-architect-interview/index.html` | 章节 index card-footer 篇章题数 |
| P06 | `java-architect-interview/chapter-core-methodology.html` | 方法论页页头 |
| P07 | `java-architect-interview/chapter-overview-priority.html` | overview ov-stat-num 11 项（顺序见 ov_stat_order） |
| P08 | `java-architect-interview-mind/index.html` | mind index idx-meta 第 5 块 |
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
| P25 | `java-architect-interview/chapter-engineering-practices.html` | 工程化页页头 |
<!-- COUNTS:END -->
## 4. 常用操作约定

- **改 HTML 前先备份**到 `java-architect-interview/tmp/`（已 gitignore）；脚本也写在这里，用绝对路径、不依赖记忆数字。
- **统计/校验脚本**：先写入 `tmp/` 再执行（Bash 内联长脚本可能被安全策略拦截）。
- **Python**：`/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3`。
- **Bash 内置 `grep` 受 `_zshz` 干扰会误返空**，交叉验证请用其他方式。
- 改题库后必须跑全量校验：`.workbuddy/skills/java-kb-expand/scripts/validate_kb.py`（校验红线 + 三权威源一致性）。

## 5. 可用 Skill

- **`java-kb-expand`**（`.agents/skills/java-kb-expand/`，软链到 `.workbuddy/skills/java-kb-expand/`）：用户提供外部链接并要求入库时使用。固化「抓取链接 → 归属判定与覆盖度核查 → 确认式给候选 → 带备份脚本全量同步 → 全量校验」五步流程。

> 约定：**链接入库必须走确认式**——先给覆盖度核查表与 OPT 候选，用户确认后才改文件。
