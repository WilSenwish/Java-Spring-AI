#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 未登记计数扫描（scan_undeclared_counts.py）
=================================================================
长官指令（2026-09-21）：「真源引擎只覆盖已被声明的键」—— 这是**反向**完备性：
每一个已登记 position 都必须有真源声明（audit_truth_source.py 管这条）。
本脚本补上**正向**完备性：**全站正文里出现的每一个计数锚点，都必须已在 SSOT `positions` 登记**——
否则就是「页面上写了一个计数，但门禁根本没管它」（= 未登记声明的键）。

为什么必须双向：
  反向（audit_truth_source）：声明了 ⇒ 必须正确。保护「已登记的数写对没」。
  正向（本脚本）          ：正文有 ⇒ 必须登记。保护「页面上冒出来的数，门禁一个都不漏」。
  只做反向，漏登记的计数永远进不了 SSOT，门禁对它零覆盖、零校验 —— 等于裸奔。

扫描对象：全站 HTML **与 Markdown 文档**（排除目录取自 SSOT `guard.exclude`，
默认 tmp/ node_modules/ rk/；不写死在脚本内）内形如
  <... data-kb-count="KEY" data-kb-pos="Pnn" ...>VALUE</span>        （HTML 站页）
  <span class="kb-count" l="KEY" data-kb-pos="Pnn">VALUE</span>     （docs/*.md 规范文档，键在 `l` 属性）
的计数锚点（data-kb-count / l 两种键属性、两种属性先后顺序都支持；键必须与 data-kb-pos 同标签）。

对比基准：SSOT `positions` 的键集合（position.key）与 position 编号集合（id 里的 P 编号）。

输出：
  FAIL [未登记计数]  键 «K» 在 <file>:line 出现，但 SSOT positions 未登记
                      —— 该计数无任何门禁覆盖（覆盖/一致/真值/豁免全管不到它）。
  FAIL [未登记计数]  位 P<nn> 在 <file>:line 出现，但 SSOT positions 无此编号
                      —— 锚点引用了不存在的 position（孤儿锚点）。
  WARN [登记缺位]    键 «K» 已登记但全站正文无锚点
                      —— 反向提示：可能是派生/汇总键无需锚点，或登记了却没落地，请人工确认。

门禁纪律：
  - 正向未登记 = 硬 FAIL（exit 1），由 validate_kb.py 0c3 步纳入全量校验。
  - 反向缺位 = WARN（exit 0），不阻塞门禁，仅提示人工复核。
  - 路径全部经 _kbroot.find_root 推导，禁写死。

用法：
  python3 scan_undeclared_counts.py [项目根] [--quiet] [--max N]
  退出码：0 = 正向完备（无未登记）；1 = 存在未登记；2 = 定位失败
"""
import argparse
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kbroot import find_root  # noqa: E402  项目根唯一实现（禁写死路径）

# 排除目录默认集；运行时优先读 SSOT guard.exclude（与 audit_truth_source /
# audit_count_drift 一致），避免忽略规则在脚本里写死而逐渐过时。
DEF_EXCLUDE = ["tmp/", "node_modules/", "rk/"]


def read(p):
    return io.open(p, encoding="utf-8", errors="ignore").read()


# 两种键属性（data-kb-count / l）× 两种先后顺序（键在前 / 位在前）
_RE_COUNT_FIRST = re.compile(
    r'data-kb-count="([^"]+)"[^>]*data-kb-pos="P(\d+)"[^>]*>(\d+)<')
_RE_POS_FIRST = re.compile(
    r'data-kb-pos="P(\d+)"[^>]*data-kb-count="([^"]+)"[^>]*>(\d+)<')
_RE_L_COUNT_FIRST = re.compile(
    r'l="([^"]+)"[^>]*data-kb-pos="P(\d+)"[^>]*>(\d+)<')
_RE_L_POS_FIRST = re.compile(
    r'data-kb-pos="P(\d+)"[^>]*l="([^"]+)"[^>]*>(\d+)<')
# (regex, key_in_group, pos_in_group)
_PATTERNS = (
    (_RE_COUNT_FIRST, 1, 2),
    (_RE_POS_FIRST, 2, 1),
    (_RE_L_COUNT_FIRST, 1, 2),
    (_RE_L_POS_FIRST, 2, 1),
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--quiet", action="store_true", help="只输出结论")
    ap.add_argument("--max", type=int, default=0,
                    help="每类 FAIL 最多打印条数（默认 0=不限；门禁不得藏发现）")
    a = ap.parse_args()

    root = os.path.abspath(a.root) if a.root else find_root(__file__)
    if not root or not os.path.isfile(os.path.join(root, "docs", "kb-counts.json")):
        print("FAIL 未能定位项目根（须含 docs/kb-counts.json）")
        return 2
    ssot = json.load(io.open(os.path.join(root, "docs", "kb-counts.json"), encoding="utf-8"))
    G = ssot.get("guard") or {}
    EXCLUDE = G.get("exclude") or DEF_EXCLUDE
    pos = ssot.get("positions") or []
    if not pos:
        print("FAIL SSOT positions 为空 —— 无法比对登记状态")
        return 2

    # ---- 登记基准：键集合 + P 编号集合 ----
    reg_keys = set()
    reg_posnum = set()
    for p in pos:
        k = p.get("key")
        if k:
            reg_keys.add(k)
        pid = p.get("id") or ""
        m = re.search(r'P(\d+)', pid)
        if m:
            reg_posnum.add(int(m.group(1)))

    # ---- 扫描全站正文（HTML 站页 + Markdown 规范文档）----
    # EXCLUDE 取自 SSOT guard.exclude（见上方 G.get("exclude")）
    body_keys = {}      # key -> [(file, line)]
    body_posnum = {}    # posnum -> [(file, line)]
    scanned = 0
    for ext in ("*.html", "*.md"):
        for f in glob.glob(os.path.join(root, "**", ext), recursive=True):
            rel = os.path.relpath(f, root)
            if any(rel.startswith(e) for e in EXCLUDE):
                continue
            t = read(f)
            scanned += 1
            for rx, kg, pg in _PATTERNS:
                for m in rx.finditer(t):
                    line = t.count("\n", 0, m.start()) + 1
                    key, pn, val = m.group(kg), int(m.group(pg)), m.group(3)
                    body_keys.setdefault(key, []).append((rel, line, val))
                    body_posnum.setdefault(pn, []).append((rel, line, key, val))

    # ---- 正向：未登记 ----
    undeclared_keys = sorted(k for k in body_keys if k not in reg_keys)
    undeclared_pos = sorted(p for p in body_posnum if p not in reg_posnum)
    # ---- 反向：已登记但正文缺位 ----
    absent_keys = sorted(k for k in reg_keys if k not in body_keys)

    cap = a.max if a.max and a.max > 0 else 10 ** 6

    if not a.quiet:
        print("扫描文件 %d 个（HTML+Markdown） · 正文锚点键 %d 个 / 位编号 %d 个 · "
              "SSOT 登记键 %d 个 / 位编号 %d 个"
              % (scanned, len(body_keys), len(body_posnum),
                 len(reg_keys), len(reg_posnum)))

    ok = True
    if undeclared_keys:
        ok = False
        for k in undeclared_keys[:cap]:
            locs = body_keys[k]
            first = locs[0]
            print("FAIL [未登记计数] 键 «%s» 在 %s:%d 出现 %d 次（值=%s），"
                  "但 SSOT positions 未登记 —— 该计数无任何门禁覆盖" % (k, first[0], first[1], len(locs), first[2]))
        print("FAIL [未登记计数] 共 %d 个键：正文有计数锚点但未在 SSOT 登记"
              "（须 sync_counts bump --add 登记，并在 guard.sources 声明真源；见 conventions §5.1.4）"
              % len(undeclared_keys))

    if undeclared_pos:
        ok = False
        for pn in undeclared_pos[:cap]:
            locs = body_posnum[pn]
            first = locs[0]
            print("FAIL [未登记计数] 位 P%d 在 %s:%d 出现（键=%s），"
                  "但 SSOT positions 无此编号 —— 孤儿锚点" % (pn, first[0], first[1], first[2]))
        print("FAIL [未登记计数] 共 %d 个位编号：正文引用了未登记的 position"
              % len(undeclared_pos))

    # 反向仅提示（不阻塞门禁）
    for k in absent_keys[:cap]:
        print("WARN [登记缺位] 键 «%s» 已登记但全站正文无锚点"
              "（可能是派生/汇总键无需锚点，或登记了却未落地，请人工确认）" % k)
    if absent_keys and not a.quiet:
        print("WARN [登记缺位] 共 %d 个键：已登记但正文无锚点（仅提示，不阻塞）"
              % len(absent_keys))

    if ok:
        print("✅ 未登记计数扫描通过：正文 %d 个计数锚点全部已在 SSOT positions 登记；"
              "无未登记键 / 无孤儿位。" % len(body_keys))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
