# chapter-01 至 chapter-15 内容审查报告

> **历史文档说明**：本文写于站点品牌名为《Java 架构师面试问答》时期，文中沿用「面试 / 八股文」等旧术语。全站已于 2026-09-04 更名为《Java 专家 · 架构师 · 高级开发 工程能力知识库》，对应术语现为「知识点 / 核心原理」。**本文为历史审查记录，内容按原文保留，不作改写。**

## 1. 审查结论

本次审查覆盖 `java-architect-interview` 目录下 15 个章节 HTML，共 216 张 QA 卡片。审查对象是文本内容、版本事实、示例代码、API、公式、结构与量化结论；未修改任何章节 HTML，未读取 yml 配置，未连接数据库，也未新增依赖。

整体结论：内容框架完整，但存在三类必须修复的问题。第一，若干版本事实和平台行为错误，可能直接误导面试回答；第二，部分示例代码调用了不存在或与当前版本不匹配的 API，且少数代码存在并发安全缺陷；第三，多张卡片有粘贴错位、重复段落、主题漂移和无来源精确量化。建议先修复下表 P0，再清理版本边界和无来源数据。

## 2. P0 快修清单

| 位置 | 问题 | 修复方向 |
|---|---|---|
| [C02.02](chapter-02-gc-performance.html#C02.02) | 结构/语义损坏，Shenandoah Brooks Pointer 描述过时 | 重排卡片并按当前 JDK 重写 Shenandoah |
| [C03.11](chapter-03-concurrency-locks.html#C03.11) | 疑似伪造 Disruptor API，示例无法编译 | 以 Disruptor 官方当前版本 API 重写 |
| [C06.01](chapter-06-spring-boot-modern.html#C06.01) | Spring Boot 3 自动配置迁移语义错误 | 说明旧 `spring.factories` 自动配置 key 已失效 |
| [C06.02](chapter-06-spring-boot-modern.html#C06.02) | starter、处理器、Native 命令和性能数字多处错误 | 按官方 AOT/Native 文档重写并删除倍数 |
| [C06.04](chapter-06-spring-boot-modern.html#C06.04) | Security 6 默认链核心过滤器写错 | 改为 `SecurityContextHolderFilter` |
| [C06.11](chapter-06-spring-boot-modern.html#C06.11) | JWT 资源服务器配置疑似无效 API | 改用 `Customizer.withDefaults()` 或 decoder lambda |
| [C06.12](chapter-06-spring-boot-modern.html#C06.12) | K8s 摘流、`preStop`、SIGTERM 时序错误 | 重写为并发流程，说明 sleep 的传播等待目的 |
| [C07.08](chapter-07-mysql-deep.html#C07.08) | 结构污染，含伪 SQL、废弃参数和不存在列/API | 拆卡重写，示例按 MySQL 当前版本验证 |
| [C07.10](chapter-07-mysql-deep.html#C07.10) | 声称 `filtered` 已从 MySQL 8.0 移除，事实相反 | 删除该结论并补齐 EXPLAIN 字段语义 |
| [C08.03](chapter-08-redis-cache.html#C08.03) | 防击穿代码会递归查缓存并误删他人锁 | 使用等待/重试或本地标记，释放锁前校验 owner |
| [C08.11](chapter-08-redis-cache.html#C08.11) | PEL 被错误描述为客户端状态 | 改为 Redis Stream 消费组服务端状态 |
| [C09.07](chapter-09-distributed-systems.html#C09.07) | 哈希取模迁移量公式错误 | 正确方向约为 `1 - 1/(N+1)` |
| [C12.01](chapter-12-ai-engineering.html#C12.01) | Spring AI 时间线与 Advisor API 不准确 | 按所用 Spring AI 版本重写 |
| [C12.21](chapter-12-ai-engineering.html#C12.21) | Milvus/向量库 API 与性能参数不可靠 | 以目标版本 SDK 文档重写并删除精确性能承诺 |
| [C14.02](chapter-14-databases.html#C14.02) | Atlas Vector Search 与 Spring AI 集成 API 不准确 | 按官方 driver/Spring AI 版本重建示例 |
| [C15.01](chapter-15-reactive.html#C15.01) | Reactor 调度、背压和 MDC 传播机制混写 | 拆分调度器、上下文和 Hooks 机制 |

## 3. 逐章明细

### chapter-01：JVM、内存与类加载

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C01.02](chapter-01-jvm-memory-classloading.html#C01.02) | 对象头、Mark Word、锁标志位和压缩布局混用了不同 JVM/JDK 行为 | 标注 64 位、`UseCompressedOops`、`UseCompressedClassPointers` 与 JDK 版本 | P1 |
| [C01.05](chapter-01-jvm-memory-classloading.html#C01.05) | finalize 相关表述与当前 JDK 默认策略冲突 | 明确 finalize 自 JDK 18 起默认禁用，并推荐 Cleaner/try-with-resources | P1 |
| [C01.06](chapter-01-jvm-memory-classloading.html#C01.06) | DirectByteBuffer、 Cleaner 和 mmap 被过度简化 | 区分堆外内存、文件映射页与内核页缓存，不把三者等同于同一种机制 | P1 |
| [C01.09](chapter-01-jvm-memory-classloading.html#C01.09) | C1/C2、GraalVM、分层编译和 AOT 的边界描述过强 | 区分 JIT Profile、去优化、AOT 缓存与 Native Image | P1 |
| [C01.10](chapter-01-jvm-memory-classloading.html#C01.10) | JDK 21 特性未统一区分 preview 与 final | 逐项标注 JEP、版本与 `--enable-preview` 要求 | P0 |
| [C01.11](chapter-01-jvm-memory-classloading.html#C01.11) | “JVM 堆是页表视图”的比喻容易误导 | 保留页表/TLB 机制，但删除把 Java 引用直接映射为虚拟地址的暗示 | P2 |

### chapter-02：GC 与性能诊断

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C02.02](chapter-02-gc-performance.html#C02.02) | 卡片结构损坏；Shenandoah Brooks Pointer 已不是当前实现的总括；收集器适用性过度绝对化 | 按当前 JDK 重组 CMS、G1、ZGC、Shenandoah，并删除历史实现细节 | P0 |
| [C02.07](chapter-02-gc-performance.html#C02.07) | Arthas 命令输出、参数和适用条件与当前版本不一致 | 用目标 Arthas 版本验证所有命令，特别是 watch/trace/ognl 的参数 | P1 |
| [C02.08](chapter-02-gc-performance.html#C02.08) | JFR 事件名、默认开关和异步 profiler 集成描述不准确 | 按 JDK 版本列出事件名、模板和启动参数 | P1 |
| [C02.10](chapter-02-gc-performance.html#C02.10) | 逃逸分析、栈上分配、标量替换的因果关系前后不一致 | 明确 HotSpot 常见表现是标量替换，不能承诺所有逃逸对象栈分配 | P1 |
| [C02.11](chapter-02-gc-performance.html#C02.11) | Generational ZGC 的版本、开关和默认状态需按 JDK 核对 | 标注 JDK 21 引入与目标 JDK 的启用方式 | P1 |
| [C02.12](chapter-02-gc-performance.html#C02.12) | Micrometer 指标名、GC 指标来源和告警阈值缺少版本边界 | 以实际 Micrometer/Prometheus 指标为准，不把经验阈值写成默认值 | P1 |

### chapter-03：并发与锁

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C03.06](chapter-03-concurrency-locks.html#C03.06) | CHM 死锁案例过度演绎，复合操作与单方法线程安全的边界不清晰 | 明确 `compute` 等方法内阻塞/递归的风险，但不泛化为必然死锁 | P1 |
| [C03.07](chapter-03-concurrency-locks.html#C03.07) | 把 `StampedLock` 与 Condition 混入同一等待模型 | 明确 `StampedLock` 不实现 `Condition`，等待语义与 `ReentrantLock` 不同 | P0 |
| [C03.09](chapter-03-concurrency-locks.html#C03.09) | ForkJoinPool 调度、commonPool 大小和工作窃取被过度简化 | 区分提交外部任务与分治子任务，标注并行流默认池风险 | P2 |
| [C03.11](chapter-03-concurrency-locks.html#C03.11) | Disruptor 示例中的类、方法、等待策略名称疑似伪造 | 以 Disruptor 当前稳定版本重写编译级示例 | P0 |
| [C03.11](chapter-03-concurrency-locks.html#C03.11) | `ExecutionException` 与 `CompletionException` 的抛出边界混用 | 按同步调用、`join`、`get` 与异步链路分别说明 | P1 |
| [C03.12](chapter-03-concurrency-locks.html#C03.12) | 平台线程 1:1、虚拟线程协作式让出和抢占式调度的表述过简 | 区分调度点、载体线程阻塞与 CPU 计算不被主动抢占 | P1 |

### chapter-04：线程池与虚拟线程

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C04.01](chapter-04-threadpool-virtual-threads.html#C04.01) | 通过反射修改队列容量是危险且不可移植的示例 | 删除反射方案，改为有界队列、监控与动态线程池封装 | P1 |
| [C04.04](chapter-04-threadpool-virtual-threads.html#C04.04) | 虚拟线程被描述为抢占式模型 | 改为调度器在阻塞点/ yields 协作让出，CPU 密集不自动抢占 | P0 |
| [C04.06](chapter-04-threadpool-virtual-threads.html#C04.06) | 异常传播与线程池透传示例容易丢失任务上下文 | 补充 MDC/TraceContext 的显式捕获与恢复 | P1 |
| [C04.08](chapter-04-threadpool-virtual-threads.html#C04.08) | Structured Concurrency 的 JEP/API 名称和可用性需核对 | 标注 preview 状态与目标 JDK，避免把孵化 API 当稳定 API | P1 |
| [C04.09](chapter-04-threadpool-virtual-threads.html#C04.09) | JFR 事件名应为 `jdk.VirtualThreadPinned`，且 pinning 成因需按 JDK 版本说明 | 修正事件名，并区分 synchronized、native frame 与 JDK 版本变化 | P0 |
| [C04.10](chapter-04-threadpool-virtual-threads.html#C04.10) | ScopedValue 与 ThreadLocal 的替代关系写得太绝对 | 标注 API 状态、不可变绑定、生命周期与重建成本 | P1 |

### chapter-05：Spring 核心原理

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C05.01](chapter-05-spring-core.html#C05.01) | “追问 4：不同类型 BeanPostProcessor”重复粘贴并插入到错误位置 | 清理重复段落，恢复生命周期顺序 | P0 |
| [C05.02](chapter-05-spring-core.html#C05.02) | `allow-circular-references` 与 Boot 2.6+ 默认行为归因到 Spring 6 不准确 | 分别说明 Spring Framework 能力与 Boot 默认策略 | P1 |
| [C05.03](chapter-05-spring-core.html#C05.03) | `proxyTargetClass=true` 被写成 Spring 5+ 通用默认 | 限定为 Spring Boot 2.x 起自动配置默认，并说明 Framework 行为 | P1 |
| [C05.04](chapter-05-spring-core.html#C05.04) | 自调用示例注释“不走代理,事务生效”自相矛盾；`publicMethodsOnly` 版本表述过强 | 修正为自调用默认不经过代理；按源码和版本核对该属性 | P0 |
| [C05.06](chapter-05-spring-core.html#C05.06) | 设计模式卡尾部混入网关 RT、规则开发提效、10w QPS 等无关内容 | 删除主题漂移段，保留 Spring 源码映射 | P1 |
| [C05.07](chapter-05-spring-core.html#C05.07) | BeanPostProcessor 的重复追问段落影响主流程 | 保留一条扩展路径，其余合并到生命周期卡 | P1 |
| [C05.08](chapter-05-spring-core.html#C05.08) | 尾部追问 2/3 与主主题上下文疑似粘贴错位 | 重排为 BeanFactory/ApplicationContext 的差异与扩展点 | P1 |
| [C05.10](chapter-05-spring-core.html#C05.10) | SpEL、占位符、Boot 条件注解和 AOT 预编译边界混写 | 分层说明 `@Value`、`@ConditionalOnExpression`、SpEL 编译与 AOT 限制 | P1 |

### chapter-06：Spring Boot 与云原生

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C06.01](chapter-06-spring-boot-modern.html#C06.01) | Boot 3 后旧自动配置 key 不再生效，不是“兼容但告警”；`@AutoConfiguration` 自 Boot 2.7 引入；示例包名可疑 | 按官方迁移说明重写，并用当前 artifact 验证示例 | P0 |
| [C06.02](chapter-06-spring-boot-modern.html#C06.02) | `spring-boot-starter-aot` 疑似不存在；处理器名称不严谨；`native:build` 注释错误；性能数字无来源 | 删除伪 starter 和倍数，按 Maven/Gradle Native 插件与 Boot AOT 任务重写 | P0 |
| [C06.03](chapter-06-spring-boot-modern.html#C06.03) | `@ConfigurationPropertiesValidation` 不存在；“所有 starter 双模块”过度泛化 | 改为 `@Validated` + Bean Validation；仅描述常见双模块模式 | P0 |
| [C06.04](chapter-06-spring-boot-modern.html#C06.04) | Security 6 默认链仍写 `SecurityContextPersistenceFilter` | 改为 `SecurityContextHolderFilter`，并补充委托关系 | P0 |
| [C06.05](chapter-06-spring-boot-modern.html#C06.05) | 启动事件时间线混乱；ApplicationRunner 没有取代 CommandLineRunner；AOT 细节未核对 | 按目标 Boot 版本重绘事件顺序，并列出 runner 差异 | P1 |
| [C06.06](chapter-06-spring-boot-modern.html#C06.06) | Session 是否每次访问 save/续期前后矛盾；Redis 过期结构版本化不足 | 按当前 Spring Session 源码或文档统一描述 | P1 |
| [C06.07](chapter-06-spring-boot-modern.html#C06.07) | Micrometer Observation 不直接统一 Logging；Actuator 通用 OpenMetrics 表述不严谨；YAML 缩进可疑 | 拆分 Metrics/Trace/Log correlation，并重写配置示例 | P1 |
| [C06.08](chapter-06-spring-boot-modern.html#C06.08) | “Spring 2.x-4.x 无 profile”错误；`nacos:` 非原生 Boot；import 不等于必然热更新；Nacos 容量数据无来源 | 修正 Spring 3.1 起的 profile 脉络，区分原生与扩展能力 | P1 |
| [C06.09](chapter-06-spring-boot-modern.html#C06.09) | `ResponseEntity.problemDetail()` 等 API 疑似错误；默认 resolver 与异常类型示例需按 Spring 6 核对 | 使用 `ProblemDetail.forStatusAndDetail` 等稳定 API 重写 | P1 |
| [C06.10](chapter-06-spring-boot-modern.html#C06.10) | `@Validated` 分组、方法校验异常与 Jakarta 迁移边界不够准确 | 分别列出请求体校验、方法级校验、异常类型和版本包名 | P1 |
| [C06.11](chapter-06-spring-boot-modern.html#C06.11) | `.oauth2ResourceServer(o -> o.jwt(JwtConfigurer::jwt))` 疑似无效 API | 改为 `jwt(Customizer.withDefaults())` 或显式 decoder 配置 | P0 |
| [C06.12](chapter-06-spring-boot-modern.html#C06.12) | K8s 顺序写成 readiness 失败 → SIGTERM → preStop，与实际删除 Pod 流程不符 | 重写为 preStop、endpoint 摘除、终止宽限并发与传播等待 | P0 |
| [C06.13](chapter-06-spring-boot-modern.html#C06.13) | Micronaut 不是 Oracle 出品；Boot 3.x 功能清单与版本时间线需逐项核对 | 修正归属，按官方 release notes 重写版本表 | P1 |

### chapter-07：MySQL 与持久层

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C07.01](chapter-07-mysql-deep.html#C07.01) | 行格式与页压缩被误写成 8.0 新增；“其他数据库都是 B+树”过度泛化；UUID 替代方案混写 | 限定 MySQL/InnoDB 范围，分开讨论 UUID、雪花和数据库生成 ID | P1 |
| [C07.02](chapter-07-mysql-deep.html#C07.02) | RC “无间隙锁、范围当前读不加锁”过于绝对 | 限定普通二级索引等值/范围场景，并补充唯一键、外键和约束检查例外 | P1 |
| [C07.03](chapter-07-mysql-deep.html#C07.03) | 非唯一索引等值命中的扫描终点和范围锁错误 | 按扫描到第一条不满足记录的间隙化行为重写 | P0 |
| [C07.04](chapter-07-mysql-deep.html#C07.04) | 组复制和组提交版本演进不准确 | MGR 改为 MySQL 5.7.17；区分 5.6/5.7 的组提交增强 | P1 |
| [C07.05](chapter-07-mysql-deep.html#C07.05) | varchar 列与数字比较的隐式转换方向写反 | 明确通常字符串列被转换为数字，导致列索引失效 | P0 |
| [C07.06](chapter-07-mysql-deep.html#C07.06) | 选择率阈值前后矛盾，且混用选择率与过滤后剩余比例 | 统一定义和公式，删除绝对阈值 | P1 |
| [C07.07](chapter-07-mysql-deep.html#C07.07) | 跨库分页取数公式少了已有 offset | 每库应取 `(offset + page)`，再统一归并排序 | P0 |
| [C07.08](chapter-07-mysql-deep.html#C07.08) | 结构污染；GTID/SQL/Java 示例多处无效；废弃参数与不存在列、线程参数混杂 | 拆分为 GTID、复制延迟、监控和客户端故障转移多张卡，逐项验证 | P0 |
| [C07.09](chapter-07-mysql-deep.html#C07.09) | MGR 版本错误；Orchestrator/MHA 维护状态写得过强 | 修正版本，并把维护状态限定到具体日期与分支 | P1 |
| [C07.10](chapter-07-mysql-deep.html#C07.10) | `filtered` 被写成 MySQL 8.0 移除，实际仍存在 | 删除错误结论，补齐 rows/filtered 估算语义 | P0 |
| [C07.11](chapter-07-mysql-deep.html#C07.11) | `innodb_deadlock_detect` 引入版本不准确；RC 间隙锁结论过强 | 按 MySQL 版本核对参数，重写隔离级别例外 | P1 |
| [C07.12](chapter-07-mysql-deep.html#C07.12) | INSTANT DDL 支持范围错误；pt-osc “不支持外键”不准确 | 按 MySQL 版本列出 INSTANT 约束，说明 pt-osc 外键方法 | P1 |
| [C07.14](chapter-07-mysql-deep.html#C07.14) | MyBatis 缓存、插件顺序与 SQL 注入示例缺少当前版本约束 | 按项目所用 MyBatis/PageHelper 版本重写，并补充一级缓存事务风险 | P1 |
| [C07.15](chapter-07-mysql-deep.html#C07.15) | MP 分页/乐观锁与 JPA 软删 API 需按当前版本核对 | 用可编译示例验证 `@Version`、分页拦截器和软删注解 | P1 |

### chapter-08：Redis 与缓存

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C08.01](chapter-08-redis-cache.html#C08.01) | quicklist 时间线错误；Bitmap/HyperLogLog 与 `TYPE` 语义矛盾；Functions 调用错误；Redis 8 营销数据无来源 | 修正 Redis 3.2 quicklist；区分编码与逻辑类型；按 Functions 名称重写调用 | P0 |
| [C08.02](chapter-08-redis-cache.html#C08.02) | AOF 时间线偏晚；Redis 7 manifest 文件名错误 | 修正为 `appendonly.aof.manifest`，并按 Redis 版本说明 multi-part AOF | P1 |
| [C08.03](chapter-08-redis-cache.html#C08.03) | 未抢锁线程递归查缓存；finally 无条件删锁，可能删除他人锁 | 使用短暂等待/重试或本地 null 标记；Lua 校验 owner 后释放 | P0 |
| [C08.04](chapter-08-redis-cache.html#C08.04) | “更新缓存是反模式”“先删缓存禁用”结论过强；Canal/MQ 顺序约束不严谨 | 改为业务一致性等级下的策略矩阵，补充幂等、重试与延迟双删成本 | P1 |
| [C08.05](chapter-08-redis-cache.html#C08.05) | ZK/etcd 被说成天然严格互斥；fencing token 争议归属和 Redisson 支持状态需核对 | 强调 fencing token、租约和幂等；按当前 Redisson 版本描述 RedLock | P1 |
| [C08.06](chapter-08-redis-cache.html#C08.06) | 与 C08.05 冲突：一边否定 RedLock，一边建议跨机房使用；Redis OSS 无原生半同步复制 | 删除冲突建议；`WAIT` 只能作为同步副本数辅助手段 | P1 |
| [C08.07](chapter-08-redis-cache.html#C08.07) | `min-replicas-to-write` 被写成请求级同步 ACK；选主规则漏 priority 等条件 | 改为写准入检查，并按 Redis 触发/状态机描述故障转移 | P1 |
| [C08.08](chapter-08-redis-cache.html#C08.08) | lazy-free 和主动过期线程版本错误 | 以 Redis 4.0 lazy-free 体系为基准，按版本说明后台线程能力 | P1 |
| [C08.10](chapter-08-redis-cache.html#C08.10) | Intel Optane 等趋势过时；“单实例 10w QPS 上限”绝对化；生态现状需核对 | 改为经验量级和压力测试模板，删除硬件趋势结论 | P1 |
| [C08.11](chapter-08-redis-cache.html#C08.11) | PEL 是 Redis Stream 消费组服务端状态，不是分散在客户端；持久化边界表述不准确 | 重写 XPENDING/XACK/XAUTOCLAIM 与持久化前提 | P0 |

### chapter-09：分布式系统

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C09.01](chapter-09-distributed-systems.html#C09.01) | Gilbert & Lynch 机构归属需核校；“单机 CA”与具体一致性模型混淆；AP/CP 产品标签过简 | 引用准确来源，按线性一致性和可用性定义分类 | P1 |
| [C09.02](chapter-09-distributed-systems.html#C09.02) | 2PC/3PC 起源和参与者超时行为过度简化；Seata AT 全局锁与 undo log 流程需按版本核对 | 按协议论文和 Seata 当前文档重写 | P1 |
| [C09.03](chapter-09-distributed-systems.html#C09.03) | ZK/etcd 分布式锁仍需 fencing token；RedLock 使用减少的结论缺版本和时间边界 | 明确锁服务不等于资源访问授权，补充 fencing/幂等设计 | P1 |
| [C09.04](chapter-09-distributed-systems.html#C09.04) | Kafka 事务示例不可运行；EOS、`transactional.id`、隔离级别和 rebalance 细节混杂 | 使用目标 Kafka client 版本编写可编译事务示例并区分内部/端到端语义 | P0 |
| [C09.05](chapter-09-distributed-systems.html#C09.05) | 紧急处理顺序混在一起；“1000 万”处理结果给出过强加速比 | 按止血、降级、扩容、回溯分层，删除无来源性能倍数 | P1 |
| [C09.06](chapter-09-distributed-systems.html#C09.06) | Leaf-segment 丢号边界、QPS、UUID 索引膨胀率缺来源 | 标注为经验值或压测模板，补充号段持久化与重启语义 | P1 |
| [C09.07](chapter-09-distributed-systems.html#C09.07) | 哈希取模扩容迁移量公式错误；一致性哈希查找复杂度与虚拟节点数量缺前提 | 修正公式，明确 hash 函数、实现结构和经验 vnode 数量 | P0 |
| [C09.08](chapter-09-distributed-systems.html#C09.08) | Token 幂等与业务事务边界不清；分布式锁被当成幂等保证；Redis 快路径失败处理不完整 | 以唯一约束/状态机为兜底，定义 Redis 标记失败后的补偿与清理 | P1 |
| [C09.09](chapter-09-distributed-systems.html#C09.09) | RocketMQ API 废弃版本不精确；RabbitMQ mirrored queue 与 Quorum Queue 架构落后；Redis 幂等标记有误标记风险 | 按当前 MQ 版本重写，并把 Redis 作为快路径而非唯一事实 | P1 |
| [C09.10](chapter-09-distributed-systems.html#C09.10) | FLP 缺少异步确定性模型限定；etcd 参数/快照行为随版本变化；“暂停写入”不准确 | 限定定理模型，按 etcd 目标版本重写运维参数 | P1 |
| [C09.11](chapter-09-distributed-systems.html#C09.11) | OpenTelemetry 时间线、OTLP/Collector 语义和无侵入结论需核对 | 按当前 OTel SDK/自动插桩文档重写 | P1 |
| [C09.12](chapter-09-distributed-systems.html#C09.12) | 缓存一致性策略写成必然双删；binlog/MQ 的顺序与幂等约束不足 | 按一致性等级列出方案、失败处理和可观测指标 | P1 |
| [C09.13](chapter-09-distributed-systems.html#C09.13) | Session 共享、JWT 吊销和网关透传身份头的安全前提缺失 | 补充加密签名、网络隔离、防伪造头和注销边界 | P1 |
| [C09.14](chapter-09-distributed-systems.html#C09.14) | HLC/Spanner/TrueTime 精度结论缺来源；“`System.nanoTime` 可用于全局逻辑时钟”错误 | 区分单调时钟、物理时钟、HLC 与全局授时服务 | P0 |
| [C09.15](chapter-09-distributed-systems.html#C09.15) | 多活 RTO/RPO 接近 0 缺少前提；“同城双活相当于 CP”标签错误；LDC 细节被写成通用标准 | 以数据一致性等级和业务 SLA 表述，删除过强分类 | P1 |
| [C09.16](chapter-09-distributed-systems.html#C09.16) | Seata 2.x Raft/GA 状态和部署建议需核对；CDC 不等于毫秒级；“2026 首选”过强 | 按当前 Seata 版本核对能力，将选型改为场景矩阵 | P1 |

### chapter-10：微服务与云原生

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C10.02](chapter-10-microservice-cloud.html#C10.02) | Gateway filter 类型、order、请求/响应上下文透传描述不一致 | 按当前 Spring Cloud Gateway 版本重写 ordered/predicated filter 流程 | P1 |
| [C10.03](chapter-10-microservice-cloud.html#C10.03) | Resilience4j 异常类、降级签名与限流器语义需核对 | 用目标版本编写可编译 fallback/rate limiter 示例 | P1 |
| [C10.04](chapter-10-microservice-cloud.html#C10.04) | Java 容器资源感知、探针与优雅停机依赖的 Boot/JDK 版本未统一 | 标注 JDK、Boot、K8s API 版本 | P1 |
| [C10.09](chapter-10-microservice-cloud.html#C10.09) | 灰度、蓝绿和滚动发布的流量一致性描述缺部署平台前提 | 区分 Service Mesh、Ingress、发布系统与数据库兼容窗口 | P2 |
| [C10.15](chapter-10-microservice-cloud.html#C10.15) | 可观测性描述与 C11.09/C09.11 存在重复且口径不同 | 统一三支柱、OTel Collector 和采样策略 | P2 |
| [C10.20](chapter-10-microservice-cloud.html#C10.20) | GlobalFilter/GatewayFilter 顺序、DirectBuffer 泄漏排查路径需按当前版本核对 | 用实际 Gateway 版本源码或调试日志验证 | P1 |
| [C10.21](chapter-10-microservice-cloud.html#C10.21) | Bootstrap 上下文移除时间与新配置导入机制混写 | 按当前 Spring Cloud 版本区分旧模式与新 Config Data | P1 |
| [C10.22](chapter-10-microservice-cloud.html#C10.22) | Sleuth 到 Micrometer Tracing 的桥接、B3/W3C 与 MDC 配置不准确 | 按目标 Boot/Tracing 版本重写 propagation/采样/MDC | P1 |
| [C10.25](chapter-10-microservice-cloud.html#C10.25) | Dubbo/Triple 协议、服务治理能力对比落后或绝对化 | 按当前 Dubbo 3.x/Triple 文档重写 | P1 |

### chapter-11：中间件与工程化

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C11.11](chapter-11-middleware-engineering.html#C11.11) | Kafka 事务示例不可运行；KRaft 精度、ISR、EOS 与 consumer group 行为混杂 | 按 Kafka 当前 client/broker 版本重写可运行示例 | P0 |
| [C11.12](chapter-11-middleware-engineering.html#C11.12) | API 网关限流、熔断、灰度与 C10.02/C10.20 口径不一致 | 合并通用网关设计，并保留产品差异 | P2 |
| [C11.13](chapter-11-middleware-engineering.html#C11.13) | 与 C11.21 主题高度重复 | 合并为单卡，保留一个选型矩阵 | P1 |
| [C11.14](chapter-11-middleware-engineering.html#C11.14) | Elasticsearch/X-Pack 许可与版本演进不准确 | 按 Elasticsearch 当前许可与分发版本重写 | P1 |
| [C11.15](chapter-11-middleware-engineering.html#C11.15) | proto3 `optional`、gRPC 流控和代码生成版本细节不准确 | 按当前 protobuf/gRPC 插件验证示例 | P1 |
| [C11.16](chapter-11-middleware-engineering.html#C11.16) | Nacos/Apollo 的一致性模型、推送机制和规模数据不准确 | 官方文档核对后删除无来源容量数字 | P1 |
| [C11.17](chapter-11-middleware-engineering.html#C11.17) | Flyway/Liquibase 的 checksum、锁、基线和回滚能力描述不完整 | 按当前版本重写迁移治理与不可回滚 DDL 策略 | P1 |
| [C11.18](chapter-11-middleware-engineering.html#C11.18) | RocketMQ 5.x 事务消息、延迟消息和客户端兼容性表述不完整 | 区分 4.x/5.x 架构与客户端协议 | P1 |
| [C11.19](chapter-11-middleware-engineering.html#C11.19) | eBPF 采集点、内核版本和安全边界过度泛化 | 明确 kernel/BTF/CO-RE 前提与 OTel 边界 | P1 |
| [C11.20](chapter-11-middleware-engineering.html#C11.20) | FinOps 与 HPA、调度器、存储成本的联动描述缺平台前提 | 拆分为云账单、K8s 成本模型和业务归因 | P2 |
| [C11.21](chapter-11-middleware-engineering.html#C11.21) | 与 C11.13 重复，且 Quartz/XXL-Job/Elastic-Job 现状需核对 | 合并重复卡并按社区维护状态更新 | P1 |

### chapter-12：AI 工程

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C12.01](chapter-12-ai-engineering.html#C12.01) | Spring AI 发布时间线与 Advisor/ChatClient API 不准确 | 固定 Spring AI 版本后重写架构与示例 | P0 |
| [C12.02](chapter-12-ai-engineering.html#C12.02) | RAG 指标、召回/精度定义、定价和 Agentic RAG 成本缺少来源或定义 | 建立评测集后给区间，不写无来源百分比 | P1 |
| [C12.03](chapter-12-ai-engineering.html#C12.03) | 量化后的字节数、维度与内存估算错误 | 按模型和量化格式计算，展示公式与容量假设 | P0 |
| [C12.06](chapter-12-ai-engineering.html#C12.06) | Function Calling SDK 方法名与回调注册疑似伪造 | 用目标 Spring AI 版本重建可编译示例 | P0 |
| [C12.07](chapter-12-ai-engineering.html#C12.07) | MCP/Agent 框架协议版本与能力边界超前或混用 | 按 MCP 规范与具体框架版本区分传输、工具和资源 | P1 |
| [C12.13](chapter-12-ai-engineering.html#C12.13) | LangChain4j 定位与 Spring AI 边界描述不当 | 改为多模型抽象/生态差异，不写成 Spring AI 子集或替代品 | P1 |
| [C12.16](chapter-12-ai-engineering.html#C12.16) | `stream()`、Flux、SSE 端点和错误信号的组合不严谨 | 用 WebFlux/WebMVC 各自当前 API 分别验证 | P1 |
| [C12.21](chapter-12-ai-engineering.html#C12.21) | Milvus/BufferOverflowStrategy 等参数和 API 无效；性能结论过强 | 按 Milvus/Qdrant 当前 SDK 重写，并删除精确 QPS/延迟承诺 | P0 |
| [C12.25](chapter-12-ai-engineering.html#C12.25) | SSE 断连恢复、幂等 ID、背压与代理缓冲边界不完整 | 补充 Last-Event-ID、去重、超时和重放策略 | P1 |
| [C12.26](chapter-12-ai-engineering.html#C12.26) | 语义缓存的相似度阈值、命中一致性和失效策略描述过简 | 增加缓存键、模型/版本失效、隐私与命中率评估 | P1 |
| [C12.29](chapter-12-ai-engineering.html#C12.29) | LLM 评测指标与 CI 卡门阈值缺少统计前提 | 定义数据集、指标方差、显著性与人工评审比例 | P1 |
| [C12.31](chapter-12-ai-engineering.html#C12.31) | 会话存储、脱敏、留存与跨区域合规被过度泛化 | 标注法规、数据边界、加密和模型供应商数据处理差异 | P1 |

### chapter-13：网络与高性能 IO

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C13.02](chapter-13-network-io.html#C13.02) | TCP 状态机、TIME_WAIT 语义和重传细节过度简化 | 区分主动关闭方、端口复用、内核参数与负载均衡影响 | P1 |
| [C13.03](chapter-13-network-io.html#C13.03) | HTTP/2、HTTP/3、QUIC 和 TLS 集成的时间线与能力边界不准确 | 按 RFC 和主流网关/浏览器支持重写 | P1 |
| [C13.04](chapter-13-network-io.html#C13.04) | TLS 1.2/1.3 握手、前向安全和证书验证细节混杂 | 分开协议握手、密钥调度、SNI/ALPN 与证书链校验 | P1 |
| [C13.05](chapter-13-network-io.html#C13.05) | Linux Selector/epoll 与 Java NIO 语义被过度对应 | 区分就绪集合、事件丢失/重复、空轮询补丁和平台差异 | P1 |
| [C13.06](chapter-13-network-io.html#C13.06) | Netty backlog、EventLoop 绑定和 Pipeline 传播描述需按当前版本核对 | 以 Netty 当前源码示例验证配置名与异常传播 | P1 |
| [C13.07](chapter-13-network-io.html#C13.07) | ByteBuf 历史、池化分配器与泄漏检测级别不准确 | 按当前 Netty 版本重写 `ResourceLeakDetector` 与 refCnt 排查 | P1 |
| [C13.08](chapter-13-network-io.html#C13.08) | sendfile、mmap、kTLS 与 `FileChannel.map()` 的平台/API 条件混写 | 分别标注 OS、JDK、文件系统、加密与零拷贝生效条件 | P1 |
| [C13.11](chapter-13-network-io.html#C13.11) | io_uring 参数、提交/完成队列与 Project Loom 关系混淆 | 删除“Loom 依赖 io_uring”暗示，按内核和 JDK 独立描述 | P1 |
| [C13.12](chapter-13-network-io.html#C13.12) | 系统调用、用户态/内核态切换与 Java IO 模型映射过强 | 用调用链路图区分 blocking/NIO/sendfile 的真实内核路径 | P1 |

### chapter-14：数据库与存储

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C14.01](chapter-14-databases.html#C14.01) | MongoDB/WiredTiger、分片事务、oplog 和选举机制细节不准确 | 按当前 MongoDB 版本核对事务、写关注、分片元数据 | P1 |
| [C14.02](chapter-14-databases.html#C14.02) | Atlas Vector Search 与 Spring AI/Mongo driver API 不准确；过滤和 ANN 性能结论无来源 | 按官方 aggregation 和目标 Spring AI 版本重建示例 | P0 |
| [C14.03](chapter-14-databases.html#C14.03) | Milvus 组件职责、索引参数和 SDK 方法需按当前版本核对 | 用 Milvus 2.x 当前 SDK/REST 校验所有字段 | P0 |
| [C14.04](chapter-14-databases.html#C14.04) | Qdrant payload 索引、过滤模式和客户端 API 与当前版本不一致 | 按官方 client 重写 pre-filter、payload index 和 HNSW 参数 | P1 |
| [C14.05](chapter-14-databases.html#C14.05) | TiDB/TiFlash/OceanBase 事务与副本协议细节过度简化或错误 | 按各数据库当前架构文档重写 HTAP 与复制模型 | P1 |
| [C14.06](chapter-14-databases.html#C14.06) | ClickHouse 版本、MergeTree 行为和物化视图一致性描述不准确 | 按当前 ClickHouse 版本核对最终一致性和后台 merge | P1 |
| [C14.07](chapter-14-databases.html#C14.07) | Neo4j Cypher、APOC 可用性和执行计划描述需核对 | 标注数据库/APOC 版本，并用 EXPLAIN 验证 | P1 |
| [C14.08](chapter-14-databases.html#C14.08) | CockroachDB/YugabyteDB/OceanBase/TiDB 能力对比缺版本边界 | 建立版本化选型矩阵，删除“全面更优”结论 | P1 |
| [C14.09](chapter-14-databases.html#C14.09) | InfluxDB/TimescaleDB 架构、压缩和高基数建议不一致 | 按当前版本重写模型与保留策略 | P1 |

### chapter-15：响应式编程

| 位置 | 问题 | 修复建议 | 优先级 |
|---|---|---|---|
| [C15.01](chapter-15-reactive.html#C15.01) | Reactor 调度器切换、背压请求传播与 MDC/Hooks 机制混写 | 分别绘制 `publishOn`/`subscribeOn`、request 传播与 context 传播 | P0 |
| [C15.02](chapter-15-reactive.html#C15.02) | WebFlux 与 MVC 的阻塞依赖、连接池和吞吐结论过强 | 改为依赖画像、SSE/流式、阻塞隔离与迁移成本矩阵 | P1 |
| [C15.03](chapter-15-reactive.html#C15.03) | R2DBC 连接属性、事务传播和批量操作 API 不准确 | 按目标 R2DBC driver 和 Spring Data R2DBC 版本验证 | P1 |
| [C15.04](chapter-15-reactive.html#C15.04) | 错误传播方向、retry 与 `onErrorResume` 位置关系不清；BlockHound 配置不完整 | 用异常信号图重写，并区分开发期检测与生产熔断 | P1 |
| [C15.05](chapter-15-reactive.html#C15.05) | 虚拟线程开关、阻塞驱动兼容性和响应式迁移结论过度绝对化 | 按具体容器、JDBC、Redis 客户端和线程模型分别评估 | P1 |
| [C15.06](chapter-15-reactive.html#C15.06) | 手动 `subscribe()` 破坏 WebFlux 请求绑定契约；响应式事务边界描述不足 | 删除控制器手动订阅示例，改用返回 Publisher 的事务模板 | P0 |

## 4. 跨章节共性问题

1. **版本归属错误**：同一能力经常同时写 Framework、Spring Boot、JDK、Redis、MySQL 的版本，但没有标明约束，例如 Spring 自动配置、Security 过滤器、MySQL INSTANT DDL、Redis lazy-free。
2. **API 无法验证**：AI 工程、微服务、Security 和中间件章节存在疑似不存在的方法、starter、配置项和回调类，必须按项目锁定版本重写示例。
3. **无来源精确量化**：QPS、延迟、内存下降率、命中率、容量上限频繁出现精确值，但没有压测环境、数据规模、版本和日期，不适合面试材料。
4. **结构性粘贴错误**：chapter-05、chapter-06、chapter-07、chapter-09 和部分扩展补全段落存在重复追问、尾部拼接、表格断裂或主题漂移。
5. **“必须/一定/首选/淘汰”过强**：缓存一致性、事务选型、响应式选型、数据库选型和多活架构中的绝对结论应改为场景、SLA 和一致性等级驱动的矩阵。
6. **扩展补全稀释主卡**：不少尾部扩展内容已变成第二张卡，导致面试卡片阅读成本上升。建议拆卡或压缩为一到两个追问。

## 5. 修复顺序建议

1. **第一批：阻断事实与不可运行代码**。先修 C06、C07、C08、C09、C12 中的 P0，所有示例必须按目标版本编译或用 CLI 执行验证。
2. **第二批：生产误导项**。修复 K8s、Security、分布式锁、Kafka 事务、缓存一致性和向量库 API。
3. **第三批：版本与版本时间线**。逐章建立“JDK / Spring Boot / MySQL / Redis / 中间件 / SDK”版本表，删除无法核对的 release 时间。
4. **第四批：结构与重复卡**。合并 C11.13/C11.21 等重复主题，清理 chapter-05/06/07 的粘贴错位。
5. **第五批：量化口径**。删除或降级无来源数字，统一为“经验区间 + 压测模板 + 业务前提”。

## 6. 审查边界

- 本报告基于章节 HTML 提取出的文本索引完成，未运行章节内代码。
- 未访问网络，因此所有外部版本问题以官方文档复核为最终修复条件。
- `chapter-core-methodology.html`、`chapter-overview-priority.html`、`chapter-questions-eight-part.html`、`chapter-questions-scenario.html`、`chapter-server-security-checkpoint.html` 不在本次 15 章范围内。
