# 20道高频八股文面试题 — HTML 实现计划

## Summary

基于现有 12 章深度 Q&A（156 题）和 40 道场景题，新增 20 道高频八股文速查题，采用精炼四层结构（核心要点 → 详细解答 → 工程实践 → 高频追问），聚焦 2026 头部大厂仍在深入考察的核心原理，排除过时无用内容。

## Current State Analysis

### 现有内容矩阵

| 模块 | 数量 | 结构 | 定位 |
|------|------|------|------|
| 12 章深度 Q&A | 156 题 | 六层结构（本质/演进/原理/实践/追问/陷阱） | 深度理解、体系化学习 |
| 场景题专篇 | 40 题 | 七层结构（背景/挑战/框架/方案/代码/追问/陷阱） | 系统设计实战 |
| **新增八股文** | **20 题** | **四层结构（要点/解答/实践/追问）** | **速查应答、面试突击** |

### 差异化策略
- 深度 Q&A 每题约 1500~3000 字，侧重"为什么"与演进脉络
- 八股文每题控制在 600~1000 字，侧重"是什么"与标准应答话术
- 八股文采用 `epq-card`（Eight-Part Question Card）专用样式，视觉上与 `qa-card` 区分，更紧凑

## Proposed Changes

### 文件变更清单

| 序号 | 文件路径 | 变更类型 | 说明 |
|------|----------|----------|------|
| 1 | `java-architect-interview/eight-part-questions.html` | **新增** | 20 道八股文主页面 |
| 2 | `java-architect-interview/index.html` | **修改** | 更新统计、新增八股文卡片、标签云补充 |
| 3 | `java-architect-interview/assets/design-system.css` | **不修改** | 完全复用，八股文专属样式以内联 `<style>` 写入新页面 |

### HTML 结构设计

#### 页面骨架
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>高频八股文速查 — Java 架构师面试问答</title>
  <link rel="stylesheet" href="assets/design-system.css">
  <script src="./_shared/js/mermaid.min.js"></script>
  <style>
    /* 八股文专属内联样式（约80行） */
    .epq-card { /* 继承 qa-card 并微调 */ }
    .epq-section { /* 四层结构统一样式 */ }
    .epq-section-title { /* 小标题：蓝色竖线+大写字母 */ }
    .epq-kp-list { /* 核心要点：绿色勾选列表 */ }
    .epq-fu-list { /* 高频追问：Q/A 紧凑列表 */ }
    .epq-tag { /* 知识点标签 */ }
  </style>
</head>
<body>
  <div class="page-wrapper">
    <aside class="sidebar-toc">...</aside>
    <main class="content-main">
      <div class="chapter-header">...</div>
      <!-- 20道 epq-card 依次排列 -->
      <div class="chapter-nav">...</div>
    </main>
  </div>
  <script src="assets/nav.js"></script>
</body>
</html>
```

#### 八股文卡片四层结构（epq-card）
```
┌─────────────────────────────────────────┐
│ [01] 题目文本  [难度标签]                  │  ← qa-header（复用）
├─────────────────────────────────────────┤
│ ▎核心要点                                │
│   • 要点1                                │
│   • 要点2                                │
│   • 要点3                                │
├─────────────────────────────────────────┤
│ ▎详细解答                                │
│   结构化正文，允许代码块、表格、Mermaid    │
├─────────────────────────────────────────┤
│ [TIP] 工程实践提示                        │  ← callout callout-tip（复用）
│   一句话落地建议 + 关键参数                │
├─────────────────────────────────────────┤
│ ▎高频追问                                │
│   Q: ...?                                │
│   A: ...                                 │
└─────────────────────────────────────────┘
```

#### 新增内联样式定义
| 选择器 | 作用 |
|--------|------|
| `.epq-card` | 继承 `.qa-card`，调整 padding 更小、margin 更紧凑 |
| `.epq-section` | 四层共用容器，底部间距 `var(--space-sm)` |
| `.epq-section-title` | 小标题样式，0.78rem uppercase，左侧 4px 竖线，比 `qa-layer-title` 更轻量 |
| `.epq-kp-list` | 核心要点列表，绿色左边框，li 前使用自定义圆点 |
| `.epq-fu-list` | 追问列表，Q 加粗深色，A 灰色，间距紧凑 |
| `.epq-tag` | 知识点标签（如 "Java 21"、"JVM"），在卡片顶部横向排列 |

### 20 道题目选题与难度分级

**难度分布：** 高级开发 11 题 / 架构级 9 题

| 编号 | 题目 | 难度 | 知识点标签 | 选题理由 |
|------|------|------|-----------|----------|
| 01 | **Java 21 新特性：Virtual Threads、Pattern Matching、ZGC Generational、Sequenced Collections** | senior | `Java 21` `Virtual Threads` `ZGC` | 2026 面试必考，已全面进入 LTS 生产环境 |
| 02 | **HashMap 底层：扩容机制、hash 扰动、链表转红黑树、并发死链** | senior | `HashMap` `红黑树` `并发安全` | 八股文常青树，源码级细节必问 |
| 03 | **ConcurrentHashMap 1.7 vs 1.8：Segment 到 CAS+synchronized 的演进** | senior | `ConcurrentHashMap` `CAS` `锁优化` | 并发容器标杆题，演进对比是加分项 |
| 04 | **JMM 内存模型：volatile/synchronized/final 的内存语义与 happens-before** | senior | `JMM` `volatile` `happens-before` | 并发编程地基，大厂 P6+ 必问 |
| 05 | **Spring 循环依赖：三级缓存源码级解析与局限性** | architect | `Spring` `循环依赖` `三级缓存` | 从"是什么"到"为什么不用二级"的追问链 |
| 06 | **Spring Boot 自动配置：@EnableAutoConfiguration + spring.factories + @Conditional** | senior | `Spring Boot` `自动配置` `SPI` | 高频八股，考察对"约定优于配置"的理解 |
| 07 | **MySQL InnoDB B+树索引：聚簇索引、二级索引、覆盖索引、最左前缀原理** | senior | `MySQL` `B+树` `索引优化` | 数据库八股 TOP1，面试开场题 |
| 08 | **MySQL MVCC 实现：Read View 构造、undo log 版本链、trx_id 可见性判断** | senior | `MySQL` `MVCC` `事务隔离` | 与"幻读是否解决"形成经典追问链 |
| 09 | **Redis 缓存一致性：Cache Aside、延迟双删、Canal 订阅 binlog** | architect | `Redis` `缓存一致性` `Canal` | 分布式系统重灾区，真实项目痛点 |
| 10 | **分布式事务：2PC/TCC/SAGA/Seata AT 原理对比与生产选型** | architect | `分布式事务` `Seata` `SAGA` | 架构师面试必考，考察权衡能力 |
| 11 | **Redis 分布式锁：Redisson 看门狗机制 vs RedLock 的争议与取舍** | architect | `Redis` `分布式锁` `Redisson` | 从 setnx 到 RedLock 的完整认知链 |
| 12 | **Netty 高性能：Reactor 线程模型、零拷贝（sendfile/mmap/DirectBuffer）** | architect | `Netty` `NIO` `零拷贝` | 中间件/高并发岗位必问 |
| 13 | **Kafka 高性能原理：顺序写、页缓存、零拷贝、批量压缩、分区并发** | architect | `Kafka` `零拷贝` `批量压缩` | 消息队列标杆，考察对 OS 级优化的理解 |
| 14 | **JVM GC 演进：Serial → Parallel → CMS → G1 → ZGC/Shenandoah 对比** | architect | `JVM` `GC` `ZGC` | 从算法到收集器的完整演进线 |
| 15 | **熔断限流算法：令牌桶、漏桶、滑动窗口、Sentinel 自适应限流** | senior | `熔断限流` `Sentinel` `令牌桶` | 微服务稳定性必考 |
| 16 | **HTTPS/TLS 1.3 握手：证书链验证、密钥交换、前向安全** | senior | `HTTPS` `TLS` `证书链` | 安全基础八股，全栈/后端均考 |
| 17 | **Elasticsearch 倒排索引：分词、postings list、Skip List、BM25 打分** | senior | `ES` `倒排索引` `BM25` | 搜索/日志场景高频考点 |
| 18 | **类加载器：双亲委派模型、打破委派（Tomcat/Spi/OSGi）** | senior | `类加载器` `双亲委派` `Tomcat` | JVM 基础但追问深度大 |
| 19 | **Java 线程池：7 参数、Executors 缺陷、ForkJoinPool 工作窃取** | senior | `线程池` `ForkJoin` `拒绝策略` | 八股文经典，结合 Java 21 虚拟线程补充 |
| 20 | **Spring AI RAG：文档分块、Embedding、向量检索、重排序、落地边界** | architect | `Spring AI` `RAG` `向量检索` | 2026 AI 工程化新八股 |

### index.html 更新计划

#### Hero 统计区域变更
当前统计（4 列）：13 篇章 / 156 深度 Q&A / 60+ 技术图表 / 40 真实场景题

更新后统计（5 列）：
- **13** 篇章
- **156** 深度 Q&A
- **20** 八股文速查
- **40** 真实场景题
- **60+** 技术图表

#### 章节卡片区域变更
在 `chapter-grid` 中，**在场景题专篇之前**插入八股文卡片（全宽样式，与场景题卡片风格一致但颜色区分）：
```html
<a href="eight-part-questions.html" class="chapter-card" style="grid-column: 1 / -1; border-left: 4px solid var(--success);">
  <div class="card-number" style="color: var(--success);">八股文速查</div>
  <div class="card-title">高频八股文 20 题</div>
  <div class="card-desc">覆盖 Java 21、JVM、Spring、MySQL、Redis、分布式事务、Netty、Kafka、GC、熔断限流、HTTPS、ES、类加载器、线程池、Spring AI RAG 等 2026 头部大厂仍在考察的核心原理。每题采用「核心要点 + 详细解答 + 工程实践 + 高频追问」精炼结构，速查导向。</div>
  <div class="card-footer">
    <span>20 题</span>
    <div class="card-tags">
      <span class="difficulty difficulty-senior">高级 ×11</span>
      <span class="difficulty difficulty-architect">架构 ×9</span>
    </div>
  </div>
</a>
```

#### 标签云补充
在现有标签云中新增以下标签（使用 `.accent` 或 `.accent2` 高亮）：
`Java 21` `HashMap` `ConcurrentHashMap` `JMM` `三级缓存` `自动配置` `B+树` `Read View` `延迟双删` `Redisson` `Netty` `Kafka 零拷贝` `GC 演进` `令牌桶` `TLS 1.3` `倒排索引` `类加载器` `ForkJoinPool` `Spring AI RAG`

## Assumptions & Decisions

1. **复用设计系统**：完全复用现有 `design-system.css`，不新增或修改 CSS 文件，八股文专属样式以内联 `<style>` 形式写入新页面，确保样式隔离。
2. **结构差异化**：八股文采用四层紧凑结构，与深度 Q&A 的六层结构形成明显视觉和内容差异，避免用户感知重复。
3. **nav.js 兼容**：新页面复用现有 `nav.js` 导航逻辑，侧边栏 TOC、返回顶部、阅读进度条自动生效。
4. **Mermaid 支持**：每题可内嵌 Mermaid 图表（如线程模型、架构图），复用现有 Mermaid 初始化逻辑。
5. **选题去重原则**：20 道八股文与 156 道深度 Q&A 主题允许少量重叠，但内容必须精炼至 600~1000 字，聚焦标准应答话术，而非演进脉络。

## Verification Steps

1. **页面渲染验证**：本地打开 `eight-part-questions.html`，验证 20 道卡片样式、四层结构、代码块、表格、Mermaid 图表渲染正常。
2. **导航验证**：验证侧边栏 TOC 高亮、章节跳转、返回顶部按钮正常工作。
3. **响应式验证**：验证移动端（≤768px）下卡片布局、表格横向滚动、统计列折行正常。
4. **index 集成验证**：验证 index.html 新增八股文卡片可正常跳转，统计数字正确，标签云新增标签样式正确。
5. **链接完整性验证**：确认所有内部链接（index → eight-part-questions.html）无 404。
