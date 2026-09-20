#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_mind_mermaid.py — 导图站一致性校验（map-card ↔ Mermaid 节点）

背景（2026-09-15 实测漏改）：
  新增卡同步导图时，容易只补 <summary> 主题卡而漏掉 <div class="mermaid"> 内的图节点，
  导致「导图卡片有、图上没有」。validate_kb.py 只校验 mind `<summary>` 的 ID 集合
  与章节页 qa-card id 对齐，查不出图节点缺失 —— 本脚本补这个盲区。

  （2026-09-20 修正）原实现只取 `["…"]` 方括号标签，而 Mermaid `mindmap` 用**裸文本**
  声明节点 → 方括号标签数为 0。凡「flowchart 走组级概览、mindmap 走逐卡」的页
  （如 mind-core-methodology.html：flowchart 17 个组级节点 vs 127 张 map-card）
  会被整页误判缺失（实测 126 条常红）。现改为**逐 mermaid 块分别取标签**：
  方括号标签 + mindmap 裸文本行（含 `root((…))` 内文案）。

不变式：
  同一 mind 页内，每一条 map-card（含 `C12.11~15 …` 这类聚合条目）
  都应在**任一** mermaid 块中有对应节点：
  flowchart 的 `["…"]` 标签 或 mindmap 的裸文本行，4-gram 文本重合即为命中。

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
# 注：2026-09-20 起图节点文案已含 mindmap 裸文本行，本条目仍**刻意保留** —— 它记录的是
#     「标题与节点文案本就不等价」这一人工裁定，不随解析范围扩大而失效。
ALLOW = {
    ('mind-14-databases.html', 'C14.12'),
}


def norm(s):
    return re.sub(r'[\s·、，,：:；;（）()「」【】\[\]/／\-—～~"\'"'']+', '', s)


def grams(s, n=4):
    return {s[i:i + n] for i in range(len(s) - n + 1)} if len(s) >= n else {s}


def mermaid_blocks(t):
    out = []
    for m in re.finditer(r'<div class="mermaid">', t):
        i = t.index('>', m.start()) + 1
        j = t.find('</div>', i)
        out.append(t[i:j])
    return out


def block_labels(b):
    """单个 mermaid 块的图节点文案：flowchart 的 ["…"] 标签 + mindmap 的裸文本行"""
    labels = re.findall(r'\["([^"]*)"\]', b)
    if b.strip().startswith('mindmap'):
        for ln in b.strip().splitlines()[1:]:
            s = ln.strip()
            if not s:
                continue
            m = re.fullmatch(r'[\w$]+\(\((.*)\)\)', s)
            labels.append(m.group(1) if m else s)
    return labels


def main():
    verbose = '-v' in sys.argv
    total = fails = 0
    for p in sorted(glob.glob(os.path.join(MI, 'mind-*.html'))):
        fn = os.path.basename(p)
        t = open(p, encoding='utf-8').read()
        blocks = mermaid_blocks(t)
        if not any(b.strip() for b in blocks):
            continue
        labels = [norm(x) for b in blocks for x in block_labels(b)]
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
            print(f'[PASS] {fn}   map-card {n} / 图节点文案 {len(labels)}')
    print()
    if fails:
        print(f'check_mind_mermaid 结果：{fails} 条 map-card 在 Mermaid 中缺节点 ❌')
        sys.exit(1)
    print(f'check_mind_mermaid 结果：{total} 条 map-card 均有对应图节点 ✅')


main()
