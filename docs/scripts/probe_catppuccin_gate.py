#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_catppuccin_gate · 配色门禁双向验证（改门禁后必跑）

用例（全部真实文件注入 + try/finally 还原，不依赖临时目录夹具）：
  1. 基线：未注入时 audit_catppuccin 必 PASS；
  2. CSS 注入非 palette hex（color:#123456）→ 必 FAIL；
  3. HTML 注入未登记的内联图表 colon 形 hex（fill:#234567）→ 必 FAIL
     （同时命中「hex 色源」与「RETINT 覆盖」两维）；
  4. 还原后复跑 → 必 PASS。

任一断言不成立即 exit 1（门禁假绿比 FAIL 更危险）。
"""
import glob
import os
import signal
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_SCRIPTS = os.path.normpath(os.path.join(
    _HERE, "..", "..", ".workbuddy", "skills", "java-kb-expand", "scripts"))
sys.path.insert(0, _SKILL_SCRIPTS)
from _kbroot import find_root  # noqa: E402


# 安全加固（2026-11-09）：SIGTERM 默认终止不执行 finally，注入态会残留污染。
# 转 SystemExit 使 finally 还原逻辑在超时/被杀时仍能运行。
def _sigterm_to_exit(*_):
    raise SystemExit(1)

signal.signal(signal.SIGTERM, _sigterm_to_exit)

BASE = find_root(__file__)
if not BASE:
    raise SystemExit("定位失败：未找到项目根")

AUDIT = os.path.join(BASE, "docs", "scripts", "audit_catppuccin.py")
CSS_TARGET = os.path.join(BASE, "java-architect-interview", "assets", "design-system.css")

_chapters = sorted(glob.glob(os.path.join(
    BASE, "java-architect-interview", "chapter-*.html")))
if not os.path.isfile(AUDIT) or not os.path.isfile(CSS_TARGET) or not _chapters:
    raise SystemExit("缺夹具：audit 脚本 / design-system.css / 章节 HTML 之一缺失，无法验证")

HTML_TARGET = _chapters[0]


def run_audit():
    r = subprocess.run([sys.executable, AUDIT], capture_output=True, text=True)
    return r.returncode


def inject(path, payload):
    """注入并返回还原函数（try/finally 消费）。"""
    orig = open(path, encoding="utf-8").read()
    with open(path, "a", encoding="utf-8") as f:
        f.write(payload)

    def restore():
        with open(path, "w", encoding="utf-8") as f:
            f.write(orig)

    return restore


def main():
    results = []

    # 用例 1：基线必 PASS
    rc = run_audit()
    results.append(("用例1 基线 PASS", rc == 0))

    # 用例 2：CSS 注入非 palette hex → 必 FAIL
    r2 = inject(CSS_TARGET, "\n/* probe */.kb-probe-x{color:#123456}\n")
    try:
        rc = run_audit()
        results.append(("用例2 CSS 注入 #123456 → FAIL", rc != 0))
    finally:
        r2()

    # 用例 3：HTML 注入未登记内联图表 colon hex → 必 FAIL
    r3 = inject(HTML_TARGET, '\n<style>/* probe */.kb-probe-y{fill:#234567}</style>\n')
    try:
        rc = run_audit()
        results.append(("用例3 HTML 注入 fill:#234567 → FAIL", rc != 0))
    finally:
        r3()

    # 用例 4：还原后必 PASS
    rc = run_audit()
    results.append(("用例4 还原后 PASS", rc == 0))

    ok = True
    print("== probe_catppuccin_gate ==")
    for name, passed in results:
        print(("PASS  " if passed else "FAIL  ") + name)
        ok = ok and passed
    print("\nALL PASS" if ok else "\nPROBE FAIL（门禁可能假绿，禁止交付）")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
