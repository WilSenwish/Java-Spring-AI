#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_index_badges.py — 根 index / overview 聚合 UI 结构 + 小屏留白门禁（防复发）
=========================================================================================
背景（2026-09-16 实测事故，两类）：

  甲 · 徽标结构
    1) overview：`.ov-item` 的 difficulty/priority 未用 `.ov-badges` 包裹 → 间距取容器
       `--space-sm`，与其余 4px 不一致（视觉「样式不统一」）。实测 15 条。
    2) 根 index：`<a>` 行顶格（缺缩进）且 `q-tags` 未闭合、priority 缺失（源页有 p1 时漏渲染）。
       实测 7 条（其中 5 条 C/S 卡漏 priority，2 条 G 卡仅缺闭合）。

  乙 · 小屏横向留白（4 个来源叠加）
    根 index 375px 下列表可用宽仅 229px（视口 61%），每侧被吃掉 68px：
    容器 24 + 页面内联 section margin 12 + **共享 design-system.css ≤768 段的 section padding 12**
    + 边框 1 + group/q-list/q-item 各 8。
    归一口径：横向留白唯一来源 = `.dir-container` 的 12px；section 的 margin/padding 均须为 0；
    列表横向内缩由 `.dir-body` **单层**承担 4px（.dir-group / .q-list 横向必须为 0；
    .q-item 只约束**左侧**为 0 —— 其右侧内缩有意保留，hover 背景才不会贴死行尾）。
    修复后可用宽 325px（87%）。

  丙 · 页内对齐（2026-09-16 风格归一化）
    1) 左侧内容线：`.q-list` / `.q-item` 的**左侧**内缩必须为 0，使题号列与分组标题左缘共线
       （改前桌面 107 vs 91、小屏 25 vs 17，各差 16/8px）。注意只约束左侧——
       右侧保留内缩，否则 hover 背景会贴死行尾。
    2) 右侧计数线：`.dir-group-title` 必须 `display:flex` + `justify-content:space-between`，
       使分组计数与章节计数胶囊落在同一条右缘垂直线（改前分组计数紧邻标题文本）。
    3) 计数胶囊定位：`.dir-count` 必须 `margin-left:auto` —— 位置**不可**依赖
       `.tagline{flex:1}` 撑开。无 tagline 的区块（深度 Q&A 15 篇章）会退化为紧贴标题
       （实测桌面右缘 294px vs 行尾 1035px）；小屏因 `.dir-title{flex:1 1 auto}` 恰好把
       胶囊推开，才掩盖了该缺陷（长官反馈「小屏统一、大屏不统一」的成因）。
    4) 列表横向内缩单层化：`.dir-body` 独占（桌面 `var(--dir-pad-panel)` / 小屏 4px），
       桌面与小屏的 `.dir-group` 横向必须为 0。否则「有分组」与「无分组」两类区块的
       题号左缘会分叉（实测 17px vs 1px），视觉上像两个不同页面。

  丁 · 页内 token 解析
    根 index 内联样式已 token 化（`:root` 下的 `--dir-*`），断言前会先把 `var(--dir-xxx)`
    解析为实际值再比对，因此「把字面量改成 token」不会造成误报。
    若出现无法解析的变量名（token 被删/改名），按缺陷报出——不静默放行（防止门禁失效）。

用法：
  python3 check_index_badges.py [项目根]     # 默认自动向上查找项目根（含 AGENTS.md + index.html 的目录）
退出码：0 = 通过；1 = 存在缺陷；2 = 路径解析失败（可直接用作门禁）。
"""
import re
import sys
import os


def find_base():
    """向上查找项目根：同时含 AGENTS.md 与 index.html 的最近祖先目录。

    不用固定层级 dirname —— 本技能可能经 `.agents/skills/java-kb-expand`
    软链调用，且脚本目录深度会随重构变化，固定层级会静默指到 `.workbuddy/`。
    """
    d = os.path.dirname(os.path.realpath(__file__))
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "AGENTS.md")) and os.path.isfile(os.path.join(d, "index.html")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


BASE = sys.argv[1] if len(sys.argv) > 1 else find_base()
if not BASE or not os.path.isdir(BASE):
    print("FAIL 无法定位项目根（请显式传入：check_index_badges.py <项目根>）")
    sys.exit(2)
IDX = os.path.join(BASE, "index.html")
OV = os.path.join(BASE, "java-architect-interview/nav-overview-priority.html")
for _p in (IDX, OV):
    if not os.path.isfile(_p):
        print(f"FAIL 目标文件不存在：{_p}")
        sys.exit(2)

badges = []   # 甲类：徽标结构
gutter = []   # 乙类：小屏留白
align = []    # 丙类：页内对齐
unresolved = []  # 丁类：无法解析的页内变量


def page_tokens(text):
    """提取根 index 内联样式 `:root` 下的页内 token（--*）。"""
    toks = {}
    for m in re.finditer(r":root\s*\{(.*?)\}", text, re.S):
        for dm in re.finditer(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", m.group(1)):
            toks[dm.group(1)] = dm.group(2).strip()
    return toks


def resolve_vars(text, toks, rounds=5):
    """把 var(--x) 就地解析为取值，供断言比对（支持多轮嵌套）。

    无法解析的变量名记入 unresolved —— 断言不得因此静默通过。
    """
    def repl(m):
        name = m.group(1)
        if name in toks:
            return toks[name]
        # 只对页内命名空间（--dir-*）报未解析；共享 CSS 的变量（--rule/--accent…）不属本门禁范围
        if name.startswith("--dir-") and name not in unresolved:
            unresolved.append(name)
        return m.group(0)
    for _ in range(rounds):
        new = re.sub(r"var\(\s*(--[a-z0-9-]+)\s*(?:,[^)]*)?\)", repl, text)
        if new == text:
            break
        text = new
    return text


def _pad_vals(decl_value):
    """把 padding 取值按空白分解为 px 数值列表。

    必须支持**无单位 0**（`padding: 0`、简写末位的 `0`）—— 早期实现用
    `(\\d+)(px|rem)` 会漏掉它们，导致简写被误判为 3 值/2 值，左值取错。
    """
    vals = []
    for tok in decl_value.split():
        m = re.match(r"^(\d+(?:\.\d+)?)(px|rem)?$", tok)
        if not m:
            continue
        vals.append(float(m.group(1)) * (16 if m.group(2) == "rem" else 1))
    return vals


def left_px(decl_value):
    """取「左侧」值（px）。1值=全边；2值=纵/横；3值=上/横/下；4值=上/右/下/左。"""
    vals = _pad_vals(decl_value)
    if not vals:
        return None
    if len(vals) == 1:
        return vals[0]
    if len(vals) == 2:
        return vals[1]
    if len(vals) == 3:
        return vals[1]
    return vals[3]


def horiz_px(decl_value):
    """取横向（左/右）值（px），返回列表。"""
    vals = _pad_vals(decl_value)
    if not vals:
        return []
    if len(vals) == 1:
        return vals
    if len(vals) in (2, 3):
        return [vals[1]]
    return [vals[1], vals[3]]


def media_block(text, width):
    """取出 `@media (max-width: <width>px) { ... }` 的块体（按花括号配对，不依赖缩进）。"""
    m = re.search(r"@media\s*\(max-width:\s*%dpx\)\s*\{" % width, text)
    if not m:
        return None
    i = text.index("{", m.start())
    depth, j = 0, i
    while j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j]
        j += 1
    return None


# ---------- 甲 1) overview：每个 ov-item 必须用 .ov-badges 包裹 difficulty+priority ----------
t = open(OV, encoding="utf-8").read()
for m in re.finditer(r'<a class="ov-item"[^>]*>.*?</a>', t, re.S):
    b = m.group(0)
    if 'class="ov-badges"' not in b:
        num = re.search(r'class="ov-num">([^<]+)<', b)
        badges.append(f"[overview] {num.group(1) if num else '?'} 缺 .ov-badges 包裹")

# ---------- 甲 2) 根 index：a) <a> 顶格；b) q-tags 标签不平衡（未闭合） ----------
t = open(IDX, encoding="utf-8").read()
for i, ln in enumerate(t.split("\n"), 1):
    if re.match(r'^<a href=', ln):
        badges.append(f"[index] L{i} <a> 顶格（缺缩进）")
    if '<span class="q-tags"' in ln:
        seg = ln[ln.index('<span class="q-tags"'):]
        if seg.count("<span") != seg.count("</span>"):
            qid = re.search(r'class="q-id">([^<]+)<', ln)
            badges.append(f"[index] L{i} q-tags 未闭合（{qid.group(1) if qid else '?'}）")

# ---------- 丁) 页内 token 解析（先做，供乙/丙断言使用；字面量→token 不误报） ----------
TOKENS = page_tokens(t)
t_res = resolve_vars(t, TOKENS)

# ---------- 乙) 小屏横向留白单一来源（静态结构断言） ----------
blk = media_block(t, 768)
if blk is not None:
    blk = resolve_vars(blk, TOKENS)
if blk is None:
    gutter.append("未找到 @media (max-width: 768px) 段（根 index 小屏样式缺失）")
else:
    # b1) .dir-container 的横向 padding 必须为 12px（唯一 gutter 来源）
    mc = re.search(r"\.dir-container\s*\{([^}]*)\}", blk)
    if not mc:
        gutter.append("≤768 段缺 .dir-container 规则（无法确立统一 gutter）")
    else:
        body = mc.group(1)
        if not re.search(r"padding:\s*0\s+12px", body):
            got = re.search(r"padding:\s*([^;]+);", body)
            gutter.append(f".dir-container 横向 padding 非 `0 12px`"
                          f"（实际 `{got.group(1).strip() if got else '?'}`）—— gutter 未归一")
    # b2) .dir-section 必须显式归零横向 margin/padding（否则叠加页面内联 margin + 共享 CSS padding）
    ms = re.search(r"\.dir-section\s*\{([^}]*)\}", blk)
    if not ms:
        gutter.append("≤768 段缺 .dir-section 归零规则（共享 CSS 会给它加 12px padding）")
    else:
        body = ms.group(1)
        for prop in ("padding-left", "padding-right", "margin-left", "margin-right"):
            m2 = re.search(prop + r"\s*:\s*([^;]+);", body)
            if not m2:
                gutter.append(f".dir-section 未显式声明 `{prop}: 0`（会回落/叠加其它留白）")
            elif m2.group(1).strip() not in ("0", "0px"):
                gutter.append(f".dir-section `{prop}: {m2.group(1).strip()}` 非 0 —— 叠加留白")
    # b3) 列表横向内缩**单层化**：.dir-body 独占（≤4px），group/q-list/q-item 必须为 0。
    #     简写解析统一走全局 horiz_px / _pad_vals（支持无单位 0）。
    m3 = re.search(r"\.dir-body\s*\{([^}]*)\}", blk)
    if not m3:
        gutter.append("≤768 段缺 .dir-body 规则（列表横向内缩失去唯一归属层）")
    else:
        mm = re.search(r"padding\s*:\s*([^;]+);", m3.group(1))
        hv = horiz_px(mm.group(1)) if mm else []
        if not hv:
            gutter.append("≤768 段 .dir-body 未声明 padding（内缩层缺失，列表会紧贴 section 边框）")
        elif max(hv) > 4.5:
            gutter.append(f".dir-body 横向 padding `{mm.group(1).strip()}` 超出 4px 内缩口径"
                          f"（{max(hv):g}px）—— 小屏可用宽被吃掉")
    for sel in (".dir-group", ".q-list", ".q-item"):
        m4b = re.search(re.escape(sel) + r"\s*\{([^}]*)\}", blk)
        if not m4b:
            gutter.append(f"≤768 段缺 {sel} 的横向归零规则（回落桌面值会叠加留白）")
            continue
        for pm in re.finditer(r"(padding|padding-left|padding-right)\s*:\s*([^;]+);", m4b.group(1)):
            prop, val = pm.group(1), pm.group(2).strip()
            if sel == ".q-item":
                # q-item 只约束**左侧**：右侧内缩有意保留（hover 背景不贴死行尾），
                # 且「有/无分组」两类区块该值相同，不会造成右缘分叉。
                if prop == "padding":
                    worst, axis = (left_px(val) or 0.0), "左侧"
                elif prop == "padding-left":
                    worst, axis = max(_pad_vals(val) or [0]), "左侧"
                else:
                    continue
            else:
                worst = max((horiz_px(val) if prop == "padding" else _pad_vals(val)) or [0])
                axis = "横向"
            if worst > 0.5:
                gutter.append(f"≤768 {sel} {axis} padding `{val}` ≠ 0 —— 内缩层必须唯一（.dir-body）")

# ---------- 丙) 页内对齐：题号列与分组标题左缘共线 + 分组计数右对齐 ----------
# 只约束「左侧」内缩为 0：右侧必须保留内缩，否则 hover 背景会贴死行尾。
for label, block in (("桌面", t_res), ("小屏", blk)):
    if not block:
        continue
    for sel in (".q-list", ".q-item"):
        m4 = re.search(re.escape(sel) + r"\s*\{([^}]*)\}", block)
        if not m4:
            align.append(f"{label} 缺 {sel} 规则（无法确认题号与分组标题共线）")
            continue
        body = m4.group(1)
        m5 = re.search(r"padding\s*:\s*([^;]+);", body)
        lp = left_px(m5.group(1)) if m5 else None
        if lp is None:
            m6 = re.search(r"padding-left\s*:\s*([^;]+);", body)
            lp = left_px(m6.group(1)) if m6 else None
        if lp is None:
            align.append(f"{label} {sel} 未声明横向 padding（无法确认左侧内缩）")
        elif lp > 0.5:
            align.append(f"{label} {sel} 左侧内缩 {lp:g}px ≠ 0 —— 题号列与分组标题左缘不共线")

mgt = re.search(r"\.dir-group-title\s*\{([^}]*)\}", t_res)
if not mgt:
    align.append("缺 .dir-group-title 规则（分组计数定位方式未知）")
else:
    gb = mgt.group(1)
    if "display: flex" not in gb:
        align.append(".dir-group-title 非 flex —— 分组计数无法右推")
    if "space-between" not in gb:
        align.append(".dir-group-title 缺 justify-content: space-between"
                     " —— 分组计数与章节计数胶囊右缘不共线")

# 丙 3) 计数胶囊定位：margin-left:auto 是唯一来源（无 .tagline 的区块也必须贴行尾）
mdc = re.search(r"\.dir-count\s*\{([^}]*)\}", t_res)
if not mdc:
    align.append("缺 .dir-count 规则（计数胶囊定位方式未知）")
elif not re.search(r"margin-left\s*:\s*auto", mdc.group(1)):
    align.append(".dir-count 缺 `margin-left: auto` —— 无 .tagline 的区块计数胶囊会紧贴标题"
                 "（深度 Q&A 15 篇章，桌面实测右缘 294px vs 行尾 1035px）")

# 丙 4) 桌面 .dir-group 横向必须为 0（内缩由 .dir-body 独占，两类区块才共线）
mgd = re.search(r"\.dir-group\s*\{([^}]*)\}", t_res)
if not mgd:
    align.append("缺桌面 .dir-group 规则（列表内缩归属未知）")
else:
    mmg = re.search(r"padding\s*:\s*([^;]+);", mgd.group(1))
    hvg = horiz_px(mmg.group(1)) if mmg else []
    if hvg and max(hvg) > 0.5:
        align.append(f"桌面 .dir-group 横向 padding `{mmg.group(1).strip()}` ≠ 0 ——"
                     " 内缩层必须唯一（.dir-body），否则无分组的篇章列表会紧贴 section 左边框")

problems = badges + gutter + align + [
    f"页内变量 {v} 无法解析（token 被删/改名 → 门禁可能失准）" for v in unresolved]
if problems:
    print(f"FAIL 发现 {len(problems)} 处缺陷（徽标结构 {len(badges)} / 小屏留白 {len(gutter)}"
          f" / 页内对齐 {len(align)} / 变量解析 {len(unresolved)}）：")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("PASS 根 index / overview：徽标结构一致（无顶格行、无未闭合 q-tags）；"
      "小屏 gutter 单一来源且列表内缩单层（.dir-body ≤4px）；题号列与分组标题左缘共线、"
      "分组计数与章节胶囊右缘共线、计数胶囊 margin-left:auto（无 tagline 区块同样贴行尾）。")
