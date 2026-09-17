#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
java-kb-expand · 全量校验脚本（通用版）
==============================================
运行位置：**本文件（`.workbuddy/skills/java-kb-expand/scripts/validate_kb.py`）原地运行**
（项目根由「向上查找同时含 AGENTS.md + index.html 的祖先目录」推导，路径全部绝对化）。
**勿再复制到 `tmp/` 运行**——曾因 tmp 副本按自身层级推导，把 BASE 解析成
`<项目根>/java-architect-interview`，报出 `docs/kb-counts.json 不存在` 之类假故障
（2026-09-16 实测）。按需填 EXPECT 字典（本轮权威计数）与 NEW_IDS（新增/改动题号列表），
然后运行：python3 validate_kb.py

校验项：
  0) **散文/SSOT 计数位**：子进程调用 sync_counts.py check（含 P01–P89，防页头「本页 N 道」漂移）
  0b) **计数标记**：每个 position 须含 `data-kb-pos="Pxx"`（ov_series=P07×len(ov_stat_order)）；场景 `group-count` / 根 `dir-group` 抽检 `data-kb-count-local`
  0c) **L1 聚合 UI**：页头/footer/desc/meta/subtitle/map-note/tagline/stat 等容器内「N题|卡|道|组」不得裸数字（见 conventions §5.1.4）
  0d) **页头难度分布**：chapter-meta 的「题目数 / 高级×N / 架构×N / 专家×N」须与本页实体卡片逐项一致（2026-09-15 补，防新增卡漏同步页头）
  1) 全部目标 HTML 文件 data-page-node-id 全 0（红线）
  1b) 手机小屏强制：design-system.css / 根·导图 index / 导图页含 MOBILE-MANDATORY；全站 HTML 含 viewport
  1c) 主题 / 暗黑模式：站点 HTML 含 theme-init.js；design-system.css 含 data-theme="dark" 令牌块
  1d) Mermaid：每个 class="mermaid" 上一行 prettier-ignore；图源码未塌缩（换行≥2）
  1e) 顶/底导航壳：根/章节 index 无导航；其余页 top 贴 body 首、bottom 在 script 前
  1f) **内部编辑字眼**：卡片正文不得出现「再加厚/补厚/占位段落/待补写」（2026-09-15 补，实测曾残留 15 处）
  1g) **横向溢出兜底**：design-system.css 含全局 `body{overflow-wrap:anywhere}` + 裸 `pre{overflow-x:auto}`；
      且全站不得存在未被 .code-block 包裹的裸 <pre>（2026-09-15 补，实测核心原理页 375px 溢出 248px/18 处）
  1h) **列表缩进兜底**：design-system.css 须含零特异度 `:where(ul,ol){padding-inline-start:1.25rem}`（reset 抹掉了
      ul/ol 默认缩进，无类规则的列表圆点/数字会画到内容盒外、贴边甚至越出卡片），且不得退化成裸 `ul, ol {…}`
      （2026-09-16 补，实测核心原理页 20 处、安全检查页 1 处）
  1i) **卡片嵌套**：任一 `qa-card` / `map-card` 不得被另一张卡包含（= 前一张卡缺 `</div>`；渲染为卡片套卡片）
      （2026-09-16 补，实测 chapter-11 的 C11.28 缺 1 个 `</div>`，C11.29/C11.30 被吞进去，当时全部门禁 PASS）
  1j) **难度标签口径**：全站 `<span class="difficulty difficulty-X">TEXT</span>` 的 TEXT 必须等于短表
      {expert:专家, architect:架构, senior:高级}（可带 ` ×N`）；禁止非难度语义占用 difficulty 类
      （2026-09-16 补，实测根 index 48 个导图节点把「想/做/守」写成 difficulty-architect）
  1k) **M/G/K 无难度分级**：三个专篇页（方法论/工程化/生产踩坑）不得出现 `data-difficulty`
      （2026-09-16 长官决策：彻底取消 M/G/K 难度分级，counts 键与不变式一并移除）
  2) 无 </spa(?!n>) 标签截断残留
  3) overview ov-stat-num 三源一致（项数=ov_stat_order：总量/优先级/难度/类型；不含 M/G/K）
  3b) overview 子组内排序：C→E→S 且题号升序；item 的 priority/difficulty 与所在组一致；子组标题题数=实际 ov-item 数
  3b2) overview 类型三级：每难度子组须拆 `ov-type`（篇章/核心原理/场景题），`ov-type-count`=块内 ov-item 且前缀一致
  3c) 全站分组/页头页尾：场景 section 无孤儿 S 卡且 group-count=卡数；根 index dir-group/dir-count=q-item；mind card-foot=篇章C/summary E·S
  4) 根 index / 章节 index 统计数字与 overview 一致
  5) 新卡双编码一致（data-priority 属性 + 可见 priority-pX 徽标）
  6) 新卡在 overview / 根 index / 宿主章节页 / 对应 mind 页落位

设计要点（来自实战坑位）：
  - 章节导航页（java-architect-interview/index.html）不枚举单题 ID，落位检查跳过它。
  - 宿主章节页按题号前缀自动扫描：Cxx/Sxx/Mxx -> 其所在 chapter-*.html（grep 全站定位，不写死文件）。
  - 导图落位扫描全部 mind-*.html，命中任一即 PASS。
  - 文件夹路径如有变动，仅改 BASE 一处即可。
"""
import re, sys, os, glob, json
from html.parser import HTMLParser

BASE = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI"
CHAPTER_DIR = f"{BASE}/java-architect-interview"
MIND_DIR = f"{BASE}/java-architect-interview-mind"
# 2026-09-15：docs/ 已由 java-architect-interview/docs 迁至项目根 docs/，
# 此处写死旧路径会导致脚本启动即 FileNotFoundError（全量校验护栏失效）。优先新路径，兼容旧布局。
COUNTS_JSON = f"{BASE}/docs/kb-counts.json"
if not os.path.isfile(COUNTS_JSON):
    COUNTS_JSON = f"{CHAPTER_DIR}/docs/kb-counts.json"

# 面向读者的卡片正文里禁止出现的内部编辑字眼（占位/批注词）
# 2026-09-15 实测：「再加厚：」曾残留在 10 个章节页 / 15 处，且无校验可拦，故纳入硬门禁
EDITORIAL_WORDS = ["再加厚", "补厚", "占位段落", "待补写"]
if not os.path.isfile(COUNTS_JSON):
    raise SystemExit(f"[FATAL] 未找到 kb-counts.json，已尝试：{BASE}/docs/ 与 {CHAPTER_DIR}/docs/")

# ====== 权威计数：单一真源 kb-counts.json（禁止硬编码，改数用 sync_counts.py bump）======
_cfg = json.load(open(COUNTS_JSON, encoding="utf-8"))
EXPECT = {k: _cfg["counts"][k] for k in
          ("total", "p0", "p1", "p2", "expert", "architect", "senior",
           "methodology", "chapters", "basics", "scenarios")}
# 跨大篇章/聚合口径仅 total=篇章+原理+场景；M/G/K 单独计数，不设全站合计
ENGINEERING = _cfg["counts"].get("engineering", 0)
PITFALLS = _cfg["counts"].get("pitfalls", 0)
# 内部一致性：章节站卡片 id 总数（不对外展示为「全站合计」）
CARDS_IN_CHAPTERS = EXPECT["total"] + EXPECT["methodology"] + ENGINEERING + PITFALLS

# ====== 待填：本轮新增/改动题号（用于落位+双编码校验）======
# 注意：方法论/工程化卡默认不进 overview；含 M/G 时跳过 overview 落位检查
NEW_IDS = ["C06.15","C07.16","C08.12","C09.17","C10.29","C10.30","C11.26","C11.27","C11.28","C11.29","C11.30","C12.33","C12.34","C12.35","C13.14","C14.13","C15.12","G01.04","G02.04","G03.04","G04.04","G05.04","G06.04","G07.04","G07.09","G08.04","K01.01","K01.02","K02.01","K02.02","K03.01","K03.02","K04.01","K04.02","K05.01","K05.02","K06.01","K06.02","K07.01","K07.02","K08.01","K08.02","S12.09","M01.08","M01.09","M01.10"]

# 4 份聚合页（固定路径）。注意：BASE 已含项目根 "Java Spring AI"，根 index 即 {BASE}/index.html
AGG_FILES = {
    "overview": f"{CHAPTER_DIR}/nav-overview-priority.html",
    "root":     f"{BASE}/index.html",
    "chap_idx": f"{CHAPTER_DIR}/index.html",
    "mind_idx": f"{MIND_DIR}/index.html",
}

def read(p): return open(p, encoding="utf-8").read()

def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        check.failed += 1
check.failed = 0

def all_chapter_files():
    fs = []
    for p in glob.glob(f"{CHAPTER_DIR}/chapter-*.html"):
        b = os.path.basename(p)
        if b in ("index.html", "nav-overview-priority.html"):
            continue
        fs.append(p)
    return fs

def all_mind_files():
    return [p for p in glob.glob(f"{MIND_DIR}/mind-*.html")
            if os.path.basename(p) != "index.html"]

def run_sync_counts_check():
    """散文计数位（P01–P89）与全部 positions 必须与 kb-counts.json 一致。
    改数入口：sync_counts.py bump/apply；禁止只改 HTML 散文数字。
    """
    script = os.path.join(os.path.dirname(__file__), "sync_counts.py")
    if not os.path.isfile(script):
        check(False, f"[散文计数] 未找到 sync_counts.py: {script}")
        return
    import subprocess
    r = subprocess.run(
        [sys.executable, script, "check"],
        cwd=BASE,
        capture_output=True,
        text=True,
    )
    out = (r.stdout or "") + (r.stderr or "")
    # 抽出 FAIL 行；无 FAIL 且 exit 0 则 PASS
    fails = [ln for ln in out.splitlines() if ln.startswith("FAIL ")]
    if r.returncode == 0 and not fails:
        check(True, "[散文计数/SSOT] sync_counts.py check 全部通过（含 P01–P89）")
    else:
        for ln in fails[:12]:
            print(ln)
        check(False, f"[散文计数/SSOT] sync_counts.py check 失败 exit={r.returncode} fail行={len(fails)}")


def run_chapter_meta_difficulty_check():
    """页头 chapter-meta 的「题目数 / 高级×N / 架构×N / 专家×N」必须与本页实体卡片一致。

    背景（2026-09-15 独立审查发现）：12 个页面的页头难度分布未随新增卡同步——
    新增 22 张篇章卡后，页头 `高级开发 ×N` 全部停留在旧值；S 页页头「题目数：71」实际 73。
    根因是 `chapter-01~15` 未纳入 SSOT positions（data-kb-pos 计数为 0），
    故 sync_counts.py check 报 PASS 也无法发现该漂移。此处按「页面自身实体卡片」自证，
    不依赖 SSOT，作为 L1 规则拦截同类漂移复发（对应 format-shared §5.1.4 聚合 UI 禁裸数字）。

    2026-09-16：标签口径改短表（高级 / 架构 / 专家），页头统计随之。
    """
    _diff = re.compile(r'data-difficulty="(senior|architect|expert)"')
    _meta = re.compile(r'<div class="chapter-meta">.*?</div>', re.S)
    _cn = {"senior": "高级", "architect": "架构", "expert": "专家"}
    _n_re = re.compile(r'题目数：\s*(?:<span class="kb-count"[^>]*>)?(\d+)')
    targets = []
    for c in range(1, 16):
        targets += sorted(glob.glob(f"{CHAPTER_DIR}/chapter-{c:02d}-*.html"))
    targets += [f"{CHAPTER_DIR}/chapter-questions-eight-part.html",
                f"{CHAPTER_DIR}/chapter-questions-scenario.html"]
    for p in targets:
        if not os.path.isfile(p):
            continue
        raw = read(p)
        bn = os.path.basename(p)
        m = _meta.search(raw)
        if not m:
            check(False, f"[页头难度] {bn}: 缺少 chapter-meta 容器")
            continue
        block = m.group(0)
        if bn == "chapter-questions-eight-part.html":
            card_pat = r'<div class="[^"]*card[^"]*"\s+id="E\d{2}\.\d{2}"[^>]*>'
        else:
            card_pat = r'<div class="qa-card(?:\s+[^"]*)?"\s+id="[CMES]\d{2}\.\d{2}"[^>]*>'
        cards = re.findall(card_pat, raw)
        cnt = {"senior": 0, "architect": 0, "expert": 0}
        for cm in cards:
            d = _diff.search(cm)
            if d:
                cnt[d.group(1)] += 1
        errs = []
        mn = _n_re.search(block)
        if mn and int(mn.group(1)) != len(cards):
            errs.append(f"题目数 页头{mn.group(1)}≠实测{len(cards)}")
        for k in ("senior", "architect", "expert"):
            h = re.search(r'<span>' + _cn[k] + r' ×(\d+)</span>', block)
            if h and int(h.group(1)) != cnt[k]:
                errs.append(f"{_cn[k]} 页头{h.group(1)}≠实测{cnt[k]}")
        check(not errs,
              f"[页头难度] {bn}: "
              + ("一致 (n=%d 高=%d 架=%d 专=%d)" % (len(cards), cnt["senior"], cnt["architect"], cnt["expert"])
                 if not errs else "；".join(errs)))


def run_kb_count_markup_check():
    """每个 SSOT position 必须带 data-kb-pos；全站禁止 kb-count-local。
    标记约定见 conventions.md §5.1.4。
    """
    cfg = json.load(open(COUNTS_JSON, encoding="utf-8"))
    miss = []
    for pos in cfg["positions"]:
        m = re.match(r"(P\d+)", pos["id"])
        pid = m.group(1) if m else pos["id"]
        path = os.path.join(BASE, pos["file"])
        if not os.path.isfile(path):
            miss.append(f"{pid} 文件缺失 {pos['file']}")
            continue
        t = read(path)
        n = t.count(f'data-kb-pos="{pid}"')
        expect = len(cfg["ov_stat_order"]) if pos.get("kind") == "ov_series" else 1
        if n != expect:
            miss.append(f"{pid} 期望 data-kb-pos×{expect}，实际 {n} @ {pos['file']}")
    # 禁止本地计数（一律升格进 kb-counts.json counts|struct）
    for path in all_chapter_files() + all_mind_files() + [
        os.path.join(BASE, "index.html"),
        os.path.join(BASE, "java-architect-interview/index.html"),
        os.path.join(BASE, "java-architect-interview-mind/index.html"),
        os.path.join(BASE, "java-architect-interview/nav-overview-priority.html"),
        os.path.join(BASE, "java-architect-interview/nav-server-security-checkpoint.html"),
    ]:
        if not os.path.isfile(path):
            continue
        t = read(path)
        if "kb-count-local" in t or "data-kb-count-local" in t:
            miss.append(f"禁止本地计数：{os.path.relpath(path, BASE)}")
        # 禁止口径控制套话（全站 HTML，含 qa-card）
        if "不计入题目总量" in t:
            miss.append(f"禁止文案「不计入题目总量」：{os.path.relpath(path, BASE)}")
    if miss:
        for x in miss[:20]:
            print("FAIL [kb-count标记]", x)
        check(False, f"[kb-count标记] {len(miss)} 处缺失/违规（须 data-kb-pos；禁 local /「不计入」文案）")
    else:
        check(True, f"[kb-count标记] SSOT positions 均含 data-kb-pos（{len(cfg['positions'])} 位）；无 local/禁语文案")


def run_l1_container_scan():
    """L1 聚合 UI 容器内不得出现未标记的「N题|卡|道|组|页|章|张」。
    口径见 conventions.md §5.1.4；排除「第 N 章」标题序号与 P0/P1 文案。
    """
    region_pats = [
        (r'<div class="card-footer">(.*?)</div>', "card-footer"),
        (r'<div class="card-foot">(.*?)</div>', "card-foot"),
        (r'<div class="card-desc">(.*?)</div>', "card-desc"),
        (r'<p class="chapter-subtitle">(.*?)</p>', "chapter-subtitle"),
        (r'<div class="chapter-meta">(.*?)</div>', "chapter-meta"),
        (r'<p class="subtitle">(.*?)</p>', "subtitle"),
        (r'<p class="map-note"[^>]*>(.*?)</p>', "map-note"),
        (r'<p class="ov-subtitle">(.*?)</p>', "ov-subtitle"),
        (r'<span class="tagline">(.*?)</span>', "tagline"),
        (r'<div class="stat-number[^"]*"[^>]*>(.*?)</div>', "stat-number"),
        (r'<tfoot>(.*?)</tfoot>', "tfoot"),
    ]
    digit_unit = re.compile(r"(\d+)\s*(题|卡|组|道|页|章|张)")
    targets = [os.path.join(BASE, "index.html")]
    targets += glob.glob(os.path.join(CHAPTER_DIR, "*.html"))
    targets += glob.glob(os.path.join(MIND_DIR, "*.html"))
    misses = []

    def tagged_at(t, pos):
        w = t[max(0, pos - 180) : pos]
        # 仅承认 L0：data-kb-pos（已废除 kb-count-local）
        if 'data-kb-pos="' in w and w.rfind('data-kb-pos="') > w.rfind("</"):
            return True
        return False

    for path in targets:
        if not os.path.isfile(path):
            continue
        t = read(path)
        rel = os.path.relpath(path, BASE)
        for rpat, rname in region_pats:
            for rm in re.finditer(rpat, t, re.S):
                region = rm.group(1)
                if 'class="mermaid"' in region:
                    continue
                for dm in digit_unit.finditer(region):
                    abs_pos = rm.start(1) + dm.start(1)
                    if tagged_at(t, abs_pos):
                        continue
                    # 「第 N 章」或「第 09/04 章」类章节引用
                    pre = region[max(0, dm.start() - 8) : dm.start()]
                    if dm.group(2) == "章" and ("第" in pre or "/" in pre):
                        continue
                    # 「E12 组」题组名，非「12 组」计数
                    if dm.group(2) == "组" and re.search(
                        r"[CEMSG]\d{0,2}$", region[max(0, dm.start() - 4) : dm.start()]
                    ):
                        continue
                    # P0/P1 文案
                    ctx = region[max(0, dm.start() - 12) : dm.end() + 8]
                    if re.search(r"P0\s*/\s*P1|P0→P2", ctx):
                        continue
                    misses.append(
                        f"{rel} [{rname}] {dm.group(1)}{dm.group(2)}"
                    )
    if misses:
        for x in misses[:20]:
            print("FAIL [L1聚合UI]", x)
        check(False, f"[L1聚合UI] 裸计数 {len(misses)} 处（须 data-kb-pos + kb-counts.json，见 §5.1.4）")
    else:
        check(True, "[L1聚合UI] 页头/footer/desc/meta/note/tagline/stat 无裸「N题|卡|道|组」")


_VOID_TAGS = {"br", "img", "meta", "link", "input", "hr", "area", "base",
              "col", "embed", "source", "track", "wbr"}


def scan_bare_pre(html):
    """扫描 <pre> 是否位于 .code-block 容器内（含 <pre class="code-block"> 自身带类写法）。

    返回 [(字符 offset, inside_code_block: bool)]。
    用途：裸挂 <pre>（未被 .code-block 包裹）既无深色代码块样式、也无 overflow-x: auto，
          长代码行会撑破卡片（2026-09-15 实测 chapter-07 溢出 814px）。
    """
    class _P(HTMLParser):
        def __init__(self, text):
            super().__init__(convert_charrefs=False)
            self.lines = [0]
            for i, ch in enumerate(text):
                if ch == "\n":
                    self.lines.append(i + 1)
            self.stack = []
            self.found = []

        def handle_starttag(self, tag, attrs):
            d = dict(attrs)
            self.stack.append((tag, "code-block" in (d.get("class") or "")))
            if tag == "pre":
                line, col = self.getpos()
                self.found.append(
                    (self.lines[line - 1] + col, any(cb for _, cb in self.stack)))
            if tag in _VOID_TAGS:
                self.stack.pop()

        def handle_endtag(self, tag):
            if tag in _VOID_TAGS:
                return
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break

    p = _P(html)
    p.feed(html)
    return p.found


CARD_CLASSES = ("qa-card", "map-card")


def scan_card_nesting(html):
    """返回被嵌套的卡片 [(id, line, outer_id, outer_line)]。

    判定：解析栈里已存在 `qa-card` / `map-card` 时又开启一张卡 ⇒ 前一张卡缺 `</div>`
    （浏览器渲染为卡片套卡片：后续卡片整块落进上一张卡的框里）。
    背景（2026-09-16 长官实测）：chapter-11 的 C11.28 少一个 `</div>`，C11.29/C11.30
    被吞进 C11.28 内部，而当时 validate_kb 全绿 —— 校验面缺这一类结构缺陷。
    """
    class _P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.stack = []
            self.found = []

        def handle_starttag(self, tag, attrs):
            d = dict(attrs)
            cls = (d.get("class") or "").split()
            if any(c in CARD_CLASSES for c in cls):
                outer = [s for s in self.stack if any(c in CARD_CLASSES for c in s[1])]
                if outer:
                    self.found.append((d.get("id") or "(无 id)", self.getpos()[0],
                                       outer[-1][2] or "(无 id)", outer[-1][3]))
            self.stack.append((tag, cls, d.get("id"), self.getpos()[0]))
            if tag in _VOID_TAGS:
                self.stack.pop()

        def handle_endtag(self, tag):
            if tag in _VOID_TAGS:
                return
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break

    p = _P()
    p.feed(html)
    return p.found


def run_card_nesting_check():
    """1i) 卡片层级：章节/导图页的 qa-card / map-card 不得互相嵌套。"""
    bad, n = [], 0
    for p in all_chapter_files() + all_mind_files():
        bn = os.path.basename(p)
        bad += [(bn,) + x for x in scan_card_nesting(read(p))]
        n += 1
    if bad:
        for x in bad[:20]:
            print("FAIL [卡片嵌套]", f"{x[0]}: {x[1]}@行{x[2]} 被嵌进 {x[3]}@行{x[4]}（缺 </div>）")
        check(False, f"[卡片嵌套] {len(bad)} 张卡被嵌进上一张卡（须 0；见 conventions §2）")
    else:
        check(True, f"[卡片嵌套] {n} 个章节/导图页的卡片层级无嵌套")


# 难度标签唯一合法文案（2026-09-16 长官口径：标签限定为「专家 / 架构 / 高级」）
DIFF_LABEL = {"expert": "专家", "architect": "架构", "senior": "高级"}
# M/G/K 三专篇：彻底取消难度分级
NO_DIFF_PAGES = ("chapter-core-methodology.html",
                 "chapter-engineering-practices.html",
                 "chapter-production-pitfalls.html")


def run_difficulty_label_check():
    """1j) 全站 difficulty 徽标文案必须是短表；difficulty 类不得被非难度语义占用。"""
    pat = re.compile(r'<span class="difficulty difficulty-(expert|architect|senior)">(.*?)</span>',
                     re.S)
    files = ([os.path.join(BASE, "index.html")]
             + sorted(glob.glob(f"{CHAPTER_DIR}/*.html"))
             + sorted(glob.glob(f"{MIND_DIR}/*.html")))
    bad, total = [], 0
    for p in files:
        s = read(p)
        for m in re.finditer(r'<span class="difficulty difficulty-([A-Za-z-]+)">(.*?)</span>',
                             s, re.S):
            total += 1
            cls, inner = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
            exp = DIFF_LABEL.get(cls)
            ok = exp is not None and re.fullmatch(re.escape(exp) + r"( ×\d+)?", inner)
            if not ok:
                ln = s[:m.start()].count("\n") + 1
                bad.append(f"{os.path.basename(p)}:{ln} difficulty-{cls} → {inner!r}（期望 {exp!r}）")
    if bad:
        for x in bad[:20]:
            print("FAIL [难度标签口径]", x)
        check(False, f"[难度标签口径] {len(bad)}/{total} 枚徽标文案非法（须 专家/架构/高级；见 conventions §2）")
    else:
        check(True, f"[难度标签口径] {total} 枚 difficulty 徽标文案全为短表（专家/架构/高级）")


def run_special_no_difficulty_check():
    """1k) M/G/K 三专篇彻底取消难度分级：不得出现 data-difficulty。"""
    bad = []
    for bn in NO_DIFF_PAGES:
        p = os.path.join(CHAPTER_DIR, bn)
        n = read(p).count("data-difficulty=")
        if n:
            bad.append(f"{bn}: data-difficulty×{n}")
    if bad:
        for x in bad:
            print("FAIL [专篇无分级]", x)
        check(False, f"[专篇无分级] {len(bad)} 个专篇页仍带 data-difficulty（须 0；见 conventions §2）")
    else:
        check(True, f"[专篇无分级] {len(NO_DIFF_PAGES)} 个专篇页均无 data-difficulty（方法论/工程化/生产踩坑不分级）")


def main():
    # 0) 权威计数位（含散文）——必须先于其他统计断言
    run_sync_counts_check()
    run_kb_count_markup_check()
    run_l1_container_scan()
    # 0d) 篇章页/E/S 页头难度分布 vs 实体卡片（2026-09-15 新增，防 12 页漂移复发）
    run_chapter_meta_difficulty_check()
    # 0e/1i) 卡片层级：qa-card / map-card 不得互相嵌套（2026-09-16 新增，防缺 </div> 卡片套卡片）
    run_card_nesting_check()
    run_difficulty_label_check()
    run_special_no_difficulty_check()

    # 4 聚合页 + 全部章节 + 全部导图（红线校验覆盖全站）
    texts = {k: read(v) for k, v in AGG_FILES.items()}
    chap_files = all_chapter_files()
    mind_files = all_mind_files()
    for p in chap_files + mind_files:
        texts[f"file:{os.path.basename(p)}"] = read(p)

    # 1) data-page-node-id 红线（全站所有目标 HTML）
    for k, t in texts.items():
        c = t.count("data-page-node-id")
        check(c == 0, f"[红线] {k}: data-page-node-id={c} (须 0)")

    # 1c) 内部编辑字眼（不得出现在面向读者的卡片正文里）
    #     来源：内容补写轮次的占位/批注词未被清理（2026-09-15 实测「再加厚：」残留 15 处，
    #     且此前无任何校验能拦住，故纳入硬门禁）
    for k, t in texts.items():
        for w in EDITORIAL_WORDS:
            c = t.count(w)
            check(c == 0, f"[内部字眼] {k}: 出现「{w}」x{c}（须 0）")

    # 1b) 手机小屏强制（MOBILE-MANDATORY / format-shared §8）
    css_path = os.path.join(CHAPTER_DIR, "assets/design-system.css")
    css_txt = read(css_path) if os.path.isfile(css_path) else ""
    check("MOBILE-MANDATORY" in css_txt,
          "[小屏] design-system.css 须含 MOBILE-MANDATORY 段")
    check("@media (max-width: 768px)" in css_txt and "@media (max-width: 480px)" in css_txt,
          "[小屏] design-system.css 须含 768/480 断点")
    _vp = re.compile(r'<meta[^>]+name=["\']viewport["\'][^>]*>', re.I)
    _site_html = (
        [AGG_FILES["root"], AGG_FILES["chap_idx"], AGG_FILES["mind_idx"], AGG_FILES["overview"]]
        + chap_files + mind_files
        + [os.path.join(CHAPTER_DIR, "nav-server-security-checkpoint.html")]
    )
    # nav-overview already in overview; avoid dup noise
    _seen = set()
    _vp_miss = []
    for p in _site_html:
        if p in _seen or not os.path.isfile(p):
            continue
        _seen.add(p)
        if not _vp.search(read(p)):
            _vp_miss.append(os.path.relpath(p, BASE))
    check(not _vp_miss, f"[小屏] 缺 viewport 的页面: {_vp_miss[:8]}")
    check("MOBILE-MANDATORY" in texts["root"] and "@media (max-width: 768px)" in texts["root"],
          "[小屏] 根 index 须含 MOBILE-MANDATORY 小屏媒体查询")
    check("MOBILE-MANDATORY" in texts["mind_idx"] and "@media (max-width: 760px)" in texts["mind_idx"],
          "[小屏] 导图 index 须含 MOBILE-MANDATORY 小屏媒体查询")

    # 1g) 移动端横向溢出兜底（2026-09-15 实测：核心原理页 375px 视口溢出 248px / 18 处越界）
    #     ① CSS 层：body 全局 overflow-wrap（长英文标识符/路径/签名可断行）
    #        + 裸 pre 横向滚动；缺任一条长 token 会再度撑破卡片
    #     ② HTML 层：不得存在未被 .code-block 包裹的裸 <pre>（既无样式也无滚动）
    #     注意：不可用简单子串匹配——CSS 里本就有多处针对特定选择器的
    #     overflow-wrap: anywhere（.chapter-card .card-title 等），子串匹配会恒真、形同虚设。
    check(re.search(r"^\s*body\s*\{[^}]*overflow-wrap:\s*anywhere", css_txt, re.M),
          "[溢出] design-system.css 须在 body 规则内声明 overflow-wrap: anywhere（全局继承兜底）")
    check(re.search(r"^\s*pre\s*\{[^}]*overflow-x:\s*auto", css_txt, re.M),
          "[溢出] design-system.css 须含裸 pre { overflow-x: auto } 横向滚动兜底")
    _pre_texts = dict(texts)
    _ck = os.path.join(CHAPTER_DIR, "nav-server-security-checkpoint.html")
    if os.path.isfile(_ck):
        _pre_texts["file:nav-server-security-checkpoint.html"] = read(_ck)
    _bare_pre = [k for k, t in _pre_texts.items()
                 if any(not inside for _, inside in scan_bare_pre(t))]
    check(not _bare_pre, f"[溢出] 存在未被 .code-block 包裹的裸 <pre>: {_bare_pre[:8]}")

    # 1h) 列表 marker 缩进兜底（2026-09-16 实测：核心原理页 20 处、安全检查页 1 处）
    #     上面的 reset `* { margin: 0; padding: 0 }` 抹掉了 ul/ol 的 UA 默认
    #     padding-inline-start(40px)，全站列表缩进因此依赖各自的类规则；凡未匹配到
    #     类规则的列表 padding-left 即为 0，而 list-style-position: outside 的圆点/
    #     数字是绘制在内容盒之外的 —— 桌面表现为「列表没有缩进、圆点贴着卡片边缘」，
    #     小屏（卡片内边距收窄到 0.9rem）直接越出卡片（实测 375px 越界 2.6px）。
    #     兜底必须写成 :where(ul, ol)（特异度 0），任何带类名的列表规则都能覆盖它；
    #     若写成裸选择器 `ul, ol { … }`（特异度 0,0,1）就会顶掉
    #     `.epq-kp-list{padding:0}` / `.map-col ul{padding:0}` 这类自定义列表的排版。
    check(re.search(r"^\s*:where\(\s*ul\s*,\s*ol\s*\)\s*\{[^}]*padding-inline-start", css_txt, re.M),
          "[列表] design-system.css 须含零特异度缩进兜底 :where(ul, ol) { padding-inline-start: … }")
    check(not re.search(r"^\s*ul\s*,\s*ol\s*\{[^}]*padding-inline-start", css_txt, re.M),
          "[列表] 列表缩进兜底不得用裸选择器 ul, ol { … }（特异度 0,0,1 会顶掉自定义列表的 padding:0）")

    _mind_media_miss = []
    for p in mind_files:
        mt = read(p)
        if "MOBILE-MANDATORY" not in mt or "@media (max-width: 760px)" not in mt:
            _mind_media_miss.append(os.path.basename(p))
    check(not _mind_media_miss, f"[小屏] 导图页缺 MOBILE-MANDATORY: {_mind_media_miss[:8]}")

    # 1c) 主题 / 暗黑模式（format-shared §9）
    check('data-theme="dark"' in css_txt or "data-theme='dark'" in css_txt,
          '[主题] design-system.css 须含 html[data-theme="dark"] 令牌块')
    check("prefers-color-scheme: dark" in css_txt,
          "[主题] design-system.css 须含 prefers-color-scheme: dark 回退")
    check(os.path.isfile(os.path.join(CHAPTER_DIR, "assets/theme-init.js")),
          "[主题] 须存在 assets/theme-init.js")
    _theme_miss = []
    _seen_theme = set()
    for p in _site_html:
        if p in _seen_theme or not os.path.isfile(p):
            continue
        _seen_theme.add(p)
        if "theme-init.js" not in read(p):
            _theme_miss.append(os.path.relpath(p, BASE))
    check(not _theme_miss, f"[主题] 缺 theme-init.js 的页面: {_theme_miss[:8]}")

    # 1d) Mermaid：prettier-ignore + 未塌缩（format-shared §10）
    _mm_miss = []
    _mm_flat = []
    for p in _site_html:
        if not os.path.isfile(p):
            continue
        raw = read(p)
        if 'class="mermaid"' not in raw:
            continue
        lines = raw.splitlines()
        for i, line in enumerate(lines):
            if re.match(r'^\s*<div class="mermaid">', line):
                prev = lines[i - 1] if i > 0 else ""
                if "prettier-ignore" not in prev:
                    _mm_miss.append(f"{os.path.basename(p)}:{i + 1}")
        for inner in re.findall(r'<div class="mermaid">(.*?)</div>', raw, re.S):
            if inner.count("\n") < 2:
                _mm_flat.append(os.path.basename(p))
                break
    check(not _mm_miss, f"[Mermaid] 缺 prettier-ignore: {_mm_miss[:8]}")
    check(not _mm_flat, f"[Mermaid] 图源码疑似被格式化塌缩: {_mm_flat[:8]}")

    # 1e) 顶/底导航壳位置（format-shared §4.2）：枢纽 index 无导航；其余有壳的页顶栏须贴 body 首
    _hubs = {
        os.path.normpath(AGG_FILES["root"]),
        os.path.normpath(AGG_FILES["chap_idx"]),
    }
    _nav_bad = []
    for p in _site_html:
        if not os.path.isfile(p):
            continue
        pn = os.path.normpath(p)
        raw = read(p)
        if pn in _hubs:
            if "site-page-nav" in raw or re.search(r'class="chapter-nav', raw):
                _nav_bad.append(f"{os.path.relpath(p, BASE)}:hub-has-nav")
            continue
        if "site-page-nav--top" not in raw:
            continue
        bm = re.search(r"<body[^>]*>([\s\S]*)</body>", raw, re.I)
        if not bm:
            _nav_bad.append(f"{os.path.basename(p)}:no-body")
            continue
        body = bm.group(1)
        if not re.match(r'\s*<div class="site-page-nav site-page-nav--top">', body):
            _nav_bad.append(f"{os.path.basename(p)}:top-not-first")
        if body.count("site-page-nav--bottom") != 1:
            _nav_bad.append(f"{os.path.basename(p)}:bottom-count")
        else:
            bi = body.find("site-page-nav--bottom")
            if re.search(r"<script\b", body[:bi], re.I):
                _nav_bad.append(f"{os.path.basename(p)}:script-before-bottom")
    check(not _nav_bad, f"[导航壳] {_nav_bad[:8]}")

    # 2) 标签截断
    for k, t in texts.items():
        trunc = len(re.findall(r"</spa(?!n>)", t))
        check(trunc == 0, f"[截断] {k}: </spa 残留={trunc} (须 0)")

    # 3) overview ov-stat-num 顺序（项数以 kb-counts.json ov_stat_order 为准；不含方法论）
    # 兼容 kb-count 标记：ov-stat-num"><span …>N</span></div>
    _KB_NUM = r'(?:<span[^>]*class="[^"]*kb-count[^"]*"[^>]*>)?(\d+)(?:</span>)?'
    _ov_n = len(_cfg["ov_stat_order"])
    ov = [int(x) for x in re.findall(
        rf'ov-stat-num"[^>]*>\s*{_KB_NUM}\s*</div>', texts["overview"]
    )[:_ov_n]]
    expect_order = [_cfg["counts"][k] for k in _cfg["ov_stat_order"]]
    check(ov == expect_order,
          f"[overview] ov-stat-num={ov} 期望={expect_order}")

    # 3b) overview 排序硬约束：P0→P2 已由 section 顺序保证；
    #     子组内必须 C→E→S + 题号升序；属性与所在组一致；标题计数=实际
    def _ov_sort_key(nid: str):
        return ({"C": 0, "E": 1, "S": 2}.get(nid[:1], 9), nid)

    _diff_from_title = {"专家": "expert", "架构": "architect", "高级": "senior"}
    _ov_sort_fail = 0
    _ov_bucket_fail = 0
    _ov_title_fail = 0
    for _gm in re.finditer(
        r'<section class="ov-group" id="(group-p[012])">(.*?)</section>',
        texts["overview"],
        re.S,
    ):
        _gid, _gbody = _gm.group(1), _gm.group(2)
        _expect_prio = _gid.replace("group-", "")  # p0/p1/p2
        for _sm in re.split(r'(?=<h3 class="ov-subgroup-title">)', _gbody):
            _tm = re.match(
                rf'<h3 class="ov-subgroup-title">(专家|架构|高级)\s*·\s*{_KB_NUM}\s*题</h3>',
                _sm,
            )
            if not _tm:
                continue
            _label, _title_n = _tm.group(1), int(_tm.group(2))
            _expect_diff = _diff_from_title[_label]
            _ids = []
            for _im in re.finditer(
                r'<a class="ov-item"[^>]*>(.*?)</a>', _sm, re.S
            ):
                _inner = _im.group(1)
                _nm = re.search(r'class="ov-num">([^<]+)<', _inner)
                if not _nm:
                    continue
                _nid = _nm.group(1).strip()
                _ids.append(_nid)
                _pm = re.search(r'priority-(p\d)', _inner)
                _dm = re.search(r'difficulty-(\w+)', _inner)
                if _pm and _pm.group(1) != _expect_prio:
                    _ov_bucket_fail += 1
                if _dm and _dm.group(1) != _expect_diff:
                    _ov_bucket_fail += 1
            if len(_ids) != _title_n:
                _ov_title_fail += 1
            for _i in range(1, len(_ids)):
                if _ov_sort_key(_ids[_i]) < _ov_sort_key(_ids[_i - 1]):
                    _ov_sort_fail += 1
                    if _ov_sort_fail <= 5:
                        print(
                            f"FAIL [overview排序] {_gid}/{_label}: {_ids[_i-1]} → {_ids[_i]}"
                        )
    check(_ov_sort_fail == 0,
          f"[overview排序] 子组内 C→E→S+题号升序 违规数={_ov_sort_fail}（须 0）")
    check(_ov_bucket_fail == 0,
          f"[overview归属] item priority/difficulty 与所在组不一致数={_ov_bucket_fail}（须 0）")
    check(_ov_title_fail == 0,
          f"[overview子组题数] 标题 N ≠ 实际 ov-item 的子组数={_ov_title_fail}（须 0）")

    # 3b2) overview 类型三级（篇章/核心原理/场景题）ov-type-count = 该块 ov-item 数
    _ov_type_fail = 0
    _ov_type_missing = 0
    _type_pref = {"篇章": "C", "核心原理": "E", "场景题": "S"}
    for _gm in re.finditer(
        r'<section class="ov-group"[^>]*id="(group-p\d)"[^>]*>(.*?)</section>',
        texts["overview"],
        re.S,
    ):
        _gid, _gbody = _gm.group(1), _gm.group(2)
        for _sm in re.split(r'(?=<h3 class="ov-subgroup-title">)', _gbody):
            if not re.match(r'<h3 class="ov-subgroup-title">', _sm or ""):
                continue
            _type_blocks = list(
                re.finditer(r'<div class="ov-type">(.*?)</div>', _sm, re.S)
            )
            if not _type_blocks:
                _ov_type_missing += 1
                continue
            for _tb in _type_blocks:
                _tbody = _tb.group(1)
                _thm = re.search(
                    rf'<h4 class="ov-type-title">\s*(篇章|核心原理|场景题)'
                    rf'<span class="ov-type-count">\s*{_KB_NUM}\s*题</span>\s*</h4>',
                    _tbody,
                )
                if not _thm:
                    _ov_type_fail += 1
                    continue
                _tlabel, _tn = _thm.group(1), int(_thm.group(2))
                _ids = re.findall(r'class="ov-num">([^<]+)<', _tbody)
                _pref = _type_pref[_tlabel]
                if len(_ids) != _tn or any(not i.startswith(_pref) for i in _ids):
                    _ov_type_fail += 1
                    if _ov_type_fail <= 6:
                        print(
                            f"FAIL [overview类型] {_gid}: {_tlabel} title={_tn} "
                            f"actual={len(_ids)} ids={_ids[:3]}"
                        )
    check(
        _ov_type_missing == 0,
        f"[overview类型结构] 缺少 ov-type 分块的子组数={_ov_type_missing}（须 0）",
    )
    check(
        _ov_type_fail == 0,
        f"[overview类型计数] ov-type-count 不一致数={_ov_type_fail}（须 0）",
    )

    # 3c) 全站分组/页头页尾结构性计数（防孤儿卡与徽标漂移）
    # --- 场景页：S 卡必须在对应 group-N section 内；group-count = 卡数 ---
    _sc_path = f"{CHAPTER_DIR}/chapter-questions-scenario.html"
    _sc = read(_sc_path)
    _sc_orphan = 0
    for _gap in re.findall(
        r'</section>\s*(.*?)\s*<section class="scenario-group"', _sc, re.S
    ):
        _sc_orphan += len(
            re.findall(r'<div class="qa-card[^"]*"[^>]*id="S\d+\.\d+"', _gap)
        )
    check(_sc_orphan == 0, f"[场景结构] section 间隙孤儿 S 卡={_sc_orphan}（须 0）")
    _sc_gc_fail = 0
    for _g in range(1, 13):
        _sm = re.search(
            rf'<section class="scenario-group"[^>]*id="group-{_g}"[^>]*>(.*?)</section>',
            _sc,
            re.S,
        )
        if not _sm:
            _sc_gc_fail += 1
            continue
        _body = _sm.group(1)
        _cards = set(
            re.findall(r'<div class="qa-card[^"]*"[^>]*id="(S\d+\.\d+)"', _body)
        )
        _gcm = re.search(rf'class="group-count"[^>]*>\s*{_KB_NUM}', _body)
        if not _gcm or int(_gcm.group(1)) != len(_cards):
            _sc_gc_fail += 1
    check(_sc_gc_fail == 0, f"[场景group-count] 不一致组数={_sc_gc_fail}（须 0）")

    # --- 根 index：dir-group-count / dir-count(题) = 后续 q-item 数 ---
    _dg_fail = 0
    for _dm in re.finditer(
        rf'<div class="dir-group">\s*<div class="dir-group-title">.*?dir-group-count"[^>]*>\s*{_KB_NUM}\s*题</span></div>\s*<ul class="q-list">(.*?)</ul>',
        texts["root"],
        re.S,
    ):
        if int(_dm.group(1)) != len(re.findall(r'<li class="q-item"', _dm.group(2))):
            _dg_fail += 1
    check(_dg_fail == 0, f"[根index dir-group] 计数≠列表 组数={_dg_fail}（须 0）")
    _ds_fail = 0
    for _sm in re.finditer(r'<section class="dir-section">(.*?)</section>', texts["root"], re.S):
        _body = _sm.group(1)
        _hm = re.search(
            rf'class="dir-count"[^>]*>\s*{_KB_NUM}\s*题</span>', _body
        )
        if not _hm:
            continue
        if int(_hm.group(1)) != len(re.findall(r'<li class="q-item"', _body)):
            _ds_fail += 1
    check(_ds_fail == 0, f"[根index dir-count] 计数≠列表 段数={_ds_fail}（须 0）")

    # --- mind index card-foot ↔ 篇章 C 数 / 导图 summary 内 E·S 数 ---
    _mf_fail = 0
    for _mp in mind_files:
        _bn = os.path.basename(_mp)
        _mm = re.match(r"mind-(\d{2})-", _bn)
        if not _mm:
            continue
        _num = _mm.group(1)
        _mt = read(_mp)
        _e = set()
        _s = set()
        for _sum in re.findall(r"<summary>([^<]*)</summary>", _mt):
            _e.update(re.findall(r"\bE\d{2}\.\d{2}\b", _sum))
            _s.update(re.findall(r"\bS\d{2}\.\d{2}\b", _sum))
        _c_act = len(
            set(
                re.findall(
                    rf'id="(C{_num}\.\d+)"',
                    read(glob.glob(f"{CHAPTER_DIR}/chapter-{_num}-*.html")[0]),
                )
            )
        )
        _fm = re.search(
            rf'href="{re.escape(_bn)}"[^>]*>.*?class="card-foot">(.*?)</div>',
            texts["mind_idx"],
            re.S,
        )
        if not _fm:
            _mf_fail += 1
            continue
        _foot = _fm.group(1)
        _cm = re.search(rf"章节\s*{_KB_NUM}", _foot)
        _em = re.search(rf"原理\s*{_KB_NUM}", _foot)
        _sm2 = re.search(rf"场景\s*{_KB_NUM}", _foot)
        if not _cm or int(_cm.group(1)) != _c_act:
            _mf_fail += 1
        if _e and (not _em or int(_em.group(1)) != len(_e)):
            _mf_fail += 1
        if (not _e) and _em:
            _mf_fail += 1
        if _s and (not _sm2 or int(_sm2.group(1)) != len(_s)):
            _mf_fail += 1
        if (not _s) and _sm2:
            _mf_fail += 1
    check(_mf_fail == 0, f"[mind card-foot] 与篇章/summary 不一致数={_mf_fail}（须 0）")

    # 4) 根 index 统计（数字在前、label 在后；兼容内层 kb-count span）
    def stat(pat, t):
        m = re.search(pat, t)
        return int(m.group(1)) if m else None
    _STAT_N = rf'(?:<span[^>]*class="[^"]*kb-count[^"]*"[^>]*>)?(\d+)(?:</span>)?'
    root_ch = stat(rf'{_STAT_N}\s*</div>\s*<div class="stat-label">深度 Q&amp;A', texts["root"])
    root_all = stat(rf'全站\s*{_STAT_N}\s*题', texts["root"])   # 「全站 N 题」= total（C+E+S），非 M/G/K 加总
    check(root_ch == EXPECT["chapters"], f"[根index] 深度Q&A={root_ch} 期望 {EXPECT['chapters']}")
    # 禁止「题目+方法论+工程化+踩坑」式合计 UI
    root_sum = stat(rf'{_STAT_N}\s*</div>\s*<div class="stat-label">合计', texts["root"])
    check(root_sum is None, f"[根index] 不应存在跨域「合计」统计卡（实际={root_sum}）")
    if root_all is not None:
        check(root_all == EXPECT["total"], f"[根index] 全站题量={root_all} 期望 {EXPECT['total']}（仅 C+E+S）")
    if ENGINEERING:
        root_eng = stat(rf'{_STAT_N}\s*</div>\s*<div class="stat-label">工程化要点</div>', texts["root"])
        if root_eng is None:
            root_eng = stat(rf'{_STAT_N}\s*</div>\s*<div class="stat-label">工程化</div>', texts["root"])
        check(root_eng == ENGINEERING, f"[根index] 工程化={root_eng} 期望 {ENGINEERING}")

    # 5) 章节 index stat-number（同结构，允许 </div> 与 <div> 间换行）+ 全站 N 道
    chap_ch = stat(rf'{_STAT_N}\s*</div>\s*<div class="stat-label">深度 Q&amp;A', texts["chap_idx"])
    chap_all = stat(rf'全站\s*{_STAT_N}\s*道', texts["chap_idx"])
    check(chap_ch == EXPECT["chapters"], f"[章节index] 深度Q&A={chap_ch} 期望 {EXPECT['chapters']}")
    check(chap_all == EXPECT["total"], f"[章节index] 全站={chap_all} 期望 {EXPECT['total']}")
    if ENGINEERING:
        chap_eng = stat(rf'{_STAT_N}\s*</div>\s*<div class="stat-label">工程化要点</div>', texts["chap_idx"])
        if chap_eng is None:
            chap_eng = stat(rf'{_STAT_N}\s*</div>\s*<div class="stat-label">工程化</div>', texts["chap_idx"])
        check(chap_eng == ENGINEERING, f"[章节index] 工程化={chap_eng} 期望 {ENGINEERING}")

    # root methodology label may be 核心方法论
    root_m = stat(rf'{_STAT_N}\s*</div>\s*<div class="stat-label">核心方法论</div>', texts["root"])
    if root_m is None:
        root_m = stat(rf'{_STAT_N}\s*</div>\s*<div class="stat-label">方法论</div>', texts["root"])
    if ENGINEERING is not None and EXPECT.get("methodology") is not None and root_m is not None:
        check(root_m == EXPECT["methodology"], f"[根index] 方法论={root_m} 期望 {EXPECT['methodology']}")

    # 6) 新卡双编码 + 落位（按题号前缀自动定位宿主章节页）
    chap_text_all = "\n@@@\n".join(read(p) for p in chap_files)
    mind_text_all = "\n@@@\n".join(read(p) for p in mind_files)
    for nid in NEW_IDS:
        # 双编码：在宿主章节页（含该 ID 的 chapter 文件）找 data-priority 属性 + 可见 priority-pX
        # 工程化卡可能无优先级双编码，仅校验卡片存在
        host = None
        for p in chap_files:
            if re.search(rf'id="{re.escape(nid)}"', read(p)):
                host = p
                break
        if host:
            ht = read(host)
            card = re.search(rf'id="{re.escape(nid)}"[^>]*data-priority="(p\d)"', ht)
            visible = re.search(rf'id="{re.escape(nid)}".*?priority priority-(p\d)', ht, re.S)
            if card and visible:
                check(card.group(1) == visible.group(1),
                      f"[双编码] {nid}: data-priority={card.group(1)} 徽标={visible.group(1)}")
            elif nid.startswith("G") or nid.startswith("K"):
                check(True, f"[双编码] {nid}: 工程化/踩坑卡无强制优先级（宿主 {os.path.basename(host)}）")
            else:
                # 方法论部分卡可能无 priority
                has_card = bool(re.search(rf'id="{re.escape(nid)}"', ht))
                check(has_card, f"[双编码] {nid}: 未找到属性或徽标（宿主 {os.path.basename(host)}）")
        else:
            check(False, f"[双编码] {nid}: 未在任何章节页找到该卡片")
        # overview 落位（C/E/S 必进；M/G 默认不进 overview）
        if not (nid.startswith("M") or nid.startswith("G") or nid.startswith("K")):
            check(nid in texts["overview"], f"[落位] {nid} 在 overview")
        # 根 index 落位（q-id）
        check(nid in texts["root"], f"[落位] {nid} 在 根index")
        # mind 落位（扫描全部 mind 文件，命中任一即 PASS）
        check(nid in mind_text_all, f"[落位] {nid} 在 mind 站（任一导图页）")

    # 7) 求和自洽
    check(EXPECT["p0"]+EXPECT["p1"]+EXPECT["p2"] == EXPECT["total"], "[自洽] P0+P1+P2=总量")
    check(EXPECT["expert"]+EXPECT["architect"]+EXPECT["senior"] == EXPECT["total"], "[自洽] 难度三级=总量")
    check(EXPECT["chapters"]+EXPECT["basics"]+EXPECT["scenarios"] == EXPECT["total"], "[自洽] 类型三级=总量（跨大篇章口径）")

    # 8) 卡片 id 三方一致性：章节正文 ↔ 章节 TOC ↔ 导图引用；id 总数=各域分计之和（非对外「全站合计」）
    IDPAT = r"((?:M|C|E|S|G|K)\d{2}\.\d{2})"
    body_ids, toc_ids, mind_ids = set(), set(), set()
    for p in chap_files:
        t = read(p)
        body_ids |= set(re.findall(rf'id="{IDPAT}"', t))
        toc_ids |= set(re.findall(rf'href="#{IDPAT}"', t))
    for p in mind_files:
        mind_ids |= set(re.findall(IDPAT, read(p)))
    check(len(body_ids) == CARDS_IN_CHAPTERS,
          f"[id总数] 章节页卡片 {len(body_ids)} 期望 {CARDS_IN_CHAPTERS}（total+methodology+engineering+pitfalls，分域加总仅作一致性校验）")
    check(not (body_ids - toc_ids),
          f"[TOC缺失] 正文有但目录无：{sorted(body_ids - toc_ids)[:10]}")
    check(not (toc_ids - body_ids),
          f"[TOC死链] 目录有但正文无：{sorted(toc_ids - body_ids)[:10]}")
    check(not (mind_ids - body_ids),
          f"[导图悬空] 导图引用但正文无：{sorted(mind_ids - body_ids)[:10]}")

    print("\n==== 校验结果 ====")
    if check.failed == 0:
        print("ALL PASS ✅ 三权威源一致，data-page-node-id=0，小屏/主题/导航壳/Mermaid-ignore 就位，新卡落位且双编码一致。")
        sys.exit(0)
    else:
        print(f"存在 {check.failed} 项 FAIL ❌，请复查。")
        sys.exit(1)

if __name__ == "__main__":
    main()
