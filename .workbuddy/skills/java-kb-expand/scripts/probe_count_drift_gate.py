#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 计数漂移审计 反向验证（probe_count_drift_gate.py）

对 `audit_count_drift.py` 做**反向注入**验证：每类缺陷注入后必须 FAIL 且点名，
还原后必须 PASS。任一等例未如期检出 → 退出码 1（门禁假绿）。

用例：
  A. 键值漂移          —— SSOT 组键改小（模拟新增卡未同步）
  B. position 未登记   —— 页面 data-kb-pos 改成 SSOT 里没有的号
  C. position 重复     —— 两处用同一 pos 号
  D. 数据驱动生效      —— 改 SSOT `guard.layers` 的 range，校验目标随之变化
  E. **derived 真源漂移** —— SSOT `guard.derived` 键值与 DOM 元素数不符
  F. **derived 独占检出** —— 页面多加一个 chip（卡数不变、position 值不变），
                            只有 DOM 派生链路能发现
  G. **derived region 失效** —— region 正则不再命中（防线自身的自检）
  H. **derived 无展示位** —— 声明的键没有已注册 position

退出码：0=双向验证通过；1=门禁失效；2=定位失败。
"""
import io
import json
import os
import re
import subprocess
import sys

BASE = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI"
SCRIPT = os.path.join(BASE, ".workbuddy/skills/java-kb-expand/scripts/audit_count_drift.py")
PY3 = "/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3"
SSOT = os.path.join(BASE, "docs/kb-counts.json")
MIND = os.path.join(BASE, "java-architect-interview-mind/mind-core-methodology.html")
CORE = os.path.join(BASE, "java-architect-interview/chapter-core-methodology.html")
DK = "misc.chap_chapter_core_methodology.layer_hang_dao"      # 道层 chip 数（该层真有 layer-chip）

for f in (SSOT, MIND, CORE):
    if not os.path.isfile(f):
        print("定位失败：缺少 %s" % f)
        sys.exit(2)

ORIG = {p: io.open(p, encoding="utf-8").read() for p in (SSOT, MIND, CORE)}


def run():
    p = subprocess.run([PY3, SCRIPT], capture_output=True, text=True, cwd=BASE)
    return p.returncode, p.stdout + p.stderr


def last(out):
    return next((l for l in reversed(out.strip().split("\n")) if l.strip()), "")[:100]


ok = True
print("== 基线（应 PASS）==")
rc, out = run()
print("  exit=%d %s" % (rc, last(out)))
if rc != 0:
    print("  ❌ 基线非 PASS，无法继续")
    sys.exit(1)


def case(name, patches, needle):
    """patches: {绝对路径: 新内容}。注入 → 断言 FAIL 且点名 → 还原。"""
    global ok
    print("\n== 用例 %s ==" % name)
    try:
        for p, t in patches.items():
            io.open(p, "w", encoding="utf-8").write(t)
        rc, out = run()
        good = rc == 1 and needle in out
        print("  exit=%d %s" % (rc, last(out)))
        for l in out.strip().split("\n"):
            if needle in l:
                print("    " + l.strip()[:120]); break
        print("  %s（点名 %r）" % ("✅ 如期检出" if good else "❌ 未检出", needle))
        ok &= good
    finally:
        for p, t in ORIG.items():
            io.open(p, "w", encoding="utf-8").write(t)
            assert io.open(p, encoding="utf-8").read() == t, "还原失败：%s" % p


def ssot_patched(mutate):
    cfg = json.loads(ORIG[SSOT])
    mutate(cfg)
    return json.dumps(cfg, ensure_ascii=False, indent=2) + "\n"


# A. 键值漂移
case("A 键值漂移：meth.group_7 4→3",
     {SSOT: ORIG[SSOT].replace('"meth.group_7": 4', '"meth.group_7": 3', 1)},
     "meth.group_7")

# B. position 未登记
case("B position 未登记：mind 页 P410→P999",
     {MIND: ORIG[MIND].replace('data-kb-pos="P410"', 'data-kb-pos="P999"', 1)},
     "P999")

# C. position 重复
case("C position 重复：mind 页 P411→P410",
     {MIND: ORIG[MIND].replace('data-kb-pos="P411"', 'data-kb-pos="P410"', 1)},
     "出现 2 次")

# D. 数据驱动生效：改 layers range 应改变校验目标
case("D 数据驱动：guard.layers 法 range 3–7→3–8",
     {SSOT: ssot_patched(lambda c: c["guard"]["layers"][1].__setitem__("range", [3, 8]))},
     "meth.theme_1")

# E. derived 真源漂移（SSOT 键值 ≠ DOM 元素数）
case("E derived 真源漂移：%s 12→11" % DK,
     {SSOT: ssot_patched(lambda c: c["struct"].__setitem__(DK, 11))},
     DK)

# F. derived 独占检出：章节页 dao 层多插一个 chip（SSOT / position 值均不变）
_dao = '<div class="layer-band dao">'
assert ORIG[CORE].count(_dao) == 1, "dao 层锚点不唯一"
case("F derived 独占检出：dao 层多插 1 个 layer-chip",
     {CORE: ORIG[CORE].replace(
         _dao, _dao + '<a class="layer-chip" href="#M01.01">探针</a>', 1)},
     DK)

# G. derived region 失效（防线自检）
case("G derived region 失效：region 正则不再命中",
     {SSOT: ssot_patched(lambda c: c["guard"]["derived"]["items"][0].__setitem__(
         "region", '<div class="layer-band __never__">'))},
     "命中 0 次")

# H. derived 无展示位（诚实性：新声明必须配已注册 position）
def _orphan(c):
    c["struct"]["misc.chap_chapter_core_methodology.probe_orphan"] = 11
    c["guard"]["derived"]["items"].append({
        "key": "struct.misc.chap_chapter_core_methodology.probe_orphan",
        "file": "java-architect-interview/chapter-core-methodology.html",
        "region": '<div class="layer-band fa">(?:(?!<div class="layer-band ).)*',
        "count": 'class="layer-chip"',
        "desc": "probe：无展示位的派生计数",
    })

case("H derived 无展示位：声明键但未注册 position",
     {SSOT: ssot_patched(_orphan)},
     "没有对应的已注册 position")

print("\n== 还原后复跑（应 PASS）==")
rc, out = run()
print("  exit=%d %s" % (rc, last(out)))
ok &= rc == 0

print("\n%s" % ("✅ 双向验证通过：8 类缺陷全部如期检出，还原后复绿；"
                "且校验目标由 SSOT 配置驱动（无写死）"
                if ok else "❌ 双向验证失败：审计脚本存在假绿风险"))
sys.exit(0 if ok else 1)
