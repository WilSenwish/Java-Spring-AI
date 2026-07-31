# 服务端开发安全 Checkpoint 手册

> **读者对象**：Java 高级开发工程师 / 架构师
> **文档版本**：v1.0
> **标准时效**：基于 OWASP Top 10:2025、NIST SP 800-131A Rev2、NIST FIPS 203/204/205、OWASP ASVS v5.0
> **最后更新**：2026-07-31

---

## 目录

- [第 0 章 文档导论](#第-0-章-文档导论)
- [第 1 章 认证与授权安全](#第-1-章-认证与授权安全)
- [第 2 章 会话管理](#第-2-章-会话管理)
- [第 3 章 输入输出安全](#第-3-章-输入输出安全)
- [第 4 章 密码学](#第-4-章-密码学)
- [第 5 章 错误处理与日志](#第-5-章-错误处理与日志)
- [第 6 章 API 安全](#第-6-章-api-安全)
- [附录 A：OWASP Top 10:2025 映射对照表](#附录-aowasp-top-102025-映射对照表)
- [附录 B：算法推荐与废弃速查表](#附录-b算法推荐与废弃速查表)
- [附录 C：Checkpoint 自检清单汇总](#附录-ccheckpoint-自检清单汇总)
- [附录 D：参考资料与权威链接](#附录-d参考资料与权威链接)

---

## 第 0 章 文档导论

### 0.1 文档目的与使用方式

本文档面向 Java 服务端开发与架构评审场景，提供系统性的安全自检参考。每节采用统一的三段式结构：**关键要点**阐述核心原则与选型依据，**Checkpoint** 列出代码评审与架构评审中需逐项确认的检查点，**雷区清单**以「禁止…」句式列出高风险反模式。第 4 章密码学为核心重点，额外补充基于 JCA（Java Cryptography Architecture）与 Bouncy Castle 的规范实现代码范例。

文档可作为代码评审 checklist、架构评审 checkpoint 与安全培训材料使用。附录 C 提供可勾选版自检清单，便于上线评审时直接使用。

### 0.2 标准依据与版本声明

| 标准来源 | 版本 | 关键变更 |
|---|---|---|
| OWASP Top 10 | 2025（2025-11 发布） | A03 升级为「软件供应链失败」；A10 新增「异常条件处理不当」 |
| OWASP ASVS | v5.0 | V11 密码学、V12 安全通信、V14 数据保护 |
| NIST SP 800-131A | Rev2 | SHA-1/RSA-1024/3DES/DES/RC4 已禁用或弃用 |
| NIST FIPS 203/204/205 | 2024 正式发布 | 后量子密码标准 ML-KEM/ML-DSA/SLH-DSA |
| NIST SP 800-63B | Rev3 | 数字身份指南，口令策略长度优先 |
| NIST SP 800-90A | Rev1 | 随机数生成器标准 |
| CWE | — | CWE-321/327/329/330/338/780/916 等 |

### 0.3 术语表

| 术语 | 含义 |
|---|---|
| CIA 三性 | 机密性（Confidentiality）、完整性（Integrity）、可用性（Availability） |
| AEAD | 认证加密，同时提供机密性与完整性（如 AES-GCM、ChaCha20-Poly1305） |
| 前向保密（PFS） | 会话密钥泄露不影响历史会话安全，依赖临时密钥交换（ECDHE） |
| KDF | 密钥派生函数，从口令或共享密钥派生密钥（如 PBKDF2、HKDF、Argon2） |
| CSPRNG | 密码学安全随机数生成器（如 Java `SecureRandom`） |
| HSM / KMS | 硬件安全模块 / 密钥管理服务，用于密钥的安全存储与运算 |
| MAC | 消息认证码，带密钥的完整性校验（如 HMAC） |
| salt | 口令哈希的随机盐，每用户唯一，非秘密 |
| pepper | 全局秘密盐，存于 HSM/配置，与数据库分离 |
| nonce / IV | 一次性随机数 / 初始化向量，加密中使用，不可重复 |
| JCA | Java Cryptography Architecture，JDK 内置密码学框架 |
| JCE | Java Cryptography Extension，JCA 的扩展部分 |
| PQC | 后量子密码，抵御量子计算机攻击的密码算法 |

### 0.4 安全设计总原则

**最小权限**：每个组件、用户、进程仅授予完成任务所需的最小权限。权限默认拒绝，显式授予。

**纵深防御**：安全不依赖单一防线。网络层、应用层、数据层各自独立防护，任一层被突破不导致全盘失守。业务层不可将安全责任完全外包给网关或框架。

**失败安全（Fail-Secure）**：异常或错误发生时，系统默认进入拒绝状态，而非放行。加密校验失败、签名验证异常时拒绝请求，而非降级为明文处理。

**零信任**：不因请求来自内网或已认证会话而隐式信任。每次资源访问均需验证身份与授权，服务间调用同样需要认证。

---

## 第 1 章 认证与授权安全

> 对应 OWASP Top 10:2025 A01（访问控制失效）、A07（身份认证失效）

### 1.1 身份认证基础与认证因素

认证（Authentication）解决「你是谁」的问题，授权（Authorization）解决「你能做什么」。两者不可混淆，认证通过不等于授权通过。

认证因素分为三类：知识因素（口令、PIN）、持有因素（令牌、设备）、固有因素（生物特征）。强认证要求至少两种不同类型的因素组合（MFA）。

认证失败的响应必须统一，避免通过错误消息差异或响应时间差异推断用户是否存在（用户枚举攻击）。

**Checkpoint**
- 登录失败提示是否统一为「用户名或密码错误」，不区分用户存在与否
- 是否有登录尝试限制与账户锁定/延时机制（指数退避）
- 认证端点是否强制 TLS 传输
- 认证失败的响应时间是否恒定（防时序枚举）

**雷区清单**
- 禁止通过不同错误消息或响应时间泄露用户是否存在
- 禁止允许无限次暴力尝试（需限流 + 指数退避 + 锁定）
- 禁止在 URL 参数中传递凭证
- 禁止「记住我」令牌长期有效且不可撤销

### 1.2 口令策略与口令存储

> 对应 OWASP A04（加密失败）、A07（身份认证失效）、CWE-916、CWE-759/760

口令存储必须使用「加盐 + 自适应慢哈希」。工作因子可随硬件升级定期提升，使 GPU/ASIC 爆破成本始终高于攻击收益。

算法推荐优先级（OWASP A04 明确建议）：

| 优先级 | 算法 | 说明 |
|---|---|---|
| 首选 | **Argon2id** | PHC 获奖算法，抗 GPU/ASIC，内存困难型 |
| 次选 | scrypt | 内存困难型，抗 ASIC |
| 可选 | bcrypt | 广泛使用，cost 可调 |
| 兼容 | PBKDF2-HMAC-SHA-512 | NIST 标准化，但抗 GPU 不如前三者 |

口令策略应遵循 NIST SP 800-63B：重视长度（建议 ≥12 位）而非强制复杂度规则（大小写+数字+特殊字符的强制组合已弃用）。维护已知泄露口令黑名单，注册/修改口令时比对拦截。

**Checkpoint**
- 是否使用 Argon2id / bcrypt / PBKDF2 而非 MD5 / SHA 直接哈希
- salt 是否每用户唯一且随机生成
- 工作因子是否定期评估并随硬件升级（bcrypt cost ≥10，PBKDF2 迭代 ≥600000）
- 是否支持口令泄露检查（HaveIBeenPwned 类比对）
- 口令最小长度是否 ≥8 位（高敏感系统 ≥12 位）

**雷区清单**
- 禁止用 MD5 / SHA-1 / SHA-256 直接哈希口令（即使加盐，速度过快，GPU 秒级爆破，CWE-916）
- 禁止明文存储或可逆加密存储口令
- 禁止全局共享 salt 或无 salt（彩虹表攻击，CWE-759/760）
- 禁止自创哈希算法或「MD5 加盐再 SHA-1」之类的叠加组合
- 禁止在日志、异常信息、监控指标中输出明文口令
- 禁止对口令强度仅做正则校验而无泄露库比对

### 1.3 多因素认证与无密码认证

TOTP（基于时间的一次性密码，如 Google Authenticator）优于短信验证码，因短信存在 SIM 劫持与拦截风险。高敏感场景不应将短信 OTP 作为唯一第二因素。

MFA 注册与重置流程本身的认证强度需与登录等同，否则成为绕过入口。攻击者可通过「忘记设备」流程关闭 MFA。

WebAuthn / Passkey 基于公钥密码学，原生抗钓鱼，是无密码认证的未来方向。服务端存储公钥，私钥永不离开设备。

**Checkpoint**
- MFA 重置流程是否要求同等强度认证
- TOTP 密钥是否加密存储
- 是否支持 WebAuthn / Passkey

**雷区清单**
- 禁止允许 MFA 绕过（如「忘记设备」直接关闭 MFA 无二次验证）
- 禁止短信 OTP 作为高敏感场景的唯一第二因素
- 禁止 MFA 状态可被未认证流程修改

### 1.4 授权模型与访问控制

> 对应 OWASP A01（访问控制失效）

授权遵循默认拒绝原则：权限显式授予，未明确允许即禁止。服务端必须强制执行授权校验，不可信任前端的隐藏菜单、按钮或路由守卫。

对象级授权（IDOR，Insecure Direct Object Reference）是高频漏洞：当资源通过自增 ID 或可猜测标识符暴露时，攻击者通过遍历 ID 访问他人数据。每个资源访问必须校验当前用户对该资源的归属权限。

横向越权指同级别用户间的越权访问，纵向越权指普通用户访问管理功能。两者均需在服务端拦截。

**Checkpoint**
- 每个接口是否都有授权注解或拦截器
- 资源 ID 访问是否校验当前用户归属
- 管理后台是否独立鉴权域
- 权限提升后是否重新校验

**雷区清单**
- 禁止仅靠前端隐藏功能实现授权
- 禁止用自增 ID 直接暴露资源且不做归属校验（IDOR）
- 禁止信任请求中的 role / isAdmin 等权限字段
- 禁止直接使用重定向参数导致权限跳转

### 1.5 OAuth2 / OIDC 协议安全

授权码模式（Authorization Code）配合 PKCE 是推荐流程，公开客户端（SPA、移动端）必须使用 PKCE 防止授权码拦截。

`state` 参数防止 CSRF 攻击，`nonce` 参数防止 OIDC 重放攻击。两者均需校验。

`redirect_uri` 必须严格白名单匹配，禁止通配或路径前缀匹配导致开放重定向。

**Checkpoint**
- 是否使用授权码 + PKCE 流程
- state / nonce 是否生成并校验
- redirect_uri 是否严格白名单匹配

**雷区清单**
- 禁止隐式流程（implicit）用于敏感应用
- 禁止忽略 state / nonce 校验
- 禁止 redirect_uri 通配或可被绕过
- 禁止 access_token 通过 URL fragment 传递

### 1.6 JWT 与令牌安全

JWT 的签名算法必须在服务端显式指定，禁止信任 JWT header 中的 `alg` 字段（防 `alg=none` 攻击与算法混淆攻击）。

access_token 应短生命周期（如 15-30 分钟），refresh_token 可较长但必须可撤销且绑定设备。JWT 本身无状态，撤销需配合黑名单或短时效设计。

JWT payload 仅做 Base64 编码，非加密，禁止存储敏感数据。

**Checkpoint**
- JWT 验签是否显式指定算法（如 `Algorithm.HMAC256(secret)`）
- access_token 生命周期是否 ≤30 分钟
- refresh_token 是否可撤销且绑定设备
- 是否校验 exp / nbf / iss / aud 声明

**雷区清单**
- 禁止接受 `alg=none` 的 JWT
- 禁止用对称密钥签名却用公钥验签（算法混淆攻击）
- 禁止在 JWT payload 存储敏感数据（仅 Base64，非加密）
- 禁止忽略 exp / nbf / iss / aud 校验
- 禁止 refresh_token 永不过期且不可吊销

---

## 第 2 章 会话管理

> 对应 OWASP A07（身份认证失效）

### 2.1 会话生命周期

会话需具备创建、续期、过期、销毁的完整闭环。登录成功后必须重新生成会话 ID（防会话固定攻击，CWE-384）。登出时服务端必须真正失效令牌，而非仅清除前端存储。

会话应设置绝对超时（如 8 小时）与空闲超时（如 30 分钟），超时后强制重新认证。

**Checkpoint**
- 登录成功是否轮换 sessionId
- 登出是否使服务端 token 失效
- 是否有绝对超时与空闲超时

**雷区清单**
- 禁止登录后复用旧 sessionId（会话固定，CWE-384）
- 禁止登出仅清前端 token 而服务端仍有效
- 禁止会话永不过期

### 2.2 会话令牌生成与传输

会话令牌必须使用 CSPRNG 生成，长度不低于 128 位熵。令牌通过 Cookie 传输时需同时设置 `HttpOnly`（防 XSS 读取）、`Secure`（仅 HTTPS 传输）、`SameSite`（防 CSRF）。

禁止在 URL 参数中传递会话令牌（Referer 头与日志会泄露）。

**Checkpoint**
- 令牌是否用 SecureRandom 生成且长度 ≥128 位
- Cookie 是否设置 HttpOnly + Secure + SameSite

**雷区清单**
- 禁止用 `Math.random()` / `java.util.Random` / 时间戳生成会话令牌（CWE-338）
- 禁止 Cookie 缺失 HttpOnly / Secure / SameSite 任一属性
- 禁止在 URL 参数中传递 session

### 2.3 会话固定、劫持与超时

检测 IP 或 User-Agent 的突变可辅助发现会话劫持。并发会话数应有限制。敏感操作（如修改密码、转账）前应要求重新认证（Step-up Authentication）。

权限提升后（如普通用户切换为管理员）必须轮换会话令牌。

**Checkpoint**
- 权限提升后是否轮换会话令牌
- 敏感操作前是否要求重新认证
- 是否限制并发会话数

**雷区清单**
- 禁止权限提升后不轮换会话
- 禁止长期不轮换长期令牌

### 2.4 CSRF 防护

SameSite Cookie 属性为首选防御，配合 anti-CSRF token 实现双重防御。状态变更请求必须使用 POST / PUT / DELETE 方法，并校验 Origin / Referer 头。

**Checkpoint**
- 状态变更请求是否使用非 GET 方法
- 是否校验 Origin / Referer 或 anti-CSRF token

**雷区清单**
- 禁止 GET 请求执行状态变更操作
- 禁止仅依赖 Referer 校验（可被缺失或伪造）

### 2.5 分布式会话与 Redis 会话安全

Redis 存储会话需设置 TTL，敏感会话数据应加密或仅存储会话 ID。Redis 实例需配置密码、网络隔离、禁用危险命令（如 `FLUSHALL`、`CONFIG`）。

**Checkpoint**
- Redis 是否配置 requirepass 与网络隔离
- 会话数据是否避免明文存储敏感信息
- 是否设置 TTL

**雷区清单**
- 禁止 Redis 无密码暴露公网
- 禁止会话数据明文存储敏感信息
- 禁止 Redis 无 TTL 导致会话堆积

---

## 第 3 章 输入输出安全

> 对应 OWASP A05（注入）、A03（供应链，含 XSS）

### 3.1 输入验证与数据净化原则

白名单验证优于黑名单。所有外部输入（表单、HTTP Header、Cookie、URL 参数、文件内容）均需在服务端校验，前端校验仅为用户体验，不可作为安全防线。

校验维度包括类型、长度、范围、字符集、业务格式。验证不通过的输入应拒绝，而非尝试净化后使用。

**Checkpoint**
- 是否对所有外部输入入口做服务端校验
- 是否使用参数化查询或预编译语句

**雷区清单**
- 禁止仅前端校验
- 禁止用黑名单过滤替代参数化查询
- 禁止信任 Content-Type 决定处理逻辑

### 3.2 注入防御

> 对应 OWASP A05、CWE-89（SQL 注入）、CWE-78（命令注入）

SQL 注入：使用参数化查询或 MyBatis `#{}` 占位符，禁止字符串拼接 SQL 或使用 `${}` 接收用户输入。

命令注入：避免 `Runtime.getRuntime().exec()` 拼接用户输入，必须执行时使用参数数组形式。

表达式注入：SpEL（Spring Expression Language）、OGNL、MVEL 等表达式引擎直接求值用户输入可导致 RCE，禁止将用户输入作为表达式求值。

NoSQL 注入：校验查询操作符，参数化查询。

**Checkpoint**
- SQL 查询是否全部使用 `#{}` 或 PreparedStatement
- 命令执行是否避免拼接用户输入
- SpEL / OGNL 是否禁用动态求值用户输入

**雷区清单**
- 禁止 MyBatis 用 `${}` 拼接用户输入（SQL 注入）
- 禁止 `Runtime.getRuntime().exec(用户输入拼接字符串)`（命令注入）
- 禁止 SpEL / OGNL 直接求值用户输入（RCE）
- 禁止 LDAP 查询拼接用户输入
- 禁止 XML 解析未禁用外部实体（XXE，CWE-611）

### 3.3 XSS 防御

输出编码需按上下文区分：HTML 上下文用 HTML 实体编码，JavaScript 上下文用 JS 编码，URL 上下文用 URL 编码，CSS 上下文用 CSS 编码。

Content-Security-Policy（CSP）作为深度防御，限制脚本来源。富文本场景使用白名单净化库（如 OWASP Java HTML Sanitizer），禁止黑名单过滤标签。

**Checkpoint**
- 输出是否按上下文做编码
- 是否设置 CSP 头
- 富文本是否使用白名单净化库

**雷区清单**
- 禁止直接拼接用户输入到 HTML 响应
- 禁止用 `innerHTML` 渲染未净化数据
- 禁止富文本场景用黑名单过滤标签

### 3.4 SSRF 防御

> 对应 OWASP Top 10:2025 A10（异常条件处理不当，SSRF 被吸收）

服务端发起请求前必须校验目标主机，禁止访问内网地址段（127.0.0.0/8、10.0.0.0/8、172.16.0.0/12、192.168.0.0/16、169.254.169.254 等）。

需禁用或校验重定向跟随，防止通过 302 跳转绕过地址校验。DNS 重绑定攻击需通过解析后校验 IP、再使用解析结果连接的方式防护。

**Checkpoint**
- 服务端发起请求前是否校验目标 IP
- 是否禁止内网地址段访问
- 重定向是否校验目标

**雷区清单**
- 禁止直接用用户输入作为 URL 发起请求
- 禁止未校验重定向链
- 禁止访问 127.0.0.1 / 10.0.0.0/8 / 169.254.169.254 等内网或元数据地址

### 3.5 文件上传与下载安全

文件校验应基于文件头魔数（magic bytes）而非扩展名。上传文件需重命名、存储于独立目录或域名下、禁止可执行权限。

下载需防止路径穿越（`../` 序列），Zip 解压需防 ZipSlip 攻击（解压路径逃逸）。

**Checkpoint**
- 是否校验文件头魔数
- 上传文件是否重命名并存储于独立目录
- 下载路径是否校验 `../` 穿越

**雷区清单**
- 禁止仅校验文件扩展名
- 禁止上传文件保存为可被服务端执行的路径
- 禁止用用户文件名直接拼接下载路径（路径穿越）
- 禁止 ZIP 解压未防 ZipSlip

### 3.6 反序列化安全

> 对应 OWASP A08（软件或数据完整性失效）、CWE-502

Java 原生序列化（`ObjectInputStream`）反序列化不可信数据可导致 RCE。优先使用 JSON 等安全格式。必须使用原生反序列化时，需通过 `ObjectInputFilter` 设置白名单类。

关注 Jackson、Fastjson、XStream 等组件的反序列化漏洞，及时升级。

**Checkpoint**
- 是否避免 Java 原生序列化用户数据
- 必须反序列化时是否使用 ObjectInputFilter 白名单
- 依赖组件是否存在已知反序列化漏洞

**雷区清单**
- 禁止 `ObjectInputStream` 直接反序列化不可信数据（RCE）
- 禁止 Fastjson 启用 autotype 且无白名单
- 禁止 XStream 反序列化不可信 XML
- 禁止依赖组件存在已知反序列化漏洞而不升级

### 3.7 输出编码与响应头安全

安全响应头是深度防御的重要组成：

| 响应头 | 作用 |
|---|---|
| Content-Security-Policy | 限制脚本与资源来源，防 XSS |
| X-Content-Type-Options: nosniff | 防止 MIME 类型嗅探 |
| X-Frame-Options / CSP frame-ancestors | 防点击劫持 |
| Referrer-Policy | 控制 Referer 泄露 |
| Strict-Transport-Security | 强制 HTTPS（HSTS） |

API 响应应遵循最小化原则，不返回多余字段，不暴露内部堆栈或调试信息。

**Checkpoint**
- 是否设置上述安全响应头
- API 响应是否最小化
- 错误响应是否泄露内部信息

**雷区清单**
- 禁止缺失 X-Content-Type-Options: nosniff
- 禁止 API 返回内部堆栈或调试信息
- 禁止响应包含未授权字段（过度暴露）

---

## 第 4 章 密码学

> 对应 OWASP Top 10:2025 A04（加密失败）、OWASP ASVS v5.0 V11/V12、NIST SP 800-131A Rev2
>
> 本章为核心重点章节。4.2-4.9 每节在概念说明后补充基于 JCA / Bouncy Castle 的 Java 规范实现代码范例，展示正确 API 用法与参数选择，错误用法以 `// 错误：` 注释对照。

### 4.1 密码学设计原则与威胁模型

密码学工程的第一原则是「不要自己实现密码学」（Don't roll your own crypto）。应用层应使用经审计的标准库（JCA、Bouncy Castle、Conscrypt），而非自实现算法或协议。

Kerckhoffs 原则要求安全性依赖密钥保密而非算法保密。任何依赖「算法不公开」来保障安全的设计（混淆）均不符合现代密码学要求。

密码学原语各司其职，不可混用：

| 安全属性 | 提供者 | 说明 |
|---|---|---|
| 机密性 | 加密（对称/非对称） | 防止数据被读取 |
| 完整性 | MAC / 哈希 / 签名 | 检测数据是否被篡改 |
| 真实性 | MAC / 签名 | 验证数据来源 |
| 不可否认性 | 数字签名 | 签名者无法否认（MAC 无法提供，因对称密钥双方共享） |

加密不提供完整性。裸加密（如 AES-CBC 无 MAC）是可篡改的——攻击者可翻转密文位导致明文对应位翻转。始终优先使用认证加密（AEAD，如 AES-GCM），同时提供机密性与完整性。

**Checkpoint**
- 是否使用标准库而非自实现密码学原语
- 是否做了数据分级，确定加密范围
- 密钥是否与代码、数据分离存储
- 加密是否配合完整性校验（AEAD 或 MAC）

**雷区清单**
- 禁止自实现加密算法、哈希函数或 PRNG
- 禁止认为「加密即可保护完整性」（加密不提供完整性，需 MAC 或 AEAD）
- 禁止用「算法保密」替代密钥保密（混淆非安全）
- 禁止用加密替代签名做身份认证（加密不提供不可否认性）

---

### 4.2 对称加密

对称加密使用同一密钥进行加密与解密，适用于大块数据的机密性保护。

**算法选型**：AES 是当前标准对称算法。AES-128 满足经典安全需求，AES-256 提供更高安全裕度（NIST SP 800-131A Rev2 推荐用于长期数据保护与抗量子场景）。DES、3DES、RC4、Blowfish 已被 NIST 禁用或弃用。

**模式选型**（关键决策）：

| 模式 | 是否 AEAD | 推荐度 | 说明 |
|---|---|---|---|
| GCM | 是 | 首选 | 同时提供机密性与完整性，性能好，硬件加速 |
| ChaCha20-Poly1305 | 是 | 推荐 | 纯软件实现性能优，无硬件加速依赖 |
| CTR + HMAC | 否（需手动 MAC） | 可用 | 需自行实现 Encrypt-then-MAC |
| CBC | 否 | 不推荐 | 无内置完整性，易受 Padding Oracle 攻击 |
| ECB | 否 | 禁用 | 相同明文产生相同密文，泄露数据模式 |

**IV / Nonce 要求**：GCM 模式的 nonce 在同一密钥下绝不可重复——重复会导致认证密钥泄露，进而可伪造密文并恢复明文。IV 必须每次随机生成且不可预测。

**Java 规范实现：AES-GCM 加解密**

```java
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import java.security.SecureRandom;
import java.util.Base64;

public class AesGcmExample {

    private static final int AES_KEY_SIZE = 256;   // AES-256
    private static final int GCM_IV_LENGTH = 12;    // 96-bit IV (GCM 推荐)
    private static final int GCM_TAG_LENGTH = 128;   // 认证标签位数

    /** 生成 AES 密钥 */
    public static SecretKey generateKey() throws Exception {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(AES_KEY_SIZE);
        return keyGen.generateKey();
    }

    /** AES-GCM 加密：返回 IV + 密文+Tag（拼接） */
    public static byte[] encrypt(SecretKey key, byte[] plaintext) throws Exception {
        // 每次加密生成随机 IV，不可复用
        byte[] iv = new byte[GCM_IV_LENGTH];
        new SecureRandom().nextBytes(iv);

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        cipher.init(Cipher.ENCRYPT_MODE, key, spec);
        byte[] ciphertext = cipher.doFinal(plaintext);

        // IV 与密文一同返回（IV 非秘密，但解密时需要）
        byte[] combined = new byte[iv.length + ciphertext.length];
        System.arraycopy(iv, 0, combined, 0, iv.length);
        System.arraycopy(ciphertext, 0, combined, iv.length, ciphertext.length);
        return combined;
    }

    /** AES-GCM 解密：校验认证标签，失败则抛 AEADBadTagException */
    public static byte[] decrypt(SecretKey key, byte[] combined) throws Exception {
        byte[] iv = new byte[GCM_IV_LENGTH];
        byte[] ciphertext = new byte[combined.length - GCM_IV_LENGTH];
        System.arraycopy(combined, 0, iv, 0, GCM_IV_LENGTH);
        System.arraycopy(combined, GCM_IV_LENGTH, ciphertext, 0, ciphertext.length);

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        cipher.init(Cipher.DECRYPT_MODE, key, spec);
        // 认证标签校验由 JCA 自动完成，校验失败抛异常
        return cipher.doFinal(ciphertext);
    }
}
```

关键要点：每次加密生成随机 IV（`SecureRandom`）；GCM 自动计算并校验认证标签；解密时标签校验失败抛 `AEADBadTagException`，调用方必须捕获并拒绝该数据。

**Checkpoint**
- 是否使用 GCM 或 ChaCha20-Poly1305 等 AEAD 模式
- IV / Nonce 是否每次随机生成且不重复
- 是否校验 GCM 认证标签（解密失败时拒绝）
- 密钥是否随机生成且足够长度（AES-256 用 32 字节）

**雷区清单**
- 禁止使用 ECB 模式（相同明文产生相同密文，泄露数据模式，CWE-327）
- 禁止 IV 固定、复用或全零（GCM 中 IV 复用导致密钥恢复，CWE-329/323）
- 禁止 CBC 模式不校验完整性（Padding Oracle 攻击）
- 禁止使用 DES / 3DES / RC4 / Blowfish 等弱算法（NIST 已禁用）
- 禁止裸加密不做认证（密文可被篡改）
- 禁止硬编码密钥（CWE-321）
- 禁止用口令直接做密钥（需 KDF 派生）

---

### 4.3 非对称加密与密钥协商

非对称加密使用公钥/私钥对，适用于密钥交换、数字签名与小数据加密。

**RSA**：加密使用 OAEP 填充（Optimal Asymmetric Encryption Padding），签名使用 PSS 填充。PKCS#1 v1.5 填充因易受 Bleichenbacher 攻击已不推荐（CWE-780）。RSA 密钥长度需 ≥2048 位（推荐 3072，CNSA 2.0 要求 3072），1024 位已被 NIST 禁用。

**椭圆曲线**：ECDSA 用于签名，ECDH 用于密钥协商。优先使用 NIST 标准曲线 P-256 / P-384。ECDSA 签名必须使用确定性 nonce（RFC 6979）或高质量随机数 k——k 值复用或可预测会导致私钥被推算泄露。

**密钥协商**：ECDHE（临时椭圆曲线 Diffie-Hellman）提供前向保密——即使长期私钥泄露，历史会话密钥仍然安全。RSA 密钥交换无前向保密，已在 TLS 1.3 中移除。

**Java 规范实现：RSA-OAEP 加密**

```java
import javax.crypto.Cipher;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PublicKey;
import java.security.spec.MGF1ParameterSpec;
import javax.crypto.spec.OAEPParameterSpec;
import javax.crypto.spec.PSource;

public class RsaOaepExample {

    private static final int RSA_KEY_SIZE = 2048;  // 最低 2048 位

    /** 生成 RSA 密钥对 */
    public static KeyPair generateKeyPair() throws Exception {
        KeyPairGenerator gen = KeyPairGenerator.getInstance("RSA");
        gen.initialize(RSA_KEY_SIZE);
        return gen.generateKeyPair();
    }

    /** RSA-OAEP 加密 */
    public static byte[] encrypt(PublicKey publicKey, byte[] plaintext) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
        // 显式指定 MGF1 的哈希算法与 OAEP 哈希一致
        OAEPParameterSpec oaepParams = new OAEPParameterSpec(
                "SHA-256",                        // OAEP 哈希
                "MGF1", MGF1ParameterSpec.SHA256,  // MGF1 掩码哈希
                PSource.PSpecified.DEFAULT);
        cipher.init(Cipher.ENCRYPT_MODE, publicKey, oaepParams);
        return cipher.doFinal(plaintext);
        // // 错误：Cipher.getInstance("RSA/ECB/PKCS1Padding") — 易受 Bleichenbacher 攻击
        // // 错误：gen.initialize(1024) — 密钥长度不足
    }
}
```

**Java 规范实现：RSA-PSS 签名与验签**

```java
import java.security.Signature;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.PSSParameterSpec;
import java.security.spec.MGF1ParameterSpec;

public class RsaPssExample {

    /** RSA-PSS 签名 */
    public static byte[] sign(PrivateKey privateKey, byte[] data) throws Exception {
        Signature signer = Signature.getInstance("RSASSA-PSS");
        PSSParameterSpec pssParams = new PSSParameterSpec(
                "SHA-256",                          // 消息摘要算法
                "MGF1", MGF1ParameterSpec.SHA256,    // 掩码生成函数
                32,                                   // 盐长度 = 哈希输出长度
                1);
        signer.setParameter(pssParams);
        signer.initSign(privateKey);
        signer.update(data);
        return signer.sign();
        // // 错误：Signature.getInstance("SHA256withRSA") — 使用 PKCS#1 v1.5 填充
    }

    /** RSA-PSS 验签 */
    public static boolean verify(PublicKey publicKey, byte[] data, byte[] signature) throws Exception {
        Signature verifier = Signature.getInstance("RSASSA-PSS");
        verifier.setParameter(new PSSParameterSpec(
                "SHA-256", "MGF1", MGF1ParameterSpec.SHA256, 32, 1));
        verifier.initVerify(publicKey);
        verifier.update(data);
        return verifier.verify(signature);
    }
}
```

**Java 规范实现：ECDSA 签名（确定性 nonce，需 Bouncy Castle）**

```java
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import java.security.PrivateKey;
import java.security.Signature;
import java.security.Security;

public class EcdsaExample {

    static {
        Security.addProvider(new BouncyCastleProvider());
    }

    /**
     * ECDSA 签名 — 使用确定性 nonce（RFC 6979）
     * Bouncy Castle 的 SHA256withECDSA 默认使用确定性 nonce
     */
    public static byte[] sign(PrivateKey privateKey, byte[] data) throws Exception {
        Signature signer = Signature.getInstance("SHA256withECDSA", "BC");
        signer.initSign(privateKey);
        signer.update(data);
        return signer.sign();
        // // 错误：使用 JDK 默认 provider 的 ECDSA，若随机数 k 可预测则私钥泄露
    }
}
```

**Checkpoint**
- RSA 加密是否使用 OAEP 填充
- RSA 签名是否使用 PSS 填充
- RSA 密钥长度是否 ≥2048 位
- ECDH 是否使用 ECDHE（临时密钥，前向保密）
- ECDSA 是否使用确定性签名或安全随机 k

**雷区清单**
- 禁止 RSA 使用 PKCS#1 v1.5 填充（Bleichenbacher 攻击，CWE-780）
- 禁止 RSA 密钥 <2048 位（NIST 已禁用 1024 位）
- 禁止 ECDSA 复用随机 k 或使用弱随机源（导致私钥泄露）
- 禁止使用 DSA 算法（已弃用）
- 禁止自选非标准椭圆曲线
- 禁止 RSA 直接加密大块数据（应混合加密：RSA 加密对称密钥，对称加密加密数据）

---

### 4.4 哈希函数

哈希函数将任意长度输入映射为固定长度输出，提供完整性校验与数字指纹。

**算法选型**：

| 算法 | 推荐度 | 说明 |
|---|---|---|
| SHA-256 / SHA-384 / SHA-512 | 推荐 | SHA-2 家族，当前通用标准 |
| SHA-3-256 / SHA-3-512 | 推荐 | Keccak 结构，与 SHA-2 互补 |
| BLAKE2 / BLAKE3 | 可用 | 高性能替代，适合非 NIST 合规场景 |
| SHA-1 | 禁用 | 已被破解，数字签名 2014 年起禁用 |
| MD5 | 禁用 | 碰撞已实战利用 |

哈希函数用途包括：完整性校验、数据指纹、HMAC 构造、KDF 派生。通用哈希函数（SHA-256）速度快，不适合口令存储（需慢哈希，见 4.6）。

**Java 规范实现：SHA-256 / SHA-3 哈希**

```java
import java.security.MessageDigest;

public class HashExample {

    /** SHA-256 哈希 */
    public static byte[] sha256(byte[] data) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        return md.digest(data);
        // // 错误：MessageDigest.getInstance("MD5") — 已被破解
        // // 错误：MessageDigest.getInstance("SHA-1") — 已被破解
    }

    /** SHA-3-256 哈希（JDK 9+ 支持） */
    public static byte[] sha3_256(byte[] data) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA3-256");
        return md.digest(data);
    }
}
```

关键要点：`MessageDigest` 是线程不安全的，每次调用应新建实例或使用线程局部变量。

**Checkpoint**
- 是否使用 SHA-2 / SHA-3 而非 MD5 / SHA-1
- 哈希用途是否匹配算法特性（通用哈希不用于口令存储）

**雷区清单**
- 禁止使用 MD5（碰撞已实战利用，CWE-327）
- 禁止使用 SHA-1 用于安全用途（已被破解）
- 禁止用通用快哈希（SHA-256）存储口令（需慢哈希 KDF）
- 禁止用非密码学哈希（如 `String.hashCode()`、CRC32）做安全校验
- 禁止依赖无密钥哈希做完整性校验（需带密钥 MAC，否则任何人可替换哈希）

---

### 4.5 消息认证码与数字签名

**HMAC**（Hash-based Message Authentication Code）使用密钥与哈希函数构造 MAC，提供带密钥的完整性校验与真实性验证。推荐 HMAC-SHA-256 / HMAC-SHA-512。

MAC 与签名的关键区别：MAC 使用对称密钥，双方共享，无法提供不可否认性；数字签名使用非对称密钥，私钥签名、公钥验签，提供不可否认性。

**MAC 与加密的组合顺序**：

| 顺序 | 安全性 | 说明 |
|---|---|---|
| Encrypt-then-MAC | 安全 | 先加密再对密文做 MAC，推荐 |
| MAC-then-Encrypt | 不安全 | Padding Oracle 攻击风险 |
| Encrypt-and-MAC | 不安全 | 明文可能从 MAC 泄露 |

使用 AEAD（如 GCM）时无需手动组合，AEAD 内部已正确处理。

**常量时间比较**：比较 MAC 或哈希时必须使用常量时间比较，防止通过响应时间差异推断正确字节数（时序攻击）。Java 中使用 `MessageDigest.isEqual()`。

**Java 规范实现：HMAC-SHA-256 与常量时间比较**

```java
import javax.crypto.Mac;
import javax.crypto.SecretKey;
import java.security.MessageDigest;

public class HmacExample {

    /** 计算 HMAC-SHA-256 */
    public static byte[] hmacSha256(SecretKey key, byte[] data) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(key);
        return mac.doFinal(data);
    }

    /** 常量时间比较 MAC（防时序攻击） */
    public static boolean verifyMac(byte[] expected, byte[] actual) {
        return MessageDigest.isEqual(expected, actual);
        // // 错误：Arrays.equals(expected, actual) — 非常量时间，存在时序攻击风险
        // // 错误：expected.equals(actual) — 非常量时间
    }
}
```

关键要点：`MessageDigest.isEqual()` 在所有 JDK 版本中均为常量时间实现；`Arrays.equals()` 在发现第一个不匹配字节时即返回，泄露前缀信息。

**Checkpoint**
- 是否使用 HMAC 校验数据完整性
- 比较 MAC / 哈希是否使用常量时间比较（`MessageDigest.isEqual`）
- 签名是否使用 PSS / ECDSA 而非 PKCS#1 v1.5
- 加密 + MAC 是否采用 Encrypt-then-MAC 顺序

**雷区清单**
- 禁止用 `==` 或 `Arrays.equals()` 比较 MAC / 哈希 / 签名（时序攻击）
- 禁止 MAC-then-Encrypt 组合（Padding Oracle 风险）
- 禁止用无密钥哈希替代 MAC（任何人可伪造）
- 禁止用 MAC 替代签名做不可否认性场景（对称密钥无法提供）

### 4.6 口令哈希与密钥派生函数

口令哈希与密钥派生是密码学应用中最易出错的领域。通用哈希函数（SHA-256）速度快，不适合口令存储——GPU 每秒可计算数十亿次 SHA-256，使口令爆破成本极低。必须使用自适应慢哈希函数（KDF），通过内存与计算开销使暴力破解不可行。

**口令存储算法选型**（OWASP A04 推荐优先级）：

| 优先级 | 算法 | 内存困难 | 说明 |
|---|---|---|---|
| 首选 | Argon2id | 是 | PHC 获奖算法，抗 GPU/ASIC，参数可调（内存、迭代、并行度） |
| 次选 | scrypt | 是 | 内存困难型，抗 ASIC |
| 可选 | bcrypt | 否 | 广泛使用，cost 可调，但仅 CPU 困难 |
| 兼容 | PBKDF2-HMAC-SHA-512 | 否 | NIST 标准化，迭代次数需 ≥600000 |

**salt**：每用户唯一的随机盐，16 字节以上。salt 非秘密，可与哈希结果一同存储。salt 使相同口令产生不同哈希，使彩虹表预计算不可行。

**pepper**：全局秘密盐，与数据库分离存储（HSM / 环境变量 / 配置中心）。pepper 是秘密，泄露后失去保护意义。pepper 使即使数据库泄露，攻击者仍需知道 pepper 才能爆破。

**工作因子**：应随硬件升级定期提升。bcrypt 的 cost 参数每增加 1，计算时间翻倍。PBKDF2 的迭代次数需根据 OWASP 2025 建议：PBKDF2-HMAC-SHA-256 ≥600000，PBKDF2-HMAC-SHA-512 ≥210000。

**Java 规范实现：Argon2id 口令哈希（需 Bouncy Castle）**

```java
import org.bouncycastle.crypto.generators.Argon2BytesGenerator;
import org.bouncycastle.crypto.params.Argon2Parameters;
import java.security.MessageDigest;
import java.security.SecureRandom;

public class Argon2idExample {

    private static final int ITERATIONS = 3;       // 迭代次数
    private static final int MEMORY_KB = 65536;    // 64 MB 内存
    private static final int PARALLELISM = 4;      // 并行度
    private static final int HASH_LENGTH = 32;     // 输出长度 32 字节
    private static final int SALT_LENGTH = 16;      // salt 长度

    /** 生成 salt */
    public static byte[] generateSalt() {
        byte[] salt = new byte[SALT_LENGTH];
        new SecureRandom().nextBytes(salt);
        return salt;
    }

    /** Argon2id 哈希 */
    public static byte[] hash(String password, byte[] salt) {
        Argon2Parameters params = new Argon2Parameters.Builder(
                Argon2Parameters.ARGON2_id)
                .withVersion(Argon2Parameters.ARGON2_VERSION_13)
                .withIterations(ITERATIONS)
                .withMemoryAsKB(MEMORY_KB)
                .withParallelism(PARALLELISM)
                .withSalt(salt)
                .build();

        Argon2BytesGenerator generator = new Argon2BytesGenerator();
        generator.init(params);
        byte[] hash = new byte[HASH_LENGTH];
        generator.generateBytes(password.toCharArray(), hash);
        return hash;
    }

    /** 验证口令：常量时间比较 */
    public static boolean verify(String password, byte[] salt, byte[] expectedHash) {
        byte[] actualHash = hash(password, salt);
        return MessageDigest.isEqual(expectedHash, actualHash);
    }
}
```

**Java 规范实现：PBKDF2-HMAC-SHA-512 密钥派生**

```java
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import java.security.SecureRandom;

public class Pbkdf2Example {

    private static final int ITERATIONS = 210000;  // OWASP 2025 建议值
    private static final int KEY_LENGTH = 512;      // 512 位 = 64 字节

    /** PBKDF2-HMAC-SHA-512 派生密钥 */
    public static byte[] deriveKey(char[] password, byte[] salt) throws Exception {
        PBEKeySpec spec = new PBEKeySpec(password, salt, ITERATIONS, KEY_LENGTH);
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA512");
        byte[] key = factory.generateSecret(spec).getEncoded();
        spec.clearPassword();  // 清除内存中的口令
        return key;
        // // 错误：iterations = 1000 — 迭代次数过低，GPU 秒级爆破
        // // 错误：使用 PBKDF2WithHmacSHA1 — SHA-1 已弃用
    }
}
```

**Java 规范实现：HKDF 密钥派生（用于已共享密钥场景）**

```java
import org.bouncycastle.crypto.digests.SHA256Digest;
import org.bouncycastle.crypto.generators.HKDFBytesGenerator;
import org.bouncycastle.crypto.params.HKDFParameters;

public class HkdfExample {

    /**
     * HKDF-SHA-256 派生密钥
     * 用于从已有共享密钥（如 ECDH 协商结果）派生会话密钥
     * 不适用于口令派生（口令需用 PBKDF2/Argon2）
     */
    public static byte[] deriveKey(byte[] ikm, byte[] salt, byte[] info, int length) {
        HKDFBytesGenerator generator = new HKDFBytesGenerator(new SHA256Digest());
        generator.init(HKDFParameters.skipExtractParameters(ikm, salt, info));
        byte[] key = new byte[length];
        generator.generateBytes(key, 0, length);
        return key;
    }
}
```

**Checkpoint**
- 是否使用 Argon2id / bcrypt / PBKDF2 而非 MD5 / SHA 直接哈希
- 工作因子是否达标（bcrypt cost ≥10，PBKDF2-SHA-512 ≥210000）且定期评估
- salt 是否每用户唯一随机生成
- 口令转密钥是否使用 KDF（PBKDF2 / Argon2）而非直接哈希
- pepper 是否与数据库分离存储

**雷区清单**
- 禁止用 MD5 / SHA-1 / SHA-256 直接哈希口令（即使加盐，GPU 秒级爆破，CWE-916）
- 禁止无 salt 或全局共享 salt（彩虹表攻击，CWE-759/760）
- 禁止工作因子过低（bcrypt cost<10，PBKDF2 迭代<210000）
- 禁止口令直接做 AES 密钥（需 PBKDF2 / Argon2 派生）
- 禁止自创 KDF
- 禁止 pepper 存于数据库同库（失去分离保护意义）

---

### 4.7 随机数与熵源

密码学场景的随机数必须使用 CSPRNG（密码学安全随机数生成器）。Java 中对应 `java.security.SecureRandom`。

`SecureRandom` 默认自动播种，从操作系统熵源获取种子（`/dev/urandom`），无需手动调用 `setSeed`。手动调用 `setSeed` 可能降低熵——若传入可预测值（如时间戳），则输出可预测。

**不同场景的随机数需求**：

| 场景 | 最小长度 | 说明 |
|---|---|---|
| 会话令牌 | 128 位（16 字节） | 防暴力枚举 |
| 对称密钥 | 与算法匹配（AES-256 = 32 字节） | KeyGenerator 生成 |
| IV / Nonce | GCM: 96 位（12 字节） | 每次唯一随机 |
| salt | 128 位（16 字节） | 每用户唯一 |
| JWT ID | 128 位 | 防碰撞 |

`java.util.Random` 与 `Math.random()` 使用线性同余生成器，仅统计随机，输出可预测，禁止用于安全场景。`UUID.randomUUID()` 内部使用 `SecureRandom`，可用于生成标识符，但不应作为会话令牌（UUID v4 格式固定，熵利用不充分）。

**Java 规范实现：SecureRandom 生成各类安全随机值**

```java
import java.security.SecureRandom;
import java.util.Base64;

public class SecureRandomExample {

    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    /** 生成会话令牌（Base64 编码） */
    public static String generateToken() {
        byte[] bytes = new byte[32];  // 256 位
        SECURE_RANDOM.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }

    /** 生成 salt */
    public static byte[] generateSalt(int length) {
        byte[] salt = new byte[length];
        SECURE_RANDOM.nextBytes(salt);
        return salt;
    }

    /** 生成 GCM IV（12 字节） */
    public static byte[] generateGcmIv() {
        byte[] iv = new byte[12];
        SECURE_RANDOM.nextBytes(iv);
        return iv;
        // // 错误：iv = new byte[12]; Arrays.fill(iv, (byte)0) — 固定全零 IV
        // // 错误：new Random().nextBytes(iv) — 非密码学随机
    }
}
```

关键要点：`SecureRandom` 实例可复用（线程安全）；获取实例时优先使用 `new SecureRandom()` 或 `SecureRandom.getInstanceStrong()`（后者在 Linux 上可能阻塞等待熵，不推荐用于高频场景）。

**Checkpoint**
- 安全令牌、密钥、IV、salt 是否使用 SecureRandom
- 是否避免手动 setSeed 固定值

**雷区清单**
- 禁止用 `java.util.Random` / `Math.random()` 生成安全令牌（CWE-338）
- 禁止用时间戳 / 进程 ID 作为随机种子（可预测，CWE-335/337）
- 禁止手动 `setSeed` 固定值（如 `new SecureRandom(固定字节)`，CWE-336）
- 禁止复用 nonce / IV（CWE-323）

---

### 4.8 密钥管理

密钥管理覆盖密钥的完整生命周期：生成、存储、分发、使用、轮换、撤销、销毁。密钥泄露使所有基于该密钥的密码学保护失效。

**密钥生成**：使用 CSPRNG（`KeyGenerator` / `SecureRandom`），密钥长度与算法匹配。

**密钥存储**：最敏感的密钥应存储于 HSM（硬件安全模块）或 KMS（密钥管理服务），应用不持有明文密钥。次敏感密钥可存储于 `KeyStore`（JKS / PKCS12），配合口令保护。禁止密钥硬编码于源码或存于配置文件明文（CWE-321/260）。

**密钥分离**：不同用途使用不同密钥——加密密钥、签名密钥、MAC 密钥分开，不可一钥多用。一钥多用时某用途泄露波及其他用途。

**密钥轮换**：定期轮换密钥，泄露后可撤销旧密钥。加密数据需支持密钥版本，解密时按版本选择密钥。

**密钥销毁**：内存中的密钥使用后应及时清零。Java 中 `byte[]` 可通过 `Arrays.fill(key, (byte)0)` 清零；`String` 不可变，无法清零，因此密钥不应以 `String` 存储。

**Java 规范实现：密钥存储于 KeyStore**

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.security.KeyStore;
import java.security.KeyStore.SecretKeyEntry;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class KeyStoreExample {

    /** 将密钥存入 KeyStore */
    public static void storeKey(SecretKey key, String alias, String keystorePass)
            throws Exception {
        KeyStore ks = KeyStore.getInstance("PKCS12");
        ks.load(null, null);  // 新建空 KeyStore

        SecretKeyEntry entry = new SecretKeyEntry(key);
        ks.setEntry(alias, entry,
                new KeyStore.PasswordProtection(keystorePass.toCharArray()));

        try (FileOutputStream fos = new FileOutputStream("keys.p12")) {
            ks.store(fos, keystorePass.toCharArray());
        }
    }

    /** 从 KeyStore 读取密钥 */
    public static SecretKey loadKey(String alias, String keystorePass)
            throws Exception {
        KeyStore ks = KeyStore.getInstance("PKCS12");
        try (FileInputStream fis = new FileInputStream("keys.p12")) {
            ks.load(fis, keystorePass.toCharArray());
        }
        SecretKeyEntry entry = (SecretKeyEntry) ks.getEntry(alias,
                new KeyStore.PasswordProtection(keystorePass.toCharArray()));
        return entry.getSecretKey();
    }
}
```

**Java 规范实现：内存密钥安全清零**

```java
import java.util.Arrays;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class KeyCleanupExample {

    public void processWithKey(byte[] keyBytes) {
        try {
            SecretKey key = new SecretKeySpec(keyBytes, "AES");
            // ... 使用密钥加解密 ...
        } finally {
            // 使用后立即清零，防止内存中被读取
            Arrays.fill(keyBytes, (byte) 0);
        }
        // // 错误：String keyStr = new String(keyBytes) — String 不可变，无法清零
    }
}
```

**Checkpoint**
- 密钥是否存储于 HSM / KMS / KeyStore 而非配置文件或源码
- 是否有密钥轮换策略
- 是否不同用途使用独立密钥
- 内存中密钥使用后是否及时清零（`byte[]` + `Arrays.fill`）
- 密钥是否以 `byte[]` 而非 `String` 存储

**雷区清单**
- 禁止硬编码密钥于源码（CWE-321，Git 历史永久泄露）
- 禁止密钥存于配置文件明文（CWE-260）
- 禁止密钥写入日志、异常信息、监控指标
- 禁止一钥多用（加密 + 签名混用）
- 禁止密钥永不轮换
- 禁止用 `String` 存储密钥（不可变，无法清零，应使用 `byte[]`）
- 禁止使用默认密钥或示例密钥上线（CWE-321）

---

### 4.9 证书与 TLS

TLS（Transport Layer Security）保障传输层机密性与完整性。TLS 1.3 是当前推荐版本，相比 1.2 移除了不安全算法（RSA 密钥交换、CBC、RC4、SHA-1），握手更快更安全。TLS 1.2 仍可用但需正确配置密码套件。

**TLS 版本与密码套件**：

| 项目 | 推荐 | 禁用 |
|---|---|---|
| TLS 版本 | TLS 1.3（首选）、TLS 1.2 | SSLv3、TLS 1.0、TLS 1.1 |
| 密钥交换 | ECDHE（前向保密） | RSA 密钥交换（无 PFS） |
| 对称加密 | AES-GCM、ChaCha20-Poly1305 | CBC、RC4、3DES |
| 证书签名 | RSA-PSS、ECDSA | RSA-PKCS#1v1.5、MD5、SHA-1 |

**证书校验**：客户端必须严格校验证书链、主机名、有效期、吊销状态（OCSP / CRL）。禁止信任所有证书（`TrustManager` 返回 true、`-DtrustAll` 参数），否则 TLS 降级为明文等效（CWE-295）。

**HSTS**：通过 `Strict-Transport-Security` 响应头强制浏览器使用 HTTPS，防止 SSL Strip 降级攻击。含 `preload` 指令可加入浏览器 HSTS 预加载列表。

**PQC 迁移**：NIST FIPS 203（ML-KEM）、FIPS 204（ML-DSA）、FIPS 205（SLH-DSA）已于 2024 年正式发布。高风险系统需在 2030 年前完成迁移。当前阶段可采用混合模式（经典算法 + PQC），如 X25519MLKEM768 密码套件。

**Java 规范实现：TLS 客户端正确证书校验**

```java
import javax.net.ssl.SSLContext;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.TrustManagerFactory;
import java.net.URL;
import java.security.KeyStore;

public class TlsClientExample {

    /**
     * 正确的 TLS 连接：使用 JVM 默认 TrustManager 校验证书
     */
    public static void connect(String urlStr) throws Exception {
        // 使用 JVM 默认信任库（cacerts），严格校验证书链与主机名
        TrustManagerFactory tmf = TrustManagerFactory.getInstance(
                TrustManagerFactory.getDefaultAlgorithm());
        tmf.init((KeyStore) null);  // null 表示使用默认 cacerts

        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(null, tmf.getTrustManagers(), null);

        URL url = new URL(urlStr);
        HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
        conn.setSSLSocketFactory(sslContext.getSocketFactory());
        // 主机名校验默认开启，不要禁用
        // conn.setHostnameVerifier((h, s) -> true) — 错误：禁用主机名校验
        conn.connect();

        // // 错误写法：信任所有证书
        // TrustManager[] trustAll = new TrustManager[]{
        //     new X509TrustManager() {
        //         public void checkClientTrusted(...) {}
        //         public void checkServerTrusted(...) {}  // 不校验，直接通过
        //         public X509Certificate[] getAcceptedIssuers() { return null; }
        //     }
        // };
        // sslContext.init(null, trustAll, null);  // CWE-295：MITM 风险
    }
}
```

**Checkpoint**
- 是否仅启用 TLS ≥1.2 且优先 1.3
- 密码套件是否使用 ECDHE + GCM（前向保密 + AEAD）
- 是否启用 HSTS
- 客户端是否严格校验证书（非 trustAll）
- 是否规划 PQC 迁移路线

**雷区清单**
- 禁止使用 TLS 1.0 / 1.1 / SSLv3（协议漏洞）
- 禁止禁用证书校验（`TrustManager` 全信任，CWE-295）
- 禁止忽略主机名校验（`setHostnameVerifier` 返回 true）
- 禁止使用 RSA 密钥交换（无前向保密）
- 禁止使用 CBC 套件（Lucky13 等攻击）
- 禁止使用 RC4 / 3DES 套件
- 禁止自签证书用于生产且无信任锚管理
- 禁止使用 STARTTLS 协议（降级攻击风险）
- 禁止证书过期不监控

---

### 4.10 密码算法雷区总清单

以下为本章核心汇总。每行为一条禁用项，标注风险与推荐替代方案及标准依据，可作为代码评审速查表使用。

| 类别 | 禁用 / 不推荐项 | 风险 | 推荐替代 | 依据 |
|---|---|---|---|---|
| 对称算法 | DES / 3DES / RC4 / Blowfish | 弱密钥、已破解 | AES-128 / AES-256 | NIST SP 800-131A |
| 对称模式 | ECB | 相同明文→相同密文，泄露模式 | GCM / CTR | CWE-327 |
| 对称模式 | CBC（无认证） | Padding Oracle | GCM（AEAD） | OWASP A04 |
| IV / Nonce | 固定 / 复用 / 全零 | 密钥恢复、信息泄露 | 每次随机且唯一 | CWE-329/323 |
| 裸加密 | 无 MAC 的加密 | 密文可篡改 | AEAD（GCM）或 Encrypt-then-MAC | OWASP A04 |
| 哈希 | MD5 | 碰撞已实战利用 | SHA-256+ | NIST |
| 哈希 | SHA-1 | 已被破解 | SHA-256 / SHA-3 | NIST SP 800-131A |
| 口令哈希 | MD5 / SHA 直接哈希 | GPU 秒级爆破 | Argon2id / bcrypt / PBKDF2 | OWASP A04, CWE-916 |
| 口令哈希 | 无 salt / 共享 salt | 彩虹表攻击 | 每用户随机 salt | CWE-759/760 |
| 口令哈希 | 工作因子过低 | 爆破成本过低 | bcrypt cost≥10, PBKDF2≥210000 | OWASP A04 |
| 非对称 | RSA <2048 位 | 已可破解 | RSA≥2048（推荐 3072） | NIST, CNSA 2.0 |
| 非对称填充 | RSA PKCS#1 v1.5 | Bleichenbacher 攻击 | RSA-OAEP / PSS | CWE-780 |
| 非对称 | DSA | 已弃用 | ECDSA / EdDSA | NIST |
| 签名 | ECDSA 随机 k 复用 / 弱随机 | 私钥泄露 | 确定性签名 RFC 6979 | — |
| 随机数 | java.util.Random / Math.random() | 可预测 | SecureRandom | CWE-338 |
| 随机数 | 固定种子 / 时间戳种子 | 可预测 | 不手动 setSeed | CWE-336/335 |
| MAC 比较 | `==` / `Arrays.equals()` | 时序攻击 | `MessageDigest.isEqual()` | — |
| MAC 组合 | MAC-then-Encrypt | Padding Oracle | Encrypt-then-MAC 或 AEAD | — |
| 密钥存储 | 硬编码 / 配置明文 / 默认密钥 | 永久泄露 | HSM / KMS / KeyStore | CWE-321/260 |
| 密钥类型 | String 存储密钥 | 无法清零 | byte[] + Arrays.fill | — |
| 密钥使用 | 一钥多用 | 跨用途泄露 | 密钥分离，各用途独立 | — |
| TLS 版本 | 1.0 / 1.1 / SSLv3 | 协议漏洞 | ≥1.2（优选 1.3） | NIST |
| TLS 套件 | RSA 交换 / CBC / RC4 | 无 PFS / 漏洞 | ECDHE + GCM | OWASP A04 |
| 证书校验 | trustAll / 忽略校验 | MITM | 严格校验链 + 主机名 + 有效期 | CWE-295 |
| TLS 协议 | STARTTLS | 降级攻击 | 隐式 TLS | — |

---

## 第 5 章 错误处理与日志

> 对应 OWASP Top 10:2025 A09（安全日志与告警失效）、A10（异常条件处理不当）

### 5.1 安全错误处理与异常管理

OWASP Top 10:2025 新增 A10「异常条件处理不当」，将异常路径列为高危区域。许多安全漏洞发生在异常处理代码中——开发者在正常路径中谨慎处理安全，却在异常路径中放松了校验。

失败安全原则要求：异常或错误发生时，系统默认进入拒绝状态。加密校验失败、签名验证异常、解密标签不匹配时，必须拒绝请求或中止操作，而非降级为明文或跳过校验。

统一异常处理应避免将内部堆栈、SQL 语句、文件路径等技术信息暴露给客户端。生产环境返回通用错误信息，详细信息记录于服务端日志。

异常捕获不应吞掉异常（empty catch），也不应捕获过宽（`catch (Exception e)` 或 `catch (Throwable t)`）掩盖真实问题。异常不应作为业务流程控制手段。

**Checkpoint**
- 异常发生时是否默认拒绝（fail-secure）
- 是否有全局异常处理器统一封装错误响应
- 错误响应是否泄露堆栈、SQL、文件路径等内部信息
- 是否避免 empty catch 吞异常

**雷区清单**
- 禁止异常时默认放行（fail-open）
- 禁止返回堆栈跟踪、SQL 语句、文件路径给客户端
- 禁止 empty catch 吞异常（CWE-390）
- 禁止用异常做业务流程控制
- 禁止捕获过宽（catch Exception / Throwable）掩盖问题

### 5.2 安全日志实践

日志需记录安全事件以支持审计与取证：登录成功/失败、权限变更、关键业务操作、异常拦截。每条安全日志应包含 who（主体）、what（操作）、when（时间）、result（结果）。

日志中禁止记录敏感数据：口令、密钥、令牌、完整卡号、身份证号、完整手机号。需要对敏感字段做脱敏处理（如卡号仅保留后四位）。

日志应防篡改——独立存储于攻击者无法修改的系统，或使用 WORM（Write Once Read Many）存储。仅记录成功操作而忽略失败操作的日志会丢失攻击痕迹。

**Checkpoint**
- 安全事件是否记录 who / what / when / result
- 日志是否对敏感字段脱敏
- 日志是否防篡改（独立存储 / WORM）
- 是否同时记录失败操作（攻击痕迹在失败中）

**雷区清单**
- 禁止日志记录口令、密钥、令牌、完整卡号、身份证号
- 禁止日志记录完整请求体含敏感字段
- 禁止日志可被普通用户篡改
- 禁止只记成功不记失败

### 5.3 敏感信息泄露防护

信息泄露不仅发生在 HTTP 响应中，还存在于日志、异常信息、监控指标、调试端点。全链路均需脱敏。

生产环境必须关闭或鉴权保护调试端点：Spring Boot Actuator、Swagger / OpenAPI 文档、Druid 监控页面。错误页面不应暴露框架版本、服务器路径、组件信息。

**Checkpoint**
- 生产环境 Actuator 端点是否鉴权或关闭
- Swagger / 接口文档是否在生产关闭
- 错误页面是否暴露框架版本或路径
- HTML 注释或隐藏域是否包含敏感信息

**雷区清单**
- 禁止生产环境 Actuator 无鉴权暴露
- 禁止 Swagger / 接口文档在生产环境暴露
- 禁止错误页暴露框架版本、服务器路径
- 禁止在 HTML 注释或隐藏域中存储敏感信息

---

## 第 6 章 API 安全

> 对应 OWASP API Security Top 10、OWASP Top 10:2025 A03（供应链）

### 6.1 API 认证与授权

API 鉴权应独立于 Web 会话，常用 OAuth2 / JWT / API Key。每个端点强制授权校验，对象级授权防 IDOR。API Key 不可硬编码于前端代码或出现在 URL 参数中。

**Checkpoint**
- 每个 API 端点是否都有鉴权与授权校验
- 资源访问是否校验对象级归属
- API Key 是否避免出现在前端或 URL

**雷区清单**
- 禁止 API 无鉴权暴露
- 禁止 API Key 出现在前端代码或 URL 参数中
- 禁止信任客户端传入的权限字段

### 6.2 API 限流、配额与防滥用

限流（令牌桶 / 漏桶算法）防止暴力破解与 DoS 攻击。限流维度应包含用户、IP、接口多层级。超过限制时返回 HTTP 429 状态码与 `Retry-After` 头。

**Checkpoint**
- 敏感接口是否配置限流
- 限流是否多维度（用户 + IP + 接口）
- 超限是否返回 429 + Retry-After

**雷区清单**
- 禁止敏感接口无限流
- 禁止限流仅按 IP（NAT / 代理环境下失效）

### 6.3 API 数据保护与响应最小化

API 响应应按调用者角色裁剪字段，不返回超权限数据。敏感字段加密或脱敏。批量查询接口必须分页，防止全量数据爬取。

**Checkpoint**
- 响应字段是否按角色裁剪
- 敏感字段是否脱敏
- 批量查询是否强制分页

**雷区清单**
- 禁止接口返回超权限字段
- 禁止无分页或无上限的批量查询
- 禁止响应包含密码哈希等内部数据

### 6.4 API 版本管理与生命周期

API 版本化便于安全修复与废弃管理。含已知漏洞的旧版本应有明确下线计划，不可无限期保留。

**Checkpoint**
- API 是否版本化
- 废弃版本是否有下线计划

**雷区清单**
- 禁止旧版本无限期保留且含已知漏洞
- 禁止无版本管理导致破坏性变更

### 6.5 第三方集成与供应链安全

> 对应 OWASP Top 10:2025 A03（软件供应链失败）

OWASP 2025 将 A03 升级为「软件供应链失败」，涵盖依赖漏洞、构建产物完整性、第三方组件安全。应用需通过 SCA（软件成分分析）工具扫描依赖中的已知 CVE，维护 SBOM（软件物料清单）。

第三方接口调用需设置超时与重试控制，严格校验 TLS 证书。构建产物（如 Docker 镜像、JAR 包）需校验签名或哈希完整性。

**Checkpoint**
- 是否有 SCA 工具扫描依赖漏洞
- 是否维护 SBOM
- 第三方调用是否校验证书并设超时
- 构建产物是否校验完整性

**雷区清单**
- 禁止使用含已知高危 CVE 的依赖而不升级
- 禁止从不信任源拉取依赖（供应链投毒）
- 禁止第三方调用 trustAll 证书
- 禁止无超时无限等待第三方响应（资源耗尽）
- 禁止 CI/CD 不校验产物完整性

---

## 附录 A：OWASP Top 10:2025 映射对照表

| OWASP 2025 编号 | 类别 | 本文对应章节 |
|---|---|---|
| A01 | 访问控制失效（Broken Access Control） | 1.4 授权模型、6.1 API 授权 |
| A02 | 安全配置错误（Security Misconfiguration） | 5.3 信息泄露防护、6.4 API 生命周期 |
| A03 | 软件供应链失败（Software Supply Chain Failures） | 6.5 供应链安全 |
| A04 | 加密失败（Cryptographic Failures） | 第 4 章全部 |
| A05 | 注入（Injection） | 3.2 注入防御 |
| A06 | 不安全设计（Insecure Design） | 0.4 安全设计总原则 |
| A07 | 身份认证失效（Authentication Failures） | 1.1-1.3 认证、第 2 章会话 |
| A08 | 软件或数据完整性失效（Software or Data Integrity Failures） | 3.6 反序列化、4.5 MAC 与签名、6.5 供应链 |
| A09 | 安全日志与告警失效（Security Logging Failures） | 5.2 安全日志 |
| A10 | 异常条件处理不当（Mishandling of Exceptional Conditions） | 5.1 错误处理、3.4 SSRF |

---

## 附录 B：算法推荐与废弃速查表

### 对称加密

| 算法 / 模式 | 状态 | 推荐 |
|---|---|---|
| AES-256-GCM | 推荐 | 首选 AEAD |
| AES-128-GCM | 推荐 | 可用 AEAD |
| ChaCha20-Poly1305 | 推荐 | 无硬件加速场景首选 |
| AES-CTR + HMAC | 可用 | 需手动 Encrypt-then-MAC |
| AES-CBC | 不推荐 | 无完整性，Padding Oracle |
| AES-ECB | 禁用 | 泄露数据模式 |
| DES / 3DES / RC4 / Blowfish | 禁用 | NIST 已禁用 |

### 哈希函数

| 算法 | 状态 | 用途 |
|---|---|---|
| SHA-256 / SHA-512 | 推荐 | 通用哈希、HMAC |
| SHA-3-256 / SHA-3-512 | 推荐 | 与 SHA-2 互补 |
| BLAKE2 / BLAKE3 | 可用 | 高性能场景 |
| SHA-1 | 禁用 | 已破解 |
| MD5 | 禁用 | 碰撞已实战 |

### 口令哈希

| 算法 | 优先级 | 工作因子建议 |
|---|---|---|
| Argon2id | 首选 | 内存 64MB+，迭代 3+ |
| scrypt | 次选 | N=2^16, r=8, p=1 |
| bcrypt | 可选 | cost ≥10 |
| PBKDF2-HMAC-SHA-512 | 兼容 | 迭代 ≥210000 |
| MD5 / SHA 直接哈希 | 禁用 | GPU 秒级爆破 |

### 非对称加密与签名

| 算法 | 状态 | 参数要求 |
|---|---|---|
| RSA-OAEP | 推荐 | ≥2048 位，优选 3072 |
| RSA-PSS | 推荐 | ≥2048 位 |
| ECDSA (P-256/P-384) | 推荐 | 确定性 nonce (RFC 6979) |
| EdDSA (Ed25519) | 推荐 | 确定性签名 |
| RSA-PKCS#1 v1.5 | 禁用 | Bleichenbacher 攻击 |
| DSA | 禁用 | 已弃用 |
| RSA <2048 位 | 禁用 | NIST 已禁用 |

### 随机数

| API | 状态 | 用途 |
|---|---|---|
| SecureRandom | 推荐 | 所有安全场景 |
| KeyGenerator | 推荐 | 密钥生成 |
| java.util.Random | 禁用 | 可预测 |
| Math.random() | 禁用 | 可预测 |

### TLS

| 项目 | 推荐 | 禁用 |
|---|---|---|
| TLS 版本 | 1.3（首选）、1.2 | 1.0、1.1、SSLv3 |
| 密钥交换 | ECDHE | RSA 交换 |
| 对称加密 | AES-GCM、ChaCha20-Poly1305 | CBC、RC4、3DES |
| 证书签名 | RSA-PSS、ECDSA | PKCS#1 v1.5、SHA-1 |
| 证书校验 | 严格校验 | trustAll |

---

## 附录 C：Checkpoint 自检清单汇总

以下为全文 Checkpoint 的可勾选汇总，用于代码评审与上线评审。

### 认证与授权

- [ ] 登录失败提示统一，不泄露用户是否存在
- [ ] 登录尝试限制与锁定机制
- [ ] 认证端点强制 TLS
- [ ] 口令使用 Argon2id / bcrypt / PBKDF2 存储
- [ ] salt 每用户唯一随机
- [ ] 工作因子达标且定期评估
- [ ] MFA 重置流程同等强度认证
- [ ] 每个接口有授权校验
- [ ] 资源 ID 访问校验归属（防 IDOR）
- [ ] OAuth2 使用授权码 + PKCE
- [ ] JWT 验签显式指定算法
- [ ] access_token 生命周期 ≤30 分钟
- [ ] refresh_token 可撤销且绑定设备

### 会话管理

- [ ] 登录后轮换 sessionId
- [ ] 登出使服务端 token 失效
- [ ] 令牌用 SecureRandom 生成，≥128 位
- [ ] Cookie 设置 HttpOnly + Secure + SameSite
- [ ] 权限提升后轮换会话
- [ ] 敏感操作前重新认证
- [ ] 状态变更请求使用非 GET 方法
- [ ] Redis 配置密码与网络隔离

### 输入输出安全

- [ ] 所有外部输入服务端校验
- [ ] SQL 使用 `#{}` 或 PreparedStatement
- [ ] 命令执行避免拼接用户输入
- [ ] SpEL / OGNL 禁用动态求值用户输入
- [ ] XML 解析禁用外部实体
- [ ] 输出按上下文编码
- [ ] 设置 CSP 头
- [ ] 富文本使用白名单净化库
- [ ] SSRF 校验目标 IP，禁止内网段
- [ ] 文件校验基于魔数
- [ ] 上传文件重命名存储
- [ ] 避免原生序列化不可信数据
- [ ] 设置安全响应头
- [ ] API 响应最小化

### 密码学

- [ ] 使用标准库（JCA / Bouncy Castle）
- [ ] 对称加密使用 GCM 等 AEAD
- [ ] IV / Nonce 每次随机且不重复
- [ ] GCM 认证标签校验失败时拒绝
- [ ] RSA 使用 OAEP / PSS 填充
- [ ] RSA 密钥 ≥2048 位
- [ ] ECDSA 使用确定性签名
- [ ] ECDH 使用 ECDHE（前向保密）
- [ ] 哈希使用 SHA-2 / SHA-3
- [ ] HMAC 使用常量时间比较
- [ ] 口令使用 Argon2id / bcrypt / PBKDF2
- [ ] 口令工作因子达标
- [ ] 安全随机数使用 SecureRandom
- [ ] 密钥存储于 HSM / KMS / KeyStore
- [ ] 密钥以 byte[] 存储，使用后清零
- [ ] 不同用途密钥分离
- [ ] TLS ≥1.2，优选 1.3
- [ ] 密码套件使用 ECDHE + GCM
- [ ] 启用 HSTS
- [ ] 客户端严格校验证书

### 错误处理与日志

- [ ] 异常时默认拒绝（fail-secure）
- [ ] 全局异常处理器统一封装
- [ ] 错误响应不泄露内部信息
- [ ] 安全事件记录 who / what / when / result
- [ ] 日志敏感字段脱敏
- [ ] 日志防篡改
- [ ] 生产关闭 Actuator / Swagger 调试端点

### API 安全

- [ ] 每个 API 端点鉴权与授权
- [ ] API Key 不出现在前端或 URL
- [ ] 敏感接口限流
- [ ] 限流多维度（用户 + IP + 接口）
- [ ] 响应字段按角色裁剪
- [ ] 批量查询强制分页
- [ ] SCA 工具扫描依赖漏洞
- [ ] 维护 SBOM
- [ ] 第三方调用校验证书并设超时

---

## 附录 D：参考资料与权威链接

| 来源 | 说明 |
|---|---|
| OWASP Top 10:2025 | https://owasp.org/Top10/ |
| OWASP ASVS v5.0 | https://owasp.org/www-project-application-security-verification-standard/ |
| OWASP Cheat Sheet Series | https://cheatsheetseries.owasp.org/ |
| NIST SP 800-131A Rev2 | 密码算法迁移指南 |
| NIST FIPS 203 / 204 / 205 | 后量子密码标准（ML-KEM / ML-DSA / SLH-DSA） |
| NIST SP 800-63B | 数字身份指南（口令策略） |
| NIST SP 800-90A | 随机数生成器标准 |
| CWE-321 | 硬编码密钥 |
| CWE-327 | 使用已破解或风险的密码算法 |
| CWE-329 | IV 不可预测性失败 |
| CWE-338 | 使用密码学不安全的 PRNG |
| CWE-780 | RSA PKCS#1 v1.5 填充 |
| CWE-916 | 口令哈希使用不足迭代次数 |
