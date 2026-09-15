#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向验证 1g 横向溢出兜底门禁：临时注入缺陷 -> 跑校验 -> 必须 FAIL -> 自动还原"""
import os, re, shutil, subprocess, sys, hashlib

B = '/Users/chenjunbing/Develop/Project/Personal/Java Spring AI'
PY = '/Users/chenjunbing/.workbuddy/binaries/python/versions/3.13.12/bin/python3'
CSS = B + '/java-architect-interview/assets/design-system.css'
PAGE = B + '/java-architect-interview/nav-server-security-checkpoint.html'
KEEP = B + '/tmp/probe_keep'


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


os.makedirs(KEEP, exist_ok=True)
shutil.copy(CSS, KEEP + '/design-system.css')
shutil.copy(PAGE, KEEP + '/page.html')
css_md5, page_md5 = md5(CSS), md5(PAGE)

try:
    # 缺陷 1：摘掉全局换行兜底
    t = open(CSS, encoding='utf-8').read()
    assert '  overflow-wrap: anywhere;' in t
    t2 = t.replace('  overflow-wrap: anywhere;', '  /* probe-removed */', 1)
    assert t2 != t
    open(CSS, 'w', encoding='utf-8').write(t2)

    # 缺陷 2：把 19 处已包裹的 pre 还原成裸挂
    shutil.copy(B + '/tmp/bare_pre_backup/nav-server-security-checkpoint.html', PAGE)

    r = subprocess.run([PY, B + '/.workbuddy/skills/java-kb-expand/scripts/validate_kb.py'],
                       capture_output=True, text=True, cwd=B)
    fails = [l for l in r.stdout.splitlines() if 'FAIL' in l and '溢出' in l]
    print('=== 注入缺陷后的校验输出 ===')
    for l in fails:
        print('  ', l)
    print(f'\n命中溢出类 FAIL: {len(fails)} 条（预期 2 条：CSS 兜底 + 裸 pre）')
    print('校验总退出码:', r.returncode, '(非 0 = 已拦住)')
finally:
    shutil.copy(KEEP + '/design-system.css', CSS)
    shutil.copy(KEEP + '/page.html', PAGE)
    ok_css = md5(CSS) == css_md5
    ok_page = md5(PAGE) == page_md5
    print(f'\n=== 还原校验 ===\ndesign-system.css MD5 一致: {ok_css}\ncheckpoint 页 MD5 一致: {ok_page}')
    print('还原状态:', 'OK' if (ok_css and ok_page) else '!! 还原失败')
