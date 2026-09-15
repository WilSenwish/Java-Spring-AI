# facts/ 官方文档证据库

本目录存放 `fix-progress.md` 中「官方证据」表与「证据索引」所引用的**官方文档本地副本**，由 `/tmp` 落地后复制入库，便于随仓库持久化与追溯。

## 说明

- 文件名与 `fix-progress.md` 中的 `facts/<file>` 引用一一对应。
- 标记为 **SPA 壳 / 重定向壳 / 403 壳** 的文件：官网为单页应用或防爬，静态 HTML 落地后抽不到事实正文，**正文事实以 WebSearch 官方源核实为准**（见 `fix-progress.md` 证据索引的「核验方式」列）。
- WebSearch 官方源核实但**无本地文件**的项：K8s KEP-1287（C10.04）、Dubbo 3 Triple（C10.25）、OceanBase 列存副本（C14.08）。其结论已写入证据索引，未生成文件。
- `validate_site.py` 为全站交叉校验脚本（工具，非官方文档），一并复制以保持 `fix-progress.md` 中脚本引用有效。

## 文件索引

| 文件 | 官方来源 | 佐证范围 | 状态 |
|---|---|---|---|
| `openjdk-jeps.html` | openjdk.org/jeps | JDK 版本、preview/final 演进边界（贯穿 JDK 相关章） | 正常 |
| `jep444.html` / `jep491.html` | openjdk.org/jeps/444、/491 | 虚拟线程调度、pinning、JFR（C04、C13.12、C15.05） | 正常 |
| `jep505.html` / `jep506.html` | openjdk.org/jeps/505、/506 | 结构化并发、ScopedValue（C13.12、C15.05） | 正常 |
| `spring-boot-reference.html` | docs.spring.io/spring-boot/reference | Boot 自动配置/AOT/Session（C10.21） | 正常 |
| `spring-security-servlet-architecture.html` | docs.spring.io/spring-security/reference | Security 过滤器链（通用） | 正常 |
| `spring-ai-reference.html` | docs.spring.io/spring-ai/reference | ChatClient/Advisor/@Tool/MCP（C12.01/06/07/26/31、C14.02） | 正常 |
| `mysql-explain.html` | dev.mysql.com/doc/refman | `EXPLAIN` 执行计划字段（chapter-07） | 正常 |
| `redis-xpending.html` | redis.io/docs | Stream PEL/消费者组（chapter-08） | 正常 |
| `kafka-transactions.html` | kafka.apache.org/documentation | 事务/EOS（C11.11） | 正常 |
| `reactor-reference.html` | projectreactor.io/docs/core/release/reference | `publishOn`/`subscribeOn`/`elastic()`（C10.03、C12.16/25、C15.01/04/06） | 重定向壳（事实 WebSearch 核实） |
| `etcd-tuning.html` | etcd.io/docs | 心跳/选举默认值（chapter-09） | 正常 |
| `otel-spec.html` / `otel-collector.html` / `otel-java-agent.html` | opentelemetry.io/docs | OTLP/Collector/自动插桩（chapter-06/09） | 正常 |
| `seata-release.json` / `seata-raft.md` / `seata-readme.md` | seata.apache.org | 2.6.0 发布元数据、Raft 模式（chapter-09） | 正常 |
| `netty-docs.html` | netty.io/wiki | 主从 Reactor、exceptionCaught、SO_BACKLOG（C13.06/07） | 正常（含真实代码） |
| `mongodb-22.html` / `mongodb-32.html` | mongodb.com/docs（**2.2 / 3.2** 版本文档） | 分片 1.6 引入、2.2 生产成熟、WiredTiger 3.0 引入/3.2 默认（**C14.01 版本史证据**：专证「何时引入/成为默认」的版本史事实，旧版文档反而是精准证据） | SPA 壳（事实 WebSearch 核实） |
| `mongodb-40.html` / `mongodb-60.html` / `mongodb-80.html` | mongodb.com/docs（**v4.0 / v6.0 / v8.0** LTS 版本文档） | 4.0 多文档事务（副本集 4.0·分片集群 4.2·2PC）；6.0 可查询加密 Preview + CSFLE KMIP + 分片 128MB chunk；8.0 当前稳定主版本 + 范围可查询加密（**C14.01 现代特性证据**） | 正常（含关键词正文；结论 WebSearch 官方源核实） |
| `tidb-tiflash.html` | docs.pingcap.com | TiFlash GA 归 4.x（C14.05） | SPA 壳（事实 WebSearch 核实） |
| `clickhouse-delete.html` / `clickhouse-variant.html` | clickhouse.com/docs | Lightweight DELETE 22.8 / Variant 24.x（C14.06） | SPA 壳（事实 WebSearch 核实） |
| `qdrant-docs.html` | qdrant.tech/documentation | FloatVectors/SearchPoints（C14.04） | SPA 壳（事实 WebSearch 核实） |
| `milvus-docs.html` | milvus.io/docs | v2 SDK：AddFieldReq/IndexParam/FloatVec/SearchResp（C12.21、C14.03） | 403 壳（事实 WebSearch/GitHub 核实） |
| `scg-developer-guide.html` | docs.spring.io/spring-cloud-gateway | NettyRoutingFilter.getOrder()/转发（C10.02/20、C11.12） | 正常 |
| `validate_site.py` | 本地工具 | 全站交叉校验脚本（非官方文档） | 工具 |

## 仅 WebSearch 核实、无本地文件的项

| 主题 | 官方来源 | 佐证 |
|---|---|---|
| K8s In-place Pod Resize（KEP-1287） | kubernetes.io/blog | C10.04（1.27 Alpha→1.33 Beta→1.35 GA） |
| Dubbo 3 Triple | dubbo.apache.org | C10.25（3.x HTTP/2 跨语言） |
| OceanBase 列存副本 | oceanbase.com | C14.08（4.x 列存副本 + 向量化；OBKV 为 KV 接口） |
