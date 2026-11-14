# Java 工程能力知识库 · 全站章节内容总览

本仓库根目录（即本项目根）为《Java 专家 · 架构师 · 高级开发 工程能力知识库》静态文档站，全部页面为**单文件自包含 HTML**，无构建步骤，可被 GitHub Pages 直接托管。

本文件给出全站章节内容与文件结构总览；格式组织规则分为「共用规则」「标准 QA 章节」「特殊章节独享」三份文档，见文末[规则文档索引](#4.md)。

## 1. 技术形态

- **语言 / 字符**：`<html lang="zh-CN">`，`<meta charset="UTF-8">`。
- **单文件**：每个页面把结构、内容、所需的 `<style>` 内联样式全部封装在一个 `.html` 文件中；仅在多处复用的全局样式抽到 `assets/design-system.css`，页面复用功能抽到 `assets/nav.js`。
- **资源目录**：
  - `core/assets/`：`design-system.css`（全站设计系统 / 设计令牌）、`nav.js` / `theme-init.js`。
  - `docs/shared/js/`：`echarts.min.js`、`mermaid.min.js`（及 d3 / three 等，按需引入）；章节页路径为 `../docs/shared/js/…`。
  - `docs/shared/fonts/`：JetBrainsMono、WorkSans（`design-system.css` 经 `../../docs/shared/fonts/` 引用）。
- **按需载入原则**：某页面若不含图表则不引入 `mermaid.min.js` / `echarts.min.js`；避免无关资源加载（见 `specs/format-shared.md` 第 4 节）。每个 Mermaid 节点须带 `<!-- prettier-ignore -->`（§10）。
- **手机小屏强制**：全站页面必须适配 ≤768px / ≤480px；共享基线见 `assets/design-system.css` 的 `MOBILE-MANDATORY` 段，规范见 `specs/format-shared.md` §8（与 `AGENTS.md` 硬红线同级）。
- **HTML 格式化**：仓库根 `npm run format:html`（Prettier 3）；配置与 Mermaid 保护见 `specs/format-shared.md` §10。

## 2. 目录结构与文件清单

```
.
├── index.html                              # 全站首页（导航 + 章节卡片 + 统计区，仓库根）
├── interview.html                          # 独立能力索引页（仓库根）
├── AGENTS.md                               # 协作规范（硬红线 / 计数位）
├── docs/                                   # 规约 / SSOT / 共享资源（本目录）
│   ├── specs/                              # 内容格式规范 format-* 四件（shared / std-qa / special / colors）
│   ├── README.md                           # 本文件
│   ├── kb-counts.json                      # 权威计数唯一真源（勿手改）
│   ├── catppuccin-tokens.json              # 配色唯一色源 SSOT（palette / derived / 豁免台账）
│   ├── search-index.json                   # 静态搜索索引（scripts/build_search_index.py 生成）
│   ├── scripts/                            # 站点构建/校验脚本（audit_catppuccin · build_search_index · build_xinchuang_site 等）
│   ├── shared/                             # 全站共用 fonts · js（echarts/mermaid 等，按需）
│   └── facts/                              # 官方参考文档归档（只读）
├── tmp/                                    # 临时文件/备份（已 gitignore）
├── core/               # 主知识库（标准 QA + 特殊章节 + nav 聚合）
│   ├── index.html                          # 章节索引
│   ├── chapter-01~15-*.html                # 标准 QA 篇章 ×15（C）
│   ├── chapter-core-methodology.html       # 方法论（M）
│   ├── chapter-core-methodology-ai.html     # AI 方法论专篇（L）
│   ├── chapter-hybrid-deployment.html       # 混合部署专题页（H）
│   ├── chapter-engineering-practices.html  # 工程化（G）
│   ├── chapter-production-pitfalls.html    # 生产踩坑（K）
│   ├── chapter-questions-eight-part.html   # 核心原理（E）
│   ├── chapter-questions-scenario.html     # 场景题（S）
│   ├── chapter-question-ai-engineering-deep.html  # AI 工程纵深（A）
│   ├── chapter-questions-domain.html       # 垂直领域（D）
│   ├── nav-overview-priority.html          # 优先级×难度×类型大盘（ov-*）
│   ├── nav-knowledge-quick-list.html       # 知识点速查清单
│   ├── nav-server-security-checkpoint.html # 安全 Checkpoint
│   ├── nav-overview-capability-matrix.html # 能力矩阵索引导航
│   ├── nav-overview-lifecycle.html         # 生产生命周期检索视图导航
│   ├── nav-overview-ai-component-stack.html # AI 应用组件分层检索视图导航
│   └── assets/                             # design-system.css · nav.js · theme-init.js
├── java-design-patterns-principles/        # 子站② 设计原则 & 超越 GoF 23
├── Software-Engineering-Laws-Theories-Principles-and-Patterns/          # 子站③ 定律 / 理论 / 原则 / 模式索引
├── Software-Engineering-Core-Philosophical-Principles-and-Methodologies/ # 子站④ 「道—法—术—器—势」哲学篇
├── xinchuang/                              # 信创独立站点（12 篇 md 源 + 自包含 HTML，非 KB 站群）
└── rk/                                     # 软考资料站（guard.exclude 全局忽略，非 KB 站群）
```

## 3. 章节内容与归属规则矩阵

> 列「格式规则类型」说明该章节是**通用规则**（与全部或多数章节共用）还是**独享规则**（有专属格式体系）。详细规则见本目录其它文档。

| 文件 | 主题 | ID 体系 | 卡片数 | 格式规则类型 |
|------|------|---------|-------|--------------|
| `../index.html` | 全站首页（导航/统计/标签云） | – | – | 独享（首页专属组件） |
| `chapter-01-jvm-memory-classloading` | JVM 内存与类加载 | `C01.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c01.n" data-kb-pos="P578">13</span> | 标准QA（共用） |
| `chapter-02-gc-performance` | GC 算法与性能调优 | `C02.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c02.n" data-kb-pos="P579">12</span> | 标准QA（共用） |
| `chapter-03-concurrency-locks` | 并发与锁 | `C03.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c03.n" data-kb-pos="P580">12</span> | 标准QA（共用） |
| `chapter-04-threadpool-virtual-threads` | 线程池与虚拟线程 | `C04.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c04.n" data-kb-pos="P581">11</span> | 标准QA（共用） |
| `chapter-05-spring-core` | Spring 核心 | `C05.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c05.n" data-kb-pos="P582">11</span> | 标准QA（共用） |
| `chapter-06-spring-boot-modern` | Spring Boot 现代化实践 | `C06.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c06.n" data-kb-pos="P583">15</span> | 标准QA（共用） |
| `chapter-07-mysql-deep` | MySQL 深入 | `C07.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c07.n" data-kb-pos="P584">16</span> | 标准QA（共用） |
| `chapter-08-redis-cache` | Redis 与缓存 | `C08.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c08.n" data-kb-pos="P585">12</span> | 标准QA（共用） |
| `chapter-09-distributed-systems` | 分布式系统 | `C09.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c09.n" data-kb-pos="P586">18</span> | 标准QA（共用） |
| `chapter-10-microservice-cloud` | 微服务与云原生 | `C10.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c10.n" data-kb-pos="P587">34</span> | 标准QA（共用） |
| `chapter-11-middleware-engineering` | 中间件工程化 | `C11.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c11.n" data-kb-pos="P588">32</span> | 标准QA（共用） |
| `chapter-12-ai-engineering` | AI 工程化 | `C12.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c12.n" data-kb-pos="P589">67</span> | 标准QA（共用） |
| `chapter-13-network-io` | 网络与 IO | `C13.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c13.n" data-kb-pos="P590">14</span> | 标准QA（共用） |
| `chapter-14-databases` | 数据库扩展 | `C14.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c14.n" data-kb-pos="P591">15</span> | 标准QA（共用） |
| `chapter-15-reactive` | 响应式编程 | `C15.##` | <span class="kb-count" data-kb-count="struct.chap.idx.c15.n" data-kb-pos="P592">12</span> | 标准QA（共用） |
| `chapter-core-methodology` | 核心方法论（M 篇）| `M##.##` | <span class="kb-count" data-kb-count="methodology_m" data-kb-pos="P40">164</span> | 独享（M 篇三层卡）|
| `chapter-core-methodology-ai` | AI 方法论专篇（L）| `L##.##` | <span class="kb-count" data-kb-count="methodology_l" data-kb-pos="P41">41</span> | 独享（L 专篇三层卡；与 M 篇合计 methodology=205）|
| `chapter-hybrid-deployment` | 混合部署专篇（H）| `H01.##` | <span class="kb-count" data-kb-count="hybrid" data-kb-pos="P42">8</span> | 独享（H 专题页）|
| `chapter-engineering-practices` | 工程化要点 | `G##.##` | <span class="kb-count" data-kb-count="engineering" data-kb-pos="P593">88</span> | 独享（工程化三层卡） |
| `chapter-production-pitfalls` | 生产踩坑 | `K##.##` | <span class="kb-count" data-kb-count="pitfalls" data-kb-pos="P594">82</span> | 独享（踩坑三层卡） |
| `chapter-questions-eight-part` | 核心原理速查 | `E##.##` | <span class="kb-count" data-kb-count="basics" data-kb-pos="P595">74</span> | 独享（epq 速查） |
| `chapter-questions-scenario` | 场景设计题 | `S##.##` | <span class="kb-count" data-kb-count="scenarios" data-kb-pos="P596">74</span> | 独享（场景卡） |
| `chapter-question-ai-engineering-deep` | AI 工程纵深 | `A##.##` | <span class="kb-count" data-kb-count="ai_engineering_deep" data-kb-pos="P597">112</span> | 独享（AI 纵深轴） |
| `chapter-questions-domain` | 垂直领域 | `D##.##` | <span class="kb-count" data-kb-count="domain_questions" data-kb-pos="P598">90</span> | 独享（领域卡） |
| `nav-overview-priority` | 优先级大盘 | `ov-*` | = `total` 条目 | 独享（优先级矩阵） |
| `nav-knowledge-quick-list` | 知识点速查清单 | 清单导航 | – | 独享（速查聚合） |
| `nav-server-security-checkpoint` | 服务端安全自检 | 章节式 `h2/h3` | – | 独享（独立单页） |
| `nav-overview-capability-matrix` | 能力矩阵索引（2026 岗位能力对标检索） | 清单导航 | – | 独享（索引聚合，不进 total、无计数位） |
| `nav-overview-lifecycle` | 生产生命周期检索视图 | 清单导航 | – | 独享（索引聚合，不进 total、无计数位） |
| `nav-overview-ai-component-stack` | AI 应用组件分层检索视图 | 组件清单导航 | – | 独享（索引聚合，不进 total、无计数位；由 `tmp/gen_component_stack_page.py` 生成） |

> 表内计数位一律带 `data-kb-pos` 由 SSOT `docs/kb-counts.json` 驱动（2026-11-09 注册，`sync_counts check` 逐位校验），**规范文中禁止裸写易漂移数字**。

### 3.1 规则分组一句话

- **共用规则**：15 个 `C##.##` 标准 QA 章节采用同一套「侧边目录 + 页头 + `content-card` 六层卡片」格式（详见 `specs/format-std-qa.md`）。
- **独享规则**：M/G/K 三层卡、E 的 epq、S/D 场景变体、A 纵深轴、`nav-*` 聚合页与安全手册各自有专属体系（详见 `specs/format-special.md`）。
- **跨所有页面的通用底层**：设计系统令牌、难度 / 优先级标签体系、资源按需载入等（详见 `specs/format-shared.md`）。

### 3.2 全站难度 / 优先级分布（按卡片）

- 难度三级：`senior`(高级) / `expert`(专家) / `architect`(架构)。**覆盖进入 `total` 的五类（C/A/E/S/D）**：专家 / 架构师 / 高级开发求和 = `total`。**文案双轨**：标签位一律短表 **专家 / 架构 / 高级**，正文用 **专家 / 架构师 / 高级开发**（见 `specs/format-shared.md` §3.1）。
- **M/G/K 三专篇不分难度等级**（2026-09-16）：无 `data-difficulty`、无专篇难度计数键。方法论（M 篇 + L 专篇）<span class="kb-count" data-kb-count="methodology" data-kb-pos="P11">205</span> 卡另计，不与题目难度加总。
- 优先级：`P0`–`P2`；C/A/E/S/D **全部携带**（求和 = `total`）；方法论属性侧优先级分子/分母为 <span class="kb-count" data-kb-count="methodology_with_priority" data-kb-pos="P12">0</span>/<span class="kb-count" data-kb-count="methodology" data-kb-pos="P13">205</span>；安全手册**不含**优先级。
- **口径**：`total` = 篇章C + AI纵深A + 核心原理E + 场景S + 垂直领域D；M/G/K 专篇键不进 total。

## 4. 规则文档索引

| 文档 | 内容 | 适用对象 |
|------|------|----------|
| [`specs/format-shared.md`](specs/format-shared.md) | 全站共用格式规则：资源与骨架、设计令牌、标签体系、**侧栏分组标题 / 顶底导航归一**（§4.1–4.2）、**手机小屏强制（§8）**、**主题/暗黑（§9）**、**Prettier + Mermaid ignore（§10）**、命名/ID 规范 | 所有页面 |
| [`specs/format-std-qa.md`](specs/format-std-qa.md) | 标准 QA 章节格式规则：15 个 `C##.##` 章节共用 | chapter-01 ~ 15 |
| [`specs/format-special.md`](specs/format-special.md) | 特殊章节独享规则（M/G/K/E/S/A/D + `nav-*`；**首页卡片顺序与难度徽标 / 折叠块**） | 方法论 / 工程化 / 踩坑 / 大盘 / 原理 / 场景 / AI 纵深 / 垂直领域 / 安全 / 首页 |
| [`specs/format-colors.md`](specs/format-colors.md) | 配色单一色源规约（红线 13）：Catppuccin 令牌、图表内联色 RETINT 登记、门禁 `scripts/audit_catppuccin.py` | 所有页面 |
