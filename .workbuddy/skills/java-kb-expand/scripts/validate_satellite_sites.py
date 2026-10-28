#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三子站基础门禁（非 java-architect-interview KB 计数体系）。

覆盖目录（见 `_site_html.SATELLITE_DIRS`）：
  - java-design-patterns-principles/
  - Software-Engineering-Core-Philosophical-Principles-and-Methodologies/
  - Software-Engineering-Laws-Theories-Principles-and-Patterns/

检查项（轻量，对齐 AGENTS 红线中与子站相关的部分）：
  1. data-page-node-id 必须为 0（预览注入红线）
  2. 禁用词：面试 / 面试官 / 八股
  3. 须有 viewport meta（小屏基线）
  4. 须声明 UTF-8 charset
  5. 若含 Mermaid：每个 <div class="mermaid"> 上一行为 prettier-ignore，且图源未塌缩（换行≥2）
  6. 无 Prettier 拆开的闭合标签 </tag\\n>
  7. 基础样式复用：各站 `assets/style.css` 须 `@import` / 引用仓库根 `assets/satellite-base.css`

用法：
  python3 validate_satellite_sites.py
  python3 validate_satellite_sites.py --only java-design-patterns-principles

退出码：0=全过；1=有 FAIL。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _kbroot import require_root  # noqa: E402
from _site_html import SATELLITE_DIRS, satellite_html_files  # noqa: E402

BASE = Path(require_root(__file__))

FORBIDDEN = ("面试官", "面试", "八股")  # 长词在前，避免重复报点时优先长匹配展示
CLOSER = re.compile(r"</([A-Za-z][\w:-]*)\s*\n\s*>")
VIEWPORT = re.compile(r'<meta[^>]+name=["\']viewport["\']', re.I)
CHARSET = re.compile(r'<meta[^>]+charset\s*=\s*["\']?utf-8', re.I)
MERMAID_OPEN = re.compile(r'^\s*<div class="mermaid">')


def check_file(path: Path, rel: str) -> list[str]:
    fails: list[str] = []
    raw = path.read_text(encoding="utf-8")

    n_dpni = raw.count("data-page-node-id")
    if n_dpni:
        fails.append(f"[红线] {rel}: data-page-node-id={n_dpni}（须 0）")

    # 先遮蔽较长禁用词，再计较短词，避免「面试官」同时触发「面试」双报
    masked = raw
    for w in FORBIDDEN:
        c = masked.count(w)
        if c:
            fails.append(f"[禁用词] {rel}: 含「{w}」×{c}")
            masked = masked.replace(w, "\0" * len(w))

    if not VIEWPORT.search(raw):
        fails.append(f"[viewport] {rel}: 缺少 meta viewport")

    if not CHARSET.search(raw):
        fails.append(f"[charset] {rel}: 缺少 UTF-8 charset meta")

    if CLOSER.search(raw):
        fails.append(f"[格式] {rel}: 存在拆开的闭合标签 </tag\\n>（先跑 npm run format:html）")

    if 'class="mermaid"' in raw:
        lines = raw.splitlines()
        miss = []
        for i, line in enumerate(lines):
            if MERMAID_OPEN.match(line):
                prev = lines[i - 1] if i else ""
                if "prettier-ignore" not in prev:
                    miss.append(i + 1)
        if miss:
            fails.append(f"[Mermaid] {rel}: 缺 prettier-ignore 于行 {miss[:8]}")
        for inner in re.findall(r'<div class="mermaid">(.*?)</div>', raw, re.S):
            if inner.count("\n") < 2:
                fails.append(f"[Mermaid] {rel}: 图源疑似塌缩（换行 < 2）")
                break

    return fails


def check_shared_base_css(dirs: tuple[str, ...]) -> list[str]:
    """各子站 assets/style.css 必须引用仓库根 assets/satellite-base.css。"""
    fails: list[str] = []
    shared = BASE / "assets" / "satellite-base.css"
    if not shared.is_file():
        fails.append("[样式复用] 缺少仓库根 assets/satellite-base.css")
        return fails
    for d in dirs:
        style = BASE / d / "assets" / "style.css"
        if not style.is_file():
            fails.append(f"[样式复用] {d}/assets/style.css 缺失")
            continue
        css = style.read_text(encoding="utf-8")
        if "satellite-base.css" not in css:
            fails.append(f"[样式复用] {d}/assets/style.css 须 @import / 引用 satellite-base.css")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--only",
        metavar="DIR",
        help="只检查某一个子站目录名（须为 SATELLITE_DIRS 之一）",
    )
    args = ap.parse_args()
    if args.only and args.only not in SATELLITE_DIRS:
        print(f"FAIL --only 须为以下之一：{', '.join(SATELLITE_DIRS)}")
        return 2

    files = satellite_html_files(BASE)
    if args.only:
        prefix = args.only + "/"
        files = [p for p in files if str(p.relative_to(BASE)).startswith(prefix)
                 or p.relative_to(BASE).parts[0] == args.only]

    if not files:
        print("FAIL 未找到任何子站 HTML（目录是否改名？）")
        return 1

    all_fails: list[str] = []
    dirs = (args.only,) if args.only else SATELLITE_DIRS
    all_fails.extend(check_shared_base_css(dirs))
    for p in files:
        rel = str(p.relative_to(BASE))
        all_fails.extend(check_file(p, rel))

    if all_fails:
        print(f"FAIL satellite sites：{len(all_fails)} 项（扫描 {len(files)} HTML）")
        for f in all_fails[:40]:
            print(" ", f)
        if len(all_fails) > 40:
            print(f"  … +{len(all_fails) - 40} more")
        return 1

    by_dir = {d: 0 for d in SATELLITE_DIRS}
    for p in files:
        top = p.relative_to(BASE).parts[0]
        if top in by_dir:
            by_dir[top] += 1
    detail = ", ".join(f"{k}={v}" for k, v in by_dir.items() if v)
    print(f"ALL PASS ✅ 三子站基础门禁（{len(files)} HTML：{detail}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
