# 服务端安全 Checkpoint 文档 — 实施计划

## 摘要

生成一份面向 Java 高级开发/架构师的**独立参考文档**（Markdown 格式），系统总结服务端开发安全 checkpoint，以密码算法使用范式及雷区为核心重点。文档以「关键要点 → Checkpoint 自检 → 雷区清单」三段式结构组织，所有结论标注权威标准来源（OWASP Top 10:2025、NIST SP 800-131A Rev2、NIST FIPS 203/204/205 PQC 标准、OWASP ASVS v5.0、CWE）。第 0-3、5-6 章为纯概念说明；**第 4 章密码学**作为核心重点，在概念说明基础上补充 JCA/Bouncy Castle 规范实现的 Java 代码范例，展示正确用法（含关键参数选择与常见错误对比）。

**交付物**：单一 Markdown 文件 `server-security-checkpoint.md`，存放在工作区根目录。

---

## 当前状态分析

工作区目录当前为空，无既有代码或文档需对齐。本文档为**独立最佳实践参考**，不依赖任何项目代码，可直接分享给团队用于代码评审、架构评审与安全培训。

### 权威标准调研结论（2026 时效）

| 标准来源 | 关键结论 |
|---|---|
| OWASP Top 10:2025（2025-11 发布） | A03 升级为「软件供应链失败」；A10 新增「异常条件处理不当」（SSRF 被吸收）；A04「加密失败」仍为核心 |
| NIST SP 800-131A Rev2 | SHA-1/RSA-1024/3DES/DES/RC4 已禁用或弃用；RSA 需≥2048 位 |
| NIST FIPS 203/204/205 | 后量子密码正式标准发布（ML-KEM/ML-DSA/SLH-DSA），高风险系统 2030 前迁移 |
| OWASP A04 密码学建议 | 口令用 Argon2/yescrypt/scrypt/PBKDF2-HMAC-SHA-512；禁用 MD5/SHA1/CBC/PKCS#1v1.5；TLS≥1.2+前向保密；始终用认证加密 |
| NIST SP 800-63B | 口令策略重视长度（≥12位）而非强制复杂度；维护泄露口令黑名单 |

---

## 文档设计原则

1. **三段式结构**：每节统一为「关键概念要点 → Checkpoint 自检清单 → 雷区清单(Forbidden)」
2. **标准溯源**：所有结论标注 OWASP 2025 / NIST / CWE / ASVS 编号
3. **密码学为核心**：第 4 章深度展开算法选型与雷区，占全文最大篇幅；4.2-4.9 每节在概念说明后补充 Java 规范实现代码范例（基于 JCA/Bouncy Castle），展示正确参数选择与 API 用法，并在代码注释中标注雷区对照
4. **代码范例原则**：仅第 4 章含代码，其他章节纯概念；代码聚焦「规范实现」而非完整工程，精简可读；错误用法以注释 `// 错误：` 形式对照，不展开完整错误示例
5. **交叉索引**：正文引用标准编号，附录提供 OWASP 映射表与算法速查表
6. **写作风格**：遵循 doc-writing-guide 规范——避免空泛修饰、避免元叙述、雷区统一「禁止…」句式便于扫描、表格呈现算法对比、bold 仅用于专有名词与关键警告

---

## 文档完整大纲

### 第 0 章 文档导论
- 0.1 文档目的、读者对象与使用方式
- 0.2 标准依据与版本声明（OWASP 2025 / NIST / ASVS v5 / CWE）
- 0.3 术语表（CIA 三性、前向保密、AEAD、KDF、HSM/KMS、CSPRNG 等）
- 0.4 安全设计总原则（最小权限、纵深防御、失败安全、零信任）

### 第 1 章 认证与授权安全
- 1.1 身份认证基础与认证因素（知识/持有/固有，强认证≥2因素，防用户枚举）
- 1.2 口令策略与口令存储（Argon2id>scrypt>bcrypt>PBKDF2-HMAC-SHA-512，NIST 800-63B 长度优先，泄露库比对）
- 1.3 多因素认证(MFA)与无密码认证（TOTP 优于短信，WebAuthn/Passkey 抗钓鱼）
- 1.4 授权模型与访问控制（RBAC/ABAC，默认拒绝，IDOR 防御，横向/纵向越权）
- 1.5 OAuth2 / OIDC 协议安全（授权码+PKCE，state/nonce，redirect_uri 校验）
- 1.6 JWT 与令牌安全（显式指定算法防 alg=none，短生命 access_token，可撤销 refresh_token）

### 第 2 章 会话管理
- 2.1 会话生命周期（创建/续期/过期/销毁闭环，登录后轮换 sessionId）
- 2.2 会话令牌生成与传输（CSPRNG ≥128位熵，HttpOnly+Secure+SameSite Cookie）
- 2.3 会话固定、劫持与超时（权限提升后轮换，敏感操作 step-up 认证）
- 2.4 CSRF 防护（SameSite Cookie + anti-CSRF token，GET 禁止状态变更）
- 2.5 分布式会话与 Redis 会话安全（TTL，敏感数据加密，Redis 鉴权隔离）

### 第 3 章 输入输出安全
- 3.1 输入验证与数据净化原则（白名单优先，全入口校验）
- 3.2 注入防御（SQL 用 `#{}` 非 `${}`，命令注入，SpEL/OGNL 表达式注入 RCE，XXE，NoSQL）
- 3.3 XSS 防御（按上下文输出编码，CSP，白名单净化库）
- 3.4 SSRF 防御（校验目标主机，禁内网段，DNS 重绑定防护）
- 3.5 文件上传与下载安全（魔数校验，重命名，路径穿越，ZipSlip）
- 3.6 反序列化安全（禁原生序列化不可信数据，ObjectInputFilter，Fastjson/Jackson/XStream 漏洞）
- 3.7 输出编码与响应头安全（CSP/X-Content-Type-Options/X-Frame-Options/Referrer-Policy，响应最小化）

### 第 4 章 密码学（核心重点章节，含 Java 规范实现代码范例）
- 4.1 密码学设计原则与威胁模型（不自实现，Kerckhoffs 原则，机密性/完整性/真实性/不可否认性区分，AEAD 优先）
- 4.2 对称加密（AES-128/256，GCM 首选 AEAD，IV/Nonce 不可重复，ECB 禁用，CBC 不推荐）— **代码范例：AES-GCM 加解密（KeyGenerator 生成密钥、SecureRandom 生成 IV、Cipher API 用法、认证标签校验）**
- 4.3 非对称加密与密钥协商（RSA-OAEP/PSS，≥2048 位，ECDSA 确定性签名 RFC6979，ECDHE 前向保密）— **代码范例：RSA-OAEP 加密、RSA-PSS/ECDSA 签名与验签（KeyPairGenerator、Signature API）**
- 4.4 哈希函数（SHA-2/SHA-3/BLAKE2/3，禁 MD5/SHA-1，通用哈希不存口令）— **代码范例：SHA-256/SHA-3 哈希（MessageDigest API）**
- 4.5 消息认证码与数字签名（HMAC-SHA-256/512，常量时间比较，Encrypt-then-MAC，签名提供不可否认性）— **代码范例：HMAC-SHA-256 计算（Mac API）、常量时间比较（MessageDigest.isEqual）**
- 4.6 口令哈希与密钥派生函数（Argon2id 首选，每用户 salt，pepper 分离存储，HKDF 派生，工作因子可调）— **代码范例：Argon2id/bcrypt 口令哈希与校验（Bouncy Castle Argon2Parameters）、PBKDF2-HMAC-SHA-512（SecretKeyFactory）、HKDF 派生**
- 4.7 随机数与熵源（SecureRandom CSPRNG，禁 Random/Math.random，禁固定种子）— **代码范例：SecureRandom 生成令牌/密钥/salt**
- 4.8 密钥管理（生成/存储 HSM-KMS/轮换/销毁 byte[] 清零/密钥分离/禁硬编码）— **代码范例：密钥生成、byte[] 清零（Arrays.fill）、KeyStore 存储**
- 4.9 证书与 TLS（TLS≥1.2 优选 1.3，ECDHE+GCM，HSTS，禁 trustAll，PQC 混合迁移路线）— **代码范例：TLS 客户端正确证书校验、禁用 trustAll 的对照**
- 4.10 密码算法雷区总清单（核心汇总表格：类别→禁用项→风险→推荐替代→标准依据）

### 第 5 章 错误处理与日志
- 5.1 安全错误处理与异常管理（OWASP 2025 A10 异常条件，失败安全默认拒绝，禁堆栈泄露）
- 5.2 安全日志实践（记录安全事件 who/what/when/result，禁记录口令/密钥/令牌，防篡改）
- 5.3 敏感信息泄露防护（生产关闭 actuator/swagger 调试端点，全链路脱敏）

### 第 6 章 API 安全
- 6.1 API 认证与授权（独立鉴权，对象级授权防 IDOR，API Key 禁前端）
- 6.2 API 限流、配额与防滥用（令牌桶，多维度限流，429+Retry-After）
- 6.3 API 数据保护与响应最小化（字段裁剪，脱敏，分页防爬取）
- 6.4 API 版本管理与生命周期（废弃版本下线计划）
- 6.5 第三方集成与供应链安全（OWASP 2025 A03，SCA 扫描 CVE，SBOM，产物签名校验，调用超时+证书校验）

### 附录
- A. OWASP Top 10:2025 映射对照表（A01-A10 → 文档章节）
- B. 算法推荐与废弃速查表（即 4.10 雷区总清单，独立可撕页）
- C. Checkpoint 自检清单汇总（可勾选版，用于代码评审/上线评审）
- D. 参考资料与权威链接

---

## 实施步骤

### 步骤 1：创建文档骨架
在工作区根目录创建 `server-security-checkpoint.md`，写入文档头部（标题、版本声明、标准依据、术语表、安全设计总原则），并搭建全部章节标题与目录锚点。

### 步骤 2：撰写第 4 章密码学（最高优先级）
按 4.1-4.10 顺序撰写，每节三段式（要点/Checkpoint/雷区）。4.2-4.9 每节在概念说明后补充 Java 规范实现代码范例（基于 JCA/Bouncy Castle），展示正确 API 用法与参数选择，错误用法以 `// 错误：` 注释对照。4.10 雷区总清单以表格呈现，整合 NIST SP 800-131A Rev2 废弃算法与 OWASP A04 建议。

### 步骤 3：撰写第 1 章认证与授权
涵盖口令存储（Argon2id 优先级链）、MFA、授权（IDOR）、OAuth2/JWT 安全。重点雷区：alg=none、MD5 存口令、信任客户端权限字段。

### 步骤 4：撰写第 2 章会话管理
会话固定防护、令牌生成（CSPRNG）、CSRF、分布式会话。

### 步骤 5：撰写第 3 章输入输出安全
注入（MyBatis `${}` vs `#{}`）、XSS、SSRF、反序列化、文件上传。重点雷区标注 CWE 编号。

### 步骤 6：撰写第 5 章错误处理与日志
结合 OWASP 2025 新增 A10「异常条件处理不当」，强调 fail-secure。

### 步骤 7：撰写第 6 章 API 安全
含 OWASP 2025 A03 供应链安全（SCA/SBOM/签名校验）。

### 步骤 8：撰写附录
OWASP 映射表、算法速查表、Checkpoint 汇总、参考资料。

### 步骤 9：通读校验
- 检查三段式结构一致性
- 检查雷区清单「禁止…」句式统一
- 检查标准编号标注完整性
- 检查无 emoji、无元叙述、bold 使用规范
- 检查表格格式正确

---

## 假设与决策

| 决策项 | 选择 | 理由 |
|---|---|---|
| 输出格式 | Markdown 单文件 | 用户明确要求 md 文件 |
| 内容范围 | 全面服务端安全，密码学为核心重点章 | 用户选择「全面服务端安全」 |
| 代码示例 | 第 4 章密码学含 Java 规范实现范例（JCA/Bouncy Castle），其他章节纯概念 | 用户反馈要求密码学章节补充代码范例 |
| 项目结合 | 独立参考文档，不依赖项目代码 | 用户选择「独立参考文档」 |
| 标准版本 | OWASP Top 10:2025 + NIST SP 800-131A Rev2 + FIPS 203/204/205 | 2026 年最新权威标准 |
| 章节结构 | 三段式（要点/Checkpoint/雷区） | 安全 checkpoint 文档的最佳实践形态 |
| 写作风格 | 遵循 doc-writing-guide：描述性语言、避免空泛修饰、雷区统一句式 | 保证专业可读性 |

---

## 验证步骤

1. **结构完整性**：文档包含第 0-6 章及附录 A-D，每节均含三段式内容
2. **标准溯源**：核心结论均标注 OWASP/NIST/CWE/ASVS 编号，附录映射表完整
3. **雷区覆盖**：4.10 雷区总清单表格覆盖对称/非对称/哈希/口令/随机数/密钥/TLS 全类别
4. **代码范例**：第 4 章 4.2-4.9 每节含 Java 规范实现代码，基于 JCA/Bouncy Castle，展示正确 API 用法与参数，错误用法以注释对照
5. **时效性**：算法推荐与废弃符合 2026 年标准（含 PQC 迁移路线）
6. **格式规范**：无 emoji、无元叙述、bold 用于专有名词/关键警告、表格格式正确、目录锚点可用
7. **可读性**：雷区清单可快速扫描，Checkpoint 可用于评审自检
