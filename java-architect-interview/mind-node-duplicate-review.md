# java-architect-interview-mind 导图节点重复排查

> 节点定义：`details.map-card`（summary 标题 + map-body-text 描述 + map-tags 主题标签）与 mermaid `flowchart` 图节点。

> 核查文件数：18（含 index.html 总览）。

> 比对口径：节点文本做空白折叠+大小写归一后精确匹配；tags 按原样词频统计（跨文件出现 = 章节重复主题信号）。


## 0. 概览

- 节点（map-card）总数：**349**
- 文件内 summary 重复：0 处（涉及 0 文件）
- 文件内 body 重复：0 处
- 跨文件 summary 精确重复：2 个节点
- 跨文件 body 精确重复：0 个节点
- 跨文件重复主题（tags 出现在 ≥2 文件）：27 个
- mermaid 图内标签重复：1 处

## 1. 文件内节点重复

✅ 所有文件内 `details.map-card` 的 summary 与 body 均无精确重复。


## 2. 跨文件精确重复节点（同 summary / 同 body 出现在 ≥2 文件）

### 2.1 相同 summary

- `八股e11.03prometheus+grafana可观测` → mind-10-microservice-cloud.html#22、mind-11-middleware-engineering.html#25
- `八股e09.02https/tls1.3握手` → mind-13-network-io.html#13、mind-server-security-checkpoint.html#8

## 3. 跨文件重复主题（map-tags 词频，出现在 ≥2 个文件 = 章节主题交叉）

> 说明：`章节`/`八股`/`场景` 为节点**类别标签**（标识题目来源），几乎每篇都有，已在下方单独列出、不计入主题表；主题表只保留**实质性技术主题**词，直接用于反推章节题目重复主题。

### 3.0 类别标签覆盖（非主题，仅参考）

- `章节`：覆盖 15 个文件
- `八股`：覆盖 14 个文件
- `场景`：覆盖 11 个文件
### 3.1 实质性主题标签跨文件重复（共 **27** 个）

按出现文件数降序：

| 主题标签 | 出现文件数 | 涉及文件 | 代表节点（摘要） |
|---|---|---|---|
| 可观测 | 4 | 02-gc-performance、10-microservice-cloud、11-middleware-engineering、core-methodology | C02.12 GC/JVM 指标监控闭环 |
| 迁移 | 3 | 01-jvm-memory-classloading、11-middleware-engineering、12-ai-engineering | C01.10 JDK 17/21 新特性与升级迁移 |
| 日志 | 3 | 07-mysql-deep、core-methodology、server-security-checkpoint | C07.04 Redo/Undo/Binlog 如何协同保证 ACID |
| 限流熔断 | 3 | 10-microservice-cloud、12-ai-engineering、core-methodology | C10.03 高并发限流熔断降级策略 |
| OOM | 2 | 01-jvm-memory-classloading、02-gc-performance | C01.05 OOM 与内存泄漏的区别与排查 |
| GC Roots | 2 | 01-jvm-memory-classloading、02-gc-performance | C01.05 OOM 与内存泄漏的区别与排查 |
| 数据结构 | 2 | 01-jvm-memory-classloading、08-redis-cache | 八股 E12.01 常用数据结构选型与复杂度 |
| 排序 | 2 | 01-jvm-memory-classloading、09-distributed-systems | 八股 E12.05 排序算法复杂度与稳定性 |
| 演进 | 2 | 02-gc-performance、03-concurrency-locks | 八股 E02.01 GC 算法演进：Serial→Parallel→CM |
| WebFlux | 2 | 04-threadpool-virtual-threads、15-reactive | C04.07 响应式 vs 传统 Servlet 本质差异 |
| K8s | 2 | 06-spring-boot-modern、10-microservice-cloud | C06.12 优雅停机与 K8s 滚动发布协同 |
| 选型 | 2 | 06-spring-boot-modern、11-middleware-engineering | C06.13 云原生 Java：Quarkus/Micronaut vs |
| 高可用 | 2 | 07-mysql-deep、10-microservice-cloud | C07.09 MySQL 高可用方案选型 |
| 一致性 | 2 | 08-redis-cache、core-methodology | C08.04 缓存与数据库一致性如何保证 |
| 分布式锁 | 2 | 08-redis-cache、09-distributed-systems | C08.05 Redisson 分布式锁如何可重入与看门狗 |
| CAP | 2 | 09-distributed-systems、core-methodology | C09.01 CAP 定理证明与 BASE 理论指导实践 |
| 幂等 | 2 | 09-distributed-systems、core-methodology | C09.08 接口幂等设计如何实现 |
| Kafka | 2 | 09-distributed-systems、11-middleware-engineering | C09.04 Kafka 高吞吐/可靠投递/消息顺序 |
| 链路追踪 | 2 | 09-distributed-systems、core-methodology | C09.10 链路追踪与可观测性落地 |
| 配置中心 | 2 | 10-microservice-cloud、11-middleware-engineering | C10.01 注册发现与配置中心选型 |
| 零信任 | 2 | 10-microservice-cloud、core-methodology | C10.13 微服务安全与零信任 |
| OAuth | 2 | 11-middleware-engineering、server-security-checkpoint | C11.04 OAuth 2.1 三种授权模式与安全 |
| Spring AI | 2 | 12-ai-engineering、core-methodology | C12.01 Spring AI 核心架构与整合模式 |
| 合规 | 2 | 12-ai-engineering、server-security-checkpoint | C12.29~31 评测/灰度/合规 |
| 背压 | 2 | 12-ai-engineering、15-reactive | 场景 S12.07 流式 AI 并发背压与降级 |
| TLS | 2 | 13-network-io、server-security-checkpoint | C13.04 HTTPS/TLS 1.2 与 1.3 握手 |
| 威胁建模 | 2 | core-methodology、server-security-checkpoint | 安全开发生命周期 |

### 3.1 文件内 tags 自身重复（同标签在一文件多节点出现，多为合理聚焦）

- mind-01-jvm-memory-classloading.html：23 个文件内重复标签
- mind-02-gc-performance.html：14 个文件内重复标签
- mind-03-concurrency-locks.html：16 个文件内重复标签
- mind-04-threadpool-virtual-threads.html：13 个文件内重复标签
- mind-05-spring-core.html：14 个文件内重复标签
- mind-06-spring-boot-modern.html：15 个文件内重复标签
- mind-07-mysql-deep.html：29 个文件内重复标签
- mind-08-redis-cache.html：19 个文件内重复标签
- mind-09-distributed-systems.html：33 个文件内重复标签
- mind-10-microservice-cloud.html：33 个文件内重复标签
- mind-11-middleware-engineering.html：28 个文件内重复标签
- mind-12-ai-engineering.html：31 个文件内重复标签
- mind-13-network-io.html：19 个文件内重复标签
- mind-14-databases.html：9 个文件内重复标签
- mind-15-reactive.html：5 个文件内重复标签
- mind-core-methodology.html：7 个文件内重复标签
- mind-server-security-checkpoint.html：12 个文件内重复标签

## 4. mermaid 图内标签重复

- **mind-10-microservice-cloud.html**：`八股 高并发架构` ×2

## 附录：各文件节点数

- index.html：0 节点，mermaid 图标签 0
- mind-01-jvm-memory-classloading.html：19 节点，mermaid 图标签 21
- mind-02-gc-performance.html：17 节点，mermaid 图标签 21
- mind-03-concurrency-locks.html：17 节点，mermaid 图标签 21
- mind-04-threadpool-virtual-threads.html：14 节点，mermaid 图标签 18
- mind-05-spring-core.html：14 节点，mermaid 图标签 18
- mind-06-spring-boot-modern.html：15 节点，mermaid 图标签 18
- mind-07-mysql-deep.html：25 节点，mermaid 图标签 29
- mind-08-redis-cache.html：18 节点，mermaid 图标签 22
- mind-09-distributed-systems.html：29 节点，mermaid 图标签 32
- mind-10-microservice-cloud.html：31 节点，mermaid 图标签 38
- mind-11-middleware-engineering.html：29 节点，mermaid 图标签 27
- mind-12-ai-engineering.html：27 节点，mermaid 图标签 32
- mind-13-network-io.html：19 节点，mermaid 图标签 23
- mind-14-databases.html：11 节点，mermaid 图标签 15
- mind-15-reactive.html：6 节点，mermaid 图标签 10
- mind-core-methodology.html：44 节点，mermaid 图标签 48
- mind-server-security-checkpoint.html：14 节点，mermaid 图标签 18
