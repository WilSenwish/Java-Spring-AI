# Java-Spring-AI

> **Java 架构师级工程能力知识库** · 纯静态 HTML 站 · GitHub Pages 发布 · 单一真源驱动全站计数

仓库地址：<https://github.com/WilSenwish/Java-Spring-AI> · 部署形态：GitHub Pages（无后端、无构建步骤）

---

## 目录结构（4 子站 + 2 索引 + 工具链 + rk/ 随笔）

```
Java-Spring-AI/
├── index.html                              # 根索引（全站聚合，三权威源之一）
├── java-architect-interview/              # ① 章节主站 · 26 HTML
│   ├── chapter-01~15-*.html                # 15 篇章（C）
│   ├── chapter-core-methodology.html       #   方法论（M）
│   ├── chapter-engineering-practices.html  #   工程化（G）
│   ├── chapter-production-pitfalls.html    #   生产踩坑（K）
│   ├── chapter-questions-eight-part.html   #   核心原理（E）
│   ├── chapter-questions-scenario.html     #   场景题（S）
│   ├── chapter-question-ai-engineering-deep.html  # AI 工程纵深（A）
│   ├── chapter-questions-domain.html       #   垂直领域（D）
│   ├── nav-overview-priority.html          #   优先级×难度×类型大盘
│   ├── nav-overview-quick-list.html        #   知识点速查清单
│   ├── nav-server-security-checkpoint.html #   服务端安全检查点
│   ├── assets/                             #   design-system.css · nav.js · theme-init.js
│   ├── shared/                             #   fonts / js（按需）
│   └── index.html                          # 章节索引
├── java-design-patterns-principles/       # ② 设计原则 & 超越 GoF 23
├── Software-Engineering-Laws-Theories-Principles-and-Patterns/ # ③ 软件工程 定律 / 理论 / 原则 / 模式 索引
├── Software-Engineering-Core-Philosophical-Principles-and-Methodologies/  # ④ 软件工程「道—法—术—器—势」核心哲学原理
├── rk/                                     # 两篇随笔（高项 / 系规），见 rk/README.md
├── .workbuddy/skills/java-kb-expand/       # 工具链 · java-kb-expand Skill
│   └── scripts/
│       ├── sync_counts.py     # 权威计数同步（改数唯一入口：bump / check / apply）
│       ├── validate_kb.py     # 全量校验（红线 / SSOT / 计数覆盖 / 落位 / 结构 …）
│       └── audit_*.py / probe_*.py / scan_*.py   # 辅助审计与门禁脚本
├── docs/
│   ├── kb-counts.json         # 单一真源（counts + struct，驱动全站 299 个计数位）
│   ├── facts/                 # 官方参考文档归档（只读）
│   ├── format-shared/special/std-qa.md  # 内容格式规范
│   └── README.md
├── .nojekyll                  # GitHub Pages 防 Liquid 误伤 Spring AI 模板占位符
└── AGENTS.md                  # 项目常驻硬约束（红线 / 禁用词 / 工具链约定）
```

---

## 题库速览（2026-09-21 · `docs/kb-counts.json` 真源）

### 对外总量（C + A + E + S + D = `total`）

| 域 | 编号 | 数量 |
|---|---|---|
| 篇章 | `C01.01 ~ C15.xx` | 252 |
| AI 工程纵深 | `A01.01 ~ Axx.xx` | 74 |
| 核心原理 | `E01.01 ~ Exx.xx` | 74 |
| 场景题 | `S01.01 ~ Sxx.xx` | 74 |
| 垂直领域 | `D01.01 ~ Dxx.xx` | 72 |
| **合计** | | **546** |

> **口径说明**：方法论 / 工程化 / 踩坑为**专篇卡**，独立计数、不进 `total`。真源：`docs/kb-counts.json`（改数走 `sync_counts.py bump`）。

### 专篇卡

| 域 | 编号 | 数量 | 组数 |
|---|---|---|---|
| 方法论 | `M01.01 ~ M16.xx` | 145 | 16 |
| 工程化要点 | `G01.01 ~ G08.xx` | 65 | 8 |
| 生产踩坑 | `K01.01 ~ K08.xx` | 65 | 8 |

### 优先级 × 难度（求和 = `total`）

| 优先级 | 题数 | | 难度 | 题数 |
|---|---|---|---|---|
| P0 | 124 | | 专家 | 65 |
| P1 | 337 | | 架构 | 260 |
| P2 | 85 | | 高级 | 221 |

---

## 快速入口

| 入口 | URL | 说明 |
|---|---|---|
| 根索引（全站） | `index.html` | 聚合所有子站，三权威源之一 |
| 章节索引 | `java-architect-interview/index.html` | 15 篇章 + 方法论 + 工程化 + 踩坑 + 核心原理 + 场景 |
| 优先级聚合 | `java-architect-interview/nav-overview-priority.html` | P0 → P1 → P2 三级分组，内按难度 / 类型再拆 |
| 安全检查点 | `java-architect-interview/nav-server-security-checkpoint.html` | 服务端开发安全速查 |
| 方法论 | `java-architect-interview/chapter-core-methodology.html` | 道法术势十六组（145 卡） |
| 工程化要点 | `java-architect-interview/chapter-engineering-practices.html` | 8 组工程化实践（65 卡） |
| 生产踩坑 | `java-architect-interview/chapter-production-pitfalls.html` | 8 组真实故障复盘（65 卡） |
| 设计原则 & GoF 23 | `java-design-patterns-principles/` | 设计原则 + 超越 GoF 23 |
| 软件定律 / 理论 / 原则 / 模式 | `Software-Engineering-Laws-Theories-Principles-and-Patterns/` | 24 条 + 7 类 + 13 类 + 6 类索引 |
| 软件工程「道法术器势」| `Software-Engineering-Core-Philosophical-Principles-and-Methodologies/` | 核心哲学原理完整篇 |

---

## 技术栈

- **纯静态 HTML** · 无后端 · 无构建步骤 · 直接由 GitHub Pages 渲染
- **共享样式系统**：`java-architect-interview/assets/design-system.css`（章节站 / 各随笔站共享）
- **Mermaid 可视化**：章节页内嵌 Mermaid 渲染方法论地图、领域关系图等
- **主题与字体**：`theme-init.js`（深色/浅色切换）、JetBrainsMono + WorkSans
- **GitHub Pages 专用**：`.nojekyll` 防止 Liquid 解析 Spring AI 模板占位符（`{{it}}` 等）

---

## 单一真源与工具链

全站数字**唯一写源**：`docs/kb-counts.json`，包含 `counts`（全局总量）与 `struct`（每章节/卡片位的精确计数）。所有 299 个计数位（以 `data-kb-pos="P01~P398"` 标记）均由它驱动。

### 三条硬约束（详见 `AGENTS.md`）

1. **禁止预览 HTML**：预览服务会注入 `data-page-node-id` 属性，单文件曾被注入 6517 处
2. **`data-page-node-id` 全站必须为 0**（改后必须扫描）
3. **禁用词**：面试 / 面试官 / 八股；术语映射为「知识点 / 技术沟通 / 核心原理」

### 关键脚本

| 脚本 | 作用 |
|---|---|
| `.workbuddy/skills/java-kb-expand/scripts/sync_counts.py` | 改数唯一入口：`python3 sync_counts.py bump 键=增量`，自动写回全部计数位并复核 |
| `.workbuddy/skills/java-kb-expand/scripts/validate_kb.py` | 全量校验：红线 / SSOT / 计数覆盖 / 落位 / 结构 / overview 排序 … |
| `.workbuddy/skills/java-kb-expand/` | Skill：`java-kb-expand`，固化「抓取外部链接 → 归属判定 → 用户确认 → 7 文件同步 → 全量校验」五步入库流程 |

### 常规工作流

```bash
# 全量校验（改前改后都跑）
python3 .workbuddy/skills/java-kb-expand/scripts/validate_kb.py

# 新增一张卡后改计数（示例：C06.15 新增，属篇章，全局 total +1、chapters +1）
python3 .workbuddy/skills/java-kb-expand/scripts/sync_counts.py bump \
  total=+1 chapters=+1 struct.chap.idx.c06.n=+1

# 入库外部链接（豆包/知乎/技术博客等）——走 Skill 固化流程
# 必须经过"覆盖度核查 → OPT 候选 → 用户确认"三步，禁止直接写
```

---

## rk/ 随笔

`rk/` 目录含两篇独立随笔（高项 / 系规），与知识库主站无强关联。自描述见 [rk/README.md](rk/README.md)。

---

## 更新频率与维护

- 计数真源 `docs/kb-counts.json` 最近更新：**2026-09-21**
- 每次入库新卡 / 调整分组结构后，必须同步 `kb-counts.json` 并跑 `validate_kb.py`
- 红线 `data-page-node-id=0` 禁止任何预览，任何改动后须全局扫描确认
