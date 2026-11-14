# Arch Codex

> **架构师知识法典** · 纯静态 HTML 站 · GitHub Pages 发布 · 单一真源驱动全站计数 · 11 大编号体系 · 686 精编卡片

仓库地址：<https://github.com/WilSenwish/arch-codex> · Pages 站点：<https://wilsenwish.github.io/arch-codex/> · 部署形态：GitHub Pages（无后端、无构建步骤）

---

## 目录结构（1 个主站 + 3 个 KB 子站 + xinchuang/ 独立站点 + 2 索引 + 工具链 + rk/ 随笔）

```
arch-codex/
├── index.html                              # 根索引（全站聚合，三权威源之一）
├── interview.html                          # 独立能力索引页
├── core/                                   # ① 章节主站 · 34 HTML
│   ├── chapter-01~15-*.html                # 15 篇章（C）
│   ├── chapter-16-ai-python-stack.html      #   AI Python 技术栈（C + A）
│   ├── chapter-17-testing-system.html       #   测试体系（C）
│   ├── chapter-18-multilang-runtime.html    #   多语言运行时（C）
│   ├── chapter-core-methodology.html        #   方法论（M）· 道法术器势六层十六组 205 卡
│   ├── chapter-core-methodology-ai.html     #   AI 应用开发方法论（L）· 41 卡
│   ├── chapter-engineering-practices.html   #   工程化要点（G）· 11 组 88 卡
│   ├── chapter-production-pitfalls.html     #   生产踩坑（K）· 10 组 82 卡
│   ├── chapter-hybrid-deployment.html       #   混合部署（H）· 8 卡
│   ├── chapter-questions-eight-part.html    #   核心原理（E）· 74 卡
│   ├── chapter-questions-scenario.html      #   场景题（S）· 74 卡
│   ├── chapter-question-ai-engineering-deep.html  # AI 工程纵深（A）· 112 卡
│   ├── chapter-questions-domain.html        #   垂直领域（D）· 90 卡
│   ├── nav-overview-priority.html           #   优先级×难度×类型大盘
│   ├── nav-knowledge-quick-list.html        #   知识点速查清单
│   ├── nav-server-security-checkpoint.html  #   服务端安全检查点
│   ├── nav-overview-capability-matrix.html  #   能力矩阵索引导航
│   ├── nav-overview-lifecycle.html          #   生产生命周期检索视图导航
│   ├── nav-overview-ai-component-stack.html #   AI 应用组件分层检索视图导航
│   ├── assets/                              #   design-system.css · nav.js · theme-init.js
│   └── index.html                           # 章节索引
├── java-design-patterns-principles/        # ② 设计原则 & 超越 GoF 23
├── Software-Engineering-Laws-Theories-Principles-and-Patterns/  # ③ 软件工程 定律/理论/原则/模式
├── Software-Engineering-Core-Philosophical-Principles-and-Methodologies/  # ④ 软件工程「道—法—术—器—势」
├── rk/                                      # 两篇随笔（高项/系规），见 rk/README.md
├── xinchuang/                               # ⑤ 信创独立站点：12 篇 md 源文档 + 自包含 HTML 站
├── .workbuddy/skills/java-kb-expand/        # 工具链 · java-kb-expand Skill
│   └── scripts/
│       ├── sync_counts.py     # 权威计数同步（改数唯一入口）
│       ├── validate_kb.py      # 全量校验（红线 / SSOT / 计数覆盖 / 落位 / 结构 …）
│       └── audit_*.py / probe_*.py / scan_*.py   # 辅助审计与门禁脚本
├── docs/
│   ├── kb-counts.json         # 单一真源（counts + struct，驱动全站全部 data-kb-pos 计数位）
│   ├── catppuccin-tokens.json # 配色唯一色源 SSOT
│   ├── shared/                # 全站共用 fonts / js（mermaid · echarts · d3 · three）
│   ├── facts/                 # 官方参考文档归档（只读）
│   ├── specs/                 # 内容格式规范
│   ├── shared/style/satellite-base.css  # ②③④ 三子站共用基础样式
│   ├── scripts/               # 站点构建/校验脚本
│   ├── search-index.json      # 静态搜索索引
│   └── README.md
├── .nojekyll                  # GitHub Pages 防 Liquid 误伤 Spring AI 模板占位符
└── AGENTS.md                  # 项目常驻硬约束
```

---

## 题库速览（2026-11-14 · `docs/kb-counts.json` 真源）

### 编号体系（11 大域）

| 编号 | 域 | 说明 |
|---|---|---|
| M | 核心方法论 | 道 M01–M02 / 法 M03–M07 / 术 M08–M15 / 势 M16 |
| L | AI 应用开发方法论 | AI 产品/架构/工程方法论专篇 |
| C | 技术栈 Q&A | 18 篇章深度 Q&A |
| A | AI 工程纵深 | AI 工程专题卡（与 C 合流成深度 Q&A 448 卡） |
| E | 核心原理 | 八分体原理速查 |
| S | 真实场景 | 生产场景题 |
| D | 垂直领域 | 金融/电商/物流/安全等领域题 |
| G | 工程化要点 | CI/CD/质量/效率工程化实践 |
| K | 生产踩坑 | 真实故障复盘 |
| H | 混合部署 | 多云/混合云部署模式 |
| SEC | 安全手册 | 服务端开发安全速查 |

### 对外总量（C + A + E + S + D = `total`）

| 域 | 编号 | 数量 |
|---|---|---|
| 篇章 | `C01.01 ~ C18.xx` | 336 |
| AI 工程纵深 | `A01.01 ~ Axx.xx` | 112 |
| 核心原理 | `E01.01 ~ Exx.xx` | 74 |
| 场景题 | `S01.01 ~ Sxx.xx` | 74 |
| 垂直领域 | `D01.01 ~ Dxx.xx` | 90 |
| **合计** | | **686** |

> **口径说明**：方法论 / AI 方法论 / 工程化 / 踩坑 / 混合部署为**专篇卡**，独立计数、不进 `total`。真源：`docs/kb-counts.json`（改数走 `sync_counts.py bump`）。

### 专篇卡

| 域 | 编号 | 数量 |
|---|---|---|
| 方法论 | `M01.01 ~ M16.xx` | 205 |
| AI 方法论 | `Lxx.xx` | 41 |
| 工程化要点 | `G01.01 ~ G13.xx` | 88 |
| 生产踩坑 | `K01.01 ~ K12.xx` | 82 |
| 混合部署 | `H01.01 ~ H02.xx` | 8 |

### 优先级 × 难度（求和 = `total`）

| 优先级 | 题数 | | 难度 | 题数 |
|---|---|---|---|---|
| P0 | 158 | | 专家 | 90 |
| P1 | 420 | | 架构 | 334 |
| P2 | 108 | | 高级 | 262 |

---

## 快速入口

| 入口 | URL | 说明 |
|---|---|---|
| 根索引（全站） | `index.html` | 主 KB 三级目录 + 独立专题站点入口，三权威源之一 |
| 章节索引 | `core/index.html` | 18 篇章 + 方法论 + AI 方法论 + 工程化 + 踩坑 + 核心原理 + 场景 + 垂直领域 |
| 优先级聚合 | `core/nav-overview-priority.html` | P0 → P1 → P2 三级分组，内按难度 / 类型再拆 |
| 安全检查点 | `core/nav-server-security-checkpoint.html` | 服务端开发安全速查 |
| 能力矩阵索引 | `core/nav-overview-capability-matrix.html` | 2026 岗位能力对标检索 |
| 生产生命周期检索 | `core/nav-overview-lifecycle.html` | 按生产阶段检索知识点 |
| AI 应用组件分层检索 | `core/nav-overview-ai-component-stack.html` | 九层组件 × 必备/生产刚需/增强 |
| 方法论 | `core/chapter-core-methodology.html` | 道法术器势六层 · 十六组（205 卡） |
| AI 方法论 | `core/chapter-core-methodology-ai.html` | AI 应用开发方法论专篇（41 卡） |
| 工程化要点 | `core/chapter-engineering-practices.html` | 11 组工程化实践（88 卡） |
| 生产踩坑 | `core/chapter-production-pitfalls.html` | 10 组真实故障复盘（82 卡） |
| 混合部署 | `core/chapter-hybrid-deployment.html` | 多云/混合云部署模式（8 卡） |
| 设计原则 & GoF 23 | `java-design-patterns-principles/` | 设计原则 + 超越 GoF 23 |
| 软件定律 / 理论 / 原则 / 模式 | `Software-Engineering-Laws-Theories-Principles-and-Patterns/` | 24 条 + 7 类 + 13 类 + 6 类索引 |
| 软件工程「道法术器势」| `Software-Engineering-Core-Philosophical-Principles-and-Methodologies/` | 核心哲学原理完整篇 |
| 信创（信息技术应用创新）研究专题 | `xinchuang/index.html` | 独立静态站点 · 政策 / 产业 / 技术 / 工程 / 安全 / 经济 多视角 |

---

## 技术栈

- **纯静态 HTML** · 无后端 · 无构建步骤 · 直接由 GitHub Pages 渲染
- **共享样式系统**：`core/assets/design-system.css`（章节站）+ `docs/shared/style/satellite-base.css`（三子站共用）
- **Mermaid 可视化**：章节页内嵌 Mermaid 渲染方法论地图、领域关系图等
- **主题与字体**：`theme-init.js`（深色/浅色切换）、JetBrainsMono + WorkSans
- **GitHub Pages 专用**：`.nojekyll` 防止 Liquid 解析 Spring AI 模板占位符（`{{it}}` 等）

---

## 单一真源与工具链

全站数字**唯一写源**：`docs/kb-counts.json`，包含 `counts`（全局总量）与 `struct`（每章节/卡片位的精确计数）。所有 `data-kb-pos` 计数位均由它驱动。

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

- 计数真源 `docs/kb-counts.json` 最近更新：**2026-11-14**
- 每次入库新卡 / 调整分组结构后，必须同步 `kb-counts.json` 并跑 `validate_kb.py`
- 红线 `data-page-node-id=0` 禁止任何预览，任何改动后须全局扫描确认
