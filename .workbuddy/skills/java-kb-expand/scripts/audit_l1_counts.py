#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""计数保护覆盖门禁（只读，单跑版）。= `validate_kb.run_l1_container_scan`：容器内裸「N+单位词」与
inline 模式（如「M## 名（N）」）未受 data-kb-pos 保护即 FAIL。配置全部读 SSOT `guard.coverage`
（scan / containers / units / inline / exempt），脚本内不写死容器名与编码。口径见 conventions §5.1.4。"""
import os, re, sys
BASE = "/Users/chenjunbing/Develop/Project/Personal/Java Spring AI"
CHAPTER_DIR = f"{BASE}/java-architect-interview"
MIND_DIR = f"{BASE}/java-architect-interview-mind"

# Import check by reusing validate module path
sys.path.insert(0, os.path.dirname(__file__))
import validate_kb as v

v.check.failed = 0
v.run_l1_container_scan()
sys.exit(1 if v.check.failed else 0)
