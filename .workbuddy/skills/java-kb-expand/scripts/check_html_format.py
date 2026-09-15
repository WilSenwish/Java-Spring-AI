#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 44 个站点 HTML 是否已处于 format:html 稳态。

稳态 = Prettier(printWidth=10000) + normalize_html_closers 后再写回与原文一致，
且不存在被拆开的闭合标签 </tag\\n>。
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve()
for _ in range(8):
    if (BASE / "java-architect-interview").is_dir() and (BASE / "index.html").is_file():
        break
    BASE = BASE.parent
else:
    raise SystemExit("cannot locate repo root")

CLOSER = re.compile(r"</([A-Za-z][\w:-]*)\s*\n\s*>")
PRETTIER = BASE / "node_modules" / ".bin" / "prettier"


def site_html_files() -> list[Path]:
    files = [BASE / "index.html"]
    files += sorted((BASE / "java-architect-interview").glob("*.html"))
    files += sorted((BASE / "java-architect-interview-mind").glob("*.html"))
    return [p for p in files if p.is_file()]


def normalize(text: str) -> str:
    return CLOSER.sub(lambda m: f"</{m.group(1)}>", text)


def prettier_format(path: Path, text: str) -> str:
    if not PRETTIER.is_file():
        raise SystemExit("prettier not installed; run npm install")
    r = subprocess.run(
        [str(PRETTIER), "--stdin-filepath", str(path.relative_to(BASE))],
        input=text,
        text=True,
        capture_output=True,
        cwd=BASE,
    )
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit(f"prettier failed on {path.name}")
    return r.stdout


def main() -> int:
    bad_split = []
    bad_drift = []
    for p in site_html_files():
        raw = p.read_text(encoding="utf-8")
        if CLOSER.search(raw):
            bad_split.append(str(p.relative_to(BASE)))
            continue
        formatted = normalize(prettier_format(p, raw))
        if formatted != raw:
            bad_drift.append(str(p.relative_to(BASE)))
    if bad_split:
        print("FAIL split closers:", bad_split[:8])
    if bad_drift:
        print("FAIL not at format steady-state:", bad_drift[:8])
    if bad_split or bad_drift:
        print("Run: npm run format:html")
        return 1
    print(f"OK format steady-state ({len(site_html_files())} HTML)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
