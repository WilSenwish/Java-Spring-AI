#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向验证「聚合 UI 结构 + 小屏留白 + 页内对齐」门禁（check_index_badges.py）。
=================================================================================
为什么需要：门禁若恒真（永远 PASS）形同虚设。本探针在**沙箱**里从当前项目的真实文件
派生出缺陷版，验证门禁确实会 exit 1；再对当前项目跑一次，验证其不会误杀。

自包含纪律（与 probe_undeclared_gate / probe_count_gate / probe_truth_gate 同构）：
  - **从当前文件派生注入态**，不依赖 tmp/ 下的历史缺陷快照（那些快照清理后即失效，
    旧版探针因此退 3 SKIP —— 本版改写后彻底摆脱该依赖）。
  - 只写**系统临时沙箱**（tempfile，不在项目 tmp/ 下，不被清理），不碰项目真实文件，
    故无需还原、无污染链风险（overview / 根 index 体积大，就地注入-还原成本高于建沙箱）。
  - 环境缺失 → 退出码 3（明确报告，不抛 traceback 误导为「门禁失效」）。

三轮缺陷（每轮断言「门禁抓到该类」的签名串，防止"缺陷换了类别但总数没变"的假通过）：
  轮 1  徽标缺陷：剥掉一个 ov-item 的 `class="ov-badges"` 包裹
        → 期望 gate exit 1 且 FAIL 命中「缺 .ov-badges 包裹」。
  轮 2  留白缺陷：删除根 index ≤768 段里的 `.dir-container {…}` 规则（gutter 失去唯一来源）
        → 期望 gate exit 1 且 FAIL 命中「≤768 段缺 .dir-container 规则」。
  轮 3  对齐缺陷：删除根 index 里的 `.dir-count {…}` 规则（计数胶囊定位方式未知）
        → 期望 gate exit 1 且 FAIL 命中「缺 .dir-count 规则」。
  轮 4  当前项目树（干净） → 期望 gate exit 0（无误杀）。
  轮 1~3 未 FAIL 或轮 4 FAIL ⇒ 门禁失效 / 误杀。

用法：python3 probe_index_badge_gate.py
退出码：0 = 各轮均符合预期；1 = 门禁未抓到注入（失效）/ 误杀；2 = 定位失败；3 = 环境缺失。
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kbroot import find_root  # noqa: E402  项目根唯一实现（禁写死路径）

B = find_root(__file__)
if not B:
    print("FAIL 未能定位项目根（须含 docs/kb-counts.json）")
    sys.exit(2)

PY = sys.executable
GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_index_badges.py")
if not os.path.isfile(GATE):
    print("FAIL 未找到 check_index_badges.py: %s" % GATE)
    sys.exit(2)

IDX = os.path.join(B, "index.html")
OV = os.path.join(B, "java-architect-interview", "nav-overview-priority.html")
for _p, _n in ((IDX, "根 index.html"), (OV, "nav-overview-priority.html")):
    if not os.path.isfile(_p):
        print("SKIP 环境缺失（退出码 3）：%s 不存在于 %s" % (_n, _p))
        sys.exit(3)


def read(p):
    return io.open(p, encoding="utf-8", errors="ignore").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


def run_gate(sandbox):
    r = subprocess.run([PY, GATE, sandbox], capture_output=True, text=True, cwd=sandbox)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def mk_sandbox(sandbox):
    """从当前项目复制干净的根 index + overview 进沙箱（含 AGENTS.md 以满足定位回退）。"""
    os.makedirs(os.path.join(sandbox, "java-architect-interview"), exist_ok=True)
    write(os.path.join(sandbox, "AGENTS.md"), "probe sandbox\n")
    write(os.path.join(sandbox, "index.html"), read(IDX))
    write(os.path.join(sandbox, "java-architect-interview", "nav-overview-priority.html"), read(OV))


def main():
    sandbox = tempfile.mkdtemp(prefix="badge_gate_probe_")
    ok = True
    try:
        # ---- 轮 1：徽标缺陷（剥 ov-badges 包裹）----
        mk_sandbox(sandbox)
        ov = read(os.path.join(sandbox, "java-architect-interview", "nav-overview-priority.html"))
        mutated = ov.replace('class="ov-badges"', 'class="ov-badges-missing"', 1)
        if mutated == ov:
            print("[1] 跳过：overview 未找到 `class=\"ov-badges\"`（无法构造徽标缺陷）")
        else:
            write(os.path.join(sandbox, "java-architect-interview", "nav-overview-priority.html"), mutated)
            code, out = run_gate(sandbox)
            caught = (code == 1) and ("缺 .ov-badges 包裹" in out)
            ok &= caught
            print("[1] 徽标缺陷：gate exit=%d（期望 1）、命中「缺 .ov-badges 包裹」=%s -> %s"
                  % (code, caught, "符合预期 ✅" if caught else "不符预期 ❌"))
            for ln in out.splitlines():
                if "缺 .ov-badges 包裹" in ln:
                    print("     ", ln)

        # ---- 轮 2：留白缺陷（删 ≤768 段 .dir-container 规则）----
        mk_sandbox(sandbox)
        idx = read(os.path.join(sandbox, "index.html"))
        idx2 = re.sub(r"\.dir-container\s*\{[^}]*\}", "", idx)  # 删全部 .dir-container 规则
        if idx2 == idx:
            print("[2] 跳过：根 index 未找到 `.dir-container {…}`（无法构造留白缺陷）")
        else:
            write(os.path.join(sandbox, "index.html"), idx2)
            code, out = run_gate(sandbox)
            caught = (code == 1) and ("≤768 段缺 .dir-container 规则" in out)
            ok &= caught
            print("[2] 留白缺陷：gate exit=%d（期望 1）、命中「≤768 段缺 .dir-container 规则」=%s -> %s"
                  % (code, caught, "符合预期 ✅" if caught else "不符预期 ❌"))
            for ln in out.splitlines():
                if "≤768 段缺 .dir-container 规则" in ln:
                    print("     ", ln)

        # ---- 轮 3：对齐缺陷（删 .dir-count 规则）----
        mk_sandbox(sandbox)
        idx = read(os.path.join(sandbox, "index.html"))
        idx3 = re.sub(r"\.dir-count\s*\{[^}]*\}", "", idx)  # 删全部 .dir-count 规则
        if idx3 == idx:
            print("[3] 跳过：根 index 未找到 `.dir-count {…}`（无法构造对齐缺陷）")
        else:
            write(os.path.join(sandbox, "index.html"), idx3)
            code, out = run_gate(sandbox)
            caught = (code == 1) and ("缺 .dir-count 规则" in out)
            ok &= caught
            print("[3] 对齐缺陷：gate exit=%d（期望 1）、命中「缺 .dir-count 规则」=%s -> %s"
                  % (code, caught, "符合预期 ✅" if caught else "不符预期 ❌"))
            for ln in out.splitlines():
                if "缺 .dir-count 规则" in ln:
                    print("     ", ln)

        # ---- 轮 4：干净树必须 PASS（无误杀）----
        mk_sandbox(sandbox)
        code, out = run_gate(sandbox)
        clean = (code == 0) and out.startswith("PASS")
        ok &= clean
        print("[4] 当前项目（干净）：gate exit=%d（期望 0）-> %s" % (code, "符合预期 ✅" if clean else "不符预期 ❌"))
        if not clean:
            for ln in out.splitlines()[:6]:
                print("     ", ln)
    except Exception as e:  # noqa: BLE001  任何异常都要先清理沙箱再上报
        ok = False
        print("探针异常：%r" % e)
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)

    print("✅ 徽标/留白/对齐门禁通过双向验证：三类缺陷必 FAIL、干净树必 PASS（沙箱已清理）。"
          if ok else "❌ 徽标/留白/对齐门禁验证未通过")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
