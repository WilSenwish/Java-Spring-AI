#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_index_badges.py — 聚合页（根 index / overview）徽标结构与缩进一致性检查（防复发）
=========================================================================================
背景（2026-09-16 实测事故）：新增题由外部插入 index.html 时出现两类缺陷——
  1) overview：`.ov-item` 的 difficulty/priority 未用 `.ov-badges` 包裹 → 间距取容器
     `--space-sm`，与其余 4px 不一致（视觉"样式不统一"）。实测 15 条。
  2) 根 index：`<a>` 行顶格（缺缩进）且 `q-tags` 未闭合、priority 缺失（源页有 p1 时漏渲染）。
     实测 7 条（其中 5 条 C/S 卡漏 priority，2 条 G 卡仅缺闭合）。

用法：
  python3 check_index_badges.py [项目根]     # 默认自动向上查找项目根（含 AGENTS.md + index.html 的目录）
退出码：0 = 通过；1 = 存在缺陷；2 = 路径解析失败（可直接用作门禁）。
"""
import re, sys, os


def find_base():
    """向上查找项目根：同时含 AGENTS.md 与 index.html 的最近祖先目录。

    不用固定层级 dirname —— 本技能可能经 `.agents/skills/java-kb-expand`
    软链调用，且脚本目录深度会随重构变化，固定层级会静默指到 `.workbuddy/`。
    """
    d = os.path.dirname(os.path.realpath(__file__))
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "AGENTS.md")) and os.path.isfile(os.path.join(d, "index.html")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


BASE = sys.argv[1] if len(sys.argv) > 1 else find_base()
if not BASE or not os.path.isdir(BASE):
    print("FAIL 无法定位项目根（请显式传入：check_index_badges.py <项目根>）")
    sys.exit(2)
IDX = os.path.join(BASE, "index.html")
OV = os.path.join(BASE, "java-architect-interview/nav-overview-priority.html")
for _p in (IDX, OV):
    if not os.path.isfile(_p):
        print(f"FAIL 目标文件不存在：{_p}")
        sys.exit(2)

problems = []

# 1) overview：每个 ov-item 必须用 .ov-badges 包裹 difficulty+priority
t = open(OV, encoding="utf-8").read()
for m in re.finditer(r'<a class="ov-item"[^>]*>.*?</a>', t, re.S):
    b = m.group(0)
    if 'class="ov-badges"' not in b:
        num = re.search(r'class="ov-num">([^<]+)<', b)
        problems.append(f"[overview] {num.group(1) if num else '?'} 缺 .ov-badges 包裹")

# 2) 根 index：a) <a> 顶格；b) q-tags 标签不平衡（未闭合）
t = open(IDX, encoding="utf-8").read()
for i, ln in enumerate(t.split("\n"), 1):
    if re.match(r'^<a href=', ln):
        problems.append(f"[index] L{i} <a> 顶格（缺缩进）")
    if '<span class="q-tags"' in ln:
        seg = ln[ln.index('<span class="q-tags"'):]
        if seg.count("<span") != seg.count("</span>"):
            qid = re.search(r'class="q-id">([^<]+)<', ln)
            problems.append(f"[index] L{i} q-tags 未闭合（{qid.group(1) if qid else '?'}）")

if problems:
    print(f"FAIL 发现 {len(problems)} 处缺陷：")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("PASS 根 index / overview 徽标结构一致，无顶格行、无未闭合 q-tags。")
