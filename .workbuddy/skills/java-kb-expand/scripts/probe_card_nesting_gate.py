#!/usr/bin/env python3
"""1i「卡片嵌套」门禁的正向验证：注入缺陷 → 必须 FAIL → 还原并核对 MD5。

背景：2026-09-16 长官实测 chapter-11 的 C11.28 少一个 `</div>`，C11.29/C11.30
被吞进 C11.28 内部（渲染为卡片套卡片），而当时 validate_kb 全绿 —— 说明校验面
缺这一类结构缺陷。本探针证明新增的 1i 门禁「不是恒真」：

  轮 1 当前树       → 期望 failed=0
  轮 2 注入缺陷     → 期望 failed≥1（删掉 chapter-11 中 C11.28 的 `</div>`）
  轮 3 还原 + MD5   → 期望 MD5 与原始一致且 failed=0

只动 chapter-11 一个文件，且结束时用内存中的原文还原。项目根由「向上查找同时含
AGENTS.md + index.html 的祖先目录」推导，不写死层级。
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

TARGET = os.path.join(V.CHAPTER_DIR, "chapter-11-middleware-engineering.html")
ANCHOR = re.compile(r'\n        </div>\n\n        <div class="qa-card" id="C11\.29"')


def md5(t):
    return hashlib.md5(t.encode("utf-8")).hexdigest()


def run(tag):
    V.check.failed = 0
    V.run_card_nesting_check()
    failed = V.check.failed
    print(f"  [{tag}] failed={failed}")
    return failed


def main():
    orig = V.read(TARGET)
    orig_md5 = md5(orig)
    print(f"目标：{os.path.basename(TARGET)}  原始 MD5={orig_md5}")

    ok = True
    print("轮 1 · 当前树（C11.28 已修）")
    if run("修复态") != 0:
        ok = False

    print("轮 2 · 注入缺陷（删 C11.28 的 </div>）")
    if not ANCHOR.search(orig):
        print("  !! 未找到注入锚点（C11.28/C11.29 边界已变动），中止")
        return 1
    open(TARGET, "w", encoding="utf-8").write(
        ANCHOR.sub('\n        <div class="qa-card" id="C11.29"', orig, count=1))
    if run("缺陷态") < 1:
        print("  !! 门禁恒真：注入缺陷后仍 PASS")
        ok = False

    print("轮 3 · 还原并核对 MD5")
    open(TARGET, "w", encoding="utf-8").write(orig)
    back = md5(V.read(TARGET))
    print(f"  还原后 MD5={back}  {'✅ 一致' if back == orig_md5 else '❌ 不一致'}")
    if back != orig_md5 or run("还原态") != 0:
        ok = False

    print("-" * 56)
    print("PROBE_EXIT=" + ("0 正向验证通过 ✅" if ok else "1 验证失败 ❌"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
