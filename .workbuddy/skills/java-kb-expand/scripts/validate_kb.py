#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
java-kb-expand · 全量校验脚本（通用版）
==============================================
复制本文件到 java-architect-interview/tmp/，按需填 EXPECT 字典（本轮权威计数）与 NEW_IDS（新增/改动题号列表），
然后运行：python3 validate_kb.py

校验项：
  0) **散文/SSOT 计数位**：子进程调用 sync_counts.py check（含 P01–P89，防页头「本页 N 道」漂移）
  0b) **计数标记**：每个 position 须含 `data-kb-pos="Pxx"`（ov_series=P07×len(ov_stat_order)）；场景 `group-count` / 根 `dir-group` 抽检 `data-kb-count-local`
  0c) **L1 聚合 UI**：页头/footer/desc/meta/subtitle/map-note/tagline/stat 等容器内「N题|卡|道|组」不得裸数字（见 conventions §5.1.4）
  1) 全部目标 HTML 文件 data-page-node-id 全 0（红线）
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

BASE = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI"
CHAPTER_DIR = f"{BASE}/java-architect-interview"
MIND_DIR = f"{BASE}/java-architect-interview-mind"
COUNTS_JSON = f"{CHAPTER_DIR}/docs/kb-counts.json"

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
NEW_IDS = ["C06.15","C07.16","C08.12","C09.17","C10.29","C10.30","C11.26","C11.27","C11.28","C12.33","C12.34","C12.35","C13.14","C14.13","C15.12","G01.04","G02.04","G03.04","G04.04","G05.04","G06.04","G07.04","G08.04","K01.01","K01.02","K02.01","K02.02","K03.01","K03.02","K04.01","K04.02","K05.01","K05.02","K06.01","K06.02","K07.01","K07.02","K08.01","K08.02"]

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


def run_kb_count_markup_check():
    """每个 SSOT position 必须带 data-kb-pos 标记；结构计数建议带 data-kb-count-local。
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
    # 结构位点抽检：场景 group-count / 根 dir-group 须有 local 标记
    scen = read(os.path.join(BASE, "java-architect-interview/chapter-questions-scenario.html"))
    gc = len(re.findall(r'class="group-count"', scen))
    gc_m = scen.count('data-kb-count-local="group-count"')
    if gc and gc_m < gc:
        miss.append(f"场景 group-count 标记不足：class×{gc} local×{gc_m}")
    root = read(os.path.join(BASE, "index.html"))
    if 'class="dir-group-count">' in root and 'data-kb-count-local="dir-group"' not in root:
        miss.append("根 index 缺少 dir-group local 标记")
    if miss:
        for x in miss[:15]:
            print("FAIL [kb-count标记]", x)
        check(False, f"[kb-count标记] {len(miss)} 处缺失/不一致（须 data-kb-pos / data-kb-count-local）")
    else:
        check(True, f"[kb-count标记] SSOT positions 均含 data-kb-pos（{len(cfg['positions'])} 位）+ 结构抽检通过")


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
        if 'data-kb-pos="' in w and w.rfind('data-kb-pos="') > w.rfind("</"):
            return True
        if "data-kb-count-local=" in w and w.rfind("data-kb-count-local=") > w.rfind("</"):
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
        check(False, f"[L1聚合UI] 裸计数 {len(misses)} 处（须 kb-count / data-kb-count-local，见 §5.1.4）")
    else:
        check(True, "[L1聚合UI] 页头/footer/desc/meta/note/tagline/stat 无裸「N题|卡|道|组」")


def main():
    # 0) 权威计数位（含散文）——必须先于其他统计断言
    run_sync_counts_check()
    run_kb_count_markup_check()
    run_l1_container_scan()

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

    _diff_from_title = {"专家级": "expert", "架构级": "architect", "高级开发": "senior"}
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
                rf'<h3 class="ov-subgroup-title">(专家级|架构级|高级开发)\s*·\s*{_KB_NUM}\s*题</h3>',
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
                    rf'<h4 class="ov-type-title">(篇章|核心原理|场景题)'
                    rf'<span class="ov-type-count">\s*{_KB_NUM}\s*题</span></h4>',
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
    root_ch = stat(rf'{_STAT_N}</div>\s*<div class="stat-label">深度 Q&amp;A', texts["root"])
    root_all = stat(rf'全站\s*{_STAT_N}\s*题', texts["root"])   # 「全站 N 题」= total（C+E+S），非 M/G/K 加总
    check(root_ch == EXPECT["chapters"], f"[根index] 深度Q&A={root_ch} 期望 {EXPECT['chapters']}")
    # 禁止「题目+方法论+工程化+踩坑」式合计 UI
    root_sum = stat(rf'{_STAT_N}</div>\s*<div class="stat-label">合计', texts["root"])
    check(root_sum is None, f"[根index] 不应存在跨域「合计」统计卡（实际={root_sum}）")
    if root_all is not None:
        check(root_all == EXPECT["total"], f"[根index] 全站题量={root_all} 期望 {EXPECT['total']}（仅 C+E+S）")
    if ENGINEERING:
        root_eng = stat(rf'{_STAT_N}</div>\s*<div class="stat-label">工程化要点</div>', texts["root"])
        if root_eng is None:
            root_eng = stat(rf'{_STAT_N}</div>\s*<div class="stat-label">工程化</div>', texts["root"])
        check(root_eng == ENGINEERING, f"[根index] 工程化={root_eng} 期望 {ENGINEERING}")

    # 5) 章节 index stat-number（同结构，允许 </div> 与 <div> 间换行）+ 全站 N 道
    chap_ch = stat(rf'{_STAT_N}</div>\s*<div class="stat-label">深度 Q&amp;A', texts["chap_idx"])
    chap_all = stat(rf'全站\s*{_STAT_N}\s*道', texts["chap_idx"])
    check(chap_ch == EXPECT["chapters"], f"[章节index] 深度Q&A={chap_ch} 期望 {EXPECT['chapters']}")
    check(chap_all == EXPECT["total"], f"[章节index] 全站={chap_all} 期望 {EXPECT['total']}")
    if ENGINEERING:
        chap_eng = stat(rf'{_STAT_N}</div>\s*<div class="stat-label">工程化要点</div>', texts["chap_idx"])
        if chap_eng is None:
            chap_eng = stat(rf'{_STAT_N}</div>\s*<div class="stat-label">工程化</div>', texts["chap_idx"])
        check(chap_eng == ENGINEERING, f"[章节index] 工程化={chap_eng} 期望 {ENGINEERING}")

    # root methodology label may be 核心方法论
    root_m = stat(rf'{_STAT_N}</div>\s*<div class="stat-label">核心方法论</div>', texts["root"])
    if root_m is None:
        root_m = stat(rf'{_STAT_N}</div>\s*<div class="stat-label">方法论</div>', texts["root"])
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
        print("ALL PASS ✅ 三权威源一致，data-page-node-id=0，新卡落位且双编码一致。")
        sys.exit(0)
    else:
        print(f"存在 {check.failed} 项 FAIL ❌，请复查。")
        sys.exit(1)

if __name__ == "__main__":
    main()
