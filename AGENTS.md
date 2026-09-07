# AGENTS.md — 项目常驻规则（Codex / Cursor / 所有支持 AGENTS.md 的 Agent 通用）

本文件是**精简版硬约束**。完整约定见 `.workbuddy/memory/MEMORY.md`（WorkBuddy 专用，其他工具可不读）。
详细格式规范见 `java-architect-interview/docs/`（README / format-shared / format-std-qa / format-special）。

## 1. 项目是什么

《Java 专家 · 架构师 · 高级开发 工程能力知识库》——**纯静态 HTML 站点**（GitHub Pages 发布），无后端、无构建步骤。

- `index.html`：站点总目录（聚合统计页，三权威源之一）
- `java-architect-interview/`：章节站。方法论页 `chapter-core-methodology.html`、`chapter-01~15-*`、`chapter-questions-eight-part.html`（核心原理）、`chapter-questions-scenario.html`（场景）、`chapter-server-security-checkpoint.html`、`chapter-overview-priority.html`（聚合页）
- `java-architect-interview-mind/`：导图站，17 个 `mind-*.html`，与章节页一一对应互链
- 共享资源：`assets/design-system.css`、`shared/js/nav.js`

**卡片编号**：`M##.##`（方法论，M01~M11 共 75 卡）/ `C##.##`（篇章 220）/ `E##.##`（核心原理 58）/ `S##.##`（场景 67）。

## 2. 硬红线（违反即返工）

1. **禁止预览/打开任何 HTML 做可视化确认**。预览服务会持有文件并回写注入 `data-page-node-id` 属性（历史上单文件被注入 6517 处）。交付方式：**绝对路径 + 文字结论**。
2. **`data-page-node-id` 全站必须为 0**。改动后必须扫描确认（42 个 HTML 文件）。
3. **禁用词**：`面试`、`面试官`、`八股`。全站已清除，新增内容一律不得出现。
   术语映射：面试→知识点/技术沟通；面试题→知识点；八股→核心原理；层名「面试应用」→「工程表达」（`data-layer="application"` 英文值不动）。
4. **`java-architect-interview/docs/facts/` 只读**：下载的官方参考文档归档，不在任何修改范围内。
5. **同文件多处修改禁止并行编辑**（会静默丢更新）；须串行修改或整文件重写后重新校验。

## 3. 权威计数（改动前必读，改后必同步）

- 题目总量 **345 = 篇章 220 + 核心原理 58 + 场景 67**
- 优先级 **P0=90 / P1=195 / P2=60**（三组求和 = 345）
- 难度 **专家 44 / 架构 160 / 高级开发 141**（三组求和 = 345）
- 方法论 **75 卡**（M01~M11），**不计入 345 口径**；全站合计 **420 = 345 + 75**
- 卡片优先级**双编码**：`data-priority="p*"` 属性 + 可见徽标 `<span class="priority priority-p*">P*</span>`，改级两处同步
- 统计口径：题目统计**只算「篇章 + 核心原理 + 场景」三页**；方法论页、概览页、安全卡页**不计入**。全文件扫描得 420 属正常，勿误判

**方法论 75 计数位（改数须 10 处同步）**：① 根 index stat「75 方法论」；② 根 index 方法论分组 `dir-count 75 题`；③ 章节 index `stat-number 75`；④ 章节 index card-footer「5 主题 · 75 方法论卡片 · 28 技术图表 · 15 篇 220 道」；⑤ methodology 页头「75 方法论卡片」；⑥ `chapter-overview-priority.html` 的 `ov-stat-num`（共 11 项，方法论为末项）；⑦ mind index `idx-meta` 第 5 块；⑧ `mind-core-methodology.html` 尾注「方法论计 75 卡」；⑨ `docs/` 三份 md（README / format-shared / format-special）；⑩ 技能脚本 `validate_kb.py`、`sync_new_card.py` 的 `methodology: 75`。

## 4. 常用操作约定

- **改 HTML 前先备份**到 `java-architect-interview/tmp/`（已 gitignore）；脚本也写在这里，用绝对路径、不依赖记忆数字。
- **统计/校验脚本**：先写入 `tmp/` 再执行（Bash 内联长脚本可能被安全策略拦截）。
- **Python**：`/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3`。
- **Bash 内置 `grep` 受 `_zshz` 干扰会误返空**，交叉验证请用其他方式。
- 改题库后必须跑全量校验：`.workbuddy/skills/java-kb-expand/scripts/validate_kb.py`（校验红线 + 三权威源一致性）。

## 5. 可用 Skill

- **`java-kb-expand`**（`.agents/skills/java-kb-expand/`，软链到 `.workbuddy/skills/java-kb-expand/`）：用户提供外部链接并要求入库时使用。固化「抓取链接 → 归属判定与覆盖度核查 → 确认式给候选 → 带备份脚本全量同步 → 全量校验」五步流程。

> 约定：**链接入库必须走确认式**——先给覆盖度核查表与 OPT 候选，用户确认后才改文件。
