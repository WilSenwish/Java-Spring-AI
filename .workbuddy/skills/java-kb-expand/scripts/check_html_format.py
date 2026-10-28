#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查站点 HTML 是否已处于 format:html 稳态。

稳态 = Prettier(printWidth=10000) + normalize_html_closers 后再写回与原文一致，
且不存在被拆开的闭合标签 </tag\\n>。

范围见 `_site_html.site_html_files`（根 2 + 章节站 + 三子站）。
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _kbroot import require_root  # noqa: E402
from _site_html import site_html_files  # noqa: E402

BASE = Path(require_root(__file__))

CLOSER = re.compile(r"</([A-Za-z][\w:-]*)\s*\n\s*>")
PRETTIER = BASE / "node_modules" / ".bin" / "prettier"


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
        raise SystemExit(f"prettier failed on {path.relative_to(BASE)}")
    return r.stdout


def main() -> int:
    files = site_html_files(BASE)
    bad_split = []
    bad_drift = []
    for p in files:
        raw = p.read_text(encoding="utf-8")
        rel = str(p.relative_to(BASE))
        if CLOSER.search(raw):
            bad_split.append(rel)
            continue
        formatted = normalize(prettier_format(p, raw))
        if formatted != raw:
            bad_drift.append(rel)
    if bad_split:
        print("FAIL split closers:", bad_split[:12])
    if bad_drift:
        print("FAIL not at format steady-state:", bad_drift[:12])
    if bad_split or bad_drift:
        print("Run: npm run format:html")
        return 1
    print(f"OK format steady-state ({len(files)} HTML)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
