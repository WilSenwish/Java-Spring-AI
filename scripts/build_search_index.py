#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build or check the static search index (titles + body text).

Writes <project-root>/search-index.json.
  python3 scripts/build_search_index.py          # write
  python3 scripts/build_search_index.py --check  # compare hash + records, exit 1 on drift

Indexed:
  - interview.html and java-architect-interview/*.html that contain .qa-card
    (chapter index is a link catalog and is skipped)
  - the three satellite sites named in the search plan

Not indexed: repo root index.html, rk/, docs/facts/, other satellites.
"""
import hashlib
import json
import os
import re
import sys
from html.parser import HTMLParser

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(_HERE),
        ".workbuddy",
        "skills",
        "java-kb-expand",
        "scripts",
    ),
)
from _kbroot import require_root  # noqa: E402

SKIP_TAGS = {"script", "style", "svg", "pre", "nav", "noscript"}
SKIP_CLASSES = {"code-block", "mermaid", "mermaid-container", "sidebar-toc", "toolbar"}
TITLE_SKIP_CLASSES = {"difficulty", "priority"}
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

SATELLITES = (
    (
        "java-design-patterns-principles",
        "设计模式",
    ),
    (
        "Software-Engineering-Core-Philosophical-Principles-and-Methodologies",
        "原则",
    ),
    (
        "Software-Engineering-Laws-Theories-Principles-and-Patterns",
        "定律",
    ),
)

_WS = re.compile(r"\s+")


def clean(text):
    return _WS.sub(" ", text or "").strip()


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {"tag": "#root", "attrs": {}, "children": [], "parent": None}
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs, tag in VOID_TAGS)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, True)

    def _start(self, tag, attrs, void):
        node = {
            "tag": tag,
            "attrs": dict(attrs),
            "children": [],
            "parent": self.stack[-1],
        }
        self.stack[-1]["children"].append(node)
        if not void:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if data:
            self.stack[-1]["children"].append(data)


def classes_of(node):
    raw = node["attrs"].get("class") or ""
    return set(raw.split())


def is_skipped(node):
    if not isinstance(node, dict):
        return False
    if node["tag"] in SKIP_TAGS:
        return True
    return bool(classes_of(node) & SKIP_CLASSES)


def under_skip(node):
    cur = node
    while cur is not None:
        if is_skipped(cur):
            return True
        cur = cur.get("parent")
    return False


def text_of(node, extra_skip=None):
    if isinstance(node, str):
        return node
    if is_skipped(node):
        return ""
    if extra_skip and extra_skip(node):
        return ""
    parts = [text_of(child, extra_skip) for child in node["children"]]
    return " ".join(part for part in parts if part)


def find_all(node, pred, out=None):
    if out is None:
        out = []
    if isinstance(node, dict):
        if pred(node):
            out.append(node)
        if not is_skipped(node):
            for child in node["children"]:
                if isinstance(child, dict):
                    find_all(child, pred, out)
    return out


def has_class(node, name):
    return name in classes_of(node)


def nearest_section_id(node):
    cur = node.get("parent")
    while cur is not None:
        if cur["tag"] == "section" and cur["attrs"].get("id"):
            return cur["attrs"]["id"]
        cur = cur.get("parent")
    return ""


def parse_html(raw):
    builder = TreeBuilder()
    builder.feed(raw)
    builder.close()
    return builder.root


def card_records(tree, rel, site):
    cards = find_all(
        tree,
        lambda n: n["tag"] == "div" and has_class(n, "qa-card") and not under_skip(n),
    )
    records = []
    for card in cards:
        questions = find_all(
            card,
            lambda n: has_class(n, "qa-question") or has_class(n, "epq-question"),
        )
        title = ""
        if questions:
            title = clean(
                text_of(
                    questions[0],
                    lambda n: bool(classes_of(n) & TITLE_SKIP_CLASSES),
                )
            )
        body = clean(text_of(card))
        if not title and not body:
            continue
        anchor = card["attrs"].get("id") or ""
        url = rel + (("#" + anchor) if anchor else "")
        records.append(
            {
                "title": title or body[:48],
                "url": url,
                "site": site,
                "text": body,
            }
        )
    return records


def h3_records(tree, rel, site):
    heads = find_all(tree, lambda n: n["tag"] == "h3" and not under_skip(n))
    records = []
    for head in heads:
        title = clean(text_of(head))
        parent = head.get("parent")
        chunks = []
        if parent is not None:
            kids = parent["children"]
            try:
                idx = kids.index(head)
            except ValueError:
                idx = -1
            if idx >= 0:
                for sib in kids[idx + 1 :]:
                    if isinstance(sib, dict) and sib["tag"] == "h3":
                        break
                    chunks.append(text_of(sib))
        body = clean("".join(chunks))
        if not title and not body:
            continue
        anchor = nearest_section_id(head) or head["attrs"].get("id") or ""
        url = rel + (("#" + anchor) if anchor else "")
        records.append(
            {
                "title": title or body[:48],
                "url": url,
                "site": site,
                "text": body,
            }
        )
    return records


def section_records(tree, rel, site):
    sections = find_all(
        tree,
        lambda n: n["tag"] == "section" and n["attrs"].get("id") and not under_skip(n),
    )
    records = []
    for sec in sections:
        heads = find_all(sec, lambda n: n["tag"] in ("h1", "h2", "h3"))
        title = clean(text_of(heads[0])) if heads else ""
        body = clean(text_of(sec))
        if not title and not body:
            continue
        anchor = sec["attrs"].get("id") or ""
        records.append(
            {
                "title": title or anchor,
                "url": rel + (("#" + anchor) if anchor else ""),
                "site": site,
                "text": body,
            }
        )
    return records


def site_of(rel):
    for prefix, label in SATELLITES:
        if rel == prefix or rel.startswith(prefix + "/"):
            return label
    return "主站"


def is_satellite(rel):
    return site_of(rel) != "主站"


def collect_paths(root):
    paths = []
    interview = os.path.join(root, "interview.html")
    if os.path.isfile(interview):
        paths.append(interview)
    chapter = os.path.join(root, "java-architect-interview")
    if os.path.isdir(chapter):
        for name in sorted(os.listdir(chapter)):
            if name.endswith(".html") and name != "index.html":
                paths.append(os.path.join(chapter, name))
    for prefix, _label in SATELLITES:
        base = os.path.join(root, prefix)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in ("assets", "docs", "node_modules")]
            for name in sorted(filenames):
                if name.endswith(".html"):
                    paths.append(os.path.join(dirpath, name))
    return paths


def rel_of(path, root):
    return os.path.relpath(path, root).replace(os.sep, "/")


def source_hash(paths, root):
    digest = hashlib.sha256()
    for path in paths:
        rel = rel_of(path, root)
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        with open(path, "rb") as fh:
            digest.update(fh.read())
        digest.update(b"\0")
    return digest.hexdigest()


def extract_file(path, root):
    rel = rel_of(path, root)
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    tree = parse_html(raw)
    site = site_of(rel)
    if not is_satellite(rel):
        return card_records(tree, rel, site)
    heads = h3_records(tree, rel, site)
    if heads:
        return heads
    return section_records(tree, rel, site)


def build(root):
    paths = collect_paths(root)
    digest = source_hash(paths, root)
    records = []
    for path in paths:
        records.extend(extract_file(path, root))
    records.sort(key=lambda rec: (rec["url"], rec["title"]))
    return {"source_hash": digest, "records": records}


def index_path(root):
    return os.path.join(root, "search-index.json")


def dump(payload):
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def main(argv):
    check = "--check" in argv
    root = require_root(__file__)
    payload = build(root)
    dest = index_path(root)
    if check:
        if not os.path.isfile(dest):
            raise SystemExit("search index missing: %s" % dest)
        with open(dest, "r", encoding="utf-8") as fh:
            current = json.load(fh)
        if current.get("source_hash") != payload["source_hash"]:
            raise SystemExit("search index source_hash drift")
        if current.get("records") != payload["records"]:
            raise SystemExit(
                "search index records drift (%s on disk, %s fresh)"
                % (len(current.get("records") or []), len(payload["records"]))
            )
        print("search index OK: %d records" % len(payload["records"]))
        return
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(dump(payload))
        fh.write("\n")
    print("wrote %s (%d records)" % (dest, len(payload["records"])))


if __name__ == "__main__":
    main(sys.argv[1:])
