#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
java-kb-expand · 权威计数同步工具（单一真源驱动）
=====================================================
真源：docs/kb-counts.json
消费：站点展示位（HTML）、docs 三份 md、脚本常量、四份文档锚点块

命令：
  python3 sync_counts.py show                      查看当前权威计数与自洽校验
  python3 sync_counts.py check                     比对全部计数位实际值 vs 真源（只读）
  python3 sync_counts.py apply                     把真源写回全部计数位（自动备份）
  python3 sync_counts.py bump methodology=+1 total=+1   改数 + 写回 + 复核（一条龙）
  python3 sync_counts.py bump struct.chap.idx.c01.n=+1  结构键同语法（前缀 struct.）
  python3 sync_counts.py render                    渲染三份文档的 COUNTS 锚点块

设计要点：
  - 真源分 counts（全局）与 struct（结构/分组）；禁止页面 kb-count-local
  - 每个 position 命中数必须等于期望（nth），命中 0 或多处即中止，杜绝误替换
  - apply 前自动备份到 tmp/counts_apply_backup/<时间戳>/
  - 全程守卫 data-page-node-id == 0（改 HTML 的红线）
"""
import json, os, re, sys, shutil, datetime, argparse

BASE = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI"
COUNTS_JSON = f"{BASE}/docs/kb-counts.json"
BACKUP_ROOT = f"{BASE}/tmp/counts_apply_backup"

# 渲染目标：这三份是「跨工具常驻规则 + 技能正文」，需要内联完整计数位表。
# `.workbuddy/memory/MEMORY.md` **不在其中** —— 它按体积上限（~3KB 每轮注入）已收敛为
# 指针版，不含 COUNTS:BEGIN/END 锚点块；计数摘要由 AGENTS.md 承载，MEMORY.md 只留
# 「权威清单 = docs/kb-counts.json 的 positions」这类指针，故不再尝试渲染（否则永久 WARN）。
RENDER_TARGETS = [
    f"{BASE}/AGENTS.md",
    f"{BASE}/.workbuddy/skills/java-kb-expand/SKILL.md",
    f"{BASE}/.workbuddy/skills/java-kb-expand/references/conventions.md",
]
COMPACT_TARGETS = set()
BEGIN = "<!-- COUNTS:BEGIN 由 scripts/sync_counts.py render 生成，勿手改 -->"
END = "<!-- COUNTS:END -->"


def load():
    return json.load(open(COUNTS_JSON, encoding="utf-8"))


def save(cfg):
    cfg["updated"] = datetime.date.today().isoformat()
    open(COUNTS_JSON, "w", encoding="utf-8").write(
        json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, t):
    open(p, "w", encoding="utf-8").write(t)


def guard_dpni(t, label):
    c = t.count("data-page-node-id")
    assert c == 0, f"[{label}] data-page-node-id={c}（红线，禁止写入）"
    return t


def backup(files):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    d = f"{BACKUP_ROOT}/{ts}"
    os.makedirs(d, exist_ok=True)
    for p in files:
        shutil.copy(p, f"{d}/{os.path.basename(p)}")
    return d


# ---------------- 读取实际值 ----------------
def actual_values(cfg, pos, t):
    """返回 (list[int], list[match])：实际值与对应匹配对象"""
    pat, kind = pos["pattern"], pos.get("kind", "number")
    if kind == "ov_series":
        ms = list(re.finditer(pat, t))
        return [int(m.group(pos.get("group", 1))) for m in ms], ms
    if kind == "ov_array":
        ms = list(re.finditer(pat, t))
        if not ms:
            return [], []
        nums = re.findall(r"\d+", ms[0].group(0))
        return [int(x) for x in nums], ms
    g, nth = pos.get("group", 1), pos.get("nth", 1)
    ms = list(re.finditer(pat, t))
    if len(ms) < nth:
        return [], []
    m = ms[nth - 1]
    return [int(m.group(g))], [m]


def resolve_key(cfg, key):
    """Resolve counts.X or struct.X (or bare counts key) to int."""
    if key.startswith("struct."):
        sk = key[len("struct.") :]
        assert "struct" in cfg and sk in cfg["struct"], f"未知 struct 键：{sk}"
        return cfg["struct"][sk]
    if key.startswith("counts."):
        ck = key[len("counts.") :]
        assert ck in cfg["counts"], f"未知 counts 键：{ck}"
        return cfg["counts"][ck]
    assert key in cfg["counts"], f"未知计数键：{key}"
    return cfg["counts"][key]


def expect_values(cfg, pos):
    kind = pos.get("kind", "number")
    if kind == "ov_series":
        return [cfg["counts"][k] for k in cfg["ov_stat_order"]]
    if kind == "ov_array":
        return [cfg["counts"][k] for k in cfg["ov_stat_order"]]
    return [resolve_key(cfg, pos["key"])]


# ---------------- 写回 ----------------
def apply_one(t, pos, new_vals):
    """按 position 把 new_vals 写回文本，返回新文本"""
    pat, kind = pos["pattern"], pos.get("kind", "number")
    if kind == "ov_series":
        ms = list(re.finditer(pat, t))
        assert len(ms) == len(new_vals), f"[{pos['id']}] ov 项数 {len(ms)} != 期望 {len(new_vals)}"
        for m, v in reversed(list(zip(ms, new_vals))):
            s, e = m.span(pos.get("group", 1))
            t = t[:s] + str(v) + t[e:]
        return t
    if kind == "ov_array":
        ms = list(re.finditer(pat, t))
        assert len(ms) == 1, f"[{pos['id']}] OV_BEFORE 命中 {len(ms)} 次，须 1 次"
        new_line = "OV_BEFORE = [" + ", ".join(str(v) for v in new_vals) + "]"
        s, e = ms[0].span(0)
        return t[:s] + new_line + t[e:]
    g, nth = pos.get("group", 1), pos.get("nth", 1)
    ms = list(re.finditer(pat, t))
    assert len(ms) >= nth, f"[{pos['id']}] 命中 {len(ms)} 次，少于 nth={nth}"
    m = ms[nth - 1]
    s, e = m.span(g)
    return t[:s] + str(new_vals[0]) + t[e:]


# ---------------- 命令 ----------------
def cmd_show(cfg):
    c = cfg["counts"]
    print(f"真源：{COUNTS_JSON}  (updated {cfg['updated']})")
    print(f"  题目总量 {c['total']} = 篇章 {c['chapters']} + 核心原理 {c['basics']} + 场景 {c['scenarios']}")
    print(f"  优先级    P0={c['p0']} / P1={c['p1']} / P2={c['p2']}")
    print(f"  难度      专家={c['expert']} / 架构师={c['architect']} / 高级开发={c['senior']}  (仅 C/E/S)")
    print(f"  方法论    {c['methodology']} 卡（带优先级 {c['methodology_with_priority']}；不分难度等级）")
    print(f"  工程化    {c.get('engineering', 0)} 卡（专篇，不分难度等级）")
    print(f"  生产踩坑  {c.get('pitfalls', 0)} 卡（专篇，不分难度等级）")
    print(f"  struct    {len(cfg.get('struct') or {})} 键（结构/分组计数）")
    print("  （聚合口径仅篇章+核心原理+场景=total；M/G/K 专篇单独键且不做难度分级）")
    ok = True
    for inv in cfg["invariants"]:
        r = eval(inv["expr"], {}, dict(c))
        print(f"  {'PASS' if r else 'FAIL'} [自洽] {inv['desc']}")
        ok &= bool(r)
    return 0 if ok else 1


def cmd_check(cfg, verbose=True):
    bad = 0
    for pos in cfg["positions"]:
        p = os.path.join(BASE, pos["file"])
        if not os.path.isfile(p):
            print(f"FAIL [{pos['id']}] 文件缺失：{pos['file']}")
            bad += 1
            continue
        t = read(p)
        act, ms = actual_values(cfg, pos, t)
        exp = expect_values(cfg, pos)
        if not ms:
            print(f"FAIL [{pos['id']}] 正则未命中（锚点失效，需修 pattern）：{pos['file']}")
            bad += 1
            continue
        if act != exp:
            print(f"FAIL [{pos['id']}] {pos['file']}：实际 {act} != 期望 {exp}  ({pos['desc']})")
            bad += 1
        elif verbose:
            print(f"PASS [{pos['id']}] {act}  ({pos['desc']})")
    print("-" * 60)
    print(f"check 结果：{len(cfg['positions']) - bad}/{len(cfg['positions'])} 通过"
          + (" ✅ 真源与站点完全一致" if bad == 0 else f" ❌ {bad} 处不一致"))
    return 0 if bad == 0 else 1


def cmd_apply(cfg):
    targets = sorted({os.path.join(BASE, p["file"]) for p in cfg["positions"]})
    d = backup(targets)
    print(f"备份 -> {d}")
    # 按文件聚合，逐文件一次性写入（同文件多 position 顺序处理）
    by_file = {}
    for pos in cfg["positions"]:
        by_file.setdefault(os.path.join(BASE, pos["file"]), []).append(pos)
    changed = []
    for f, poss in by_file.items():
        t = read(f)
        orig = t
        for pos in poss:
            act, ms = actual_values(cfg, pos, t)
            exp = expect_values(cfg, pos)
            if act == exp:
                continue
            assert ms, f"[{pos['id']}] 锚点失效，拒绝写入"
            t = apply_one(t, pos, exp)
        if t != orig:
            if f.endswith(".html"):
                guard_dpni(t, os.path.basename(f))
            write(f, t)
            changed.append(os.path.relpath(f, BASE))
    print(f"已写回 {len(changed)} 个文件：" + (", ".join(changed) if changed else "（无差异，未改动）"))
    return cmd_check(cfg, verbose=False)


def cmd_bump(cfg, assigns):
    c = cfg["counts"]
    struct = cfg.setdefault("struct", {})
    # snapshot for rollback
    snap_c = dict(c)
    snap_s = dict(struct)
    for a in assigns:
        k, v = a.split("=", 1)
        if k.startswith("struct."):
            sk = k[len("struct.") :]
            assert sk in struct, f"未知 struct 键：{sk}"
            cur = struct[sk]
            struct[sk] = cur + int(v) if v[0] in "+-" else int(v)
        else:
            assert k in c, f"未知计数键：{k}（可选：{', '.join(c)} 或 struct.*）"
            cur = c[k]
            c[k] = cur + int(v) if v[0] in "+-" else int(v)
    ok = True
    for inv in cfg["invariants"]:
        r = eval(inv["expr"], {}, dict(c))
        if not r:
            print(f"FAIL [自洽] {inv['desc']} —— 已回滚，未写入")
            ok = False
    if not ok:
        cfg["counts"] = snap_c
        cfg["struct"] = snap_s
        return 1
    save(cfg)
    print(f"真源已更新：{' '.join(assigns)}")
    rc = cmd_apply(cfg)
    print()
    cmd_render(cfg)   # 同步刷新四份文档的 COUNTS 锚点块
    return rc


def render_block(cfg, compact=False):
    c = cfg["counts"]
    lines = [
        BEGIN,
        f"- 题目总量 **{c['total']}** = 篇章 {c['chapters']} + 核心原理 {c['basics']} + 场景 {c['scenarios']}",
        f"- 优先级 **P0={c['p0']} / P1={c['p1']} / P2={c['p2']}**（求和 = {c['total']}）",
        f"- 难度 **专家 {c['expert']} / 架构师 {c['architect']} / 高级开发 {c['senior']}**（求和 = {c['total']}；仅覆盖 C/E/S，M/G/K 不分级）",
        f"- 方法论 **{c['methodology']} 卡**（M01~M17：道 M01–M02 / 法 M03–M07 / 术 M08–M15 / 势 M16 / 附 M17，专篇键 methodology；**不分难度等级**）",
        f"- 工程化 **{c.get('engineering', 0)} 卡**（G01~G08，专篇键 engineering；**不分难度等级**）",
        f"- 生产踩坑 **{c.get('pitfalls', 0)} 卡**（K01~K08，专篇键 pitfalls；**不分难度等级**）",
        f"- 口径（程序约束）：题目总量 total=篇章+核心原理+场景；M/G/K 为专篇键，不进 total；结构计数见 struct；**禁止 kb-count-local；禁止页面用自然语言声明口径**",
        f"- 方法论细分：带优先级 {c['methodology_with_priority']}/{c['methodology']}（2026-09-16 起 M/G/K 不设难度计数）",
    ]
    if compact:
        ids = [p["id"].split("_")[0] for p in cfg["positions"]]
        files = sorted({p["file"] for p in cfg["positions"]})
        lines += [
            "",
            f"- **计数位清单（{len(ids)} 项，{ids[0]}~{ids[-1]}，覆盖 {len(files)} 个文件）不在此展开**："
            f"权威清单 = `docs/kb-counts.json` 的 `positions`（唯一写源）；完整表格见项目根 `AGENTS.md` 同名块。",
            "- 核对/改数一律用脚本，**勿手工维护本块**：只读核对 `sync_counts.py check`；"
            "改数唯一入口 `sync_counts.py bump <key>=<±n>`（自动写回全部计数位 + 刷新本块）。",
        ]
    else:
        lines += [
            "",
            "计数位（改数须全部同步，由 sync_counts.py check 自动核查）：",
            "",
            "| 编号 | 载体 | 说明 |",
            "|---|---|---|",
        ]
        for pos in cfg["positions"]:
            lines.append(f"| {pos['id'].split('_')[0]} | `{pos['file']}` | {pos['desc']} |")
    lines.append(END)
    return "\n".join(lines)


def cmd_render(cfg):
    pat = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    d = backup([p for p in RENDER_TARGETS if os.path.isfile(p)])
    print(f"备份 -> {d}")
    for f in RENDER_TARGETS:
        if not os.path.isfile(f):
            print(f"SKIP 缺失：{f}")
            continue
        t = read(f)
        if BEGIN in t and END in t:
            block = render_block(cfg, compact=(f in COMPACT_TARGETS))
            t2 = pat.sub(lambda m: block, t, count=1)
        else:
            print(f"WARN 未找到锚点块，跳过（需先手工插入 BEGIN/END 标记）：{f}")
            continue
        if t2 != t:
            write(f, t2)
            print(f"rendered{'(compact)' if f in COMPACT_TARGETS else ''}: {os.path.relpath(f, BASE)}")
        else:
            print(f"unchanged: {os.path.relpath(f, BASE)}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="权威计数同步工具")
    ap.add_argument("cmd", choices=["show", "check", "apply", "bump", "render"])
    ap.add_argument("assigns", nargs="*", help="bump 用：key=+N / key=-N / key=N")
    a = ap.parse_args()
    cfg = load()
    if a.cmd == "show":
        sys.exit(cmd_show(cfg))
    if a.cmd == "check":
        sys.exit(cmd_check(cfg))
    if a.cmd == "apply":
        sys.exit(cmd_apply(cfg))
    if a.cmd == "bump":
        if not a.assigns:
            print("bump 需要参数，例：bump methodology=+1 total=+1")
            sys.exit(1)
        sys.exit(cmd_bump(cfg, a.assigns))
    if a.cmd == "render":
        sys.exit(cmd_render(cfg))


if __name__ == "__main__":
    main()
