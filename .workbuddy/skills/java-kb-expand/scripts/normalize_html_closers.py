#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prettier 偶发把闭合标签拆成 </tag\\n>；本脚本压回 </tag>。

在 `npm run format:html` 之后运行，保证 kb-count / validate_kb 的
`>(\\d+)</span>` 等锚点仍可命中。见 format-shared.md §10。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve()
for _ in range(8):
    if (BASE / "java-architect-interview").is_dir() and (BASE / "index.html").is_file():
        break
    BASE = BASE.parent
else:
    raise SystemExit("cannot locate repo root")

# </span\n          >  → </span>
CLOSER = re.compile(r"</([A-Za-z][\w:-]*)\s*\n\s*>")


def site_html_files() -> list[Path]:
    files = [BASE / "index.html"]
    files += sorted((BASE / "java-architect-interview").glob("*.html"))
    files += sorted((BASE / "java-architect-interview-mind").glob("*.html"))
    return [p for p in files if p.is_file()]


def normalize(text: str) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        return f"</{m.group(1)}>"

    return CLOSER.sub(repl, text), n


def main() -> int:
    total = 0
    touched = 0
    for p in site_html_files():
        raw = p.read_text(encoding="utf-8")
        fixed, n = normalize(raw)
        if n:
            p.write_text(fixed, encoding="utf-8")
            touched += 1
            total += n
    print(f"normalized closers={total} files={touched}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
