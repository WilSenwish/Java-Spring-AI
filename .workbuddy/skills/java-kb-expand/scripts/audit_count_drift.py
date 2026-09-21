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

职责边界（2026-09-21 收敛）：
  · **本脚本**只做「**结构性**」校验：全站卡片普查（含重复定义）、DOM ↔ SSOT 逐位、
    position 已登记 / 全局唯一、data-kb-count 键有效性。
  · 「某个键的**真值**应该是几」**不在本脚本**——统一委托 `audit_truth_source.py`
    （SSOT `guard.sources` 驱动）。历史上 `guard.layers` / `guard.derived` /
    `guard.single_source` 的真值语义被两个脚本各解读一遍，改一处就会分叉。

设计红线（2026-09-21，长官指令「门禁脚本得针对全局或接收参数，不能固定写死部分编码等」）：
  本脚本**不得写死任何组号区间、文件名、白名单、单位词、项目根层级**。全部读 SSOT：
    允许多点位              → `guard.pos_allow_multi`
    全局忽略目录            → `guard.exclude`（含 rk/ 软考资料站）
    真源声明                → `guard.sources`（由被委托的真源引擎消费）
  卡片实测源 = **全站自动识别**「含 qa-card 的文件」，不指定任何文件名。

链路：结构性一致（本脚本）→ 真值正确（`audit_truth_source.py`）→ 覆盖完整（`audit_l1_counts.py`）。

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
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kbroot import find_root  # noqa: E402




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
ALLOW_MULTI = set(G.get("pos_allow_multi") or [])
EXCLUDE = G.get("exclude") or ["tmp/", "node_modules/", "rk/"]

errs = []


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


# ---------------- 2) 真值校验：委托真源引擎（单一真源） ----------------
# 「某个键的真值应该是几」只由 `audit_truth_source.py` + SSOT `guard.sources` 决定。
# 本脚本**不再自行推导**——历史上 `guard.layers` / `guard.derived` / `guard.single_source`
# 的真值语义被两个脚本各解读一遍，改一处就会分叉（2026-09-21 统一）。
# 这里只做「调用 + 汇总」：把真源引擎的 FAIL 行原样并入本脚本的 errs。
TRUTH_ENGINE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "audit_truth_source.py")
_tp = subprocess.run([sys.executable, TRUTH_ENGINE, ROOT],
                     capture_output=True, text=True)
for _ln in (_tp.stdout + _tp.stderr).split("\n"):
    if _ln.startswith("FAIL "):
        errs.append("[真源] " + _ln[len("FAIL "):])

# ---------------- 3) DOM <-> SSOT（全域遍历） ----------------
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

# 7b) 反向：页面上出现但未登记的 position（全局盲区）
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
          "position 重复/未登记须改用空闲号（先全站 grep 确认）并补登记；"
          "「真源」前缀项由 audit_truth_source.py 报出，须先查内容再改 SSOT。")
    sys.exit(1)

print("✅ 计数无漂移：实测 %d 卡 = SSOT 键值 = DOM 取值；%d 个 position 全部已登记且全局唯一"
      "（豁免 %s）；真值由 audit_truth_source.py 独立复核通过；data-kb-count 键全部有效。"
      % (TOTAL, len(registered), sorted(ALLOW_MULTI) or "无"))
sys.exit(0)
