#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_mind_mermaid.py — 导图站一致性校验（map-card ↔ Mermaid 节点）

背景（2026-09-15 实测漏改）：
  新增卡同步导图时，容易只补 <summary> 主题卡而漏掉 <div class="mermaid"> 内的图节点，
  导致「导图卡片有、图上没有」。validate_kb.py 只校验 mind `<summary>` 的 ID 集合
  与章节页 qa-card id 对齐，查不出图节点缺失 —— 本脚本补这个盲区。

不变式：
  同一 mind 页内，每一条 map-card（含 `C12.11~15 …` 这类聚合条目）
  都应在 Mermaid 图中有对应节点（4-gram 文本重合即为命中）。

用法：
  python3 scripts/check_mind_mermaid.py          # 有缺失 → exit 1
  python3 scripts/check_mind_mermaid.py -v       # 打印每页统计
"""
import re
import sys
import os
import glob

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
MI = os.path.join(BASE, 'java-architect-interview-mind')

# 已知误报白名单：map-card 标题 与 图节点文案刻意不同义（形近但人工确认一致）
ALLOW = {
    ('mind-14-databases.html', 'C14.12'),
}


def norm(s):
    return re.sub(r'[\s·、，,：:；;（）()「」【】\[\]/／\-—～~"\'"'']+', '', s)


def grams(s, n=4):
    return {s[i:i + n] for i in range(len(s) - n + 1)} if len(s) >= n else {s}


def mermaid_text(t):
    out = []
    for m in re.finditer(r'<div class="mermaid">', t):
        i = t.index('>', m.start()) + 1
        j = t.find('</div>', i)
        out.append(t[i:j])
    return '\n'.join(out)


def main():
    verbose = '-v' in sys.argv
    total = fails = 0
    for p in sorted(glob.glob(os.path.join(MI, 'mind-*.html'))):
        fn = os.path.basename(p)
        t = open(p, encoding='utf-8').read()
        mer = mermaid_text(t)
        if not mer.strip():
            continue
        labels = [norm(x) for x in re.findall(r'\["([^"]*)"\]', mer)]
        blob = '|'.join(labels)
        bad = []
        n = 0
        for m in re.finditer(r'<summary>\s*([CESGKM]\d{2}\.\d{2})\s*([^<]*)<', t):
            cid, title = m.group(1), norm(m.group(2))
            if not title:
                continue
            n += 1
            total += 1
            if (fn, cid) in ALLOW:
                continue
            if not any(g in blob for g in grams(title, 4)):
                bad.append((cid, m.group(2).strip()[:38]))
        if bad:
            fails += len(bad)
            print(f'[FAIL] {fn}')
            for cid, tt in bad:
                print(f'        {cid}  「{tt}」在 Mermaid 中无对应节点')
        elif verbose:
            print(f'[PASS] {fn}   map-card {n} / 图节点 {len(labels)}')
    print()
    if fails:
        print(f'check_mind_mermaid 结果：{fails} 条 map-card 在 Mermaid 中缺节点 ❌')
        sys.exit(1)
    print(f'check_mind_mermaid 结果：{total} 条 map-card 均有对应图节点 ✅')


main()
