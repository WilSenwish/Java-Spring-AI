#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""信创研究站构建脚本：把 xinchuang/*.md 编译为「完全自包含」的静态 HTML 站点。

设计约束（对齐 AGENTS.md 红线）：
  1. 自包含：站点只引用自身 assets/ 下的 CSS/JS，不引用 docs/ 或
     core/ 的任何资源；xinchuang/ 可整体拷贝单独部署。
  2. 视觉复用：基础样式由 docs/shared/style/satellite-base.css 复制而来
     （Catppuccin Latte/Mocha 官方色，已通过 docs/scripts/audit_catppuccin.py），
     仅改写文件头注释，保证与 Laws 子站同款 toolbar / hero / toc / 卡片 / 表格 / 暗色令牌。
  3. 独立：不改动 KB 站群任何 SSOT、门禁配置、package.json 或根 index.html；
     构建脚本按红线 12 置于 docs/。
  4. 零第三方依赖：Markdown 渲染仅用 Python 标准库。
  5. 不预览 HTML（红线 1）；本脚本只写文件，可视化确认一律禁止。

用法：
  python3 docs/scripts/build_xinchuang_site.py            # 生成站点
  python3 docs/scripts/build_xinchuang_site.py --check   # 幂等检查：生成结果与磁盘比对，不写文件

产物（均落在 xinchuang/）：
  index.html + 10 篇专题页 + appendix.html
  assets/base.css / site.css / app.js / search-data.js
  源 .md 文件原样保留。
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "xinchuang"
ASSETS = SRC / "assets"
BASE_CSS_SRC = ROOT / "docs" / "shared" / "style" / "satellite-base.css"

SITE_NAME = "信创研究站"
BASELINE = "2026-11-05"

# 页面元数据（唯一真源）：md 源文件名 → HTML 短名 + 导航展示信息。
# 短英文名避免跨系统中文文件名编码差异，页面标题仍为中文。
PAGES: list[dict[str, str]] = [
    {
        "md": "README.md", "html": "index.html", "num": "00", "nav": "研究总纲",
        "title": "信创（信息技术应用创新）研究总纲", "kicker": "全局结论 / 证据规则 / 阅读路径",
        "q": "全局结论、证据规则与按角色阅读路径", "view": "总览",
        "desc": "信创研究总纲：十条核心结论、文档地图、证据分级与使用约定。",
    },
    {
        "md": "01-概念边界与战略逻辑.md", "html": "01-concept.html", "num": "01", "nav": "概念边界与战略逻辑",
        "title": "01 概念边界与战略逻辑", "kicker": "概念 / 战略",
        "q": "信创到底是什么、不是什么、为什么要做", "view": "概念 / 战略",
        "desc": "概念族辨析、三层内涵、战略逻辑、边界与常见误解。",
    },
    {
        "md": "02-政策脉络与法规体系.md", "html": "02-policy.html", "num": "02", "nav": "政策脉络与法规体系",
        "title": "02 政策脉络与法规体系", "kicker": "政策 / 法务 / 采购",
        "q": "从核高基到 834 号令，制度如何演进、条款如何落地", "view": "政策 / 法务 / 采购",
        "desc": "2006—2026 政策时间轴、34 号文逐条拆解、834 号令与 46 号令。",
    },
    {
        "md": "03-产业链全景与技术栈.md", "html": "03-industry.html", "num": "03", "nav": "产业链全景与技术栈",
        "title": "03 产业链全景与技术栈", "kicker": "产业 / 架构",
        "q": "产业链分几层、每层谁在做、卡在哪", "view": "产业 / 架构",
        "desc": "四层/六层模型、厂商图谱、国产化率口径与上游约束。",
    },
    {
        "md": "04-核心硬件与算力底座.md", "html": "04-hardware.html", "num": "04", "nav": "核心硬件与算力底座",
        "title": "04 核心硬件与算力底座", "kicker": "硬件 / 供应链",
        "q": "六条 CPU 路线怎么选、上游短板在哪", "view": "硬件 / 供应链",
        "desc": "六条 CPU 指令集路线、AI 芯片、整机固件、半导体上游与 RISC-V。",
    },
    {
        "md": "05-基础软件与平台软件.md", "html": "05-software.html", "num": "05", "nav": "基础软件与平台软件",
        "title": "05 基础软件与平台软件", "kicker": "基础软件 / 选型",
        "q": "OS、数据库、中间件、云、工具链的真实格局", "view": "基础软件 / 选型",
        "desc": "操作系统、数据库、中间件、一云多芯与 JDK 工具链。",
    },
    {
        "md": "06-安全合规与测评认证体系.md", "html": "06-compliance.html", "num": "06", "nav": "安全合规与测评认证体系",
        "title": "06 安全合规与测评认证体系", "kicker": "安全 / 合规",
        "q": "等保、密评、安全可靠测评、适配认证四套体系的区别", "view": "安全 / 合规",
        "desc": "四套合规体系对照、测评公告全批次索引与误传辨析。",
    },
    {
        "md": "07-行业落地与工程迁移方法论.md", "html": "07-migration.html", "num": "07", "nav": "行业落地与工程迁移方法论",
        "title": "07 行业落地与工程迁移方法论", "kicker": "工程 / 实施",
        "q": "怎么迁、怎么验、Java 栈具体改什么", "view": "工程 / 实施",
        "desc": "行业进度与案例库、六阶段门禁、Java/Spring Boot 专项与 20 项验收清单。",
    },
    {
        "md": "08-产业经济与生态格局.md", "html": "08-economy.html", "num": "08", "nav": "产业经济与生态格局",
        "title": "08 产业经济与生态格局", "kicker": "经济 / 国际比较",
        "q": "市场到底多大、钱从哪来、国际怎么比", "view": "经济 / 国际比较",
        "desc": "市场规模口径大表、驱动力、区域与人才、TCO 与国际比较。",
    },
    {
        "md": "09-风险挑战与批判性视角.md", "html": "09-risks.html", "num": "09", "nav": "风险挑战与批判性视角",
        "title": "09 风险挑战与批判性视角", "kicker": "批判性 / 风控",
        "q": "哪里会失败、哪些说法是错的", "view": "批判性 / 风控",
        "desc": "七类风险、三组正反论点与全站误传辨析汇总。",
    },
    {
        "md": "10-趋势展望与决策建议.md", "html": "10-outlook.html", "num": "10", "nav": "趋势展望与决策建议",
        "title": "10 趋势展望与决策建议", "kicker": "趋势 / 决策",
        "q": "未来往哪走、不同角色现在该做什么", "view": "趋势 / 决策",
        "desc": "五个趋势、三情景推演、分角色建议与 90 天计划。",
    },
    {
        "md": "APPENDIX-参考资料与术语表.md", "html": "appendix.html", "num": "附", "nav": "参考资料与术语表",
        "title": "附录 · 参考资料与术语表", "kicker": "工具书",
        "q": "术语、政策清单、标准清单、来源索引", "view": "工具书",
        "desc": "术语缩略语、政策与标准清单、测评批次、厂商速查与 S01–S70 来源索引。",
    },
]

MD_TO_HTML = {p["md"]: p["html"] for p in PAGES}

# ---------------------------------------------------------------------------
# 行内 / 块级 Markdown 渲染
# ---------------------------------------------------------------------------
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
RE_HR = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
RE_TABLE_SEP = re.compile(r"^\|(?:\s*:?-{2,}:?\s*\|)+\s*$")
RE_UL = re.compile(r"^(\s*)([-*+])\s+(.*)$")
RE_OL = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
RE_FENCE = re.compile(r"^\s*(```|~~~)\s*([A-Za-z0-9_+-]*)\s*$")
RE_LINK = re.compile(r"\[([^\]\n]*)\]\(([^)\n]+)\)")
RE_CODE = re.compile(r"`([^`\n]+?)`")
RE_BARE_URL = re.compile(r"(?<![\w\"'=])https?://[^\s\x00|)）」》，,、；;]+")
RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
RE_EM = re.compile(r"(?<![\w*])\*([^*\s][^*\n]*?[^*\s]|[^*\s])\*(?![\w*])")


def esc(text: str) -> str:
    """HTML 文本转义（不转义引号，正文用）。"""
    return html_lib.escape(text, quote=False)


def esc_attr(text: str) -> str:
    """HTML 属性转义。"""
    return html_lib.escape(text, quote=True)


def strip_inline(text: str) -> str:
    """去掉行内 Markdown 标记，用于 hero 摘要等纯文本位置。"""
    t = RE_CODE.sub(r"\1", text)
    t = RE_LINK.sub(r"\1", t)
    t = t.replace("**", "").replace("*", "").replace("`", "")
    return re.sub(r"\s+", " ", t).strip()


class MarkdownRenderer:
    """轻量 Markdown 渲染器。

    覆盖本套源文档实际使用的语法：h1~h3（自动锚点）、表格（含对齐行）、
    有序/无序列表、引用块、围栏代码块、水平线、粗体/斜体/行内代码、
    Markdown 链接与裸 URL。不支持 Mermaid / 图片 / 脚注（源文档未使用）。
    """

    def __init__(self, md_to_html: dict[str, str]):
        self.md_to_html = md_to_html
        self.toc: list[dict[str, str]] = []
        self._sec = 0
        self._used_ids: set[str] = set()

    # -- 链接映射 ----------------------------------------------------------
    def map_url(self, url: str) -> str:
        """把源文档里的 ./xxx.md 映射为站内 xxx.html；外链与纯锚点原样保留。"""
        u = url.strip()
        if u.startswith(("http://", "https://", "mailto:", "#")):
            return u
        path, _, anchor = u.partition("#")
        if path.startswith("./"):
            path = path[2:]
        if path in self.md_to_html:
            target = self.md_to_html[path]
        elif path.endswith(".md"):
            target = path[:-3] + ".html"  # 兜底：未在元数据登记的同目录 md
        else:
            target = path
        return target + ("#" + anchor if anchor else "")

    # -- 标题锚点 ----------------------------------------------------------
    def make_id(self, level: int) -> str:
        """页内顺序锚点 sec-N（唯一、稳定、可深链），h2/h3 共用同一序列。"""
        self._sec += 1
        base = "sec-%d" % self._sec
        candidate, n = base, 2
        while candidate in self._used_ids:
            candidate = "%s-%d" % (base, n)
            n += 1
        self._used_ids.add(candidate)
        return candidate

    # -- 行内渲染 ----------------------------------------------------------
    def inline(self, text: str) -> str:
        """行内渲染。用占位符隔离代码片段与链接，避免转义破坏标记。"""
        codes: list[str] = []
        links: list[str] = []

        def hold_code(m: re.Match[str]) -> str:
            codes.append("<code>%s</code>" % esc(m.group(1)))
            return "\x00C%d\x00" % (len(codes) - 1)

        def hold_link(m: re.Match[str]) -> str:
            label, url = m.group(1), m.group(2).strip()
            href = self.map_url(url)
            external = href.startswith(("http://", "https://"))
            attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
            # 链接文字递归渲染（可含 **粗体**），但不再次解析链接，避免死循环
            inner = self.inline_text_only(label)
            links.append('<a href="%s"%s>%s</a>' % (esc_attr(href), attrs, inner))
            return "\x00L%d\x00" % (len(links) - 1)

        t = RE_CODE.sub(hold_code, text)
        t = RE_LINK.sub(hold_link, t)

        def hold_url(m: re.Match[str]) -> str:
            u = m.group(0).rstrip(".,;:!?")
            links.append(
                '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
                % (esc_attr(u), esc(u))
            )
            return "\x00L%d\x00" % (len(links) - 1)

        t = RE_BARE_URL.sub(hold_url, t)
        t = esc(t)
        t = RE_BOLD.sub(r"<strong>\1</strong>", t)
        t = RE_EM.sub(r"<em>\1</em>", t)
        t = re.sub(r"\x00C(\d+)\x00", lambda m: codes[int(m.group(1))], t)
        t = re.sub(r"\x00L(\d+)\x00", lambda m: links[int(m.group(1))], t)
        if "\x00" in t:
            raise ValueError("行内占位符未完全还原：%r" % t[:120])
        return t

    def inline_text_only(self, text: str) -> str:
        """链接文字渲染：处理粗体/行内代码，忽略链接与裸 URL。"""
        codes: list[str] = []

        def hold_code(m: re.Match[str]) -> str:
            codes.append("<code>%s</code>" % esc(m.group(1)))
            return "\x00C%d\x00" % (len(codes) - 1)

        t = RE_CODE.sub(hold_code, text)
        t = esc(t)
        t = RE_BOLD.sub(r"<strong>\1</strong>", t)
        t = RE_EM.sub(r"<em>\1</em>", t)
        t = re.sub(r"\x00C(\d+)\x00", lambda m: codes[int(m.group(1))], t)
        return t

    # -- 块级渲染 ----------------------------------------------------------
    def render(self, text: str) -> tuple[str, list[dict[str, str]]]:
        lines = text.splitlines()
        body = self._blocks(lines)
        return body, self.toc

    def _blocks(self, lines: list[str]) -> str:
        out: list[str] = []
        i, n = 0, len(lines)
        while i < n:
            raw = lines[i]
            s = raw.strip()

            if not s:
                i += 1
                continue

            # 围栏代码块
            fm = RE_FENCE.match(s)
            if fm:
                lang, i, buf = fm.group(2), i + 1, []
                while i < n and not RE_FENCE.match(lines[i].strip()):
                    buf.append(lines[i])
                    i += 1
                i += 1  # 跳过结束围栏
                cls = ' class="language-%s"' % esc_attr(lang) if lang else ""
                out.append("<pre><code%s>%s</code></pre>" % (cls, esc("\n".join(buf))))
                continue

            # 标题
            hm = RE_HEADING.match(s)
            if hm:
                level, title = len(hm.group(1)), hm.group(2).strip()
                hid = self.make_id(level) if level in (2, 3) else ""
                id_attr = ' id="%s"' % hid if hid else ""
                out.append("<h%d%s>%s</h%d>" % (level, id_attr, self.inline(title), level))
                if hid:
                    self.toc.append({"level": str(level), "text": strip_inline(title), "id": hid})
                i += 1
                continue

            # 水平线（弱化显示，章节分界）
            if RE_HR.match(s):
                out.append('<hr class="sec-sep" />')
                i += 1
                continue

            # 表格：当前行 |...| 且下一行为分隔行
            if s.startswith("|") and i + 1 < n and RE_TABLE_SEP.match(lines[i + 1].strip()):
                head = self._cells(lines[i])
                sep = self._cells(lines[i + 1])
                aligns = [
                    "ta-center" if c.strip().startswith(":") and c.strip().endswith(":")
                    else "ta-right" if c.strip().endswith(":")
                    else "ta-left" if c.strip().startswith(":")
                    else ""
                    for c in sep
                ]
                i += 2
                rows: list[list[str]] = []
                while i < n and lines[i].strip().startswith("|"):
                    rows.append(self._cells(lines[i]))
                    i += 1
                out.append(self._table(head, rows, aligns))
                continue

            # 引用块：连续 > 行，空行分段
            if s.startswith(">"):
                buf: list[str] = []
                while i < n and lines[i].strip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                out.append("<blockquote>%s</blockquote>" % self._quote(buf))
                continue

            # 列表（源文档无嵌套，按标记类型切分连续块）
            if RE_UL.match(raw) or RE_OL.match(raw):
                i = self._list(lines, i, out)
                continue

            # 段落：连续非空且非块级起始行
            buf = []
            while i < n:
                cur = lines[i].strip()
                if not cur:
                    break
                if (RE_FENCE.match(cur) or RE_HEADING.match(cur) or RE_HR.match(cur)
                        or cur.startswith(">") or RE_UL.match(lines[i]) or RE_OL.match(lines[i])
                        or (cur.startswith("|") and i + 1 < n
                            and RE_TABLE_SEP.match(lines[i + 1].strip()))):
                    break
                buf.append(cur)
                i += 1
            if buf:
                out.append("<p>%s</p>" % "<br />".join(self.inline(x) for x in buf))
            else:
                i += 1
        return "\n".join(out)

    @staticmethod
    def _cells(line: str) -> list[str]:
        """切分表格行，去掉首尾竖线并 trim 单元格。"""
        return [c.strip() for c in line.strip().strip("|").split("|")]

    def _table(self, head: list[str], rows: list[list[str]], aligns: list[str]) -> str:
        def cls(j: int) -> str:
            return ' class="%s"' % aligns[j] if j < len(aligns) and aligns[j] else ""

        thead = "<thead><tr>%s</tr></thead>" % "".join(
            "<th%s>%s</th>" % (cls(j), self.inline(c)) for j, c in enumerate(head)
        )
        body = "".join(
            "<tr>%s</tr>" % "".join(
                "<td%s>%s</td>" % (cls(j), self.inline(c)) for j, c in enumerate(row)
            )
            for row in rows
        )
        return ('<div class="table-wrap"><table>%s<tbody>%s</tbody></table></div>'
                % (thead, body))

    def _quote(self, buf: list[str]) -> str:
        """引用块内按空行分段；段内仍走行内渲染（粗体 / 代码 / 链接不能丢）。"""
        paras: list[list[str]] = []
        cur: list[str] = []
        for line in buf:
            if not line.strip():
                if cur:
                    paras.append(cur)
                    cur = []
            else:
                cur.append(line.strip())
        if cur:
            paras.append(cur)
        return "".join("<p>%s</p>" % "<br />".join(self.inline(x) for x in p) for p in paras)

    def _list(self, lines: list[str], i: int, out: list[str]) -> int:
        """解析连续的同型列表；允许空行后仍属同一列表（源文档未出现嵌套）。"""
        n = len(lines)
        first_ol = bool(RE_OL.match(lines[i]))
        items: list[str] = []
        while i < n:
            s = lines[i].strip()
            if not s:
                # 空行：若下一行仍是同型列表项则继续，否则结束列表
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                if j < n and (RE_OL.match(lines[j]) if first_ol else RE_UL.match(lines[j])):
                    i = j
                    continue
                break
            m = RE_OL.match(s) if first_ol else RE_UL.match(s)
            if not m:
                break
            # 列表项内可能嵌有缩进的围栏代码块（如 07 文档的 Java 启动参数示例）。
            # 文本段与代码块分段渲染：文本走 inline()，围栏独立成 <pre>，避免互相转义。
            segments: list[str] = []
            text_buf: list[str] = [m.group(3)]
            i += 1

            def flush_text() -> None:
                if text_buf:
                    segments.append(self.inline("<br />".join(text_buf)))
                    text_buf.clear()

            while i < n:
                cur = lines[i].strip()
                if not cur:
                    break
                fm = RE_FENCE.match(cur)
                if fm:
                    flush_text()
                    lang = fm.group(2)
                    i += 1
                    buf: list[str] = []
                    while i < n and not RE_FENCE.match(lines[i].strip()):
                        buf.append(lines[i])
                        i += 1
                    if i < n:
                        i += 1  # 跳过结束围栏
                    cls = ' class="language-%s"' % esc_attr(lang) if lang else ""
                    segments.append("<pre><code%s>%s</code></pre>" % (cls, esc("\n".join(buf))))
                    continue
                if (RE_UL.match(cur) or RE_OL.match(cur) or cur.startswith(">")
                        or cur.startswith("|") or RE_HEADING.match(cur) or RE_HR.match(cur)):
                    break
                text_buf.append(cur)
                i += 1
            flush_text()
            items.append("<li>%s</li>" % "".join(segments))
        tag = "ol" if first_ol else "ul"
        out.append("<%s>%s</%s>" % (tag, "".join(items), tag))
        return i


# ---------------------------------------------------------------------------
# HTML 外壳与页面组装
# ---------------------------------------------------------------------------
def toc_html(entries: list[dict[str, str]], css_class: str = "doc-toc") -> str:
    """页内目录：h2 平铺、h3 归入最近 h2 之下（视觉缩进）。"""
    parts: list[str] = []
    for e in entries:
        cls = "toc-h3" if e["level"] == "3" else "toc-h2"
        parts.append(
            '<a class="%s" href="#%s">%s</a>' % (cls, esc_attr(e["id"]), esc(e["text"]))
        )
    return '<nav class="toc %s" id="docToc" aria-label="页内目录"><div class="wrap">%s</div></nav>' % (
        css_class, "".join(parts)
    )


def doc_grid_html() -> str:
    """首页 12 张文档导航卡。"""
    cards: list[str] = []
    for p in PAGES:
        cards.append(
            '<a class="doc-card" href="%s">'
            '<span class="doc-num">%s</span>'
            "<h3>%s</h3>"
            '<p class="doc-q">%s</p>'
            '<span class="doc-view">%s</span>'
            "</a>" % (
                esc_attr(p["html"]), esc(p["num"]), esc(p["nav"]),
                esc(p["q"]), esc(p["view"]),
            )
        )
    return (
        '<section class="doc-map" id="doc-map">'
        '<div class="wrap">'
        '<h2><span class="idx">目录</span>12 篇文档地图</h2>'
        '<p class="lead">每篇独立成页，页内目录可跳转；顶部搜索框可跨页检索全部章节标题。</p>'
        '<div class="doc-grid">%s</div>'
        "</div></section>" % "".join(cards)
    )


def pager_html(index: int) -> str:
    """上一页 / 下一页 / 返回总纲。"""
    prev_p = PAGES[index - 1] if index > 0 else None
    next_p = PAGES[index + 1] if index + 1 < len(PAGES) else None
    left = (
        '<a class="pg-link" href="%s"><span>← 上一篇</span><b>%s %s</b></a>'
        % (esc_attr(prev_p["html"]), esc(prev_p["num"]), esc(prev_p["nav"]))
        if prev_p else '<span class="pg-empty"></span>'
    )
    right = (
        '<a class="pg-link pg-right" href="%s"><span>下一篇 →</span><b>%s %s</b></a>'
        % (esc_attr(next_p["html"]), esc(next_p["num"]), esc(next_p["nav"]))
        if next_p else '<span class="pg-empty"></span>'
    )
    return '<nav class="doc-pager" aria-label="上下篇导航">%s%s</nav>' % (left, right)


def shell(*, title: str, desc: str, hero: str, toc: str, main: str,
          pager: str = "", source_md: str = "", page: str) -> str:
    """统一 HTML 外壳。所有资源均为站内相对路径，无外部依赖。"""
    return """<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="%(desc)s" />
    <meta name="color-scheme" content="light dark" />
    <title>%(title)s · %(site)s</title>
    <script>
      /* 首屏主题同步初始化：在 CSS 之前定好 data-theme，避免深色偏好用户闪白。
         与 assets/app.js 的 readPref() 口径一致：仅 light/dark 为显式偏好，其余跟随系统。 */
      (function () {
        try {
          var v = localStorage.getItem('xc-theme');
          var dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
          document.documentElement.setAttribute('data-theme',
            (v === 'light' || v === 'dark') ? v : (dark ? 'dark' : 'light'));
        } catch (e) { /* 隐私模式忽略持久化失败 */ }
      })();
    </script>
    <link rel="stylesheet" href="assets/base.css" />
    <link rel="stylesheet" href="assets/site.css" />
  </head>
  <body data-page="%(page)s">
    <div class="toolbar">
      <a class="brand" href="index.html">%(site)s</a>
      <div class="tools">
        <div class="search-box">
          <input id="siteSearch" type="search" placeholder="搜索章节 / 文档" autocomplete="off"
                 aria-label="站内搜索" aria-expanded="false" role="combobox" />
          <div id="searchResults" class="search-results" role="listbox" hidden></div>
        </div>
        <button class="btn" id="themeBtn" type="button" title="切换颜色主题">◐ 系统</button>
        <button class="btn" id="topBtn" type="button" title="平滑回到顶部">↑ 顶部</button>
      </div>
    </div>

%(hero)s

%(toc)s

%(main)s

%(pager)s

    <footer>
      <div class="wrap">
        <div class="src">
          <strong>站点说明</strong><br />
          本页由 <code>%(source)s</code> 编译生成，<a href="%(source)s">查看 Markdown 原文</a>；
          调研基准日 %(baseline)s，政策与数据具时效性，引用前请按附录核验路径复核。<br />
          纯静态、零外部依赖：样式与脚本均在 <code>assets/</code> 内，可离线阅读。
        </div>
        <p>信创（信息技术应用创新）研究专题 · 独立站点 · 不隶属于 KB 站群</p>
      </div>
    </footer>

    <script src="assets/search-data.js"></script>
    <script src="assets/app.js"></script>
  </body>
</html>
""" % {
        "site": SITE_NAME,
        "title": esc(title),
        "desc": esc_attr(desc),
        "hero": hero,
        "toc": toc,
        "main": main,
        "pager": pager,
        "source": esc_attr(source_md),
        "baseline": BASELINE,
        "page": esc_attr(page),
    }


def hero_html(*, title: str, sub: str, pills: list[tuple[str, str]], kicker: str,
              compact: bool = False) -> str:
    """生成 hero 区。pills 为 (标签, 值) 元组，值用 <b> 强调（均为构建期常量）。"""
    cls = "hero hero--compact" if compact else "hero"
    pill_html = "".join(
        '<span class="pill">%s <b>%s</b></span>' % (esc(label), esc(value))
        for label, value in pills
    )
    return (
        '<header class="%s"><div class="wrap">'
        '<div class="kicker">%s</div>'
        "<h1>%s</h1>"
        '<p class="sub">%s</p>'
        '<div class="meta">%s</div>'
        "</div></header>" % (cls, esc(kicker), esc(title), esc(sub), pill_html)
    )


def first_quote_summary(md_text: str, fallback: str) -> str:
    """取首个引用块首行作为页面摘要；没有则回退到元数据描述。"""
    for line in md_text.splitlines():
        if line.strip().startswith(">"):
            t = strip_inline(re.sub(r"^\s*>\s?", "", line))
            if t:
                return t[:150]
    return fallback


def build_index(md_text: str) -> tuple[str, list[dict[str, str]]]:
    """首页 = 站点化 hero + 卡片快速导航 + README 全文。

    README 全文（含「二、文档地图」表格与「按角色推荐阅读路径」）完整保留，
    卡片网格承担视觉导航，表格承担可复制的完整索引，二者不互相替代、不删内容。
    """
    renderer = MarkdownRenderer(MD_TO_HTML)
    body, toc = renderer.render(md_text)
    hero = hero_html(
        title="信创（信息技术应用创新）研究总纲",
        sub="面向技术决策者、架构师、采购与合规人员、ISV 与研究者的结构化知识底座："
            "在采购制度、测评体系、技术栈、工程方法、产业组织五个层面同时重建可验证、可审计、可迭代的数字基础设施供给体系。",
        kicker="Information Technology Application Innovation · 研究专题",
        pills=[
            ("调研基准日", BASELINE),
            ("规模", "12 篇 · 约 9.4 万字"),
            ("证据等级", "A / B / C / D"),
            ("形态", "独立静态站点"),
        ],
    )
    nav = '<nav class="toc toc--top" aria-label="本页目录"><div class="wrap">%s</div></nav>' % "".join(
        '<a href="#%s">%s</a>' % (esc_attr(e["id"]), esc(e["text"])) for e in toc if e["level"] == "2"
    )
    # 顺序：hero → 文档卡片 → 本页章节目录 → README 正文
    main = (
        '%s%s<section class="doc-body doc-body--index"><div class="wrap">%s</div></section>'
        % (doc_grid_html(), nav, body)
    )
    return shell(
        title="研究总纲", desc=PAGES[0]["desc"], hero=hero, toc="", main=main,
        source_md="README.md", page="index",
    ), toc


def build_page(idx: int, md_text: str) -> tuple[str, list[dict[str, str]]]:
    p = PAGES[idx]
    renderer = MarkdownRenderer(MD_TO_HTML)
    body, toc = renderer.render(md_text)
    hero = hero_html(
        title=p["title"],
        sub=first_quote_summary(md_text, p["desc"]),
        kicker="%s · %s" % (p["num"], p["kicker"]),
        pills=[
            ("文档", p["num"]),
            ("视角", p["view"]),
            ("基准日", BASELINE),
        ],
        compact=True,
    )
    main = (
        '<div class="wrap doc-layout">%s<article class="doc-body">%s</article></div>'
        % (toc_html(toc), body)
    )
    return shell(
        title=p["nav"], desc=p["desc"], hero=hero, toc="", main=main,
        pager=pager_html(idx), source_md=p["md"], page=p["html"],
    ), toc


# ---------------------------------------------------------------------------
# 站内资源
# ---------------------------------------------------------------------------
SITE_CSS = """/* xinchuang/assets/site.css · 信创研究站专属样式
 * 基础令牌 / toolbar / hero / toc / 卡片 / 表格 / 暗色 / 小屏抽屉来自 base.css。
 * 本文件只写文档站特有的排版与组件；所有颜色一律走 CSS 变量，不引入新色值。
 */

/* ---------- 工具条：品牌 + 搜索 ---------- */
.toolbar .brand { color: var(--strong); text-decoration: none; }
.toolbar .brand:hover { color: var(--accent); text-decoration: none; }
.search-box { position: relative; }
.search-box input {
  font-family: var(--font-sans); font-size: .85rem; color: var(--text);
  background: var(--bg-page); border: 1px solid var(--border-strong);
  border-radius: 9px; padding: .4rem .7rem; width: 190px; outline: none;
  transition: var(--transition);
}
.search-box input:focus { border-color: var(--accent); }
.search-box input::placeholder { color: var(--dim); }
.search-results {
  position: absolute; top: calc(100% + 8px); right: 0; z-index: 1200;
  width: min(420px, 86vw); max-height: 340px; overflow-y: auto;
  background: var(--bg-card); border: 1px solid var(--line);
  border-radius: 10px; box-shadow: var(--shadow-md); padding: 6px;
}
.search-results[hidden] { display: none; }
.search-result {
  display: block; padding: 8px 10px; border-radius: 7px;
  color: var(--text); font-size: 13.5px; text-decoration: none;
}
.search-result:hover, .search-result.is-active { background: var(--bg-elev); text-decoration: none; }
.search-result .sr-doc { display: block; font-size: 11.5px; color: var(--dim); margin-top: 2px; }
.search-empty { padding: 10px; font-size: 13px; color: var(--dim); }

/* ---------- 首页文档地图卡片 ---------- */
.doc-map { padding: 42px 0 8px; }
.doc-map h2 { margin-bottom: 6px; }
.doc-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 14px; margin: 20px 0 8px;
}
.doc-card {
  display: block; position: relative; padding: 16px 18px 18px;
  background: var(--bg-card); border: 1px solid var(--line);
  border-left: 4px solid var(--accent); border-radius: 10px;
  color: var(--text); text-decoration: none; transition: var(--transition);
}
.doc-card:hover { border-color: var(--accent); text-decoration: none; transform: translateY(-2px); box-shadow: var(--shadow-md); }
.doc-card .doc-num {
  display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: .06em;
  color: var(--accent); margin-bottom: 6px;
}
.doc-card h3 { margin: 0 0 8px; font-size: 16.5px; color: var(--strong); }
.doc-card .doc-q { margin: 0 0 10px; font-size: 13.5px; color: var(--muted); line-height: 1.6; }
.doc-card .doc-view {
  display: inline-block; font-size: 11.5px; color: var(--dim);
  border: 1px solid var(--line); border-radius: 999px; padding: 2px 9px;
}

/* ---------- 文档正文 ---------- */
.doc-body { min-width: 0; }
.doc-body--index { padding: 8px 0 46px; }
.doc-body h2 {
  font-size: 23px; margin: 38px 0 14px; padding-bottom: 8px;
  border-bottom: 1px solid var(--line); scroll-margin-top: calc(var(--toolbar-h) + 18px);
}
.doc-body h3 { font-size: 18px; margin: 28px 0 10px; scroll-margin-top: calc(var(--toolbar-h) + 18px); }
.doc-body h4 { font-size: 16px; }
.doc-body p { line-height: 1.85; }
.doc-body ul, .doc-body ol { padding-left: 1.35rem; }
.doc-body li { line-height: 1.8; margin: 5px 0; }
.doc-body hr.sec-sep { border: none; border-top: 1px dashed var(--line); margin: 30px 0; }
.doc-body blockquote {
  background: var(--bg-card); border-left: 4px solid var(--accent);
  border-radius: 8px; padding: 12px 16px; margin: 18px 0; color: var(--muted);
}
.doc-body blockquote p { margin: 4px 0; color: var(--muted); font-size: 14.5px; }
.doc-body pre {
  background: var(--code-bg); color: var(--code-ink); border: 1px solid var(--line);
  border-radius: 9px; padding: 14px 16px; overflow-x: auto; margin: 18px 0;
  font-size: 13px; line-height: 1.7;
}
.doc-body pre code { background: none; padding: 0; font-size: inherit; color: inherit; }
.table-wrap { overflow-x: auto; margin: 18px 0; border: 1px solid var(--line); border-radius: 10px; }
.table-wrap table { margin: 0; min-width: 520px; }
.table-wrap th, .table-wrap td { white-space: normal; }
.table-wrap tbody tr:last-child td { border-bottom: none; }
.ta-left { text-align: left; } .ta-center { text-align: center; } .ta-right { text-align: right; }
.doc-body a { text-decoration: underline; text-underline-offset: 2px; }

/* ---------- 页内目录（桌面左侧竖排；小屏交给 base.css 抽屉） ---------- */
@media (min-width: 1025px) {
  .doc-layout { display: grid; grid-template-columns: 232px minmax(0, 1fr); gap: 30px; align-items: start; }
  nav.toc.doc-toc {
    position: sticky; top: calc(var(--toolbar-h) + 16px); margin: 28px 0 0;
    max-height: calc(100vh - var(--toolbar-h) - 40px); overflow-y: auto;
    background: transparent; border: none; padding: 0;
  }
  nav.toc.doc-toc .wrap {
    display: flex; flex-direction: column; gap: 1px;
    background: transparent; border: none; border-radius: 0; padding: 0;
    font-size: 13.5px;
  }
  nav.toc.doc-toc .wrap a {
    display: block; padding: 5px 9px; border-radius: 6px;
    border-left: 2px solid var(--line); color: var(--muted); line-height: 1.5;
  }
  nav.toc.doc-toc .wrap a:hover { background: var(--bg-card); color: var(--text); text-decoration: none; }
  nav.toc.doc-toc .wrap a.toc-h3 { padding-left: 20px; font-size: 12.5px; }
  nav.toc.doc-toc .wrap a.is-current {
    color: var(--accent); font-weight: 650; border-left-color: var(--accent);
    background: color-mix(in srgb, var(--accent) 10%, transparent);
  }
  .doc-layout > .doc-body { padding: 28px 0 40px; }
}

/* 首页横排目录（沿用 base.css 的 nav.toc 视觉） */
nav.toc--top { margin-top: 24px; }

/* ---------- 上下篇 ---------- */
.doc-pager {
  max-width: var(--maxw); margin: 8px auto 0; padding: 0 22px 24px;
  display: flex; justify-content: space-between; gap: 14px;
}
.pg-link {
  flex: 1 1 0; display: flex; flex-direction: column; gap: 3px;
  background: var(--bg-card); border: 1px solid var(--line);
  border-radius: 10px; padding: 12px 16px; color: var(--text); text-decoration: none;
}
.pg-link:hover { border-color: var(--accent); text-decoration: none; }
.pg-link span { font-size: 12px; color: var(--dim); }
.pg-link b { font-size: 14.5px; color: var(--strong); font-weight: 650; }
.pg-right { text-align: right; }
.pg-empty { flex: 1 1 0; }

/* ---------- 小屏 ---------- */
@media (max-width: 1024px) {
  /* doc-toc 由 base.css 的 .toc-fab + 抽屉机制接管，这里只做正文单列 */
  .doc-layout { display: block; padding-top: 20px; }
  .doc-layout > .doc-body { padding: 0 0 30px; }
  .doc-map { padding-top: 30px; }
}
@media (max-width: 768px) {
  .search-box input { width: 130px; font-size: 12.5px; }
  .toolbar { padding: 8px 14px; }
  .toolbar .brand { font-size: .88rem; }
  .doc-grid { grid-template-columns: 1fr; }
  .doc-body h2 { font-size: 20px; }
  .doc-body h3 { font-size: 16.5px; }
  .doc-pager { flex-direction: column; }
  .pg-empty { display: none; }
  .hero--compact { padding: 40px 0 28px; }
  .table-wrap table { min-width: 480px; font-size: 13px; }
}
@media (max-width: 480px) {
  .search-box input { width: 96px; }
  .btn { padding: 4px 7px; font-size: 12px; }
  .search-results { right: -56px; width: min(340px, 92vw); }
  .doc-body pre { font-size: 12px; padding: 10px 12px; }
  footer { padding-bottom: 90px; }
}

@media print {
  .toolbar, .toc-fab, .toc-backdrop, .doc-pager { display: none !important; }
  .doc-layout { display: block; }
  .table-wrap { overflow: visible; }
}
"""

APP_JS = """/* xinchuang/assets/app.js · 信创研究站交互（零依赖、零外部资源）
 * 职责：
 *  1) 主题三态（浅色 / 深色 / 系统），localStorage 持久化，单一状态源为 html[data-theme]；
 *  2) 顶部工具条：回顶、主题按钮文案同步；
 *  3) 阅读进度（顶栏细条 + 右下浮动环）与回顶 / 去底按钮（DOM 由本文件注入，样式在 base.css）；
 *  4) 页内目录滚动高亮 + 折叠开关；
 *  5) 小屏目录抽屉（左下 FAB + 遮罩 + Esc 关闭）；
 *  6) 站内搜索：读取 assets/search-data.js 的 window.XC_SEARCH，跨页检索章节标题。
 * 说明：本文件刻意使用 ES5 风格字符串拼接，避免模板字符串与构建期转义纠缠。
 */
(function () {
  'use strict';

  /* ---------- 1. 主题 ---------- */
  var KEY = 'xc-theme';
  var LABELS = { light: '☀ 浅色', dark: '☾ 深色', system: '◐ 系统' };
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function readPref() {
    try {
      var v = localStorage.getItem(KEY);
      return (v === 'light' || v === 'dark') ? v : 'system';
    } catch (e) { return 'system'; }
  }
  function effective(pref) {
    if (pref === 'light' || pref === 'dark') return pref;
    return mq && mq.matches ? 'dark' : 'light';
  }
  function apply(pref, fire) {
    var eff = effective(pref);
    document.documentElement.setAttribute('data-theme', eff);
    var btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = LABELS[pref] || LABELS.system;
    if (fire) document.dispatchEvent(new CustomEvent('xc-theme-change', { detail: { pref: pref, effective: eff } }));
  }
  function cycle() {
    var order = ['light', 'dark', 'system'];
    var next = order[(order.indexOf(readPref()) + 1) % order.length];
    try {
      if (next === 'system') localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, next);
    } catch (e) { /* 隐私模式下忽略持久化失败 */ }
    apply(next, true);
  }
  apply(readPref(), false);
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) themeBtn.addEventListener('click', cycle);
  if (mq) {
    var onSys = function () { if (readPref() === 'system') apply('system', true); };
    if (mq.addEventListener) mq.addEventListener('change', onSys);
    else if (mq.addListener) mq.addListener(onSys);
  }

  /* ---------- 2. 工具条回顶 ---------- */
  var topBtn = document.getElementById('topBtn');
  if (topBtn) topBtn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ---------- 3. 阅读进度 / 回顶 / 去底（注入 DOM） ---------- */
  function injectFab(cls, label, svg, onClick) {
    var b = document.createElement('button');
    b.className = cls; b.type = 'button';
    b.setAttribute('aria-label', label); b.setAttribute('title', label);
    b.innerHTML = svg;
    b.addEventListener('click', onClick);
    document.body.appendChild(b);
    return b;
  }
  var bar = document.createElement('div');
  bar.className = 'reading-progress';
  document.body.appendChild(bar);

  var ring = document.createElement('div');
  ring.className = 'reading-progress-fab';
  ring.setAttribute('aria-hidden', 'true');
  ring.innerHTML = '<svg class="reading-progress-fab__svg" viewBox="0 0 40 40">'
    + '<circle class="reading-progress-fab__track" cx="20" cy="20" r="17"></circle>'
    + '<circle class="reading-progress-fab__value" cx="20" cy="20" r="17"></circle></svg>'
    + '<span class="reading-progress-fab__label">0%</span>';
  document.body.appendChild(ring);
  var ringValue = ring.querySelector('.reading-progress-fab__value');
  var ringLabel = ring.querySelector('.reading-progress-fab__label');

  var bottomFab = injectFab('go-to-bottom', '去底部',
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 16l-6-6h4V4h4v6h4l-6 6z"/></svg>',
    function () { window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' }); });
  var topFab = injectFab('back-to-top', '回到顶部',
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 8l6 6h-4v6h-4v-6H6l6-6z"/></svg>',
    function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  var ticking = false;
  function onScrollFrame() {
    ticking = false;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var y = window.scrollY || window.pageYOffset || 0;
    var pct = h > 0 ? Math.max(0, Math.min(100, Math.round(y / h * 100))) : 0;
    bar.style.width = pct + '%';
    ringValue.style.strokeDashoffset = String(106.814 * (1 - pct / 100));
    ringLabel.textContent = pct + '%';
    if (y > 320) { topFab.classList.add('visible'); } else { topFab.classList.remove('visible'); }
    if (h - y > 320) { bottomFab.classList.add('visible'); } else { bottomFab.classList.remove('visible'); }
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScrollFrame); }
  }, { passive: true });
  window.addEventListener('resize', onScrollFrame);
  onScrollFrame();

  /* ---------- 4. 目录：滚动高亮 + 折叠开关 ---------- */
  function initToc() {
    var toc = document.querySelector('nav.toc');
    if (!toc) return;
    var links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
    var pairs = links.map(function (a) {
      return { a: a, el: document.getElementById(a.getAttribute('href').slice(1)) };
    }).filter(function (p) { return p.el; });

    var fold = document.createElement('button');
    fold.type = 'button'; fold.className = 'toc-fold-toggle'; fold.textContent = '目录';
    fold.setAttribute('aria-expanded', 'true');
    var wrap = toc.querySelector('.wrap');
    if (wrap) wrap.insertBefore(fold, wrap.firstChild);
    fold.addEventListener('click', function () {
      var collapsed = toc.classList.toggle('is-collapsed');
      fold.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
    });

    function highlight() {
      var vTop = (window.scrollY || window.pageYOffset || 0) + 160;
      var current = pairs[0];
      for (var i = 0; i < pairs.length; i++) {
        var top = pairs[i].el.getBoundingClientRect().top + (window.scrollY || window.pageYOffset || 0);
        if (top <= vTop) current = pairs[i]; else break;
      }
      pairs.forEach(function (p) { p.a.classList.remove('is-current'); });
      if (current) current.a.classList.add('is-current');
    }
    var tocTick = false;
    window.addEventListener('scroll', function () {
      if (!tocTick) { tocTick = true; window.requestAnimationFrame(function () { tocTick = false; highlight(); }); }
    }, { passive: true });
    highlight();
  }

  /* ---------- 5. 小屏抽屉 ---------- */
  function initDrawer() {
    var toc = document.querySelector('nav.toc');
    if (!toc) return;
    if (!toc.id) toc.id = 'xc-toc';
    var mqSmall = window.matchMedia ? window.matchMedia('(max-width: 1024px)') : null;
    function isSmall() { return mqSmall ? mqSmall.matches : window.innerWidth <= 1024; }

    var fab = document.createElement('button');
    fab.className = 'toc-fab'; fab.type = 'button';
    fab.setAttribute('aria-label', '目录'); fab.setAttribute('title', '目录');
    fab.setAttribute('aria-expanded', 'false'); fab.setAttribute('aria-controls', toc.id);
    fab.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 6h16v2H4V6zm0 5h16v2H4v-2zm0 5h10v2H4v-2z"/></svg>';
    document.body.appendChild(fab);

    var backdrop = document.createElement('button');
    backdrop.className = 'toc-backdrop'; backdrop.type = 'button';
    backdrop.setAttribute('aria-label', '关闭目录');
    document.body.appendChild(backdrop);

    function setOpen(open) {
      if (!isSmall()) open = false;
      document.documentElement.classList.toggle('toc-drawer-open', open);
      fab.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (isSmall()) toc.setAttribute('aria-hidden', open ? 'false' : 'true');
      else toc.removeAttribute('aria-hidden');
    }
    fab.addEventListener('click', function () {
      setOpen(!document.documentElement.classList.contains('toc-drawer-open'));
    });
    backdrop.addEventListener('click', function () { setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.documentElement.classList.contains('toc-drawer-open')) {
        setOpen(false);
        try { fab.focus(); } catch (e2) { /* noop */ }
      }
    });
    toc.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
      if (a && isSmall()) setOpen(false);
    });
    function onResize() {
      if (!isSmall()) { setOpen(false); toc.removeAttribute('aria-hidden'); }
      else if (!document.documentElement.classList.contains('toc-drawer-open')) toc.setAttribute('aria-hidden', 'true');
    }
    onResize();
    if (mqSmall && mqSmall.addEventListener) mqSmall.addEventListener('change', onResize);
    window.addEventListener('resize', onResize);
  }

  /* ---------- 6. 站内搜索 ---------- */
  function initSearch() {
    var input = document.getElementById('siteSearch');
    var box = document.getElementById('searchResults');
    var data = window.XC_SEARCH || [];
    if (!input || !box) return;
    var active = -1, shown = [];

    function close() { box.hidden = true; box.innerHTML = ''; shown = []; active = -1; input.setAttribute('aria-expanded', 'false'); }
    function go(item) {
      if (!item) return;
      window.location.href = item.p + (item.a ? '#' + item.a : '');
      close();
    }
    function paint(list) {
      shown = list; active = -1;
      if (!list.length) {
        box.innerHTML = '<div class="search-empty">没有匹配的章节，试试「口径」「测评」「迁移」</div>';
        box.hidden = false; input.setAttribute('aria-expanded', 'true'); return;
      }
      box.innerHTML = list.map(function (it, i) {
        return '<a class="search-result" data-i="' + i + '" href="' + it.p + (it.a ? '#' + it.a : '') + '">'
          + it.t + '<span class="sr-doc">' + it.d + (it.a ? ' · 章节' : ' · 文档') + '</span></a>';
      }).join('');
      box.hidden = false; input.setAttribute('aria-expanded', 'true');
      Array.prototype.forEach.call(box.querySelectorAll('.search-result'), function (a) {
        a.addEventListener('mousedown', function (e) { e.preventDefault(); go(shown[Number(a.getAttribute('data-i'))]); });
      });
    }
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      if (!q) { close(); return; }
      var hits = [];
      for (var i = 0; i < data.length && hits.length < 8; i++) {
        if (data[i].t.toLowerCase().indexOf(q) !== -1 || data[i].d.toLowerCase().indexOf(q) !== -1) hits.push(data[i]);
      }
      paint(hits);
    });
    input.addEventListener('keydown', function (e) {
      if (box.hidden || !shown.length) {
        if (e.key === 'Escape') close();
        return;
      }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        active = (active + (e.key === 'ArrowDown' ? 1 : -1) + shown.length) % shown.length;
        Array.prototype.forEach.call(box.querySelectorAll('.search-result'), function (a, i) {
          a.classList.toggle('is-active', i === active);
        });
      } else if (e.key === 'Enter') {
        e.preventDefault(); go(shown[active >= 0 ? active : 0]);
      } else if (e.key === 'Escape') { close(); }
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest || !e.target.closest('.search-box')) close();
    });
  }

  function boot() { initToc(); initDrawer(); initSearch(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
"""


def base_css_text() -> str:
    """复制共享基础样式，仅改写文件头注释，保持色值与规则完全一致。"""
    src = BASE_CSS_SRC.read_text(encoding="utf-8")
    header = """/* xinchuang/assets/base.css · 信创研究站基础样式（自包含副本）
 * 来源：docs/shared/style/satellite-base.css（三子站共用基础样式，Catppuccin Latte/Mocha 官方色）。
 * 站点要求「完全自包含」，故复制一份到站内 assets/，不跨目录引用任何共享资源；
 * 色值与规则与来源保持一致，视觉对齐 Software-Engineering-Laws-Theories-Principles-and-Patterns。
 * 注意：这是独立副本，上游基础样式更新时不会自动同步；如需同步请重新运行
 *       python3 docs/scripts/build_xinchuang_site.py
 * 主题：浅色 :root + html[data-theme="dark"]；系统偏好由 assets/app.js 处理。
 */
"""
    # 去掉原文件的多行文件头注释（首个 /* ... */），其余规则原样保留
    body = re.sub(r"^/\*.*?\*/\s*", "", src, count=1, flags=re.S)
    return header + body


def build_search_data(all_tocs: dict[str, list[dict[str, str]]]) -> str:
    """生成跨页章节检索数据（普通 script 赋值，file:// 下无需 fetch）。"""
    items: list[dict[str, str]] = []
    for p in PAGES:
        items.append({"t": p["nav"], "p": p["html"], "a": "", "d": "%s %s" % (p["num"], p["nav"])})
        for e in all_tocs.get(p["html"], []):
            items.append({"t": e["text"], "p": p["html"], "a": e["id"], "d": "%s %s" % (p["num"], p["nav"])})
    return ("/* xinchuang/assets/search-data.js · 由 docs/scripts/build_xinchuang_site.py 生成，勿手改 */\n"
            "window.XC_SEARCH = " + json.dumps(items, ensure_ascii=False, indent=2) + ";\n")


def generate() -> dict[Path, str]:
    """生成全部产物，返回 {目标路径: 内容}，不写磁盘（便于 --check 幂等比对）。"""
    out: dict[Path, str] = {}
    all_tocs: dict[str, list[dict[str, str]]] = {}

    for idx, p in enumerate(PAGES):
        md_path = SRC / p["md"]
        if not md_path.is_file():
            raise SystemExit("FAIL 缺少源文档：%s" % md_path)
        md_text = md_path.read_text(encoding="utf-8")
        if idx == 0:
            page_html, toc = build_index(md_text)
        else:
            page_html, toc = build_page(idx, md_text)
        out[SRC / p["html"]] = page_html
        all_tocs[p["html"]] = toc

    out[ASSETS / "base.css"] = base_css_text()
    out[ASSETS / "site.css"] = SITE_CSS
    out[ASSETS / "app.js"] = APP_JS
    out[ASSETS / "search-data.js"] = build_search_data(all_tocs)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="幂等检查：与磁盘内容比对，不写文件")
    args = ap.parse_args()

    if not BASE_CSS_SRC.is_file():
        print("FAIL 缺少基础样式源：%s" % BASE_CSS_SRC)
        return 1

    generated = generate()
    if args.check:
        drift = [str(p.relative_to(ROOT)) for p, content in generated.items()
                 if not p.is_file() or p.read_text(encoding="utf-8") != content]
        if drift:
            print("FAIL 产物与构建脚本不一致（%d 个）：" % len(drift))
            for d in drift:
                print("  ", d)
            return 1
        print("OK 幂等：%d 个产物与构建脚本输出一致" % len(generated))
        return 0

    ASSETS.mkdir(parents=True, exist_ok=True)
    for path, content in generated.items():
        path.write_text(content, encoding="utf-8")
        print("  WRITE %-52s %7d bytes" % (str(path.relative_to(ROOT)), len(content.encode("utf-8"))))
    print("DONE 生成 %d 个文件（%d 个 HTML 页面 + 4 个 assets）"
          % (len(generated), len(PAGES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
