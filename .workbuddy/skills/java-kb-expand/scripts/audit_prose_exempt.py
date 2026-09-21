#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 正文聚合计数「豁免台账」审计（audit_prose_exempt.py，只读）

用途：把 `guard.coverage.prose.exempt` 从「配置里的一串正则」变成**可见台账**。

`validate_kb` 的 D 段（正文聚合计数）只报「未被豁免的裸计数」；但**豁免本身也会成为盲区** ——
豁免写宽了会把真计数一起放过，且不报错、无声无息。本脚本用**同一套判据**枚举全部候选，
再逐条标注「被哪条豁免放过 / 未被豁免（即门禁会 FAIL）」，供人工复核豁免是否过宽。

退出码：0=全部候选均已被豁免覆盖或有既定豁免（信息性）；1=存在**未被豁免**的候选（= 门禁会 FAIL，
       说明站点有裸计数待升格）；2=定位失败。

用法：python3 audit_prose_exempt.py [项目根] [--quiet]
"""
import io, os, re, sys, json, glob, argparse


def find_root(start):
    """向上查找含 docs/kb-counts.json 的目录（脚本禁写死项目根层级）。"""
    cur = os.path.abspath(start)
    for _ in range(12):
        if os.path.isfile(os.path.join(cur, "docs", "kb-counts.json")):
            return cur
        nxt = os.path.dirname(cur)
        if nxt == cur:
            break
        cur = nxt
    return None


DEFAULT_ROOT = find_root(os.path.dirname(os.path.abspath(__file__)))


def load_cfg(root):
    d = json.load(io.open(os.path.join(root, "docs/kb-counts.json"), encoding="utf-8"))
    return d, (d.get("guard") or {}).get("coverage") or {}


def truth_value_set(d):
    """V = counts 全部正整数值 ∪ 所有已注册 position 的键的当前值（与 validate_kb 同判据）。"""
    C, S, vals = d.get("counts") or {}, d.get("struct") or {}, set()
    for v in C.values():
        if isinstance(v, int) and v > 0:
            vals.add(v)
    for p in d.get("positions") or []:
        k = p.get("key")
        if not k:
            continue
        v = C.get(k)
        if v is None and k.startswith("struct."):
            v = S.get(k[len("struct."):])
        if isinstance(v, int) and v > 0:
            vals.add(v)
    return vals


def main():
    ap = argparse.ArgumentParser(description="正文聚合计数豁免台账审计（只读）")
    ap.add_argument("root", nargs="?", default=DEFAULT_ROOT)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root) + os.sep
    d, cfg = load_cfg(root)
    pr = cfg.get("prose") or {}
    if not pr.get("enabled", True):
        print("prose 段已停用（guard.coverage.prose.enabled=false）—— 无台账可审")
        return 2
    units = list(pr.get("units") or cfg.get("units") or [])
    exs = [(re.compile((e.get("re") if isinstance(e, dict) else e), re.S),
            (e.get("name") if isinstance(e, dict) else "")) for e in (pr.get("exempt") or [])]
    win = int(pr.get("exempt_window", 40))
    masks = [re.compile(p, re.S) for p in (pr.get("mask") or [])]
    V = truth_value_set(d)
    digit = re.compile(r"(?<![\w.\-/])(\d+)\s*(%s)" % "|".join(units))
    span_re = re.compile(r'<span[^>]*data-kb-pos="P\d+"[^>]*>\s*\d+\s*</span>', re.S)
    targets = sorted({p for pat in cfg["scan"] for p in glob.glob(os.path.join(root, pat))})

    rows, guarded = [], 0
    for path in targets:
        if not os.path.isfile(path):
            continue
        t = io.open(path, encoding="utf-8", errors="ignore").read()
        rel = os.path.relpath(path, root)
        vis = bytearray(b"\x01" * len(t))
        for mp in masks:
            for m in mp.finditer(t):
                for i in range(m.start(), m.end()):
                    vis[i] = 0
        spans = [(m.start(), m.end()) for m in span_re.finditer(t)]
        for dm in digit.finditer(t):
            ap_ = dm.start(1)
            if not vis[ap_]:
                continue
            num = dm.group(1)
            if len(num) > 1 and num[0] == "0":
                continue
            if int(num) not in V:
                continue
            if any(s <= ap_ < e for s, e in spans):
                guarded += 1
                continue
            w = t[max(0, ap_ - win): dm.end() + win]
            hit = next((n for e, n in exs if e.search(w)), None)
            ctx = re.sub(r"\s+", " ", re.sub(r"<[^>]*>", "", t[max(0, ap_ - 44): dm.end() + 24]))
            rows.append((rel, t.count("\n", 0, ap_) + 1, dm.group(0), hit, ctx))

    ex_rows = [r for r in rows if r[3]]
    un_rows = [r for r in rows if not r[3]]
    if not a.quiet:
        print("项目根：%s" % root)
        print("真值集 V：%d 个值；单位集：%d 个；豁免：%d 条；窗口：%d 字" % (len(V), len(units), len(exs), win))
        print("扫描 %d 个文件：候选（数字∈V 且**紧邻**单位词）%d 处；"
              "其中 %d 处落在 kb-count span 内（正常恒为 0 —— 受保护位的形态是「N</span> 单位」，"
              "数字与单位词之间有标签，天然不紧邻）" % (len(targets), len(rows), guarded))
        print()
        print("=== 被豁免放过（%d 处；**豁免台账**，请复核是否过宽）===" % len(ex_rows))
        by = {}
        for rel, ln, s, hit, ctx in ex_rows:
            by.setdefault(hit, []).append((rel, ln, s, ctx))
        for name, items in by.items():
            print("  ▸ %s —— %d 处" % (name, len(items)))
            for rel, ln, s, ctx in items[:4]:
                print("      %-52s L%-5d %-7s | %s" % (rel, ln, s, ctx[:72]))
            if len(items) > 4:
                print("      …其余 %d 处" % (len(items) - 4))
        print()
        print("=== 未被豁免（门禁将 FAIL 的候选）= %d 处 ===" % len(un_rows))
        for rel, ln, s, hit, ctx in un_rows[:24]:
            print("  %-52s L%-5d %-7s | %s" % (rel, ln, s, ctx[:80]))
    return 1 if un_rows else 0


if __name__ == "__main__":
    sys.exit(main())
