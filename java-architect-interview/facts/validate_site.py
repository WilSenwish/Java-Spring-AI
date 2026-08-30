#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-architect-interview 全站交叉校验脚本。
覆盖：标签配平 / 内部锚点一致性 / 跨文件引用 / 全局锚点悬空孤儿 / 量化数字扫描。
"""
import os, re, sys
from html.parser import HTMLParser

ROOT = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI/java-architect-interview"

# ---------- 1. 标签配平 ----------
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
CONTAINER = {"html","head","body","div","span","a","section","p","table","thead","tbody",
             "tfoot","tr","td","th","ul","ol","li","pre","code","blockquote","h1","h2","h3",
             "h4","h5","h6","header","footer","nav","article","aside","main","figure",
             "figcaption","details","summary","button","form","label","select","option",
             "fieldset","legend","dl","dt","dd","script","style","svg","g","text","tspan",
             "mermaid","small","strong","em","i","b","u","sub","sup","caption","colgroup",
             "template","canvas"}

class BalanceChecker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        if tag in CONTAINER:
            self.stack.append((tag, self.getpos()[0]))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in VOID: return
        if tag not in CONTAINER: return
        if not self.stack:
            self.errors.append(f"多余的闭合 </{tag}> @line {self.getpos()[0]}")
            return
        top, ln = self.stack[-1]
        if top == tag:
            self.stack.pop()
        else:
            # 尝试在栈内向后查找匹配
            idx = None
            for i in range(len(self.stack)-1, -1, -1):
                if self.stack[i][0] == tag:
                    idx = i
                    break
            if idx is not None:
                skipped = [t for t,_ in self.stack[idx+1:]]
                self.errors.append(f"标签错配: 期望 </{top}> 却遇到 </{tag}> @line {self.getpos()[0]} (未闭合: {skipped})")
                self.stack = self.stack[:idx]
            else:
                self.errors.append(f"未匹配的闭合 </{tag}> @line {self.getpos()[0]}")

def check_balance(path):
    with open(path, encoding="utf-8") as f:
        data = f.read()
    p = BalanceChecker()
    p.feed(data)
    if p.stack:
        left = [f"<{t}> @line {ln}" for t,ln in p.stack]
        return False, p.errors + [f"文件结束仍有未闭合: {left}"]
    return (len(p.errors)==0), p.errors

# ---------- 2/3/4. 锚点扫描 ----------
ID_RE = re.compile(r'\bid="([^"]+)"')
HREF_RE = re.compile(r'\bhref="([^"]+)"')

def collect(path):
    with open(path, encoding="utf-8") as f:
        data = f.read()
    ids = set(ID_RE.findall(data))
    refs = []
    for m in HREF_RE.finditer(data):
        refs.append(m.group(1))
    return ids, refs

# ---------- 5. 量化数字扫描 ----------
# 匹配百分比 / ms / 毫秒 / QPS / TPS / 吞吐 / 延迟 / 倍 / 万级 / 千万级 等
NUM_PATTERNS = [
    (r'\d+(?:\.\d+)?\s*%', "百分比"),
    (r'\d+(?:\.\d+)?\s*(?:ms|毫秒|微秒|µs|us|ns)', "时延"),
    (r'\d+(?:\.\d+)?\s*(?:QPS|TPS|qps|tps)', "吞吐率"),
    (r'\d+(?:\.\d+)?\s*(?:倍|倍率)', "倍数"),
    (r'(?:千万|百万|亿|万)级', "量级词"),
    (r'\d+\s*-\s*\d+\s*(?:ms|%)', "区间数字"),
    (r'召回率', "召回率"),
    (r'准确率', "准确率"),
]
NUM_RE = [(re.compile(p), label) for p, label in NUM_PATTERNS]

def scan_numbers(path):
    hits = []
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        for rgx, label in NUM_RE:
            for mm in rgx.finditer(line):
                snippet = line.strip()
                if len(snippet) > 160:
                    snippet = snippet[:160] + "..."
                hits.append((i, label, mm.group(0), snippet))
    return hits

# ---------- 主流程 ----------
def main():
    html_files = []
    for dp, dn, fn in os.walk(ROOT):
        if ".bak" in dp:  # 排除备份目录
            continue
        for f in fn:
            if f.endswith(".html"):
                html_files.append(os.path.join(dp, f))
    html_files.sort()

    print("="*70)
    print("【1】标签配平校验")
    print("="*70)
    bal_fail = 0
    for fp in html_files:
        rel = os.path.relpath(fp, ROOT)
        ok, errs = check_balance(fp)
        status = "OK" if ok else "FAIL"
        if not ok: bal_fail += 1
        print(f"  [{status}] {rel}")
        for e in errs[:8]:
            print(f"         - {e}")

    print("\n" + "="*70)
    print("【2-4】锚点扫描（内部一致性 + 跨文件引用 + 全局悬空/孤儿）")
    print("="*70)
    all_ids = {}      # id -> set(file)
    internal_refs = {}  # file -> [ref]
    cross_refs = []     # (src_file, tgt_file, anchor)
    file_ids = {}
    for fp in html_files:
        ids, refs = collect(fp)
        file_ids[fp] = ids
        for i in ids:
            all_ids.setdefault(i, set()).add(fp)
        internal_refs[fp] = []
        for r in refs:
            if r.startswith("#"):
                internal_refs[fp].append((r[1:], "internal"))
            elif "#" in r:
                tf, anc = r.split("#", 1)
                if tf.endswith(".html"):
                    cross_refs.append((fp, tf, anc))
            # 纯文件名无锚点 或 外部 http 跳过

    # 内部 dangling
    dangling_internal = []
    for fp, refs in internal_refs.items():
        for anc, _ in refs:
            if anc and anc not in file_ids[fp]:
                dangling_internal.append((fp, anc))
    # 跨文件 dangling
    dangling_cross = []
    for src, tf, anc in cross_refs:
        tgt = os.path.join(os.path.dirname(src), tf)
        if not os.path.exists(tgt):
            dangling_cross.append((src, tf, anc, "文件不存在"))
        else:
            tids = file_ids.get(tgt, set())
            if anc not in tids:
                dangling_cross.append((src, tf, anc, "锚点不存在"))
    # 孤儿 id（从未被任何 href 引用）
    referenced = set()
    for fp, refs in internal_refs.items():
        for anc, _ in refs:
            referenced.add(anc)
    for src, tf, anc in cross_refs:
        referenced.add(anc)
    # 仅统计章节卡锚点 Cxx.yy / Exx.yy / Sxx.yy / Mxx 形式，避免噪声
    orphan_cards = []
    for i in all_ids:
        if re.match(r'^[CMES]\d{2}\.\d{2}$', i) or re.match(r'^M\d+$', i):
            if i not in referenced:
                orphan_cards.append(i)

    print(f"  内部悬空锚点: {len(dangling_internal)}")
    for fp, anc in dangling_internal:
        print(f"    - {os.path.relpath(fp,ROOT)} : #{anc}")
    print(f"  跨文件悬空引用: {len(dangling_cross)}")
    for src, tf, anc, why in dangling_cross:
        print(f"    - {os.path.relpath(src,ROOT)} -> {tf}#{anc} ({why})")
    print(f"  孤儿卡片锚点(未被任何链接引用): {len(orphan_cards)}")
    for i in sorted(orphan_cards):
        files = [os.path.relpath(x,ROOT) for x in all_ids[i]]
        print(f"    - #{i} 定义于 {files}")

    print("\n" + "="*70)
    print("【5】量化数字扫描（供人工核对，非自动判定）")
    print("="*70)
    total_hits = 0
    for fp in html_files:
        hits = scan_numbers(fp)
        if hits:
            total_hits += len(hits)
            rel = os.path.relpath(fp, ROOT)
            print(f"  {rel}: {len(hits)} 处")
            for ln, label, val, snip in hits[:4]:
                print(f"    L{ln} [{label}] {val}  :: {snip[:90]}")
            if len(hits) > 4:
                print(f"    ... 其余 {len(hits)-4} 处省略")
    print(f"  量化数字命中合计: {total_hits}")

    print("\n" + "="*70)
    print("汇总")
    print("="*70)
    print(f"  文件数(排除.bak): {len(html_files)}")
    print(f"  标签配平失败: {bal_fail}")
    print(f"  内部悬空锚点: {len(dangling_internal)}")
    print(f"  跨文件悬空引用: {len(dangling_cross)}")
    print(f"  孤儿卡片锚点: {len(orphan_cards)}")
    print(f"  量化数字命中: {total_hits}")

if __name__ == "__main__":
    main()
