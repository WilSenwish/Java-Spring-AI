#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L1 聚合 UI 裸计数审计（只读）。口径同 validate_kb.run_l1_container_scan / conventions §5.1.4。"""
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
