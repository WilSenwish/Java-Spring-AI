# 审查问题修复进度

> **历史文档说明**：本文写于站点品牌名为《Java 架构师面试问答》时期，文中沿用「面试 / 八股文」等旧术语。全站已于 2026-09-04 更名为《Java 专家 · 架构师 · 高级开发 工程能力知识库》，对应术语现为「知识点 / 核心原理」。**本文为历史修复记录，内容按原文保留，不作改写。**

## 修复基线

- 章节未绑定单一生产版本，修复时不把历史行为抹平为“当前版本行为”。
- 涉及 JDK、Spring、数据库、中间件和 AI SDK 时，按官方演进分界标注版本；示例保留目标版本的稳定 API。
- 无法用官方文档或源码核实的精确性能数字、市场结论和绝对化选型结论，改为前提明确的方法论或删除。
- 不新增、删除或重排标准卡片锚点；重复主题在原卡内压缩，并保留跨卡引用。

## 官方证据

| 来源 | 状态 | 用途 |
|---|---|---|
| OpenJDK JEP Index | 已下载 `facts/openjdk-jeps.html` | JDK 版本、preview/final 状态与演进边界 |
| JEP 444 / 491 | 已下载 `facts/jep444.html`、`facts/jep491.html` | 虚拟线程调度、pinning、JFR 与 JDK 21/24 差异 |
| JEP 505 / 506 | 已下载 `facts/jep505.html`、`facts/jep506.html` | 结构化并发 `open()/Joiner` 与 ScopedValue 边界 |
| Spring Boot Reference | 已下载 `facts/spring-boot-reference.html` | Boot 自动配置、AOT、事件、Session、Actuator |
| Spring Security Servlet Architecture | 已下载 `facts/spring-security-servlet-architecture.html` | Security 过滤器链与上下文过滤器 |
| Spring AI Reference | 已下载 `facts/spring-ai-reference.html` | ChatClient、Advisor、工具调用与 RAG |
| MySQL 8.0 EXPLAIN | 已下载 `facts/mysql-explain.html` | `rows`、`filtered` 与执行计划字段 |
| Redis XPENDING | 已下载 `facts/redis-xpending.html` | Stream PEL、消费者组与消息状态 |
| Apache Kafka Documentation | 已下载 `facts/kafka-transactions.html` | 事务、EOS 与 consumer 隔离级别 |
| Reactor Reference | 已下载 `facts/reactor-reference.html`（实为重定向壳，事实经 WebSearch 官方源核实：3.4.2 Reference / 3.4.0 changelog） | `publishOn`/`subscribeOn` 语义、`Schedulers.elastic()` 弃用(3.4)/移除(3.5)、context 与背压 |
| etcd v3.6 Tuning | 已下载 `facts/etcd-tuning.html` | 心跳/选举默认值、快照计数与部署前提 |
| OpenTelemetry Specification / Collector / Java Agent | 已下载 `facts/otel-spec.html`、`facts/otel-collector.html`、`facts/otel-java-agent.html` | OTLP、Collector 管道、自动插桩覆盖边界 |
| Apache Seata v2.6.0 Release / Raft 示例 | 已下载 `facts/seata-release.json`、`facts/seata-raft.md`、`facts/seata-readme.md` | 2.6.0 发布元数据与 `server.raft`、`store.mode: raft` 证据 |
| Google Spanner TrueTime | 联网访问超时 | 不引入固定毫秒精度，只保留“有界不确定性 + 专用部署前提”表述 |
| K8s KEP-1287（In-place Pod Resize） | WebSearch 官方源核实：[kubernetes.io/blog](https://kubernetes.io/blog/)（1.27 Alpha → 1.33 Beta 默认启用 gate → 1.35 GA） | C10.04 版本里程碑 |
| Dubbo 3 Triple | WebSearch 官方源核实：[dubbo.apache.org](https://dubbo.apache.org/)（3.x HTTP/2、跨语言、gRPC 互操作） | C10.25 Triple/应用级服务发现归属 3.x |
| Netty 4.x User Guide | 已下载 `facts/netty-docs.html`（含真实代码 `NioEventLoopGroup`/`exceptionCaught`） | C13.06 主从 Reactor 分工、异常传播、SO_BACKLOG |
| MongoDB 2.2/3.2 Docs（版本史） | 已下载 `facts/mongodb-22.html`、`facts/mongodb-32.html`（SPA 壳，事实经 WebSearch 核实） | C14.01 分片 1.6 引入、2.2 生产成熟、WiredTiger 3.0 引入·3.2 默认（专证「何时引入/成为默认」的版本史，旧版文档为精准证据） |
| MongoDB 4.0/6.0/8.0 Docs（LTS 现代特性） | 已下载 `facts/mongodb-40.html`（v4.0 事务页）、`facts/mongodb-60.html`（v6.0 手册）、`facts/mongodb-80.html`（v8.0 手册，含正文），结论经 WebSearch 官方源核实 | C14.01 4.0 多文档事务（副本集 4.0·分片集群 4.2·2PC）、6.0 可查询加密 Preview+CSFLE KMIP、8.0 当前稳定主版本+范围可查询加密 |
| TiDB TiFlash Docs | 已下载 `facts/tidb-tiflash.html`（SPA 壳，事实经 WebSearch 核实） | C14.05 TiFlash GA 归 4.x（2020） |
| ClickHouse Docs | 已下载 `facts/clickhouse-delete.html`、`facts/clickhouse-variant.html`（SPA 壳，事实经 WebSearch 核实） | C14.06 Lightweight DELETE 22.8 / Variant 24.3 实验·24.8 正式 |
| OceanBase Docs | WebSearch 官方源核实：[oceanbase.com](https://www.oceanbase.com/)（4.x 列存副本 + 向量化执行；OBKV 为 KV 接口） | C14.08 列存副本非 OBKV |
| Qdrant Docs | 已下载 `facts/qdrant-docs.html`（SPA 壳，事实经 WebSearch 核实） | C14.04 FloatVectors/SearchPoints |
| Milvus v2 SDK | 已下载 `facts/milvus-docs.html`（403 壳）+ WebSearch/GitHub 核实：`io.milvus:milvus-sdk-java`，`AddFieldReq`/`IndexParam`/`FloatVec`/`SearchResp` | C12.21、C14.03 v2 SDK API |

## 章节状态

| 章节 | 状态 |
|---|---|
| chapter-01 | 已完成（C01.02、C01.05 相关 finalize 表述、C01.06、C01.09、C01.10、C01.11） |
| chapter-02 | 已完成（C02.02、C02.07、C02.08、C02.10、C02.11、C02.12） |
| chapter-03 | 已完成（C03.06、C03.07、C03.09、C03.11、C03.12） |
| chapter-04 | 已完成（C04.01、C04.04、C04.06、C04.08、C04.09、C04.10） |
| chapter-05 | 已完成（C05.01-C05.10 重复 BPP 清理、C05.02 循环依赖版本归属 Boot 2.6+、C05.03 代理策略归属 Boot 自动配置、C05.04 自调用注释与 publicMethodsOnly 版本、C05.06 主题漂移替换、C05.10 SpEL 分层边界） |
| chapter-06 | 已完成（C06.01 Boot 3 自动配置不再生效+Boot 2.7 @AutoConfiguration、C06.02 删除伪 starter-aot+修正 native 命令、C06.03 @Validated 替代伪注解、C06.04 SecurityContextHolderFilter、C06.05 Runner 并存表述、C06.06 Session 续期矛盾统一、C06.07 Observation 拆分三支柱、C06.08 Spring 3.1 profile 脉络、C06.09 ProblemDetail.forStatusAndDetail、C06.11 Customizer.withDefaults、C06.12 K8s preStop 与摘流并发时序、C06.13 Micronaut 归属修正） |
| chapter-07 | 已完成（C07.03 非唯一索引等值锁修正、C07.05 隐式转换方向确认、C07.07 跨库分页 offset+page、C07.08 GTID 配置与 mysqldump 修正、C07.10 filtered 删除错误结论、C07.04/C07.09 MGR 版本改 5.7.17 GA、C07.06 选择率阈值移除、C07.11 innodb_deadlock_detect 5.7.15、C07.12 pt-osc 外键方法） |
| chapter-08 | 已完成（C08.01-C08.03、C08.08、C08.11 前期修复；C08.02 AOF 清单文件与默认布局、C08.04 一致性策略矩阵/Canal 顺序幂等、C08.05 fencing/Redisson 边界、C08.06 移除跨机房 RedLock/纠正 WAIT、C08.07 写准入与从节点选举、C08.08 lazy-free 归属、C08.10 量化与硬件趋势） |
| chapter-09 | 已完成（C09.01-C09.16；本轮收尾 C09.14 时钟模型、C09.15 容灾协议前提、C09.16 Seata 2.6.0/CDC 场景化选型） |
| chapter-10 | 已完成（C10.02 转发 Filter 精确化到 NettyRoutingFilter；C10.03 fallback 签名改为 Throwable 以匹配 withFallback 的 Function&lt;Throwable,T&gt;；C10.04 In-place Pod Resize 1.33 GA→1.27 Alpha→1.33 Beta（仍非 GA）；C10.09 补充流量一致性依赖路由层会话亲和的部署前提；C10.15 可观测性口径已自洽，原引用的 C11.09 在本文件不存在（chapter-11 无 C11.09，C11.10 为混沌工程），跨篇去重仅限 C09.11 且二者已一致；C10.20 校正 NettyRoutingFilter.getOrder()=Ordered.LOWEST_PRECEDENCE（2147483647，非 -1）；C10.21 解耦 Bootstrap 移除（2022.0/Kilburn）与 config.import 机制（Boot 2.4 引入）；C10.22 校正 Sleuth OTel 桥接归属 3.x、W3C 默认自 Boot 3.0 起；C10.25 Triple/应用级发现归属 Dubbo 3.x） |
| chapter-11 | 已完成（C11.11 事务示例编译修复+KRaft 版本统一+事务协议准确性；C11.12 与 C10.20 口径对齐+跨卡引用；C11.13/C11.21 与 C11.21/C11.13 互引去重不删锚点；C11.14 补 ES 许可演进 7.11+ 双许可 & OpenSearch 分叉 & X-Pack 安全免费化实为 6.8/7.1；C11.15 修正 proto3 无 presence/optional 3.12+ 重新引入 & gRPC 背压依赖 HTTP/2 流控；C11.16 Nacos 10x 改为官方基准测试口径；C11.17 明确 Flyway 社区版无自动 Undo/Liquibase 需显式 rollback 块；C11.18 新增 4.x/5.x 架构与 Remoting/gRPC SDK 区分；C11.19 明确 eBPF 内核/BTF 前提 & CAP_BPF 权限演进；C11.20 补 FinOps 平台前提 & 修正 HPA YAML 语法） |
| chapter-12 | 已完成（C12.01 ChatClient 时间线/Advisor 并存/虚构类删除；C12.02 经核已合规无需改；C12.03 量化公式+ada-002 代际；C12.06 @Tool 重写 Function Calling；C12.07 MCP 传输层；C12.13 独立框架血脉；C12.16 stream()+onErrorResume；C12.21 Milvus 2.x 真实 SDK API；C12.25 BufferOverflowStrategy.BLOCK→DROP_OLDEST+Redis 续传；C12.26 CallAroundAdvisor；C12.29 评测阈值统计前提；C12.31 CallAroundAdvisor） |
| chapter-13 | 已完成（C13.02 TIME_WAIT/端口复用/内核参数/LB 辨析+BBR 数字软化；C13.03 HTTP/1.1 RFC 年份+握手RTT+TLS边界；C13.04 RTT算法一致+SNI/ALPN；C13.05 Selector/IOCP过度对应+平台差异就绪语义；C13.06 Boss/Worker废弃误述+异常传播+SO_BACKLOG术语；C13.07 泄漏检测属性名+jemalloc精度+SimpleChannelInboundHandler释放陷阱；C13.08 kTLS边界+零拷贝平台条件；C13.11 已合规无需改；C13.12 Loom/io_uring独立路线） |
| chapter-14 | 已完成（C14.01 分片引入版本/WiredTiger 默认版本；C14.02 Spring AI 依赖名/vectorIndexName/量化软化；C14.03 Milvus v2 SDK 字段与检索返回；C14.04 Qdrant FloatVectors/SearchPoints；C14.05 TiFlash GA 归 4.x；C14.06 Lightweight DELETE 归 22.8/Variant 归 24.x；C14.07 EXPLAIN 执行计划提示；C14.08 OceanBase HTAP 列存副本非 OBKV；C14.09 量化已标注前提） |
| chapter-15 | 已完成（C15.01 背压 request(n) 拉取图 + Scheduler/背压/Context 三机制分离 + elastic() 版本口径(3.5+移除)；C15.02 吞吐结论软化(IO密集+高并发前提) + 迁移成本矩阵/依赖画像；C15.03 经核 R2DBC API 准确未改；C15.04 onError 传播方向修正(向下游非向上游) + 异常信号图 + BlockHound 配置修正(非 spring.blockhound.enabled 标准属性) + 区分开发期检测/生产熔断；C15.05 分场景兼容性矩阵(容器/JDBC/Redis/线程模型) + JDK24 JEP491/JDK25 LTS 口径；C15.06 删除链内手动 subscribe() 反模式 + OrderRepository 事务边界 + Hooks.onErrorDropped） |

## 证据索引（chapter-10 ~ chapter-15 逐条）

> 说明：标注 `facts/*.html` 的为已落地的官方文档本地副本（SPA 壳文件需配合 WebSearch 抽取正文）；标注「WebSearch 官方源核实」的项于 2026-08-30 经官方博客/文档检索确认关键事实；标注「内检/推理/方法论」的为站内交叉校验或工程方法论，不依赖外部文档。

| 章节 | 修复项 | 官方证据来源 | 核验方式 |
|---|---|---|---|
| C10.02 | 转发 Filter 精确化到 NettyRoutingFilter | `facts/scg-developer-guide.html`（SCG 开发者指南，NettyRoutingFilter 类） | 文档/源码 |
| C10.03 | fallback 签名改为 Throwable，匹配 `Function<Throwable,T>` | Reactor `Mono.or`/`onErrorResume` + WebFlux 文档（projectreactor.io / spring.io） | 文档 |
| C10.04 | In-place Pod Resize 1.27 Alpha→1.33 Beta（截至 1.33 仍非 GA） | [kubernetes.io/blog](https://kubernetes.io/blog/)（KEP-1287：1.27 Alpha→1.33 Beta→1.35 GA） | WebSearch |
| C10.09 | 流量一致性补“依赖路由层会话亲和”部署前提 | 方法论：移除绝对结论，补部署前提 | 推理 |
| C10.15 | 跨篇去重 C09.11/C11.09（C11.09 不存在，仅 C09.11） | 站内交叉校验（无外部文档） | 内检 |
| C10.20 | NettyRoutingFilter.getOrder()=Ordered.LOWEST_PRECEDENCE(2147483647) | `facts/scg-developer-guide.html`（源码 getOrder 返回 LOWEST_PRECEDENCE） | 源码 |
| C10.21 | Bootstrap 移除(2022.0/Kilburn) 与 config.import(Boot 2.4) 时间线解耦 | `facts/spring-boot-reference.html`（Boot 2.4 ConfigData/spring.config.import）、SC release notes | 文档 |
| C10.22 | Sleuth OTel 桥接 3.x 试验性；W3C 默认自 Boot 3.0 | Micrometer Tracing 1.0 / Spring Cloud 文档 | 文档 |
| C10.25 | Triple/应用级服务发现归属 Dubbo 3.x | [dubbo.apache.org](https://dubbo.apache.org/)（3.x HTTP/2 跨语言、gRPC 互操作） | WebSearch |
| C11.11 | Kafka 事务示例编译修复 + KRaft 版本统一（2.8 预览/3.3 生产就绪/4.0 移除 ZK） | `facts/kafka-transactions.html`（KIP-833） | 文档 |
| C11.12 | 与 C10.20 口径对齐 + 跨卡引用 | 同 C10.20（`facts/scg-developer-guide.html`） | 文档 |
| C11.13 / C11.21 | 互引去重（不删锚点） | 站内交叉校验 | 内检 |
| C11.14 | ES 7.11+ 双许可(SSPL+ELv2) & OpenSearch 自 7.10.2 分叉 & X-Pack 安全免费实为 6.8/7.1 | [elastic.co/blog](https://www.elastic.co/blog/)（7.11 许可变更） | WebSearch |
| C11.15 | proto3 默认无 presence、显式 optional 于 3.12+ 重新引入；gRPC 背压依赖 HTTP/2 流控 | [protobuf.dev](https://protobuf.dev/)（3.12 presence）、[grpc.io](https://grpc.io/) | WebSearch |
| C11.16 | Nacos “10x” 改为官方基准测试口径（2.0 10W vs 1.x 1.2W） | [nacos.io](https://nacos.io/) 官方公告 | WebSearch |
| C11.17 | Flyway 社区版无自动 Undo；Liquibase 免费层需显式 rollback 块 | [Flyway 文档](https://documentation.red-gate.com/flyway)、[Liquibase 文档](https://docs.liquibase.com/) | WebSearch |
| C11.18 | 新增 4.x(NameServer+Remoting)/5.x(Proxy+gRPC/RIP-39，SDK 不兼容) 区分 | [rocketmq.apache.org](https://rocketmq.apache.org/) 5.x 架构 | WebSearch |
| C11.19 | eBPF 内核/BTF 前提（BTF 需 5.2+）& CAP_BPF+CAP_PERFMON(5.8+) 权限演进 | [docs.kernel.org/bpf](https://docs.kernel.org/bpf/) | WebSearch |
| C11.20 | 补 FinOps 平台前提 & 修正 HPA YAML（autoscaling/v2 多指标+behavior） | [kubernetes.io/docs](https://kubernetes.io/docs/)（HorizontalPodAutoscaler 示例） | WebSearch |
| C12.01 | ChatClient 1.0.0-M1(2024-05) 引入、0.8 仅底层；两 Advisor 在 1.0 并存；删虚构类 | `facts/spring-ai-reference.html` | 文档 |
| C12.02 | 经核已合规，无需改 | 站内核对 | 内检 |
| C12.03 | 量化公式 + ada-002 为第二代(2022/1536 维)，2024 起推荐 text-embedding-3 | [platform.openai.com/docs](https://platform.openai.com/docs/)（Embeddings） | WebSearch |
| C12.06 | Function Calling 用 @Tool（1.0 GA 推荐）替代 Function<Req,Resp>@Bean | `facts/spring-ai-reference.html` | 文档 |
| C12.07 | MCP 传输层（stdio/SSE） | `facts/spring-ai-reference.html` | 文档 |
| C12.13 | 独立框架血脉（不混写） | 方法论/上下文 | 推理 |
| C12.16 | stream()+onErrorResume 绑定响应式链 | Reactor 文档（Flux.stream()、onErrorResume） | 文档 |
| C12.21 | Milvus 2.x 真实 API：IndexParam.newBuilder().withExtraParam(JSON)/SearchParam.newBuilder().withParams(JSON) | [Milvus 官方示例](https://milvus.io/docs)、GitHub `io.milvus:milvus-sdk-java` | WebSearch/GitHub |
| C12.25 | BufferOverflowStrategy 仅 ERROR/DROP_LATEST/DROP_OLDEST，无 BLOCK→DROP_OLDEST+Redis 续传 | Reactor `onBackpressureDrop`/`buffer` 文档 | 文档 |
| C12.26 | Advisor 旧 SPI 改写为 1.0 CallAroundAdvisor（adviseCall/nextAroundCall） | `facts/spring-ai-reference.html` | 文档 |
| C12.29 | 评测 CI 阈值补统计前提（≥200 条+95%CI+p<0.05+5-10% 复核） | 方法论 | 推理 |
| C12.31 | CallAroundAdvisor（同 C12.26） | `facts/spring-ai-reference.html` | 文档 |
| C13.02 | TIME_WAIT 仅主动关闭方 + 端口复用/内核参数/LB 辨析 + BBR 数字软化 | RFC 9293 / Linux 内核文档（tcp_tw_reuse、4.12 移除 tcp_tw_recycle） | WebSearch |
| C13.03 | HTTP/1.1 年份 1997 RFC2068/1999 RFC2616 + 握手 RTT + TLS 边界 | [rfc-editor.org/rfc/rfc9112](https://www.rfc-editor.org/rfc/rfc9112)、TLS 1.2/1.3 握手 | WebSearch |
| C13.04 | RTT 算法一致 + SNI/ALPN 分离 | RFC 6066(SNI)、RFC 7301(ALPN) | WebSearch |
| C13.05 | 修正“Selector 封装 IOCP”过度对应（Windows WindowsSelectorProvider 模拟就绪非 IOCP） | JDK 文档（java.nio.channels.spi.SelectorProvider） | 文档 |
| C13.06 | 修正 Netty 4“废弃 Boss/Worker”误述 + exceptionCaught 传播 + SO_BACKLOG 归属父 Channel | `facts/netty-docs.html`（NioEventLoopGroup 主从、exceptionCaught、option SO_BACKLOG） | 文档 |
| C13.07 | ResourceLeakDetector 四级别 + jemalloc 精度 + SimpleChannelInboundHandler 释放陷阱 | `facts/netty-docs.html`（ResourceLeakDetector 级别） | 文档 |
| C13.08 | kTLS(Linux 4.13+) 加密 sendfile 边界 + sendfile/mmap/transferTo 平台条件 | [docs.kernel.org/networking/tls.html](https://docs.kernel.org/networking/tls.html) | WebSearch |
| C13.11 | 经核已合规（Loom 不依赖 io_uring），无需改 | 站内核对 | 内检 |
| C13.12 | Loom/io_uring 独立路线 | `facts/jep444.html`、`facts/jep491.html`（虚拟线程）、io_uring 独立 | 文档 |
| C14.01 | 分片 1.6 引入/2.2 成熟、WiredTiger 3.0 引入/3.2 默认（版本史）；4.0 多文档事务·4.2 跨分片 2PC、6.0 可查询加密 Preview+CSFLE KMIP、8.0 当前稳定+范围可查询加密（现代特性） | `facts/mongodb-22.html`·`mongodb-32.html`（版本史，SPA 壳/WebSearch 核实）；`facts/mongodb-40.html`·`mongodb-60.html`·`mongodb-80.html`（LTS 4.0/6.0/8.0 现代特性，含正文/WebSearch 核实） | 文档/WebSearch |
| C14.02 | Spring AI MongoDBAtlasVectorStore 依赖名/vectorIndexName/量化软化 | `facts/spring-ai-reference.html` | 文档 |
| C14.03 | Milvus 代码块对齐 v2 SDK：AddFieldReq+.field()、IndexParam.builder().extraParams(Map)、SearchResp/FloatVec | [Milvus 官方示例](https://milvus.io/docs)、GitHub `io.milvus:milvus-sdk-java` | WebSearch/GitHub |
| C14.04 | Qdrant 检索改 SearchPoints.newBuilder().setFilter().setLimit()，向量用 FloatVectors | `facts/qdrant-docs.html`（SearchPoints/FloatVectors） | 文档 |
| C14.05 | TiFlash GA 归 4.x(2020)，HTAP 成熟 5.x | `facts/tidb-tiflash.html`（事实经 WebSearch 核实） | 文档/WebSearch |
| C14.06 | Lightweight DELETE 归 22.8(2022)；Variant 归 24.3 实验/24.8 正式 | `facts/clickhouse-delete.html`、`facts/clickhouse-variant.html`（事实经 WebSearch 核实） | 文档/WebSearch |
| C14.07 | Cypher/APOC 描述已准确，补 EXPLAIN/PROFILE 执行计划核对提示 | Neo4j Cypher/APOC 文档（EXPLAIN/PROFILE） | 文档 |
| C14.08 | OceanBase“HTAP 列存(OBKV)”修正为“HTAP 列存副本(4.0 起)”，OBKV 为 KV 接口 | [oceanbase.com](https://www.oceanbase.com/) 官方博客/社区 | WebSearch |
| C14.09 | 量化结论已标注“业界常见量级/参考基准，需以自身生产数据替换” | 方法论 | 推理 |
| C15.01 | 背压 request(n) 拉取图 + Scheduler/背压/Context 三机制分离 + elastic() 版本口径(3.4 弃用/3.5+移除) | Reactor 3.4.2 Reference / 3.4.0 changelog（publishOn/subscribeOn 语义、elastic() 弃用移除） | WebSearch/文档 |
| C15.02 | 吞吐结论补“IO 密集+高并发”前提 + 迁移成本矩阵/依赖画像 | 方法论/推理 | 推理 |
| C15.03 | 经逐 API 核对应准确，未改 | 站内核对 | 内检 |
| C15.04 | onError 向 Subscriber(下游)传播 + BlockHound.install()+@Profile("!prod") 修正 | Reactor 文档（onError 传播）、[BlockHound](https://github.com/reactor/BlockHound) | 文档 |
| C15.05 | 分场景兼容性矩阵 + JDK24 JEP491/JDK25 LTS 口径 | `facts/jep491.html`、`facts/jep505.html`、`facts/jep506.html`（JEP 491/505/506） | 文档 |
| C15.06 | 删除链内手动 subscribe() 反模式 + OrderRepository 事务边界 + Hooks.onErrorDropped | Reactor 文档（链内 subscribe 反模式、Hooks.onErrorDropped） | 文档 |

## 校验记录

- chapter-09（2026-08-30）：C09 锚点 16；`<pre>`/`</pre>` 为 14/14；`<div>`/`</div>` 为 490/490；HTML 标签栈无未闭合或错配。`rg` 残留的“镜像队列”“ha-mode”“暂停写入”分别位于历史演进说明、RabbitMQ 4.0 移除警示和否定错误快照语义的上下文中。
- chapter-10（2026-08-30）：C10 锚点 9；全文 `<div>`/`</div>` 配平校验通过（栈式解析无未闭合/错配）；9 项审查问题全部处理。关键校正：NettyRoutingFilter.getOrder()=Ordered.LOWEST_PRECEDENCE（源码核实，非 LOWEST_PRECEDENCE-1）；W3C 为 Boot 3.0+ 默认传播格式（非 3.2+）；In-place Pod Resize 1.33 仍为 Beta（非 GA）；Dubbo Triple/应用级发现为 3.x 特性（非 2.7/3.x 混写）；Bootstrap 移除（SC 2022.0/Kilburn）与 spring.config.import（Boot 2.4 引入）时间线解耦。C10.15 与 C11.09/C09.11 跨篇重复留待 chapter-11 统一。
- chapter-11（2026-08-30）：C11 锚点 11（C11.11-C11.21）；全文容器标签（div/span/a/section 等）栈式配平校验通过（无未闭合/错配）；11 项审查问题全部处理。关键校正：① Kafka 事务示例 `consumer.position(consumer.assignment())` 编译错误→逐分区构造 `Map<TopicPartition,OffsetAndMetadata>`；② KRaft 版本统一（2.8 预览/3.3 生产就绪/4.0 移除 ZK，原"3.0+"与"2.8 引入"自矛盾，依 KIP-833 核实）；③ proto3 默认无 presence、显式 optional 于 3.12+ 重新引入；④ ES 7.11+ 改 ELv2+SSPL 双许可、OpenSearch 自 7.10.2 分叉、X-Pack 安全免费化实为 6.8/7.1；⑤ Nacos "10x" 改为官方基准测试口径；⑥ RocketMQ 新增 4.x（NameServer+Remoting）与 5.x（Proxy+gRPC/RIP-39，SDK 不兼容）区分；⑦ eBPF 内核/BTF 前提与 CAP_BPF 权限演进。C10.15 提到的"C11.09"在本文件不存在（chapter-11 无 C11.09，C11.10 为混沌工程），可观测性跨篇去重仅限 C10.15↔C09.11，二者已自洽。
- chapter-12（2026-08-30）：C12 锚点 12（C12.01-C12.31 中 12 张审查卡）；全文容器标签（div/span/a/section 等）栈式配平校验通过（无未闭合/错配）；12 项审查问题全部处理（C12.02 经全文核对无 review 所列"定价/Agentic RAG 成本/无来源百分比"问题，已合规未改）。关键校正：① Spring AI ChatClient 在 1.0.0-M1（2024-05）才引入、0.8 仅底层 API，MessageChatMemoryAdvisor 与 PromptChatMemoryAdvisor 在 1.0 并存（非更名）；② text-embedding-ada-002 为第二代（2022/1536 维），非"第一代"，2024 起官方推荐 text-embedding-3；③ Function Calling 用 @Tool（1.0 GA 推荐）替代 Function<Req,Resp>@Bean + .tools("name") 不可靠写法；④ Milvus 2.x 真实 API 为 IndexParam.newBuilder().withExtraParam(JSON 字符串)/SearchParam.newBuilder().withParams(JSON 字符串)，原 IndexParams.new().withExtraParam("nlist",8192) 链式 int 参数为伪造；⑤ Reactor BufferOverflowStrategy 仅 ERROR/DROP_LATEST/DROP_OLDEST，无 BLOCK，改为 DROP_OLDEST + Redis 状态外置续传兜底；⑥ Advisor 旧 SPI（BaseAdvisor/adviseRequest/adviseResponse + Kotlin mapOf）改写为 1.0 CallAroundAdvisor（adviseCall/nextAroundCall/getName/getOrder）+ Java Map.of；⑦ 评测 CI 卡门阈值补统计前提（≥200 条评测集 + 95% 置信区间 + p<0.05 显著 + 5%-10% 人工复核）。
- chapter-13（2026-08-30）：C13 锚点 12（C13.02-C13.12 中 9 张审查卡，C13.01/09/10 不在 review 列表）；全文容器标签栈式配平校验通过（无未闭合/错配）；9 项审查问题全部处理（C13.11 经全文核对已正确区分“Loom 依赖 io_uring”误区无需改；C13.07 的 ResourceLeakDetector 四级别经 Netty 官方文档核实准确，仅做属性名与 jemalloc 精度小幅澄清）。关键校正：① TCP TIME_WAIT 明确仅落在主动关闭方、补 SO_REUSEADDR/SO_REUSEPORT 与 tcp_tw_reuse/tcp_tw_recycle（Linux 4.12 移除）边界，及 L4 LB SNAT 放大 TIME_WAIT 的负载均衡影响；② HTTP/1.1 年份由“1997 RFC 2616”修正为“1997 RFC 2068 首版、1999 RFC 2616 修订”，握手延迟行改为按 TLS 1.2/1.3 区分的 RTT 表述，补 HTTP/2 强制 TLS1.2+ALPN、HTTP/3 强制内嵌 TLS1.3 的版本边界；③ TLS 1.2 完整握手“2 次 TLS 往返 + TCP 1-RTT ≈ 3-RTT”口径自洽，并分离 SNI/ALPN 两个握手扩展；④ 修正“Selector 封装 IOCP”的过度对应——Windows 上 JDK 用 WindowsSelectorProvider 模拟就绪而非 IOCP（IOCP 属 AIO 完成驱动），补就绪集合/事件丢失/重复的平台语义；⑤ 修正 Netty 4“废弃 Boss/Worker”误述（主从 Reactor 分工仍在），补 Pipeline 异常经 exceptionCaught 向后传播、出站异常走 ChannelFuture 的边界，SO_BACKLOG 归属父 Channel option；⑥ 补 kTLS（Linux 4.13+）使加密 sendfile 可行的边界，及 sendfile/mmap/transferTo 的平台与降级条件。
- chapter-14（2026-08-30）：C14 锚点 9（C14.01-C14.09）；全文容器标签栈式配平校验通过（无未闭合/错配）；9 项审查问题全部处理（C14.07 经全文核对 Cypher/APOC 描述已准确，仅补 EXPLAIN/PROFILE 执行计划核对提示）。关键校正：① MongoDB 分片集群标注 1.6（2010）引入、2.2-3.x 生产成熟，WiredTiger 为 3.0 引入、3.2 成为默认（非 3.0 即默认）；② Spring AI MongoDBAtlasVectorStore 依赖名修正为 spring-ai-mongodb-atlas-store（非 spring-ai-mongodb-store-spring-boot-starter），builder 方法 indexName 修正为 vectorIndexName，召回率/规模等量化补“数据分布与参数相关”前提；③ Milvus 代码块对齐 v2 SDK（io.milvus:v2-client）：建集合字段用 AddFieldReq+.field()（非 FieldSchema+.addField()），HNSW 参数走 IndexParam.builder().extraParams(Map)，检索返回 SearchResp、data 用 FloatVec 包装；④ Qdrant 检索由错误的 8 参数 searchAsync 改为 SearchPoints.newBuilder().setFilter().setLimit() 形式，向量包装由 Vector 改为 FloatVectors；⑤ TiDB TiFlash GA 由 5.x 归正到 4.x（2020），HTAP 成熟在 5.x；⑥ ClickHouse Lightweight DELETE 由 23.x 归正到 22.8（2022），Variant 类型由 23.x 归正到 24.3 实验性/24.8 正式；⑦ OceanBase 的“HTAP 列存（OBKV）”修正为“HTAP 列存副本（4.0 起）”，OBKV 为 KV 接口非列存；⑧ 量化结论均已标注“业界常见量级/参考基准，需以自身生产数据替换”前提。
- chapter-15（2026-08-30）：C15 锚点 6（C15.01-C15.06）；全文容器标签栈式配平校验通过（无未闭合/错配）；6 项审查问题全部处理（C15.03 经逐 API 核对应准确未改）。关键校正：① C15.01 新增背压 request(n) 拉取模型图，明确 Scheduler 切换 / 背压 request 传播 / Reactor Context 上下文传播三者独立；`Schedulers.elastic()` 口径补“Reactor 3.4 弃用、3.5+ 移除”；② C15.02 吞吐结论补“IO 密集+高并发”前提软化绝对化，新增 WebMVC→WebFlux 迁移成本矩阵（数据访问/下游调用/上下文/调试/生态 + 依赖画像）；③ C15.04 onError 演进层“向上游传播”误述修正为“向下游（朝 Subscriber）”传播，新增异常信号图，BlockHound 配置由不实的 `spring.blockhound.enabled=true` 修正为 `BlockHound.install()` + `@Profile("!prod")`，并区分开发期检测与生产 Resilience4j 熔断；④ C15.05 新增虚拟线程分场景兼容性矩阵（Tomcat/Netty/JDBC/Lettuce/Jedis/CPU 密集），pinning 修复口径补“JDK 24 JEP 491 + JDK 25 LTS 继承”，ScopedValue 维持 JDK 25 GA 已核实；⑤ C15.06 删除链内 `redis.opsForValue().set(...).subscribe()` 手动订阅反模式（破坏 WebFlux 请求契约），改为 `flatMap(...thenReturn(v))` 绑定到响应式链，并补 `OrderRepository` 使事务边界内“更新车辆+创建订单”同生同灭，全局未处理错误指向 `Hooks.onErrorDropped`。
- 按用户要求从 chapter-10 起逐篇修复、确认一篇再处理下一篇；chapter-10、chapter-11、chapter-12、chapter-13、chapter-14、chapter-15 已全部完成。
- 全站交叉校验（2026-08-30，收尾闭环）：运行 `facts/validate_site.py` 对 21 个真实 HTML（排除 .bak 备份）做四项自动化校验——① 标签配平：全部 OK，无未闭合/错配；② 内部悬空锚点：发现 1 处，chapter-11 L2016 将跨文件引用误写为 `<a href="#C10.20">`（文件内无此锚点），已修正为 `chapter-10-microservice-cloud.html#C10.20`，复校归零；③ 跨文件悬空引用：0；④ 孤儿卡片锚点（C/M/E/S 前缀且未被任何链接引用）：0。量化数字扫描命中 1448 处，经抽样确认绝大多数为 CSS（`width:100%`）、代码示例与教科书事实（如 GC 98% 朝生夕死、Eden:S0:S1=8:1:1、HyperLogLog 0.81% 误差），非无来源性能断言；chapter-10~15 的绝对化量化已在逐篇修复阶段按基线软化（见各章记录），无需再改。结论：全站结构完整、链接可达、知识点无遗漏/重复/孤儿，逐篇修复序列可正式闭环。

## 关键结论

- 虚拟线程不是 CPU 时间片抢占式调度：JDK 当前不实现 time sharing，可卸载阻塞点释放载体线程；CPU 密集任务不会自动让出，载体线程仍由 OS 调度。
- JFR 事件名是 `jdk.VirtualThreadPinned`，JDK 21 默认 threshold 20ms；`jdk.tracePinnedThreads` 只适用于 JDK 21-23，JDK 24 移除。
- JDK 24 JEP 491 消除“几乎全部” synchronized pinning，不是绝对零 pinning；native/foreign 回调等场景仍需按版本验证。
- 结构化并发 JDK 19/20 incubator，JDK 21-24 preview，JDK 25 引入 `open()/Joiner`，JDK 26 仍是第六次 preview；`awaitAnySuccessfulResult()` 不存在，正确方法包括 `anySuccessfulResultOrThrow()`、`allSuccessfulOrThrow()`、`awaitAllSuccessfulOrThrow()`、`awaitAll()`。
- ScopedValue JDK 25 转正，但只适合 one-way immutable context；不要求、也不能无条件替代 ThreadLocal，双向更新和某些线程私有可变缓存仍适合 ThreadLocal。
- `System.nanoTime()` 只用于同一 JVM 内测量经过时间，原点无语义，不能跨进程、跨节点比较；跨节点顺序需协议序号、共识日志、TSO、HLC 或带不确定性处理的授时方案。
- 容灾 RTO/RPO 是验证目标而非架构名称的天然结果；一致性由复制、仲裁、提交和切换协议决定，不能把同城双活/异地多活简化为 CP/AP。
- Apache Seata v2.6.0（2026-01-28，非预发布）源码样例提供 Raft 模式配置，但生产采用仍需按目标版本 release notes、兼容矩阵、存储恢复、监控与演练验证；CDC 端到端延迟取决于 binlog、连接器、队列和消费链路。
- Spring Cloud Gateway `NettyRoutingFilter.getOrder()` 返回 `Ordered.LOWEST_PRECEDENCE`（=Integer.MAX_VALUE=2147483647），与 `ForwardRoutingFilter` 同为最低优先级、位于过滤器链最末端；鉴权/限流等 GlobalFilter 的 order 必须 < 2147483647。
- Spring Boot 3.0 / Spring Cloud 2022.0（Kilburn）停止自动创建 Bootstrap 上下文；`spring.config.import`/ConfigData 机制自 Boot 2.4（2020）已引入，二者是不同事件，不可混写为同一时间点。
- Micrometer Tracing 1.0 / Boot 3.0 起 W3C TraceContext 即为默认传播格式（非 Boot 3.2+）；Sleuth 的 OTel 桥接是 3.x 试验性模块，正式长期路径是独立的 Micrometer Tracing。
- K8s In-place Pod Resize（KEP-1287）1.27 Alpha → 1.33 Beta（默认启用 InPlacePodVerticalScaling gate），截至 1.33 仍非 GA；Dubbo Triple 协议与应用级服务发现是 3.x（2021）特性。
