#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
java-kb-expand · 全量校验脚本（通用版）
==============================================
复制本文件到 java-architect-interview/tmp/，按需填 EXPECT 字典（本轮权威计数）与 NEW_IDS（新增/改动题号列表），
然后运行：python3 validate_kb.py

校验项：
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
import re, sys, os, glob

BASE = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI"
CHAPTER_DIR = f"{BASE}/java-architect-interview"
MIND_DIR = f"{BASE}/java-architect-interview-mind"

# ====== 待填：本轮权威计数（与 references/conventions.md §6 同口径）======
EXPECT = {
    "total": 345, "p0": 90, "p1": 195, "p2": 60,
    "expert": 44, "architect": 160, "senior": 141,
    "methodology": 75,
    "chapters": 220, "basics": 58, "scenarios": 67,
}
# 根 index 合计 = 题数 + 方法论卡片数（75）
ROOT_SUM_EXTRA = 75

# ====== 待填：本轮新增/改动题号（用于落位+双编码校验）======
NEW_IDS = ["C10.26"]  # 例：["C13.13"] 或 ["C10.26", "S04.06"]

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

def main():
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

    # 3) overview ov-stat-num 顺序（11 项）：
    #    total,p0,p1,p2,expert,architect,senior,methodology,chapters,basics,scenarios
    ov = re.findall(r'ov-stat-num">(\d+)</div>', texts["overview"])
    ov = [int(x) for x in ov[:11]]
    expect_order = [EXPECT["total"], EXPECT["p0"], EXPECT["p1"], EXPECT["p2"],
                    EXPECT["expert"], EXPECT["architect"], EXPECT["senior"],
                    EXPECT["methodology"], EXPECT["chapters"],
                    EXPECT["basics"], EXPECT["scenarios"]]
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

    # 5) 章节 index stat-number（同结构，允许 </div> 与 <div> 间换行）+ 全站 N 道
    chap_ch = stat(r'(\d+)</div>\s*<div class="stat-label">深度 Q&amp;A', texts["chap_idx"])
    chap_all = stat(r'全站\s*(\d+)\s*道', texts["chap_idx"])
    check(chap_ch == EXPECT["chapters"], f"[章节index] 深度Q&A={chap_ch} 期望 {EXPECT['chapters']}")
    check(chap_all == EXPECT["total"], f"[章节index] 全站={chap_all} 期望 {EXPECT['total']}")

    # 6) 新卡双编码 + 落位（按题号前缀自动定位宿主章节页）
    chap_text_all = "\n@@@\n".join(read(p) for p in chap_files)
    mind_text_all = "\n@@@\n".join(read(p) for p in mind_files)
    for nid in NEW_IDS:
        # 双编码：在宿主章节页（含该 ID 的 chapter 文件）找 data-priority 属性 + 可见 priority-pX
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
            else:
                check(False, f"[双编码] {nid}: 未找到属性或徽标（宿主 {os.path.basename(host)}）")
        else:
            check(False, f"[双编码] {nid}: 未在任何章节页找到该卡片")
        # overview 落位
        check(nid in texts["overview"], f"[落位] {nid} 在 overview")
        # 根 index 落位（q-id）
        check(nid in texts["root"], f"[落位] {nid} 在 根index")
        # mind 落位（扫描全部 mind 文件，命中任一即 PASS）
        check(nid in mind_text_all, f"[落位] {nid} 在 mind 站（任一导图页）")

    # 7) 求和自洽
    check(EXPECT["p0"]+EXPECT["p1"]+EXPECT["p2"] == EXPECT["total"], "[自洽] P0+P1+P2=总量")
    check(EXPECT["expert"]+EXPECT["architect"]+EXPECT["senior"] == EXPECT["total"], "[自洽] 难度三级=总量")
    check(EXPECT["chapters"]+EXPECT["basics"]+EXPECT["scenarios"] == EXPECT["total"], "[自洽] 类型三级=总量")

    print("\n==== 校验结果 ====")
    if check.failed == 0:
        print("ALL PASS ✅ 三权威源一致，data-page-node-id=0，新卡落位且双编码一致。")
        sys.exit(0)
    else:
        print(f"存在 {check.failed} 项 FAIL ❌，请复查。")
        sys.exit(1)

if __name__ == "__main__":
    main()
