#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe · audit_cross_axis_dedup 双向验证
=========================================
注入必 FAIL、还原必 PASS、豁免生效必 PASS、基线必 PASS。
- 全程 try/finally 还原三个文件（宿主 A / 宿主 C12 / SSOT），不留痕；
- 不依赖 tmp/ 夹具：注入文本从真实页面卡片动态提取；
- 夹具缺失（文件 / 配置 / 目标卡）一律退 3，不静默放行。
"""
import os, sys, re, json, subprocess

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS)
from _kbroot import require_root
import audit_cross_axis_dedup as M

BASE = require_root(__file__)
GATE = os.path.join(SCRIPTS, "audit_cross_axis_dedup.py")
SSOT = os.path.join(BASE, "docs", "kb-counts.json")
A_HOST = os.path.join(BASE, "java-architect-interview", "chapter-question-ai-engineering-deep.html")
C_HOST = os.path.join(BASE, "java-architect-interview", "chapter-12-ai-engineering.html")
SRC, DST = "A19.03", "C12.40"

# 兼容空数组与已有豁免台账：按锚点定位 cross_axis_dedup 的 exempt 数组整体
EXEMPT_ANCHOR = '"jaccard_fail": 0.3,\n      "exempt": '


def exempt_span(t):
    assert t.count(EXEMPT_ANCHOR) == 1, "exempt 锚点异常（须唯一命中 cross_axis_dedup 块）"
    s = t.index(EXEMPT_ANCHOR) + len(EXEMPT_ANCHOR)
    assert t[s] == "[", "exempt 值须为数组"
    depth, in_str, esc = 0, False, False
    for j in range(s, len(t)):
        ch = t[j]
        if in_str:
            if esc:
                esc = False
            elif ch == chr(92):
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return s, j + 1
    raise AssertionError("exempt 数组未闭合")


def read_exempt(t):
    s, e = exempt_span(t)
    return json.loads(t[s:e])


def write_exempt(items):
    s0 = open(SSOT, encoding="utf-8").read()
    s, e = exempt_span(s0)
    open(SSOT, "w", encoding="utf-8").write(
        s0[:s] + json.dumps(items, ensure_ascii=False) + s0[e:])



def run_gate():
    r = subprocess.run([sys.executable, GATE, "--json"], cwd=BASE,
                       capture_output=True, text=True)
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        data = {}
    return r.returncode, data


def card_span(t, cid):
    m = re.search(r'<div class="content-card" id="' + re.escape(cid) + r'"', t)
    if not m:
        return None
    s = m.start(); d = 0; i = s
    while i < len(t):
        if t.startswith("<div", i):
            d += 1; i += 4
        elif t.startswith("</div", i):
            d -= 1
            if d == 0:
                return s, i + 6
            i += 5
        else:
            i += 1
    return None


def inject(path, dst, sentences):
    t = open(path, encoding="utf-8").read()
    span = card_span(t, dst)
    assert span, f"{dst} 卡块未找到"
    s, e = span
    block = t[s:e]
    pm = re.search(r'(<div class="content-layer" data-layer="pitfall">.*?'
                   r'<div class="content-layer-body">\s*<p>)(.*?)(</p>)', block, re.S)
    assert pm, f"{dst} pitfall 层 <p> 未找到"
    payload = "。" + "。".join(sentences) + "。"
    new_block = block[:pm.end(2)] + payload + block[pm.end(2):]
    open(path, "w", encoding="utf-8").write(t[:s] + new_block + t[e:])


def expect(cond, label, detail=""):
    if cond:
        print(f"  PASS {label}")
        return True
    print(f"  FAIL {label} {detail}")
    return False


def main():
    for p in (GATE, SSOT, A_HOST, C_HOST):
        if not os.path.isfile(p):
            print(f"FAIL [夹具] 缺文件：{p}")
            return 3
    cfg = json.load(open(SSOT, encoding="utf-8"))
    g = cfg.get("guard", {}).get("cross_axis_dedup")
    if not g or SRC not in g.get("focus_ids", []) or DST not in g.get("focus_ids", []):
        print("FAIL [夹具] guard.cross_axis_dedup 缺配置或 focus_ids 未含探针卡")
        return 3
    a_cards = M.extract_cards(A_HOST)
    src = next((c for c in a_cards if c["id"] == SRC), None)
    if not src:
        print(f"FAIL [夹具] 源卡 {SRC} 未找到")
        return 3
    sents = [s for s in M.sents_of(src["text"], 15) if len(s) >= 15]
    if len(sents) < 12:
        print(f"FAIL [夹具] 源卡可注入句不足：{len(sents)}")
        return 3

    orig = {p: open(p, encoding="utf-8").read() for p in (A_HOST, C_HOST, SSOT)}
    ok = True
    try:
        print("=== 1) 基线（未注入）应 PASS ===")
        rc, _ = run_gate()
        ok &= expect(rc == 0, "基线 PASS", f"rc={rc}")

        print("=== 2) 注入 4 句逐字复制（验证 exact_fail）应 FAIL ===")
        inject(C_HOST, DST, sents[:4])
        rc, data = run_gate()
        hit = [v for v in data.get("violations", [])
               if {v["a"], v["b"]} == {SRC, DST}]
        ok &= expect(rc == 1 and bool(hit), "注入必 FAIL", f"rc={rc} hit={hit[:1]}")
        for p, s in orig.items():
            open(p, "w", encoding="utf-8").write(s)

        print("=== 3) 还原后应 PASS ===")
        rc, _ = run_gate()
        ok &= expect(rc == 0, "还原必 PASS", f"rc={rc}")

        print("=== 4) 注入 12 句整段复制（验证 jaccard/near 判据）应 FAIL ===")
        inject(C_HOST, DST, sents[:12])
        rc, data = run_gate()
        hit = [v for v in data.get("violations", [])
               if {v["a"], v["b"]} == {SRC, DST}]
        ok &= expect(rc == 1 and bool(hit), "整段注入必 FAIL", f"rc={rc} hit={hit[:1]}")
        for p, s in orig.items():
            open(p, "w", encoding="utf-8").write(s)

        print("=== 5) 豁免台账生效（注入 + 合法豁免）应 PASS ===")
        cur = read_exempt(open(SSOT, encoding="utf-8").read())
        cur.append({"a": DST, "b": SRC, "reason": "probe 临时豁免验证"})
        write_exempt(cur)
        inject(C_HOST, DST, sents[:4])
        rc, data = run_gate()
        ok &= expect(rc == 0, "豁免生效 PASS", f"rc={rc} violations={data.get('violations', [])[:1]}")
        for p, s in orig.items():
            open(p, "w", encoding="utf-8").write(s)

        print("=== 6) 豁免缺 reason 应 FAIL（台账校验） ===")
        write_exempt([{"a": DST, "b": SRC}])
        rc, _ = run_gate()
        ok &= expect(rc == 1, "豁免无理由必 FAIL", f"rc={rc}")
    finally:
        for p, s in orig.items():
            open(p, "w", encoding="utf-8").write(s)
        print("=== finally：三份文件已还原 ===")

    rc, _ = run_gate()
    ok &= expect(rc == 0, "最终还原态 PASS", f"rc={rc}")
    print("\n==== PROBE %s ====" % ("ALL PASS ✅" if ok else "FAILED ❌"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
