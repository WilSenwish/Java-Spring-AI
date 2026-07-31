# 场景题扩充 S41-S55 实施计划

## Summary

为 `scenario-questions.html` 新增 15 道场景题（S41~S55）：两个全新分组（十、网络与IO架构 5题；十一、搜索引擎与大数据 5题），以及 5 道补充题分散插入现有分组（S51→高并发、S52→分布式、S53→微服务、S54→性能、S55→综合）。同步更新侧边栏 TOC 与头部统计（40题→55题，9类→11类）。

## Current State Analysis

### 已有资产
- `scenario-questions.html`：现有 9 个分组 40 题，约 5120 行，末尾为 `group-9`（安全架构）+ `chapter-nav`
- `patch_scenario.py`：已完成编写，包含全部插入逻辑（TOC、header stats、group counts、补充题、新组），等待 s43~s55 的 snippet 文件就位后即可执行
- `s41.html`、`s42.html`：已完成（百万级长连接IM网关、实时音视频信令系统）
- `s43.html` ~ `s55.html`：**尚未创建**，需按 plan doc 3.3 补齐

### 题目清单（plan doc 3.3）
| 编号 | 分组 | 难度 | 标题 | 技术栈 |
|------|------|------|------|--------|
| S41 | 十-网络IO | 架 | 百万级长连接IM网关设计 | Netty + WebSocket + 心跳 + 分布式路由 |
| S42 | 十-网络IO | 架 | 实时音视频信令与媒体转发系统 | WebSocket + UDP + QoS + 全球加速 |
| S43 | 十-网络IO | 高 | 大文件分片上传与断点续传 | HTTP/HTTPS + 分片 + 秒传 + 合并 |
| S44 | 十-网络IO | 高 | DNS故障排查与HTTPDNS落地 | DNS + HTTPDNS + CDN + 智能调度 |
| S45 | 十-网络IO | 架 | 全站HTTPS迁移与性能优化 | TLS 1.3 + OCSP + HSTS + 证书管理 |
| S46 | 十一-搜索大数据 | 架 | 亿级商品搜索系统设计 | ES + Redis + 分词 + 聚合 + 推荐 |
| S47 | 十一-搜索大数据 | 架 | 日志采集与ELK实时分析架构 | Filebeat + Logstash + ES + Kibana |
| S48 | 十一-搜索大数据 | 高 | 海量数据实时聚合统计 | ClickHouse/ES + 预聚合 + 物化视图 |
| S49 | 十一-搜索大数据 | 架 | 个性化推荐系统架构 | 召回 + 排序 + 特征工程 + AB测试 |
| S50 | 十一-搜索大数据 | 架 | 数据仓库与实时数仓选型 | Hive/ClickHouse/Flink + 离线/实时链路 |
| S51 | 一-高并发（补充） | 专 | 12306高并发抢票系统设计 | 库存分桶 + 异步队列 + 限流 + 降级 |
| S52 | 二-分布式（补充） | 架 | 分布式任务调度平台设计 | XXL-Job/ElasticJob + 分片 + 故障转移 |
| S53 | 四-微服务（补充） | 架 | 多租户SaaS平台架构设计 | 数据隔离 + 配置隔离 + 资源配额 + 灰度 |
| S54 | 五-性能（补充） | 架 | 全链路压测与容量规划 | 影子库 + 流量复制 + 瓶颈定位 + 扩缩容 |
| S55 | 七-综合（补充） | 架 | 开放平台API网关与安全设计 | OAuth2 + 限流 + 签名 + 审计 + SDK |

## Proposed Changes

### 步骤1：创建 s43.html ~ s55.html（13个snippet文件）

**位置**：`/Users/chenjunbing/.trae-cn/work/6a6b7240026c2863e26bac90/`

每道题严格遵循现有七层结构：
```html
<div class="qa-card" id="sXX" data-difficulty="...">
  <div class="qa-header">...</div>
  <div class="scenario-tags">...</div>
  <div class="qa-layer" data-layer="scenario">场景背景</div>
  <div class="qa-layer" data-layer="challenge">核心挑战</div>
  <div class="qa-layer" data-layer="principle">分析框架</div>
  <div class="qa-layer" data-layer="practice">解决方案（含对比表格）</div>
  <div class="qa-layer" data-layer="practice">关键代码（.code-block）</div>
  <div class="qa-layer" data-layer="deep">深度追问（ul.followup-list）</div>
  <div class="qa-layer" data-layer="pitfall">常见陷阱（ul.pitfall-list）</div>
</div>
```

内容要点依据 plan doc 3.3 的技术栈标签展开，每题 600~1000 字，代码片段 20~40 行。

### 步骤2：执行 patch_scenario.py 更新 scenario-questions.html

**目标文件**：`/Users/chenjunbing/Develop/Project/Personal/Java Spring AI/java-architect-interview/scenario-questions.html`

脚本自动完成以下替换/插入：
1. **Sidebar TOC**：在 group-9 后追加 group-10、group-11 的 TOC 分组
2. **Header Stats**：40题→55题，高级15→17，架构19→32，专家5→6，9类→11类
3. **Group Counts**：group-1（5→6）、group-2（5→6）、group-4（4→5）、group-5（4→5）、group-7（4→5）
4. **补充题插入**：S51 插入 group-1 末尾、S52→group-2、S53→group-4、S54→group-5、S55→group-7
5. **新组插入**：在 group-9 后、`chapter-nav` 前插入 group-10（S41-S45）和 group-11（S46-S50）

### 步骤3：更新 index.html 统计数字

将首页 Hero 区场景题统计从 40 更新为 55。

## Assumptions & Decisions

1. **复用现有设计系统**：不修改 `design-system.css`，所有样式复用已有类（qa-card、qa-layer、code-block、compare-table 等）
2. **Snippet 策略**：每道题保存为独立 HTML snippet，由 patch 脚本读取并插入，避免单文件过大导致编辑困难
3. **不新增 Mermaid 图**：本批次 15 题不新增 Mermaid 图表，保持页面加载性能
4. **难度标签对齐**：高级=蓝、架构级=紫、专家级=渐变，与现有 40 题保持一致
5. **最小改动原则**：仅修改 scenario-questions.html 和 index.html，不触及已有 12 章 Q&A 和其他文件

## Verification Steps

1. **脚本执行**：运行 `python3 patch_scenario.py`，确认所有 print 输出均为成功状态（无 WARNING/ERROR）
2. **HTML 结构检查**：grep 统计 `qa-card` 数量应为 55；`scenario-group` 数量应为 11
3. **TOC 完整性**：确认 sidebar 包含 group-10、group-11 及其下 10 道题的链接
4. **Header 统计**：确认页面头部显示"题目数：55"、"11 大场景类别"
5. **补充题位置**：确认 S51 在 group-1 内、S52 在 group-2 内、S53 在 group-4 内、S54 在 group-5 内、S55 在 group-7 内
6. **新组位置**：确认 group-10、group-11 位于 group-9 之后、chapter-nav 之前
7. **index.html**：确认首页场景题统计已更新为 55
8. **浏览器验证**：打开文件确认无控制台报错、卡片渲染正常、TOC 跳转正确
