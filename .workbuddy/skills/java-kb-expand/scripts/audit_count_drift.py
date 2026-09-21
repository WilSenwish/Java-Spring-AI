#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 计数漂移反向审计（数据驱动 · 全域）

背景（2026-09-21 血泪）：`sync_counts.py check` 只做「SSOT 键 ↔ DOM 取值」的**逐位一致性**，
查不出两类缺陷：
  ① **键值本身漂移**——键与 DOM 同为旧值，check 全绿，却 ≠ 页面真实卡数
     （实测：meta_1/2/4=22 应为 29、theme_1/2/4=45 应为 50、table_1/2/3=15/7/3 应为 16/13/7、
       meth-groups_1=16 应为 17、mind-foot-meta_1=16 应为 17）；
  ② **data-kb-pos 跨文件重复 / 未登记**——check 按 position 的 `file` 字段过滤，
     重复位在「非登记文件」里完全不校验（实测：mind 页误复用章节页 P405/P404）。

设计红线（2026-09-21，长官指令「门禁脚本得针对全局或接收参数，不能固定写死部分编码等」）：
  本脚本**不得写死任何组号区间、文件名、白名单、单位词**。全部读 SSOT：
    层归属（range + sum_keys）→ `guard.layers`
    单值键来源              → `guard.single_source`
    允许多点位              → `guard.pos_allow_multi`
    全局忽略目录            → `guard.exclude`（含 rk/ 软考资料站）
  组卡数实测源 = **全站自动识别**「含 qa-card 的文件」，不指定任何文件名。

四条链路互证：宿主页实际 qa-card 数 → SSOT 键值 → DOM 取值 → position 全局唯一且全部已登记。

用法：
  python3 scripts/audit_count_drift.py [项目根] [--only <glob>] [--quiet]
  退出码：0=全通过；1=有漂移（逐条给修复命令）；2=定位失败。
"""
import argparse
import collections
import glob
import io
import json
import os
import re
import sys


def find_root(start):
    """不写死项目根层级：从起点向上找「同时含 AGENTS.md 与 index.html」的目录。"""
    d = os.path.abspath(start)
    while d != "/":
        if os.path.isfile(os.path.join(d, "AGENTS.md")) and os.path.isfile(os.path.join(d, "index.html")):
            return d
        d = os.path.dirname(d)
    return None


ap = argparse.ArgumentParser(description="计数漂移反向审计（数据驱动 · 全域）")
ap.add_argument("root", nargs="?", default=None, help="项目根（缺省自动定位）")
ap.add_argument("--only", default=None, help="限定扫描 glob（相对项目根，仅调试用）")
ap.add_argument("--quiet", action="store_true", help="只输出结论行")
args = ap.parse_args()

ROOT = os.path.abspath(args.root) if args.root else find_root(os.path.dirname(os.path.abspath(__file__)))
if not ROOT:
    print("定位失败：未找到同时含 AGENTS.md 与 index.html 的祖先目录")
    sys.exit(2)
ROOT = os.path.abspath(ROOT)

SSOT = os.path.join(ROOT, "docs", "kb-counts.json")
if not os.path.isfile(SSOT):
    print("定位失败：缺少 %s" % SSOT)
    sys.exit(2)

cfg = json.load(io.open(SSOT, encoding="utf-8"))
S, C, POS = cfg["struct"], cfg["counts"], cfg["positions"]
G = cfg.get("guard") or {}
LAYERS = G.get("layers") or []
SINGLE = G.get("single_source") or {}
ALLOW_MULTI = set(G.get("pos_allow_multi") or [])
EXCLUDE = G.get("exclude") or ["tmp/", "node_modules/", "rk/"]

errs = []
warns = []


def excluded(rel):
    return any(rel == e.rstrip("/") or rel.startswith(e) for e in EXCLUDE)


def scan_files(exts):
    out = []
    for ext in exts:
        for p in glob.glob(os.path.join(ROOT, "**", "*." + ext), recursive=True):
            rel = os.path.relpath(p, ROOT)
            if excluded(rel):
                continue
            out.append((rel, p))
    if args.only:
        out = [(rel, p) for rel, p in out if glob.fnmatch.fnmatch(rel, args.only)]
    return sorted(set(out))


# ---------------- 1) 实测：全站 qa-card 数（自动识别宿主页，不写死文件名） ----------------
CARD_RE = re.compile(r'<div class="qa-card"\s+id="(M\d\d\.\d\d)"')
cards = {}          # id -> rel（首个定义文件）
dups = []
hosts = collections.Counter()
for rel, p in scan_files(["html"]):
    t = io.open(p, encoding="utf-8", errors="ignore").read()
    for m in CARD_RE.finditer(t):
        cid = m.group(1)
        hosts[rel] += 1
        if cid in cards and cards[cid] != rel:
            dups.append("%s 在 %s 与 %s 重复定义" % (cid, cards[cid], rel))
        cards.setdefault(cid, rel)
if not cards:
    print("定位失败：全站未解析出任何 qa-card（M##.##）")
    sys.exit(2)

actual = collections.Counter(cid[:3] for cid in cards)      # 'M01' -> n
GN = len(actual)
TOTAL = sum(actual.values())
for d in dups:
    errs.append("卡片重复定义：%s" % d)

if not args.quiet:
    print("实测：%d 组 / %d 卡；宿主页 %s"
          % (GN, TOTAL, ", ".join("%s(%d)" % (r, n) for r, n in sorted(hosts.items()))))
    print("      %s" % "  ".join("%s=%d" % (k, actual[k]) for k in sorted(actual)))


def chk(key, val, hint, scope=None):
    """比对 struct 键（key 无 struct. 前缀）与实测值。"""
    cur = S.get(key)
    if cur == val:
        return
    if isinstance(cur, int) and isinstance(val, int):
        errs.append('%-46s 当前=%-5s 应为=%-5s  →  sync_counts.py bump %s%s=%+d'
                    % (scope + "." + key if scope else key, cur, val,
                       scope + "." if scope else "", key, val - cur))
    else:
        errs.append("%-46s 当前=%s 应为=%s（%s）" % (key, cur, val, hint))


# 2) 组卡数键：通用正则识别 meth.group_<n> —— 不写死组号范围
for k in S:
    m = re.fullmatch(r"meth\.group_(\d+)", k)
    if m:
        chk(k, actual.get("M%02d" % int(m.group(1)), 0), "组卡数")

# 3) 层合计键：range + sum_keys 全部来自 SSOT guard.layers
for L in LAYERS:
    a, b = L["range"]
    val = sum(actual.get("M%02d" % g, 0) for g in range(a, b + 1))
    for k in L.get("sum_keys") or []:
        chk(k, val, "%s层合计（组 %d–%d）" % (L.get("label", L.get("id")), a, b))

# 4) 组卡数对照表键：通用正则 meth.table_<n>
for k in S:
    m = re.fullmatch(r"meth\.table_(\d+)", k)
    if m:
        chk(k, actual.get("M%02d" % int(m.group(1)), 0), "组卡数对照表")

# 5) 单值键（来源由 SSOT guard.single_source 声明，脚本不写死键名）
#    键可写成 `meth.x`（落 struct）或 `counts.x`；脚本按存在性自动判归属。
for k, kind in SINGLE.items():
    val = {"group_count": GN, "card_total": TOTAL}.get(kind)
    if val is None:
        errs.append("guard.single_source 声明了未知来源类型 «%s»（键 %s）" % (kind, k))
        continue
    sk = k[len("struct."):] if k.startswith("struct.") else k
    ck = k[len("counts."):] if k.startswith("counts.") else k
    if sk in S:
        chk(sk, val, "单值键(%s)" % kind)
    elif ck in C:
        if C.get(ck) != val:
            errs.append("%-46s 当前=%s 应为=%s  →  sync_counts.py bump counts.%s=%+d"
                        % (ck, C.get(ck), val, ck, val - (C.get(ck) or 0)))
    else:
        errs.append("guard.single_source 声明的键 «%s» 在 SSOT 中不存在" % k)

# 6) 总卡数
if C.get("methodology") != TOTAL:
    errs.append("counts.methodology 当前=%s 应为=%s  →  sync_counts.py bump methodology=%+d"
                % (C.get("methodology"), TOTAL, TOTAL - (C.get("methodology") or 0)))

# ---------------- 6b) 结构性派生计数（真源 = 宿主页 DOM 可见元素数） ----------------
# 这类数字不是「卡片数」（如 layer-hang 下挂 chip 数），真源无法由 qa-card 推出，
# 故由 SSOT `guard.derived` 声明：region 取块 → count 计数 = 真值。
# 脚本内不写死任何文件名 / 区块名 / 元素类名。
DERIVED = (G.get("derived") or {}).get("items") or []
derived_keys = set()
for item in DERIVED:
    key = item.get("key") or ""
    relf = item.get("file") or ""
    fp = os.path.join(ROOT, relf)
    if not os.path.isfile(fp):
        errs.append("guard.derived 条目 %s 的宿主文件不存在：%s" % (key or "?", relf))
        continue
    t = io.open(fp, encoding="utf-8", errors="ignore").read()
    hits = list(re.finditer(item["region"], t, re.S))
    if len(hits) != 1:
        errs.append("guard.derived 条目 %s 的 region 在 %s 命中 %d 次（须恰好 1 次）"
                    % (key, relf, len(hits)))
        continue
    n = len(re.findall(item["count"], hits[0].group(0)))
    derived_keys.add(key)
    if key.startswith("struct."):
        sk, cur = key[len("struct."):], S.get(key[len("struct."):])
    elif key.startswith("counts."):
        sk, cur = key, C.get(key[len("counts."):])
    else:
        errs.append("guard.derived 键 «%s» 须以 struct. / counts. 前缀声明" % key)
        continue
    if cur is None:
        errs.append("guard.derived 声明的键 «%s» 在 SSOT 中不存在" % key)
    elif cur != n:
        errs.append("%-46s 当前=%-5s 应为=%-5s（DOM 派生：%s @ %s）"
                    % (key, cur, n, item.get("desc") or item.get("count"), relf))

# ---------------- 7) DOM <-> SSOT（全域遍历） ----------------
dom = collections.defaultdict(list)          # pos -> [(rel, value)]
count_keys = collections.Counter()           # data-kb-count 键 -> 出现次数
for rel, p in scan_files(["html", "md"]):
    t = io.open(p, encoding="utf-8", errors="ignore").read()
    for m in re.finditer(r'data-kb-pos="(P\d+)"[^>]*>(\d+)</span>', t):
        dom[m.group(1)].append((rel, m.group(2)))
    for m in re.finditer(r'data-kb-count="([^"]+)"', t):
        count_keys[m.group(1)] += 1

registered = {}
for pos in POS:
    registered[pos.get("id", "").split("_")[0]] = pos

# 7a) 每个登记 position：锚点存在 + 值 == SSOT 键
for pid, pos in registered.items():
    key = pos.get("key")
    if not key:
        continue
    if key.startswith("struct."):
        want = S.get(key[len("struct."):])
    elif key.startswith("counts."):
        want = C.get(key[len("counts."):])
    else:
        want = C.get(key)
    if want is None:
        errs.append("position %s 的 key «%s» 在 SSOT 中不存在（键被删/改名）" % (pid, key))
        continue
    hits = dom.get(pid, [])
    if not hits:
        errs.append("position %s 在 %s 中找不到 data-kb-pos 锚点" % (pid, pos["file"]))
        continue
    for rf, val in hits:
        if int(val) != want:
            errs.append("position %s（%s，登记 file=%s）DOM=%s ≠ SSOT %s=%s"
                        % (pid, rf, pos["file"], val, key, want))

# 7a2) guard.derived 声明的键必须有已注册 position（否则「真源」无展示位可证）
_pos_keys = {(p.get("key") or "") for p in POS}
for key in sorted(derived_keys):
    if key not in _pos_keys:
        errs.append("guard.derived 键 «%s» 没有对应的已注册 position" % key)

# 7b) 反向：页面上出现但未登记的 position（全局盲区，本次新增）
for pid in sorted(dom):
    if pid not in registered:
        errs.append("position %s 出现在 %s，但未在 SSOT positions 登记"
                    % (pid, ", ".join(sorted({r for r, _ in dom[pid]}))))

# 7c) data-kb-count 的键必须在 SSOT 存在
for key, n in sorted(count_keys.items()):
    if key.startswith("struct."):
        ok = key[len("struct."):] in S
    elif key.startswith("counts."):
        ok = key[len("counts."):] in C
    else:
        ok = key in C
    if not ok:
        errs.append("data-kb-count=«%s»（%d 处）在 SSOT 中不存在" % (key, n))

# 7d) position 全局唯一（白名单来自 SSOT guard.pos_allow_multi）
for pid, hits in sorted(dom.items()):
    if len(hits) > 1 and pid not in ALLOW_MULTI:
        errs.append("position %s 在全站出现 %d 次（须全局唯一；登记 file=%s，实际 %s）"
                    % (pid, len(hits), registered.get(pid, {}).get("file", "?"),
                       ", ".join("%s=%s" % h for h in hits)))

# ---------------- 结论 ----------------
if errs:
    print("\n" + "=" * 68)
    print("计数漂移 %d 项：\n" % len(errs))
    for e in errs:
        print("  ✗ " + e)
    print("\n修复一律走 sync_counts.py bump 唯一入口，勿手改数字；"
          "position 重复/未登记须改用空闲号（先全站 grep 确认）并补登记。")
    sys.exit(1)

print("✅ 计数无漂移：实测 %d 卡 = SSOT 键值 = DOM 取值；%d 个 position 全部已登记且全局唯一"
      "（豁免 %s）；%d 项结构性派生计数（guard.derived）与 DOM 元素数一致；"
      "data-kb-count 键全部有效。"
      % (TOTAL, len(registered), sorted(ALLOW_MULTI) or "无", len(derived_keys)))
sys.exit(0)
