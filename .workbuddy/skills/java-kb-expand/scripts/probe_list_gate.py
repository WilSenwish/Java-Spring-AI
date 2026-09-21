#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向验证 1h「列表缩进兜底」门禁：注入缺陷 → 跑校验 → 必须 FAIL → 自动还原

两轮的注入态**都从当前 design-system.css 派生**（2026-09-21 加固）：
  轮 1：删除零特异度 `:where(ul, ol) { padding-inline-start: 1.25rem; }`   → 期望命中「须含」
  轮 2：保留兜底、另加裸选择器 `ul, ol { … }`（特异度更高会盖掉兜底）      → 期望命中「不得用裸选择器」

此前脚本依赖 `tmp/list_indent_backup/design-system.after.css` 这个历史夹具：
夹具随 `tmp/` 清理而消失 → 脚本直接 FileNotFoundError（被误读成「门禁失效」），
且注入时直写**真实** CSS 文件、还原交给调用方（一旦中途失败就留下脏树）。
现在：就地派生 + `finally` 还原 + MD5 核验。

用法：probe_list_gate.py [1|2]   （缺省跑完两轮）
退出码：0=双向验证通过；1=门禁失效；2=定位失败。
"""
import hashlib
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _kbroot import find_root  # noqa: E402  项目根唯一实现（禁写死路径）

B = find_root(__file__) or sys.exit(2)
PY = sys.executable
GATE = os.path.join(HERE, "validate_kb.py")
CSS = os.path.join(B, "java-architect-interview/assets/design-system.css")

ROUNDS = [sys.argv[1]] if (len(sys.argv) > 1 and sys.argv[1] in ("1", "2")) else ["1", "2"]

FALLBACK = re.compile(r":where\(ul,\s*ol\)\s*\{\s*padding-inline-start:\s*1\.25rem;\s*\}")


def read(p):
    return io.open(p, encoding="utf-8").read()


def md5(p):
    return hashlib.md5(io.open(p, "rb").read()).hexdigest()


ORIG = read(CSS)
ORIG_MD5 = md5(CSS)
ok = True

for rnd in ROUNDS:
    print("\n== 轮 %s ==" % rnd)
    try:
        if rnd == "1":
            if not FALLBACK.search(ORIG):
                print("  !! 未找到注入锚点（CSS 无零特异度缩进兜底），本用例判失败")
                ok = False
                continue
            io.open(CSS, "w", encoding="utf-8").write(
                FALLBACK.sub("/* probe: removed */", ORIG, count=1))
            expect_needle = "须含零特异度缩进兜底"
        else:
            if ":where(ul, ol) {" not in ORIG:
                print("  !! 未找到注入锚点（CSS 无 :where(ul, ol)）")
                ok = False
                continue
            io.open(CSS, "w", encoding="utf-8").write(
                ORIG.replace(":where(ul, ol) {",
                             "ul, ol {\n  padding-inline-start: 1.25rem;\n}\n:where(ul, ol) {", 1))
            expect_needle = "不得用裸选择器"

        r = subprocess.run([PY, GATE], capture_output=True, text=True, cwd=B)
        out = (r.stdout or "") + (r.stderr or "")
        hits = [l for l in out.split("\n") if "FAIL" in l and "[列表]" in l]
        for l in hits:
            print("  " + l.strip()[:150])
        good = r.returncode != 0 and any(expect_needle in l for l in hits)
        print("  校验 exit=%d，命中 [列表] FAIL %d 条（须含 %r）%s"
              % (r.returncode, len(hits), expect_needle, "✅ 如期检出" if good else "❌ 未检出"))
        ok &= good
    finally:
        io.open(CSS, "w", encoding="utf-8").write(ORIG)
        print("  已还原 design-system.css（MD5 一致: %s）" % (md5(CSS) == ORIG_MD5))

print("\nPROBE_EXIT=%s" % ("0 双向验证通过 ✅" if ok else "1 门禁失效 ❌"))
sys.exit(0 if ok else 1)
