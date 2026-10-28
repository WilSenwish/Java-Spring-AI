# Java 工程能力知识库 · 全站章节内容总览

本仓库根目录（即本项目根）为《Java 专家 · 架构师 · 高级开发 工程能力知识库》静态文档站，全部页面为**单文件自包含 HTML**，无构建步骤，可被 GitHub Pages 直接托管。

本文件给出全站章节内容与文件结构总览；格式组织规则分为「共用规则」「标准 QA 章节」「特殊章节独享」三份文档，见文末[规则文档索引](#4.md)。

## 1. 技术形态

- **语言 / 字符**：`<html lang="zh-CN">`，`<meta charset="UTF-8">`。
- **单文件**：每个页面把结构、内容、所需的 `<style>` 内联样式全部封装在一个 `.html` 文件中；仅在多处复用的全局样式抽到 `assets/design-system.css`，页面复用功能抽到 `assets/nav.js`。
- **资源目录**：
  - `java-architect-interview/assets/`：`design-system.css`（全站设计系统 / 设计令牌）、`nav.js` / `theme-init.js`。
  - `docs/shared/js/`：`echarts.min.js`、`mermaid.min.js`（及 d3 / three 等，按需引入）；章节页路径为 `../docs/shared/js/…`。
  - `docs/shared/fonts/`：JetBrainsMono、WorkSans（`design-system.css` 经 `../../docs/shared/fonts/` 引用）。
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
│   ├── kb-counts.json                      # 权威计数唯一真源（勿手改）
│   ├── shared/                             # 全站共用 fonts · js（echarts/mermaid 等，按需）
│   └── facts/                              # 官方参考文档归档（只读）
├── tmp/                                    # 临时文件/备份（已 gitignore；有 git 时勿长期堆备份）
├── java-architect-interview/               # 主知识库（标准 QA + 特殊章节 + nav 聚合）
│   ├── index.html                          # 章节索引
│   ├── chapter-01~15-*.html                # 标准 QA 篇章 ×15（C）
│   ├── chapter-core-methodology.html       # 方法论（M）
│   ├── chapter-engineering-practices.html  # 工程化（G）
│   ├── chapter-production-pitfalls.html    # 生产踩坑（K）
│   ├── chapter-questions-eight-part.html   # 核心原理（E）
│   ├── chapter-questions-scenario.html     # 场景题（S）
│   ├── chapter-question-ai-engineering-deep.html  # AI 工程纵深（A）
│   ├── chapter-questions-domain.html       # 垂直领域（D）
│   ├── nav-overview-priority.html          # 优先级×难度×类型大盘（ov-*）
│   ├── nav-overview-quick-list.html        # 知识点速查清单
│   ├── nav-server-security-checkpoint.html # 安全 Checkpoint
│   └── assets/                             # design-system.css · nav.js · theme-init.js
```

## 3. 章节内容与归属规则矩阵

> 列「格式规则类型」说明该章节是**通用规则**（与全部或多数章节共用）还是**独享规则**（有专属格式体系）。详细规则见本目录其它文档。

| 文件 | 主题 | ID 体系 | 卡片数 | 格式规则类型 |
|------|------|---------|-------|--------------|
| `../index.html` | 全站首页（导航/统计/标签云） | – | – | 独享（首页专属组件） |
| `chapter-01-jvm-memory-classloading` | JVM 内存与类加载 | `C01.##` | 12 | 标准QA（共用） |
| `chapter-02-gc-performance` | GC 算法与性能调优 | `C02.##` | 12 | 标准QA（共用） |
| `chapter-03-concurrency-locks` | 并发与锁 | `C03.##` | 12 | 标准QA（共用） |
| `chapter-04-threadpool-virtual-threads` | 线程池与虚拟线程 | `C04.##` | 10 | 标准QA（共用） |
| `chapter-05-spring-core` | Spring 核心 | `C05.##` | 11 | 标准QA（共用） |
| `chapter-06-spring-boot-modern` | Spring Boot 现代化实践 | `C06.##` | 15 | 标准QA（共用） |
| `chapter-07-mysql-deep` | MySQL 深入 | `C07.##` | 16 | 标准QA（共用） |
| `chapter-08-redis-cache` | Redis 与缓存 | `C08.##` | 12 | 标准QA（共用） |
| `chapter-09-distributed-systems` | 分布式系统 | `C09.##` | 17 | 标准QA（共用） |
| `chapter-10-microservice-cloud` | 微服务与云原生 | `C10.##` | 30 | 标准QA（共用） |
| `chapter-11-middleware-engineering` | 中间件工程化 | `C11.##` | 30 | 标准QA（共用） |
| `chapter-12-ai-engineering` | AI 工程化 | `C12.##` | 35 | 标准QA（共用） |
| `chapter-13-network-io` | 网络与 IO | `C13.##` | 14 | 标准QA（共用） |
| `chapter-14-databases` | 数据库扩展 | `C14.##` | 14 | 标准QA（共用） |
| `chapter-15-reactive` | 响应式编程 | `C15.##` | 12 | 标准QA（共用） |
| `chapter-core-methodology` | 核心方法论 | `M##.##` | <span class="kb-count" data-kb-count="methodology" data-kb-pos="P10">145</span> | 独享（方法论三层卡） |
| `chapter-engineering-practices` | 工程化要点 | `G##.##` | <span class="kb-count" data-kb-count="engineering">65</span> | 独享（工程化三层卡） |
| `chapter-production-pitfalls` | 生产踩坑 | `K##.##` | <span class="kb-count" data-kb-count="pitfalls">65</span> | 独享（踩坑三层卡） |
| `chapter-questions-eight-part` | 核心原理速查 | `E##.##` | <span class="kb-count" data-kb-count="basics">74</span> | 独享（epq 速查） |
| `chapter-questions-scenario` | 场景设计题 | `S##.##` | <span class="kb-count" data-kb-count="scenarios">74</span> | 独享（场景卡） |
| `chapter-question-ai-engineering-deep` | AI 工程纵深 | `A##.##` | <span class="kb-count" data-kb-count="ai_engineering_deep">74</span> | 独享（AI 纵深轴） |
| `chapter-questions-domain` | 垂直领域 | `D##.##` | <span class="kb-count" data-kb-count="domain_questions">72</span> | 独享（领域卡） |
| `nav-overview-priority` | 优先级大盘 | `ov-*` | = `total` 条目 | 独享（优先级矩阵） |
| `nav-overview-quick-list` | 知识点速查清单 | 清单导航 | – | 独享（速查聚合） |
| `nav-server-security-checkpoint` | 服务端安全自检 | 章节式 `h2/h3` | – | 独享（独立单页） |

> 篇章卡数以宿主页实计为准；上表 C 列已与 2026-10-28 宿主页对齐。聚合计数一律以 SSOT `docs/kb-counts.json` 为准，**禁止在规范文中长期写死易漂移数字**。

### 3.1 规则分组一句话

- **共用规则**：15 个 `C##.##` 标准 QA 章节采用同一套「侧边目录 + 页头 + `qa-card` 六层卡片」格式（详见 `format-std-qa.md`）。
- **独享规则**：M/G/K 三层卡、E 的 epq、S/D 场景变体、A 纵深轴、`nav-*` 聚合页与安全手册各自有专属体系（详见 `format-special.md`）。
- **跨所有页面的通用底层**：设计系统令牌、难度 / 优先级标签体系、资源按需载入等（详见 `format-shared.md`）。

### 3.2 全站难度 / 优先级分布（按卡片）

- 难度三级：`senior`(高级) / `expert`(专家) / `architect`(架构)。**覆盖进入 `total` 的五类（C/A/E/S/D）**：专家 / 架构师 / 高级开发求和 = `total`。**文案双轨**：标签位一律短表 **专家 / 架构 / 高级**，正文用 **专家 / 架构师 / 高级开发**（见 `format-shared.md` §3.1）。
- **M/G/K 三专篇不分难度等级**（2026-09-16）：无 `data-difficulty`、无专篇难度计数键。方法论 <span class="kb-count" data-kb-count="methodology" data-kb-pos="P11">145</span> 卡另计，不与题目难度加总。
- 优先级：`P0`–`P2`；C/A/E/S/D **全部携带**（求和 = `total`）；方法论属性侧优先级分子/分母为 <span class="kb-count" data-kb-count="methodology_with_priority" data-kb-pos="P12">0</span>/<span class="kb-count" data-kb-count="methodology" data-kb-pos="P13">145</span>；安全手册**不含**优先级。
- **口径**：`total` = 篇章C + AI纵深A + 核心原理E + 场景S + 垂直领域D；M/G/K 专篇键不进 total。

## 4. 规则文档索引

| 文档 | 内容 | 适用对象 |
|------|------|----------|
| [`format-shared.md`](format-shared.md) | 全站共用格式规则：资源与骨架、设计令牌、标签体系、**侧栏分组标题 / 顶底导航归一**（§4.1–4.2）、**手机小屏强制（§8）**、**主题/暗黑（§9）**、**Prettier + Mermaid ignore（§10）**、命名/ID 规范 | 所有页面 |
| [`format-std-qa.md`](format-std-qa.md) | 标准 QA 章节格式规则：15 个 `C##.##` 章节共用 | chapter-01 ~ 15 |
| [`format-special.md`](format-special.md) | 特殊章节独享规则（M/G/K/E/S/A/D + `nav-*`；**首页卡片顺序与难度徽标 / 折叠块**） | 方法论 / 工程化 / 踩坑 / 大盘 / 原理 / 场景 / AI 纵深 / 垂直领域 / 安全 / 首页 |
