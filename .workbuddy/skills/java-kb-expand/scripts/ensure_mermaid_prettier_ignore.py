#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为站点 HTML 中每个 <div class="mermaid"> 补上一行 <!-- prettier-ignore -->。

用法（仓库根）:
  python3 .workbuddy/skills/java-kb-expand/scripts/ensure_mermaid_prettier_ignore.py
  python3 .workbuddy/skills/java-kb-expand/scripts/ensure_mermaid_prettier_ignore.py --check

随后建议: npm run format:html && python3 …/validate_kb.py
规范: docs/format-shared.md §10
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve()
for _ in range(8):
    if (BASE / "java-architect-interview").is_dir() and (BASE / "index.html").is_file():
        break
    BASE = BASE.parent
else:
    raise SystemExit("cannot locate repo root (need index.html + java-architect-interview/)")

MERMAID_OPEN = re.compile(r"^([ \t]*)<div class=\"mermaid\">")


def site_html_files() -> list[Path]:
    files = [BASE / "index.html"]
    files += sorted((BASE / "java-architect-interview").glob("*.html"))
    files += sorted((BASE / "java-architect-interview-mind").glob("*.html"))
    return [p for p in files if p.is_file()]


def ensure_file(path: Path, check_only: bool) -> tuple[int, int]:
    """Returns (mermaid_count, added_or_missing)."""
    text = path.read_text(encoding="utf-8")
    if 'class="mermaid"' not in text:
        return 0, 0
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    added = 0
    mermaid_n = 0
    for i, line in enumerate(lines):
        m = MERMAID_OPEN.match(line)
        if m:
            mermaid_n += 1
            prev = out[-1] if out else ""
            if "prettier-ignore" not in prev:
                if check_only:
                    added += 1
                else:
                    out.append(f'{m.group(1)}<!-- prettier-ignore -->\n')
                    added += 1
            out.append(line)
            continue
        out.append(line)
    if not check_only and added:
        path.write_text("".join(out), encoding="utf-8")
    return mermaid_n, added


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="只检查，不写文件（缺 ignore 时 exit 1）")
    args = ap.parse_args()
    total_m = total_a = 0
    touched = []
    for p in site_html_files():
        n, a = ensure_file(p, args.check)
        total_m += n
        total_a += a
        if a:
            touched.append(f"{p.relative_to(BASE)} (+{a})" if not args.check else f"{p.relative_to(BASE)} missing={a}")
    mode = "check" if args.check else "write"
    print(f"[{mode}] mermaid={total_m} {'missing' if args.check else 'added'}={total_a}")
    for t in touched[:20]:
        print(" ", t)
    if args.check and total_a:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
