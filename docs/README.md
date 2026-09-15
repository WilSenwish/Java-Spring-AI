# Java 工程能力知识库 · 全站章节内容总览

本仓库根目录（即本项目根）为《Java 专家 · 架构师 · 高级开发 工程能力知识库》静态文档站，全部页面为**单文件自包含 HTML**，无构建步骤，可被 GitHub Pages 直接托管。

本文件给出全站章节内容与文件结构总览；格式组织规则分为「共用规则」「标准 QA 章节」「特殊章节独享」三份文档，见文末[规则文档索引](#4.md)。

## 1. 技术形态

- **语言 / 字符**：`<html lang="zh-CN">`，`<meta charset="UTF-8">`。
- **单文件**：每个页面把结构、内容、所需的 `<style>` 内联样式全部封装在一个 `.html` 文件中；仅在多处复用的全局样式抽到 `assets/design-system.css`，页面复用功能抽到 `assets/nav.js`。
- **资源目录**：
  - `assets/`：`design-system.css`（全站设计系统 / 设计令牌）、`nav.js`（全站导航交互脚本）。
  - `shared/js/`：`echarts.min.js`、`mermaid.min.js`（按需引入）。
  - `shared/fonts/`：JetBrainsMono、WorkSans。
- **按需载入原则**：某页面若不含图表则不引入 `mermaid.min.js` / `echarts.min.js`；避免无关资源加载（见 `format-shared.md` 第 4 节）。每个 Mermaid 节点须带 `<!-- prettier-ignore -->`（§10）。
- **手机小屏强制**：全站页面必须适配 ≤768px / ≤480px；共享基线见 `assets/design-system.css` 的 `MOBILE-MANDATORY` 段，规范见 `format-shared.md` §8（与 `AGENTS.md` 硬红线同级）。
- **HTML 格式化**：仓库根 `npm run format:html`（Prettier 3）；配置与 Mermaid 保护见 `format-shared.md` §10。

## 2. 目录结构与文件清单

```
.
├── index.html                              # 全站首页（导航 + 章节卡片 + 统计区，仓库根）
├── AGENTS.md                               # 协作规范（硬红线 / 计数位）
├── docs/                                   # 格式规范文档（本目录）
│   ├── format-shared.md                    # 全站共用格式规则
│   ├── format-std-qa.md                    # 标准 QA 章节格式规则
│   ├── format-special.md                   # 特殊章节独享规则
│   ├── README.md                           # 本文件
│   ├── fix_mermaid.py                      # Mermaid 格式化辅助
│   ├── kb-counts.json                      # 权威计数唯一真源（勿手改）
│   └── facts/                              # 官方参考文档归档（只读，不在任何修改范围内）
├── tmp/                                    # 临时文件/备份（已 gitignore，不进版本库）
├── java-architect-interview/               # 主知识库（标准 QA + 特殊章节）
│   ├── index.html                          # 知识库首页（导航 + 章节卡片 + 统计区）
│   ├── chapter-01-jvm-memory-classloading.html # 标准QA章节 ×15
│   ├── chapter-02-gc-performance.html
│   ├── chapter-03-concurrency-locks.html
│   ├── chapter-04-threadpool-virtual-threads.html
│   ├── chapter-05-spring-core.html
│   ├── chapter-06-spring-boot-modern.html
│   ├── chapter-07-mysql-deep.html
│   ├── chapter-08-redis-cache.html
│   ├── chapter-09-distributed-systems.html
│   ├── chapter-10-microservice-cloud.html
│   ├── chapter-11-middleware-engineering.html
│   ├── chapter-12-ai-engineering.html
│   ├── chapter-13-network-io.html
│   ├── chapter-14-databases.html
│   ├── chapter-15-reactive.html
│   ├── chapter-core-methodology.html       # 特殊章节：核心方法论（M系列）
│   ├── nav-overview-priority.html          # 特殊章节：优先级大盘（ov组件）
│   ├── chapter-questions-eight-part.html   # 特殊章节：核心原理速查（E系列）
│   ├── chapter-questions-scenario.html     # 特殊章节：场景题（S系列）
│   ├── nav-server-security-checkpoint.html # 特殊章节：安全 Checkpoint 手册
│   ├── assets/                             # design-system.css, nav.js
│   └── shared/                             # fonts, js（echarts/mermaid）
└── java-architect-interview-mind/          # 思维导图版（mind-* 对应篇章）
```

## 3. 章节内容与归属规则矩阵

> 列「格式规则类型」说明该章节是**通用规则**（与全部或多数章节共用）还是**独享规则**（有专属格式体系）。详细规则见本目录其它文档。

| 文件 | 主题 | ID 体系 | 卡片数 | 格式规则类型 |
|------|------|---------|-------|--------------|
| `../index.html` | 全站首页（导航/统计/标签云） | – | – | 独享（首页专属组件） |
| `chapter-01-jvm-memory-classloading` | JVM 内存与类加载 | `C01.##` | 11 | 标准QA（共用） |
| `chapter-02-gc-performance` | GC 算法与性能调优 | `C02.##` | 12 | 标准QA（共用） |
| `chapter-03-concurrency-locks` | 并发与锁 | `C03.##` | 12 | 标准QA（共用） |
| `chapter-04-threadpool-virtual-threads` | 线程池与虚拟线程 | `C04.##` | 10 | 标准QA（共用） |
| `chapter-05-spring-core` | Spring 核心 | `C05.##` | 11 | 标准QA（共用） |
| `chapter-06-spring-boot-modern` | Spring Boot 现代化实践 | `C06.##` | 13 | 标准QA（共用） |
| `chapter-07-mysql-deep` | MySQL 深入 | `C07.##` | 15 | 标准QA（共用） |
| `chapter-08-redis-cache` | Redis 与缓存 | `C08.##` | 11 | 标准QA（共用） |
| `chapter-09-distributed-systems` | 分布式系统 | `C09.##` | 16 | 标准QA（共用） |
| `chapter-10-microservice-cloud` | 微服务与云原生 | `C10.##` | 27 | 标准QA（共用） |
| `chapter-11-middleware-engineering` | 中间件工程化 | `C11.##` | 25 | 标准QA（共用） |
| `chapter-12-ai-engineering` | AI 工程化 | `C12.##` | 31 | 标准QA（共用） |
| `chapter-13-network-io` | 网络与 IO | `C13.##` | 13 | 标准QA（共用） |
| `chapter-14-databases` | 数据库扩展 | `C14.##` | 12 | 标准QA（共用） |
| `chapter-15-reactive` | 响应式编程 | `C15.##` | 6 | 标准QA（共用） |
| `chapter-core-methodology` | 核心方法论 | `M##.##` | <span class="kb-count" data-kb-count="methodology" data-kb-pos="P10">91</span> | 独享（方法论变体卡片） |
| `chapter-overview-priority` | 知识点大盘与优先级 | `ov-*` 组件 | 359 条目 | 独享（优先级矩阵） |
| `chapter-questions-eight-part` | 核心原理速查 | `E##.##` | 61 | 独享（epq 速查组件） |
| `chapter-questions-scenario` | 场景设计题 | `S##.##` | 70 | 独享（场景卡片变体） |
| `chapter-server-security-checkpoint` | 服务端安全自检清单 | 章节式 `h2/h3` | – | 独享（独立样式单页） |

### 3.1 规则分组一句话

- **共用规则**：15 个 `C##.##` 标准 QA 章节采用同一套「侧边目录 + 页头 + `qa-card` 六层卡片」格式（详见 `format-std-qa.md`）。
- **独享规则**：其余 5 个特殊章节各自拥有专属的格式体系，互不相同（详见 `format-special.md`）。
- **跨所有页面的通用底层**：设计系统令牌、难度 / 优先级标签体系、资源按需载入等（详见 `format-shared.md`）。

### 3.2 全站难度 / 优先级分布（按卡片）

- 难度三级：`senior`(高级开发) / `expert`(专家级) / `architect`(架构级)。**题目 359**（篇章+核心原理+场景）：专家 46 / 架构 172 / 高级开发 141；**方法论 <span class="kb-count" data-kb-count="methodology" data-kb-pos="P11">91</span> 卡另计**（专家 23 / 架构 49 / 高级开发 3）。方法论/工程化/踩坑难度各自单独统计，不与题目难度加总。
- 优先级：`P0`–`P2`；标准 QA、核心原理速查、场景题三类**全部携带**（合计 92/209/58 = 359）；方法论仅部分卡片（<span class="kb-count" data-kb-count="methodology_with_priority" data-kb-pos="P12">45</span>/<span class="kb-count" data-kb-count="methodology" data-kb-pos="P13">91</span>）携带；安全手册**不含**优先级。

## 4. 规则文档索引

| 文档 | 内容 | 适用对象 |
|------|------|----------|
| [`format-shared.md`](format-shared.md) | 全站共用格式规则：资源与骨架、设计令牌、标签体系、**侧栏分组标题 / 顶底导航归一**（§4.1–4.2）、**手机小屏强制（§8）**、**主题/暗黑（§9）**、**Prettier + Mermaid ignore（§10）**、命名/ID 规范 | 所有页面 |
| [`format-std-qa.md`](format-std-qa.md) | 标准 QA 章节格式规则：15 个 `C##.##` 章节共用 | chapter-01 ~ 15 |
| [`format-special.md`](format-special.md) | 特殊章节独享规则（含方法论 / 工程化侧栏分组锚点；**首页卡片顺序与难度徽标 / 折叠块**） | 方法论 / 工程化 / 大盘 / 原理 / 场景 / 安全 / 首页 |
