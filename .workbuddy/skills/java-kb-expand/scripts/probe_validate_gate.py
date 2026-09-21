#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向验证 1g「横向溢出兜底」门禁：临时注入缺陷 → 跑校验 → 必须 FAIL → 自动还原

两处缺陷（都从**当前文件**派生，不依赖任何 `tmp/` 历史夹具）：
  ① design-system.css 摘掉 `body{overflow-wrap:anywhere}` 全局兜底
  ② 安全检查页把一个 `.code-block` 拆开，制造未被包裹的裸 `<pre>`

**2026-09-21 加固**：此前 ② 直接 `shutil.copy(tmp/bare_pre_backup/...)`——
夹具随 `tmp/` 清理而消失，脚本抛 FileNotFoundError（被误读成「门禁失效」），
且若夹具是旧版本还会把页面还原成旧内容。现在改为「就地派生注入 + finally 还原 + MD5 核验」。

退出码：0=双向验证通过（两条缺陷都被拦下且还原一致）；1=门禁失效；2=定位失败。
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
PAGE = os.path.join(B, "java-architect-interview/nav-server-security-checkpoint.html")


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, t):
    io.open(p, "w", encoding="utf-8").write(t)


def md5(p):
    return hashlib.md5(io.open(p, "rb").read()).hexdigest()


orig = {p: read(p) for p in (CSS, PAGE)}
before = {p: md5(p) for p in (CSS, PAGE)}
ok = True

try:
    # ---- 缺陷 ①：摘掉 CSS 全局换行兜底（只动 body 规则内的那一条，全站共 10 处同名声明） ----
    t = orig[CSS]
    pat = re.compile(r"(^\s*body\s*\{[^}]*?)overflow-wrap:\s*anywhere", re.M)
    assert len(pat.findall(t)) == 1, "body 规则内 overflow-wrap 命中 %d 次" % len(pat.findall(t))
    write(CSS, pat.sub(r"\1/* probe-removed */", t, count=1))

    # ---- 缺陷 ②：派生裸 pre（拆掉一个 .code-block 包裹） ----
    p0 = orig[PAGE]
    m = re.search(r'<div class="code-block">(\s*)<pre', p0)
    assert m, "未找到 .code-block 包裹的 <pre> 锚点"
    write(PAGE, p0[:m.start()] + "<pre" + p0[m.end():])

    r = subprocess.run([PY, GATE], capture_output=True, text=True, cwd=B)
    out = (r.stdout or "") + (r.stderr or "")
    fails = [l for l in out.split("\n") if "FAIL" in l and "溢出" in l]
    print("=== 注入缺陷后的校验输出 ===")
    for l in fails:
        print("  " + l.strip()[:150])
    hit_ok = len(fails) >= 2 and r.returncode != 0
    print("\n命中「溢出」类 FAIL %d 条（期望 ≥2：CSS 兜底 + 裸 pre）；校验退出码 %d %s"
          % (len(fails), r.returncode, "✅" if hit_ok else "❌"))
    ok &= hit_ok
finally:
    for p, t in orig.items():
        if read(p) != t:
            write(p, t)
    same = all(md5(p) == before[p] for p in orig)
    print("=== 还原核验 ===\n  CSS MD5 一致: %s\n  页面 MD5 一致: %s"
          % (md5(CSS) == before[CSS], md5(PAGE) == before[PAGE]))
    print("  还原状态:", "✅ OK（逐字节一致）" if same else "❌ 还原失败")
    ok &= same

print("\nPROBE_EXIT=%s" % ("0 双向验证通过 ✅" if ok else "1 门禁失效 ❌"))
sys.exit(0 if ok else 1)
