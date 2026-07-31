# Java 架构师高频场景题 HTML 生成计划

## Summary

在现有 `java-architect-interview/` 目录下新增一份独立的**高频真实场景题** HTML 文件，包含 30 道覆盖 2026 年 Java 高级开发与架构师面试要求的真实业务场景题。与已有 12 章知识点问答（六层结构：本质→演进→原理→实践→追问→陷阱）不同，场景题以**真实业务背景**为切入点，强调多技术栈叠加、多场景重叠的综合性分析能力。每道题遵循七层结构：场景背景 → 核心挑战 → 分析框架 → 解决方案 → 关键代码 → 深度追问 → 常见陷阱。同时更新 `index.html` 导航首页，新增场景题入口卡片。

## Current State Analysis

### 已有资产
- **设计系统**：`assets/design-system.css`（Solid 冷峻技术文档风格，蓝紫色系）
- **共享资源**：`_shared/fonts/`（WorkSans + JetBrainsMono）、`_shared/js/`（echarts.min.js + mermaid.min.js）
- **导航脚本**：`assets/nav.js`
- **12 章知识点问答**：chapter-01 ~ chapter-12，共 116 道 Q&A
- **导航首页**：`index.html`，含 Hero 区 + 12 张章节卡片

### 现有 CSS 可复用组件
| 组件 | 类名 | 用途 |
|------|------|------|
| Q&A 卡片 | `.qa-card` + `data-difficulty` | 场景题卡片容器 |
| 难度标签 | `.difficulty-senior/architect/expert` | 难度标识 |
| 分层结构 | `.qa-layer` + `data-layer` | 七层结构复用 |
| 代码块 | `.code-block` | 代码示例 |
| 提示框 | `.callout-tip/pitfall/deep/danger` | 陷阱/提示/深度标注 |
| 对比表格 | `.compare-table` | 方案对比 |
| 图表容器 | `.mermaid-container` / `.chart-figure` | 架构图/流程图 |
| 侧边栏 TOC | `.sidebar-toc` | 题目导航 |
| 章节导航 | `.chapter-nav` | 底部翻页 |

### 差异点
现有 `.qa-layer` 的 `data-layer` 仅支持 6 种（essence/evolution/principle/practice/deep/pitfall）。场景题需要 7 层，新增 `scenario` 和 `challenge` 两种 layer 类型对应的 CSS 样式。

## Proposed Changes

### 文件 1：新建 `scenario-questions.html`

**路径**：`/Users/chenjunbing/Develop/Project/Personal/Java Spring AI/java-architect-interview/scenario-questions.html`

**页面结构**：
```
<head>
  - <link> design-system.css
  - <script> mermaid.min.js（用于架构流程图）
  - <style> 场景题专属样式（新增 layer 类型 + 场景标签 + 布局微调）
</head>
<body>
  <div class="page-wrapper">
    <aside class="sidebar-toc">  ← 分组目录（7 大类 30 题）
    <main class="content-main">
      <div class="chapter-header">  ← 篇章头部（标题/副标题/统计信息）
      <!-- 7 个分类区块，每块含若干场景题卡片 -->
      <section class="scenario-group">  ×7
        <h2 class="group-title">
        <div class="qa-card" data-difficulty="...">  ×30
          - 场景背景 (data-layer="scenario")
          - 核心挑战 (data-layer="challenge")
          - 分析框架 (data-layer="principle")
          - 解决方案 (data-layer="practice")
          - 关键代码 (data-layer="practice" + .code-block)
          - 深度追问 (data-layer="deep")
          - 常见陷阱 (data-layer="pitfall")
      <nav class="chapter-nav">  ← 返回首页
    </main>
  </div>
  <script> mermaid 初始化
</body>
```

**新增 CSS（内联在 `<style>` 中）**：
```css
/* 新增 layer 类型 */
.qa-layer[data-layer="scenario"] .qa-layer-title::before { background: var(--accent); }
.qa-layer[data-layer="challenge"] .qa-layer-title::before { background: var(--danger); }

/* 场景分组标题 */
.scenario-group { margin-bottom: var(--space-xl); }
.group-title {
  font-size: 1.4rem; font-weight: 700;
  color: var(--ink);
  margin-bottom: var(--space-md);
  padding-bottom: var(--space-xs);
  border-bottom: 1px solid var(--rule);
  display: flex; align-items: center; gap: var(--space-sm);
}
.group-title .group-number {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--accent);
  background: rgba(37,99,235,0.1);
  padding: 2px 10px;
  border-radius: 20px;
}

/* 场景标签（行业/技术栈） */
.scenario-tags {
  display: flex; flex-wrap: wrap; gap: 6px;
  margin-bottom: var(--space-sm);
}
.scenario-tag {
  font-size: 0.72rem; font-weight: 600;
  padding: 2px 8px; border-radius: 4px;
  background: var(--bg2); color: var(--muted);
  border: 1px solid var(--rule);
}
.scenario-tag.tag-hot { color: var(--danger); border-color: rgba(220,38,38,0.2); }

/* 侧边栏分组 */
.sidebar-toc .toc-group { margin-bottom: var(--space-md); }
.sidebar-toc .toc-group-title {
  font-size: 0.72rem; font-weight: 700;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 4px;
  padding-left: 10px;
}
```

### 30 道场景题清单

#### 一、高并发系统设计（5 题）
| # | 场景题 | 难度 | 重叠场景 |
|---|--------|------|----------|
| S01 | 百万 QPS 秒杀系统设计 | 架构级 | 缓存+MQ+分布式锁+限流+数据库 |
| S02 | 千亿级短链服务设计 | 架构级 | 布隆过滤器+分库分表+缓存+302跳转 |
| S03 | 春晚红包系统设计 | 专家级 | 流量削峰+异步+数据一致性+容灾 |
| S04 | 直播带货系统设计 | 架构级 | 实时推送+高并发下单+IM+CDN |
| S05 | 热点账户高并发扣款 | 架构级 | 数据库锁+缓存+异步+对账 |

#### 二、分布式系统（5 题）
| # | 场景题 | 难度 | 重叠场景 |
|---|--------|------|----------|
| S06 | 分布式锁选型与实现 | 高级 | Redis+ZooKeeper+Redlock+锁续命 |
| S07 | 跨服务分布式事务方案 | 架构级 | Seata+TCC+本地消息表+MQ |
| S08 | 分布式 ID 生成方案 | 高级 | 雪花算法+号段模式+分库分表 |
| S09 | 微服务雪崩排查与治理 | 架构级 | 熔断降级+链路追踪+线程池+监控 |
| S10 | 缓存与数据库一致性 | 高级 | 延时双删+Canal+最终一致性 |

#### 三、数据库与存储（4 题）
| # | 场景题 | 难度 | 重叠场景 |
|---|--------|------|----------|
| S11 | 亿级数据分库分表方案 | 架构级 | ShardingSphere+迁移+双写+扩容 |
| S12 | 线上慢 SQL 优化实战 | 高级 | EXPLAIN+索引+重写+分区表 |
| S13 | MySQL 主从延迟解决 | 高级 | 读写分离+强制主库+半同步+缓存 |
| S14 | Redis 缓存三大问题 | 高级 | 穿透+击穿+雪崩+布隆过滤器+互斥锁 |

#### 四、微服务架构（4 题）
| # | 场景题 | 难度 | 重叠场景 |
|---|--------|------|----------|
| S15 | 单体到微服务拆分 | 架构级 | DDD+领域边界+数据迁移+灰度 |
| S16 | API 网关统一设计 | 架构级 | 鉴权+限流+路由+灰度+协议转换 |
| S17 | 消息队列积压处理 | 高级 | Kafka+消费者扩容+跳过积压+监控 |
| S18 | 灰度发布与流量染色 | 架构级 | 网关+标签路由+全链路灰度+回滚 |

#### 五、性能与稳定性（4 题）
| # | 场景题 | 难度 | 重叠场景 |
|---|--------|------|----------|
| S19 | 线上 OOM 排查实战 | 高级 | JVM+堆dump+MAT+Arthas+代码定位 |
| S20 | CPU 100% 问题排查 | 高级 | top+jstack+线程分析+GC+代码定位 |
| S21 | 接口性能优化 200ms→20ms | 高级 | 缓存+异步+批量+索引+连接池 |
| S22 | 消息可靠性保障 | 高级 | 丢失+重复+顺序+积压+幂等 |

#### 六、云原生与 AI（4 题）
| # | 场景题 | 难度 | 重叠场景 |
|---|--------|------|----------|
| S23 | Java 21 虚拟线程落地 | 架构级 | 虚拟线程+线程池+结构化并发+迁移 |
| S24 | 大模型 API 高可用封装 | 架构级 | 重试+降级+限流+缓存+多模型切换 |
| S25 | RAG 知识库 Java 实现 | 架构级 | 向量数据库+文档分块+Embedding+检索 |
| S26 | K8s 容器化部署 Java 应用 | 高级 | Docker+K8s+HPA+健康检查+配置管理 |

#### 七、综合场景（4 题）
| # | 场景题 | 难度 | 重叠场景 |
|---|--------|------|----------|
| S27 | 电商订单全链路设计 | 专家级 | 下单+支付+库存+物流+一致性 |
| S28 | 金融风控系统设计 | 专家级 | 实时计算+规则引擎+特征+流处理 |
| S29 | 千万级消息推送系统 | 架构级 | WebSocket+MQ+离线推送+分片 |
| S30 | 数据迁移与零停机发布 | 架构级 | 双写+灰度+回滚+数据校验+流量切换 |

### 每道场景题的七层内容规范

1. **场景背景**（data-layer="scenario"）
   - 业务背景描述（公司类型、业务场景、规模指标）
   - 技术约束（QPS、数据量、延迟要求、可用性要求）
   - 现有系统现状（可选）

2. **核心挑战**（data-layer="challenge"）
   - 列出 3-5 个核心技术难点
   - 标注多场景重叠点（如"缓存+分布式锁+MQ 三重叠加"）
   - 说明为什么这些问题难解

3. **分析框架**（data-layer="principle"）
   - 系统化拆解思路（分层/分维度/分阶段）
   - 关键决策点与权衡维度
   - 第一性原理分析

4. **解决方案**（data-layer="practice"）
   - 整体架构设计（含 Mermaid 架构图/流程图）
   - 分层详细方案（接入层→应用层→数据层）
   - 关键技术选型对比（用对比表格）
   - 容灾与降级方案

5. **关键代码**（data-layer="practice" + .code-block）
   - 核心逻辑的 Java 代码片段（伪代码或关键实现）
   - 配置示例（如 Redis Lua 脚本、SQL 索引设计）
   - 代码片段控制在 20-40 行，突出核心逻辑

6. **深度追问**（data-layer="deep"）
   - 3-5 个面试官可能的追问问题
   - 每个追问附核心答题思路（2-3 句）
   - 涵盖极端场景、容量规划、故障演练

7. **常见陷阱**（data-layer="pitfall"）
   - 3-5 个生产环境常见踩坑点
   - 每个陷阱附规避方案
   - 使用 .callout-danger 或 .callout-pitfall 样式标注

### 文件 2：更新 `index.html`

在现有 12 张章节卡片后，新增一张**场景题专篇卡片**：
```html
<a href="scenario-questions.html" class="chapter-card chapter-card-scenario">
  <div class="card-number">场景题专篇</div>
  <div class="card-title">高频真实场景题</div>
  <div class="card-desc">30 道覆盖高并发、分布式、数据库、微服务、性能、云原生与 AI 的综合场景设计题</div>
  <div class="card-footer">
    <span>30 题</span>
    <div class="card-tags">
      <span class="difficulty difficulty-senior">高级</span>
      <span class="difficulty difficulty-architect">架构</span>
      <span class="difficulty difficulty-expert">专家</span>
    </div>
  </div>
</a>
```

同时更新 Hero 区统计数字（116 → 146 道 Q&A，12 → 13 篇章）。

### Mermaid 图表

在以下场景题中嵌入 Mermaid 架构图/流程图：
- S01 秒杀系统：整体架构流程图
- S07 分布式事务：TCC/Seata 时序图
- S11 分库分表：数据分片架构图
- S16 API 网关：请求路由流程图
- S27 电商订单：全链路时序图

Mermaid JS 引用路径：`./_shared/js/mermaid.min.js`（已存在）。

## Assumptions & Decisions

1. **单页 vs 多页**：选择单页方案（`scenario-questions.html`），因为场景题之间有交叉引用，单页更便于横向对比，侧边栏 TOC 提供分组导航。
2. **七层结构 vs 六层结构**：场景题新增"场景背景"和"核心挑战"两层（替换原有的"本质问题"和"演进脉络"），更贴合场景题特性。"分析框架"对应原"第一性原理"，"解决方案"对应原"工程实践"。
3. **难度分布**：高级开发 12 题、架构级 14 题、专家级 4 题，符合高级开发+架构师双层级覆盖。
4. **代码语言**：所有代码片段使用 Java（结合 Spring Boot/Redis/MQ 等技术栈），配置片段使用 YAML/SQL/JSON。
5. **Mermaid 图表**：仅在高价值场景中嵌入（5 道题），避免过度使用导致页面加载缓慢。
6. **不新增字体/JS 依赖**：复用现有 `_shared/` 资源，不引入新的第三方库。
7. **CSS 方案**：新增样式内联在页面 `<style>` 中，不修改 `design-system.css`，保持已有 12 章样式不受影响。

## Verification Steps

1. **HTML 合法性**：在浏览器中打开 `scenario-questions.html`，确认页面正常渲染、无控制台报错
2. **Mermaid 渲染**：确认 5 张架构图/流程图正确渲染
3. **侧边栏导航**：点击侧边栏 TOC 链接，确认跳转到对应场景题
4. **响应式布局**：在移动端（375px）和桌面端（1440px）分别验证布局
5. **代码高亮**：确认代码块中的语法高亮类（.kw/.str/.com 等）正确渲染
6. **首页入口**：从 `index.html` 点击场景题卡片，确认跳转到 `scenario-questions.html`
7. **统计数字**：确认首页 Hero 区统计数字已更新（146 道 Q&A、13 篇章）
8. **难度标签**：确认 30 道题的难度标签颜色正确（蓝/紫/渐变）
