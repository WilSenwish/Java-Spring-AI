#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 计数真源审计 反向验证（probe_truth_gate.py）

对 `audit_truth_source.py` 做**反向注入**验证：往系统里注入缺陷，真源门禁必须 FAIL
并点名；还原后必须 PASS（逐字节一致）。

用例（每类都必须被**点名检出**，否则视为假绿）：
  A. **值错但四处自洽（本门禁存在的理由）** —— 同时改 DOM 显示值 + SSOT 键值，
     使覆盖 / 一致（`sync_counts check`）/ 豁免台账三层全绿，
     只有真源审计能发现「这个数本身就是错的」。
  B. 未声明真源 —— 改掉一条规则的正则，其键立刻变成「没人管正确性」→ FAIL。
  C. 不变式破损 —— 把某篇「高级」计数减 1（DOM + SSOT 同步，站内自洽）→
     三难度之和 ≠ 题数 → FAIL。
  D. 键路径冲突 —— 往 SSOT 塞一份嵌套重复键（展平后与扁平点分键同路径、值不同）。
  E. 真源配置写错 —— 规则的 type 改成未实现的值。
  F. 声明未生效 —— 规则的块锚点改坏（正则仍覆盖键，但求不出真值）。

**注入方式（2026-09-21 加固）**：SSOT 一律「解析 → 就地改 → 规范化写回」，不依赖
文件空白与缩进的字面锚点（此前逐字替换因 SSOT 被重排而误报「锚点命中 0 次」）；
HTML 侧仍用 `data-kb-count + data-kb-pos` 的精确串替换并断言唯一命中。

任一用例未如期检出 → 退出码 1。退出码：0=双向验证通过；1=门禁失效；2=定位失败。
"""
import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kbroot import find_root  # noqa: E402  项目根唯一实现（禁写死路径）

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "audit_truth_source.py")
SYNC = os.path.join(HERE, "sync_counts.py")



ROOT = find_root(sys.argv[1] if len(sys.argv) > 1 else HERE)
if not ROOT:
    print("FAIL 未能定位项目根（须含 docs/kb-counts.json）")
    sys.exit(2)

SSOT = os.path.join(ROOT, "docs", "kb-counts.json")
OV = os.path.join(ROOT, "java-architect-interview", "nav-overview-priority.html")
CHAP_IDX = os.path.join(ROOT, "java-architect-interview", "index.html")

ok = True


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, t):
    io.open(p, "w", encoding="utf-8").write(t)


def dump_ssot(d):
    return json.dumps(d, ensure_ascii=False, indent=2) + "\n"


def run_gate():
    r = subprocess.run([sys.executable, GATE, ROOT], cwd=ROOT,
                       capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def run_sync():
    r = subprocess.run([sys.executable, SYNC, "check"], cwd=ROOT,
                       capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def inject(title, expects, html_edits=None, ssot_mutate=None,
           note="", sync_should_pass=False):
    """html_edits: [(path, old, new)] 逐字替换并断言唯一命中。
    ssot_mutate: callable(dict) 就地修改（写回规范化 JSON，不依赖空白）。
    expects: 门禁输出中必须出现的关键字列表。"""
    global ok
    print("\n== 用例 %s ==" % title)
    html_edits = html_edits or []
    snaps = {}
    try:
        for p in {e[0] for e in html_edits} | ({SSOT} if ssot_mutate else set()):
            snaps[p] = read(p)

        for p, old, new in html_edits:
            t = read(p)
            c = t.count(old)
            assert c == 1, "注入锚点 %r 命中 %d 次" % (old[:70], c)
            write(p, t.replace(old, new))

        if ssot_mutate:
            d = json.loads(read(SSOT))
            ssot_mutate(d)
            write(SSOT, dump_ssot(d))

        if sync_should_pass:
            src, sout = run_sync()
            print("  （前置）sync_counts check exit=%d —— %s"
                  % (src, sout.strip().split("\n")[-1][:80]))
            ok &= (src == 0)
            if src != 0:
                print("  ❌ 本用例前提不成立：注入后应当「站内自洽」")

        rc, out = run_gate()
        hit = all(e in out for e in expects)
        print("  gate exit=%d" % rc)
        for l in out.strip().split("\n"):
            if l.startswith("FAIL "):
                print("    " + l.strip()[:130])
        print("  %s（要求命中 %s）%s"
              % ("✅ 如期检出" if (rc == 1 and hit) else "❌ 未检出 —— 门禁失效",
                 " + ".join(repr(e) for e in expects), (" " + note) if note else ""))
        ok &= (rc == 1 and hit)
    finally:
        for p, t in snaps.items():
            write(p, t)
            assert read(p) == t, "还原失败：%s" % p
        print("  已还原 %s（逐字节一致）"
              % ", ".join(sorted(os.path.basename(p) for p in snaps)))


def rule(d, rid):
    for r in d["guard"]["sources"]["rules"]:
        if r.get("id") == rid:
            return r
    raise AssertionError("SSOT 中找不到规则 %s" % rid)


ssot = json.loads(read(SSOT))

# ---------------------------------------------------------------- A 值错但四处自洽
pos = next(p for p in ssot["positions"] if p.get("key") == "struct.ov.subgroup_1")
pid = re.match(r"(P\d+)", pos["id"]).group(1)
m = re.search(pos["pattern"], read(OV))
old_v = int(m.group(1))
flat_key = pos["key"][len("struct."):]


def a_mut(d):
    d["struct"][flat_key] = old_v + 1


inject(
    "A 值错但四处自洽（覆盖/一致/豁免台账全绿，只有真源审计看得见）",
    ["真值不符", pos["key"]],
    html_edits=[
        (OV, 'data-kb-count="%s" data-kb-pos="%s">%d</span>' % (pos["key"], pid, old_v),
         'data-kb-count="%s" data-kb-pos="%s">%d</span>' % (pos["key"], pid, old_v + 1)),
    ],
    ssot_mutate=a_mut,
    note="← 本门禁存在的唯一理由",
    sync_should_pass=True,
)

# ---------------------------------------------------------------- B 未声明真源
r = rule(ssot, "ov_subgroup")
old_re = r["key_re"]


def b_mut(d):
    rule(d, "ov_subgroup")["key_re"] = old_re.replace("subgroup_", "subgroupX_")


inject(
    "B 未声明真源（改掉规则正则 → 键变成「没人管正确性」）",
    ["未声明真源"],
    ssot_mutate=b_mut,
    note="← 防「新增计数不声明真源」",
)

# ---------------------------------------------------------------- C 不变式破损
posc = next(p for p in ssot["positions"] if p.get("key") == "struct.chap.idx.c06.senior")
pidc = re.match(r"(P\d+)", posc["id"]).group(1)
mc = re.search(posc["pattern"], read(CHAP_IDX))
oldc = int(mc.group(1))
k_senior = posc["key"][len("struct."):]


def c_mut(d):
    d["struct"][k_senior] = oldc - 1


inject(
    "C 不变式破损（三难度之和 ≠ 题数）",
    ["不变式", "chap_levels_eq_n"],
    html_edits=[
        (CHAP_IDX, 'data-kb-count="%s" data-kb-pos="%s">%d</span>' % (posc["key"], pidc, oldc),
         'data-kb-count="%s" data-kb-pos="%s">%d</span>' % (posc["key"], pidc, oldc - 1)),
    ],
    ssot_mutate=c_mut,
    note="← 防「分项陈旧 / 缺展示位」",
    sync_should_pass=True,
)

# ---------------------------------------------------------------- D 键路径冲突
dup_flat = "mind.idx.mind-foot-c_1"


def d_mut(d):
    d["struct"]["mind"] = {"idx": {dup_flat.split("mind.idx.")[1]: 999}}


inject(
    "D 键路径冲突（同一逻辑键写了扁平 + 嵌套两份）",
    ["键路径冲突"],
    ssot_mutate=d_mut,
    note="← 2026-09-21 实测缺陷（struct.mind 陈旧重复）",
)

# ---------------------------------------------------------------- E 真源配置写错
old_type = rule(ssot, "single_dom_count")["type"]


def e_mut(d):
    rule(d, "single_dom_count")["type"] = old_type + "X"


inject(
    "E 真源配置写错（规则 type 未实现）",
    ["真源配置"],
    ssot_mutate=e_mut,
    note="← 防规则类型拼错后静默跳过",
)

# ---------------------------------------------------------------- F 声明未生效
old_block = rule(ssot, "meth_group")["block_re"]


def f_mut(d):
    rule(d, "meth_group")["block_re"] = "<h2 id=\"m-groupZZZ-%02d\""


inject(
    "F 声明未生效（块锚点改坏 → 正则仍覆盖键，但求不出真值）",
    ["声明未生效"],
    ssot_mutate=f_mut,
    note="← 防「声明了真源却从未真的求值」",
)

# ---------------------------------------------------------------- 收尾复跑
print("\n== 还原后复跑（应 PASS）==")
rc2, out2 = run_gate()
print("  exit=%d %s" % (rc2, out2.strip().split("\n")[-1][:120]))
ok &= rc2 == 0

print("\n%s" % ("✅ 双向验证通过：6 类缺陷（值错自洽 / 未声明真源 / 不变式破损 / 键双写 / "
                "配置写错 / 声明未生效）全部如期检出，还原后复绿"
                if ok else "❌ 双向验证失败：门禁存在假绿风险"))
sys.exit(0 if ok else 1)
