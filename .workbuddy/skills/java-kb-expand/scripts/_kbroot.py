#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 项目根定位（全脚本唯一实现）

所有脚本一律 `find_root(__file__)` 取项目根，**禁止写死绝对路径**。
（2026-09-21 长官指令「门禁脚本不能固定写死部分编码等」；此前 9 个脚本里
硬编码了「某个用户的家目录 + 项目名」的绝对路径，换机器 / 换目录 / 换用户即全部失效。）

判据：向上找**同时**含 `AGENTS.md` 与 `docs/kb-counts.json` 的目录。
两者都在才认——避免把 `java-architect-interview/` 等子目录误判为根，
也避免 `tmp/` 里的一次性副本按自身层级乱解析（副本里找不到就会返回 None，
调用方须自行报错退出，不得静默退回 cwd）。

用法：
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from _kbroot import find_root
    BASE = find_root(__file__)
"""
import os

MARKERS = ("AGENTS.md", os.path.join("docs", "kb-counts.json"))


def find_root(start=None):
    """从 start（文件或目录）向上找项目根；找不到返回 None。"""
    d = os.path.abspath(start or os.getcwd())
    if os.path.isfile(d):
        d = os.path.dirname(d)
    while True:
        if all(os.path.isfile(os.path.join(d, m)) for m in MARKERS):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def require_root(start=None):
    """找不到项目根即报错退出（脚本入口用，避免写死路径又怕静默失败）。"""
    r = find_root(start)
    if not r:
        raise SystemExit("定位失败：向上未找到同时含 %s 的目录（见 _kbroot.py）"
                         % " + ".join(MARKERS))
    return r


if __name__ == "__main__":
    import sys
    print(require_root(sys.argv[1] if len(sys.argv) > 1 else __file__))
