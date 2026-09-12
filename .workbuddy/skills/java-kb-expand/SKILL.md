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

- **章节站** `java-architect-interview/`：15 个编号篇章页 `chapter-01~15-*.html` + 方法论页 `chapter-core-methodology.html`（M 前缀）+ 安全卡 `chapter-server-security-checkpoint.html` + 核心原理页 `chapter-questions-eight-part.html`（E 前缀）+ 场景页 `chapter-questions-scenario.html`（S 前缀）+ 章节导航 `index.html`。
- **导图站** `java-architect-interview-mind/`：对应 `mind-01~15-*.html` + `mind-core-methodology.html` + `mind-server-security-checkpoint.html` + 导图导航 `index.html`（17 个导图页，线性链顺序见 `references/conventions.md` §7）。
- **项目根** `Java Spring AI/index.html`：全部题目的扁平全量快照（每题一个 `q-item` li，带难度 + `priority-pX` 徽标）。

题号前缀：方法论页（`chapter-core-methodology.html`）用 **M**，`chapter-01~15` 用 **C**，`E` 核心原理、`S` 场景。卡片三级目录为 `页面篇章 / 分组 / 题号`。

聚合统计页共 **4 份**，任何题目数/优先级的增删改都必须联动（详见 `references/conventions.md` §4）：① 项目根 `index.html`；② `java-architect-interview/index.html`；③ `java-architect-interview-mind/index.html`（题量表达式 `N篇章+N核心原理+N场景`）；④ `chapter-overview-priority.html`（`ov-stat-num` + 9 子组标题，按**优先级×难度**组织）。

**绝对红线：**
1. **禁止用 `present_files` 预览任何 HTML**（含在预览面板点击链接）。实测预览服务会持有文件并在外部变更时重新序列化、注入 `data-page-node-id` 属性。交付方式只有「绝对路径 + 文字结论」。
2. **禁止重复**：先核查覆盖度，不得新增与现有卡片/场景题重复的题。同源重复内容应补入现有卡（不新增计数）或不入库。
3. **P3 优先级已废除**：`data-priority` 仅 P0/P1/P2 三级。
4. 共享样式集中在 `assets/design-system.css`，优先改共享 CSS，不逐卡内联。

权威计数口径（以 `ov-stat-num` 与根 index 全量徽标为权威三源，三者须相等）：
- 总量 = 篇章(深度Q&A) + 核心原理 + 场景
- 优先级 P0 / P1 / P2（求和 = 总量）
- 难度三级：专家级 / 架构级 / 高级开发（求和 = 总量）

<!-- COUNTS:BEGIN 由 scripts/sync_counts.py render 生成，勿手改 -->
- 题目总量 **365** = 篇章 229 + 核心原理 64 + 场景 72
- 优先级 **P0=92 / P1=217 / P2=56**（求和 = 365）
- 难度 **专家 46 / 架构 178 / 高级开发 141**（求和 = 365）
- 方法论 **75 卡**（M01~M11），不计入 365；全站合计 **440**
- 方法论细分：带优先级 31/75；难度 专家 23 / 架构 49 / 高级开发 3

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
1. **先备份**所有待改文件到 `java-architect-interview/tmp/`（如 `java-architect-interview/tmp/kb_<task>_backup/`）。
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
1. 跑 `scripts/validate_kb.py`（或等效脚本）核对：三权威源一致、各文件 `data-page-node-id` 全 0、无 `</spa`（缺 n）标签截断、新卡双编码（`data-priority` + 可见徽标）一致、新卡在 overview/根 index/mind 均落位。
2. **补层轮次也要做"计数体检"（2026-09-03 新增，高收益）**：即使本轮不改计数，也应顺手全量核对 4 份聚合页，因为历史轮次常留下孤儿数字。已实测抓出 3 处遗留错误，务必覆盖三类隐藏位：
   - **① `stat-number` 全部字段**（不只看"全站 N 题"）。根 index 的「**题目总数**」曾长期停留在 **413**（＝旧合计 339+74 的值被误填），正确值应＝题数 345；而「合计」= 题数 + 方法论卡片 = 420 本身没错。**题目总数 ≠ 合计**，改题数时两个都要动。
   - **② 散文式数字**（不在任何统计字段里，正则抓 `stat-*` 会漏）。章节 index 方法论卡的 `card-desc`「…15 篇 **219** 道…」与 `card-footer`「5 主题 · 74 方法论卡片 · 28 技术图表 · 15 篇 **218** 道」，两处都应为 220。校验技巧：`re.findall(r'(\d+)\s*道', t)` + 上下文打印，或直接断言页面内不存在 `219`/`218` 等旧值。
   - **③ mind 页 summary 编号 ↔ 章节页 qa-card id 逐一对齐**。`mind-08` 曾把 **C08.08（过期策略）与 C08.09（布隆过滤器）整对互换**，与章节页相反，且其正文交叉引用（E12.03「与 C08.01/C08.0X 印证」、E12.04「缓存侧印证 C08.0X」）跟着一起错。发现后应按**章节页为准**纠偏 summary + 交叉引用。校验脚本：分别提取两边编号→标题映射后比对。
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
| `chapter-overview-priority.html` | 新增 ov-item；`ov-stat-num` 共 **11 个**字段须同步 +N：**总量 / P0 / P1 / P2 / 专家级 / 架构级 / 高级开发 / 方法论 / 章节题 / 核心原理 / 场景题**（第 8 项「方法论 75」易漏，务必逐项核对）；对应子组标题（优先级×难度 9 宫格）+N |
| `Java Spring AI/index.html`（根） | 类型计数 / 合计（题数+方法论卡片）/ 全站 / dir-count +N；新增 q-item li |
| `java-architect-interview/index.html` | stat-number +N；全站 +N；章节 card-footer +N（**不枚举单题 ID**） |
| `mind-xx-*.html` | 主干范围 `C10.01–C10.N` 扩尾；插 map-card（summary/body/tags）；meta |
| `mind/index.html` | 题量表达式 `N+N+N` 同步 |

## 坑位速查（高频踩坑）

- **Edit 大数字竞态**：overview 的 `ov-stat-num` 用 `Edit` 报成功却未落盘，改用 Python 脚本替换。
- **章节导航页不枚举单题 ID**：`java-architect-interview/index.html` 只列章节卡片与统计，不含 `Cxx.xx`/`Sxx.xx` 条目——校验时"落位=False"属预期。
- **9 子组标题按 优先级×难度**（P0/P1/P2 各含 专家级/架构级/高级开发），不是难度×类型；同步前先算真实 9 宫格再对齐「子组标题 + ov-stat-num」两处。
- **overview `ov-stat-num` 共 11 项全要改**：总量/P0/P1/P2/专家级/架构级/高级开发/方法论/章节题/核心原理/场景题。最易漏的是「章节题」（篇章数）与「方法论」（第 8 项，取值见下方 COUNTS 块），漏改会导致 overview 与根 index、章节 index 的计数不一致。
- **根 index 合计 ≠ 题数**：合计 = 题数 + 方法论卡片数（取值见下方 COUNTS 块的「全站合计」），加题时题数与合计各 +1。
- **mind 页 `1+15+1` 计数与题量无关**，勿动；只改题量表达式 `N+N+N`。
- **`</spa` 误判**：截断检测用负向前瞻排除合法 `</span>`（正则 `</spa(?!n>)`）。
- **路径双层**：`Java Spring AI/index.html` 是项目根全量快照，与子目录 `java-architect-interview/index.html` 是不同文件，全局核对须覆盖根那一层。
- **Bash 内置 `grep` 受 `_zshz` 干扰**：交叉验证用 `Grep` 工具或 `git grep`。
- **校验提取正则必须覆盖新编号空间（2026-09-04 实测）**：升层重编号后若用旧模式（如 `M0[1-7]\.\d{2}`）提取 after 集合做多重集断言，会"看不见" M08+ 的新号而误报不一致（替换其实已成功）；after 一律用宽模式 `M\d{2}\.\d{2}`。

## Resources

- `references/conventions.md` — 完整结构约定：题号前缀、卡片 HTML 模板（`.qa-card`/`.qa-layer` 七层/场景七层）、导图节点模板、4 份聚合页字段名与 `ov-stat-num` 顺序、权威计数示例。
- `scripts/validate_kb.py` — 可复用全量校验脚本骨架（参数化 BASE 路径），核对三权威源一致性、`data-page-node-id`=0、标签截断、双编码落位。复制后按本轮新增的题号/计数填空即可。
- `scripts/sync_new_card.py` — 新增卡片的 7 文件同步脚本骨架（参数化），含备份、断言、`data-page-node-id` 守卫；按需填充卡片 HTML 与计数增量。
