#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 计数真源审计（audit_truth_source.py）

长官指令（2026-09-21）：「先要登记计数位置点，然后登记的位置点的计数得有正确性校验」。
本脚本补上最后一环 —— **值本身的正确性**。此前四重门禁全在证明「站内自洽」
（position ↔ SSOT ↔ DOM 互相对齐），但若某个值一开始就写错、或页面内容变了而 SSOT 没跟，
门禁照样全绿（2026-09-21 实测抓到 `dir_group_1` 显示 16 而实际 17 项，长期无人发现）。

两道检查：
  A) **真源完备性** —— 每一个已登记 position 的键，必须能被 SSOT `guard.sources` 的某条规则
     或 `sources.manual` 覆盖。**未被覆盖即 FAIL「未声明真源」**（不允许存在「没人管正确性」的计数）。
  B) **真值校验** —— 按规则独立求出真值，与 SSOT 键值、DOM 显示值**三方比对**。

真源类型（全部读 SSOT，脚本内不写死键名/区间/文件名）：
  dom_scan / cards_by_link / block_count_same_file / host_page_cards / sum / file_count

用法：
  python3 audit_truth_source.py [项目根] [--quiet] [--list]
  退出码：0=全绿；1=有缺陷；2=配置/定位失败
"""
import argparse
import glob
import io
import json
import os
import re
import sys

DEF_EXCLUDE = ["tmp/", "node_modules/", "rk/"]


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "docs", "kb-counts.json")):
            return d
        nd = os.path.dirname(d)
        if nd == d:
            break
        d = nd
    return None


def read(p):
    return io.open(p, encoding="utf-8", errors="ignore").read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--quiet", action="store_true", help="只输出结论")
    ap.add_argument("--list", action="store_true", help="列出每条规则求出的真值")
    ap.add_argument("--max", type=int, default=0,
                    help="每类 FAIL 最多打印条数（默认 0=不限；门禁不得藏发现）")
    a = ap.parse_args()

    root = os.path.abspath(a.root) if a.root else find_root(
        os.path.dirname(os.path.abspath(__file__)))
    if not root or not os.path.isfile(os.path.join(root, "docs", "kb-counts.json")):
        print("FAIL 未能定位项目根（须含 docs/kb-counts.json）")
        return 2
    ssot = json.load(io.open(os.path.join(root, "docs", "kb-counts.json"), encoding="utf-8"))
    G = ssot.get("guard") or {}
    SRC = G.get("sources") or {}
    RULES = SRC.get("rules") or []
    MANUAL = SRC.get("manual") or []
    EXCLUDE = G.get("exclude") or DEF_EXCLUDE
    if not RULES:
        print("FAIL guard.sources.rules 为空 —— 真源未声明（见 conventions.md §5.1.4）")
        return 2

    # ---------- 键取值 ----------
    def ssot_val(key):
        if key.startswith("counts."):
            return (ssot.get("counts") or {}).get(key[7:])
        k = key[7:] if key.startswith("struct.") else key
        v = (ssot.get("struct") or {}).get(k)
        if v is None:
            v = (ssot.get("counts") or {}).get(k)
        return v

    def flat_struct():
        out = {}

        def w(o, pre=""):
            if isinstance(o, dict):
                for k2, v in o.items():
                    w(v, pre + ("." if pre else "") + k2)
            else:
                out[pre] = o
        w(ssot.get("struct") or {})
        return out
    FLAT = flat_struct()

    # ---------- 键路径冲突：扁平点分键 vs 嵌套键「双写」 ----------
    # 2026-09-21 实测：SSOT 同时存在 `struct["mind.idx.mind-foot-c_11"] = 30`（扁平）
    # 与 `struct["mind"]["idx"]["mind-foot-c_11"] = 28`（嵌套），展平后同路径、值不同。
    # `sync_counts.resolve_key` 只认扁平键，故嵌套那份是「看不见的第二写源」——
    # 谁来都查不出，直到真源审计把它当「双写」暴露出来。
    def _dup_paths(node, path=""):
        out = []
        if not isinstance(node, dict):
            return out
        ks = set(node.keys())
        for k, v in node.items():
            if "." in k:
                segs = k.split(".")
                for i in range(1, len(segs)):
                    pref = ".".join(segs[:i])
                    if pref in ks and isinstance(node.get(pref), dict):
                        out.append("%s%s.（展平后与嵌套键 «%s» 同路径 —— 同一逻辑键写了两处）"
                                   % (path, k, pref))
            out += _dup_paths(v, path + k + ".")
        return out

    DUPS = _dup_paths(ssot.get("struct") or {}, "struct.") + \
        _dup_paths(ssot.get("counts") or {}, "counts.")

    def lookup(key):
        """按键名取值（支持 struct.* / counts.* / 裸键，以及 ov.subgroup_N 这类无 struct. 前缀写法）"""
        if key.startswith("struct."):
            return FLAT.get(key[7:])
        if key.startswith("counts."):
            return (ssot.get("counts") or {}).get(key[7:])
        if key in FLAT:
            return FLAT[key]
        return (ssot.get("counts") or {}).get(key)

    truth = {}      # key -> 真值
    evid = {}       # key -> 证据串
    kbcount = {}    # key -> (position id, DOM 显示值)
    CONFLICT = []   # 同一键被两条声明求出不同值

    def put(key, val, why):
        # 同一键被多条声明覆盖是允许的，但**值必须一致** ——
        # 不一致说明「双写」，必须暴露（2026-09-21 曾在 SSOT 抓到扁平/嵌套双写不同值）。
        if key in truth and truth[key] != val:
            CONFLICT.append("%s：本次 %s（%s）≠ 先前 %s（%s）"
                            % (key, val, why, truth[key], evid.get(key, "")))
        else:
            truth[key] = val
            evid[key] = why

    # ---------- 规则实现 ----------
    def r_dom_scan(r):
        p = os.path.join(root, r["file"])
        if not os.path.isfile(p):
            return ["规则 %s 文件不存在：%s" % (r["id"], r["file"])]
        t = read(p)
        if r.get("end_re"):
            blocks = re.findall(r["block_re"] + r"[\s\S]*?" + r["end_re"], t)
        else:
            ms = list(re.finditer(r["block_re"], t))
            blocks = [t[m.end():ms[i + 1].start() if i + 1 < len(ms) else len(t)]
                      for i, m in enumerate(ms)]
        kr = re.compile(r["key_re"])
        n = 0
        for b in blocks:
            dm = re.search(r'data-kb-count="([^"]+)"[^>]*data-kb-pos="(P\d+)"[^>]*>(\d+)<', b)
            if not dm:
                continue
            key = dm.group(1)
            if not kr.match(key):
                continue
            cnt = len(re.findall(r["count_re"], b))
            kbcount[key] = (dm.group(2), int(dm.group(3)))
            put(key, cnt, "%s 块内 %s" % (r["file"].split("/")[-1], r["count_re"][:24]))
            n += 1
        if n == 0:
            return ["dom_scan 规则 %s 未命中任何块（block_re=%s）" % (r["id"], r["block_re"][:40])]
        return []

    def r_cards_by_link(r):
        errs = []
        idx = os.path.join(root, r["index_file"])
        if not os.path.isfile(idx):
            return ["规则 %s index_file 不存在" % r["id"]]
        t = read(idx)
        kr = re.compile(r["key_re"])
        if r.get("seq_by") == "chip_present":
            cards = [(m.group(1), m.group(0)) for m in re.finditer(
                r["link_re"] + r"[\s\S]*?</a>", t)]
            seq = {}
            for href, body in cards:
                # 一张卡片可能同时挂 c/e/s 三个 chip —— 必须 finditer 全取，
                # 只取第一个会让后两类永远求不出真值（2026-09-21 修复）。
                for km in re.finditer(
                        r'data-kb-count="([^"]+)"[^>]*data-kb-pos="(P\d+)"[^>]*>(\d+)<', body):
                    mk = kr.match(km.group(1))
                    if not mk:
                        continue
                    typ, nn = mk.group(1), int(mk.group(2))
                    seq.setdefault(typ, []).append((nn, href, km.group(2), int(km.group(3))))
            for typ, items in seq.items():
                for i, (nn, href, pid, shown) in enumerate(items, 1):
                    if nn != i:
                        errs.append("mind_foot 编号断裂：%s 第 %d 个 chip 编号为 %d" % (typ, i, nn))
                    tgt = os.path.join(root, os.path.dirname(r["index_file"]), href)
                    if not os.path.isfile(tgt):
                        errs.append("mind_foot 目标页不存在：%s" % href)
                        continue
                    cnt = len(re.findall(r["count"][typ], read(tgt)))
                    key = "struct.mind.idx.mind-foot-%s_%d" % (typ, nn)
                    kbcount[key] = (pid, shown)
                    put(key, cnt, "%s 的 %s 类卡数" % (href, typ))
            return errs
        # nth_from == key
        links = re.findall(r["link_re"], t)
        for pos_key in [k for k in _pos_keys() if kr.match(k)]:
            mk = kr.match(pos_key)
            groups = mk.groups()
            # 末组若为难度名则用它选 count
            kind = None
            if isinstance(r.get("count"), dict):
                kind = groups[-1]
                nn = int(groups[-2])
            else:
                nn = int(groups[-1])
            if nn < 1 or nn > len(links):
                errs.append("规则 %s：键 %s 序号 %d 超出链接数 %d" % (r["id"], pos_key, nn, len(links)))
                continue
            href = links[nn - 1]
            tgt = os.path.join(root, os.path.dirname(r["index_file"]), href)
            if not os.path.isfile(tgt):
                errs.append("规则 %s：目标页不存在 %s" % (r["id"], href))
                continue
            pat = r["count"][kind] if kind else r["count_re"]
            cnt = len(re.findall(pat, read(tgt)))
            put(pos_key, cnt, "%s 内 %s" % (href, (kind or "qa-card")))
        return errs

    def r_block_count_same_file(r):
        errs = []
        p = os.path.join(root, r["file"])
        if not os.path.isfile(p):
            return ["规则 %s 文件不存在" % r["id"]]
        t = read(p)
        kr = re.compile(r["key_re"])
        for pos_key in [k for k in _pos_keys() if kr.match(k)]:
            nn = int(kr.match(pos_key).groups()[-1])
            anchor = (r["block_re"] % nn) if "%" in r["block_re"] else r["block_re"]
            bm = re.search(re.escape(anchor), t)
            if not bm:
                errs.append("规则 %s：键 %s 找不到块 %s" % (r["id"], pos_key, anchor))
                continue
            rest = t[bm.end():]
            nx = re.search(re.escape(r["next_re"]), rest) if r.get("next_re") else None
            blk = rest[:nx.start()] if nx else rest
            cnt = len(re.findall(r["count_re"], blk))
            put(pos_key, cnt, "%s 块内 %s 数" % (r["file"].split("/")[-1], r["count_re"][:20]))
        return errs

    def r_host_page_cards(r):
        errs = []
        for it in r["items"]:
            p = os.path.join(root, it["file"])
            if not os.path.isfile(p):
                errs.append("host_page_cards：文件不存在 %s" % it["file"])
                continue
            put(it["key"], len(re.findall(it["count_re"], read(p))),
                "%s 的 qa-card 数" % it["file"].split("/")[-1])
        return errs

    def r_sum(r):
        errs = []
        cands = set("struct." + k for k in FLAT)
        cands |= set((ssot.get("counts") or {}).keys())
        for it in r["items"]:
            tp = re.compile(it["terms"])
            tot = 0
            used = 0
            for cand in sorted(cands):
                if not tp.match(cand):
                    continue
                v = truth.get(cand)
                if v is None:
                    v = lookup(cand)
                if isinstance(v, int):
                    tot += v
                    used += 1
            if used == 0:
                errs.append("sum 规则：%s 的 terms 未命中任何键" % it["key"])
                continue
            put(it["key"], tot, "Σ%d 个键（%s）" % (used, it["terms"][:34]))
        return errs

    def r_file_count(r):
        errs = []
        for it in r["items"]:
            n = len([p for p in glob.glob(os.path.join(root, it["glob"]))
                     if not any(os.path.relpath(p, root).startswith(e) for e in EXCLUDE)])
            if n == 0:
                errs.append("file_count 规则：%s 的 glob 未命中文件" % it["key"])
            put(it["key"], n, "glob %s" % it["glob"])
        return errs

    def r_derived(r):
        """结构性派生计数：真源是 guard.derived.items 里声明的 region + count。"""
        items = (G.get(r.get("from") or "derived") or {}).get("items") or []
        if not items:
            return ["derived 规则 %s：guard.derived.items 为空" % r["id"]]
        errs = []
        for it in items:
            p = os.path.join(root, it["file"])
            if not os.path.isfile(p):
                errs.append("derived：文件不存在 %s" % it["file"])
                continue
            t = read(p)
            ms = list(re.finditer(it["region"], t, re.S))
            if len(ms) != 1:
                errs.append("derived %s：region 命中 %d 次（须恰好 1 次）" % (it["key"], len(ms)))
                continue
            put(it["key"], len(re.findall(it["count"], ms[0].group(0))),
                "derived 块内 %s" % it["count"][:26])
        return errs

    def r_dom_count(r):
        """单值 DOM 计数：直接数宿主页内某结构元素个数。"""
        errs = []
        for it in r["items"]:
            p = os.path.join(root, it["file"])
            if not os.path.isfile(p):
                errs.append("dom_count：文件不存在 %s" % it["file"])
                continue
            put(it["key"], len(re.findall(it["count_re"], read(p))),
                "%s 的 %s" % (it["file"].split("/")[-1], it["count_re"][:26]))
        return errs

    def r_page_diff(r):
        """某个页面自身的难度分布（与 cards_by_link 不同：不经过索引页链接）。"""
        errs = []
        for it in r["items"]:
            p = os.path.join(root, it["file"])
            if not os.path.isfile(p):
                errs.append("page_diff：文件不存在 %s" % it["file"])
                continue
            t = read(p)
            for lvl, pat in sorted((r.get("levels") or {}).items()):
                put(it["prefix"] + "." + lvl, len(re.findall(pat, t)),
                    "%s 的 difficulty-%s 数" % (it["file"].split("/")[-1], lvl))
        return errs

    def r_layer_sum(r):
        """层合计：层归属读 guard.layers.range，键表读 guard.layers.sum_keys。"""
        layers = G.get(r.get("from") or "layers") or []
        if not layers:
            return ["layer_sum 规则 %s：guard.%s 为空" % (r["id"], r.get("from") or "layers")]
        errs = []
        for L in layers:
            lo, hi = L["range"]
            tot, miss = 0, []
            for n in range(lo, hi + 1):
                k = "struct.meth.group_%d" % n
                v = truth.get(k)
                if v is None:
                    v = lookup(k)
                if not isinstance(v, int):
                    miss.append(k)
                    continue
                tot += v
            if miss:
                errs.append("layer_sum：层 %s(%s) 的成员未求出真值 %s" % (L["id"], L["label"], miss))
            for k in L.get("sum_keys") or []:
                put("struct." + k, tot, "Σ 层 %s.range=%s 的 M 组卡数" % (L["id"], L["range"]))
        return errs

    def r_sum_equals(r):
        """不变式：**展示值**分项之和 == 该组真值合计（题数）。

        分项取 SSOT / 页面**展示值**，合计取**真值**（题数）。
        —— 若两边都用重算真值，检查退化成恒真（`truth == truth`），
        展示值写错或整项缺展示位都抓不到（2026-09-21 probe 用例 C 实测的假绿）。
        对比即可发现：① 分项陈旧（和 < 题数）；② 整项缺展示位（该分项键在 SSOT 中不存在 → 记「缺位」）。
        """
        errs = []
        pr, tr = re.compile(r["parts_re"]), re.compile(r["total_re"])
        universe = set("struct." + k for k in FLAT) | set(truth)
        groups, totals = {}, {}
        for k in universe:
            m = pr.match(k)
            if m:
                groups.setdefault(m.group(1), set()).add(k)
            m2 = tr.match(k)
            if m2:
                totals[m2.group(1)] = k
        if not groups:
            errs.append("不变式 %s 的 parts_re 未命中任何键" % r["id"])
        for g, ks in sorted(groups.items()):
            if g not in totals:
                errs.append("不变式 %s：组 %s 缺合计键（total_re 未命中 " % (r["id"], g) + g + "）")
                continue
            tk = totals[g]
            tv = truth.get(tk)
            if tv is None:
                tv = ssot_val(tk)
            if tv is None:
                continue
            s, shown = 0, []
            for k in sorted(ks):
                v = ssot_val(k)
                if v is None:
                    shown.append("%s=缺展示位" % k.split(".")[-1])
                    continue
                s += v
                shown.append("%s=%d" % (k.split(".")[-1], v))
            if s != tv:
                errs.append("不变式 %s：%s 展示值分项之和 %d ≠ 真值合计 %s=%d（分项 %s）"
                            % (r["id"], g, s, tk, tv, ", ".join(shown)))
        return errs

    _POS_CACHE = [None]

    def _pos_keys():
        if _POS_CACHE[0] is None:
            _POS_CACHE[0] = []
            for p in ssot.get("positions") or []:
                k = p.get("key")
                if k and k not in _POS_CACHE[0]:
                    _POS_CACHE[0].append(k)
        return _POS_CACHE[0]

    DISPATCH = {
        "dom_scan": r_dom_scan,
        "cards_by_link": r_cards_by_link,
        "block_count_same_file": r_block_count_same_file,
        "host_page_cards": r_host_page_cards,
        "sum": r_sum,
        "file_count": r_file_count,
        "derived": r_derived,
        "dom_count": r_dom_count,
        "page_diff": r_page_diff,
        "layer_sum": r_layer_sum,
        "sum_equals": r_sum_equals,
    }

    fatal = []
    for r in RULES:
        fn = DISPATCH.get(r.get("type"))
        if not fn:
            fatal.append("未知真源类型 «%s»（规则 %s）" % (r.get("type"), r.get("id")))
            continue
        fatal += fn(r)

    # ---------- 不变式 ----------
    INV = (SRC.get("invariants") or [])
    inv_fail = []
    for r in INV:
        fn = DISPATCH.get(r.get("type"))
        if not fn:
            inv_fail.append("未知不变式类型 «%s»（%s）" % (r.get("type"), r.get("id")))
            continue
        inv_fail += fn(r)

    # ---------- A) 真源完备性 ----------
    rule_res = [(re.compile(r["key_re"]), r["id"]) for r in RULES if r.get("key_re")]
    man_res = [(re.compile(m["key_re"]), m) for m in MANUAL if m.get("key_re")]

    uncovered = []
    for k in _pos_keys():
        if any(rx.match(k) for rx, _ in rule_res):
            continue
        hit = None
        for rx, m in man_res:
            if rx.match(k):
                hit = m
                break
        if hit:
            continue
        uncovered.append(k)

    # 「声明了但没算出真值」= 假声明（正则没命中 / 规则写错），同样必须暴露
    noverify = [k for k in _pos_keys()
                if k not in truth and any(rx.match(k) for rx, _ in rule_res)]

    # ---------- A2) 反向完备性：有真源必有展示位 ----------
    # 每个求出真值的键都必须有已登记的 position —— 否则「真源」没有展示位可证，
    # 等于声明了一个页面上根本不存在的计数（probe 用例 H 守这条）。
    _pk = set(_pos_keys())
    orphan = [k for k in sorted(truth) if k not in _pk]

    # ---------- B) 真值校验 ----------
    # 合并 SSOT 里 positions 的 DOM 显示值（规则执行中已采集的更新之）
    for p in ssot.get("positions") or []:
        k = p.get("key")
        if not k or k in kbcount:
            continue
        kbcount[k] = (p["id"], None)
        # 从登记文件实测 DOM 值
        f = os.path.join(root, p["file"])
        if os.path.isfile(f):
            m = re.search(p["pattern"], read(f))
            if m:
                for g in m.groups():
                    if g and g.isdigit():
                        kbcount[k] = (p["id"], int(g))
                        break

    mismatch = []
    checked = 0
    for k, tv in sorted(truth.items()):
        sv = lookup(k)
        pid, dv = kbcount.get(k, (None, None))
        checked += 1
        if sv is None:
            mismatch.append("%-58s 真值=%-5s 但 SSOT 无此键（规则 %s）" %
                            (k, tv, evid.get(k, "")[:20]))
            continue
        if sv != tv:
            mismatch.append("%-58s SSOT=%-5s ≠ 真值=%-5s (%s)" % (k, sv, tv, evid.get(k, "")[:34]))
        elif dv is not None and dv != tv:
            mismatch.append("%-58s DOM=%-5s ≠ 真值=%-5s 位=%s" % (k, dv, tv, pid))

    # ---------- 输出 ----------
    if a.list:
        for k in sorted(truth):
            print("  %-58s 真值=%-5s %s" % (k, truth[k], evid.get(k, "")))
        print()

    if not a.quiet:
        print("规则 %d 条 · 不变式 %d 条 · 人工锚定 %d 条 · 求出真值 %d 个键 · 已登记 position 键 %d 个"
              % (len(RULES), len(INV), len(MANUAL), len(truth), len(_pos_keys())))

    ok = True
    # 门禁不得藏发现：默认全量输出（`--max N` 可截断，仅用于人类阅读）
    cap = a.max if a.max and a.max > 0 else 10 ** 6
    if fatal:
        ok = False
        for x in fatal[:cap]:
            print("FAIL [真源配置]", x)
    if DUPS:
        ok = False
        for x in DUPS[:cap]:
            print("FAIL [键路径冲突]", x)
        print("FAIL [键路径冲突] 共 %d 处：同一逻辑键在 SSOT 写了两个表示（扁平点分键 + 嵌套键），"
              "展平后互相覆盖 —— 删掉嵌套那份，只保留扁平键" % len(DUPS))
    if CONFLICT:
        ok = False
        for x in CONFLICT[:cap]:
            print("FAIL [真源冲突]", x)
        print("FAIL [真源冲突] 共 %d 处：同一键被多条声明求出不同值（双写，须合并为单一声明）"
              % len(CONFLICT))
    if inv_fail:
        ok = False
        for x in inv_fail[:cap]:
            print("FAIL [不变式]", x)
        print("FAIL [不变式] 共 %d 处：分项与合计不符（多为缺展示位或分项陈旧）" % len(inv_fail))
    if uncovered:
        ok = False
        for k in uncovered[:cap]:
            print("FAIL [未声明真源]", k)
        print("FAIL [未声明真源] 共 %d 个键没有任何规则/人工锚定覆盖 —— "
              "新增计数必须在 SSOT guard.sources 声明真源（见 conventions.md §5.1.4）" % len(uncovered))
    if noverify:
        ok = False
        for k in noverify[:cap]:
            print("FAIL [声明未生效]", k)
        print("FAIL [声明未生效] 共 %d 个键被某条规则的正则声明覆盖，但该规则未求出其真值"
              "（正则写错或规则未实现）" % len(noverify))
    if orphan:
        ok = False
        for k in orphan[:cap]:
            print("FAIL [无展示位]", k)
        print("FAIL [无展示位] 共 %d 个键求出了真值，但没有对应的已注册 position —— "
              "真源必须配展示位（否则是「声明了却没人看得见的计数」）" % len(orphan))
    if mismatch:
        ok = False
        for x in mismatch[:cap]:
            print("FAIL [真值不符]", x)
        print("FAIL [真值不符] 共 %d 处：SSOT/统计值与真源实测不一致（先查内容，再改 SSOT）" % len(mismatch))

    if ok:
        print("✅ 真源审计通过：%d 个键全部有真源声明，SSOT 值 = 真源实测值 = DOM 显示值；"
              "%d 条不变式成立；无真源冲突。" % (checked, len(INV)))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
