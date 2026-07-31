# Java 架构师面试问答 — 全面复核与补充实施计划

## 一、当前状态分析

### 1.1 精确题数统计

| 模块 | 文件 | 当前题数 |
|------|------|----------|
| 第1篇 JVM内存与类加载 | chapter-01 | 8 |
| 第2篇 GC算法与性能调优 | chapter-02 | 10 |
| 第3篇 并发编程与锁机制 | chapter-03 | 10 |
| 第4篇 线程池与虚拟线程 | chapter-04 | 8 |
| 第5篇 Spring核心原理 | chapter-05 | 10 |
| 第6篇 Spring Boot与现代框架 | chapter-06 | 10 |
| 第7篇 MySQL深度原理 | chapter-07 | 10 |
| 第8篇 Redis与缓存架构 | chapter-08 | 10 |
| 第9篇 分布式系统 | chapter-09 | 10 |
| 第10篇 微服务与云原生 | chapter-10 | 10 |
| 第11篇 中间件与工程化 | chapter-11 | 10 |
| 第12篇 AI工程与实践 | chapter-12 | 10 |
| **12篇深度Q&A小计** | — | **116** |
| 八股文速查 | eight-part-questions.html | 20 |
| 场景题专篇 | scenario-questions.html | 40 |
| **总计** | — | **176** |

**上限256，余80题空间。**

### 1.2 盲区矩阵（按2026大厂面试要求）

| 盲区领域 | 现有覆盖 | 缺失深度 | 面试高频度 | 优先级 |
|----------|----------|----------|------------|--------|
| **网络与IO** | 仅NIO(1.6)、Netty八股(1题) | 无专门章节；TCP/IP、HTTP/2/3、DNS、WebSocket、零拷贝深度缺失 | 极高 | P0 |
| **消息队列多样性** | 只有Kafka深度(9.4) | 无RocketMQ/RabbitMQ/Pulsar深入专题；无MQ选型对比 | 高 | P0 |
| **Elasticsearch** | 八股文倒排索引(1题) | 无分片机制、查询优化、ES与MySQL协同、冷热分离 | 高 | P0 |
| **DDD领域驱动设计** | 10.6/S15顺带提及 | 无限界上下文、聚合根、领域事件、CQRS深入 | 高 | P1 |
| **Zookeeper** | 9.3分布式锁对比有提及 | 无ZAB协议、Watcher机制、Leader选举专题 | 中 | P1 |
| **Netty深度** | 八股文EPQ-12(1题) | 无线程模型、ByteBuf内存池、ChannelPipeline深入 | 高 | P1 |

### 1.3 质量评估

- 内容深度：A（六层结构完整，演进脉络清晰）
- 设计一致性：A（统一CSS、TOC、导航、难度标签）
- 技术时效性：A（覆盖Java 21、GraalVM、Spring AI、OpenTelemetry）
- **知识覆盖完整性：B+（网络IO、DDD、ES、ZK、MQ多样性存在盲区）**

---

## 二、补充方案

### 2.1 总体题数分配

| 补充类型 | 新增题数 | 说明 |
|----------|----------|------|
| **新增完整Chapter** | **10题** | 第13篇：网络与高性能IO |
| **现有Chapter扩充** | **15题** | Ch09+5(MQ/ZK/链路追踪)、Ch10+5(DDD/架构演进)、Ch11+3(ES/gRPC)、Ch07+1(MySQL+ES)、Ch08+1(缓存+搜索) |
| **场景题扩充** | **15题** | 新增"网络与IO架构"(5题)、"搜索引擎与大数据"(5题)；现有类别补充(5题) |
| **八股文扩充** | **20题** | 覆盖新增章节与盲区的高频速查题 |
| **合计新增** | **60题** | **总题数从176提升至236题，余20题空间用于后续微调** |

### 2.2 新增/修改文件清单

| 序号 | 文件路径 | 变更类型 | 说明 |
|------|----------|----------|------|
| 1 | `chapter-13-network-io.html` | **新建** | 第13篇：网络与高性能IO（10题） |
| 2 | `chapter-09-distributed-systems.html` | **编辑扩充** | 新增Q9.11~Q9.15（5题） |
| 3 | `chapter-10-microservice-cloud.html` | **编辑扩充** | 新增Q10.11~Q10.15（5题） |
| 4 | `chapter-11-middleware-engineering.html` | **编辑扩充** | 新增Q11.11~Q11.13（3题） |
| 5 | `chapter-07-mysql-deep.html` | **编辑扩充** | 新增Q7.11（1题） |
| 6 | `chapter-08-redis-cache.html` | **编辑扩充** | 新增Q8.11（1题） |
| 7 | `scenario-questions.html` | **编辑扩充** | 新增S41~S55（15题），新增第十、十一分组 |
| 8 | `eight-part-questions.html` | **编辑扩充** | 新增EPQ-21~EPQ-40（20题） |
| 9 | `index.html` | **编辑** | 更新统计数字、新增第13篇卡片、更新标签云、更新场景题描述 |

---

## 三、新增题目详细清单

### 3.1 新增Chapter 13：网络与高性能IO（10题）

| 编号 | 难度 | 问题标题 | 核心要点 |
|------|------|----------|----------|
| 13.1 | 高 | OSI七层与TCP/IP四层模型如何映射？各层核心协议与数据封装过程？ | 五层/七层/四层对比；各层PDU；ARP/IP/TCP/HTTP位置；**从OSI到TCP/IP到QUIC的演进** |
| 13.2 | 高 | TCP三次握手与四次挥手完整状态机？TIME_WAIT与CLOSE_WAIT根因？ | SYN/ACK/FIN状态转换；2MSL；**TCP从Tahoe到Reno到CUBIC到BBR的拥塞控制演进**；滑动窗口 |
| 13.3 | 高 | HTTP/1.1 vs HTTP/2 vs HTTP/3核心差异与选型依据？ | 队头阻塞、多路复用、HPACK/QPACK、QUIC基于UDP、**HTTP演进时间线** |
| 13.4 | 高 | HTTPS/TLS 1.2与1.3握手流程差异？证书链验证与前向安全？ | RSA vs ECDHE密钥交换；证书链；OCSP Stapling；**TLS 1.0→1.3演进**；Session Resumption |
| 13.5 | 架 | Java NIO核心原理：Selector、Channel、Buffer如何协同工作？ | Reactor模式；IO多路复用(epoll/kqueue)；**从BIO到NIO到AIO的演进**；DirectByteBuffer |
| 13.6 | 架 | Netty线程模型与ChannelPipeline设计哲学？ | EventLoopGroup(Boss/Worker)；单线程EventLoop；Pipeline Handler链；**Netty vs Tomcat线程模型对比** |
| 13.7 | 专 | Netty内存管理：ByteBuf池化、引用计数与内存泄漏排查？ | PooledByteBufAllocator；jemalloc算法(tiny/small/normal/huge)；引用计数；ResourceLeakDetector |
| 13.8 | 架 | 零拷贝技术深度：sendfile、mmap、DMA在Java中的实现？ | 传统4次拷贝→sendfile 2次→mmap；**Java FileChannel.transferTo**；Netty CompositeByteBuf |
| 13.9 | 高 | WebSocket握手、心跳与断线重连如何设计？ | Upgrade握手；Ping/Pong帧；**从轮询到长轮询到SSE到WebSocket的演进**；Netty实现 |
| 13.10 | 高 | DNS解析原理与智能调度：递归/迭代查询、HTTPDNS、CDN调度？ | DNS层级；TTL缓存；**DNS劫持与HTTPDNS绕过**；GSLB全局负载均衡；EDNS Client Subnet |

### 3.2 现有Chapter扩充（15题）

**Chapter-09 分布式系统（+5题）**

| 编号 | 难度 | 问题标题 | 核心要点 |
|------|------|----------|----------|
| 9.11 | 架 | RocketMQ架构深度：NameServer、Broker、事务消息与延迟消息？ | 无NameServer设计；CommitLog+ConsumeQueue；事务消息半消息+回查；延迟消息18级时间轮 |
| 9.12 | 高 | RabbitMQ核心：AMQP协议、Exchange路由类型与死信队列？ | Direct/Topic/Fanout/Headers；DLX+TTL；镜像队列；**RabbitMQ vs Kafka场景选型** |
| 9.13 | 架 | Pulsar存算分离架构：BookKeeper、多租户与Geo-Replication？ | Broker无状态+BookKeeper分层存储；**Pulsar vs Kafka架构差异**；跨地域复制 |
| 9.14 | 架 | Zookeeper深入：ZAB协议、Watcher机制与Leader选举？ | ZAB崩溃恢复+消息广播；znode类型；Watcher一次性；**ZK vs etcd选型** |
| 9.15 | 高 | 分布式链路追踪原理：TraceId/SpanId、SkyWalking vs Zipkin？ | OpenTracing规范；baggage透传；采样策略；**从Zipkin到SkyWalking到OpenTelemetry演进** |

**Chapter-10 微服务与云原生（+5题）**

| 编号 | 难度 | 问题标题 | 核心要点 |
|------|------|----------|----------|
| 10.11 | 架 | DDD战略设计：限界上下文、上下文映射与通用语言？ | Bounded Context；Context Map（合作伙伴/共享内核/防腐层）；Ubiquitous Language；**DDD与微服务边界对应** |
| 10.12 | 架 | DDD战术设计：实体、值对象、聚合根与资源库？ | Entity vs Value Object；Aggregate Root不变量；Domain Service；Repository vs DAO |
| 10.13 | 专 | 领域事件与CQRS：事件存储、读写分离与最终一致性？ | Domain Event；Event Store；CQRS读写分离；**Eventual Consistency与CAP权衡** |
| 10.14 | 专 | 事件溯源与Saga：状态重建、补偿事务与长事务处理？ | Event Sourcing；Saga编排与编排；补偿事务；**与2PC/TCC的互补关系** |
| 10.15 | 架 | 架构演进模式：绞杀者模式、模块化单体与数据库先行？ | Strangler Fig Pattern；Modular Monolith；**单体→模块化单体→微服务的渐进演进**；数据耦合处理 |

**Chapter-11 中间件与工程化（+3题）**

| 编号 | 难度 | 问题标题 | 核心要点 |
|------|------|----------|----------|
| 11.11 | 架 | Elasticsearch核心：倒排索引、分片机制与近实时搜索？ | Inverted Index；Segment与Merge；Shard/Replica；Refresh/Flush；**ES与MySQL索引本质差异** |
| 11.12 | 架 | ES搜索性能优化：分片策略、冷热分离与查询缓存？ | 分片数=节点数×1~3；ILM索引生命周期；Filter Cache；Routing优化；**ES容量规划** |
| 11.13 | 高 | gRPC与Protobuf：HTTP/2流式RPC、序列化与服务定义？ | .proto语法；HTTP/2多路复用；Unary/Streaming RPC；**gRPC vs REST vs GraphQL选型** |

**Chapter-07 MySQL深度原理（+1题）**

| 编号 | 难度 | 问题标题 | 核心要点 |
|------|------|----------|----------|
| 7.11 | 架 | MySQL与Elasticsearch双写一致性如何保证？ | Canal订阅Binlog；MQ异步同步；**双写方案对比**；数据异构与最终一致 |

**Chapter-08 Redis与缓存（+1题）**

| 编号 | 难度 | 问题标题 | 核心要点 |
|------|------|----------|----------|
| 8.11 | 架 | 缓存与搜索引擎协同：Redis+ES多级查询架构设计？ | 热点数据Redis缓存+全量ES搜索；缓存预热；**搜索缓存一致性**；降级策略 |

### 3.3 场景题扩充（15题）

**新增类别十：网络与IO架构（5题）**

| 编号 | 难度 | 场景题标题 | 重叠技术栈 |
|------|------|------------|------------|
| S41 | 架 | 百万级长连接IM网关设计 | Netty + WebSocket + 心跳 + 分布式路由 |
| S42 | 架 | 实时音视频信令与媒体转发系统 | WebSocket + UDP + QoS + 全球加速 |
| S43 | 高 | 大文件分片上传与断点续传 | HTTP/HTTPS + 分片 + 秒传 + 合并 |
| S44 | 高 | DNS故障排查与HTTPDNS落地 | DNS + HTTPDNS + CDN + 智能调度 |
| S45 | 架 | 全站HTTPS迁移与性能优化 | TLS 1.3 + OCSP + HSTS + 证书管理 |

**新增类别十一：搜索引擎与大数据（5题）**

| 编号 | 难度 | 场景题标题 | 重叠技术栈 |
|------|------|------------|------------|
| S46 | 架 | 亿级商品搜索系统设计 | ES + Redis + 分词 + 聚合 + 推荐 |
| S47 | 架 | 日志采集与ELK实时分析架构 | Filebeat + Logstash + ES + Kibana |
| S48 | 高 | 海量数据实时聚合统计 | ClickHouse/ES + 预聚合 + 物化视图 |
| S49 | 架 | 个性化推荐系统架构 | 召回 + 排序 + 特征工程 + AB测试 |
| S50 | 架 | 数据仓库与实时数仓选型 | Hive/ClickHouse/Flink + 离线/实时链路 |

**现有类别补充（5题）**

| 编号 | 类别 | 难度 | 场景题标题 | 重叠技术栈 |
|------|------|------|------------|------------|
| S51 | 高并发 | 专 | 12306高并发抢票系统设计 | 库存分桶 + 异步队列 + 限流 + 降级 |
| S52 | 分布式 | 架 | 分布式任务调度平台设计 | XXL-Job/ElasticJob + 分片 + 故障转移 |
| S53 | 微服务 | 架 | 多租户SaaS平台架构设计 | 数据隔离 + 配置隔离 + 资源配额 + 灰度 |
| S54 | 性能 | 架 | 全链路压测与容量规划 | 影子库 + 流量复制 + 瓶颈定位 + 扩缩容 |
| S55 | 综合 | 架 | 开放平台API网关与安全设计 | OAuth2 + 限流 + 签名 + 审计 + SDK |

### 3.4 八股文扩充（20题）

| 编号 | 难度 | 问题标题 | 知识点标签 |
|------|------|----------|------------|
| EPQ-21 | 高 | TCP三次握手与四次挥手完整状态机 | TCP / 状态机 / TIME_WAIT |
| EPQ-22 | 高 | HTTP/2多路复用与HTTP/3 QUIC协议 | HTTP/2 / HTTP/3 / QUIC |
| EPQ-23 | 高 | Java NIO Selector与Reactor模式 | NIO / Selector / Reactor |
| EPQ-24 | 架 | Netty ByteBuf内存池与引用计数 | Netty / ByteBuf / 内存池 |
| EPQ-25 | 高 | 零拷贝sendfile与mmap原理 | 零拷贝 / sendfile / mmap |
| EPQ-26 | 架 | RocketMQ事务消息与顺序消息原理 | RocketMQ / 事务消息 / 顺序消息 |
| EPQ-27 | 高 | RabbitMQ Exchange路由与死信队列 | RabbitMQ / AMQP / 死信队列 |
| EPQ-28 | 高 | Zookeeper Watcher与临时节点机制 | ZK / Watcher / ZAB |
| EPQ-29 | 高 | Elasticsearch分词器与倒排索引查询 | ES / 分词 / 倒排索引 |
| EPQ-30 | 架 | DDD限界上下文与聚合根设计 | DDD / 限界上下文 / 聚合根 |
| EPQ-31 | 架 | 服务网格Istio Sidecar模式原理 | Service Mesh / Istio / Sidecar |
| EPQ-32 | 高 | gRPC vs REST vs GraphQL性能对比 | gRPC / Protobuf / HTTP/2 |
| EPQ-33 | 高 | DNS解析原理与智能调度 | DNS / CDN / HTTPDNS |
| EPQ-34 | 高 | 数据库连接池HikariCP原理 | HikariCP / 连接池 / 性能 |
| EPQ-35 | 高 | 分布式Session共享方案对比 | Session / Redis / JWT |
| EPQ-36 | 高 | WebSocket握手与心跳设计 | WebSocket / 长连接 / 心跳 |
| EPQ-37 | 架 | 一致性协议Paxos vs Raft vs ZAB | Paxos / Raft / ZAB |
| EPQ-38 | 架 | 容器网络CNI与Calico/Flannel | K8s / CNI / 容器网络 |
| EPQ-39 | 高 | Protobuf序列化与Schema演进 | Protobuf / 序列化 / 版本兼容 |
| EPQ-40 | 架 | 多级缓存与搜索协同架构 | Redis / ES / 多级缓存 |

---

## 四、实施步骤与优先级

### Phase 1：新增章节（P0）

**步骤1：新建 `chapter-13-network-io.html`**
- 复用现有设计系统（`assets/design-system.css` + `_shared/`资源）
- 10道Q&A严格遵循六层结构
- 侧边栏TOC + 章节头部元信息 + 章节间导航
- 难度分布：高×4 / 架×4 / 专×2

**步骤2：更新 `index.html`**
- Hero统计区：深度Q&A 116→131，篇章12→13，场景题40→55，八股文20→40
- 插入第13篇卡片
- 标签云新增网络IO相关标签

### Phase 2：现有Chapter扩充（P0-P1）

**步骤3：扩充 chapter-09（+5题）**
- 在Q9.10后插入Q9.11~Q9.15
- 更新TOC、头部统计（10→15题）

**步骤4：扩充 chapter-10（+5题）**
- 在Q10.10后插入Q10.11~Q10.15
- 更新TOC、头部统计（10→15题）

**步骤5：扩充 chapter-11（+3题）**
- 在Q11.10后插入Q11.11~Q11.13
- 更新TOC、头部统计（10→13题）

**步骤6：扩充 chapter-07（+1题）**
- 在Q7.10后插入Q7.11
- 更新TOC、头部统计（10→11题）

**步骤7：扩充 chapter-08（+1题）**
- 在Q8.10后插入Q8.11
- 更新TOC、头部统计（10→11题）

### Phase 3：场景题与八股文扩充（P1）

**步骤8：扩充 `scenario-questions.html`**
- 新增第十组（网络IO 5题）、第十一组（搜索大数据 5题）
- 插入S41~S55
- 更新TOC、头部统计

**步骤9：扩充 `eight-part-questions.html`**
- 插入EPQ-21~EPQ-40
- 更新TOC、头部统计

### Phase 4：全量验证（P2）

**步骤10：全站验证**
- 浏览器打开index.html验证13篇链接可达
- 逐篇检查Mermaid图渲染、代码块、响应式
- 验证TOC跳转、统计数字、章节间导航
- 验证题数统计准确性

---

## 五、验证方案

### 5.1 结构验证

| 验证项 | 验证方法 | 通过标准 |
|--------|----------|----------|
| 题数统计 | grep统计各文件qa-card/epq-card | ch13=10; ch09=15; ch10=15; ch11=13; ch07=11; ch08=11; 场景=55; 八股=40 |
| 首页统计 | 检查index.html Hero区 | 深度Q&A=131; 八股文=40; 场景题=55; 篇章=13 |

### 5.2 内容质量验证

| 验证项 | 验证方法 | 通过标准 |
|--------|----------|----------|
| 六层结构完整性 | 抽查新增题目 | 每题均含：本质/演进/原理/实践/追问/陷阱 |
| 盲区填补确认 | 搜索新增文件关键词 | Netty/DNS/HTTP3/DDD/ZAB/RocketMQ/ES分词等均有独立题目 |

### 5.3 设计一致性验证

| 验证项 | 验证方法 | 通过标准 |
|--------|----------|----------|
| CSS复用 | 确认未修改design-system.css | 完全复用现有设计系统 |
| 响应式 | 浏览器DevTools多尺寸测试 | 侧边栏折叠、卡片布局、表格滚动正常 |
| 链接与导航 | 点击测试 | 首页跳转、章节间导航、TOC跳转均正确 |

---

## 六、关键决策

| 决策项 | 选择 | 理由 |
|--------|------|------|
| 新增章节 vs 全部分散 | **新增1个完整Chapter（网络IO）** | 网络IO内容量大、主题独立、大厂面试极高频，独立成章更符合知识体系 |
| ES/MQ/ZK/DDD归属 | **分散到现有Chapter扩充** | ES归中间件、MQ/ZK归分布式、DDD归微服务，保持章节主题聚焦 |
| 场景题新增类别 | **新增2个类别（网络IO+搜索大数据）** | 2026面试中网络架构和搜索场景高频出现 |
| 八股文扩充至40题 | **新增20题** | 速查导向，覆盖新增章节和盲区的核心高频点 |
| 总题数236 vs 256 | **保留20题余量** | 避免为填满而降低质量；余量用于后续新趋势补充 |
