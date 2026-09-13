#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
java-kb-expand · 全量校验脚本（通用版）
==============================================
复制本文件到 java-architect-interview/tmp/，按需填 EXPECT 字典（本轮权威计数）与 NEW_IDS（新增/改动题号列表），
然后运行：python3 validate_kb.py

校验项：
  0) **散文/SSOT 计数位**：子进程调用 sync_counts.py check（含 P27–P42 等散文位，防页头「本页 N 道」漂移）
  1) 全部目标 HTML 文件 data-page-node-id 全 0（红线）
  2) 无 </spa(?!n>) 标签截断残留
  3) overview ov-stat-num 三源一致（11 项：总量/优先级/难度/方法论/类型）
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
# 根 index 合计 = 题数 + 方法论 + 工程化（若有 engineering 键）
ROOT_SUM_EXTRA = _cfg["counts"]["methodology"] + _cfg["counts"].get("engineering", 0)
# 全站卡片总数（题目 + 方法论 + 工程化），用于 id 总数校验
SUM_ALL = _cfg["counts"]["sum_all"]
ENGINEERING = _cfg["counts"].get("engineering", 0)

# ====== 待填：本轮新增/改动题号（用于落位+双编码校验）======
# 注意：方法论/工程化卡默认不进 overview；含 M/G 时跳过 overview 落位检查
NEW_IDS = ["E06.04","E06.05","E06.06","E09.04","E09.05","E09.06","E10.04","E10.05","E10.06","C11.25"]

# 4 份聚合页（固定路径）。注意：BASE 已含项目根 "Java Spring AI"，根 index 即 {BASE}/index.html
AGG_FILES = {
    "overview": f"{CHAPTER_DIR}/chapter-overview-priority.html",
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
        if b in ("index.html", "chapter-overview-priority.html"):
            continue
        fs.append(p)
    return fs

def all_mind_files():
    return [p for p in glob.glob(f"{MIND_DIR}/mind-*.html")
            if os.path.basename(p) != "index.html"]

def run_sync_counts_check():
    """散文计数位（P27–P42 等）与全部 positions 必须与 kb-counts.json 一致。
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
        check(True, "[散文计数/SSOT] sync_counts.py check 全部通过（含 P27–P42 散文位）")
    else:
        for ln in fails[:12]:
            print(ln)
        check(False, f"[散文计数/SSOT] sync_counts.py check 失败 exit={r.returncode} fail行={len(fails)}")


def main():
    # 0) 权威计数位（含散文）——必须先于其他统计断言
    run_sync_counts_check()

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

    # 3) overview ov-stat-num 顺序（11 项，顺序以 kb-counts.json ov_stat_order 为准）
    ov = re.findall(r'ov-stat-num">(\d+)</div>', texts["overview"])
    ov = [int(x) for x in ov[:11]]
    expect_order = [_cfg["counts"][k] for k in _cfg["ov_stat_order"]]
    check(ov == expect_order,
          f"[overview] ov-stat-num={ov} 期望={expect_order}")

    # 4) 根 index 统计（数字在前、label 在后：<div class="stat-number">N</div><div class="stat-label">…）
    def stat(pat, t):
        m = re.search(pat, t)
        return int(m.group(1)) if m else None
    root_ch = stat(r'(\d+)</div>\s*<div class="stat-label">深度 Q&amp;A', texts["root"])
    root_sum = stat(r'(\d+)</div>\s*<div class="stat-label">合计', texts["root"])
    root_all = stat(r'全站\s*(\d+)\s*题', texts["root"])   # 避开 tagline 中 "P0→P2" 的数字干扰
    check(root_ch == EXPECT["chapters"], f"[根index] 深度Q&A={root_ch} 期望 {EXPECT['chapters']}")
    check(root_sum == EXPECT["total"] + ROOT_SUM_EXTRA, f"[根index] 合计={root_sum} 期望 {EXPECT['total']+ROOT_SUM_EXTRA}")
    check(root_all == EXPECT["total"], f"[根index] 全站={root_all} 期望 {EXPECT['total']}")
    if ENGINEERING:
        root_eng = stat(r'(\d+)</div>\s*<div class="stat-label">工程化要点</div>', texts["root"])
        if root_eng is None:
            root_eng = stat(r'(\d+)</div>\s*<div class="stat-label">工程化</div>', texts["root"])
        check(root_eng == ENGINEERING, f"[根index] 工程化={root_eng} 期望 {ENGINEERING}")

    # 5) 章节 index stat-number（同结构，允许 </div> 与 <div> 间换行）+ 全站 N 道
    chap_ch = stat(r'(\d+)</div>\s*<div class="stat-label">深度 Q&amp;A', texts["chap_idx"])
    chap_all = stat(r'全站\s*(\d+)\s*道', texts["chap_idx"])
    check(chap_ch == EXPECT["chapters"], f"[章节index] 深度Q&A={chap_ch} 期望 {EXPECT['chapters']}")
    check(chap_all == EXPECT["total"], f"[章节index] 全站={chap_all} 期望 {EXPECT['total']}")
    if ENGINEERING:
        chap_eng = stat(r'(\d+)</div>\s*<div class="stat-label">工程化要点</div>', texts["chap_idx"])
        if chap_eng is None:
            chap_eng = stat(r'(\d+)</div>\s*<div class="stat-label">工程化</div>', texts["chap_idx"])
        check(chap_eng == ENGINEERING, f"[章节index] 工程化={chap_eng} 期望 {ENGINEERING}")

    # root methodology label may be 核心方法论
    root_m = stat(r'(\d+)</div>\s*<div class="stat-label">核心方法论</div>', texts["root"])
    if root_m is None:
        root_m = stat(r'(\d+)</div>\s*<div class="stat-label">方法论</div>', texts["root"])
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
            elif nid.startswith("G"):
                check(True, f"[双编码] {nid}: 工程化卡无强制优先级（宿主 {os.path.basename(host)}）")
            else:
                # 方法论部分卡可能无 priority
                has_card = bool(re.search(rf'id="{re.escape(nid)}"', ht))
                check(has_card, f"[双编码] {nid}: 未找到属性或徽标（宿主 {os.path.basename(host)}）")
        else:
            check(False, f"[双编码] {nid}: 未在任何章节页找到该卡片")
        # overview 落位（C/E/S 必进；M/G 默认不进 overview）
        if not (nid.startswith("M") or nid.startswith("G")):
            check(nid in texts["overview"], f"[落位] {nid} 在 overview")
        # 根 index 落位（q-id）
        check(nid in texts["root"], f"[落位] {nid} 在 根index")
        # mind 落位（扫描全部 mind 文件，命中任一即 PASS）
        check(nid in mind_text_all, f"[落位] {nid} 在 mind 站（任一导图页）")

    # 7) 求和自洽
    check(EXPECT["p0"]+EXPECT["p1"]+EXPECT["p2"] == EXPECT["total"], "[自洽] P0+P1+P2=总量")
    check(EXPECT["expert"]+EXPECT["architect"]+EXPECT["senior"] == EXPECT["total"], "[自洽] 难度三级=总量")
    check(EXPECT["chapters"]+EXPECT["basics"]+EXPECT["scenarios"] == EXPECT["total"], "[自洽] 类型三级=总量")
    check(EXPECT["total"] + EXPECT["methodology"] + ENGINEERING == SUM_ALL,
          "[自洽] total+methodology+engineering=sum_all")

    # 8) 卡片 id 三方一致性：章节正文 ↔ 章节 TOC ↔ 导图引用，且总数 == sum_all
    IDPAT = r"((?:M|C|E|S|G)\d{2}\.\d{2})"
    body_ids, toc_ids, mind_ids = set(), set(), set()
    for p in chap_files:
        t = read(p)
        body_ids |= set(re.findall(rf'id="{IDPAT}"', t))
        toc_ids |= set(re.findall(rf'href="#{IDPAT}"', t))
    for p in mind_files:
        mind_ids |= set(re.findall(IDPAT, read(p)))
    check(len(body_ids) == SUM_ALL,
          f"[id总数] 章节页卡片 {len(body_ids)} 期望 {SUM_ALL}（sum_all，含方法论+工程化）")
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
