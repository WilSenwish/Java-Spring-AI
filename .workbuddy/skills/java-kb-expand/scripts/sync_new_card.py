#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
java-kb-expand · 新增卡片 7 文件同步脚本骨架
===================================================
复制本文件到 java-architect-interview/tmp/，按需填 TODO 区（新增题号、卡片 HTML、计数增量、各文件锚点），
然后运行：python3 sync_new_card.py

设计要点（来自实战坑位）：
  - 先备份全部目标文件到 java-architect-interview/tmp/kb_<task>_backup/
  - 用精确字符串替换 + 断言（命中数=预期），规避 Edit 对 overview 大数字的"竞态未落盘"
  - 全程守卫 data-page-node-id == 0
  - 章节导航页（java-architect-interview/index.html）不枚举单题 ID，只改统计与 card-footer

本骨架仅给结构与辅助函数；具体锚点字符串请先用 Grep/Read 定位真实文本再填。
"""
import os, re, shutil, sys, datetime

BASE = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI"
TASK = "optx"  # TODO: 改成本轮任务标识，如 optc / opta_c13
BACKUP = f"{BASE}/java-architect-interview/tmp/kb_{TASK}_backup"
os.makedirs(BACKUP, exist_ok=True)

# ===================== TODO 区 =====================
# 已知真实文件名（避免猜错）：
#   篇章页 chapter-01~15-*.html / 方法论 chapter-core-methodology.html / 安全卡 chapter-server-security-checkpoint.html
#   核心原理页 chapter-questions-eight-part.html / 场景页 chapter-questions-scenario.html
#   导图页 mind-01~15-*.html / mind-core-methodology.html / mind-server-security-checkpoint.html
# 场景题 Sxx 的宿主章节页 = 其 group-N 对应的篇章（如 group-4 微服务架构 -> chapter-10-microservice-cloud.html / mind-10）
NEW_ID = "C13.13"          # 新增题号
NEW_CARD_HTML = """<!-- TODO: 完整卡片 HTML（含双编码 data-priority + 可见徽标）-->"""
CHAPTER_FILE = f"{BASE}/java-architect-interview/chapter-13-network-io.html"
MIND_FILE = f"{BASE}/java-architect-interview-mind/mind-13-network-io.html"
ANCHOR_INSERT_CARD = "<!-- ============ 章节间导航 ============ -->"  # TODO: 卡片插在此锚点前
ANCHOR_INSERT_MAPCARD = "</details>\n    <h3 class=\"theme-h\">②"      # TODO: map-card 插此前

# 计数增量（形式1/2/3 新增卡时填；形式4 补增量时全 0）
DELTA = {"total": 1, "p1": 1, "architect": 1, "chapters": 1}
# 当前 overview ov-stat-num 顺序（11 项）：
#   [total, p0, p1, p2, expert, architect, senior, methodology, chapters, basics, scenarios]
OV_BEFORE = [345, 90, 195, 60, 44, 160, 141, 74, 220, 58, 67]  # TODO: 填执行前实际值
# ==================================================

FILES = {
    "chapter": CHAPTER_FILE,
    "overview": f"{BASE}/java-architect-interview/chapter-overview-priority.html",
    "root": f"{BASE}/index.html",   # 注意：BASE 已含项目根 "Java Spring AI"，根 index 即 {BASE}/index.html
    "chap_idx": f"{BASE}/java-architect-interview/index.html",
    "mind": MIND_FILE,
    "mind_idx": f"{BASE}/java-architect-interview-mind/index.html",
}

def read(p): return open(p, encoding="utf-8").read()
def write(p, t): open(p, "w", encoding="utf-8").write(t)

def backup_all():
    for k, p in FILES.items():
        shutil.copy(p, f"{BACKUP}/{os.path.basename(p)}")
    print(f"backup -> {BACKUP}")

def replace_once(t, old, new, label, n=1):
    cnt = t.count(old)
    assert cnt == n, f"[{label}] 期望命中 {n} 次，实际 {cnt} 次：{old[:40]!r}"
    return t.replace(old, new, n)

def guard_dpni(t, label):
    c = t.count("data-page-node-id")
    assert c == 0, f"[{label}] data-page-node-id={c}（红线）"
    return t

# ---------- Step A: 章节页插入卡片 + meta ----------
def patch_chapter(t):
    # TODO: meta 题目数/难度计数/复习分钟 +N；TOC 加条目
    # 插入卡片（在导航锚点前）
    t = replace_once(t, ANCHOR_INSERT_CARD, NEW_CARD_HTML + "\n\n      " + ANCHOR_INSERT_CARD, "chapter-insert-card")
    return t

# ---------- Step B: overview 新增 ov-item + ov-stat-num ----------
def patch_overview(t):
    # TODO: 在对应位置插入 ov-item（NEW_ID 的 <div class="ov-item">…</div>）
    # ov-stat-num 用脚本精确替换（Edit 对此大数字可能竞态未落盘）
    ov = re.findall(r'ov-stat-num">(\d+)</div>', t)
    ov = [int(x) for x in ov[:11]]
    assert ov == OV_BEFORE, f"overview ov-stat-num 实际 {ov} != 预期 {OV_BEFORE}"
    after = [ov[i] + DELTA.get(k, 0) for i, k in enumerate(
        ["total","p0","p1","p2","expert","architect","senior","methodology","chapters","basics","scenarios"])]
    # 逐个数字替换（正向顺序替换，避免前导 0 误伤）
    for before_v, after_v in zip(OV_BEFORE, after):
        t = t.replace(f'ov-stat-num">{before_v}</div>', f'ov-stat-num">{after_v}</div>', 1)
    # TODO: 对应 优先级×难度 子组标题 +N（先算真实 9 宫格再对齐）
    return t

# ---------- Step C: 根 index + 章节 index + mind ----------
def patch_root(t):
    # TODO: 类型计数/合计/全站/dir-count +N；新增 q-item li（在对应 ID li 后）
    return t
def patch_chap_idx(t):
    # TODO: stat-number +N；全站 +N；章节 card-footer +N（不枚举单题 ID）
    return t
def patch_mind(t):
    # TODO: 主干范围扩尾；插 map-card（summary/body/tags）；meta +N
    t = replace_once(t, ANCHOR_INSERT_MAPCARD, "<!-- TODO: map-card -->\n    " + ANCHOR_INSERT_MAPCARD, "mind-insert-mapcard")
    return t
def patch_mind_idx(t):
    # TODO: 题量表达式 N+N+N 同步（方法论 74 不计入该表达式）
    return t

def main():
    backup_all()
    patches = {
        "chapter": patch_chapter, "overview": patch_overview, "root": patch_root,
        "chap_idx": patch_chap_idx, "mind": patch_mind, "mind_idx": patch_mind_idx,
    }
    for k, fn in patches.items():
        t = read(FILES[k])
        t = fn(t)
        t = guard_dpni(t, k)
        write(FILES[k], t)
        print(f"patched: {k}")
    print("\n全部文件已写入，data-page-node-id 守卫通过。请随后运行 validate_kb.py 做三源一致性校验。")

if __name__ == "__main__":
    main()
