# Java 架构师面试问答复习知识点 — 实施方案（v2）

## 一、需求概述

以简历 `陈俊兵-Java架构师简历.md` 技术栈为起点，在项目根目录下生成分篇的面试问答复习知识点（HTML 格式），每篇独立文件。

**核心要求**：
- 以第一性原理直击问题根本，拒绝泛泛而谈
- 要深入、要归纳总结、要指明方向
- 每篇独立 HTML 文件，共享统一设计系统
- **框架不局限于某一版本**：覆盖 Spring Boot 2.x/3.x、Java 8/11/17/21+，注重原理而非版本绑定
- **知识点不限于简历内容**：以简历技术栈为锚点，向 Java 高级开发/架构师 2026 面试招聘需求全面拓展
- **双层级覆盖**：既包含高级开发必会的实战编码、框架使用、问题排查内容，也包含架构师的系统设计、权衡取舍、演进规划内容
- **演进脉络与发展趋势**：对 Spring 框架家族、JVM GC 收集器、Java 并发模型、数据库架构等核心主题，给出从起源到现状的演进路线与未来趋势，帮助理解"为什么是这样"而非仅"现在是什么"
- **基于 2026 面试趋势**：覆盖 Virtual Threads、GraalVM Native Image、OpenTelemetry 可观测性、云原生/K8s、系统设计实战、Agent/MCP 等 2026 年高频新方向

## 二、2026 面试趋势调研结论

基于 2025-2026 年大厂（阿里、字节、腾讯、京东、美团等）真实面试趋势调研 [$TRAE_REF](https://blog.csdn.net/likuoelie/article/details/157969239)：

| 趋势 | 说明 |
|------|------|
| 八股文占比下降 | 真实场景 + 取舍能力 + 系统设计占比上升 |
| 分布式深度必考 | 分布式事务、缓存一致性、流量治理仍是重灾区 |
| 可观测性兴起 | OpenTelemetry、Trace/Metrics/Log、混沌工程开始频繁出现 [$TRAE_REF](https://m.toutiao.com/group/7611089387246256640/) |
| Java 21 新特性 | Virtual Threads（Project Loom）成为高频考点 [$TRAE_REF](https://blog.csdn.net/cxyxysam/article/details/159544247) |
| 云原生架构 | K8s、Service Mesh、GraalVM Native Image 成为架构师必备 [$TRAE_REF](https://springdoc.cn/spring-boot-3-2-with-virtual-threads-and-graalvm-out-of-the-box/) |
| 系统设计实战 | 秒杀系统、消息系统、短链服务、登录认证系统为高频开放题 |
| AI 工程化 | Spring AI、RAG、Function Calling、Agent 框架成为新方向 |
| 架构演进思维 | 架构文档、演进路径、风险评估、技术债治理终面必问 |

## 三、当前状态分析

### 简历技术栈（作为锚点，非边界）

| 维度 | 简历技术点 | 2026 拓展方向 |
|------|-----------|---------------|
| 后端框架 | Spring Boot 2.x、Spring、SpringMVC、MyBatis | Spring Boot 3.x、Spring Framework 6、GraalVM AOT、Native Image |
| 数据存储 | MySQL、MongoDB、Redis | NewSQL（TiDB）、Elasticsearch、ClickHouse、多级缓存 |
| 中间件 | Spring Session、OAuth、Activiti、QLExpress | Kafka、RocketMQ、OpenTelemetry、Service Mesh |
| AI 技术 | Spring AI、LLM、Prompt、RAG | Function Calling、Agent 框架、MCP 协议、向量数据库 |
| 工程化 | Jenkins、Maven、APM | GitOps、ArgoCD、K8s、可观测性体系 |
| 并发 | 多线程、Redis 缓存 | Virtual Threads、响应式编程、协程模型 |
| 架构 | 微内核+插件、性能优化 | 云原生架构、系统设计、高可用设计、架构演进 |

### 输出目录

`/Users/chenjunbing/Develop/Project/Personal/Java Spring AI/java-architect-interview/`

## 四、章节规划（12 篇 + 1 导航页）

| 篇号 | 文件名 | 主题 | 题目数 | 核心覆盖 |
|------|--------|------|--------|----------|
| 导航 | `index.html` | 总览导航页 | — | 12 篇卡片入口 + 技术栈全景图 |
| 第1篇 | `chapter-01-jvm-memory-classloading.html` | JVM 内存与类加载 | 8 | 运行时数据区、OOM 场景、直接内存与 NIO、类加载机制、双亲委派、打破场景、JMM happens-before、内存模型设计动机 |
| 第2篇 | `chapter-02-gc-performance.html` | GC 算法与性能调优 | 10 | GC Roots、三种 GC 算法、收集器演进(Serial→ZGC)、JVM 参数调优、CPU 100% 排查、FullGC 排查、内存泄漏、JFR/Arthas、线上调优实战、性能分析工具演进 |
| 第3篇 | `chapter-03-concurrency-locks.html` | 并发编程与锁机制 | 10 | JMM、volatile 内存屏障、synchronized 锁升级、AQS(CAS+CLH)、ConcurrentHashMap、ReentrantLock、Condition、并发集合、ForkJoin、CAS 与 ABA |
| 第4篇 | `chapter-04-threadpool-virtual-threads.html` | 线程池与虚拟线程 | 8 | 线程池 7 参数、拒绝策略、ThreadLocal、Virtual Threads(Java 21)、Spring Boot 集成、CompletableFuture、响应式编程(WebFlux)、结构化并发 |
| 第5篇 | `chapter-05-spring-core.html` | Spring 核心原理 | 10 | IoC/Bean 生命周期、三级缓存循环依赖、AOP 代理、事务传播、事件机制、设计模式、BeanPostProcessor 扩展点、BeanFactory vs ApplicationContext、类型转换、SpEL |
| 第6篇 | `chapter-06-spring-boot-modern.html` | Spring Boot 与现代框架 | 10 | 自动配置 SPI、AOT/GraalVM Native Image、Starter 设计、Spring Security、Spring AI 架构、Spring Session、Actuator、配置管理、异常处理、Spring 验证 |
| 第7篇 | `chapter-07-mysql-deep.html` | MySQL 深度原理 | 10 | B+树索引、MVCC、锁机制、Redo/Undo/Binlog、SQL 调优、索引优化、分库分表、主从复制、高可用(MGR/MHA)、执行计划 |
| 第8篇 | `chapter-08-redis-cache.html` | Redis 与缓存架构 | 10 | 数据结构、持久化(RDB/AOF/混合)、缓存穿透/击穿/雪崩、缓存一致性、Redisson 分布式锁、多级缓存、Redis Cluster、过期策略、内存淘汰、布隆过滤器 |
| 第9篇 | `chapter-09-distributed-systems.html` | 分布式系统 | 10 | CAP/BASE、分布式事务(2PC/TCC/Seata/SAGA)、分布式锁、Kafka 深度、消息积压处理、分布式 ID、一致性哈希、幂等设计、分布式缓存、消息可靠性 |
| 第10篇 | `chapter-10-microservice-cloud.html` | 微服务与云原生 | 10 | 服务注册发现、API 网关、限流熔断降级、K8s 部署、Service Mesh、架构演进路径、高可用设计、配置中心、灰度发布、Serverless |
| 第11篇 | `chapter-11-middleware-engineering.html` | 中间件与工程化 | 10 | Activiti 工作流、流程配置化、QLExpress/Drools 规则引擎、OAuth 2.1、JWT、CI/CD 流水线、APM 系统设计、OpenTelemetry、TraceId 透传、混沌工程 |
| 第12篇 | `chapter-12-ai-engineering.html` | AI 工程与实践 | 10 | Spring AI 架构、RAG 全流程、向量检索、文档分块、Prompt 工程、Function Calling、Agent/MCP、LLM 评估、成本优化、多模态与未来趋势 |

**内容总量**：约 116 道深度 Q&A，约 55 个技术图表（Mermaid 约 35 个 + ECharts 约 20 个）。

## 五、每道 Q&A 的六层结构

每道问答严格遵循以下层次，确保深度、系统性和演进视角：

1. **本质问题**：这道题在考察什么核心能力（一句话点题）
2. **演进脉络**：该技术/机制的起源 → 各版本演进 → 现状 → 未来趋势。回答"为什么演变成现在这样"而非仅"现在是什么"
3. **第一性原理**：从底层机制/数学原理/源码层面解释当前版本的实现原理
4. **工程实践**：在实际项目中如何应用（关联简历项目经验 + 2026 行业实践），区分高级开发的编码实战与架构师的设计决策
5. **深度追问**：面试官可能的进阶问题与应答思路
6. **常见陷阱**：容易答错或答浅的点

### 难度标签体系（双层级）

| 标签 | 颜色 | 定位 | 典型特征 |
|------|------|------|----------|
| `高级开发` | 蓝色 accent | 3-5 年经验必会 | 框架使用、编码实战、问题排查、性能调优、常见模式 |
| `架构级` | 紫色 accent2 | 5-10 年经验必会 | 系统设计、权衡取舍、演进规划、技术选型、高可用设计 |
| `专家级` | 渐变(蓝→紫) | 资深架构师/技术专家 | 底层源码、原理创新、前沿趋势、复杂场景综合决策 |

每篇保证高级开发题占 40-50%、架构级题占 40-50%、专家级题占 10-20%，确保双层级覆盖。

### 演进脉络重点覆盖

| 技术主题 | 演进路线 | 趋势方向 |
|----------|----------|----------|
| JVM GC | Serial → Parallel → CMS → G1 → ZGC → Shenandoah → Generational ZGC(JDK21) | 从吞吐优先 → 低延迟 → 无停顿 |
| Java 并发 | Thread → Executor → ForkJoin → CompletableFuture → Virtual Threads → Structured Concurrency | 从手动管理 → 池化 → 异步组合 → 轻量级线程 → 结构化并发 |
| Spring 框架 | Spring 2.x(XML) → 3.x(注解) → 4.x(Boot) → 5.x(响应式) → 6.x(AOT/Native) | 从配置繁重 → 约定优于配置 → 原生编译 |
| Spring Boot | 1.x → 2.x(响应式) → 3.x(GraalVM/Virtual Threads/Java17+) | 从开发友好 → 生产优化 → 云原生 |
| 数据库 | 单机 MySQL → 主从 → 读写分离 → 分库分表 → NewSQL(TiDB/Spanner) | 从单点 → 分布式 → 云原生数据库 |
| 微服务 | 单体 → SOA → 微服务 → Service Mesh → Serverless | 从库侵入 → Sidecar → 平台能力下沉 |
| 可观测性 | 日志 → APM(SkyWalking/Pinpoint) → OpenTelemetry → eBPF | 从碎片化 → 标准化 → 内核级无侵入 |

### 简历关联策略

简历技术栈作为实践案例融入各篇，体现"知行合一"，但知识点本身不受简历边界限制：

| 章节 | 关联简历点 | 拓展方向 |
|------|-----------|----------|
| 第1篇 | MySQL/MongoDB 慢查询治理 | 线上问题定位全流程(Arthas/JFR/MAT) |
| 第2篇 | 多线程车辆租赁业务 | Virtual Threads 重构传统线程模型 |
| 第3篇 | Spring Boot 项目架构 | Boot 3.x 迁移、GraalVM Native Image |
| 第4篇 | MySQL/MongoDB 慢查询优化 | 缓存一致性、多级缓存架构 |
| 第5篇 | 自研 APM 全链路监控 | OpenTelemetry 标准化可观测性 |
| 第6篇 | 公共组件平台化 | 微服务拆分、K8s 部署、系统设计 |
| 第7篇 | Activiti/QLExpress/OAuth/Spring AI | 现代中间件选型、AI 工程化 |

## 六、目录结构

```
java-architect-interview/
├── index.html                                      # 导航首页
├── chapter-01-jvm-memory-classloading.html         # JVM 内存与类加载（8题）
├── chapter-02-gc-performance.html                  # GC 算法与性能调优（10题）
├── chapter-03-concurrency-locks.html               # 并发编程与锁机制（10题）
├── chapter-04-threadpool-virtual-threads.html       # 线程池与虚拟线程（8题）
├── chapter-05-spring-core.html                     # Spring 核心原理（10题）
├── chapter-06-spring-boot-modern.html              # Spring Boot 与现代框架（10题）
├── chapter-07-mysql-deep.html                      # MySQL 深度原理（10题）
├── chapter-08-redis-cache.html                     # Redis 与缓存架构（10题）
├── chapter-09-distributed-systems.html             # 分布式系统（10题）
├── chapter-10-microservice-cloud.html              # 微服务与云原生（10题）
├── chapter-11-middleware-engineering.html           # 中间件与工程化（10题）
├── chapter-12-ai-engineering.html                  # AI 工程与实践（10题）
├── assets/
│   ├── design-system.css                           # 共享设计系统
│   ├── charts-01.js ~ charts-12.js                 # 各篇 ECharts 逻辑
│   └── nav.js                                      # 导航交互逻辑
└── _shared/
    ├── js/
    │   ├── echarts.min.js                          # 数据图表库
    │   └── mermaid.min.js                          # 结构图库
    └── fonts/
        ├── WorkSans-Regular.ttf                    # 正文+标题
        ├── WorkSans-Bold.ttf
        ├── WorkSans-Italic.ttf
        └── JetBrainsMono-Regular.ttf               # 代码块
```

## 七、设计系统

### 风格定位

冷峻技术文档风格，大量留白，等宽字体点缀，知识密度高。采用 Solid 模式（非渐变），保证代码与图示的可读性。

### 调色板

```css
:root {
  --bg: #fafbfc;        /* 页面底色 */
  --bg2: #f0f3f7;       /* 卡片/代码块底色 */
  --ink: #1a1f36;       /* 正文 */
  --muted: #6b7280;     /* 次要文字 */
  --rule: #e2e8f0;      /* 分割线/边框 */
  --accent: #2563eb;    /* 主强调色（Java蓝） */
  --accent2: #7c3aed;   /* 次强调色（紫色/AI标记） */
  --code-bg: #1e293b;   /* 代码块深色底 */
  --code-ink: #e2e8f0;  /* 代码块文字 */
  --success: #059669;   /* 最佳实践 */
  --warn: #d97706;      /* 警告/陷阱 */
  --danger: #dc2626;    /* 错误/反模式 */
}
```

### 排版与布局

- 标题/正文字体：WorkSans（几何无衬线，现代技术感）
- 等宽字体：JetBrainsMono（代码、技术术语）
- 正文字号：16px，行高 1.75
- 最大宽度：920px，单列居中 + 桌面端右侧 sticky 侧边栏 TOC
- 标题风格：加粗左对齐，h2 底部 2px accent 色横线

### 核心组件

| 组件 | 用途 | 样式 |
|------|------|------|
| `.qa-card` | 单道问答卡片 | bg2 填充，左侧 4px accent 色条，radius 8px |
| `.qa-question` | 问题标题 | 加粗 18px，前缀"Q"用 accent 色圆形徽章 |
| `.code-block` | Java 代码块 | 深色底，JetBrainsMono，手动 span 着色关键字 |
| `.callout-tip` | 最佳实践 | 左边框 4px success 色 |
| `.callout-pitfall` | 常见陷阱 | 左边框 4px warn 色 |
| `.callout-deep` | 深度追问 | 左边框 4px accent2 色 |
| `.compare-table` | 对比表格 | 表头 accent 色底白字 |
| `.difficulty` | 难度标签 | 圆角小徽章（基础/进阶/架构级） |
| `.chapter-nav` | 章节间导航 | 底部上一篇/下一篇按钮 |

## 八、各篇内容大纲

> **说明**：每道 Q&A 均包含六层结构（本质→演进脉络→第一性原理→工程实践→深度追问→常见陷阱），下表仅列问题标题与核心要点。难度标签：`[高]`=高级开发、`[架]`=架构级、`[专]`=专家级。每篇难度分布约 4:4:2。

### 第1篇：JVM 内存与类加载（8题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 1.1 | [高] | JVM 运行时数据区如何划分？各区域作用与 OOM 场景？ | 堆/栈/方法区(元空间)/程序计数器/本地方法栈；直接内存与 NIO；**JDK6→8→17 永久代到元空间演进** | Mermaid: JVM 内存结构图 |
| 1.2 | [高] | 对象的创建过程与内存布局？ | 类加载检查→分配内存→零值初始化→设置对象头→构造方法；指针碰撞 vs 空闲列表；TLAB；Mark Word 结构 | Mermaid: 对象内存布局图 |
| 1.3 | [高] | 类加载机制与双亲委派模型为何被设计成这样？ | 加载-验证-准备-解析-初始化；双亲委派安全性与隔离性；**打破场景演进(SPI/JDBC/Tomcat/JDK9模块化)** | Mermaid: 类加载器层次图 |
| 1.4 | [架] | JMM 的 happens-before 规则如何保证可见性与有序性？ | 主内存与工作内存；8种原子操作；happens-before 8条规则；指令重排与内存屏障；**JMM 设计动机与 MESI 协议** | Mermaid: JMM 内存交互图 |
| 1.5 | [高] | 内存溢出(OOM)与内存泄漏的区别与排查？ | OOM 类型(堆/元空间/直接内存)；泄漏模式(静态集合/ThreadLocal/监听器)；jmap+MAT 精确定位 | 代码块: 内存泄漏代码模式 |
| 1.6 | [架] | 直接内存(Direct Memory)与 NIO 的关系？ | 堆外内存分配(ByteBuffer.allocateDirect)；零拷贝(sendfile/mmap)；DirectByteBuffer 回收机制；Netty 池化缓冲区 | Mermaid: NIO 零拷贝原理图 |
| 1.7 | [高] | Java 对象的引用类型与 GC 回收？ | 强/软/弱/虚引用；ReferenceQueue；SoftReference 缓存应用；WeakHashMap；Finalizer 的问题 | 表格: 四种引用对比 |
| 1.8 | [专] | JDK 9 模块系统(JPMS) 对类加载的影响？ | module-info.java；模块化与类加载器关系；对双亲委派的影响；反射访问限制；迁移挑战 | Mermaid: JPMS 模块依赖图 |

### 第2篇：GC 算法与性能调优（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 2.1 | [高] | GC Roots 可达性分析与三种 GC 算法的本质权衡？ | 根对象枚举(GC Roots 类型)；标记-清除(碎片)/复制(空间)/标记-整理(STW)；分代收集理论依据 | ECharts: 三种算法多维对比雷达图 |
| 2.2 | [专] | CMS/G1/ZGC/Shenandoah 四个收集器的核心差异与选型？ | **完整演进：Serial→Parallel→CMS→G1→ZGC→Shenandoah→Generational ZGC(JDK21)**；染色指针/读屏障/转发指针；停顿时间模型 | Mermaid: GC 收集器演进时间线 + G1 Region 布局图 |
| 2.3 | [架] | JVM 参数如何设置？年轻代/老年代/GC 如何选？ | -Xms=-Xmx；**G1(默认)/ZGC(大堆)/Shenandoah 选型决策树**；MaxGCPauseMillis；IHOP；**JDK8→21 默认 GC 变迁** | 表格: JVM 参数调优对照表 |
| 2.4 | [高] | 线上 CPU 100% 如何快速定位与解决？ | top→top -Hp→jstack→线程dump；Arthas dashboard/thread/trace；**从jstack到Arthas到async-profiler工具演进** | 代码块: Arthas 诊断命令序列 |
| 2.5 | [架] | 线上 FullGC 频繁如何排查与调优？ | jstat GC统计；jmap dump+MAT；GC日志+GCEasy；**不同GC收集器的调优参数差异**；常见原因 | ECharts: GC 日志分析示意 |
| 2.6 | [高] | 如何选择 GC 收集器？各场景的推荐配置？ | 小堆(Parallel)/中堆(G1)/大堆(ZGC/Shenandoah)；低延迟 vs 高吞吐；**GC 选型决策矩阵** | 表格: GC 收集器场景选型表 |
| 2.7 | [高] | Arthas 的核心命令与线上诊断实战？ | dashboard/jad/watch/trace/stack；热更新(redefine)；**从BTrace到Arthas到JFR到eBPF的工具演进** | 代码块: Arthas 实战命令集 |
| 2.8 | [专] | JDK Flight Recorder(JFR) 与异步 profiling 如何用于性能分析？ | JFR 低开销采集；事件模型(GC/分配/锁/IO)；async-profiler 火焰图；**性能分析工具演进趋势** | Mermaid: JFR 架构与采集流程图 |
| 2.9 | [架] | 如何进行 JVM 线上调优全流程？ | 监控告警→问题定位→参数调整→灰度验证→全量发布；**调优方法论与常见陷阱**；容量规划 | Mermaid: JVM 调优全流程图 |
| 2.10 | [高] | 逃逸分析与标量替换如何优化对象分配？ | 逃逸分析(方法内/线程内逃逸)；栈上分配；标量替换；同步消除；**JIT 编译优化层级** | Mermaid: 逃逸分析决策树 |

### 第3篇：并发编程与锁机制（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 3.1 | [高] | volatile 如何保证可见性？为何不能保证原子性？ | 内存屏障(LoadLoad/StoreStore/LoadStore/StoreLoad)；禁止重排；DCL单例；MESI协议 | 代码块: DCL 单例示例 |
| 3.2 | [高] | synchronized 的锁升级过程是怎样的？ | 偏向锁→轻量级锁→重量级锁；Mark Word结构；**锁升级演进动机与JDK15偏向锁废弃** | ECharts: 锁状态对比表 |
| 3.3 | [专] | AQS 的 CLH 队列与 CAS 如何实现同步？ | state变量；CLH变体队列；独占/共享模式；**JUC同步器框架设计哲学**；ReentrantLock实现 | Mermaid: AQS 队列结构图 |
| 3.4 | [高] | CAS 与 ABA 问题如何解决？ | Unsafe.compareAndSwap；ABA问题；AtomicStampedReference；AtomicMarkableReference；**CAS的局限性** | 代码块: CAS 与 ABA 解决示例 |
| 3.5 | [高] | ReentrantLock 与 synchronized 如何选择？ | 可中断/超时/公平锁/条件变量；**从synchronized到ReentrantLock到StampedLock的锁演进**；性能对比 | 代码块: ReentrantLock vs synchronized |
| 3.6 | [高] | ConcurrentHashMap 的并发安全如何保证？ | **JDK7分段锁→JDK8 CAS+synchronized演进**；Node数组+链表/红黑树；sizeCtl；counterCell | Mermaid: ConcurrentHashMap 结构演进图 |
| 3.7 | [架] | Condition 条件变量与 LockSupport 如何实现等待/通知？ | Condition.await/signal；LockSupport.park/unpark；与Object.wait/notify对比；生产消费模型 | 代码块: Condition 生产消费示例 |
| 3.8 | [高] | Java 并发集合有哪些？各自的使用场景？ | CopyOnWriteArrayList/ConcurrentLinkedQueue/BlockingQueue家族；**并发集合的演进与选型** | 表格: 并发集合对比 |
| 3.9 | [专] | ForkJoinPool 的分治与工作窃取算法？ | 分治任务模型；工作窃取(work-stealing)；ForkJoinPool vs ThreadPoolExecutor；**在Stream并行与Virtual Threads中的应用** | Mermaid: 工作窃取算法图 |
| 3.10 | [高] | 如何实现一个线程安全的计数器？ | synchronized/AtomicInteger/LongAdder；**从AtomicInteger到LongAdder的性能演进**；分段CAS | 代码块: 三种计数器实现对比 |

### 第4篇：线程池与虚拟线程（8题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 4.1 | [高] | 线程池 7 个参数如何调优？拒绝策略如何选？ | corePoolSize/maxPoolSize/queue/keepAlive/factory/handler；IO密集vs CPU密集；**美团动态调参方案** | 代码块: ThreadPoolExecutor + 动态调参 |
| 4.2 | [高] | 线程池的工作流程与状态流转？ | 核心线程→队列→最大线程→拒绝；RUNNING→SHUTDOWN→STOP→TIDYING→TERMINATED；**线程池状态机** | Mermaid: 线程池工作流程与状态图 |
| 4.3 | [高] | ThreadLocal 为何会内存泄漏？如何避免？ | ThreadLocalMap弱引用Key+强引用Value；remove()清理；**ThreadLocal→InheritableThreadLocal→TransmittableThreadLocal演进** | Mermaid: ThreadLocal 引用链图 |
| 4.4 | [架] | Virtual Threads(Java 21)如何重构并发模型？ | **完整演进：Thread→Executor→ForkJoin→CompletableFuture→Virtual Threads→Structured Concurrency**；平台线程vs虚拟线程；pinning问题 | Mermaid: Java 并发模型演进图 |
| 4.5 | [高] | Virtual Threads 在 Spring Boot 中如何落地？ | spring.threads.virtual.enabled=true；Tomcat线程池替换；**与传统线程池性能对比**；pinning排查 | 代码块: Virtual Thread 配置与对比 |
| 4.6 | [高] | CompletableFuture 如何编排异步任务？ | supplyAsync/thenApply/thenCompose/allOf/anyOn；**从Future到CompletableFuture的异步编排演进**；异常处理 | 代码块: CompletableFuture 链式编排 |
| 4.7 | [架] | 响应式编程(WebFlux)与传统 Servlet 模型的本质差异？ | **从Servlet到WebFlux到Virtual Threads的编程模型演进**；命令式vs声明式；Reactor背压；**Virtual Threads是否会取代响应式** | Mermaid: 三种并发模型对比图 |
| 4.8 | [专] | Structured Concurrency(结构化并发)如何管理并发任务？ | JDK21+ StructuredTaskScope；父子任务生命周期绑定；**从非结构化到结构化并发的演进趋势**；ShutdownOnFailure/ShutdownOnSuccess | 代码块: 结构化并发示例 |

### 第5篇：Spring 核心原理（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 5.1 | [高] | Spring IoC 容器的启动流程与 Bean 生命周期？ | BeanDefinition注册；实例化→属性填充→初始化→销毁；BeanPostProcessor扩展点 | Mermaid: Bean 生命周期全流程图 |
| 5.2 | [专] | 三级缓存如何解决循环依赖？为何需要三级？ | singletonObjects/earlySingletonObjects/singletonFactories；**Spring 6对循环依赖处理的变更**；构造器注入与@Lazy | Mermaid: 三级缓存交互时序图 |
| 5.3 | [高] | Spring AOP 的 JDK 动态代理与 CGLIB 如何选择？ | Proxy.newProxyInstance(接口)vs CGLIB(类)；代理链执行顺序；**从Spring AOP到AspectJ编译时织入演进** | 代码块: 两种代理实现对比 |
| 5.4 | [高] | @Transactional 的 7 种传播行为与失效场景？ | REQUIRED/REQUIRES_NEW/NESTED等；自调用失效(代理)；异常不匹配；**解决方案演进** | ECharts: 传播行为矩阵 |
| 5.5 | [高] | Spring 事件机制(ApplicationEvent)原理？ | ApplicationEventPublisher；事件广播器；**从ApplicationEvent到@EventListener到@TransactionalEventListener演进** | 代码块: 事件发布订阅示例 |
| 5.6 | [高] | Spring 中用到了哪些设计模式？ | 工厂/代理/单例/模板/观察者/责任链/适配器；**Spring框架设计模式应用全景** | 表格: 模式与Spring应用场景 |
| 5.7 | [架] | BeanPostProcessor 与 BeanFactoryPostProcessor 的区别与扩展？ | BPP(实例后扩展)vs BFPP(定义阶段扩展)；常用扩展点；**Spring扩展点体系与优先级** | Mermaid: Spring 扩展点时序图 |
| 5.8 | [高] | BeanFactory 与 ApplicationContext 的区别？ | BeanFactory(基础容器)vs ApplicationContext(企业级)；**从BeanFactory到ClassPathXmlApplicationContext到AnnotationConfigApplicationContext演进** | 表格: BeanFactory vs ApplicationContext |
| 5.9 | [高] | Spring 类型转换与数据绑定机制？ | PropertyEditor→Converter→Formatter演进；ConversionService；数据绑定(DataBinder)；验证(Validator) | 代码块: 自定义类型转换器 |
| 5.10 | [高] | SpEL(Spring表达式语言)的原理与应用？ | 解析器(ExpressionParser)；EvaluationContext；**SpEL在@Value/@Cache/@Conditional中的应用** | 代码块: SpEL 使用示例 |

### 第6篇：Spring Boot 与现代框架（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 6.1 | [高] | Spring Boot 自动配置的 SPI 机制如何工作？ | @EnableAutoConfiguration；**spring.factories(2.x)→AutoConfiguration.imports(3.x)演进**；@Conditional过滤；Starter设计 | Mermaid: 自动配置加载流程图 |
| 6.2 | [专] | Spring Boot 3.x 的 AOT 与 GraalVM Native Image 如何工作？ | **完整演进：JIT→AOT→GraalVM Native Image**；闭世界分析；反射/动态代理限制；**Spring Native到Boot3原生支持** | ECharts: JIT vs AOT vs Native 性能对比 |
| 6.3 | [高] | 如何设计一个自定义 Spring Boot Starter？ | 自动配置类+条件注解+配置属性；**Starter设计最佳实践**；与官方Starter的差异 | 代码块: 自定义 Starter 实现 |
| 6.4 | [架] | Spring Security 的过滤器链与认证授权流程？ | **从XML配置到DSL到Lambda DSL演进**；FilterChainProxy；SecurityFilterChain；JWT集成；OAuth2资源服务器 | Mermaid: Spring Security 过滤器链图 |
| 6.5 | [架] | Spring AI 的核心抽象与架构是怎样的？ | **Spring生态从Web到AI应用的演进**；ChatClient/ChatModel/EmbeddingModel/VectorStore；Advisor链 | Mermaid: Spring AI 架构分层图 |
| 6.6 | [高] | Spring Session 如何实现分布式 Session？ | **从Session到Spring Session到JWT的认证方案演进**；@EnableRedisHttpSession；Session事件；与OAuth整合 | 代码块: Spring Session 配置 |
| 6.7 | [高] | Spring Boot Actuator 的监控端点与自定义？ | 内置端点(health/info/metrics)；**从Actuator 1.x到2.x+的安全演进**；自定义HealthIndicator；Prometheus集成 | 代码块: Actuator 配置与自定义 |
| 6.8 | [高] | Spring Boot 的配置加载机制与优先级？ | 命令行参数 > 环境变量 > application.yml；profile机制；**配置加载优先级与覆盖规则**；配置加密 | 表格: 配置优先级对照表 |
| 6.9 | [高] | Spring Boot 全局异常处理如何设计？ | @ControllerAdvice+@ExceptionHandler；**从HandlerExceptionResolver到@ControllerAdvice的演进**；统一ApiResponse封装 | 代码块: 全局异常处理实现 |
| 6.10 | [高] | Spring Validation 数据校验机制？ | JSR-303注解(@NotNull/@Size等)；@Valid/@Validated；**从Hibernate Validator到Spring Validation的演进**；自定义校验器；分组校验 | 代码块: 校验注解与自定义校验器 |

### 第7篇：MySQL 深度原理（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 7.1 | [高] | InnoDB 的 B+树索引为何比 B树更适合数据库？ | B+树非叶子不存数据(扇出大)；叶子链表(范围查询)；**从B树到B+树到LSM树的索引结构演进**；聚簇vs二级索引；回表 | Mermaid: B+树结构图 |
| 7.2 | [专] | MVCC 如何实现 RC 和 RR 两种隔离级别？ | undo log版本链；read view生成时机；可见性判断；**隔离级别从锁到MVCC的演进**；快照读vs当前读 | Mermaid: MVCC 版本链与 ReadView 图 |
| 7.3 | [高] | InnoDB 的行锁/间隙锁/临键锁如何工作？ | 记录锁/间隙锁/临键锁；Next-Key Lock解决幻读；**不同隔离级别下的锁行为**；死锁检测与排查 | ECharts: 锁类型矩阵 |
| 7.4 | [架] | Redo Log、Undo Log 与 Binlog 如何协同保证 ACID？ | Redo(crash恢复,WAL)；Undo(回滚+MVCC)；Binlog(复制)；两阶段提交；**组提交与MySQL高可用复制演进(异步/半同步/MGR)** | Mermaid: 两阶段提交时序图 |
| 7.5 | [高] | 慢 SQL 如何排查与优化？ | EXPLAIN分析(type/key/rows/Extra)；索引失效(函数/隐式转换/最左前缀)；分页优化(延迟关联) | 代码块: EXPLAIN 分析示例 |
| 7.6 | [高] | 索引设计原则与优化策略？ | 最左前缀；覆盖索引；索引下推(ICP)；**从单列索引到联合索引到覆盖索引的优化演进**；前缀索引 | 表格: 索引优化策略对照表 |
| 7.7 | [架] | 分库分表如何设计与落地？ | 垂直拆分vs水平拆分；分片策略(范围/哈希/一致性哈希)；**从读写分离到分库分表到NewSQL的演进**；ShardingSphere | Mermaid: 分库分表架构图 |
| 7.8 | [高] | MySQL 主从复制原理与延迟优化？ | binlog→relay log→apply；**从异步到半同步到MGR的复制演进**；并行复制(MTS)；延迟排查与优化 | Mermaid: 主从复制架构图 |
| 7.9 | [架] | MySQL 高可用方案如何选型？ | MHA/Orchestrator/MGR/Group Replication；**MySQL高可用方案演进**；读写分离中间件；故障切换 | 表格: MySQL 高可用方案对比 |
| 7.10 | [高] | MySQL 的执行计划(EXPLAIN)如何解读？ | id/select_type/table/type/key/key_len/rows/Extra；**从EXPLAIN到EXPLAIN ANALYZE的演进**；优化器trace | 代码块: EXPLAIN 字段解读 |

### 第8篇：Redis 与缓存架构（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 8.1 | [高] | Redis 的 5+3 种数据结构与应用场景？ | String/List/Hash/Set/Zset + Stream/Bitmap/HyperLogLog；**Redis数据结构的演进**；底层数据结构(ziplist/skiplist/listpack) | 表格: 数据结构与应用场景 |
| 8.2 | [高] | Redis RDB 与 AOF 持久化的权衡？ | RDB(全量,fork)/AOF(增量,appendfsync)/混合持久化(4.0+)；**持久化从RDB到AOF到混合的演进**；fork对性能影响 | ECharts: 持久化方式多维度对比 |
| 8.3 | [高] | 缓存穿透/击穿/雪崩的区别与解决方案？ | 穿透(布隆过滤器)；击穿(互斥锁/逻辑过期)；雪崩(随机TTL/多级缓存)；**组合方案设计** | 表格: 三大问题对比 |
| 8.4 | [架] | 缓存与数据库一致性如何保证？ | Cache Aside；双写问题；延迟双删；Canal binlog订阅；**从双写到延迟双删到Canal订阅的方案演进** | Mermaid: 缓存一致性方案对比图 |
| 8.5 | [专] | Redisson 分布式锁如何实现可重入与看门狗？ | Lua脚本加锁；Hash记录重入；WatchDog续期；**从单节点到RedLock到Redisson的分布式锁演进**；Martin Kleppmann质疑 | 代码块: Redisson 加锁Lua脚本 |
| 8.6 | [架] | 多级缓存架构如何设计？ | 本地缓存(Caffeine)+Redis+DB；**从单层到多级缓存的架构演进**；缓存一致性；热点探测；缓存预热 | Mermaid: 多级缓存架构图 |
| 8.7 | [高] | Redis Cluster 的工作原理？ | 哈希槽(16384)；节点通信(gossip)；主从故障转移；**从主从到哨兵到Cluster的Redis架构演进**；脑裂问题 | Mermaid: Redis Cluster 架构图 |
| 8.8 | [高] | Redis 的过期策略与内存淘汰机制？ | 定期删除+惰性删除；**从noeviction到LRU到LFU的淘汰策略演进**；maxmemory配置；内存碎片 | 表格: 8种淘汰策略对比 |
| 8.9 | [高] | 布隆过滤器的原理与缓存穿透防护？ | 位数组+多个哈希函数；误判率与空间效率；**从布隆过滤器到布谷鸟过滤器到Counting Bloom Filter的演进** | Mermaid: 布隆过滤器原理图 |
| 8.10 | [架] | Redis 在高并发场景的常见问题与优化？ | 大Key/热Key问题；pipeline批量操作；Lua原子性；**Redis性能优化全链路**；集群扩缩容 | 表格: Redis 常见问题与优化 |

### 第9篇：分布式系统（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 9.1 | [架] | CAP 定理的证明与 BASE 理论如何指导实践？ | CP vs AP选择；分区容忍性P的必然性；BASE最终一致性；**业务场景取舍(支付CP/库存AP)** | Mermaid: CAP 三角图 |
| 9.2 | [专] | 分布式事务的 2PC/3PC/TCC/Seata AT/SAGA 原理与选型？ | **完整演进：2PC→3PC→TCC→Seata AT→SAGA→可靠消息**；空回滚/悬挂/幂等；**分布式事务方案选型决策** | ECharts: 方案多维度对比矩阵 |
| 9.3 | [架] | 分布式锁的三种实现(Redis/ZK/数据库)对比？ | Redis(setnx+RedLock争议)；ZK(临时顺序节点)；数据库(唯一索引)；**各自边界、性能与正确性权衡** | 表格: 三种方案对比 |
| 9.4 | [架] | Kafka 如何保证高吞吐、可靠投递与消息顺序？ | 分区并行+顺序写+零拷贝；ISR副本；acks/retry；Exactly-Once；**从ActiveMQ到RabbitMQ到Kafka到Pulsar的MQ演进** | Mermaid: Kafka 架构与ISR机制图 |
| 9.5 | [高] | 消息积压 1000 万条如何紧急处理？ | 扩消费组；跳过偏移量；暂停非核心；binlog回溯；**根因分析与预防** | 代码块: 消费积压处理脚本 |
| 9.6 | [架] | 分布式 ID 生成方案如何选型？ | UUID/雪花算法/号段模式(Leaf)/Redis INCR；**从UUID到雪花到号段到Leaf的演进**；时钟回拨 | Mermaid: 雪花算法结构图 |
| 9.7 | [高] | 一致性哈希如何解决分布式缓存的数据分布？ | 传统哈希取模扩容问题；一致性哈希环；虚拟节点；**Redis Cluster哈希槽vs一致性哈希对比** | Mermaid: 一致性哈希环图 |
| 9.8 | [高] | 接口幂等设计如何实现？ | 天然幂等(查询/删除)；唯一索引；Token机制；乐观锁；**幂等设计模式与适用场景** | 代码块: 幂等设计实现 |
| 9.9 | [架] | 消息队列如何保证可靠投递与顺序？ | 生产端确认+重试；存储持久化；消费端手动ACK；顺序(分区)；**消息可靠性全链路保障** | Mermaid: 消息可靠性投递流程图 |
| 9.10 | [高] | 分布式系统的拜占庭将军问题与共识算法？ | 拜占庭容错；Paxos/Raft/ZAB；**从Paxos到Raft到ZAB的共识算法演进**；Leader选举 | Mermaid: Raft 选举流程图 |

### 第10篇：微服务与云原生（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 10.1 | [高] | 微服务架构的服务注册发现与配置中心如何选型？ | Eureka(AP)/Nacos(AP+CP)/Consul(CP)/ZK(CP)；**从Eureka到Nacos到Service Mesh的演进** | Mermaid: 服务注册发现架构图 |
| 10.2 | [高] | API 网关在微服务中的核心职责？ | 路由/限流/熔断/鉴权/协议转换；**从Zuul到Gateway到APISIX的网关演进** | Mermaid: API 网关架构图 |
| 10.3 | [高] | 高并发系统的限流算法与熔断降级策略？ | 计数器/滑动窗口/漏桶/令牌桶；**从Hystrix到Resilience4j到Sentinel的熔断框架演进**；状态机 | ECharts: 限流算法对比 |
| 10.4 | [架] | 容器化与 Kubernetes 如何部署 Java 应用？ | Docker镜像分层；K8s Pod/Deployment/Service/Ingress；**JVM容器感知从Java8到10+演进**；优雅停机 | Mermaid: K8s 部署架构图 |
| 10.5 | [专] | Service Mesh(Istio) 如何解耦微服务治理？ | **完整演进：单体→SOA→微服务→Service Mesh→Serverless**；Sidecar；Istiod；**从库侵入到Sidecar到平台下沉** | Mermaid: 微服务演进图 + Service Mesh架构 |
| 10.6 | [架] | 单体到微服务的架构演进路径如何规划？ | 何时拆/怎么拆(DDD,绞杀者模式)；**模块化单体过渡**；数据库先行vs服务先行；技术债治理 | Mermaid: 架构演进路线图 |
| 10.7 | [架] | 高可用架构设计的核心原则与实践？ | 冗余/故障隔离/故障转移/降级预案；异地多活；**混沌工程(Chaos Monkey→ChaosBlade)** | Mermaid: 高可用架构设计框架图 |
| 10.8 | [高] | 微服务配置中心的设计与选型？ | Nacos Config/Apollo/Config Server；**配置中心演进**；配置热更新；灰度发布配置 | Mermaid: 配置中心架构图 |
| 10.9 | [架] | 灰度发布与蓝绿部署如何设计？ | 蓝绿/金丝雀/灰度(流量染色)；**发布策略演进**；全链路灰度；回滚机制 | Mermaid: 灰度发布架构图 |
| 10.10 | [架] | Serverless 架构的适用场景与挑战？ | FaaS+BaaS；冷启动；**从IaaS到PaaS到Serverless的云计算演进**；Java在Serverless中的挑战 | Mermaid: 云计算演进图 |

### 第11篇：中间件与工程化（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 11.1 | [高] | 工作流引擎(Activiti)的 BPMN 2.0 模型与执行原理？ | 流程定义/部署/实例/任务；BPMN元素；**从jBPM到Activiti到Flowable到Camunda的演进** | Mermaid: Activiti 引擎架构图 |
| 11.2 | [高] | 如何实现流程节点的批量配置化？ | 动态表单+流程变量；任务监听器；节点属性配置化；**配置驱动vs代码驱动** | 代码块: 流程配置化实现 |
| 11.3 | [架] | 规则引擎(QLExpress/Drools)的执行原理与选型？ | QLExpress AST编译；Drools Rete算法；**从硬编码到脚本到规则引擎到决策引擎的演进** | Mermaid: 规则引擎执行流程图 |
| 11.4 | [高] | OAuth 2.1 四种授权模式的流程与安全考量？ | **从OAuth1.0到2.0到2.1的演进**；授权码+PKCE；隐式/密码废弃；令牌刷新与吊销 | Mermaid: 授权码+PKCE 时序图 |
| 11.5 | [高] | JWT 的结构与安全实践？ | Header.Payload.Signature；续期与吊销；**从Session到JWT到双Token的认证演进**；JWS vs JWE | 代码块: JWT 结构解析 |
| 11.6 | [架] | CI/CD 流水线如何设计标准化？ | Jenkinsfile/GitLab CI；多环境部署；蓝绿/灰度/金丝雀；**从Jenkins到GitLab CI到GitOps(ArgoCD)的演进** | Mermaid: CI/CD 演进图 + 流水线图 |
| 11.7 | [专] | APM 全链路监控系统的架构如何设计？ | 微内核+插件；Java Agent+Instrumentation；**从字节码增强到OpenTelemetry到eBPF的监控技术演进** | Mermaid: APM 系统架构图 |
| 11.8 | [高] | 全链路 TraceId 如何在多线程与跨服务间透传？ | ThreadLocal/MDC；线程池TaskDecorator；W3C TraceContext；**Virtual Thread兼容** | 代码块: TraceId 透传实现 |
| 11.9 | [专] | OpenTelemetry 的可观测性三支柱如何落地？ | **完整演进：日志→APM→OpenTelemetry→eBPF**；Trace/Metrics/Log统一标准；OTel Collector | Mermaid: 可观测性演进图 + OTel架构 |
| 11.10 | [架] | 混沌工程如何验证系统韧性？ | Chaos Monkey/ChaosBlade/Litmus；故障注入实验设计；**从测试到混沌工程的演进**；稳态假设 | Mermaid: 混沌工程实验流程图 |

### 第12篇：AI 工程与实践（10题）

| 编号 | 难度 | 问题 | 深度要点 | 配图 |
|------|------|------|----------|------|
| 12.1 | [架] | Spring AI 的核心架构与整合模式？ | **Spring生态从Web到AI应用的演进**；ChatClient/ChatModel/EmbeddingModel/VectorStore；Advisor链 | Mermaid: Spring AI 架构分层图 |
| 12.2 | [架] | RAG 检索增强生成的完整流程与各环节优化？ | 文档→分块→嵌入→存储→检索→重排→Prompt→生成；**从关键词到语义到RAG到Agentic RAG的演进** | Mermaid: RAG 演进图 + 全流程图 |
| 12.3 | [专] | 向量 Embedding 与相似度检索的数学原理？ | 文本向量化；余弦/点积/欧氏距离；HNSW/IVF索引；**维度与召回权衡** | ECharts: 相似度算法对比 |
| 12.4 | [高] | 文档分块(Chunking)策略如何影响 RAG 效果？ | 固定/语义/递归分块；overlap窗口；**分块策略演进**；元数据附加 | 表格: 分块策略对比 |
| 12.5 | [专] | Prompt 工程的核心技巧与模板设计？ | **从Prompt到Few-shot到CoT到ReAct到Agent的演进**；结构化输出(JSON mode)；防注入 | 代码块: Prompt 模板示例 |
| 12.6 | [专] | Spring AI 的 Function Calling 如何让 LLM 调用工具？ | @Bean注册Function；LLM决策调用；参数序列化；**多轮调用与Agent框架趋势**；MCP协议 | Mermaid: Function Calling 时序图 |
| 12.7 | [架] | Agent 框架与 MCP 协议如何构建自主智能体？ | **从单次调用到Function Calling到Agent到Multi-Agent的演进**；ReAct/Plan-and-Execute；MCP(Model Context Protocol)；工具编排 | Mermaid: Agent 架构与MCP协议图 |
| 12.8 | [架] | 如何评估和监控 LLM 应用的质量？ | 检索召回率/精确率；生成质量(忠实度/相关性)；RAGAS框架；**LLM评估方法演进**；自动化评测 | ECharts: RAG 评估指标雷达图 |
| 12.9 | [架] | LLM 应用的成本优化与工程实践？ | **模型选型从GPT-4到Claude到开源到多模型路由的演进**；缓存语义查询；Token压缩；流式输出；批处理 | 表格: 成本优化策略 |
| 12.10 | [专] | 多模态 LLM 与 AI 应用的未来趋势？ | 文本/图像/音频/视频多模态；**从单模态到多模态到具身智能的演进**；AI Agent平台化；AGI路径探讨 | Mermaid: AI 应用演进路线图 |

## 九、实施步骤

### 步骤 1：脚手架初始化

执行 html-report 技能的 `new-report.sh` 创建基础目录结构。

### 步骤 2：复制共享资源

将技能目录中的字体（WorkSans × 3 + JetBrainsMono × 1）和 JS 库（echarts.min.js + mermaid.min.js）复制到 `_shared/` 目录。

### 步骤 3：编写共享设计系统 CSS

创建 `assets/design-system.css`，包含：
- `@font-face` 声明
- `:root` CSS 变量（全部设计令牌）
- Reset 样式 + 基础排版
- 全部组件类（.qa-card / .code-block / .callout-* / .compare-table / .difficulty / .chapter-nav 等）
- Mermaid 主题配置
- 响应式断点 + 打印样式

### 步骤 4：编写导航首页 index.html

包含：标题 + 12 张章节卡片（编号/名称/问题数/难度分布/简短描述/点击跳转）+ 技术栈全景标签云 + 2026 面试趋势摘要 + 知识体系全景 Mermaid 图。

### 步骤 5-16：逐篇编写 12 个 HTML 文件

按篇号顺序依次创建：
- 第1篇 `chapter-01-jvm-memory-classloading.html`（8题）
- 第2篇 `chapter-02-gc-performance.html`（10题）
- 第3篇 `chapter-03-concurrency-locks.html`（10题）
- 第4篇 `chapter-04-threadpool-virtual-threads.html`（8题）
- 第5篇 `chapter-05-spring-core.html`（10题）
- 第6篇 `chapter-06-spring-boot-modern.html`（10题）
- 第7篇 `chapter-07-mysql-deep.html`（10题）
- 第8篇 `chapter-08-redis-cache.html`（10题）
- 第9篇 `chapter-09-distributed-systems.html`（10题）
- 第10篇 `chapter-10-microservice-cloud.html`（10题）
- 第11篇 `chapter-11-middleware-engineering.html`（10题）
- 第12篇 `chapter-12-ai-engineering.html`（10题）

每篇 HTML 统一结构：
- `<link>` 引入 design-system.css
- 侧边栏 TOC（桌面端 sticky，列出本篇所有 Q&A 编号与标题）
- 章节头部（编号 + 标题 + 副标题 + 元信息：题目数/难度分布/预计复习时长）
- Q&A 主体（每题含 .qa-card → .qa-header + .qa-answer，六层结构：本质→演进脉络→第一性原理→工程实践→深度追问→常见陷阱）
- 章节间导航（上一篇/目录/下一篇）
- 引用来源（footer + sources）
- 共享 JS 引用（mermaid + echarts + charts-0N.js）

### 步骤 17：编写各篇 ECharts 逻辑

为需要数据可视化的篇章创建 `assets/charts-0N.js`（共约 12 个文件），IIFE 封装，从 CSS 变量读取颜色。涵盖：GC算法对比雷达图、锁状态对比、JIT/AOT/Native性能对比、MVCC锁矩阵、持久化对比、限流算法对比、分布式事务方案矩阵、RAG评估指标雷达图等。

### 步骤 18：编写导航交互 nav.js

实现：TOC 高亮当前题号、移动端侧边栏折叠/展开、返回顶部按钮、进度条。

### 步骤 19：验证与自测

- 浏览器打开 index.html，验证 12 篇链接可达
- 逐篇检查：代码块渲染、Mermaid 图渲染、ECharts 图渲染、响应式布局
- 检查打印样式
- 检查难度标签颜色一致性（蓝/紫/渐变）
- 检查章节间导航正确性

## 十、假设与决策

| 决策项 | 选择 | 理由 |
|--------|------|------|
| 输出格式 | HTML | 排版精美、支持代码高亮和图表、浏览器直接打开 |
| 文件结构 | 每篇独立 HTML | 便于分模块复习，单文件不过大 |
| 输出位置 | 项目根目录下 `java-architect-interview/` 子目录 | 用户指定项目根目录，子目录保持整洁 |
| 设计风格 | Solid 模式（非渐变） | 技术文档需保证代码与图示可读性 |
| 章节数量 | 12 篇 + 1 导航页 | 覆盖 2026 Java 高级开发/架构师全知识域，每篇 8-10 题，共约 116 题 |
| 框架版本 | 不绑定特定版本 | 覆盖 Spring Boot 2.x/3.x、Java 8/11/17/21+，注重原理 |
| 知识边界 | 简历为锚点 + 2026 面试需求拓展 | 不受简历技术栈限制，覆盖行业最新趋势 |
| **难度层级** | **高级开发 + 架构师双层级** | 每篇高级开发题 40-50%、架构级题 40-50%、专家级题 10-20% |
| **演进脉络** | **六层 Q&A 结构含演进维度** | 每道题包含技术演进路线与趋势分析，理解"为什么"而非仅"是什么" |
| 图表工具 | Mermaid（结构图+演进时间线）+ ECharts（数据对比） | html-report 技能规范要求，演进图用 Mermaid 时间线 |
| 字体 | WorkSans + JetBrainsMono | 几何无衬线现代技术感 + 等宽代码字体 |
| 代码高亮 | 手动 span 着色 | 避免引入第三方高亮库，保持轻量自包含 |

## 十一、验证步骤

1. 打开 `index.html`，确认 12 个章节卡片链接均可正常跳转
2. 逐篇打开，确认 Mermaid 图正确渲染（无语法错误）
3. 逐篇打开，确认 ECharts 图正确渲染（数据对比图/雷达图/矩阵）
4. 检查代码块格式（深色底、等宽字体、关键字着色）
5. 检查移动端响应式（侧边栏折叠、表格滚动）
6. 检查章节间导航（上一篇/下一篇/返回目录）
7. 确认每个 HTML 可独立打开（无需本地服务器）
8. 确认难度标签颜色一致：蓝色（高级开发）/ 紫色（架构级）/ 渐变（专家级）
9. 抽查每篇六层结构完整性（本质→演进→原理→实践→追问→陷阱）

## 十二、产出清单

| 文件 | 说明 |
|------|------|
| `index.html` | 导航首页，12 篇卡片入口 + 知识体系全景图 |
| `chapter-01-jvm-memory-classloading.html` | JVM 内存与类加载（8题） |
| `chapter-02-gc-performance.html` | GC 算法与性能调优（10题） |
| `chapter-03-concurrency-locks.html` | 并发编程与锁机制（10题） |
| `chapter-04-threadpool-virtual-threads.html` | 线程池与虚拟线程（8题） |
| `chapter-05-spring-core.html` | Spring 核心原理（10题） |
| `chapter-06-spring-boot-modern.html` | Spring Boot 与现代框架（10题） |
| `chapter-07-mysql-deep.html` | MySQL 深度原理（10题） |
| `chapter-08-redis-cache.html` | Redis 与缓存架构（10题） |
| `chapter-09-distributed-systems.html` | 分布式系统（10题） |
| `chapter-10-microservice-cloud.html` | 微服务与云原生（10题） |
| `chapter-11-middleware-engineering.html` | 中间件与工程化（10题） |
| `chapter-12-ai-engineering.html` | AI 工程与实践（10题） |
| `assets/design-system.css` | 共享设计系统 |
| `assets/charts-01.js ~ charts-12.js` | 各篇 ECharts 逻辑 |
| `assets/nav.js` | 导航交互逻辑 |
| `_shared/js/echarts.min.js` | ECharts 库 |
| `_shared/js/mermaid.min.js` | Mermaid 库 |
| `_shared/fonts/*.ttf` | 4 个字体文件 |
