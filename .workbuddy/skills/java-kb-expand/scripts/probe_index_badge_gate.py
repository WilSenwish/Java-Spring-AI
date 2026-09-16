#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向验证「聚合页徽标结构」门禁（check_index_badges.py）：必须能 FAIL，也必须在当前树上 PASS。

为什么需要：门禁若恒真（永远 PASS）形同虚设。本探针用**权威备份的缺陷版**在沙箱里构造
反例，验证门禁确实会 exit 1；再对当前项目跑一次，验证其不会误杀。

与 probe_list_gate.py 的差异：本探针**不写入项目真实文件**——只在 tmp/ 下建沙箱目录，
因此无需还原、无污染链风险。（overview / 根 index 体积大，就地注入-还原成本高于建沙箱。）

用法：
  python3 probe_index_badge_gate.py            # 双向验证（沙箱 FAIL + 当前树 PASS）
  python3 probe_index_badge_gate.py --expect 29   # 指定缺陷版期望命中数
退出码：0 = 双向验证均符合预期；1 = 任一不符（说明门禁失效或误杀）。
"""
import os
import shutil
import subprocess
import sys

B = '/Users/chenjunbing/Develop/Project/Personal/Java Spring AI'
PY = '/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3'
GATE = B + '/.workbuddy/skills/java-kb-expand/scripts/check_index_badges.py'
BACKUP = B + '/tmp/badge_fix_backup_20260916'
SANDBOX = B + '/tmp/badge_gate_probe'

expect = 29
for i, a in enumerate(sys.argv):
    if a == '--expect' and i + 1 < len(sys.argv):
        expect = int(sys.argv[i + 1])


def run_gate(target=None):
    cmd = [PY, GATE] + ([target] if target else [])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd='/tmp')
    return r.returncode, r.stdout.strip().splitlines()


# ---- 1) 缺陷版（权威备份）必须 FAIL ----
shutil.rmtree(SANDBOX, ignore_errors=True)
os.makedirs(SANDBOX + '/java-architect-interview', exist_ok=True)
open(SANDBOX + '/AGENTS.md', 'w').write('probe sandbox\n')
shutil.copy(BACKUP + '/index.html.bak', SANDBOX + '/index.html')
shutil.copy(BACKUP + '/nav-overview-priority.html.bak',
            SANDBOX + '/java-architect-interview/nav-overview-priority.html')

code, out = run_gate(SANDBOX)
m = out[0] if out else ''
n = 0
if m.startswith('FAIL 发现') and '处缺陷' in m:
    n = int(m.split('发现 ')[1].split(' 处')[0])
ok_fail = (code == 1 and n == expect)

print(f'[1] 缺陷版沙箱：exit={code}（预期 1）、命中 {n} 处（预期 {expect}）'
      f' -> {"符合预期 ✅" if ok_fail else "不符预期 ❌"}')
for l in out[1:4]:
    print('     ', l)

# ---- 2) 当前项目树必须 PASS（无误杀）----
code2, out2 = run_gate()
ok_pass = (code2 == 0 and out2 and out2[0].startswith('PASS'))
print(f'[2] 当前项目：exit={code2}（预期 0）-> {"符合预期 ✅" if ok_pass else "不符预期 ❌"}')
if out2:
    print('     ', out2[0])

shutil.rmtree(SANDBOX, ignore_errors=True)
sys.exit(0 if (ok_fail and ok_pass) else 1)
