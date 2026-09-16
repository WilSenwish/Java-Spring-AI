#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
strip_page_node_id.py — 清除 HTML 中意外注入的 data-page-node-id 属性（红线恢复工具）
=================================================================================
预览服务可能在打开 HTML 时回写注入 `data-page-node-id="..."`，污染全站（历史上单文件被注入 6517 处）。
本脚本按 java-kb-expand 知识库既定的三步归一法清除，把污染计数恢复到 0。

用法：
    python3 strip_page_node_id.py --check [路径...]   # 只统计每文件 data-page-node-id 计数，不改写
    python3 strip_page_node_id.py --fix   [路径...]   # 对计数>0 的文件执行三步归一并回写

路径缺省：扫描站点全部目标 HTML（根 index.html + java-architect-interview/*.html + java-architect-interview-mind/*.html）
基准目录：脚本所在仓库向上三级（scripts -> java-kb-expand -> .workbuddy -> 项目根）。非标准位置运行时显式传路径。

三步归一（仅动 `<...>` 标签内、不动文本节点，保护 <pre> 缩进）：
    1) 删除属性：           re.sub(r'\s*data-page-node-id="[^"]*"', '', t)
    2) 标签内空白归一：     re.sub(r'<[^>]+>', lambda m: re.sub(r'\s{2,}',' ',m.group(0)), t)
    3) 属性与 > 间去空格：  re.sub(r'(\s*=\s*"[^"]*")(\s+>)', r'\1>', t)
"""
import re, sys, os, glob

# scripts/.workbuddy/skills/java-kb-expand -> 项目根
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def target_files(paths):
    if paths:
        return paths
    files = [os.path.join(BASE, "index.html")]
    files += glob.glob(os.path.join(BASE, "java-architect-interview", "*.html"))
    files += glob.glob(os.path.join(BASE, "java-architect-interview-mind", "*.html"))
    return [f for f in files if os.path.isfile(f)]


def strip_three(t):
    t = re.sub(r'\s*data-page-node-id="[^"]*"', '', t)
    t = re.sub(r'<[^>]+>', lambda m: re.sub(r'\s{2,}', ' ', m.group(0)), t)
    t = re.sub(r'(\s*=\s*"[^"]*")(\s+>)', r'\1>', t)
    return t


def main():
    mode = "--fix" if "--fix" in sys.argv else "--check"
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = target_files(paths)
    total = 0
    changed = 0
    for f in files:
        with open(f, encoding="utf-8") as fh:
            t = fh.read()
        c = t.count("data-page-node-id")
        total += c
        if c and mode == "--fix":
            new = strip_three(t)
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(new)
            changed += 1
            print(f"[FIX]   {f}: 清除 {c} 处 -> 0")
        elif c:
            print(f"[CHECK] {f}: data-page-node-id={c}（需 --fix 清除）")
    tag = "已修复 " + str(changed) + " 个文件" if mode == "--fix" else "未改写（--check）"
    print(f"\n合计 data-page-node-id={total}；{tag}")
    sys.exit(1 if (total and mode == "--check") else 0)


if __name__ == "__main__":
    main()
