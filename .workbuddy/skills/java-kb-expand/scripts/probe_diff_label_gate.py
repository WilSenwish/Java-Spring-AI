#!/usr/bin/env python3
"""1j「难度标签口径」+ 1k「M/G/K 无难度分级」门禁的正向验证。

证明这两条新门禁**不是恒真**：

  轮 1 当前树                   → 期望 failed=0
  轮 2 注入缺陷 A（徽标长表）    → 期望 1j FAIL（chapter-01 某枚徽标改回「高级开发」）
  轮 3 注入缺陷 B（非难度占用）  → 期望 1j FAIL（根 index 首个 layer-tag 改回 difficulty-architect）
  轮 4 注入缺陷 C（专篇带属性）  → 期望 1k FAIL（chapter-core-methodology 加回 data-difficulty）
  轮 5 还原 + MD5               → 期望两份文件 MD5 与原始一致且 failed=0

只动三个文件，**还原一律走 `finally`**（2026-09-21 事故：轮 3 找不到锚点就直接
`return 1`，绕过轮 5 的还原，把 chapter-01 一枚徽标留成「高级开发」，随后
`validate_kb` FAIL。验证脚本一旦会污染被测对象，结论就不可信）。
注入锚点**动态取**，不写死具体汉字；项目根由 `_kbroot.find_root` 推导，不写死层级。
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def find_root(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(d, "AGENTS.md")) and os.path.isfile(os.path.join(d, "index.html")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit("未找到项目根（需含 AGENTS.md + index.html）")
        d = parent


import validate_kb as V  # noqa: E402

CH1 = os.path.join(V.CHAPTER_DIR, "chapter-01-jvm-memory-classloading.html")
METH = os.path.join(V.CHAPTER_DIR, "chapter-core-methodology.html")
ROOT_IDX = os.path.join(V.BASE, "index.html")

CHIP_LONG = re.compile(r'<span class="difficulty difficulty-senior">高级</span>')
CARD_DIFF = re.compile(r'(<div class="qa-card" id="M01\.01")')


def md5(t):
    return hashlib.md5(t.encode("utf-8")).hexdigest()


def run(tag):
    V.check.failed = 0
    V.run_difficulty_label_check()
    j = V.check.failed
    V.check.failed = 0
    V.run_special_no_difficulty_check()
    k = V.check.failed
    print(f"  [{tag}] 1j failed={j}  1k failed={k}")
    return j, k


def main():
    """外壳：**无论中途是否中止，都必须还原被测文件**。

    2026-09-21 实测事故：轮 3 因「锚点不存在」直接 `return 1`，绕过轮 5 的还原，
    把 chapter-01 的一枚徽标留成「高级开发」，随后 `validate_kb` 因此 FAIL ——
    验证脚本一旦会污染被测对象，它的结论就不可信。故还原放进 `finally`。
    """
    f1, f2, f3 = V.read(CH1), V.read(ROOT_IDX), V.read(METH)
    m1, m2, m3 = md5(f1), md5(f2), md5(f3)
    print(f"目标：{os.path.basename(CH1)} / index.html / {os.path.basename(METH)}")
    print(f"  原始 MD5：{m1[:12]} / {m2[:12]} / {m3[:12]}")
    try:
        return _cases(f1, f2, f3, m1, m2, m3)
    finally:
        for _p, _t in ((CH1, f1), (ROOT_IDX, f2), (METH, f3)):
            if V.read(_p) != _t:
                open(_p, "w", encoding="utf-8").write(_t)
        b1, b2, b3 = md5(V.read(CH1)), md5(V.read(ROOT_IDX)), md5(V.read(METH))
        print("  finally 还原核验：%s / %s / %s  %s"
              % (b1[:12], b2[:12], b3[:12],
                 "✅ 一致" if (b1, b2, b3) == (m1, m2, m3) else "❌ 不一致"))


def _cases(f1, f2, f3, m1, m2, m3):
    ok = True
    print("轮 1 · 当前树")
    j, k = run("当前")
    if (j, k) != (0, 0):
        ok = False

    print("轮 2 · 注入 A：徽标文案改回长表（expect 1j FAIL）")
    if not CHIP_LONG.search(f1):
        print("  !! 未找到注入锚点（chapter-01 无「高级」徽标），中止")
        return 1
    open(CH1, "w", encoding="utf-8").write(
        CHIP_LONG.sub('<span class="difficulty difficulty-senior">高级开发</span>', f1, count=1))
    j, k = run("缺陷A")
    if j < 1 or k != 0:
        print("  !! 门禁恒真：A 未触发 1j" if j < 1 else "  !! A 误触 1k")
        ok = False

    print("轮 3 · 注入 B：难度类被非难度语义占用（expect 1j FAIL）")
    # 锚点**动态**取「根 index 的第一个 layer-tag」——不写死具体汉字（文案随内容演进会变，
    # 写死锚点是本 probe 上次「未找到锚点即中止并留下脏树」的根因）。
    _lt = re.search(r'<span class="layer-tag">([^<]+)</span>', f2)
    if not _lt:
        print("  !! 未找到注入锚点（根 index 无 layer-tag），本用例判失败")
        ok = False
    else:
        open(CH1, "w", encoding="utf-8").write(f1)  # 复位 A，保证缺陷互不叠加
        open(ROOT_IDX, "w", encoding="utf-8").write(
            f2.replace(_lt.group(0),
                       '<span class="difficulty difficulty-architect">%s</span>' % _lt.group(1), 1))
        j, k = run("缺陷B")
        if j < 1 or k != 0:
            print("  !! 门禁恒真：B 未触发 1j" if j < 1 else "  !! B 误触 1k")
            ok = False

    print("轮 4 · 注入 C：M 卡加回 data-difficulty（expect 1k FAIL）")
    if not CARD_DIFF.search(f3):
        print("  !! 未找到注入锚点（M01.01 卡头已变动），中止")
        return 1
    open(ROOT_IDX, "w", encoding="utf-8").write(f2)  # 复位 B
    open(METH, "w", encoding="utf-8").write(
        CARD_DIFF.sub(r'\1 data-difficulty="architect"', f3, count=1))
    j, k = run("缺陷C")
    if k < 1 or j != 0:
        print("  !! 门禁恒真：C 未触发 1k" if k < 1 else "  !! C 误触 1j")
        ok = False

    print("轮 5 · 还原并核对 MD5")
    open(CH1, "w", encoding="utf-8").write(f1)
    open(ROOT_IDX, "w", encoding="utf-8").write(f2)
    open(METH, "w", encoding="utf-8").write(f3)
    b1, b2, b3 = md5(V.read(CH1)), md5(V.read(ROOT_IDX)), md5(V.read(METH))
    same = (b1, b2, b3) == (m1, m2, m3)
    print(f"  还原后 MD5：{b1[:12]} / {b2[:12]} / {b3[:12]}  {'✅ 一致' if same else '❌ 不一致'}")
    if not same:
        ok = False
    j, k = run("还原态")
    if (j, k) != (0, 0):
        ok = False

    print("-" * 56)
    print("PROBE_EXIT=" + ("0 正向验证通过 ✅" if ok else "1 验证失败 ❌"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
