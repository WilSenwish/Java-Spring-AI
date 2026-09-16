#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向验证 1h 列表缩进兜底门禁：单轮注入缺陷 -> 跑校验 -> 必须 FAIL

用法: probe_list_gate.py 1|2
  轮 1：删除整条 :where(ul, ol) 兜底          -> 期望命中「须含零特异度缩进兜底」
  轮 2：保留兜底、另加裸选择器 ul, ol { … }    -> 期望命中「不得用裸选择器」

注入态始终由权威备份 tmp/list_indent_backup/design-system.after.css 构造（无污染链）；
还原由调用方命令负责（脚本不写回权威备份）。
"""
import re, subprocess, sys

B = '/Users/chenjunbing/Develop/Project/Personal/Java Spring AI'
PY = '/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3'
CSS = B + '/java-architect-interview/assets/design-system.css'
AUTH = B + '/tmp/list_indent_backup/design-system.after.css'

rnd = sys.argv[1] if len(sys.argv) > 1 else '1'
t = open(AUTH, encoding='utf-8').read()

if rnd == '1':
    t2 = re.sub(r":where\(ul, ol\) \{\s*padding-inline-start: 1\.25rem;\s*\}",
                '/* probe: removed */', t, count=1)
else:
    t2 = t.replace(':where(ul, ol) {',
                   ':where(ul, ol) {\n  padding-inline-start: 1.25rem;\n}\nul, ol {', 1)
assert t2 != t, '注入模式未匹配'
open(CSS, 'w', encoding='utf-8').write(t2)

if '--inject' in sys.argv:
    print(f'轮 {rnd} 缺陷已注入（仅注入模式，未跑校验）')
    sys.exit(0)

r = subprocess.run([PY, B + '/.workbuddy/skills/java-kb-expand/scripts/validate_kb.py'],
                   capture_output=True, text=True, cwd=B)
fails = [l for l in r.stdout.splitlines() if 'FAIL' in l and '[列表]' in l]
print(f'轮 {rnd} 注入后：校验 exit={r.returncode}（预期非 0），命中 [列表] FAIL {len(fails)} 条（预期 1）')
for l in fails:
    print('   ', l)
