#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 计数保护覆盖门禁 反向验证（probe_count_coverage_gate.py）

对 `validate_kb.run_l1_container_scan`（= `audit_l1_counts.py`）做**反向注入**验证：
把已受保护的计数改回裸文本，门禁必须 FAIL；还原后必须 PASS。

用例：
  A. inline 模式      —— mind 页 map-col 的「M## 名（N）」去掉 kb-count 包裹
  B. 容器模式         —— 给某 card-foot 注入裸「N 卡」
  C. **通用兜底（核心）** —— 注入一个**不在 containers 白名单里的全新容器样式**，
                          内放裸「N 卡」；容器枚举必然漏，只有兜底能抓
  D. **短块兜底**     —— 把 chapter-core-methodology 的 layer-count 去保护（裸「12 项」）

C/D 是 2026-09-21 长官指令「所有计数必须设置门禁保护 + 门禁不得写死编码子集」的
反向证据：若哪天有人把兜底关掉或改回容器枚举，本 probe 立即变红。

任一用例未如期检出 → 退出码 1（**假绿**，门禁不可信）。
退出码：0=双向验证通过；1=门禁失效；2=定位失败。
"""
import io, os, re, subprocess, sys, glob

BASE = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI"
SCRIPT = os.path.join(BASE, ".workbuddy/skills/java-kb-expand/scripts/audit_l1_counts.py")
PY3 = "/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3"
MIND = os.path.join(BASE, "java-architect-interview-mind/mind-core-methodology.html")
CORE = os.path.join(BASE, "java-architect-interview/chapter-core-methodology.html")

# 容器用例目标：任一含 card-foot 的页面
_cands = glob.glob(os.path.join(BASE, "java-architect-interview-mind/*.html"))
FOOT = next((p for p in _cands if '<div class="card-foot">' in io.open(p, encoding="utf-8").read()), None)
if not all(os.path.isfile(p) for p in (MIND, CORE)) or not FOOT:
    print("定位失败：缺少 mind 页 / core 页 / card-foot 载体"); sys.exit(2)


def run_gate():
    p = subprocess.run([PY3, SCRIPT], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def restore(path, text):
    io.open(path, "w", encoding="utf-8").write(text)


ok = True
print("== 基线（应 PASS）==")
rc0, out0 = run_gate()
print("  exit=%d %s" % (rc0, out0.strip().split("\n")[-1][:120]))
if rc0 != 0:
    print("  ❌ 基线非 PASS，无法继续"); sys.exit(1)


def norm(s):
    return re.sub(r"\s+", "", s)


def inject(path, bad, expect, title, note=""):
    """写坏 → 断言 exit 1 + [计数覆盖] + 命中关键字（空白归一化比较）→ 还原。返回是否通过。"""
    global ok
    print("\n== 用例 %s ==" % title)
    orig = io.open(path, encoding="utf-8").read()
    try:
        restore(path, bad)
        rc, out = run_gate()
        good = rc == 1 and "[计数覆盖]" in out and norm(expect) in norm(out)
        print("  目标 %s" % os.path.relpath(path, BASE))
        for l in out.strip().split("\n"):
            if "FAIL [计数覆盖]" in l:
                print("    " + l.strip()[:120]); break
        print("  exit=%d %s" % (rc, out.strip().split("\n")[-1][:110]))
        print("  %s（要求命中 %r）%s"
              % ("✅ 如期检出" if good else "❌ 未检出 —— 门禁失效", expect, (" " + note) if note else ""))
        ok &= good
    finally:
        restore(path, orig)
        assert io.open(path, encoding="utf-8").read() == orig, "还原失败"
        print("  已还原 %s（逐字节一致）" % os.path.basename(path))


# ---------- A：inline 括号式组数去保护 ----------
_orig = io.open(MIND, encoding="utf-8").read()
m = re.search(r'<li>(M\d\d [^<（]*?（)<span class="kb-count"[^>]*data-kb-pos="(P\d+)"[^>]*>(\d+)</span>(）)</li>',
              _orig)
if not m:
    print("  ❌ 未找到可注入的已保护 li"); sys.exit(2)
inject(MIND,
       _orig[:m.start()] + '<li>%s%s%s</li>' % (m.group(1), m.group(3), m.group(4)) + _orig[m.end():],
       "括号式组数", "A inline「M## 名（N）」去保护")

# ---------- B：容器内裸「N 卡」 ----------
_b = io.open(FOOT, encoding="utf-8").read()
_a = _b.find('<div class="card-foot">')
assert _a >= 0
_e = _b.find("</div>", _a)
inject(FOOT, _b[:_e] + " 99 卡" + _b[_e:], "99卡", "B card-foot 注入裸「99 卡」")

# ---------- C：全新容器样式（不在白名单）内裸计数 → 只有通用兜底能抓 ----------
_c = io.open(MIND, encoding="utf-8").read()
_patch = re.sub(
    r"(</body>)",
    r'<div class="probe-brand-new-shell" data-probe="1">本页共 99 卡</div>\1',
    _c, count=1)
assert _patch != _c, "注入锚点 </body> 未命中"
inject(MIND, _patch, "99卡",
       "C 全新容器样式内裸「99 卡」（白名单外）",
       note="← 容器枚举必漏，证明兜底生效")

# ---------- D：短块兜底（layer-count 去保护） ----------
_d = io.open(CORE, encoding="utf-8").read()
_d2 = re.sub(
    r'<span class="layer-count"><span class="kb-count"[^>]*data-kb-pos="(P\d+)"[^>]*>(\d+)</span>',
    r'<span class="layer-count">\2', _d, count=1)
assert _d2 != _d, "layer-count 注入锚点未命中"
inject(CORE, _d2, "兜底·短块", "D layer-count 去保护（裸「12 项」）")

# ---------- 收尾复跑 ----------
print("\n== 还原后复跑（应 PASS）==")
rc2, out2 = run_gate()
print("  exit=%d %s" % (rc2, out2.strip().split("\n")[-1][:120]))
ok &= rc2 == 0

print("\n%s" % ("✅ 双向验证通过：4 类未保护计数（含白名单外容器 / 短块）全部如期检出，还原后复绿"
                if ok else "❌ 双向验证失败：门禁存在假绿风险"))
sys.exit(0 if ok else 1)
