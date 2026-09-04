# Java 工程能力知识库 · 全站章节内容总览

本目录（`..`）为《Java 专家 · 架构师 · 高级开发 工程能力知识库》静态文档站，全部页面为**单文件自包含 HTML**，无构建步骤，可被 GitHub Pages 直接托管。

本文件给出全站章节内容与文件结构总览；格式组织规则分为「共用规则」与「独享规则」两份文档，见文末[规则文档索引](#4.md)。

## 1. 技术形态

- **语言 / 字符**：`<html lang="zh-CN">`，`<meta charset="UTF-8">`。
- **单文件**：每个页面把结构、内容、所需的 `<style>` 内联样式全部封装在一个 `.html` 文件中；仅在多处复用的全局样式抽到 `assets/design-system.css`，页面复用功能抽到 `assets/nav.js`。
- **资源目录**：
  - `assets/`：`design-system.css`（全站设计系统 / 设计令牌）、`nav.js`（全站导航交互脚本）。
  - `shared/js/`：`echarts.min.js`、`mermaid.min.js`（按需引入）。
  - `shared/fonts/`：JetBrainsMono、WorkSans。
- **按需载入原则**：某页面若不含图表则不引入 `mermaid.min.js` / `echarts.min.js`；避免无关资源加载（见 `format-shared.md` 第 4 节）。

## 2. 目录结构与文件清单

```
java-architect-interview/
├── index.html                              # 全站首页（导航 + 章节卡片 + 统计区）
├── chapter-01-jvm-memory-classloading.html # 标准QA章节 ×15
├── chapter-02-gc-performance.html
├── chapter-03-concurrency-locks.html
├── chapter-04-threadpool-virtual-threads.html
├── chapter-05-spring-core.html
├── chapter-06-spring-boot-modern.html
├── chapter-07-mysql-deep.html
├── chapter-08-redis-cache.html
├── chapter-09-distributed-systems.html
├── chapter-10-microservice-cloud.html
├── chapter-11-middleware-engineering.html
├── chapter-12-ai-engineering.html
├── chapter-13-network-io.html
├── chapter-14-databases.html
├── chapter-15-reactive.html
├── chapter-core-methodology.html           # 特殊章节：核心方法论（M系列）
├── chapter-overview-priority.html          # 特殊章节：优先级大盘（ov组件）
├── chapter-questions-eight-part.html       # 特殊章节：八股速查（E系列）
├── chapter-questions-scenario.html         # 特殊章节：场景题（S系列）
├── chapter-server-security-checkpoint.html # 特殊章节：安全 Checkpoint 手册
├── assets/                                 # design-system.css, nav.js
├── shared/                                 # fonts, js（echarts/mermaid）
└── docs/                                   # 本文档所在目录（规则说明，非站点页面）
```

## 3. 章节内容与归属规则矩阵

> 列「格式规则类型」说明该章节是**通用规则**（与全部或多数章节共用）还是**独享规则**（有专属格式体系）。详细规则见本目录其它文档。

| 文件 | 主题 | ID 体系 | 卡片数 | 格式规则类型 |
|------|------|---------|-------|--------------|
| `../../index.html` | 全站首页（导航/统计/标签云） | – | – | 独享（首页专属组件） |
| `chapter-01-jvm-memory-classloading` | JVM 内存与类加载 | `C01.##` | 10 | 标准QA（共用） |
| `chapter-02-gc-performance` | GC 算法与性能调优 | `C02.##` | 12 | 标准QA（共用） |
| `chapter-03-concurrency-locks` | 并发与锁 | `C03.##` | 11 | 标准QA（共用） |
| `chapter-04-threadpool-virtual-threads` | 线程池与虚拟线程 | `C04.##` | 10 | 标准QA（共用） |
| `chapter-05-spring-core` | Spring 核心 | `C05.##` | 10 | 标准QA（共用） |
| `chapter-06-spring-boot-modern` | Spring Boot 现代化实践 | `C06.##` | 13 | 标准QA（共用） |
| `chapter-07-mysql-deep` | MySQL 深入 | `C07.##` | 15 | 标准QA（共用） |
| `chapter-08-redis-cache` | Redis 与缓存 | `C08.##` | 11 | 标准QA（共用） |
| `chapter-09-distributed-systems` | 分布式系统 | `C09.##` | 16 | 标准QA（共用） |
| `chapter-10-microservice-cloud` | 微服务与云原生 | `C10.##` | 25 | 标准QA（共用） |
| `chapter-11-middleware-engineering` | 中间件工程化 | `C11.##` | 20 | 标准QA（共用） |
| `chapter-12-ai-engineering` | AI 工程化 | `C12.##` | 31 | 标准QA（共用） |
| `chapter-13-network-io` | 网络与 IO | `C13.##` | 11 | 标准QA（共用） |
| `chapter-14-databases` | 数据库扩展 | `C14.##` | 9 | 标准QA（共用） |
| `chapter-15-reactive` | 响应式编程 | `C15.##` | 6 | 标准QA（共用） |
| `chapter-core-methodology` | 面试核心方法论 | `M##.##` | 48 | 独享（方法论变体卡片） |
| `chapter-overview-priority` | 知识点大盘与优先级 | `ov-*` 组件 | 321 条目 | 独享（优先级矩阵） |
| `chapter-questions-eight-part` | 八股文速查 | `E##.##` | 50 | 独享（epq 速查组件） |
| `chapter-questions-scenario` | 场景设计题 | `S##.##` | 65 | 独享（场景卡片变体） |
| `chapter-server-security-checkpoint` | 服务端安全自检清单 | 章节式 `h2/h3` | – | 独享（独立样式单页） |

### 3.1 规则分组一句话

- **共用规则**：15 个 `C##.##` 标准 QA 章节采用同一套「侧边目录 + 页头 + `qa-card` 六层卡片」格式（详见 `format-std-qa.md`）。
- **独享规则**：其余 5 个特殊章节各自拥有专属的格式体系，互不相同（详见 `format-special.md`）。
- **跨所有页面的通用底层**：设计系统令牌、难度 / 优先级标签体系、资源按需载入等（详见 `format-shared.md`）。

### 3.2 全站难度 / 优先级分布（按卡片）

- 难度三级：`senior`(高级开发) / `expert`(专家级) / `architect`(架构级)；全站 `data-difficulty`：architect 203、senior 143、expert 67。
- 优先级：`P0`–`P2`；仅 标准 QA、八股速查、场景题 三类携带；方法论与安全手册**不含**优先级。

## 4. 规则文档索引

| 文档 | 内容 | 适用对象 |
|------|------|----------|
| [`format-shared.md`](format-shared.md) | 全站共用格式规则：资源与骨架、设计令牌、标签体系、命名/ID 规范、通用注意事项 | 所有页面 |
| [`format-std-qa.md`](format-std-qa.md) | 标准 QA 章节格式规则：15 个 `C##.##` 章节共用 | chapter-01 ~ 15 |
| [`format-special.md`](format-special.md) | 特殊章节独享规则 | 方法论 / 大盘 / 八股 / 场景 / 安全 / 首页 |