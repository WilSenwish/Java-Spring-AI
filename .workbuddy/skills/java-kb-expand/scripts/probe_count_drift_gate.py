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
  E. **derived 真源漂移** —— 注入派生夹具后 SSOT 键值与 DOM 元素数不符
  F. **derived 独占检出** —— 夹具 region 多插一个匹配项（卡数/其它 position 不变）
  G. **derived region 失效** —— region 正则不再命中（防线自身的自检）
  H. **derived 无展示位** —— 声明的键没有已注册 position

退出码：0=双向验证通过；1=门禁失效；2=定位失败。

夹具说明（2026-10-27）：图 0d layer-hang 已清除，基线 `guard.derived.items` 为空。
E/F/G/H 自包含注入临时 derived 规则 + items，靶区为方法论开篇 `#hang-cross` 的 `<li>`（恒为 3）。
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
SCRIPT = os.path.join(HERE, "audit_count_drift.py")


BASE = find_root(sys.argv[1] if len(sys.argv) > 1 else HERE)
if not BASE:
    print("定位失败：未找到同时含 AGENTS.md 与 index.html 的祖先目录")
    sys.exit(2)
PY3 = sys.executable
SSOT = os.path.join(BASE, "docs", "kb-counts.json")
CORE = os.path.join(BASE, "java-architect-interview/chapter-core-methodology.html")
# 夹具键（仅 probe 注入，不在基线 SSOT）
DK = "misc.chap_chapter_core_methodology.probe_hang_cross_li"
DK_FULL = "struct." + DK
POS_PROBE = "P998"
CROSS_ANCHOR = '<div class="cross-ex" id="hang-cross">'
CROSS_REGION = (
    r'<div class="cross-ex" id="hang-cross">(?:(?!</div>\s*<div class="mermaid-container").)*'
)
DERIVED_RULE = {
    "id": "derived",
    "type": "derived",
    "from": "derived",
    "key_re": r"^struct\.misc\.chap_chapter_core_methodology\.probe_hang_cross_li$",
    "desc": "probe 临时派生规则（靶区 #hang-cross <li>）",
}
DERIVED_ITEM = {
    "key": DK_FULL,
    "file": "java-architect-interview/chapter-core-methodology.html",
    "region": CROSS_REGION,
    "count": r"<li>",
    "desc": "probe：开篇三例竖切 <li> 数",
}
POS_ENTRY = {
    "id": POS_PROBE + "_probe_hang_cross_li",
    "file": "java-architect-interview/chapter-core-methodology.html",
    "pattern": r'data-kb-pos="' + POS_PROBE + r'"[^>]*>(\d+)</span>',
    "key": DK_FULL,
    "desc": "probe 临时展示位",
}

for f in (SSOT, CORE):
    if not os.path.isfile(f):
        print("定位失败：缺少 %s" % f)
        sys.exit(2)

ORIG = {p: io.open(p, encoding="utf-8").read() for p in (SSOT, CORE)}

# 基线须有 hang-cross 且恰 3 个 <li>
_m = re.search(CROSS_REGION, ORIG[CORE], re.S)
if not _m:
    print("定位失败：方法论页缺少可匹配的 #hang-cross 块")
    sys.exit(2)
_li_n = len(re.findall(r"<li>", _m.group(0)))
if _li_n != 3:
    print("定位失败：#hang-cross <li> 期望 3，实际 %d" % _li_n)
    sys.exit(2)
if ORIG[CORE].count(CROSS_ANCHOR) != 1:
    print("定位失败：#hang-cross 锚点不唯一")
    sys.exit(2)


def run():
    p = subprocess.run([PY3, SCRIPT, BASE], capture_output=True, text=True, cwd=BASE)
    return p.returncode, p.stdout + p.stderr


def last(out):
    return next((l for l in reversed(out.strip().split("\n")) if l.strip()), "")[:100]


ok = True
print("== 基线（应 PASS）==")
rc, out = run()
print("  exit=%d %s" % (rc, last(out)))
if rc != 0:
    print("  ❌ 基线非 PASS，无法继续")
    print(out[-2000:])
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
                print("    " + l.strip()[:120])
                break
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


def install_derived_fixture(cfg, struct_val=3, with_position=True, broken_region=False):
    """在 SSOT 中安装临时 derived 规则 + item +（可选）position/struct。"""
    cfg.setdefault("struct", {})[DK] = struct_val
    der = cfg.setdefault("guard", {}).setdefault("derived", {})
    der["items"] = [dict(DERIVED_ITEM)]
    if broken_region:
        der["items"][0] = dict(DERIVED_ITEM, region='<div class="cross-ex" id="hang-cross__never__">')
    rules = cfg.setdefault("guard", {}).setdefault("sources", {}).setdefault("rules", [])
    rules[:] = [r for r in rules if r.get("id") != "derived"]
    rules.append(dict(DERIVED_RULE))
    if with_position:
        positions = cfg.setdefault("positions", [])
        positions[:] = [p for p in positions if not str(p.get("id", "")).startswith(POS_PROBE)]
        positions.append(dict(POS_ENTRY))


def core_with_probe_span(extra_li=False):
    """在 hang-cross 标题旁挂临时展示 span；可选多插一个 <li>。"""
    t = ORIG[CORE]
    span = (
        '<span class="kb-count" data-kb-pos="%s" data-kb-count="%s">3</span>'
        % (POS_PROBE, DK_FULL)
    )
    t = t.replace(
        CROSS_ANCHOR + "\n            <h3>同一词跨层：三例竖切</h3>",
        CROSS_ANCHOR + "\n            " + span + "\n            <h3>同一词跨层：三例竖切</h3>",
        1,
    )
    if extra_li:
        t = t.replace(
            CROSS_ANCHOR,
            CROSS_ANCHOR + "<ol><li>探针</li></ol>",
            1,
        )
    return t


# A. 键值漂移
case("A 键值漂移：meth.group_7 4→3",
     {SSOT: ORIG[SSOT].replace('"meth.group_7": 4', '"meth.group_7": 3', 1)},
     "meth.group_7")

# B. position 未登记（用现存 P434）
case("B position 未登记：方法论页 P434→P999",
     {CORE: ORIG[CORE].replace('data-kb-pos="P434"', 'data-kb-pos="P999"', 1)},
     "P999")

# C. position 重复（P434 → P437，P437 本页已存在）
case("C position 重复：方法论页 P434→P437",
     {CORE: ORIG[CORE].replace('data-kb-pos="P434"', 'data-kb-pos="P437"', 1)},
     "出现 2 次")

# D. 数据驱动生效：改 layers range 应改变校验目标
case("D 数据驱动：guard.layers 法 range 3–7→3–8",
     {SSOT: ssot_patched(lambda c: c["guard"]["layers"][1].__setitem__("range", [3, 8]))},
     "meth.theme_1")

# E. derived 真源漂移（夹具 struct 3→2，DOM 仍为 3）
case(
    "E derived 真源漂移：%s 3→2" % DK,
    {
        SSOT: ssot_patched(lambda c: install_derived_fixture(c, struct_val=2)),
        CORE: core_with_probe_span(),
    },
    DK,
)

# F. derived 独占检出：多插 1 个 <li>（SSOT / position 值均仍为 3）
case(
    "F derived 独占检出：#hang-cross 多插 1 个 <li>",
    {
        SSOT: ssot_patched(lambda c: install_derived_fixture(c, struct_val=3)),
        CORE: core_with_probe_span(extra_li=True),
    },
    DK,
)

# G. derived region 失效（防线自检）
case(
    "G derived region 失效：region 正则不再命中",
    {
        SSOT: ssot_patched(lambda c: install_derived_fixture(c, broken_region=True)),
        CORE: core_with_probe_span(),
    },
    "命中 0 次",
)

# H. derived 无展示位（诚实性：新声明必须配已注册 position）
def _orphan(c):
    install_derived_fixture(c, with_position=False)
    # 覆盖为 orphan 键，避免与 E/F 夹具键混淆阅读
    c["struct"]["misc.chap_chapter_core_methodology.probe_orphan"] = 3
    c["guard"]["derived"]["items"] = [{
        "key": "struct.misc.chap_chapter_core_methodology.probe_orphan",
        "file": "java-architect-interview/chapter-core-methodology.html",
        "region": CROSS_REGION,
        "count": r"<li>",
        "desc": "probe：无展示位的派生计数",
    }]
    c["guard"]["sources"]["rules"] = [
        r for r in c["guard"]["sources"]["rules"] if r.get("id") != "derived"
    ] + [{
        "id": "derived",
        "type": "derived",
        "from": "derived",
        "key_re": r"^struct\.misc\.chap_chapter_core_methodology\.probe_orphan$",
        "desc": "probe orphan",
    }]


case("H derived 无展示位：声明键但未注册 position（真源引擎反向完备性）",
     {SSOT: ssot_patched(_orphan)},
     "无展示位")

print("\n== 还原后复跑（应 PASS）==")
rc, out = run()
print("  exit=%d %s" % (rc, last(out)))
ok &= rc == 0

print("\n%s" % ("✅ 双向验证通过：8 类缺陷全部如期检出，还原后复绿；"
                "且校验目标由 SSOT 配置驱动（无写死）"
                if ok else "❌ 双向验证失败：审计脚本存在假绿风险"))
sys.exit(0 if ok else 1)
