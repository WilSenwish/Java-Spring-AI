#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
java-kb-expand · 新增卡片 7 文件同步脚本骨架
===================================================
复制本文件到 tmp/，按需填 TODO 区（新增题号、卡片 HTML、计数增量、各文件锚点），
然后运行：python3 sync_new_card.py

设计要点（来自实战坑位）：
  - 先备份全部目标文件到 tmp/kb_<task>_backup/
  - 用精确字符串替换 + 断言（命中数=预期），规避 Edit 对 overview 大数字的"竞态未落盘"
  - 全程守卫 data-page-node-id == 0
  - 章节导航页（java-architect-interview/index.html）不枚举单题 ID，只改统计与 card-footer

本骨架仅给结构与辅助函数；具体锚点字符串请先用 Grep/Read 定位真实文本再填。
"""
import os, re, shutil, sys, datetime, json

BASE = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI"
TASK = "optx"  # TODO: 改成本轮任务标识，如 optc / opta_c13
BACKUP = f"{BASE}/tmp/kb_{TASK}_backup"
os.makedirs(BACKUP, exist_ok=True)

# ============ 必同步清单（2026-09-15 新增 4 卡实测，漏一处即 validate_kb FAIL）============
# 宿主页（chapter-*.html）
#   [1] 卡片本体：C/E/S 卡必带双编码（data-priority + 可见 priority-pX 徽标）；G/K 卡按组体例
#   [2] 页头 <div class="chapter-meta">：题目数 + 高级开发×N / 架构级×N / 专家级×N
#       —— 不在 SSOT positions 内，必须手工改；
#          由 validate_kb「0d) 页头难度」按「本页实体卡片」自证拦截（不依赖 SSOT）
#   [3] 侧栏 TOC <li><a href="#ID">…</a></li>
#       —— ⚠ 场景页 chapter-questions-scenario.html 与 E 页同样有 TOC；漏加 → FAIL [TOC缺失]
# 根 index（{BASE}/index.html）
#   [4] q-item 必须【独立 li 包裹】：
#         <li class="q-item">
#           <a href="…#ID">…</a><span class="q-tags">…</span>
#         </li>
#       ✗ 高频错误：把新 <a> 追加到既有 q-item 的 <a> 之后 → 落在同一 li 内，
#         <li class="q-item"> 计数不增 → FAIL [根index dir-count] 计数≠列表
#   [5] 对应 dir-group-count / dir-count 增量（struct.root.dir_group_N / struct.root.dir_count_N）
# overview（nav-overview-priority.html）
#   [6] ov-item 插到正确的「优先级 × 难度」子组，子组内按 C(0) → E(1) → S(2)、题号升序
#   [7] 三级计数同改：ov-stat-num（struct.ov.subgroup_*）、ov-type-count（struct.ov.type_*）、
#       组标题题数（p0/p1/p2）。漏 ov-type-count → FAIL [overview类型计数]
#       （ov-type 为每个难度子组内的「篇章/核心原理/场景题」三分块，易被整体忽略）
# 章节 index（java-architect-interview/index.html）
#   [8] c{NN}.n / c{NN}.expert / c{NN}.architect（struct.chap.idx.*）；不枚举单题 ID
# mind 站（一处漏改即「导图与正文不同步」，validate_kb 查不出，必须人工双改）
#   [9] 对应 mind-NN 页须改【四处】，缺任一即不同步：
#       (a) 主干范围句（如「主干 C11.01–C11.28」→ C11.30）
#       (b) 主题卡 <details class="map-card"><summary>ID 简称</summary>…（体例对齐同组兄弟卡）
#       (c) ⚠ Mermaid 图节点：<div class="mermaid"> 内的 `tN --> nNNN["简称"]`。
#           实测 2026-09-15：新增 4 卡时只补了 (a)(b)，漏 (c)，
#           导致 mind-11 缺 C11.29/C11.30、mind-engineering-practices 缺 G07.09。
#           导图 Mermaid 是「本篇章卡的全量列点」——章节 +N 张卡，图里就必须 +N 个节点。
#           节点 id 保持在分支内递增；插在交叉卡（E/S）节点之前，与原卡序一致；
#           若需插队在既有 id 之前，把后续节点 id 顺延（如 n113 → n115），
#           mermaid 节点 id 不被其它位置引用，重编安全。
#       (d) mind index 的 card-foot（struct.mind.idx.mind-foot-c_N / -e_N / -s_N）
#       ⚠ S 场景卡并入其所属篇章的 mind 页（如 S12.x → mind-12-ai-engineering.html），
#         不存在独立的 mind 场景页
#       ⚠⚠ E 核心原理卡同样并入「其所属篇章」的 mind 页（2026-09-20 实测）：
#         如 E03.09 → mind-03-concurrency-locks.html。E 卡不是只进 eight-part 页——
#         mind-foot-e_N 校验 = 该 mind 页 <summary> 里的 E 号集合数，漏补则
#         validate_kb「[mind card-foot] 与篇章/summary 不一致」FAIL。
#       ⚠⚠ 一个 mind 页有【两个】<div class="mermaid">：block0=flowchart（`tN --> nNNN["简称"]`）、
#         block1=mindmap（纯文本行 `C14.13 慢 SQL…`）。新卡【两处都要加节点】。
#         （2026-09-20 更新）check_mind_mermaid 已改为**逐块取标签**（flowchart 方括号标签
#         + mindmap 裸文本行），故它只能判「两块都缺该卡」——**两块彼此不一致它查不出来**
#         （任一图有即 PASS）。因此「两处都改」属人工纪律，不可再依赖该门禁兜底。
# 收尾
#   [10] sync_counts.py bump（counts 与 struct.* 一并传参）→ check 全 PASS
#   [11] validate_kb.py 的 NEW_IDS 补入本轮新题号 → 全量校验 ALL PASS
#   【能拦住 TOC / overview 类型 / 页头难度 / dir-count 漂移的只有 validate_kb.py；
#     sync_counts.py check 只校验 SSOT 已声明的计数位，新增结构漏同步它发现不了】
# =====================================================================================

# ===================== TODO 区 =====================
# 已知真实文件名（避免猜错）：
#   篇章页 chapter-01~15-*.html / 方法论 chapter-core-methodology.html / 安全卡 nav-server-security-checkpoint.html
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
# 执行前 overview ov-stat-num（11 项）：取自单一真源 kb-counts.json，禁止硬编码
#   [total, p0, p1, p2, expert, architect, senior, methodology, chapters, basics, scenarios]
_cfg = json.load(open(f"{BASE}/docs/kb-counts.json", encoding="utf-8"))
OV_KEYS = list(_cfg["ov_stat_order"])
OV_BEFORE = [_cfg["counts"][k] for k in OV_KEYS]
# ==================================================

FILES = {
    "chapter": CHAPTER_FILE,
    "overview": f"{BASE}/java-architect-interview/nav-overview-priority.html",
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
    # 插入位置硬约束（conventions.md §5.1.1）：
    #   #group-p{N} → 对应难度 subgroup；子组内按 (C=0,E=1,S=2, 题号) 升序插入
    #   同步：子组 ·N 题、组标题 ·N 题、ov-nav-cnt、ov-stat-num、页头「全站 N 道」
    # 禁止：插在「同 priority 任意兄弟卡」后（会破坏 E 题号升序 / C→E→S）
    # TODO: 在正确排序位置插入 ov-item（NEW_ID 的 <a class="ov-item">…</a>）
    # ov-stat-num 用脚本精确替换（Edit 对此大数字可能竞态未落盘）
    ov = re.findall(r'ov-stat-num">(\d+)</div>', t)
    ov = [int(x) for x in ov[:11]]
    assert ov == OV_BEFORE, f"overview ov-stat-num 实际 {ov} != 预期 {OV_BEFORE}"
    after = [ov[i] + DELTA.get(k, 0) for i, k in enumerate(OV_KEYS)]
    # 逐个数字替换（正向顺序替换，避免前导 0 误伤）
    for before_v, after_v in zip(OV_BEFORE, after):
        t = t.replace(f'ov-stat-num">{before_v}</div>', f'ov-stat-num">{after_v}</div>', 1)
    # TODO: 对应 优先级×难度 子组标题 +N（先算真实 9 宫格再对齐）
    return t

# ---------- Step C: 根 index + 章节 index + mind ----------
def patch_root(t):
    # TODO: 类型计数/全站(=total)/dir-count +N（禁跨域合计）；新增 q-item li（在对应 ID li 后）
    return t
def patch_chap_idx(t):
    # TODO: stat-number +N；全站(=total)+N；章节 card-footer +N（不枚举单题 ID）
    return t
def patch_mind(t):
    # TODO: 主干范围扩尾；插 map-card（summary/body/tags）；meta +N
    t = replace_once(t, ANCHOR_INSERT_MAPCARD, "<!-- TODO: map-card -->\n    " + ANCHOR_INSERT_MAPCARD, "mind-insert-mapcard")
    return t
def patch_mind_idx(t):
    # TODO: 题量表达式 N+N+N 同步（方法论/工程化不计入该表达式）
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
