#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_catppuccin · 配色单一色源门禁

检查（细则见 docs/specs/format-colors.md §7）：
  1. hex 全量扫描：站点自有文件中「颜色上下文」出现的每个 hex，
     必须 ∈ palette ∪ derived ∪ exempt（SSOT：docs/catppuccin-tokens.json）。
  2. RETINT 覆盖：HTML 内联图表 colon 形 fill:/stroke: hex，
     必须被 theme-init.js 的 RETINT_FILL_DARK ∪ RETINT_STROKE_DARK 键集覆盖。

约定：
  - 配置全部数据化于 docs/catppuccin-tokens.json（脚本不写死色值/路径/文件清单）；
  - 项目根定位统一走 _kbroot.find_root（禁写死绝对路径）；
  - FAIL 全部点名（file:line），不截断；发现即 exit 1。
"""
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_SCRIPTS = os.path.normpath(os.path.join(
    _HERE, "..", "..", ".workbuddy", "skills", "java-kb-expand", "scripts"))
sys.path.insert(0, _SKILL_SCRIPTS)
from _kbroot import find_root  # noqa: E402

BASE = find_root(__file__)
if not BASE:
    raise SystemExit("定位失败：未找到项目根（AGENTS.md + docs/kb-counts.json）")

SSOT = os.path.join(BASE, "docs", "catppuccin-tokens.json")
CFG = json.load(open(SSOT, encoding="utf-8"))

# ---------- 色源集合 ----------
def _norm6(h):
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return h[:6]

ALLOWED = {_norm6(v) for _f in CFG["flavors"].values() for v in _f.values()}
ALLOWED |= {_norm6(d["hex"]) for _k, _g in CFG["derived"].items()
            if not _k.startswith("_") for d in _g}
ALLOWED |= {_norm6(e["hex"]) for e in CFG["exempt"]}

SCAN = CFG["scan"]
EXCLUDE_DIRS = set(SCAN["exclude_dirs"])
EXCLUDE_GLOBS = list(SCAN.get("exclude_globs", []))
INCLUDE_EXT = set(SCAN["include_ext"])

# ---------- 文件收集 ----------
import fnmatch  # noqa: E402

def _dir_excluded(rel_posix):
    """rel_posix：相对根的目录路径（/ 分隔）。逐级前缀或任一段名命中即排除。"""
    parts = rel_posix.split("/")
    for i in range(1, len(parts) + 1):
        if "/".join(parts[:i]) in EXCLUDE_DIRS or parts[i - 1] in EXCLUDE_DIRS:
            return True
    return False

def collect_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(BASE):
        rel = os.path.relpath(dirpath, BASE).replace(os.sep, "/")
        if rel != "." and _dir_excluded(rel):
            dirnames[:] = []
            continue
        for name in filenames:
            if os.path.splitext(name)[1] not in INCLUDE_EXT:
                continue
            if any(fnmatch.fnmatch(name, g) for g in EXCLUDE_GLOBS):
                continue
            out.append(os.path.join(dirpath, name))
    return sorted(out)

# ---------- 颜色上下文正则 ----------
# CSS 声明值内的 hex（覆盖 --var 定义 / color-mix / gradient / var(,兜底) / 注释示例）
DECL = re.compile(r'(?:[-a-zA-Z]+\s*:\s*[^;{}<>]*?)#([0-9a-fA-F]{3,8})\b')
# HTML style 属性内容
STYLE_ATTR = re.compile(r'style\s*=\s*"([^"]*)"')
# SVG 属性形 fill="…"/stroke="…"
ATTR_HEX = re.compile(r'\b(fill|stroke)\s*=\s*"(#[0-9a-fA-F]{3,8})"')
# HTML/SVG/JS 内联图表 colon 形（RETINT 覆盖域）
COLON = re.compile(r'\b(fill|stroke)\s*:\s*#([0-9a-fA-F]{3,8})\b')
# JS 字符串字面量内以 # 开头的 hex
JS_LIT = re.compile(r'([\'"])#([0-9a-fA-F]{3,8})\b')
# HTML 内非颜色上下文（锚点/资源引用），先剔除再扫
HTML_STRIP = re.compile(
    r'\b(?:href|src|id|data-[a-z-]+|url)\s*=\s*("[^"]*"|\'[^\']*\')')

def scan_css(text):
    """返回 [(line_no, hex)] —— 声明值上下文。"""
    return _hits(DECL, text, group=1)

def _hits(pat, text, group):
    out = []
    line_starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            line_starts.append(i + 1)
    import bisect
    for m in pat.finditer(text):
        ln = bisect.bisect_right(line_starts, m.start())
        out.append((ln, m.group(group)))
    return out

def scan_html(text):
    hits = []
    stripped = HTML_STRIP.sub(lambda m: " " * len(m.group(0)), text)
    hits += _hits(DECL, stripped, 1)
    hits += _hits(ATTR_HEX, text, 2)
    return hits

def scan_js(text):
    hits = _hits(JS_LIT, text, 2)
    hits += _hits(DECL, text, 1)   # 注释里的 fill:#x / --var:#x 示例同样受管
    return hits

SCANNERS = {".css": scan_css, ".html": scan_html, ".js": scan_js}

# ---------- RETINT 键集 ----------
def retint_keys():
    p = os.path.join(BASE, "core", "assets", "theme-init.js")
    js = open(p, encoding="utf-8").read()
    keys = set()
    for name in ("RETINT_FILL_DARK", "RETINT_STROKE_DARK"):
        i = js.index("var " + name + " = {")
        j = js.index("{", i)
        depth, k = 0, j
        while k < len(js):
            if js[k] == "{":
                depth += 1
            elif js[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        keys |= {_norm6(m) for m in re.findall(r"'(#[0-9a-fA-F]{3,8})'\s*:", js[j:k + 1])}
    return keys

def main():
    files = collect_files()
    fails, retint_fails = [], []
    rkeys = retint_keys()

    for fp in files:
        rel = os.path.relpath(fp, BASE)
        ext = os.path.splitext(fp)[1]
        try:
            text = open(fp, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError) as e:
            fails.append("%s: 读取失败 %s" % (rel, e))
            continue
        for ln, raw in SCANNERS[ext](text):
            h = _norm6(raw)
            if h not in ALLOWED:
                fails.append("%s:%d  #%s  [非 Catppuccin 色源（palette/derived/exempt 均未登记）]"
                             % (rel, ln, raw.lower()))
        if ext == ".html":
            for ln, m in _hits(COLON, text, 2):
                if _norm6(m) not in rkeys:
                    retint_fails.append(
                        "%s:%d  #%s  [内联图表色未登记 RETINT（暗黑下不可读）]"
                        % (rel, ln, m.lower()))

    print("== audit_catppuccin ==")
    print("SSOT     : %s" % os.path.relpath(SSOT, BASE))
    print("扫描文件 : %d" % len(files))
    print("色源集合 : palette %d + derived %d + exempt %d = %d"
          % (len(ALLOWED) - sum(len(v) for k, v in CFG["derived"].items()
                                if not k.startswith("_")) - len(CFG["exempt"]),
             sum(len(v) for k, v in CFG["derived"].items() if not k.startswith("_")),
             len(CFG["exempt"]), len(ALLOWED)))
    if fails:
        print("\nFAIL hex 色源（%d 处）:" % len(fails))
        for f in fails:
            print("  " + f)
    if retint_fails:
        print("\nFAIL RETINT 覆盖（%d 处）:" % len(retint_fails))
        for f in retint_fails:
            print("  " + f)
    if not fails and not retint_fails:
        print("\nALL PASS")
        return 0
    print("\nGATE FAIL")
    return 1

if __name__ == "__main__":
    sys.exit(main())
