#!/usr/bin/env python3
"""1c-2「图表深色适配」门禁的正向验证（注入缺陷 → 必须 FAIL → 还原核 MD5）

两轮：① 图内注入未映射内联色 #abcdef 须 FAIL；② 删掉深色块 cScale0 须 FAIL。
全程 try/finally 内存还原，跑完核对两文件 MD5 一致。
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

BASE = None
d = os.path.dirname(os.path.abspath(__file__))
while d != os.path.dirname(d):
    if os.path.isfile(os.path.join(d, "AGENTS.md")) and os.path.isfile(os.path.join(d, "index.html")):
        BASE = d
        break
    d = os.path.dirname(d)
if not BASE:
    sys.exit("找不到项目根")

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate_kb.py")
PAGE = os.path.join(BASE, "java-architect-interview/chapter-05-spring-core.html")
JS = os.path.join(BASE, "java-architect-interview/assets/theme-init.js")


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def run_gate():
    r = subprocess.run([sys.executable, SCRIPT], cwd=BASE, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def expect(cond, label):
    print(("  ✅ " if cond else "  ❌ ") + label)
    return cond


ok = True
before = {p: md5(p) for p in (PAGE, JS)}
originals = {p: open(p, encoding="utf-8").read() for p in (PAGE, JS)}


def restore_all():
    for p, txt in originals.items():
        open(p, "w", encoding="utf-8").write(txt)


print("初始 MD5:")
for p in before:
    print("  ", os.path.basename(p), before[p])

try:
    # ---- 注入 A：图内出现未映射的内联色 ----
    print("\n[注入 A] mermaid 内联色 #abcdef（未纳入映射）")
    src = originals[PAGE]
    marker = '<div class="mermaid">\n'
    i = src.find(marker)
    open(PAGE, "w", encoding="utf-8").write(
        src[: i + len(marker)] + "    style ZZZ fill:#abcdef,stroke:#abcdef\n" + src[i + len(marker):]
    )
    rc, out = run_gate()
    ok &= expect(rc != 0, f"门禁应 FAIL（实际 RC={rc}）")
    ok &= expect("未纳入深色改写映射" in out and "#abcdef" in out, "报错须点名未映射色值")
    if rc == 0:
        print(out[-1600:])
    open(PAGE, "w", encoding="utf-8").write(src)
    ok &= expect(md5(PAGE) == before[PAGE], "还原后 PAGE MD5 一致")
    rc2, _ = run_gate()
    ok &= expect(rc2 == 0, f"还原后门禁应恢复 PASS（实际 RC={rc2}）")

    # ---- 注入 B：删掉深色 cScale0 ----
    print("\n[注入 B] 删除深色块 cScale0")
    js = originals[JS]
    js2 = js.replace("    cScale0: '#1e3a5f',\n", "", 1)
    ok &= expect(js2 != js, "注入生效（确有待删行）")
    open(JS, "w", encoding="utf-8").write(js2)
    rc, out = run_gate()
    ok &= expect(rc != 0, f"门禁应 FAIL（实际 RC={rc}）")
    ok &= expect("cScale0" in out, "报错须点名 cScale0")
    if rc == 0:
        print(out[-1600:])
    open(JS, "w", encoding="utf-8").write(js)
    ok &= expect(md5(JS) == before[JS], "还原后 JS MD5 一致")
finally:
    restore_all()
    for p in before:
        if md5(p) != before[p]:
            print(f"  ⚠️ {os.path.basename(p)} 还原失败")
            ok = False

rc, out = run_gate()
ok &= expect(rc == 0, f"最终门禁 PASS（实际 RC={rc}）")
print("\n总判定:", "✅ 正向验证通过（断言可捕获缺陷，且无误伤）" if ok else "❌ 存在问题")
sys.exit(0 if ok else 1)
