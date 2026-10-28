#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""站点用户可见 HTML 清单（格式化 / Mermaid ignore / 子站门禁共用）。

范围（相对项目根）：
  - 根：`index.html`、`interview.html`
  - 章节主站：`java-architect-interview/*.html`（仅顶层，不含 shared/tmp）
  - 三子站（递归 `**/*.html`，跳过 tmp/node_modules）：
      java-design-patterns-principles/
      Software-Engineering-Core-Philosophical-Principles-and-Methodologies/
      Software-Engineering-Laws-Theories-Principles-and-Patterns/

勿在此写死家目录绝对路径；项目根一律 `find_root`。
"""
from __future__ import annotations

import os
from pathlib import Path

from _kbroot import require_root

# 子站目录名（相对根；与磁盘目录一一对应）
SATELLITE_DIRS = (
    "java-design-patterns-principles",
    "Software-Engineering-Core-Philosophical-Principles-and-Methodologies",
    "Software-Engineering-Laws-Theories-Principles-and-Patterns",
)

CHAPTER_DIR = "java-architect-interview"
ROOT_HTML = ("index.html", "interview.html")

_SKIP_PARTS = {"tmp", "node_modules", ".git", "shared"}


def _skip(path: Path) -> bool:
    return any(p in _SKIP_PARTS for p in path.parts)


def site_html_files(base: str | Path | None = None) -> list[Path]:
    """全站用户可见 HTML（格式化 / 稳态检查 / Mermaid ignore）。"""
    root = Path(base or require_root(__file__))
    files: list[Path] = []
    for name in ROOT_HTML:
        p = root / name
        if p.is_file():
            files.append(p)
    chap = root / CHAPTER_DIR
    if chap.is_dir():
        files += sorted(p for p in chap.glob("*.html") if p.is_file())
    for rel in SATELLITE_DIRS:
        d = root / rel
        if not d.is_dir():
            continue
        files += sorted(
            p for p in d.rglob("*.html") if p.is_file() and not _skip(p.relative_to(root))
        )
    # 去重保序
    seen: set[Path] = set()
    out: list[Path] = []
    for p in files:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return out


def satellite_html_files(base: str | Path | None = None) -> list[Path]:
    """仅三子站 HTML（基础门禁范围）。"""
    root = Path(base or require_root(__file__))
    files: list[Path] = []
    for rel in SATELLITE_DIRS:
        d = root / rel
        if not d.is_dir():
            continue
        files += sorted(
            p for p in d.rglob("*.html") if p.is_file() and not _skip(p.relative_to(root))
        )
    return files


def prettier_globs() -> list[str]:
    """供 npm/prettier CLI 使用的 glob（相对项目根，含引号时由 shell 展开）。"""
    globs = list(ROOT_HTML) + [f"{CHAPTER_DIR}/*.html"]
    for rel in SATELLITE_DIRS:
        globs.append(f"{rel}/**/*.html")
    return globs


if __name__ == "__main__":
    root = require_root(__file__)
    fs = site_html_files(root)
    print(f"root={root}")
    print(f"site_html={len(fs)}")
    for p in fs:
        print(" ", os.path.relpath(p, root))
