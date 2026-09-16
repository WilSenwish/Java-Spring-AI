#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向验证「聚合 UI 结构 + 小屏留白 + 页内对齐」门禁（check_index_badges.py）。
=================================================================
为什么需要：门禁若恒真（永远 PASS）形同虚设。本探针用**权威备份的缺陷版**在沙箱里构造
反例，验证门禁确实会 exit 1；再对当前项目跑一次，验证其不会误杀。

与 probe_list_gate.py 的差异：本探针**不写入项目真实文件**——只在 tmp/ 下建沙箱目录，
因此无需还原、无污染链风险（overview / 根 index 体积大，就地注入-还原成本高于建沙箱）。

五轮场景（每轮都断言分类计数，防止"缺陷换了类别但总数没变"的假通过）：
  轮 1  徽标缺陷版     tmp/badge_fix_backup_20260916          → 徽标 = 29、留白 > 0
  轮 2  留白缺陷版     tmp/root_index_mobile_backup_20260916  → 留白 > 0、徽标 = 0
  轮 3  对齐缺陷版     tmp/root_index_style_backup_20260916   → 对齐 = 8、留白 = 3、徽标 = 0
  轮 4  内缩/计数缺陷版 tmp/root_index_unify_backup_20260916    → 对齐 = 2、留白 = 1、徽标 = 0
       （必须命中两条新口径：`.dir-count 缺 margin-left: auto` 与 `桌面 .dir-group 横向 ≠ 0`）
  轮 5  当前项目树                                             → 期望 exit 0
  轮 5 通过但轮 1~4 未 FAIL ⇒ 门禁恒真；轮 5 FAIL ⇒ 门禁误杀。

用法：python3 probe_index_badge_gate.py [--expect-badge 29] [--expect-align 6]
退出码：0 = 各轮均符合预期；1 = 任一不符。
"""
import os
import re
import shutil
import subprocess
import sys

B = '/Users/chenjunbing/Develop/Project/Personal/Java Spring AI'
PY = '/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3'
GATE = B + '/.workbuddy/skills/java-kb-expand/scripts/check_index_badges.py'
BADGE_BK = B + '/tmp/badge_fix_backup_20260916'
MOBILE_BK = B + '/tmp/root_index_mobile_backup_20260916'
STYLE_BK = B + '/tmp/root_index_style_backup_20260916'
UNIFY_BK = B + '/tmp/root_index_unify_backup_20260916'   # 2026-09-16「两类列表风格归一」改前
SANDBOX = B + '/tmp/badge_gate_probe'
LIVE_OV = 'java-architect-interview/nav-overview-priority.html'

expect_badge, expect_align = 29, 8       # 轮 3 对齐：增补两条口径后由 6 → 8
expect_gutter3 = 3                       # 轮 3 留白：小屏 .dir-group/.q-list/.q-item 各 4px（内缩未单层化）
expect_align4, expect_gutter4 = 2, 1     # 轮 4：计数缺 margin-left:auto + 桌面 .dir-group 横向 16px
for i, a in enumerate(sys.argv):
    if a == '--expect-badge' and i + 1 < len(sys.argv):
        expect_badge = int(sys.argv[i + 1])
    if a == '--expect-align' and i + 1 < len(sys.argv):
        expect_align = int(sys.argv[i + 1])


def run_gate(target=None):
    cmd = [PY, GATE] + ([target] if target else [])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd='/tmp')
    return r.returncode, r.stdout.strip()


def counts(out):
    """解析 `FAIL 发现 N 处缺陷（徽标结构 X / 小屏留白 Y / 页内对齐 Z / 变量解析 W）：`。"""
    m = re.search(r'徽标结构 (\d+) / 小屏留白 (\d+)(?: / 页内对齐 (\d+) / 变量解析 (\d+))?', out)
    if m:
        return (int(m.group(1)), int(m.group(2)),
                int(m.group(3) or 0), int(m.group(4) or 0))
    if out.startswith('PASS'):
        return 0, 0, 0, 0
    return -1, -1, -1, -1


def make_sandbox(index_src, ov_src):
    shutil.rmtree(SANDBOX, ignore_errors=True)
    os.makedirs(SANDBOX + '/java-architect-interview', exist_ok=True)
    open(SANDBOX + '/AGENTS.md', 'w').write('probe sandbox\n')
    shutil.copy(index_src, SANDBOX + '/index.html')
    shutil.copy(ov_src, SANDBOX + '/' + LIVE_OV)


ok = True

# ---- 轮 1：徽标缺陷 ----
make_sandbox(BADGE_BK + '/index.html.bak', BADGE_BK + '/nav-overview-priority.html.bak')
code, out = run_gate(SANDBOX)
bd, gu, al, uv = counts(out)
r1 = (code == 1 and bd == expect_badge and gu > 0)
ok &= r1
print(f'[1] 徽标缺陷版：exit={code}（期望 1）、徽标 {bd}（期望 {expect_badge}）、留白 {gu}（期望 >0）'
      f' -> {"符合预期 ✅" if r1 else "不符预期 ❌"}')

# ---- 轮 2：留白缺陷（overview 用当前已修版本 → 徽标应为 0）----
make_sandbox(MOBILE_BK + '/index.html.bak', B + '/' + LIVE_OV)
code, out = run_gate(SANDBOX)
bd, gu, al, uv = counts(out)
r2 = (code == 1 and bd == 0 and gu > 0)
ok &= r2
print(f'[2] 留白缺陷版：exit={code}（期望 1）、徽标 {bd}（期望 0）、留白 {gu}（期望 >0）'
      f' -> {"符合预期 ✅" if r2 else "不符预期 ❌"}')

# ---- 轮 3：对齐缺陷（本轮改前，留白已归一 → 留白应为 0）----
if os.path.isfile(STYLE_BK + '/index.html.bak'):
    make_sandbox(STYLE_BK + '/index.html.bak', B + '/' + LIVE_OV)
    code, out = run_gate(SANDBOX)
    bd, gu, al, uv = counts(out)
    r3 = (code == 1 and al == expect_align and gu == expect_gutter3 and bd == 0)
    ok &= r3
    print(f'[3] 对齐缺陷版：exit={code}（期望 1）、对齐 {al}（期望 {expect_align}）、'
          f'留白 {gu}（期望 {expect_gutter3}）、徽标 {bd}（期望 0） -> '
          f'{"符合预期 ✅" if r3 else "不符预期 ❌"}')
    for line in out.splitlines()[1:4]:
        print('     ', line)
else:
    print(f'[3] 跳过：未找到对齐缺陷备份 {STYLE_BK}/index.html.bak')

# ---- 轮 4：列表内缩单层化 / 计数胶囊位置 缺陷（本轮改前）----
# 除分类计数外，额外断言**两条新口径确实被触发** —— 防止"新断言写成恒真"。
if os.path.isfile(UNIFY_BK + '/index.html.bak'):
    make_sandbox(UNIFY_BK + '/index.html.bak', B + '/' + LIVE_OV)
    code, out = run_gate(SANDBOX)
    bd, gu, al, uv = counts(out)
    r4 = (code == 1 and al == expect_align4 and gu == expect_gutter4 and bd == 0
          and 'margin-left: auto' in out and '桌面 .dir-group 横向' in out)
    ok &= r4
    print(f'[4] 内缩/计数位置缺陷版：exit={code}（期望 1）、对齐 {al}（期望 {expect_align4}）、'
          f'留白 {gu}（期望 {expect_gutter4}） -> {"符合预期 ✅" if r4 else "不符预期 ❌"}')
    for line in out.splitlines()[1:]:
        print('     ', line)
else:
    print(f'[4] 跳过：未找到备份 {UNIFY_BK}/index.html.bak')

# ---- 轮 5：当前项目树必须 PASS（无误杀）----
code, out = run_gate()
rcur = (code == 0 and out.startswith('PASS'))
ok &= rcur
print(f'[5] 当前项目：exit={code}（期望 0）-> {"符合预期 ✅" if rcur else "不符预期 ❌"}')
print('     ', out.splitlines()[0] if out else '')

shutil.rmtree(SANDBOX, ignore_errors=True)
sys.exit(0 if ok else 1)
