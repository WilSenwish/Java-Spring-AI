#!/usr/bin/env python3
"""Restore mermaid diagram newlines collapsed by HTML formatter.

Strategy: for each HTML file with mermaid blocks, extract the pre-formatting
version from git (commit 85a7bcd), match mermaid blocks by normalized content,
and replace collapsed single-line blocks with the original multi-line format.
"""

import re
import subprocess
import os
import sys

BASE_DIR = '/Users/chenjunbing/Develop/Project/Personal/Java Spring AI'
OLD_COMMIT = '85a7bcd'
MERMAID_PATTERN = re.compile(r'<div class="mermaid">(.*?)</div>', re.DOTALL)


def normalize_mermaid(content):
    """Normalize mermaid content for matching: strip whitespace, unify br tags."""
    content = content.replace('<br />', '<br/>')
    content = re.sub(r'\s+', '', content)
    return content


def get_indent(content, pos):
    """Get whitespace indentation of the line containing pos."""
    line_start = content.rfind('\n', 0, pos) + 1
    indent = ''
    i = line_start
    while i < pos and content[i] in ' \t':
        indent += content[i]
        i += 1
    return indent


def extract_mermaid_blocks(content):
    """Extract all mermaid blocks from HTML content.
    Returns list of dicts with: match, inner, start, end, indent.
    """
    blocks = []
    for m in MERMAID_PATTERN.finditer(content):
        blocks.append({
            'inner': m.group(1),
            'start': m.start(),
            'end': m.end(),
            'indent': get_indent(content, m.start()),
            'full': m.group(0),
        })
    return blocks


def build_old_lookup(old_content):
    """Build a lookup dict: normalized_content -> original_inner_content."""
    lookup = {}
    blocks = extract_mermaid_blocks(old_content)
    for block in blocks:
        norm = normalize_mermaid(block['inner'])
        if norm not in lookup:
            lookup[norm] = block['inner']
    return lookup


def fix_file(filepath, old_lookup):
    """Fix mermaid blocks in a single file. Returns (num_fixed, num_unmatched)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        current_content = f.read()

    if 'class="mermaid"' not in current_content:
        return 0, 0

    current_blocks = extract_mermaid_blocks(current_content)
    if not current_blocks:
        return 0, 0

    num_fixed = 0
    num_unmatched = 0
    # Replace from end to start to preserve positions
    new_content = current_content
    for block in reversed(current_blocks):
        norm = normalize_mermaid(block['inner'])
        if norm in old_lookup:
            old_inner = old_lookup[norm].strip()
            indent = block['indent']
            replacement = f'<div class="mermaid">\n{old_inner}\n{indent}</div>'
            new_content = (new_content[:block['start']] + replacement +
                           new_content[block['end']:])
            num_fixed += 1
        else:
            num_unmatched += 1
            print(f"  WARNING: No match for mermaid block (normalized: {norm[:80]}...)")

    if num_fixed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return num_fixed, num_unmatched


def find_html_files_with_mermaid():
    """Find all HTML files with mermaid blocks, excluding rk-xigui and docs/facts."""
    files = []
    for root, dirs, filenames in os.walk(BASE_DIR):
        # Skip excluded directories
        rel_root = os.path.relpath(root, BASE_DIR)
        if 'rk-xigui' in rel_root.split(os.sep) or '.git' in dirs:
            continue
        if 'docs/facts' in rel_root or rel_root.startswith('java-architect-interview/docs/facts'):
            continue
        if 'node_modules' in dirs:
            dirs.remove('node_modules')

        for fname in filenames:
            if fname.endswith('.html'):
                filepath = os.path.join(root, fname)
                # Quick check for mermaid
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'class="mermaid"' in content:
                    files.append(filepath)

    return sorted(files)


def main():
    os.chdir(BASE_DIR)

    html_files = find_html_files_with_mermaid()
    print(f"Found {len(html_files)} HTML files with mermaid blocks\n")

    total_fixed = 0
    total_unmatched = 0

    for filepath in html_files:
        rel_path = os.path.relpath(filepath, BASE_DIR)
        print(f"Processing: {rel_path}")

        # Get old version from git
        result = subprocess.run(
            ['git', 'show', f'{OLD_COMMIT}:{rel_path}'],
            capture_output=True, text=True, cwd=BASE_DIR
        )

        if result.returncode != 0:
            print(f"  SKIP: File not in old commit {OLD_COMMIT}")
            continue

        old_content = result.stdout
        if 'class="mermaid"' not in old_content:
            print(f"  SKIP: No mermaid blocks in old version")
            continue

        old_lookup = build_old_lookup(old_content)
        print(f"  Old version has {len(old_lookup)} unique mermaid blocks")

        num_fixed, num_unmatched = fix_file(filepath, old_lookup)
        print(f"  Fixed: {num_fixed}, Unmatched: {num_unmatched}")

        total_fixed += num_fixed
        total_unmatched += num_unmatched

    print(f"\n=== Summary ===")
    print(f"Total files processed: {len(html_files)}")
    print(f"Total blocks fixed: {total_fixed}")
    print(f"Total unmatched: {total_unmatched}")

    if total_unmatched > 0:
        print("\nWARNING: Some mermaid blocks could not be matched to old version.")
        print("These may need manual fixing.")


if __name__ == '__main__':
    main()
