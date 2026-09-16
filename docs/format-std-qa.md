# 标准 QA 章节格式规则（format-std-qa.md）

适用对象：**chapter-01 ~ chapter-15**，共 15 个「标准 QA」章节。这些章节共用同一套页面骨架与 `qa-card` 卡片格式，改动与新增必须保持一致。

---

## 1. 适用章节与规模

| 章节 | 主题 | 卡片数 | 章节 | 主题 | 卡片数 |
|------|------|-------:|------|------|-------:|
| 01 | JVM 内存与类加载 | 11 | 09 | 分布式系统 | 16 |
| 02 | GC 算法与性能调优 | 12 | 10 | 微服务与云原生 | 27 |
| 03 | 并发与锁 | 12 | 11 | 中间件工程化 | 23 |
| 04 | 线程池与虚拟线程 | 10 | 12 | AI 工程化 | 31 |
| 05 | Spring 核心 | 11 | 13 | 网络与 IO | 13 |
| 06 | Spring Boot 现代化 | 13 | 14 | 数据库扩展 | 9 |
| 07 | MySQL 深入 | 15 | 15 | 响应式编程 | 6 |
| 08 | Redis 与缓存 | 11 | | **合计** | **220** |

## 2. 页面骨架（固定顺序）

```
<body>
  <div class="page-wrapper">

    <!-- ① 侧边目录 -->
    <aside class="sidebar-toc">
      <h3>本篇目录</h3>
      <ol>
        <li><a href="#C01.01"><span class="toc-number">C01.01</span>题干</a></li>
        … 每题目 1 项，锚点 = 卡片 ID …
      </ol>
    </aside>

    <!-- ② 主体 -->
    <main class="content-main">

      <!-- ③ 顶部章节导航（底部 .chapter-nav 内侧须与此完全一致） -->
      <nav class="chapter-nav-top">
        <a href="chapter-NN-prev.html" class="nav-prev">← 第 NN 篇 …</a>
        <!-- 首篇可用：<a href="index.html" class="nav-home">← 返回目录</a> -->
        <span class="nav-center"><a href="chapter-core-methodology.html" class="nav-mind">核心方法论 &#8599;</a><a href="index.html" class="nav-mind">全部章节 &#8599;</a><a href="../java-architect-interview-mind/mind-NN-….html" class="nav-mind">查看本章思维导图 &#8599;</a></span>
        <a href="chapter-NN-next.html" class="nav-next">第 NN 篇 … →</a>
      </nav>

      <!-- ④ 章节头部 -->
      <div class="chapter-header">
        <div class="chapter-number">CHAPTER NN / TOPIC WORDS</div>
        <h1 class="chapter-title">主标题</h1>
        <p class="chapter-subtitle">钩子副题（约一两句；禁止「演进罗列：直击考点」句式）</p>
        <div class="chapter-meta">
          <span>题目数：N</span> <span class="meta-divider">|</span>
          <span>高级 ×a</span> <span class="meta-divider">|</span>
          <span>架构 ×b</span>   <span class="meta-divider">|</span>
          <span>专家 ×c</span>   <span class="meta-divider">|</span>
          <span>预计复习：XX 分钟</span>
        </div>
        <!-- 篇章导读：知识链（含阶段说明）+ 工程化要点 + 本篇思维模式 -->
        <div class="chapter-lead">
          <div class="chapter-lead-block">
            <div class="chapter-lead-label">核心知识链</div>
            <div class="chapter-lead-chain">
            <p>一句话主线。</p>
            <ol>
              <li><strong>阶段名</strong>：为何存在、解决什么。</li>
            </ol>
            </div>
          </div>
          <div class="chapter-lead-block">
            <div class="chapter-lead-label">工程化要点</div>
            <ul class="chapter-lead-points">
              <li>大厂生产视角的发布 / 观测 / 回滚 / 门禁口径（分点）。</li>
            </ul>
          </div>
          <div class="chapter-lead-block">
            <div class="chapter-lead-label">本篇思维模式</div>
            <ul class="chapter-lead-mind">
              <li><strong>模式名</strong>：本领域落地口径（勿重复粘贴跨篇通用句；通用方法论见导航「核心方法论」）。</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- ⑤ 正文：qa-card 序列 -->
      <div class="qa-card" id="C01.01" data-difficulty="…" data-priority="p…">
        …（见下）…
      </div>
      …

      <!-- ⑥ 参考资料 -->
      <h2 id="references">参考资料</h2>

    </main>
  </div>
  <script src="assets/nav.js"></script>
</body>
```

要点：
- 每章**正文几乎不使用 `h2/h3` 分隔**（正文以 `qa-card` 为唯一单元，通常仅侧栏 `h3 本篇目录` 与末尾 `h2 参考资料` 两个标题）。
- `chapter-header` 的难度分布（`×a/×b/×c`）必须与下方各卡片的 `data-difficulty` 统计一致；`题目数：N` 必须等于 `qa-card` 数量。
- `chapter-subtitle` 只做钩子；**核心知识链（含阶段说明）+ 工程化要点（分点）+ 本篇思维模式** 放在 `chapter-lead`（每章恰好一处）。知识链要对齐 mind ①②③ 并写清因果，禁止只剩箭头关键词；工程化要点用 `<ul class="chapter-lead-points">`，建议 **7～8 条**，每条写清发布/观测/回滚/门禁/容量等可执行口径，忌口号化短句；思维模式用命名条目（`<strong>模式名</strong>：口径`），建议 **6 条**，写本领域落地口径，禁止每章复制同一句「见方法论」。顶部/底部导航须同文（详见 `format-shared.md` §4.2）：箭头用字面量 `←`/`→`；`nav-center` 顺序固定为 **核心方法论 → 全部章节 → 本章思维导图**。

## 3. `qa-card` 卡片规范

### 3.1 卡片根节点

```html
<div class="qa-card" id="C01.01" data-difficulty="senior|expert|architect" data-priority="p0|p1|p2">
```

- `id`：`C{章}.{序}`；`data-difficulty` / `data-priority` 供全局检索 / 统计。
- 不携带的功能性样式写在属性里，视觉标签放提问行（见 3.3）。

### 3.2 卡片头部

```html
<div class="qa-header">
  <div class="qa-badge">C01.01</div>
  <div class="qa-question">题干<span class="difficulty difficulty-senior">高级</span><span class="priority priority-p0">P0</span></div>
</div>
```

- **难度标签文案 = 短表 `专家 / 架构 / 高级`**（2026-09-16 长官决策）；正文表述用 `专家 / 架构师 / 高级开发`。门禁 `validate_kb.py` 1j。
- **M/G/K 三专篇不参与难度分级（2026-09-16 长官决策）**：方法论 / 工程化要点 / 生产踩坑页的 `.qa-card` **不写 `data-difficulty`**（原 220 处已全清），`.qa-question` 也不写任何等级、优先级徽标，只留题干文本；`data-priority` 仍保留（M 卡部分携带，不呈现）。
  - **视觉影响**：`design-system.css` 有 `.qa-card[data-difficulty="architect"]`（紫左边框 + 紫 `qa-badge`）与 `["expert"]`（青绿左边框 + 青绿 `qa-badge`，2026-09-16 晚由「蓝→紫渐变」改定）属性选择器，故 M/G/K 220 张卡由「按难度变色」回落为 `.qa-card` 默认蓝色左边框——这是「取消分级」的预期结果。同步口径见 `conventions.md` §2。
- **难度配色（2026-09-16 晚修订）**：`senior` 蓝 / `architect` 紫 / `expert` **青绿**（`--diff-expert`），卡片边框与 `qa-badge` 底色用 `--diff-expert-solid`；改前 `expert` 与 `architect` 文字色同为 `var(--accent2)`，区分度不足。难度胶囊与优先级胶囊同框，色相须避开 `P0` 红 / `P1` 琥珀 / `P2` 蓝。

### 3.3 内容层（layer）

每层结构统一为：

```html
<div class="qa-layer" data-layer="essence">
  <div class="qa-layer-title">本质问题</div>
  <div class="qa-layer-body">…段落 / 表格 / 代码…</div>
</div>
```

**6 个核心层（每张卡片必须全）、固定顺序：**

| data-layer | 层标题 | 内容职责 |
|-----------|--------|----------|
| `essence` | 本质问题 | 一针见血指出考点 / 认知地基 |
| `evolution` | 演进脉络 | 版本 / 方案演进线与关键节点 |
| `principle` | 第一性原理 | 底层原理与归约 |
| `practice` | 工程实践 | 落地做法、参数、示例 |
| `deep` | 深度追问 | 需要进一步挖掘的次级问题 |
| `pitfall` | 常见陷阱 | 易错点 / 反面清单 |

**可选层（非每卡必有）：**

| data-layer | 层标题 | 说明 |
|-----------|--------|------|
| `extension` | 扩展补全 | 延伸知识补全，可有可无 |
| `production` | 生产量化证据（压测 / 命中率 / 容量） | 仅部分章节 / 部分卡片出现，给出可量化工程证据 |

> 使用分布参考：`essence / evolution / principle / practice / deep / pitfall` 全站均等（= 卡片数）；`extension`、`production` 为补充层，各章数量不一。所有层平铺可见（无 tab 折叠），阅读顺序即 DOM 顺序。

## 4. 图表与代码

- Mermaid 图：仅在需要的卡片内嵌入；对应页头部或底部引入 `shared/js/mermaid.min.js` 并初始化。
- 表格：统一 `<table class="compare-table">`（详见 `format-shared.md` 第 5 节）；禁止裸 `<table>`。
- 行内代码：`<code class="inline-code">`；参数名 / 关键字使用等宽强调。
- 代码块：`<pre><code>` 内的 `<` / `>` 必须转义为 `&lt;` / `&gt;`（泛型、比较符、注解等），见 `format-shared.md` 第 7 节。

## 5. 新增 / 修改自检清单

1. 新题 → 新增 `qa-card`，同时在侧栏 `sidebar-toc`、`chapter-header` 的 `题目数 / 难度分布` 里同步数字。
2. 卡片 `id`、`data-difficulty`、`data-priority` 与提问行的视觉标签三者必须一致。
3. 6 个核心层顺序不可乱；`extension / production` 为可选项。
4. 更新首页 / 大盘页对该题锚点的引用（`../../index.html`、`nav-overview-priority.html`）。
5. 含图卡片才引入 mermaid；数字 / 括号 / 颜色须符合 `format-shared.md` 第 7 节转义铁律。
6. 若改动顶/底导航：保证 `chapter-nav-top` 与 `chapter-nav` 内侧同文（`format-shared.md` §4.2）。
