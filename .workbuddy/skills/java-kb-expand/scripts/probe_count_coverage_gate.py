#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 计数保护覆盖门禁 反向验证（probe_count_coverage_gate.py）

对 `validate_kb.run_l1_container_scan`（= `audit_l1_counts.py`）做**反向注入**验证：
把已受保护的计数改回裸文本 / 注入裸计数，门禁必须 FAIL；还原后必须 PASS。

用例：
  A. inline 模式      —— 注入裸「M## 名（N）」（站点已无 mind 页括号式组数载体）
  B. 容器模式         —— 给章节 index `card-footer` 注入裸「N 卡」
  C. **通用兜底（核心）** —— 注入一个**不在 containers 白名单里的全新容器样式**，
                          内放裸「N 项」（勿用「N 卡」：fallback.exempt 豁免了卡/章）
  D. **短块兜底**     —— 注入短块裸「12 项」（图 0d layer-count 已于 2026-10-27 清除）
  E. **正文聚合（核心）** —— 把正文长段落里已保护的「15 篇」去保护；**短块兜底抓不到长段落**，
                          只有真值锚定的 D 段能抓
  F. **正文新增裸计数** —— 往页面注入一段**长正文**（可见文本 > 100 字，绕开短块兜底），
                          内写裸「{total} 道 / {methodology} 张」；证明 D 段不是只认既有位置

C/D/E/F 是 2026-09-21 长官指令「所有计数必须设置门禁保护 + 门禁不得写死编码子集 +
**正文聚合计数也要应管尽严**」的反向证据：若哪天有人把兜底关掉、改回容器枚举，
或把正文段（prose）停用，本 probe 立即变红。

任一用例未如期检出 → 退出码 1（**假绿**，门禁不可信）。
退出码：0=双向验证通过；1=门禁失效；2=定位失败。
"""
import io
import json
import os
import re
import subprocess
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kbroot import find_root  # noqa: E402  项目根唯一实现（禁写死路径）

BASE = find_root(__file__)

SCRIPT = os.path.join(BASE, ".workbuddy/skills/java-kb-expand/scripts/audit_l1_counts.py")
PY3 = sys.executable
CORE = os.path.join(BASE, "java-architect-interview/chapter-core-methodology.html")

# 容器用例目标：章节 index 的 card-footer（2026-10-27：原 card-foot 精确类名已不存在）
_cands = glob.glob(os.path.join(BASE, "java-architect-interview/*.html"))
FOOT = next(
    (p for p in _cands
     if '<div class="card-footer">' in io.open(p, encoding="utf-8").read()),
    None,
)
if not os.path.isfile(CORE) or not FOOT:
    print("定位失败：缺少 methodology 页 / card-footer 载体")
    sys.exit(2)


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
    print("  ❌ 基线非 PASS，无法继续")
    sys.exit(1)


def norm(s):
    return re.sub(r"\s+", "", s)


def inject(path, bad, expect, title, note=""):
    """写坏 → 断言 exit 1 + [计数覆盖] + 命中关键字（空白归一化比较）→ 还原。"""
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
                print("    " + l.strip()[:120])
                break
        print("  exit=%d %s" % (rc, out.strip().split("\n")[-1][:110]))
        print("  %s（要求命中 %r）%s"
              % ("✅ 如期检出" if good else "❌ 未检出 —— 门禁失效", expect,
                 (" " + note) if note else ""))
        ok &= good
    finally:
        restore(path, orig)
        assert io.open(path, encoding="utf-8").read() == orig, "还原失败"
        print("  已还原 %s（逐字节一致）" % os.path.basename(path))


# ---------- A：inline 括号式组数（站点已无存量载体 → 自注入裸 li） ----------
_a = io.open(CORE, encoding="utf-8").read()
_a2 = re.sub(
    r"(</body>)",
    r'<ul data-probe="1"><li>M99 探针组（3）</li></ul>\1',
    _a, count=1)
assert _a2 != _a, "A 注入锚点 </body> 未命中"
inject(CORE, _a2, "括号式组数", "A inline 注入裸「M99 探针组（3）」")

# ---------- B：容器内裸「N 卡」 ----------
_b = io.open(FOOT, encoding="utf-8").read()
_a = _b.find('<div class="card-footer">')
assert _a >= 0
_e = _b.find("</div>", _a)
inject(FOOT, _b[:_e] + " 99 卡" + _b[_e:], "99卡",
       "B card-footer 注入裸「99 卡」")

# ---------- C：全新容器样式（不在白名单）内裸计数 → 只有通用兜底能抓 ----------
# 单位须用「项」：fallback.exempt 豁免了「N 卡 / N 章」，用卡会假绿。
_c = io.open(CORE, encoding="utf-8").read()
_patch = re.sub(
    r"(</body>)",
    r'<div class="probe-brand-new-shell" data-probe="1">本页共 99 项</div>\1',
    _c, count=1)
assert _patch != _c, "注入锚点 </body> 未命中"
inject(CORE, _patch, "99项",
       "C 全新容器样式内裸「99 项」（白名单外）",
       note="← 容器枚举必漏，证明兜底生效")

# ---------- D：短块兜底（图 0d layer-count 已清除 → 自注入短块裸「12 项」） ----------
_d = io.open(CORE, encoding="utf-8").read()
_d2 = re.sub(
    r"(</body>)",
    r'<div data-probe="short">共 12 项</div>\1',
    _d, count=1)
assert _d2 != _d, "D 短块注入锚点未命中"
inject(CORE, _d2, "兜底·短块", "D 短块注入裸「12 项」")

# ---------- E：正文聚合计数去保护（长段落；短块兜底抓不到） ----------
_e = io.open(CORE, encoding="utf-8").read()
_e2 = re.sub(
    r'<span class="kb-count"[^>]*data-kb-pos="P434"[^>]*>(\d+)</span>',
    r"\1", _e, count=1)
assert _e2 != _e, "P434 正文位注入锚点未命中"
inject(CORE, _e2, "正文聚合", "E 正文长段落「15 篇」去保护",
       note="← 短块兜底只覆盖 ≤100 字块，长正文只有真值锚定的 D 段能抓")

# ---------- F：注入一段长正文里的全新裸计数（绕开短块兜底） ----------
# 注入值必须**动态取 V 中的真值**（禁写死）：旧版写死「400 道」锚定彼时 total=400，
# 计数演进后 400 ∉ V，D 段（真值锚定）按设计放行非 V 数字 → 探针假绿。改从 SSOT 取 total。
_ssot = json.load(io.open(os.path.join(BASE, "docs/kb-counts.json"), encoding="utf-8"))
_TOTAL = (_ssot.get("counts") or {}).get("total")
_METH = (_ssot.get("counts") or {}).get("methodology")
assert isinstance(_TOTAL, int) and _TOTAL > 0, "SSOT counts.total 缺失，无法构造 F 用例"
assert isinstance(_METH, int) and _METH > 0, "SSOT counts.methodology 缺失，无法构造 F 用例"
_f = io.open(CORE, encoding="utf-8").read()
_patch = re.sub(
    r"(</body>)",
    ('<p data-probe="1">本库共 %d 道知识点，覆盖 JVM 内存与类加载、并发编程、MySQL 索引与事务、'
     'Redis 缓存治理、消息队列、微服务治理与可观测性等领域；另附 %d 张方法论卡片，'
     '按道法术器势五层组织，供架构决策、故障排查与跨团队表达时快速检索与对照使用。</p>\\1'
     % (_TOTAL, _METH)),
    _f, count=1)
assert _patch != _f, "长正文注入锚点 </body> 未命中"
inject(CORE, _patch, "%d道" % _TOTAL,
       "F 长正文注入裸「%d 道 / %d 张」（值取自 SSOT）" % (_TOTAL, _METH),
       note="← 证明 D 段对**新增**正文计数同样生效，不是只认既有位置")

# ---------- 收尾复跑 ----------
print("\n== 还原后复跑（应 PASS）==")
rc2, out2 = run_gate()
print("  exit=%d %s" % (rc2, out2.strip().split("\n")[-1][:120]))
ok &= rc2 == 0

print("\n%s" % ("✅ 双向验证通过：6 类未保护计数（含白名单外容器 / 短块 / 正文长段落 / 新增正文计数）"
                "全部如期检出，还原后复绿"
                if ok else "❌ 双向验证失败：门禁存在假绿风险"))
sys.exit(0 if ok else 1)
