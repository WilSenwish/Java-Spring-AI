# 附录 参考资料与术语表

> 本附录是全站工具书：术语与缩略语、政策清单、标准清单、测评批次索引、厂商图谱速查、参考来源索引、证据分级与数据使用守则。
>
> 调研基准日：**2026-11-05**。所有 URL 为该日期检索所得，链接可能失效或被后续文件替代，引用前请复核。

---

## A. 术语表

| 术语 | 释义 | 辨析要点 |
|---|---|---|
| 信创 | 信息技术应用创新，词源为 2016 年成立的「信息技术应用创新工作委员会」 | 产业/工程概念，**非法定术语** |
| 核高基 | 核心电子器件、高端通用芯片及基础软件产品，2006 年国家重大科技专项之一 | 产业起点 |
| 安可 | 安全可控，2014—2019 年前后的阶段性表述 | 现行正式文件中较少使用 |
| 自主可控 | 关键技术、供应链与持续演进能力不受制于人 | ≠ 国产；看控制权而非产地 |
| 安全可靠 | 指南 V3.0 定义：产品及研发单位的核心技术、安全保障、持续发展，覆盖全生命周期 | ≠ 等保等级 |
| 本国产品 | 34 号文定义：关境内实现属性改变 + 组件成本占比达标 + 特定产品关键组件/工序达标 | 产地与成本概念，不含知识产权要求 |
| 属性改变 | 经制造、加工、组装产生完全不同于原材料/组件的新产品，具新名称与特征（用途） | 五类细微操作不构成属性改变 |
| 组件成本占比 | 境内生产的组件成本 / 产品总成本，按二级组件核算 | 34 号文附件 1 |
| 价格评审优惠 | 对本国产品报价给予 20% 扣除后参与评审 | 不是补贴、不是成交价打折 |
| 「2+8+N」 | 党政两大体系 + 八大关键行业 + 全行业的分层推进框架 | 行业共识性表述，非法定分类 |
| 等保 2.0 | 网络安全等级保护制度第二版，GB/T 22239-2019 为核心标准 | 评价对象是**系统** |
| 密评 | 商用密码应用安全性评估 | 评价密码应用合规性、正确性、有效性 |
| 关基 | 关键信息基础设施 | 义务主体，触发三同步、采购审查、年度密评等 |
| 三同步 | 商用密码保障系统同步规划、同步建设、同步运行 | 局令第 5 号 |
| 安全可靠测评 | 中国信息安全测评中心 + 国家保密科技测评中心联合开展的产品与研发单位测评 | **自愿申请**，Ⅰ/Ⅱ 级，有效期 3 年 |
| 适配测试报告 | 第三方机构在指定国产环境组合下出具的兼容性/性能/安全性测试报告 | 常为申请评估证书的前置 |
| 兼容互认证书 | 由单一软硬件厂商出具的产品互通证明 | 企业间互认，不能替代第三方报告 |
| 信创产品评估证书 | 工委会/专委会组织专家评审后颁发，含知识产权自主率、供应链、股权结构审查 | 名称不统一，无统一国标 |
| 一云多芯 | 统一云管平台纳管 x86/ARM/LoongArch 等异构算力 | 碎片化收敛手段，同时带来锁定风险 |
| 双轨并行 | 新旧系统长期同时运行并实时同步，逐步切流量 | 高风险迁移的安全阀 |
| 伪信创 / 套壳 | 内核或核心组件仍依赖境外技术，仅外层国产化 | 制造虚假安全感 |
| SBOM | Software Bill of Materials，软件物料清单 | 漏洞溯源、许可证合规、供应链透明的核心依据 |
| 根技术 | 指令集、内核、数据库引擎、编译器、EDA 算法等底层原创能力 | 下半场竞争焦点 |
| 全栈协同 | 芯片—OS—DB—中间件—应用跨层联合调优 | 相对「组合式适配」 |
| TCO | Total Cost of Ownership，总拥有成本 | 信创项目应按 5 年计 |

---

## B. 缩略语表

| 缩写 | 全称 / 中文 |
|---|---|
| BAA | Buy American Act（美国《购买美国产品法》） |
| TAA | Trade Agreements Act（美国《贸易协定法》） |
| FAR | Federal Acquisition Regulation（美国联邦采购条例） |
| FIPS | Federal Information Processing Standards |
| CC | Common Criteria（信息技术安全评估通用准则） |
| CMMC | Cybersecurity Maturity Model Certification |
| NDAA | National Defense Authorization Act |
| GPA | WTO Government Procurement Agreement |
| CNAS / CMA | 中国合格评定国家认可委员会 / 检验检测机构资质认定 |
| SCA / SAST / DAST | 软件成分分析 / 静态应用安全测试 / 动态应用安全测试 |
| SDS / CMP | 软件定义存储 / 多云管理平台 |
| BMC / BIOS / UEFI | 基板管理控制器 / 基本输入输出系统 / 统一可扩展固件接口 |
| TPCM / TCM | 可信平台控制模块 / 可信密码模块 |
| TLCP | 传输层密码协议（GB/T 38636-2020） |
| SM2/SM3/SM4/SM9 | 国密公钥/杂凑/分组/标识密码算法 |
| OFD | 开放式版式文档 |
| RPO / RTO | 恢复点目标 / 恢复时间目标 |
| TPS / P99 | 每秒事务数 / 99 分位响应时间 |
| HTAP | 混合事务/分析处理 |
| JCE / JSSE | Java 加密扩展 / Java 安全套接字扩展 |
| ISV | 独立软件供应商 |
| C86 | 国产 x86 兼容路线（海光/兆芯）的采购分包称谓 |
| PKS | 飞腾（Phytium）+ 麒麟（Kylin）+ 安全（Security）体系 |

---

## C. 政策与法规清单

| 文号 / 名称 | 发布机关 | 关键日期 | 效力/性质 | 一手链接 |
|---|---|---|---|---|
| 《国务院办公厅关于在政府采购中实施本国产品标准及相关政策的通知》**国办发〔2025〕34 号** | 国务院办公厅 | 成文 2025-09-28；发布 2025-09-30；**施行 2026-01-01** | 规范性文件 | https://www.gov.cn/zhengce/zhengceku/202509/content_7043000.htm ；国务院公报版 https://www.gov.cn/gongbao/2025/issue_12346/202510/content_7044731.html |
| 《中共中央关于制定国民经济和社会发展第十五个五年规划的建议》 | 二十届四中全会通过 | 2025-10-23 通过；2025-10-28 发布 | 中央政策文件 | https://www.gov.cn/zhengce/202510/content_7046052.htm |
| **国务院令第 834 号**《国务院关于产业链供应链安全的规定》 | 国务院 | 2026-03-13 常务会议通过；**2026-03-31 公布并施行**；新华社 2026-04-07 受权发布 | 行政法规 | https://www.gov.cn/zhengce/content/202604/content_7064837.htm |
| 司法部负责人就 834 号令答记者问 | 司法部 | 2026-04 | 官方解读 | https://www.gov.cn/zhengce/202604/content_7064912.htm （繁体镜像 big5.www.gov.cn 同路径） |
| 《中华人民共和国网络安全法》2025 年修改决定 | 全国人大常委会 | 2025-10-28 通过；**2026-01-01 施行** | 法律 | 全国人大网 / gov.cn；解读见 https://m.gmw.cn/toutiao/2026-01/01/content_38513202.htm |
| 《关键信息基础设施商用密码使用管理规定》（国家密码管理局、网信办、公安部令第 5 号） | 三部门 | 2025 年公布 | 部门规章 | https://www.gov.cn/zhengce/202506/content_7030047.htm |
| 《中央企业违规经营投资责任追究实施办法》**国务院国资委令第 46 号** | 国务院国资委 | 2025-11-28 公布；**2026-01-01 施行** | 部门规章 | https://wap.sasac.gov.cn/n2588035/n2588320/n2588335/c35128064/content.html ；答记者问 http://www.sasac.gov.cn/n2588035/n16549643/n16549895/n16550082/c35128141/content.html |
| 国资委 79 号文（2022-09） | 国务院国资委 | 2022-09 | **未见官网公开全文**，均为转述 | 转述见 https://www1.xinhuanet.com/info/20241205/e070a059c21a4467aaa79b52a35527d9/c.html 、https://paper.cnstock.com/html/2023-04/18/content_1749448.htm |
| 《商用密码应用安全性评估管理办法》（局令第 3 号） | 国家密码管理局 | 2023-11-01 施行 | 部门规章 | 国家密码管理局 https://www.oscca.gov.cn/ |
| 《关键信息基础设施安全保护条例》《商用密码管理条例》《网络数据安全管理条例》《网络安全审查办法》 | 国务院 / 多部门 | 各自行施行日期 | 行政法规 / 规章 | gov.cn 政策文件库 |
| 《安全可靠测评工作指南（试行）》 | 中国信息安全测评中心等 | 2023-07 | 测评依据 | 经公告援引 |
| **《安全可靠测评工作指南 V3.0》** | 中国信息安全测评中心等 | 2025-07 | 测评依据 | http://www.itsec.gov.cn/ |
| 《国家中长期科学和技术发展规划纲要（2006—2020）》「核高基」 | 国务院 | 2006 | 科技规划 | 公开资料 |
| 财政部/工信部「三类九款」政府采购配置标准（含《中央国家机关台式计算机批量集中采购配置标准—2024 版》） | 财政部、工信部、国机采 | 分版本更新 | 采购需求标准 | 以最新采购文件为准 |

---

## D. 标准清单（常用）

| 标准号 | 名称 | 用途 |
|---|---|---|
| GB/T 22239-2019 | 信息安全技术 网络安全等级保护基本要求 | 等保 2.0 核心 |
| GB/T 39786-2021 | 信息安全技术 信息系统密码应用基本要求 | 密评核心 |
| GM/T 0054-2018 | 信息系统密码应用基本要求 | 密评行业版 |
| GB/T 37092-2018 | 信息安全技术 密码模块安全要求 | 密码产品分级 |
| GB/T 38625-2020 | 信息安全技术 密码模块安全检测要求 | 检测 |
| GB/T 32918.1~5 | SM2 椭圆曲线公钥密码算法（总则/签名/密钥交换/加密/参数） | 国密 |
| GB/T 35275 / GB/T 35276 | SM2 密码算法加密签名消息语法规范 / 使用规范 | 国密（注意 2026 修订版） |
| GB/T 32905-2016 | 信息安全技术 SM3 密码杂凑算法 | 国密 |
| GB/T 32907-2016 | 信息安全技术 SM4 分组密码算法 | 国密 |
| GB/T 38635.1/.2-2020、GB/T 41389-2022、GM/T 0044 系列 | SM9 标识密码算法及使用规范 | 国密 |
| GB/T 38636-2020 | 信息安全技术 传输层密码协议（TLCP） | 国密传输 |
| GB/T 36322-2018 | 信息安全技术 密码设备应用接口规范 | 接口 |
| GB/T 36968-2018 / GM/T 0023-2014 / GM/T 0025-2014 | IPSec VPN / SSL VPN 网关规范 | 网关 |
| GB/T 35291-2017 / GM/T 0017-2012 | 智能密码钥匙应用接口 | UKey |
| GB/T 39204-2022 | 信息安全技术 关键信息基础设施安全保护要求 | 关基 |
| GB/T 25000.51-2016 | 系统与软件工程 软件产品质量测试细则 | 适配测试常用依据 |
| GB/T 33560-2026、GB/T 35275-2026、GB/T 47471-2026 等 | 2024—2026 新发布/修订密码国标 | 引用前核对现行版本 |

> 标准状态查询：全国标准信息公共服务平台 https://std.samr.gov.cn/ ；密码行业标准 https://www.oscca.gov.cn/sca/xxgk/bzgf.shtml

---

## E. 安全可靠测评公告批次索引

| 公告 | 日期 | 依据 | 品类 | 一手链接 |
|---|---|---|---|---|
| 2023 年第 1 号 | 2023-12 | 指南（试行） | CPU、OS、集中式数据库（首批） | itsec.gov.cn 测评公告栏目 |
| 2024 年第 1 号 | 2024-05 | 指南（试行） | CPU、OS | 同上 |
| 2024 年第 2 号 | 2024-09 | 指南（试行） | CPU、OS | 同上 |
| **2025 年第 1 号** | **2025-03-14** | 指南（试行） | CPU 8 款；桌面/服务器 OS 各 1 款 | http://www.nsstec.org.cn/tzgg/354344.shtml |
| 2025 年第 2 号 | 2025-08 | V3.0 | 据行业汇总无新增芯片 | itsec.gov.cn |
| **2025 年第 3 号** | **2025-09-12** | **V3.0** | CPU 4 款；OS 4 款 | https://www.itsec.gov.cn/aqkkcp/cpgg/202509/t20250912_235645.html |
| **2026 年第 1 号** | **2026-01-16** | V3.0 | **仅操作系统 5 款** | https://www.itsec.gov.cn/aqkkcp/cpgg/202601/t20260116_249958.html |
| **2026 年第 2 号** | **2026-05-26** | V3.0 | **AI 训推芯片 9 款 + 集中式 DB 8 款 + 分布式 DB 15 款** | https://www.itsec.gov.cn/aqkkcp/cpgg/202605/t20260526_259396.html ；镜像 http://www.nsstec.org.cn/tzgg/354469.shtml |

机构主页：中国信息安全测评中心 http://www.itsec.gov.cn/ ；国家保密科技测评中心 http://www.nsstec.org.cn/

> 全部公告自发布之日起**有效期三年**，引用须核对公告日期、产品名、版本号与等级。详见 [06](./06-安全合规与测评认证体系.md) §4。

---

## F. 厂商与生态速查

| 层 | 代表（非完整名录，不构成推荐） |
|---|---|
| CPU | 海光、兆芯（x86）；鲲鹏/海思、飞腾（ARM）；龙芯（LoongArch）；申威（SW64）；玄铁/香山/进迭时空（RISC-V） |
| AI 芯片 | 昇腾、平头哥真武、壁仞、海光 DCU、天数智芯、沐曦、摩尔线程、寒武纪、燧原、昆仑芯 |
| 整机 | 华为 TaiShan、浪潮、中科曙光、长城、联想开天、同方、宝德、中兴 |
| 桌面/服务器 OS | 麒麟软件、统信软件、中科方德、麒麟信安、凝思、中兴新支点；云 OS：华为云欧拉、阿里云、腾讯云、天翼云 CTyunOS |
| 终端/全场景 OS | HarmonyOS / OpenHarmony |
| 开源根社区 | openEuler、OpenAnolis（龙蜥）、OpenHarmony、openGauss、deepin、RISC-V 社区 |
| 数据库 | 达梦、人大金仓/电科金仓、南大通用 GBase、OceanBase、GaussDB、GoldenDB、TDSQL、PolarDB、TiDB、崖山、星环、海量数据 Vastbase、DolphinDB、TimechoDB |
| 中间件 | 东方通、宝兰德、中创股份、金蝶天燕、普元信息；云厂商 EDAS/TDMQ/RocketMQ |
| 云平台 | 华为云 Stack、中国电子云 CECSTACK、天翼云、阿里云、腾讯云、EasyStack ECF、ZStack、青云 |
| JDK/编译器 | 毕昇 JDK、Dragonwell（龙井）、Kona、龙芯 JDK、麒麟信安 JDK；毕昇编译器、GCC/LLVM 国产架构后端 |
| 办公/应用 | 金山 WPS、永中 Office、OFD/电子签章、用友 YonBIP、金蝶苍穹、致远互联、泛微 |
| 行业 ISV | 中电金信、宇信科技、神州信息、长亮科技、南天信息、东软、卫宁、太极等 |
| 安全 | 奇安信、启明星辰、绿盟科技、安恒信息、深信服、北信源、江民、格尔软件、电科网安 |
| 上游 | 华大九天（EDA）、中芯国际、华虹、长电科技、通富微电、北方华创、中微公司等 |

---

## G. 参考来源索引

> 编号规则：`Sxx`。等级定义见 [README §四](./README.md)。**B/C 级多为聚合站或媒体转述，引用前请回溯原始报告/公告。**

### G.1 A 级（一手权威原文）

| 编号 | 来源 | URL | 主要引用位置 |
|---|---|---|---|
| S01 | 中国政府网：国办发〔2025〕34 号全文 | https://www.gov.cn/zhengce/zhengceku/202509/content_7043000.htm | 02 §3、01 §3.1、09 |
| S02 | 国务院公报版 34 号文 | https://www.gov.cn/gongbao/2025/issue_12346/202510/content_7044731.html | 02 §3 |
| S03 | 中国政府网：「十五五」规划建议 | https://www.gov.cn/zhengce/202510/content_7046052.htm | 02 §4.1、08、10 |
| S04 | 中国政府网：国务院令第 834 号全文 | https://www.gov.cn/zhengce/content/202604/content_7064837.htm | 02 §4.2、09 |
| S05 | 司法部就 834 号令答记者问 | https://www.gov.cn/zhengce/202604/content_7064912.htm | 02 §4.2 |
| S06 | 中国政府网：关键信息基础设施商用密码使用管理规定 | https://www.gov.cn/zhengce/202506/content_7030047.htm | 02 §4.5、06 §3 |
| S07 | 国务院国资委：令第 46 号全文 | https://wap.sasac.gov.cn/n2588035/n2588320/n2588335/c35128064/content.html | 02 §4.4、09 |
| S08 | 国务院国资委：46 号令答记者问 | http://www.sasac.gov.cn/n2588035/n16549643/n16549895/n16550082/c35128141/content.html | 02 §4.4、09 |
| S09 | 中国信息安全测评中心：2025 年第 3 号公告 | https://www.itsec.gov.cn/aqkkcp/cpgg/202509/t20250912_235645.html | 04 §2、05 §1.2、06 §4.2 |
| S10 | 中国信息安全测评中心：2026 年第 1 号公告 | https://www.itsec.gov.cn/aqkkcp/cpgg/202601/t20260116_249958.html | 05 §1.2、06 §4.2、09 |
| S11 | 中国信息安全测评中心：2026 年第 2 号公告 | https://www.itsec.gov.cn/aqkkcp/cpgg/202605/t20260526_259396.html | 04 §3、05 §2.2、06 §4.2 |
| S12 | 国家保密科技测评中心：2025 年第 1 号公告 | http://www.nsstec.org.cn/tzgg/354344.shtml | 04 §2、06 §4.2 |
| S13 | 国家保密科技测评中心：2026 年第 2 号公告（镜像） | http://www.nsstec.org.cn/tzgg/354469.shtml | 06 §4.2 |
| S14 | 中国信息安全测评中心主页（机构与业务说明） | http://www.itsec.gov.cn/ | 06 §4.1 |
| S15 | 国家密码管理局标准规范页 | https://www.oscca.gov.cn/sca/xxgk/bzgf.shtml | 附录 D |
| S16 | 全国标准信息公共服务平台 | https://std.samr.gov.cn/ | 附录 D |
| S17 | OpenHarmony 项目官网 | https://www.openharmony.cn/ | 05 §1.1 |
| S18 | 玄铁 RISC-V 官网 | http://www.xrvm.cn/ | 04 §6 |
| S19 | 中国电子云 CECSTACK V5 白皮书 | https://cecloud.com/upload/2024/10-23/14-21-5404812029920107.pdf | 03 §5、05 §4 |
| S20 | 新华网：2024 年「信创+AI」访谈（79 号文转述） | https://www1.xinhuanet.com/info/20241205/e070a059c21a4467aaa79b52a35527d9/c.html | 02 §5.1 |
| S21 | 上海证券报：能科科技公告（79 号文转述） | https://paper.cnstock.com/html/2023-04/18/content_1749448.htm | 02 §5.1 |
| S22 | 上海证券报：邦彦技术公告（政策与市场判断） | https://paper.cnstock.com/html/2026-04/29/content_2209428.htm | 08 §2.3 |
| S23 | 光明网：网络安全法修改解读 | https://m.gmw.cn/toutiao/2026-01/01/content_38513202.htm | 02 §4.3 |

### G.2 B 级（权威机构结论 / 主流媒体，多为转引）

| 编号 | 来源 | URL | 说明 |
|---|---|---|---|
| S24 | 北京通信信息协会《信创发展史及信创相关政策》 | https://www.bita.org.cn/newsinfo/7476469.html | 发展史三阶段、2+8 行业清单 |
| S25 | 中国高新网《规范化发展信创产业迫在眉睫》 | http://www.chinahightech.com/chanye/2025-02/28/content_303060.html | 开放生态、整机厂作用、赛迪硬件预测 |
| S26 | 人民日报《中国经济周刊》倪光南访谈 | https://paper.people.com.cn/zgjjzk/html/2016-04/18/content_1677475.htm | 自主可控定义、「增值」准则、反假国产 |
| S27 | 人民网财经 / 中国经济网《聚力开源「芯」生态 国产算力谋破局》 | https://finance.people.com.cn/BIG5/n1/2026/1022/c1004-40819240.html | RISC-V 产业进展与瓶颈 |
| S28 | Federal News Network: Competing global supply chain approaches | https://federalnewsnetwork.com/commentary/2024/07/competing-global-supply-chain-approaches | 美国 BAA/TAA 价格优惠与门槛 |
| S29 | USFCR: The Trade Agreements Act and Buy American Act Updates | https://blogs.usfcr.com/the-trade-agreements-act-and-buy-american-act-updates | 65%→75% 成分门槛、TAA 指定国家 |
| S30 | 律所分析：Buy American, TAA and the False Claims Act | https://www.customsfraud.com/blog/buy-american-trade-agreements-act-requirements-and-the-false-claims-act | FAR 25.1、实质性改变、FCA 责任 |
| S31 | Uniqcli: TAA Compliance for Federal IT | https://getuniqcli.com/learn/taa-compliance-guide-federal-it | FIPS 140-3 与 TAA 相互独立、Section 889 |
| S32 | 通信产业网：2025 年首批安全可靠测评结果 | https://www.ccidcom.com/yaowen/20250319/P4ebJBWzpfcX1fcQg1bnm3m42wjro.html | 测评原则与对象 |
| S33 | 经济观察网：鸿蒙 OS 通过 Ⅱ 级测评 | https://www.eeo.com.cn/2026/0123/782439.shtml | 「首个 Ⅱ 级国产桌面 OS」 |
| S34 | 重庆日报转载：9 款 AI 芯片纳入安全可靠清单 | https://www.cqrb.cn/caijingzonghe/2026-05-29/2684534_pc.html | **含「Ⅰ 级为最高」错误表述，见 09 §8** |
| S35 | FreeBuf：万亿替代浪潮下的安全合规全景 | https://www.freebuf.com/articles/database/493657.html | 法规矩阵、信创安全细分市场（数字需核口径） |
| S36 | 中研网：2026-2030 中国信创云深度研究 | https://m.chinairn.com/hyzx/20260611/092601247.shtml | 一云多芯、信创云产业链 |
| S37 | 经济观察网/腾讯新闻：2026 年第 1 号公告报道 | https://view.inews.qq.com/a/20260116A07MXF00 | 操作系统测评结果 |

### G.3 C 级（行业媒体 / 聚合报告 / 厂商稿，仅作线索）

| 编号 | 来源 | URL | 用途 |
|---|---|---|---|
| S38 | 三个皮匠报告：赛迪顾问 2025 中国信创产业发展报告（聚合） | https://www.sgpjbg.com.cn/searchtag/26699457.html | 国产化率一览表（口径混杂，需回溯原报告） |
| S39 | 三个皮匠报告：中国信通院信创产业白皮书（聚合） | https://www.sgpjbg.com.cn/searchtag/26695317.html | 2.3 万亿、硬件 68%→52%、人才缺口 |
| S40 | 三个皮匠报告：中国电子工业标准化技术协会信创图谱 | https://www.sgpjbg.com/searchtag/27135561.html | CPU 份额、数据库分行业替换率 |
| S41 | 三个皮匠报告：信创（市场规模多口径汇总） | https://m.sgpjbg.com.cn/news/6820087.html | 1.2/1.5/2/2.3/2.8/3 万亿口径对照 |
| S42 | 三个皮匠报告：国产信创产业现状 | https://www.sgpjbg.com/searchtag/26303573.html | **「核心准入目录」讹误来源之一**，见 09 §8 |
| S43 | 三个皮匠报告：中国平台软件市场研究年度报告 | https://www.sgpjbg.com/searchtag/27209526.html | OS/中间件/数据库份额 |
| S44 | 三个皮匠报告：信创人才需求白皮书 2026 | https://www.sgpjbg.com.cn/searchtag/27138023.html | 人才缺口、师资、承载城市 |
| S45 | 三个皮匠报告：2026 数据库国产化替代白皮书 | https://www.sgpjbg.com/labels/shujukuguochanhuatidai.html | 行业案例与性能数据 |
| S46 | 中软泰和：国产数据库选型观察（案例清单） | http://css-th.com/insights/domestic-database-selection-2026 | 20 个金融/运营商/政务案例 |
| S47 | 电科金仓：Kingbase FlySync 双轨并行实践 | https://www.kingbase.com.cn/KingbaseFlySync/tech-blog/ | 医院 HIS 双轨迁移细节 |
| S48 | 电科金仓：金仓替代 Oracle 信贷平台案例 | https://kingbase.com.cn/archives/xejJy4mX2rJy | Oracle 兼容与信贷核心迁移 |
| S49 | HIT 专家网：河科大一附院双模式并行 | https://www.hit180.com/?p=73916 | 迁移五步法、5TB 数据、三阶段切换 |
| S50 | 不舍昼夜技术：稀土高新区信创迁移适配实录 | https://www.xiandedanteng.com/4852.html | 四步法、双库并行、慢 SQL 重调 |
| S51 | 全美网络：信创国产化适配改造全链路 | https://www.kelede.com/news/guochanhua/858.html | 六层适配、代码适配问题清单 |
| S52 | 墨滴：Java 项目如何做信创改造 | https://mdnice.com/writing/c96cc4e34e684edea547c65b4b7df7f3 | JDK/GC/字符集、数据库方言工时 |
| S53 | CSDN：Java 项目信创改造全流程 | https://bbs.csdn.net/weixin_33226548/article/details/100416209 | 国产 JDK 选型、JCE 策略、SecureRandom |
| S54 | CSDN：Spring Boot 项目信创国产化适配指南 | https://blog.csdn.net/huangyourself/article/details/146986135 | 替换点清单 |
| S55 | 灾备联盟信创工作委员会：三类证书区别 | https://www.xcpc.org.cn/news/detail?id=78 | 适配/互认/产品认证证书辨析 |
| S56 | 等保测评网：密评和等保要一起做吗 | https://www.dengbaoceping.net.cn/news/1078.html | 《密码法》27 条、《商密条例》42 条衔接 |
| S57 | 等保测评网：信创产品认证问答（2026） | https://www.dengbaoceping.net.cn/list2/2026/0427/1005.html | 认证流程、周期、证书差异 |
| S58 | 福建省信创适配中心：834 号令落地与软件供应链 | http://www.fjxcsp.cn/contents/7/103.html | 开源依赖、SBOM、SCA/SAST/DAST |
| S59 | 电子工程专辑：46 号令落地 信创告别套壳 | https://www.eet-china.com/mp/a516019.html | **「伪国产首要追责」误传来源**，见 09 §8 |
| S60 | 电子工程专辑：竞争性国企不宜强制信创 | https://www.eet-china.com/mp/a531992.html | 批判性视角（观点） |
| S61 | TrueSight：信创验收现场被掩盖的真相 | https://tsight.io/articles/19682135?lang=zh | 三大死穴（自查框架） |
| S62 | 中国工业新闻网：信创工控深水场景 | https://www.cinn.cn/hz/2026/08-11/71eBwLJr.html | 工控全栈国产、BOM 溯源 |
| S63 | 中国工业新闻网：芯片业卡脖子难题 | https://www.cinn.cn/caijing/2026/08-19/Nk07vE4D.html | EDA、光刻、人才缺口 |
| S64 | NSTL：「十五五」科技自立自强短板研究 | http://dtjc.gdinfo.net/dynamic/recordShow/19552740/203/MzI3MTkwMzM0Nw== | 半导体设备/材料/工业软件国产化率 |
| S65 | 天翼云：一云多芯技术解析 | https://www.ctyun.cn/developer/article/759226141229125 | 动态资源感知、标准化接口 |
| S66 | 中国经济新闻网：达梦一体机与中银保险案例 | https://www.cet.com.cn/wzsy/kjzx/10358453.shtml | 金融保险案例 |
| S67 | 中国日报网：金蝶信创替代实践 | https://cnews.chinadaily.com.cn/a/202410/25/WS671b279ea310b59111d9fda4.html | 大型企业国产化替代计数 |
| S68 | 中国供销合作网：扬中农商银行 OA 全栈改造 | https://www.chinacoop.gov.cn/news.html?aid=1882457 | OA 全栈改造案例 |
| S69 | 太平洋科技 / CSDN：国产 CPU 路线对比 | https://g.pconline.com.cn/best/guide/90205.html 、https://blog.csdn.net/qq_22473611/article/details/128025320 | **后者含 LoongArch/SW64 归属错误**，见 09 §8 |
| S70 | cnBeta：7 颗龙芯获 Ⅱ 级 | https://www.cnbeta.com.tw/articles/tech/1526614.htm | Ⅱ 级为最高等级的表述 |

---

## H. 证据分级与数据使用守则

详见 [README §四](./README.md)。此处补充三条引用格式：

**政策引用格式**
> 《文件全称》（文号），发布机关，成文 YYYY-MM-DD，施行 YYYY-MM-DD，条款号，来源 URL。

**测评公告引用格式**
> 《安全可靠测评结果公告（YYYY 年第 N 号）》，中国信息安全测评中心、国家保密科技测评中心，YYYY-MM-DD，附表 X，产品名 + 版本 + 等级，有效期至 YYYY-MM-DD 前后，来源 URL。

**市场数据引用格式**
> 数字 + 口径定义 + 时点 + 实绩/预测 + 机构《报告全名》（年份）+ 证据等级；若为转引，须标注「转引自」。

**禁止事项**：

1. 不得跨口径数字计算增速、份额或 CAGR。
2. 不得把预测值表述为实绩。
3. 不得把未公开全文的内部文件（如 79 号文）表述为法定义务。
4. 不得引用 [09 §8](./09-风险挑战与批判性视角.md) 中已判定为错误的说法。
5. 不得把自媒体对 Ⅰ/Ⅱ 级、等保级别的类比写入招标文件或合规结论。

---

## I. 文档清单与更新记录

| 文件 | 主题 |
|---|---|
| README.md | 总纲、核心结论、证据规则 |
| 01-概念边界与战略逻辑.md | 定义、概念族、三层内涵、八视角、四组张力 |
| 02-政策脉络与法规体系.md | 时间轴、34 号文逐条拆解、834 号令、46 号令、79 号文引用规范 |
| 03-产业链全景与技术栈.md | 四层/六层模型、图谱、国产化率口径表、上游约束 |
| 04-核心硬件与算力底座.md | 六条 CPU 路线、AI 芯片、整机固件、半导体上游、RISC-V |
| 05-基础软件与平台软件.md | OS、数据库、中间件、云、办公、JDK 工具链 |
| 06-安全合规与测评认证体系.md | 四套体系对照、等保/密评、测评公告全批次、误传辨析 |
| 07-行业落地与工程迁移方法论.md | 行业进度、案例库、六阶段门禁、Java/Spring Boot 专项 |
| 08-产业经济与生态格局.md | 市场规模口径大表、驱动力、集群人才、TCO、国际比较 |
| 09-风险挑战与批判性视角.md | 七类风险、三组正反论点、14 条误传辨析汇总 |
| 10-趋势展望与决策建议.md | 五个趋势、三情景、分角色建议、90 天计划 |
| APPENDIX-参考资料与术语表.md | 本文件 |

| 日期 | 版本 | 说明 |
|---|---|---|
| 2026-11-05 | v1.0 | 首次成稿。8 轮定向检索、6 份一手政策/公告原文核验、70 条来源索引、14 条误传辨析 |
