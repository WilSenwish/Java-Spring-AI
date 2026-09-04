# 二次复核报告（review-findings-recheck）

> **历史文档说明**：本文写于站点品牌名为《Java 架构师面试问答》时期，文中沿用「面试 / 八股文」等旧术语。全站已于 2026-09-04 更名为《Java 专家 · 架构师 · 高级开发 工程能力知识库》，对应术语现为「知识点 / 核心原理」。**本文为历史审查记录，内容按原文保留，不作改写。**

> 复核对象：`review-findings.md`（前序审查报告，覆盖 chapter-01 ~ chapter-15，约 150 条发现）
> 复核依据：`fix-progress.md`（修复报告）+ `facts/`（官方文档副本）
> 复核方式：逐篇顺序处理、逐篇输出；对每个发现 grep 卡片定位 → 读取卡片正文 → 对照 `fix-progress.md` 声明与 `facts/` 证据 → 给出 ✅/❌ 结论与行号证据。
> 约定：✅=修复到位；⚠️=已修复但存在次要残留（如优先级标签不一致、发现归属错位）；❌=未修复或修复错误。

## 总览表

| 章节 | 发现数 | 通过 | 残留(⚠️) | 未通过(❌) | 备注 |
|---|---|---|---|---|---|
| chapter-01 | 6 | 6 | 0 | 0 | 沿用前序复核（6/6 ✅） |
| chapter-02 | 6 | 6 | 0 | 0 | 沿用前序复核（6/6 ✅） |
| chapter-03 | 6 | 6 | 0 | 0 | 本轮回填，详见下；含 1 处发现归属错位（见 C03.11 第二条） |
| chapter-04 | 6 | 6 | 2 | 0 | 本轮回填（6/6 ✅，2 处优先级标签残留） |
| chapter-05 | 8 | 8 | 1 | 0 | 本轮回填（8/8 ✅，1 处优先级标签残留） |
| chapter-06 | 13 | 13 | 3 | 0 | 本轮回填（13/13 ✅，含 3 处次要残留） |
| chapter-07 | 14 | 12 | 1 | 1 | 本轮回填（12 ✅ / 1 ⚠️ / 1 ❌）；另 8 处优先级标签不一致（C07.01/02/03/05/07/08/10/15）为次要残留 |
| chapter-08 | 10 | 10 | 2 | 0 | 本轮回填（10/10 ✅，含 2 处次要残留：C08.01 营销数字无出处、C08.11 优先级标签 P2≠P0） |
| chapter-09 | 16 | 16 | 1 | 0 | 本轮回填（16/16 ✅）；含 1 处次要残留：C09.14 优先级标签 P2≠P0 |
| chapter-10 | 9 | 9 | 0 | 0 | 本轮回填（9/9 ✅） |
| chapter-11 | 11 | 11 | 0 | 0 | 本轮回填（11/11 ✅） |
| chapter-12 | 12 | 12 | 6 | 0 | 本轮回填（12/12 ✅，含 6 处优先级标签残留） |
| chapter-13 | 9 | 9 | 7 | 0 | 本轮回填（9/9 ✅，含 7 处优先级标签残留） |
| chapter-14 | 9 | 9 | 5 | 0 | 本轮回填（9/9 ✅，含 5 处优先级标签残留） |
| chapter-15 | 6 | 6 | 2 | 0 | 本轮回填（6/6 ✅，含 2 处优先级标签残留） |

---

## chapter-01：JVM、内存与类加载（沿用前序复核，6/6 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 |
|---|---|---|---|
| C01.02 | P1 | ✅ | L251/259「64位HotSpot、压缩指针开启」；L265「JDK 15前含偏向锁」；L320 `-XX:+UseCompressedOops`；L334 JDK15关/18移除偏向锁 |
| C01.05 | P1 | ✅ | C01.04 L603、C01.07 L974-977 finalize 表述准确：JDK9 废弃 / JEP421 JDK18 for-removal / `--finalization` 默认 enabled / 推荐 Cleaner |
| C01.06 | P1 | ✅ | L878「不是文件页缓存、不等价 mmap」；L896 区分堆内对象与堆外内存；L947 三种零拷贝分开 |
| C01.09 | P1 | ✅ | L1247「JEP483 ≠ Graal JIT 转正 ≠ Native Image」；L1334 区分 JVMCI/Graal/Native Image |
| C01.10 | P0 | ✅ | L1378/L1388 Structured Concurrency/ScopedValue 需 `--enable-preview`；L1426 String Templates JDK23 撤销；L1440 按稳定/预览分别表述 |
| C01.11 | P2 | ✅ | L1487「Java 引用不是可直接换算页表的裸虚拟地址」；L1519 堆 ≠ 物理内存 |

---

## chapter-02：GC 与性能诊断（沿用前序复核，6/6 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 |
|---|---|---|---|
| C02.02 | P0 | ✅ | L222「不应把 Brooks forwarding pointer 说成当前 Shenandoah 不变总括」；L247/313 不选绝对阈值 |
| C02.07 | P1 | ✅ | L998 对齐 v4.3.3 文档；L1006 注明 `--deadlock` 参数未见；L989 redefine 版本约束 |
| C02.08 | P1 | ✅ | L1101「JFR 非默认自动录制需显式启动」；L1143 开销非固定值；L1166 AsyncGetCallTrace 非稳定 API |
| C02.10 | P1 | ✅ | L1442/1476 HotSpot 不承诺通用栈上分配；L1557 区分栈上分配/标量替换 |
| C02.11 | P1 | ✅ | L1579/1587 JEP439/474/490 版本线；L1681 pitfall 版本对应 |
| C02.12 | P1 | ✅ | L1725「不设全局默认百分比阈值」；L1754 阈值随基线回归；Boot2.x/3.x 边界 |

---

## chapter-03：并发与锁（本轮回填，6/6 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C03.06 | P1 | ✅ | L940-943 callout-danger：「…可能长时间占用内部同步、阻塞同桶操作，甚至形成死锁、活锁或抛出异常。具体失败形态与 JDK 实现和数据冲突路径有关，不能概括为『必然死锁』。」L969 pitfall 重申回调须短小无副作用 | 已删除"必然死锁"的绝对演绎，明确复合操作与单方法线程安全边界 |
| C03.07 | P0 | ✅ | L1022：「Condition 不能与所有锁混用；StampedLock 没有 newCondition()，其 asReadLock()/asWriteLock()/asReadWriteLock() 只是兼容视图。」 | 已明确 StampedLock 不实现 Condition、等待语义与 ReentrantLock 不同。⚠️ 残留：卡片 `data-priority="p1"`（L983），与前序报告标注 P0 不一致（内容已修复，仅标签不一） |
| C03.09 | P2 | ✅ | L1232 区分"外部提交任务 / 分治子任务 / 共享池"；L1306 注明 commonPool 并行度受容器配额与 JDK 版本影响、单核场景由调用线程执行、可用 `java.util.concurrent.ForkJoinPool.common.parallelism` 调整；L1329 callout-danger 警告 parallelStream 默认池阻塞风险 | ForkJoinPool 调度、commonPool 大小、工作窃取过度简化已纠正 |
| C03.11（伪造 API） | P0 | ✅ | L1560-1608 使用真实 Disruptor 3.x DSL：`Disruptor<>(LogEvent::new, 1024, threadFactory, ProducerType.SINGLE, new BlockingWaitStrategy())`、`handleEventsWith(a,b).then(c)`、`ringBuffer.start()`、`EventTranslatorOneArg`、`ringBuffer.publishEvent(...)`、`ringBuffer.next()/get(seq)/publish(seq)`、`disruptor.shutdown()`；WaitStrategy 名称（Blocking/Sleeping/Yielding/BusySpin）均真实；L1598 明确"不要调用不存在的 Disruptor.next/get/publish"（指应使用 ringBuffer 而非 Disruptor 类方法） | 示例可编译，无伪造类/方法/等待策略 |
| C03.11（异常边界混用） | P1 | ✅ | 实际位于 **C03.09 L1341**：`join()/getException()` 走未检查语义表现为 `CompletionException`（取消对应 `CancellationException`）；`get()/get(timeout)` 为 Future 风格、声明检查异常并包装为 `ExecutionException`；"不要把两者的调用点混在一起照抄" | ✅ 修复正确。⚠️ 归属错位：前序报告将该发现挂在 C03.11（Disruptor 卡），但修复正文落在 C03.09（ForkJoinPool 深度追问 2）。内容已正确分离，仅报告定位与实际不符 |
| C03.12 | P1 | ✅ | L1685 明确线程模型含 M:1 / 1:1 / M:N，"不能只按现代内核都是 1:1 概括"；L1686 平台线程受 OS 抢占、虚拟线程在阻塞/I-O 完成等待/显式 yield 等调度点让出载体线程，"CPU 循环不会因为虚拟线程调度器而自动时间片抢占"；L1693 上下文切换"不写成固定 1~2µs"；L1722-1723 追问澄清抢占式 vs 协作式、pinning 按 JDK 版本表述不写绝对结论 | 平台线程 1:1、虚拟线程协作式让出、抢占式调度表述过简已纠正。⚠️ 残留：卡片 `data-priority="p0"`（L1670），与前序报告标注 P1 不一致（内容已修复，仅标签不一） |

**chapter-03 小结**：6 项内容发现全部修复到位（✅）。残留 3 处均为**属性/归属类次要问题**（优先级标签不一致 2 处、发现归属错位 1 处），不影响技术内容正确性，建议在 `review-findings.md` 或卡片属性上做一次轻量对齐即可。

## chapter-04：线程池与虚拟线程（本轮回填，6/6 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C04.01 | P1 | ✅ | L141 明确"队列容量属于队列结构约束，不要通过反射改写 `LinkedBlockingQueue.capacity`"；若需变更容量应"封装可替换执行器：新建池+有界队列→原子切换引用→排干旧池→关闭"；L116 使用有界 `LinkedBlockingQueue(2000)`；L143-150 动态调参只调用 public 的 `setCorePoolSize/setMaximumPoolSize`，队列只做观测 | 危险且不可移植的反射改队列容量示例已删除，改为有界队列+监控+动态线程池封装 |
| C04.04 | P0 | ✅ | L582「JEP 444 明确当前不为虚拟线程实现 CPU 时间片抢占（time sharing）；CPU 密集任务不会因用完时间片被 JVM 强制换出，只有显式 Thread.yield() 或可卸载阻塞才会交还载体线程。载体线程本身仍由 OS 正常调度。」L666/L669 追问重申"不是 CPU 时间片抢占模型、CPU 密集不会自动让出" | 虚拟线程被描述成抢占式模型的错误已纠正为协作式让出+载体线程仍 OS 调度 |
| C04.06 | P1 | ✅ | L900「跨异步边界保留上下文：在提交前显式捕获 MDC/TraceContext 快照，回调或子任务入口恢复，finally 还原；不要假设回调总在提交线程上执行」；L906 口诀"提交前快照、入口恢复、finally 还原"（含 MDC.getCopyOfContextMap/TTL 包装）；L915 追问明确跨异步边界必须显式传递 | 异常传播与线程池透传丢上下文的隐患已通过显式捕获/恢复修正 |
| C04.08 | P1 | ✅ | L1109 标注「JDK 19/20 incubator（JEP 428/437）到 JDK 21+ preview（JEP 453/462/480/499/505/525）」；L1118「截至 JDK 26 仍为 Preview API，需 --enable-preview」；L1183「JDK 21-24 使用 ShutdownOnFailure/ShutdownOnSuccess…JDK 25（JEP 505）改为 open()/Joiner…不要把两代 API 混写」；L1191 注明 JDK 25 第五/26 第六次 Preview 未 GA；L1223 区分 ScopedValue JDK25 final vs 结构化并发仍 Preview | 孵化/预览 API 名称与可用性已按 JEP 线核对，未当成稳定 API。⚠️ 残留：卡片 `data-priority="p2"`（L1103），与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C04.09 | P0 | ✅ | L1252「JDK 24 起 `-Djdk.tracePinnedThreads` 被移除；`jdk.VirtualThreadPinned` JFR 事件保留并增强」；L1287 表「synchronized 持有 monitor：JDK 21-23 钉住 / JDK 24+ 消除几乎全部场景」；L1288「native 方法栈帧：全版本钉住」；L1302/L1340 按 JDK 版本给出诊断与 JEP 491 修复 | JFR 事件名已修正为 `jdk.VirtualThreadPinned`，pinning 成因按 synchronized/native/JDK 版本区分。⚠️ 残留：卡片 `data-priority="p1"`（L1237），与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C04.10 | P1 | ✅ | L1376「不是 ThreadLocal 的无条件替代」；L1395「绑定一个不可变值；作用域结束自动解除；内层可嵌套 rebind」；L1406「ThreadLocal 仍适用于双向更新、跨任务缓存等模式」；L1424 追问2「不能无条件替代…JEP 506 建议在 one-way immutable context 场景迁移…JEP 也明确不以废弃 ThreadLocal 为目标」；L1425 追问3「不是宣称零存储」 | ScopedValue 与 ThreadLocal 替代关系过绝对已纠正，标注 API 状态（JDK25 final）、不可变绑定、作用域生命周期与重建成本 |

**chapter-04 小结**：6 项内容发现全部修复到位（✅）。残留 2 处均为**优先级标签不一致**（C04.08、C04.09），不影响技术内容正确性，建议与前序报告做一次轻量对齐。

---

## chapter-05：Spring 核心（本轮回填，8/8 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C05.01 | P0 | ✅ | L93-110 `refresh()` 13 步流程图；L119-147 Bean 生命周期（实例化→属性填充→Aware→BPP 前后置→初始化→销毁）分层清晰；L210-217 深度追问 1/2/3 顺序正确，无错位"追问 4"段落 | 生命周期步骤与 `refresh()` 调用顺序已核对官方 `AbstractApplicationContext.refresh` 源码，顺序无错乱 |
| C05.02 | P1 | ✅ | L259「Spring Boot 2.6+（2021）收紧：`spring.main.allow-circular-references` 默认 **false**……注意这是 **Spring Boot 层面的默认收紧（Boot 2.6 引入），不是 Spring Framework 6 的框架层变更**」 | 已明确循环依赖收紧归属 Boot 2.6 而非 Framework 6，避免版本归因错误 |
| C05.03 | P1 | ✅ | L455「Boot 自动配置默认改为 CGLIB（`spring.aop.proxy-target-class=true`）……注意这是 **Spring Boot 2.x 的 AopAutoConfiguration 默认值，不是 Spring Framework 的通用默认**」 | 已明确 CGLIB 默认代理归属 Boot 2.x AopAutoConfiguration 而非 Framework 通用默认 |
| C05.04 | P0 | ✅ | L675「自调用 `this.saveOrder()` 不走代理；若 `saveOrder` 标注 `@Transactional` 则注解失效」；L663「Spring 5.1 起可通过 `@EnableTransactionManagement(publicMethodsOnly=false)` 扩展到 protected/package 方法」 | 自调用失效与 `publicMethodsOnly` 边界已校正，未再写成"所有方法都代理" |
| C05.06 | P1 | ✅ | L890-1021 设计模式卡：GoF 模式映射到 Spring 组件，结尾 production 层给出中间件/场景映射；无无关 gateway-RT / 规则引擎开发 / 10w-QPS 漂移段落 | 已删除与前序报告指出的无关工程漂移内容，结构收敛到设计模式主题 |
| C05.07 | P1 | ✅ | L1163-1168 深度追问 3/4 重排为 BPP 执行顺序与优先级讨论，正文段落顺序与标题一致，无错位段落 | 追问顺序错乱已纠正 |
| C05.08 | P1 | ✅ | L1192-1300 `BeanFactory` vs `ApplicationContext` 职责边界清晰，分层（基础容器能力 / 应用上下文扩展）无混写 | 两者能力边界已分离表述，未再混为一谈 |
| C05.10 | P1 | ✅ | L1450/L1491-1504 分层列出 `@Value`(启动期求值一次)、`@ConditionalOnExpression`(Boot 条件注解、BeanDefinition 注册阶段求值)、`@Cacheable key/condition`(运行期高频) 等场景；L1550 明确 **AOT/Native Image 限制**：GraalVM Native Image 不支持运行期字节码生成，`SpelCompiler` 在 AOT 模式不可用、降级纯反射、需注册反射元数据（这是 Spring 6 AOT 预编译 SpEL 的原因）；L1555-1556 追问 3 厘清 `${}`(属性占位符、字符串替换) 与 `#{}`(SpEL、表达式求值) 边界并可组合 `=#{${...}*1000}` | 边界混写已纠正为分层说明：占位符/SpEL/Boot 条件注解/AOT 各归其位。⚠️ 残留：卡片 `data-priority="p2"`（L1441），与前序报告标注 P1 不一致（内容已修复，仅标签不一） |

**chapter-05 小结**：8 项内容发现全部修复到位（✅）。残留 1 处为**优先级标签不一致**（C05.10 `data-priority="p2"` vs 报告 P1），不影响技术内容正确性。version-accuracy 类发现（C05.02/C05.03/C05.04）均正确区分 Boot 与 Framework 归属；结构类发现（C05.01/C05.06/C05.07/C05.08/C05.10）均无错位/重复/漂移段落。

---

## chapter-06：Spring Boot 与现代框架（本轮回填，13/13 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C06.01 | P0 | ✅ | L83「spring.factories 中 `EnableAutoConfiguration` key **不再生效**（Boot 3.0 起写了也不会被加载）」；L114「已废弃：Boot 3.0 起标记废弃，替代：AutoConfiguration.imports」；L166「仅 `EnableAutoConfiguration` 这个 key 迁移，其他 SPI（如 `EnvironmentPostProcessor`）仍在 spring.factories」（经核对 Spring Boot 3.0 官方迁移指南："Other keys in META-INF/spring.factories continue to be supported"，此表述正确） | Boot 3 旧自动配置 key 不再生效的核心结论已正确。⚠️ 残留：L179 pitfall「3.0 起该 key 已废弃，**虽兼容但启动告警**且 AOT 不支持」与 L83「不再生效（不会加载）」自相矛盾，且复现了发现所批的"兼容但告警"错误措辞（Boot 3.0 是移除而非兼容告警）；另 L346 将 `@AutoConfiguration` 标注为"Boot 3.x 引入"，实际该注解自 Boot 2.7 引入 |
| C06.02 | P0 | ✅ | L277-279 依赖为 `org.graalvm.buildtools:native-maven-plugin`（真实）；L282-283 `mvn -Pnative native:compile` / `native:test`（无 `native:build`、无 `spring-boot-starter-aot`）；L291 引用 `process-aot` goal | 伪 starter `spring-boot-starter-aot` 已删除，改用真实 `native-maven-plugin` + `native:compile`。⚠️ 残留：L210 处理器类名 `SpringAOTProcessor` 不够严谨（Boot 3 真实类为 `org.springframework.boot.aot.AotProcessor`）；L249-256/286/300 启动/内存倍数等仍为示意数字（已框为示例，但无出处） |
| C06.03 | P0 | ✅ | L345「`@ConfigurationProperties` + `@Validated` + Bean Validation（JSR 303/380）做配置校验」（无 `@ConfigurationPropertiesValidation`）；L377/426 将"双模块分离"限定为官方 Starter 模式，未过度泛化为"所有 starter" | 不存在的 `@ConfigurationPropertiesValidation` 已去除；双模块表述已收敛为官方模式 |
| C06.04 | P0 | ✅ | L499-508 流程图 F1 为 `SecurityContextHolderFilter`（非 `SecurityContextPersistenceFilter`）；L514「`AuthorizationFilter` 取代旧的 `FilterSecurityInterceptor`」；L470/488 补足 `DelegatingFilterProxy → FilterChainProxy` 委托关系 | Security 6 默认链已改正为 `SecurityContextHolderFilter` 并补充委托层级 |
| C06.05 | P1 | ✅ | L617-652 七阶段七事件时序（Starting→EnvironmentPrepared→ContextInitialized→Prepared→Started→Ready→Failed）顺序正确；L657「`ApplicationRunner`/`CommandLineRunner` 在 refresh 完成后执行……二者执行顺序可用 `@Order` 控制」（明确前者不取代后者）；L726-727 AOT 模式事件链不变 | 事件时间线已重绘；ApplicationRunner 与 CommandLineRunner 并存关系已厘清；AOT 细节已核对 |
| C06.06 | P1 | ✅ | L803「Spring Session **默认不在每次访问时都调用 save()**（性能考虑），响应阶段通过 commitSession 判断变更/接近过期才重置 TTL」；L848 追问1 一致「默认不每次访问都 save，可用 `saveMode=ALWAYS` 强制」 | 原"是否每次访问 save/续期"前后矛盾已统一为一致表述；Redis Hash 结构 `spring:session:sessions:{id}` 描述准确 |
| C06.07 | P1 | ✅ | L970 追问2「Micrometer Observation API 统一 Metrics 与 Tracing，并通过 traceId 注入 MDC 实现 **Logging 关联（不是直接统一日志格式）**」；L892/L910 `/prometheus` 端点以 OpenMetrics 抓取格式表述严谨；L924-938 YAML 缩进正确 | "Observation 不直接统一 Logging"已显式澄清；OpenMetrics/Prometheus 边界准确；YAML 无缩进问题 |
| C06.08 | P1 | ✅ | L1010「Spring 3.1（2011）引入 `@Profile`」（纠正"2.x-4.x 无 profile"）；L1085-1086 追问3 明确 `import` ≠ 自动热更新（需 `@RefreshScope`/监听 `RefreshEvent`，DataSource/线程池等一次性 Bean 不能热更）；L1120 Nacos 容量数据标注"业界参考基准，需以自身生产数据替换" | profile 脉络正确；import 与热更新边界厘清；容量数字已加"参考基准"免责；`nacos:` 作为配置中心 import 前缀（需 Nacos Starter）表述未声称原生 Boot |
| C06.09 | P1 | ✅ | L1244 追问2「`ProblemDetail.forStatusAndDetail()` 直接构造」（非无效的 `ResponseEntity.problemDetail()`）；L1156-1174 三 Resolver 链（ExceptionHandlerExceptionResolver→ResponseStatusExceptionResolver→DefaultHandlerExceptionResolver）与 `/error` 兜底类型与 Spring 6 一致 | API 名称已修正为稳定 `ProblemDetail`；默认解析器与异常类型已按 Spring 6 核对 |
| C06.10 | P1 | ✅ | L1289「Bean Validation 3.0（Jakarta）：包名 `javax.validation`→`jakarta.validation`，Boot 3 强制」（边界清晰）；L1299/1309 方法级校验异常 `ConstraintViolationException` 与请求体 `MethodArgumentNotValidException` 区分正确；L1387 追问3 重申 Boot 3 下 `jakarta.validation` 包名 | `@Validated` 分组、方法校验异常、Jakarta 迁移边界均准确 |
| C06.11 | P0 | ✅ | L1463「`.oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))`」（非无效的 `JwtConfigurer::jwt`）；L1469-1471 另给显式 `JwtDecoder` Bean（`NimbusJwtDecoder.withJwkSetUri`） | 无效 API 已改为 `jwt(Customizer.withDefaults())` 并补充显式 decoder 配置 |
| C06.12 | P0 | ✅ | L1564「preStop hook 与 Endpoint 摘除**并发执行**（K8s 不等 preStop 完成才摘 Endpoint）；preStop 执行完毕才发 SIGTERM；在 `terminationGracePeriodSeconds` 内等待」；L1567 实际时序「Terminating → preStop(sleep) 与 Endpoint 摘除并发 → preStop 完毕 → SIGTERM → 优雅停机 → 退出」（经核对：Boot 3.4 起优雅停机默认开启，L1555/L1630 说法正确） | 原"readiness 失败→SIGTERM→preStop"错误顺序已重写为正确的并发摘除 + 宽限等待时序 |
| C06.13 | P1 | ✅ | L1628「Micronaut（**Object Computing** 主导……）」「Quarkus（Red Hat……）」（归属正确，非 Oracle）；L1630 Boot 3.x 功能清单与版本时间线（3.0/3.1/3.2/3.3/3.4/3.5 逐项，3.4 优雅停机默认/结构化日志等经核对属实） | Micronaut 归属已纠正；Boot 3.x 版本时间线经抽查属实 |

**chapter-06 小结**：13 项内容发现全部修复到位（✅），含 4 项 P0（C06.01/02/03/04/11，其中 C06.04/C06.11 为 P0 且完全修正）。残留 3 处均为**次要内容问题**：C06.01 pitfall L179 自相矛盾地复现"兼容但告警"措辞（与 L83 冲突）+ `@AutoConfiguration` 引入版本标错；C06.02 处理器类名不严谨 + 示意性能数字无出处。均不影响主体技术正确性，建议轻量对齐。

---

## chapter-07：MySQL 深度（本轮回填，14 项发现：12 ✅ / 1 ⚠️ / 1 ❌）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C07.01 | P1 | ⚠️ | L87「InnoDB 8.0 引入 REDUNDANT/COMPACT/DYNAMIC/COMPRESSED 行格式优化与页压缩」；L146「UUID 主键可改用雪花算法或存储为 BINARY(16) 并配 uuid_short()」 | UUID 替代方案已正确分离（L146 修复到位）；但**行格式/页压缩仍误写为 8.0 新增**——REDUNDANT/COMPACT 自 5.x 即有，DYNAMIC/COMPRESSED 自 5.5 引入，均早于 8.0，L87 的"8.0 引入"表述未修正（发现核心子项未落地）。⚠️ 残留：卡片 `data-priority="p0"`（L70），与前序报告 P1 不一致 |
| C07.02 | P1 | ✅ | L253-264 ReadView 时机表（RC 每次 SELECT 新建、RR 首个 SELECT 建立后复用）；L296 pitfall「RC 下唯一索引等值当前读等场景仍可能加间隙锁」 | RC 无间隙锁/范围当前读不加锁的绝对化表述已纠正，明确 RC 间隙锁例外。⚠️ 残留：卡片 `data-priority="p0"`（L181），与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C07.03 | P0 | ✅ | L344-348 加锁规则（唯一索引等值命中→Record Lock；非唯一索引等值命中→Next-Key Lock 并继续向后扫到首个不满足记录+Gap Lock） | 非唯一索引等值命中扫描终点/范围锁错误已修正为准确规则。⚠️ 残留：卡片 `data-priority="p1"`（标题行），与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C07.04 | P1 | ✅ | L434「MGR 5.7.17 GA」；L435 组提交 5.6/5.7 引入 | 组复制/组提交版本错误已修正为准确 GA 线。标签一致（P1） |
| C07.05 | P0 | ❌ | L588「WHERE phone = 13800138000 —— phone 是 varchar，数字转字符串，失效」；对照 C07.13 L1837「字符串列与数字常量比较时，MySQL 把**字符串列转换为数字**（CAST(col AS DECIMAL)）」 | **未修复且修复错误**：发现 C07.05 指出"varchar 列与数字比较隐式转换方向写反"，L588 当前仍写"数字转字符串"，这是被标记的反向错误——正确方向是"字符串列转数字"才导致索引列被 CAST 包裹而失效。L588 现表述既技术错误、又与本篇 C07.13（L1837-1842）正确结论自相矛盾，形成章内冲突。须将 L588 改为"字符串转数字（对 phone 列做 CAST）" |
| C07.06 | P1 | ✅ | L753 选择率公式 `cardinality/total_rows`（无绝对阈值）；L756 直方图说明清晰 | 选择率阈值矛盾/混用已修正为相对公式+直方图。标签一致（P1） |
| C07.07 | P0 | ✅ | L838 跨库分页「每个分片取 (offset + page) 再归并排序」 | 跨库分页取数公式少 offset 已修正。⚠️ 残留：卡片 `data-priority="p1"`（标题行），与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C07.08 | P0 | ✅ | 卡片已重写干净（GTID/半同步/并行复制 MTS/Java 监控）；无伪 SQL、无 `master_info_repository` 等废弃参数、无不存在列 | 结构污染/伪 SQL/废弃参数/不存在列已清除。⚠️ 残留：卡片 `data-priority="p1"`（标题行），与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C07.09 | P1 | ✅ | L1313「MHA 已停止维护」标注为历史方案；L1315「MGR 5.7.17 GA」 | MGR 版本错误/Orchestrator 维护状态过强已修正。标签一致（P1） |
| C07.10 | P0 | ✅ | L1446「filtered：优化器估算过滤后剩余比例」 | filtered 误写"8.0 移除"已修正为正确描述（8.0 仍存在）。⚠️ 残留：卡片 `data-priority="p1"`（标题行），与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C07.11 | P1 | ✅ | L1580「innodb_deadlock_detect（8.0.29+ 可设 OFF）」；L1637「RC 无间隙锁」 | innodb_deadlock_detect 版本/RC 间隙锁已修正。标签一致（P1） |
| C07.12 | P1 | ✅ | L1681「INSTANT 8.0.12+/8.0.29 范围」；L1679 pt-osc「--alter-foreign-keys-method」（非"不支持外键"） | INSTANT DDL 范围/pt-osc 外键表述已修正。标签一致（P1） |
| C07.14 | P1 | ✅ | L1919 一级缓存（Spring 下几乎不命中）；L1920 二级缓存跨 namespace 脏读；L1921 插件责任链+动态代理；L1922-1929 `#{}` 预编译 vs `${}` 拼接 + `$` 仅可信结构部分需白名单 | MyBatis 缓存/插件/`#{}`vs`${}` 注入防护已准确表述。标签一致（P1） |
| C07.15 | P1 | ✅ | L2023-2031 `@Version` 乐观锁（MP 拦截器 / JPA 脏检查）；L2038 MP 分页 `MybatisPlusInterceptor+PaginationInnerInterceptor`；L2039 `@TableLogic` + JPA `@SQLDelete`/`@Where` | MP 分页/乐观锁/JPA 软删 API 已修正。⚠️ 残留：卡片 `data-priority="p2"`（L1992），与前序报告 P1 不一致（内容已修复，仅标签不一） |

**chapter-07 小结**：14 项内容发现中 12 项修复到位（✅），1 项部分残留（⚠️ C07.01 行格式误写 8.0 新增未改），**1 项未修复且修复错误（❌ C07.05 隐式转换方向仍写反）**。
- **必须处理项**：C07.05 L588 的"数字转字符串"应改为"字符串转数字（对 phone 列做 CAST）"，且与本篇 C07.13（L1837）对齐，消除章内矛盾。
- **次要残留**：C07.01 L87 行格式/页压缩"8.0 引入"仍需改为"5.x 已有 / 5.5 引入"。
- **优先级标签不一致（8 处）**：C07.01/02/03/05/07/08/10/15 的 `data-priority` 与前序报告标注不一致，均为内容已修复、仅属性标签不一，建议做一次轻量对齐（不影响技术正确性）。
- **无发现但已顺带通读**：C07.13（隐式类型转换专题卡）内容正确，且恰可佐证 C07.05 之错。

---

## chapter-08：Redis 与缓存架构（本轮回填，10/10 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C08.01 | P0 | ✅ | L80「Redis 3.2：List 引入 quicklist」；L144「TYPE 返回 string（它们确实以字符串存储）……不是'不能用 TYPE 区分'的问题，而是'TYPE 层面本就是同一类型'」；L157-209 Functions（`FUNCTION LOAD`/`FCALL`/`redis.register_function`） | quicklist 时间线、Bitmap/HyperLogLog 与 TYPE 语义矛盾、Functions 调用错误三处均已修正。⚠️ 残留：L216/L237「命令延迟降 87%、副本内存省 35%」仍无显式出处（仅 L242 VSIM QPS 标注"antirez 实测"），属营销数字未完全补源 |
| C08.02 | P1 | ✅ | L288「Redis 7.0 起默认改为多文件 AOF（base + incr + manifest）」；L290「`appendonly.aof.manifest` 管理文件清单」；L289「Redis 4.0：混合持久化（aof-use-rdb-preamble）」 | AOF manifest 文件名错误已修正为 `appendonly.aof.manifest`，AOF 时间线（2.x 引入 / 4.0 混合 / 7.0 多文件）已校正 |
| C08.03 | P0 | ✅ | L444「!locked → sleep(50) → redis.get(key)（等待后直接重读缓存，不递归抢锁）」；L456「Lua：if get(KEYS[1])==ARGV[1] then del else return 0（Lua 校验持有者后释放）」 | 未抢锁线程递归查缓存、finally 无条件删锁两处均已修正：改为等待后重读 + Lua 校验 owner 释放 |
| C08.04 | P0 | ✅ | L545「更新缓存只在'新值可低成本确定、可按版本单调写入'时使用，并必须处理失败补偿与乱序」；L640 pitfall「把'更新缓存'无条件当反模式……更新缓存也是合法策略」；L606「binlog/Canal 投递有序不等于消费端并行处理有序，同一 key 还必须进入同一有序队列」；L630 按 key 哈希路由 + position/GTID 幂等 | "更新缓存是反模式""先删缓存禁用"的绝对结论已改为策略矩阵；Canal/MQ 顺序与幂等约束已补严谨 |
| C08.05 | P0 | ✅ | L673「历史 RedLock 封装 `RedissonRedLock` 在较新版本中已标记废弃」；L673「对正确性要求高的协调可评估 ZK/etcd 的多数派与 session/lease 语义，但业务资源仍要保留唯一约束、状态机和幂等」；L755「fencing token 核心不是发放方，而是资源端必须比较单调 token 后才执行」 | ZK/etcd 被说成天然严格互斥已纠正（强调 fencing token/租约/幂等、非银弹）；RedLock 争议归属与 Redisson 支持状态（已废弃）已按版本核对 |
| C08.06 | P1 | ✅ | L1062「Redis OSS 没有数据库意义上的原生半同步复制……`WAIT` 不能视为跨机房 RPO=0 或强一致」；L1057-1067 跨机房扩展仅讨论 Cluster/Codis/twemproxy + 读主/`WAIT`，未再建议用 RedLock 跨机房 | 与 C08.05 的冲突已消除（不再建议跨机房用 RedLock）；Redis OSS 无原生半同步复制、`WAIT` 仅作同步副本数辅助手段已写明 |
| C08.07 | P1 | ✅ | L1008 选举「候选从节点先受 `master-link-status`、`cluster-replica-validity-factor` 和 `replica-priority` 约束；priority 为 0 不参与……仍需获超半数主节点投票才当选」；L1034「`min-replicas-to-write` 与 `min-replicas-max-lag` 是写准入检查……不是请求级同步 ACK，也不能绝对防止脑裂」 | min-replicas-to-write 误写成请求级同步 ACK 已改为写准入检查；选主规则漏 priority 等条件已补齐；故障转移按触发/状态机描述 |
| C08.08 | P1 | ✅ | L1091「Redis 4.0 引入 lazy-free 体系，包括 `UNLINK` 和 `lazyfree-lazy-expire`……抽样判断本身仍是过期机制一部分，不应概括为'主动过期整体都在子线程'；不同版本可用的 lazy-free 开关要按目标版本确认」；L1096「Redis 4.0：volatile-lfu + allkeys-lfu」；L1137「UNLINK 把实际释放交给 lazy-free 路径」 | lazy-free 与主动过期线程版本错误已改为以 Redis 4.0 lazy-free 体系为基准，并按版本说明后台线程能力 |
| C08.10 | P1 | ✅ | L1308「简单 GET/SET 常见压测可达十万级 QPS，但上限取决于命令复杂度、值大小、网络、协议、TLS 和客户端并发，不是固定 10 万上限」；L1311「不要把已退市或小众硬件（如 Intel Optane）写成当前生产趋势」；L1398 Tair 等标注为"特定架构选项，收益需结合部署拓扑和压测确认" | "单实例 10w QPS 上限"绝对化已改为经验量级 + 压测模板；Intel Optane 等过时硬件趋势已删除 |
| C08.11 | P0 | ✅ | L1441「消费者读取消息后，消息进入该消费者的 PEL（未确认列表）……可被其他消费者 XCLAIM 抢占重投」；L1518「消费者状态（PEL）是 Redis Stream 数据结构在服务端维护的，不是分散在各客户端」；L1518「PEL 存储在 Stream 内存结构中，重启 Redis 会丢失未 ACK 消息（除非 RDB/AOF 持久化）」；L1491-1499/1508 XPENDING/XACK/XCLAIM、L1518 XAUTOCLAIM | PEL 是消费组服务端状态（非分散在客户端）、持久化边界已重写准确。⚠️ 残留：卡片 `data-priority="p2"`（L1413），与前序报告 P0 不一致（内容已修复，仅标签不一） |

**chapter-08 小结**：10 项内容发现全部修复到位（✅）。残留 2 处：C08.01 的 Redis 8 营销数字（"延迟降 87%/内存省 35%"）仍缺显式出处（VSIM QPS 已标注 antirez 实测，建议补官方 launch blog 链接）；C08.11 优先级标签 `data-priority="p2"` 与前序报告 P0 不一致。均为次要问题，不影响技术内容正确性。C08.09 无对应发现，已顺带通读，内容为布隆过滤器专题，准确。

## chapter-09：分布式系统（本轮回填，16/16 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C09.01 | P1 | ✅ | L85「Brewer 2000 猜想 → Gilbert & Lynch 2002 形式化证明」；L87「BASE：Basically Available/Soft-state/Eventual-consistency（Pritchett 2008）」；L160 deep「'单机 CA'是误称：单机若发生网络分区则不可用，分区容忍在分布式定义下无法被'绕过'」；L114-115「AP/CP 不是产品标签，而是系统在分区下的取舍」 | 机构归属已核校为 Gilbert & Lynch 2002；"单机 CA"误称已纠正为误称本身（不是简单"CA"）；AP/CP 从产品标签改为"分区下的取舍"描述 |
| C09.02 | P1 | ✅ | L216「2PC 并非 X/Open 首先提出，而是数据库与分布式事务领域长期演进」；L219/L278 Seata AT 全局锁 + undo log 流程标注"按目标 Seata 版本核对"；L357 版本证据「Apache Seata v2.6.0（2026-01-28）」 | 2PC/3PC 起源过度简化已修正（非 X/Open 首创）；Seata AT 全局锁/undo log 已按版本核对并标注目标版本依赖 |
| C09.03 | P1 | ✅ | L374/L384/L443/L456「ZK/etcd 的临时节点/租约只是互斥手段，资源端仍需 fencing token/唯一约束/幂等」；L384/L444「`RedissonRedLock` 在较新版本中已标记废弃」 | ZK/etcd 被说成天然严格互斥已纠正（强调 fencing/幂等、非银弹）；RedLock 支持状态（已废弃）已按版本核对 |
| C09.04 | P0 | ✅ | L571-593 可编译 Kafka 事务骨架（`transactional.id`/`initTransactions`/`beginTransaction`/`commitTransaction`，含 `ProducerFencedException` 处理）；L550「EOS 指端到端恰好一次，依赖 transactional.id + 幂等生产者 + 仅一次消费位移提交」；L594 `isolation.level=read_committed`；L607「rebalance 协议演进 KIP-848（增量协作再平衡）」 | 不可运行示例已重写为可编译骨架；EOS/transactional.id/隔离级别区分清晰；rebalance 细节（KIP-848）已补 |
| C09.05 | P1 | ✅ | L644「先止血（降级/熔断/限流）→ 再定位 → 扩容 → 回溯」分层；L660-681 决策树按数据域/影响面/可回滚性分支，未给"1000 万加速比" | "紧急处理顺序混在一起"已按四层（止血→定位→扩容→回溯）重组；无来源性能倍数已删除 |
| C09.06 | P1 | ✅ | L814/L840「Leaf-segment 重启会浪费当前号段未分配部分（已分配不丢，未分配需补持久化或接受浪费）」；L850/L870「UUID 作为聚簇索引导致页分裂与随机 IO 膨胀，但无固定倍数，需压测」；L863-876 QPS 标注为"经验量级/压测模板" | 丢号边界、UUID 索引膨胀率、QPS 均改为经验值或压测模板；号段持久化与重启语义已补 |
| C09.07 | P0 | ✅ | L901/L934 哈希取模扩容迁移量公式修正为 `1 - 1/(N+1)`；L902「查找复杂度取决于 hash 函数与实现（开放寻址/链表），平均 O(1)」；L935/L943/L950 一致性哈希「查找为有序结构（TreeMap）O(log N)，虚拟节点经验值 100~200」 | 取模扩容公式错误已修正；一致性哈希查找复杂度与虚拟节点数量（100~200）已注明实现前提 |
| C09.08 | P1 | ✅ | L1022/L1039/L1061「Token 是去重凭证，业务事务是状态机，二者边界不同」；L1025/L1042/L1132「分布式锁≠幂等保证，锁失败/超时仍可能重复执行」；L1115「Redis 快路径写入失败 → 降级到 DB 唯一约束/状态机兜底 + 重试」 | Token 与业务事务边界已厘清；锁≠幂等已写明；Redis 快路径失败补偿与清理路径已补 |
| C09.09 | P1 | ✅ | L1223-1261「RocketMQ `MessageQueueSelector` + `MessageListenerOrderly` 保证分区内顺序」；L1280-1283「RabbitMQ Quorum Queue 替代 classic mirrored queue（后者在 4.0 移除镜像模式）」；L1286-1302「Redis 标记作快路径，DB UNIQUE/状态机才是事实源」 | RocketMQ API 版本、RabbitMQ 队列架构（Quorum 替代镜像）已按当前版本重写；Redis 误标记风险已改为快路径而非唯一事实 |
| C09.10 | P1 | ✅ | L1384「FLP 针对异步确定性模型（无时钟假设、消息可任意延迟但必达）」；L1459-1471 etcd 参数按版本列出（`election-timeout`/`heartbeat-interval`/`snapshot-count` 行为随版本变化）；L1384「'暂停写入'表述不准确，应描述为'拒绝新提案/降级可用'」 | FLP 异步确定性模型限定已补；etcd 运维参数按目标版本重写；"暂停写入"已改准确 |
| C09.11 | P1 | ✅ | L1499「OpenTelemetry（CNCF，2019 合并 OpenTracing + OpenCensus）提供跨语言 API/SDK、OTLP 数据协议和 Collector」；L1499「自动插桩/Agent/eBPF 降低侵入，但其覆盖范围以官方支持矩阵为准」；L1507「仅覆盖受支持组件」；L1530「采样率结合 SLO/流量/存储压测，不能固定 1%~10%」 | OTel 时间线（2019 合并）、OTLP/Collector 语义已核对；"无侵入"绝对结论已加支持矩阵前提，未再夸大为零侵入 |
| C09.12 | P1 | ✅ | L1598「延迟双删只是特定竞态下的补救，不是所有缓存一致性方案的必然步骤」；L1621「binlog/CDC 同一 key 事件须按版本/顺序消费，失败进死信+人工兜底」；L1634-1644 按一致性等级（强一致/读己之写/单调读/最终一致）列出方案矩阵 | "必然双删"已改为竞态补救；binlog/MQ 顺序与幂等约束已补；按一致性等级列举方案、失败处理与可观测指标齐备 |
| C09.13 | P1 | ✅ | L1726「签名≠吊销：主动失效需短 TTL/版本号/denylist/状态端点」；L1759「denylist 将 jti/token hash 入 Redis，TTL=剩余有效期」；L1761「网关先剥离客户端内部身份头，认证后才由网关注入」；L1724/L1790「Redis/传输须 TLS+认证+ACL+网络隔离」 | JWT 吊销、网关防伪造身份头、加密签名与网络隔离等安全前提已补全；L1778/1790 将其列为易错点与演练项 |
| C09.14 | P0 | ✅ | L1812「`System.nanoTime()` 只适合同一 JVM 内测量耗时，不是跨节点时钟、逻辑时钟或墙上时间」；L1822「TrueTime 靠 Google 原子钟/GPS 返回带不确定性的时间区间，是有界不确定性+专用部署前提，不应把固定毫秒精度当通用结论」；L1858「`System.nanoTime()` 原点无语义、不能跨进程比较」 | HLC/Spanner/TrueTime 精度已无未来源结论（改为"有界不确定性+专用前提"）；`System.nanoTime` 误作全局逻辑时钟已纠正为单调时钟用途。⚠️ 残留：卡片 `data-priority="p2"`（L1803/L1806），与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C09.15 | P1 | ✅ | L1900「RTO/RPO 接近 0 是经设计、自动化、演练与对账验证后的目标，不是架构名称带来的天然结果」；L1923「不要将'同城双活=CP''异地多活=AP'当作架构定律」；L1987「LDC 角色/事务选择反映其公开思路，不是行业统一标准」 | 多活接近 0 前提已补；"同城双活=CP"错误标签已删除（改为按复制协议/提交确认定义）；LDC 写成通用标准已改为案例说明 |
| C09.16 | P1 | ✅ | L2024「Apache Seata v2.6.0（2026-01-28，非预发布）含 `server.raft` + `store.mode: raft` 示例配置，是否生产需核 release notes/兼容矩阵」；L2023「CDC 端到端延迟取决于全链路，不是天然毫秒级」；L2014「不是'2026 必选某方案'，而是一次可验证的架构决策」；L2069-2079 五维场景决策矩阵 | Seata 2.x Raft/版本状态已按 v2.6.0 核对；CDC≠毫秒级已写明；"2026 首选"过强已改为场景矩阵（Saga/Outbox/TCC/AT/本地消息表） |

**chapter-09 小结**：16 项内容发现全部修复到位（✅）。残留 1 处：C09.14 优先级标签 `data-priority="p2"`（L1803）与前序报告 P0 不一致（内容已修复，仅标签不一）。封面/演进/原理/实践/深度/陷阱/扩展七层结构完整，引用来源（OpenTelemetry 合并、Seata v2.6.0、RocketMQ/RabbitMQ 当前版本、FLP 异步模型、CAP 形式化）均已落位。

## chapter-10：微服务与云原生（本轮回填，9/9 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C10.02 | P0 | ✅ | L258「Route = Predicate + Filter；GatewayFilter 与 GlobalFilter 按 order 合并成链，order 小先执行，响应阶段反向回流；真正转发的是 NettyRoutingFilter（全局 Filter，链最末端、order=LOWEST_PRECEDENCE）」；L320-338 JwtAuth 自定义 Filter 演示 `mutate()` 注入身份头 | Gateway filter 类型（GatewayFilter vs GlobalFilter）、order 语义、请求/响应上下文透传已统一重写，无前后矛盾 |
| C10.03 | P0 | ✅ | L468「熔断抛 CallNotPermittedException，限流抛 RequestNotPermitted」；L469-516 可编译 Resilience4j 示例（CircuitBreakerConfig/RateLimiterConfig + fallback(request, cause) + withFallback List.of(CallNotPermittedException, RequestNotPermitted)）；L392 starter 版本「boot2 对应 resilience4j-spring-boot2、boot3 对应 resilience4j-spring-boot3」 | 异常类、降级签名（追加 Throwable 入参）、限流器语义均按目标版本核对，示例可编译 |
| C10.04 | P0 | ✅ | L590 K8s 版本里程碑（1.16 移除 extensions/v1beta1、1.20→1.24 移除 Dockershim、1.25 PodSecurityPolicy→Pod Security Admission、1.28-1.29 原生 Sidecar、1.31-1.33 Pod 垂直弹性）；L593-597 JDK 8u131/9/10/11+ 容器感知演进；L659 优雅停机（terminationGracePeriodSeconds/preStop/SIGTERM/server.shutdown=graceful）；L682-722 apps/v1 + probe + MaxRAMPercentage | Java 容器资源感知、探针与优雅停机依赖的 Boot/JDK/K8s API 版本均已统一标注 |
| C10.09 | P1 | ✅ | L1440「是否可用取决于网格与 Gateway API 版本」；L1458 全链路灰度平台分层前提（Spring Cloud 注册中心元数据/Dubbo TagRouter/Ingress/Mesh Sidecar/MQ 标签，且“并非所有平台默认可用，需先确认平台能力边界”）；L1507/1515 数据库兼容窗口（扩展→双写→切读→收缩，新旧应用兼容窗口） | 灰度/蓝绿/滚动发布的流量一致性已补部署平台前提（区分 Mesh、Ingress、发布系统与数据库兼容窗口），不再绝对化 |
| C10.15 | P1 | ✅ | L2094-2098 三支柱（Metrics/Logging/Tracing）+ Profile 第四支柱；L2096「Tracing：OpenTracing 标准 → OpenTelemetry 统一 SDK」；L2111 Exemplar 关联；L2132「OpenTelemetry Java Agent」；L2146「OpenTelemetry Collector 的 Tail Sampling Processor」 | 可观测性口径与 C09.11 一致：三支柱 + OTel Collector + 采样策略；与 C11.09 的跨章一致性将在 chapter-11 复核时二次核对（本卡内容已统一） |
| C10.20 | P0 | ✅ | L2807-2818 GlobalFilter order 表（AdaptCachedBodyGlobalFilter -2147482648 / NettyWriteResponseFilter -1 / NettyRoutingFilter LOWEST_PRECEDENCE）；L2818「鉴权 GlobalFilter order 必须 < NettyRoutingFilter.order()」；L2836 DirectBuffer 泄漏三类根因（DataBufferUtils.join 未 release / 3.1.2 前 Bug / 客户端 RST）；L2853 MDC→Reactor Context | GlobalFilter/GatewayFilter 顺序、DirectBuffer 泄漏排查路径均按当前 Gateway 3.x/WebFlux 版本核对，含实际 order 值与排查命令 |
| C10.21 | P1 | ✅ | L2989「Boot 1.5/2.x：BootstrapApplicationListener 自动创建父上下文」；L2990「Boot 3.0 / Spring Cloud 2022.0.x 停止自动创建 Bootstrap，改用 spring.config.import；恢复老行为加 spring-cloud-starter-bootstrap」；L2990 并澄清「spring.config.import/ConfigData 机制本身在 Boot 2.4（2020）已引入，并非新机制诞生点」 | Bootstrap 上下文移除时间与新 Config Data 机制已分清（旧模式 vs 新 import），不再混写 |
| C10.22 | P1 | ✅ | L3141-3145 Sleuth 1.x/2.x/3.x → Micrometer Tracing 1.0（Boot 3.0，2022-11）→ 1.2+（2024）→ 1.3+（W3C 默认）；L3145「W3C TraceContext 自 Micrometer Tracing 1.0/Boot 3.0 起为默认，B3 可配置切换」；L3178-3187 W3C/B3 传播表；L3189 sampling、L3191 MDC | Sleuth→Micrometer Tracing 桥接、B3/W3C 与 MDC 配置均按目标 Boot/Tracing 版本重写，准确 |
| C10.25 | P1 | ✅ | L3849「Dubbo 3.x（2021）引入 Triple 协议（gRPC over HTTP/2）与应用级服务发现」；L3864「3.x Triple(gRPC) 改善跨语言」；L3880「Dubbo 3 推荐应用级服务发现 register-mode=instance」；L3890「接口级发现 URL 爆炸→应用级发现降一到两个数量级」 | Dubbo/Triple 协议、服务治理能力对比已按 Dubbo 3.x 当前文档重写，未绝对化为旧 2.x |

**chapter-10 小结**：9 项内容发现全部修复到位（✅）。无次要残留。卡片版本标注严谨（K8s 1.16~1.33、JDK 8u131~11+、Gateway 3.x/WebFlux、Spring Cloud 2022.0.x、Dubbo 3.x/Triple、Sleuth→Micrometer Tracing 1.0~1.3），七层结构完整。C10.15 与 C09.11 在本卡层面口径一致，与 C11.09 的跨章最终一致性留待 chapter-11 复核确认。

## chapter-11：中间件与工程化（本轮回填，11/11 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C11.11 | P0 | ✅ | L1879/1993 KRaft 时间线「2.8 引入预览、3.3 生产就绪、4.0 移除 ZK」；L1930-1955 事务示例用 `sendOffsetsToTransaction(offsets, consumer.groupMetadata())`（Kafka 2.5+ 正确 API）；L1934 明确 `initTransactions()` 前提（producerProps 必须配 `transactional.id` 且 `enable.idempotence=true`）；L1889-1903 EOS 三要素 + 事务协调器两阶段提交；L1902 `isolation.level=read_committed` 过滤 Abort；L1905-1910 EOS 边界（跨外部系统退化为业务幂等/Outbox+CDC） | 不可运行示例已重写为可编译事务骨架；KRaft/ISR/EOS/consumer-group 细节均已按当前 client/broker 版本核对。⚠️ 极轻残留：L1943 `transform(r)` 为业务转换占位方法（未在本卡定义），属面试示例惯例，读者需自行实现；不影响 API 正确性 |
| C11.12 | P2 | ✅ | L2017「基础限流算法、熔断状态机、Spring Cloud Gateway 实现、灰度染色原理详见 C10.03/C10.02/C10.09」；L2017 并锚定 SC Gateway 过滤器链与转发末端（NettyRoutingFilter, order=LOWEST_PRECEDENCE）以 `C10.20` 为准；L2035/L2056 重复指向 C10.x 增量 | API 网关限流/熔断/灰度与 C10.02/C10.20 的口径不一致已消解：本卡显式 defer 产品实现到 C10.x，自身聚焦网关层 vs 服务层纵深协同 + AI 流量治理（Token 限流/MCP 配额/流式背压）增量，无重复展开 |
| C11.13 | P1 | ✅ | L2142「各框架运维成熟度、社区现状与详细对比见 C11.21（两卡互补，不重复展开）」；本卡覆盖设计/四大问题/分片故障转移原理/选型矩阵 | 与 C11.21 主题高度重复已解决。注：前序报告建议"合并为单卡"，实际修复采用"互补拆分"（C11.13=设计原理+四大问题，C11.21=框架对比+社区状态），重复段落已消除、职责不重叠，属可接受等价修复 |
| C11.14 | P1 | ✅ | L2282-2290 callout「许可演进（关键）」：Apache 2.0 至 7.10.2（OpenSearch 即基于此分叉）；7.11+ 改 ELv2+SSPL 双许可（非 OSI 认证开源）；L2287「X-Pack 安全免费化自 6.8/7.1 起在 Basic 授权下免费，并非 7.7；7.7 起才是 dense_vector + 近似 KNN」；L2273-2281 版本时间线（1.x→8.x）准确 | Elasticsearch/X-Pack 许可与版本演进不准确已重写：许可边界（Apache 2.0→双许可）、X-Pack 免费起点（6.8/7.1 非 7.7）均已正确区分，并纠正潜在误述 |
| C11.15 | P1 | ✅ | L2538 深度追问「proto3 默认字段无 presence（无 optional 语义）……如需判定需声明显式 optional 关键字（protobuf 3.12+ 重新引入，行为同 proto2）」；L2453「HTTP/2 提供流级/连接级流量控制（滑动窗口），gRPC 背压依赖该机制而非应用层」；L2481-2501 有效 proto3 示例（`syntax="proto3"` + service/message） | proto3 `optional`（3.12+ 重新引入）、gRPC 流控（HTTP/2 滑动窗口背压）、代码生成示例均按当前 protobuf/gRPC 插件核对，无版本错误 |
| C11.16 | P1 | ✅ | L2606「Apollo 长轮询（服务端 hold 连接）」；L2607/L2620「Nacos gRPC 长连接（2.x）/长轮询+UDP（1.x 兼容）」；L2621「Nacos AP/CP 可切换，Apollo 强一致（DB）」；L2584「Nacos 2.0（2021）……官方基准测试称约 10x 提升，实际以官方与自身压测为准」 | Nacos/Apollo 一致性模型、推送机制已准确区分；无来源容量数字已删除或加「以官方与自身压测为准」免责（L2584/L2713），未再呈现为事实 |
| C11.17 | P1 | ✅ | L2757「checksum 校验防篡改、flyway repair 修正历史表、Baseline 设定基线版本、Undo 仅 Teams 付费版（社区版无自动回滚）」；L2757「Liquibase 回滚仅当 changeset 显式定义 rollback 块时生效」；L2758「DATABASECHANGELOGLOCK 锁表串行化」；L2759/L2799/L2804 不可回滚 DDL 策略（向前兼容迁移/Expand-Contract/备份+PITR） | Flyway/Liquibase 的 checksum、锁、基线与回滚能力描述不完整已补全；不可回滚 DDL 治理（向前兼容、Expand-Contract、PITR 兜底）策略齐备 |
| C11.18 | P1 | ✅ | L2861「RocketMQ 5.x（2022）：Proxy 无状态代理 + gRPC 客户端协议（RIP-39）；客户端 SDK 分 Remoting SDK（4.x/5.x 通用）与 gRPC SDK（仅 5.0+，多语言），二者 API 不兼容需改代码迁移」；L2879-2889 事务消息（Half+回查）；L2900「延迟队列固定 18 level，5.x gRPC API 额外支持任意精度 timing message」；L2957-2958 DLQ（%DLQ%…重试 16 次）+ 18 档重试间隔 | RocketMQ 5.x 事务/延迟/客户端兼容性表述不完整已修正：明确 4.x/5.x 架构与双 SDK 协议边界、事务/延迟/顺序/DLQ 机制准确；容量数字加「业界参考基准，需以自身生产数据替换」免责（L2946） |
| C11.19 | P1 | ✅ | L3021「局限：内核/BTF 前提——基础 eBPF 需 4.9+ 稳定；CO-RE 需内核启用 BTF（5.1+，或发行版随镜像提供 BTF 转储），否则按内核版本重编译」；L3011/L3028「eBPF 与 Agent 互补而非替代，OTel 统一采集」；L3030「权限随内核演进收敛——5.8+ 引入细粒度 CAP_BPF，无需再授 CAP_SYS_ADMIN；校验器强制内存安全」 | eBPF 采集点/内核版本/安全边界过度泛化已纠正：明确 kernel/BTF/CO-RE 前提、OTel/Agent 边界、校验器与 CAP_BPF 安全边界 |
| C11.20 | P2 | ✅ | L3077「（注意：预留/Spot 折扣、跨 AZ 流量计费、账单粒度等具体机制高度依赖云厂商，本卡给出通用方法论，落地须对照目标平台计费文档与 API）」；L3061 三大支柱 Inform→Optimize→Operate；L3077/L3089-3094/L3095-3116 覆盖云账单 + K8s 成本模型（HPA 示例）+ 业务归因（Tag/Label） | FinOps 与 HPA/调度器/存储成本联动缺平台前提已补：显式平台前提免责，并拆分为云账单、K8s 成本模型、业务归因三段，HPA 示例（autoscaling/v2）准确 |
| C11.21 | P1 | ✅ | L3159「调度四大问题、分片/故障转移原理与完整选型矩阵见 C11.13（两卡互补，不重复展开）」；L3170「Elastic-Job（当当）：社区并入 Apache 后改名 ShardingSphere-ElasticJob」；L3166-3171 Quartz/XXL-Job/Elastic-Job 现状描述 | 与 C11.13 重复已消解（互补拆分，见 C11.13）；Quartz/XXL-Job/Elastic-Job 现状已按社区维护状态更新（Elastic-Job→ShardingSphere-ElasticJob） |

**chapter-11 小结**：11 项内容发现全部修复到位（✅）。无 ❌。残留 1 处极轻（C11.11 事务示例中 `transform(r)` 为占位方法，属面试示例惯例，不影响 API 正确性）。
- **重复卡处理（C11.13/C11.21）**：前序报告建议"合并为单卡"，实际修复采用"互补拆分"（C11.13 讲设计原理与四大问题、C11.21 讲框架对比与社区状态），重复段落已消除、职责不重叠，属可接受的等价修复，且两卡互相锚定（L2142↔L3159）。
- **版本/许可准确性**：C11.14（ES 许可 Apache 2.0→ELv2+SSPL、X-Pack 6.8/7.1 免费）、C11.15（proto3 optional 3.12+）、C11.17（Flyway/Liquibase 版本能力）、C11.18（RocketMQ 4.x/5.x 双 SDK）均已按当前版本重写并标注前提。
- **无来源数字**：C11.16/C11.18/C11.19 涉及容量/性能的数字均加「以官方与自身压测为准」或「业界参考基准」免责，未再呈现为事实。
- **跨章一致性收口**：C11.09（三支柱+OTel Collector+采样）与 C09.11、C10.15 口径一致，chapter-09/10/11 可观测性表述在本轮复核中已三级对齐，C10.15 遗留的跨章一致性确认项已闭环。

## chapter-12：AI 工程化（本轮回填，12/12 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C12.01 | P0 | ✅ | L99「Spring AI（2025 GA）统一 AI 应用开发」；L100「ChatClient Fluent API 在 1.0.0-M1（2024-05）才引入，并非 0.8 即有」；L102「Spring AI 1.0 GA（2025）+ MCP」；L165-167 ChatModel vs ChatClient、Advisor 链（QuestionAnswerAdvisor/PromptChatMemoryAdvisor）；L204-207 `@Tool`/`@ToolParam` 可编译示例 | Spring AI 发布时间线与 Advisor/ChatClient API 已按 1.0 GA 重写，无伪造类/方法，演进脉络（0.8.x→1.0 M→1.0 GA）准确 |
| C12.02 | P1 | ✅ | L298 RAG 2020 Facebook 论文；L324 离线建库(1-4)/在线问答(5-7) 分离；L330-334 七环节表（含失效模式与优化）；召回/精度定义在 C12.03（相似度度量表）/C12.29（评测集与召回率）给出；成本为定性描述（L391「延迟与 Token 成本上升」）未给无来源金额 | RAG 指标/召回/精度已建立定义与流程，Agentic RAG 成本以定性表述为主、未写无来源百分比。⚠️ 残留：卡片 `data-priority="p0"`（L264）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C12.03 | P0 | ✅ | L457 InfoNCE 对比学习损失；L463-467 余弦/点积/L2 三相似度度量表；L468「归一化后余弦相似度=点积=1-L2²/2」；L573-574 容量公式「字节=维度数×每维字节数，float32=4B、binary=0.125B」，相对 1024 维 float32 全流程压缩 128x；bge-m3 1024 维（L509/514） | 量化后字节数、维度与内存估算已按模型与量化格式给出公式与容量假设，纠正原估算错误。⚠️ 残留：卡片 `data-priority="p1"`（L432）与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C12.06 | P0 | ✅ | L911-932 Spring AI 1.0 GA 真实 `@Tool`/`@ToolParam` 注解（自动生成 JSON Schema）；L904 `FunctionToolCallback.builder()` 注册；L925 `.tools(new RentTools())` 可编译调用 | Function Calling 疑似伪造 SDK 方法名/回调注册已改为目标版本真实 `@Tool`/`@ToolParam` 注解 + 可编译示例 |
| C12.07 | P1 | ✅ | L1004 MCP（Anthropic 2024.11 主导标准）；L1051 三大原语 Tools/Resources/Prompts；L1052 传输层 stdio + Streamable HTTP 两种、均基于 JSON-RPC 2.0，Client/Server 解耦于具体传输 | MCP/Agent 框架协议版本与能力边界已按规范区分（传输/工具/资源），未超前或混用 |
| C12.13 | P1 | ✅ | L1855「LangChain4j 与 Spring AI 是两条独立的 Java AI 框架血脉……互为补充而非子集/替代品」；L1910-1918 对比表（模型适配数 30+/20+、框架中立：Spring 专属否）；L1993 与 Spring AI 分层协作而非替代 | LangChain4j 定位与 Spring AI 边界已纠正为独立/互补框架，非子集或替代品。⚠️ 残留：卡片 `data-priority="p2"`（L1849）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C12.16 | P1 | ✅ | L2501-2512 WebFlux SSE 端点（`Flux<String>` + `produces=TEXT_EVENT_STREAM_VALUE`）；L2509 `onBackpressureBuffer(100)`；L2510 `onErrorResume`（异常转错误事件防断连）；L2511 `concatWith("[DONE]")`；L2482 背压三策略（buffer/drop/latest） | `stream()`/Flux/SSE 端点/错误信号组合已用 WebFlux 当前 API 严谨验证，未混写 WebMVC |
| C12.21 | P0 | ✅ | L3178-3194 Milvus 2.x Java SDK 真实 API（`IndexParam`/`SearchParam` + `withExtraParam` JSON，无无效 `BufferOverflowStrategy`）；L3157-3165 HNSW/IVF_PQ 参数 M/efConstruction/efSearch/nlist/nprobe；L3201「十亿级别别用 HNSW」；性能为区间（L3705 等「需以自身生产数据替换」） | Milvus/BufferOverflowStrategy 等无效参数与 API 已删除，按 2.x SDK 重写；性能结论改为区间不加精确 QPS/延迟承诺。⚠️ 残留：卡片 `data-priority="p1"`（L3127）与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C12.25 | P1 | ✅ | L3622 Last-Event-ID 续传；L3631 `onBackpressureBuffer(N, DROP_OLDEST)` + Redis 状态外置补偿（缓冲丢弃的旧 token 由 Redis 续传，不真正丢失）；L3655 有界缓冲；L3660 网关 `proxy_buffering off`；L3703-3707 压测基准「参考基准，需以自身生产数据替换」 | SSE 断连恢复、幂等 ID、背压与代理缓冲边界已补全，量化数字加自身生产数据免责 |
| C12.26 | P0 | ✅ | L3789 语义缓存相似度阈值 0.92；L3741 命中率 20-40%；L3841 缓存随知识库更新失效（带版本/更新失效）；L3856-3865 命中率/成本「参考基准，需以自身生产数据替换」 | 语义缓存的相似度阈值、命中一致性与失效策略已补全，数字加免责。⚠️ 残留：卡片 `data-priority="p0"`（L3721）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C12.29 | P1 | ✅ | L4126 CI 卡门统计前提：评测集 ≥200 条、95% 置信区间、p<0.05 显著、人工评审 5%-10%、回归容忍 2%；L4153-4155 阈值示例（忠实度≥0.85/格式≥98%）；L4121 规模 200-1000 | LLM 评测指标与 CI 卡门阈值已定义统计前提（数据集/方差/显著性/人工比例），消除原缺前提问题 |
| C12.31 | P1 | ✅ | L4342/4351/4366 GDPR/个保法具名；数据边界（境内驻留 L4352）；加密（vault 反向脱敏 L4365）；模型供应商差异（国产通义/百炼/DeepSeek vs 境外 OpenAI/Anthropic L4434）；三层记忆+PII 脱敏+删除权全链路（L4411-4416） | 会话存储/脱敏/留存/跨区域合规已从过度泛化改为标注法规、数据边界、加密与模型供应商数据处理差异 |

**chapter-12 小结**：12 项内容发现全部修复到位（✅）。含 6 处**优先级标签不一致**（C12.02/C12.03/C12.13/C12.16/C12.21/C12.26 的 `data-priority` 与前序报告标注不一致），均为内容已修复、仅属性标签不一，不影响技术内容正确性。
- **API 准确性（P0 重点）**：C12.01（Spring AI 1.0 GA 时间线/Advisor/ChatClient）、C12.06（真实 `@Tool`/`@ToolParam`）、C12.21（Milvus 2.x SDK 无无效 `BufferOverflowStrategy`）均已按目标版本重写，无伪造类/方法/参数；示例代码可编译。
- **量化/数学修正**：C12.03 字节数/维度/内存容量公式已按模型与量化格式给出（float32=4B、binary=0.125B、128x 压缩）。
- **无来源数字治理**：C12.25/C12.26 的压测/命中率/成本数字均加「参考基准，需以自身生产数据替换」免责，未再呈现为事实结论。
- **边界澄清**：C12.07（MCP 原语与传输）、C12.13（LangChain4j 与 Spring AI 独立互补）、C12.31（合规按法规具名+数据边界+加密+模型差异）均已消除原混用/过度泛化。
- **结构残留（非 12  findings 之一）**：文件 L4497+ 在 `</html>`（L4496）之后仍存在一段孤立的「传统召回评估指标 / RAG Recall@K 代码」片段（疑似从 C12.02 漂移出的内容），属 HTML 结构残留，不影响任一发现的技术结论，建议顺手回收或归入对应卡片。

## chapter-13：网络与高性能 IO（本轮回填，9/9 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C13.02 | P1 | ✅ | L217-383 区分主动关闭方（TIME_WAIT 归主动关闭方）/端口复用（SO_REUSEADDR 与 SO_REUSEPORT）/内核参数（`tcp_tw_reuse` 仅客户端生效、`tcp_tw_recycle` 已于 Linux 4.12 移除）/负载均衡 SNAT 放大 TIME_WAIT | TCP 状态机与 TIME_WAIT 语义已由"过度简化"改为按角色、参数、内核版本、负载均衡四维度拆分，无混写。⚠️ 残留：卡片 `data-priority="p0"`（L217）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C13.03 | P1 | ✅ | L388-510 HTTP/1.1→2(RFC 7540)→3(RFC 9114) 时间线；TCP HOL 阻塞与 HTTP/2 多路复用、`h2c`/ALPN/`h3`、QPACK、各版本 TLS 集成边界 | HTTP/2/3/QUIC/TLS 的时间线与能力边界已按 RFC 与主流网关/浏览器支持重写，未再笼统混述。⚠️ 残留：卡片 `data-priority="p0"`（L388）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C13.04 | P1 | ✅ | L515-656 TLS 1.2（2-RTT）vs 1.3（1-RTT/0-RTT）、ECDHE/PFS、SNI/ALPN、OCSP Stapling、0-RTT 重放风险分别展开 | TLS 1.2/1.3 握手、前向安全与证书验证细节已分协议、密钥调度、SNI/ALPN、证书链校验展开，互不混杂。卡片 `data-priority="p1"`（L515）与前序报告 P1 一致 |
| C13.05 | P1 | ✅ | L661-816 L711「epoll/kqueue 是'事件驱动/就绪通知'…Windows 的 IOCP 是'完成驱动'…Java NIO 的 Selector 抽象统一为就绪模型」；`selectedKeys()` 必须 `remove()`（L711 附近）、事件丢失/重复、`epoll` 空轮询 busy-spin bug + Netty 重建 Selector 补丁 | Linux Selector/epoll 与 Java NIO 语义已从"过度对应"改为就绪集合/事件丢失重复/空轮询补丁/平台差异分层。⚠️ 残留：卡片 `data-priority="p0"`（L661）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C13.06 | P1 | ✅ | L821-972 EventLoop 单线程模型、Boss/Worker Reactor、`Pipeline` 异常传播（入站 `exceptionCaught` vs 出站 `ChannelFuture`）、`SO_BACKLOG` 为 parent（boss）选项 | Netty backlog/EventLoop 绑定/Pipeline 传播已按当前版本源码示例核对配置名与异常传播路径。⚠️ 残留：卡片 `data-priority="p0"`（L821）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C13.07 | P1 | ✅ | L977-1099 `ResourceLeakDetector` 四级（DISABLED/SIMPLE 1%/ADVANCED/PARANOID）、PoolArena/jemalloc 思路、refCnt、`SimpleChannelInboundHandler` 自动释放 | ByteBuf 历史、池化分配器与泄漏检测级别已按当前 Netty 版本重写，无过时级别/API。卡片 `data-priority="p1"`（L977）与前序报告 P1 一致 |
| C13.08 | P1 | ✅ | L1104-1235 L1184 sendfile/mmap/DMA gather/kTLS/`FileChannel.map()` 的平台/API 条件分别标注（Windows TransmitFile、SG 需 NIC 支持、TLS 在未启用 kTLS 时使零拷贝失效） | sendfile/mmap/kTLS/`FileChannel.map()` 的平台/API 条件已由"混写"改为按 OS/JDK/文件系统/加密分项，零拷贝生效条件清晰。⚠️ 残留：卡片 `data-priority="p0"`（L1104）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C13.11 | P1 | ✅ | L1558-1647 io_uring SQ/CQ 环形队列、完成驱动模型；L1591「JDK 21 虚拟线程…本质仍是 epoll 事件驱动…它并不直接使用 io_uring」明确删除"Loom 依赖 io_uring"暗示 | io_uring 参数、提交/完成队列与 Project Loom 关系已按内核与 JDK 独立描述，混淆项已纠正。⚠️ 残留：卡片 `data-priority="p2"`（L1558）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C13.12 | P1 | ✅ | L1652-1729 系统调用用户态/内核态切换成本、epoll vs select 差异、sendfile/mmap 与 Java 调用的映射、Loom=epoll 与 C13.11 互锚 | 系统调用、用户态/内核态切换与 Java IO 模型映射已由"过强对应"改为调用链路图区分 blocking/NIO/sendfile 真实内核路径。⚠️ 残留：卡片 `data-priority="p0"`（L1652）与前序报告 P1 不一致（内容已修复，仅标签不一） |

**chapter-13 小结**：9 项内容发现全部修复到位（✅）。含 7 处**优先级标签不一致**（C13.02/C13.03/C13.05/C13.06/C13.08/C13.11/C13.12 的 `data-priority` 与前序报告标注不一致），均为内容已修复、仅属性标签不一，不影响技术内容正确性；C13.04/C13.07 标签与原报告一致。
- **TCP/HTTP/TLS 分层**：C13.02（TIME_WAIT 按角色+内核参数+LB 拆分）、C13.03（HTTP/1.1→3 按 RFC 时间线）、C13.04（TLS 1.2/1.3 分协议展开）均已消除原"过度简化/混写"。
- **NIO/Netty 精确化**：C13.05（Selector 就绪模型 vs IOCP 完成驱动、空轮询补丁）、C13.06（EventLoop/backlog/Pipeline 异常传播）、C13.07（ResourceLeakDetector 四级+refCnt）均已按当前版本源码核对。
- **零拷贝/异步边界澄清**：C13.08（零拷贝各路径平台/API 条件分项）、C13.11（删除 Loom 依赖 io_uring 暗示）、C13.12（调用链路图区分内核路径）已纠正原跨层强对应。

## chapter-14：数据库与存储（本轮回填，9/9 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C14.01 | P1 | ✅ | L96-101 分片 1.6 引入/2.2 生产成熟、WiredTiger 3.0 引入/3.2 默认、4.0 多文档事务、4.2 跨分片 2PC、5.0 时间窗事务、7.0 Queryable Encryption；L137 Raft 变体选举、writeConcern w:majority；L139 WiredTiger B+树+MVCC+文档级锁 | MongoDB/WiredTiger、分片事务、oplog、选举细节已按当前版本核对（事务 4.0·跨分片 2PC 4.2），无过时版本号。⚠️ 残留：卡片 `data-priority="p0"`（L62）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C14.02 | P0 | ✅ | L286-296 `$vectorSearch`（index/path/queryVector/numCandidates/limit/filter 真实字段）；L333-338 Spring AI `MongoDBAtlasVectorStore.builder(mongo, model).vectorIndexName(...)` 方法名为 `vectorIndexName` 非 `indexName`；L298 ANN 召回"典型区间约 95%-99%"为定性区间；L300-305 pre/post-filter 策略；L369 性能边界"千万级向量量级" | Atlas Vector Search 与 Spring AI/Mongo driver API 已按官方版本重建（vectorIndexName 已纠正），过滤与 ANN 性能改为区间/定性表述，未再给无来源硬数字。⚠️ 残留：卡片 `data-priority="p1"`（L234）与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C14.03 | P0 | ✅ | L492-523 Milvus v2 Java SDK：`CreateCollectionReq.builder().field(AddFieldReq.builder()...)`、`IndexParam.builder().indexType(...).metricType(...).extraParams(Map.of("M",16,"efConstruction",200))`、`client.loadCollection(LoadCollectionReq...)`、`client.search(SearchReq.builder()...)` 返回 `SearchResp`、`FloatVec` | Milvus 组件职责、索引参数与 SDK 方法已按 2.x 当前 SDK 校验（extraParams 用 Map 而非无效 JSON），无失效字段/方法。⚠️ 残留：卡片 `data-priority="p1"`（L396）与前序报告 P0 不一致（内容已修复，仅标签不一） |
| C14.04 | P1 | ✅ | L619 Qdrant 选 Rust（零成本抽象+无 GC+内存安全）；L629 HNSW；L631 Payload 索引；L635-638 pre-filter 自动切精确 KNN / post-filter；L654-688 Java SDK `QdrantClient`/`createPayloadIndexAsync`(PayloadSchemaType.Keyword/Integer)/`FloatVectors`/`Filter`/`SearchPoints.newBuilder().setFilter().setLimit()` | Qdrant payload 索引、过滤模式与客户端 API 已按官方 client 重写（FloatVectors/SearchPoints 对应），pre/post-filter 与 HNSW 参数一致。卡片 `data-priority="p1"`（L587）与前序报告 P1 一致 |
| C14.05 | P1 | ✅ | L767 TiFlash 列存 GA 归 4.x（2020）、HTAP 成熟 5.x、8.x Vector Search；L795 Region 96MB、Raft Leader 选举/日志复制；L799-804 Percolator 两阶段（Prewrite/Commit + primary lock）+ MVCC SI + TSO；L1103 等跨章一致 | TiDB/TiFlash/OceanBase 事务与副本协议已从过度简化改为按当前架构文档写（TiFlash GA 4.x、Percolator 2PC、Raft）。卡片 `data-priority="p1"`（L728）与前序报告 P1 一致 |
| C14.06 | P1 | ✅ | L923 版本演进：Lightweight DELETE 归 22.8（2022）、Variant 归 24.3 实验/24.8 正式、Query Cache 23.x、JSON 24.x；L956-961 MergeTree 三要素（PARTITION BY/ORDER BY/Part 合并）；L963 物化视图=预聚合自动维护表；L965 ReplacingMergeTree 去重+FINAL | ClickHouse 版本、MergeTree 行为与物化视图一致性已按当前版本核对（Lightweight DELETE 22.8、Variant 24.8 正式），最终一致性描述准确。卡片 `data-priority="p1"`（L886）与前序报告 P1 一致 |
| C14.07 | P1 | ✅ | L1101 GQL 标准（ISO/IEC 39075，2024）；L1103 Neo4j 5.x「APOC Core 转正」（450+ 过程入官方包）、GDS 库成熟；L1130 Cypher MATCH 模式匹配；L1226 末尾明确「复杂查询应先用 EXPLAIN/PROFILE 验证是否走 NodeIndexSeek 而非 AllNodesScan」；L1247 量化结论加「参考基准，需以自身生产数据替换」 | Neo4j Cypher、APOC 可用性与执行计划已核对（APOC 5.x 转正、补 EXPLAIN/PROFILE 提示），量化数字加免责。⚠️ 残留：卡片 `data-priority="p2"`（L1066）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C14.08 | P1 | ✅ | L1286 OceanBase「HTAP 列存副本（4.0 起支持列存副本 + 向量化执行）」正确表述为列存副本而非 OBKV；L1354-1366 扩展补全 OceanBase vs TiDB（Paxos vs Raft、LSM、2PC+GTS），OBKV 仅作为 KV 接口提及 | CockroachDB/YugabyteDB/OceanBase/TiDB 能力对比已建立版本化表述（OceanBase 列存副本 4.0 起、删除"全面更优"结论），OBKV 概念边界厘清。卡片 `data-priority="p1"`（L1256）与前序报告 P1 一致 |
| C14.09 | P1 | ✅ | L1402 时序数据特征（高基数 tag 组合爆炸）；L1403 delta-of-delta 时间戳编码/Gorilla 浮点压缩；L1407-1410 InfluxDB(measurement+Tag/Field)/TimescaleDB(PG hypertable)/Prometheus/TDengine 模型；量化结论以「业界常见量级/参考基准，需以自身生产数据替换」标注 | InfluxDB/TimescaleDB 架构、压缩与高基数建议已按当前版本重写模型与保留策略，无无来源硬结论。⚠️ 残留：卡片 `data-priority="p2"`（L1375）与前序报告 P1 不一致（内容已修复，仅标签不一） |

**chapter-14 小结**：9 项内容发现全部修复到位（✅）。含 5 处**优先级标签不一致**（C14.01/C14.02/C14.03/C14.07/C14.09 的 `data-priority` 与前序报告标注不一致），均为内容已修复、仅属性标签不一，不影响技术内容正确性；C14.04/C14.05/C14.06/C14.08 标签与原报告一致。
- **版本事实核实（核心修复）**：C14.01（分片 1.6/2.2、WiredTiger 3.0/3.2、4.0 事务·4.2 跨分片 2PC）、C14.05（TiFlash GA 4.x）、C14.06（Lightweight DELETE 22.8、Variant 24.8 正式）均按官方版本史重写，无伪造/过时版本号。
- **SDK/API 准确性**：C14.02（Spring AI `vectorIndexName` 纠正）、C14.03（Milvus v2 `IndexParam.extraParams(Map)`/`SearchResp`）、C14.04（Qdrant `FloatVectors`/`SearchPoints`）均按目标版本 SDK 重建示例，无失效方法/字段。
- **能力边界厘清**：C14.08（OceanBase HTAP 列存副本而非 OBKV、删除"全面更优"）、C14.07（APOC 5.x 转正 + EXPLAIN/PROFILE 提示）已消除原缺版本边界/可用性错误。
- **无来源数字治理**：C14.02/C14.07/C14.09 的量化结论均加「参考基准，需以自身生产数据替换」免责，未再呈现为事实。

## chapter-15：响应式编程（本轮回填，6/6 ✅）

| 位置 | 优先级 | 复核结论 | 关键证据 | 说明 |
|---|---|---|---|---|
| C15.01 | P0 | ✅ | L106 Reactive Streams 四接口契约（Publisher/Subscriber/Subscription/Processor）+ request(n) 拉取；L114-123 背压四策略（BUFFER/DROP/LATEST/ERROR）；L138 `publishOn`(下游)/`subscribeOn`(上游) 明确区分；L250-280 MDC 传播（Hooks.onEachOperator 恢复 MDC、contextWrite/deferContextual 写入读取、Context 不可变"最近写入者生效"） | Reactor 调度、背压 request 传播与 MDC/Hooks 已从混写改为分别绘制 publishOn/subscribeOn、request 传播与 context 传播（三个独立机制）。卡片 `data-priority="p0"`（L59）与前序报告 P0 一致 |
| C15.02 | P1 | ✅ | L327 Netty EventLoop（CPU×2 共享）；L331 背压全链路传导（Netty 写缓冲满→反压 Controller Flux→R2DBC/WebClient 自动降速）；L333-350 WebMVC vs WebFlux 全维度对比；L352-363 迁移成本矩阵（依赖画像/SSE/流式、阻塞隔离 boundedElastic 或替代、吞吐收益前提=全栈非阻塞）；L319 Virtual Threads 削弱 WebFlux 价值 | WebFlux 与 MVC 的阻塞依赖、连接池与吞吐结论已改为依赖画像、SSE/流式、阻塞隔离与迁移成本矩阵，删除"全面更优"式绝对结论。⚠️ 残留：卡片 `data-priority="p0"`（L287）与前序报告 P1 不一致（内容已修复，仅标签不一） |
| C15.03 | P1 | ✅ | L493 R2DBC 技术分层（API 规范/驱动/框架/执行模型），明确「HikariCP 是 JDBC 连接池，不适用于 R2DBC；R2DBC 用 r2dbc-pool」；L502 SPI（ConnectionFactory/Connection/Statement/Result 全部返回 Publisher）；L506 `r2dbc-pool` 异步获取（create 返回 Mono）；L508 `TransactionalOperator`（替代 @Transactional）；L510-524 JDBC vs R2DBC 对比 | R2DBC 连接属性、事务传播与批量操作 API 已按目标 R2DBC driver 与 Spring Data R2DBC 版本验证（连接池/事务/对比无误）。卡片 `data-priority="p1"`（L457）与前序报告 P1 一致 |
| C15.04 | P1 | ✅ | L681「onError 是终止信号，沿数据流向下游传播（与 try-catch 向上相反）」；L692 onErrorResume/onErrorReturn/doOnError/onErrorMap 位置语义；L719 异常信号图注明「retry 在前、onErrorResume 在后构成先重试后降级」；L722 `Retry.backoff(3,1s).jitter(0.5).filter(可重试异常)`；L814 区分 BlockHound（开发/测试期阻塞检测，配 @Profile("!prod")）与 Resilience4j 断路器（生产熔断），职责不混用 | 错误传播方向、retry 与 onErrorResume 位置已用异常信号图重写；BlockHound 配置区分开发期检测与生产熔断。卡片 `data-priority="p1"`（L647）与前序报告 P1 一致 |
| C15.05 | P1 | ✅ | L865 VT 调度（阻塞 unmount 载体线程，不占 OS 线程）；L875 Pinning（synchronized/native 块内阻塞无法 unmount，JDK 21 仍 pin，JDK 24 JEP 491 修复，解法则 ReentrantLock 替换，检测 -Djdk.tracePinnedThreads）；L877 结构化并发（JEP 453/499/505）；L879-896 三模型对比；L898-909 兼容性分场景评估（Tomcat/Netty/JDBC-HikariCP/Redis Lettuce/Jedis/CPU 密集） | 虚拟线程开关、阻塞驱动兼容性与响应式迁移结论已按具体容器/JDBC 驱动/Redis 客户端/线程模型分别评估，删除过度绝对化。卡片 `data-priority="p1"`（L833）与前序报告 P1 一致 |
| C15.06 | P0 | ✅ | L1088 全链路背压从客户端经 Web 层/服务层/数据层反压传导；L1128 缓存回写注释「禁止手动 subscribe() 破坏 WebFlux 请求契约」已改用链式返回；L1141 响应式事务 `.as(txOp::transactional)`（返回 Publisher 的事务模板，非控制器手动订阅）；L1113-1157 全栈 WebFlux+R2DBC+Reactive Redis+WebClient 示例；L1221 StepVerifier 测试 | 手动 subscribe() 破坏 WebFlux 请求绑定契约的问题已消除（控制器返回 Publisher、事务用 TransactionalOperator 包裹）；响应式事务边界已补全。⚠️ 残留：卡片 `data-priority="p2"`（L1039）与前序报告 P0 不一致（内容已修复，仅标签不一） |

**chapter-15 小结**：6 项内容发现全部修复到位（✅）。含 2 处**优先级标签不一致**（C15.02/C15.06 的 `data-priority` 与前序报告标注不一致），均为内容已修复、仅属性标签不一，不影响技术内容正确性；C15.01/C15.03/C15.04/C15.05 标签与原报告一致。
- **机制拆分（核心修复）**：C15.01（publishOn/subscribeOn、request 拉取、context 传播三机制独立绘制）、C15.04（onError 向下游传播、retry 在 onErrorResume 前的信号图）已将原混写内容按机制拆分清晰。
- **结论去绝对化**：C15.02（WebFlux vs MVC 改为依赖画像+迁移成本矩阵）、C15.05（VT 按容器/JDBC/Redis/线程模型分别评估，保留"不能完全替代 Reactive"边界）已消除原过强吞吐/迁移结论。
- **API 准确性**：C15.03（r2dbc-pool 非 HikariCP、TransactionalOperator 替代 @Transactional）、C15.06（用返回 Publisher 的事务模板替代控制器手动 subscribe）均已按目标版本验证。
- **开发期/生产边界厘清**：C15.04 明确 BlockHound（开发/测试检测）与 Resilience4j 断路器（生产熔断）职责分离，不混用。

---

## 二次复核总结论（chapter-01 ~ chapter-15）

| 维度 | 结果 |
|---|---|
| 复核范围 | review-findings.md 全文（chapter-01 ~ chapter-15） |
| 总发现数 | 141 条（逐篇累加：1~15 章合计见总览表） |
| 通过（✅） | 140/141 逐篇复核通过（仅 chapter-07 有 1 处 ❌） |
| 未通过（❌） | 1（位于 chapter-07，详见该章小结） |
| 次要残留（⚠️） | 主要为「优先级标签（data-priority）与前序报告标注不一致」，集中在 chapter-04/05/06/07/08/09/12/13/14/15，均为内容已修复仅属性标签不一 |
| 结论 | 除 chapter-07 有 1 处 ❌（前序报告已记录的具体发现未修复/修复错误）外，前序报告所列其余发现均已按 fix-progress.md 声明与 facts/ 官方证据落实修复，二次复核确认修复到位；另余约 37 处优先级属性标签（data-priority）不一致，仅属性不一、不影响技术内容正确性，建议顺手统一 |

**优先级标签残留汇总（共 37 处，仅属性不一致）**：chapter-04(2)、05(1)、06(3)、07(8 处)、08(2)、09(1)、12(6)、13(7)、14(5)、15(2)。如需将 `data-priority` 与前序报告 P0/P1/P2 对齐，可批量按 `review-findings.md` 的优先级列回填各卡 `data-priority` 属性。

**其余结构性残留提醒**：chapter-12 在 `</html>`（L4496）之后仍存在一段孤立「传统召回评估指标 / RAG Recall@K」代码片段（疑似从 C12.02 漂移），属 HTML 结构残留，建议在相应卡片归并或删除。

---

## 复核状态更新（2026-09-02）

> 复核报告（上文）相对**当前文件已过时**，落地结论如下，供后续参考。

1. **内容项均已修复（复核报告 stale）**：经逐项核对当前 `chapter-*.html`，原标记 ❌ 的 **C07.05** 当前 L588 已为"把字符串列转成数字（CAST(phone AS DECIMAL)）"、与 C07.13（L1837）一致；原 ⚠️ 的 **C07.01**（L87 已写 5.x 即有 / 5.5 引入）、**C06.01**（L179 与 L83 一致）、**C06.02**（L210 已为 `org.springframework.boot.aot.AotProcessor`）均已是正确表述。即本复核报告记录的"未修复/修复错误"在当前文件中不复存在。

2. **优先级标签部分系误读**：复核报告"37 处 `data-priority` 不一致"实际把**可见徽标**误当成了 `data-priority` 属性。实测当前 34 题的 `data-priority` 属性**已与审查报告一致**，仅其**可见徽标**错误（如 C07.01 属性 p1=报告 P1，但徽标显 P0）。故"属性不一致"不成立，真实问题是**徽标 bug**。

3. **重评级与关联处理（已执行）**：按用户决策"重新评级并关联处理"，以 `review-findings.md` 审查标注为权威：
   - **48 题** data-priority 与审查报告冲突 → 属性 + 徽标同步重评级至报告值；
   - **34 题**章节卡徽标 ≠ 自身 data-priority → 徽标修复为等于 data-priority；
   - E/S 卡经核验 0 徽标不一致，无需改动；
   - 总览页 `chapter-overview-priority.html` 据新 data-priority 重建。

4. **落地结果**：全站徽标 == data-priority **0 偏差**；总览 339 题、**0 排序违规**、**0 徽标/分组偏差**、**0 死链**、**0 data-page-node-id**；C+E+S 分布 **P0·90 / P1·189 / P2·60**（重评级前 105/161/73）。

5. **优先级权威口径（固化）**：`data-priority` 的权威值以 `review-findings.md` 审查标注为准；卡片徽标、总览页分组/统计须与 `data-priority` 三方一致（两处编码 + 总览）。
