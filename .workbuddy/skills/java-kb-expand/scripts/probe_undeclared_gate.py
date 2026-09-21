#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向验证「未登记计数扫描」门禁（scan_undeclared_counts.py）。
=================================================================
为什么需要：门禁若恒真（永远 PASS）形同虚设。本探针在**当前项目文件**里就地注入一个
未登记的计数锚点，验证扫描脚本确实会 FAIL；再还原文件，验证其回到 PASS。

与 probe_truth_gate.py 同一纪律：
  - 自包含：**从当前文件派生注入态**，不依赖 tmp/ 下的历史缺陷快照（那些快照清理后即失效）。
  - try/finally 保证还原：无论断言成败、是否异常，被注入的文件都恢复字节一致。
  - 夹具/环境缺失 → 退出码 3（明确报告，不抛 traceback 误导为「门禁失效」）。

场景：
  轮 1  注入未登记键  __probe_undeclared_x7k2__ 到根 index.html 正文（用已登记的 P01 编号，
        只测「键未登记」这一条路径）→ 期望 scan 脚本 exit 1 且 FAIL 行命中该键。
  轮 2  还原后跑一次   → 期望 exit 0（无误杀，文件已字节级还原）。

用法：python3 probe_undeclared_gate.py
退出码：0 = 各轮符合预期；1 = 门禁未抓到注入（失效）/ 误杀；2 = 定位失败；3 = 环境/夹具缺失。
"""
import io
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kbroot import find_root  # noqa: E402  项目根唯一实现（禁写死路径）

B = find_root(__file__)
if not B:
    print("FAIL 未能定位项目根（须含 docs/kb-counts.json）")
    sys.exit(2)

PY = sys.executable
SCAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_undeclared_counts.py")
if not os.path.isfile(SCAN):
    print("FAIL 未找到 scan_undeclared_counts.py: %s" % SCAN)
    sys.exit(2)

TARGET = os.path.join(B, "index.html")
if not os.path.isfile(TARGET):
    print("SKIP 环境缺失（退出码 3）：根 index.html 不存在")
    sys.exit(3)

BOGUS_KEY = "__probe_undeclared_x7k2__"
# 用已登记的 P01 编号，隔离「键未登记」路径（避免同时触发未登记位编号）
INJECT = ('<span class="probe-undeclared" data-kb-count="%s" '
          'data-kb-pos="P01">1</span>' % BOGUS_KEY)


def run_scan():
    r = subprocess.run([PY, SCAN, B], capture_output=True, text=True, cwd=B)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main():
    orig = io.open(TARGET, encoding="utf-8", errors="ignore").read()
    ok = True
    try:
        # ---- 轮 1：注入未登记锚点 ----
        if "</body>" in orig:
            injected = orig.replace("</body>", INJECT + "</body>", 1)
        else:
            injected = orig + INJECT
        io.open(TARGET, "w", encoding="utf-8").write(injected)

        code, out = run_scan()
        caught = (code == 1) and any(BOGUS_KEY in ln for ln in out.splitlines() if ln.startswith("FAIL "))
        ok &= caught
        print("[1] 注入未登记键 %s：scan exit=%d（期望 1）、命中 FAIL=%s -> %s"
              % (BOGUS_KEY, code, caught, "符合预期 ✅" if caught else "不符预期 ❌"))
        for ln in out.splitlines():
            if ln.startswith("FAIL ") and BOGUS_KEY in ln:
                print("     ", ln)

        # ---- 轮 2：还原后必须 PASS（无误杀）----
        io.open(TARGET, "w", encoding="utf-8").write(orig)
        code2, out2 = run_scan()
        restored = (code2 == 0)
        ok &= restored
        print("[2] 还原后：scan exit=%d（期望 0）-> %s" % (code2, "符合预期 ✅" if restored else "不符预期 ❌"))
        if not restored:
            for ln in out2.splitlines()[:6]:
                print("     ", ln)
    except Exception as e:  # noqa: BLE001  任何异常都要先还原再上报
        ok = False
        print("探针异常：%r" % e)
    finally:
        # 字节级还原（防止断言失败时遗留注入锚点污染根 index）
        io.open(TARGET, "w", encoding="utf-8").write(orig)
        after = io.open(TARGET, encoding="utf-8", errors="ignore").read()
        if after != orig:
            print("❌ 还原失败：根 index.html 内容不一致，请手工检查！")
            return 1

    print("✅ 未登记计数门禁通过双向验证：注入必 FAIL、还原必 PASS，且根 index.html 已字节级还原。"
          if ok else "❌ 未登记计数门禁验证未通过")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
