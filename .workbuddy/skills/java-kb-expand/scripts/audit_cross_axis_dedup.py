#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""java-kb-expand · 跨轴卡片去重门禁
========================================
检测「逐句复制」与「换几个词但整句照搬」——6-gram Jaccard 会低估后者，
故同时统计：完全相同句数、近似句数、全文 shingle Jaccard。

配置全部来自 SSOT `guard.cross_axis_dedup`（阈值 / 扫描范围 / 豁免台账），
项目根由 `_kbroot.require_root(__file__)` 推导，脚本内不写死绝对路径、
不写死编码子集、不提供关闭开关。

退出码：0=PASS / 1=FAIL / 3=缺夹具（配置或扫描对象缺失）。
"""
import os, sys, re, json, glob, html, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kbroot import require_root

BASE = require_root(__file__)
SSOT = os.path.join(BASE, "docs", "kb-counts.json")
TAG = re.compile(r"<[^>]+>")


def load_cfg():
    if not os.path.isfile(SSOT):
        print("FAIL [夹具] 缺 docs/kb-counts.json")
        return None
    cfg = json.load(open(SSOT, encoding="utf-8"))
    g = cfg.get("guard", {}).get("cross_axis_dedup")
    if not g:
        print("FAIL [夹具] 缺 guard.cross_axis_dedup 配置")
        return None
    required = ("scan", "exclude", "min_sentence_len", "template_doc_freq", "focus_ids",
                "ngram", "coarse_ngram", "coarse_min_shared", "high_freq_gram_cap",
                "near_threshold", "exact_fail", "near_fail", "jaccard_fail", "exempt")
    miss = [k for k in required if k not in g]
    if miss:
        print(f"FAIL [夹具] 配置缺字段：{miss}")
        return None
    return g


def scan_files(g):
    out = []
    for pat in g["scan"]:
        for p in glob.glob(os.path.join(BASE, pat)):
            rel = os.path.relpath(p, BASE).replace(os.sep, "/")
            if any(rel.startswith(e) for e in g["exclude"]):
                continue
            out.append(p)
    return sorted(set(out))


def text_of(s):
    s = TAG.sub(" ", re.sub(r"<br\s*/?>", " ", s))
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def extract_cards(path):
    t = open(path, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<div class="content-card"([^>]*)>', t):
        idm = re.search(r'\bid="([^"]+)"', m.group(1))
        cid = idm.group(1) if idm else None
        if not cid:
            continue
        s = m.start(); d = 0; i = s; end = None
        while i < len(t):
            if t.startswith("<div", i):
                d += 1; i += 4
            elif t.startswith("</div", i):
                d -= 1
                if d == 0:
                    end = i + 6; break
                i += 5
            else:
                i += 1
        if end is None:
            continue
        # 整块文本（含标题与全部层），避免嵌套 div 导致层提取截断；
        # 短层标题/徽标会被 min_sentence_len 自然过滤。
        body = text_of(t[s:end])
        out.append({"id": cid, "file": os.path.relpath(path, BASE).replace(os.sep, "/"), "text": body})
    return out


def sents_of(txt, minlen):
    out = []
    for s in re.split(r"[。！？；\n]", txt):
        s = re.sub(r"[^\w\u4e00-\u9fff]", "", s)
        if len(s) >= minlen:
            out.append(s)
    return out


def grams_of(txt, n):
    t = re.sub(r"[^\w\u4e00-\u9fff]", "", txt)
    return {t[i:i + n] for i in range(max(0, len(t) - n + 1))}


def sh_of(s, n):
    return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}


def pair_counter(inv, cap):
    c = collections.Counter()
    for _, lst in inv.items():
        if len(lst) > cap:
            continue
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                c[(lst[i], lst[j])] += 1
    return c


def main():
    as_json = "--json" in sys.argv
    g = load_cfg()
    if g is None:
        return 3
    for e in g["exempt"]:
        if not isinstance(e, dict) or not e.get("reason") or not e.get("a") or not e.get("b"):
            print("FAIL [豁免台账] 每条豁免须含 a / b / reason，当前不合规：%s" % e)
            return 1
    files = scan_files(g)
    if not files:
        print("FAIL [夹具] 扫描范围内无 HTML 文件")
        return 3

    cards = []
    for p in files:
        cards.extend(extract_cards(p))
    if len(cards) < 2:
        print(f"FAIL [夹具] 卡片数不足：{len(cards)}")
        return 3

    # 结构性兜底：全库 doc_freq 过高的句子判定为模板套话（如 G 篇卡片共用提纲句），
    # 从句子集合与全文 shingle 中一并剔除，避免把历史模板误报成内容复制。
    # 阈值来自 SSOT，不枚举卡号、不写死编码子集，新增卡自动纳入检测。
    focus = set(g["focus_ids"])
    found = {c["id"] for c in cards}
    missing_focus = sorted(focus - found)
    if missing_focus:
        print(f"FAIL [配置漂移] focus_ids 中 {len(missing_focus)} 张卡未命中站点：{missing_focus}")
        return 1

    sents_all = [sents_of(c["text"], g["min_sentence_len"]) for c in cards]
    doc_freq = collections.Counter()
    for ss in sents_all:
        for s in set(ss):
            doc_freq[s] += 1
    template = {s for s, n in doc_freq.items() if n >= g["template_doc_freq"]}
    sents = [[s for s in ss if s not in template] for ss in sents_all]
    full_g = [grams_of("".join(ss), g["coarse_ngram"]) for ss in sents]
    sent_sh = [[sh_of(s, g["ngram"]) for s in ss] for ss in sents]

    sent_inv = collections.defaultdict(list)
    for i, ss in enumerate(sents):
        for s in set(ss):
            sent_inv[s].append(i)
    gram_inv = collections.defaultdict(list)
    for i, gg in enumerate(full_g):
        for x in gg:
            gram_inv[x].append(i)

    exact_c = pair_counter(sent_inv, g["high_freq_gram_cap"])
    coarse_c = pair_counter(gram_inv, g["high_freq_gram_cap"])
    cands = set(exact_c) | {k for k, v in coarse_c.items() if v >= g["coarse_min_shared"]}

    exempt = set()
    for e in g["exempt"]:
        exempt.add(frozenset((e["a"], e["b"])))

    bad, baseline = [], []
    for (i, j) in cands:
        a, b = cards[i], cards[j]
        if frozenset((a["id"], b["id"])) in exempt:
            continue
        inter = len(full_g[i] & full_g[j])
        union = len(full_g[i]) + len(full_g[j]) - inter
        jac = inter / union if union else 0.0
        exact = exact_c.get((i, j), 0)
        near = 0
        if exact >= 1 or jac >= 0.12:
            for sa in sent_sh[i]:
                for sb in sent_sh[j]:
                    it = len(sa & sb)
                    if it and it / (len(sa) + len(sb) - it) >= g["near_threshold"]:
                        near += 1
                        break
        if exact >= g["exact_fail"] or near >= g["near_fail"] or jac >= g["jaccard_fail"]:
            rec = {"a": a["id"], "b": b["id"], "file_a": a["file"], "file_b": b["file"],
                   "exact": exact, "near": near, "jaccard": round(jac, 3)}
            # 门禁只阻断「本轮新增/改动卡」引入的复制；历史基线（两卡均不在 focus）
            # 仍完整扫描并 WARN 可见，避免因枚举漏登而完全失察。
            (bad if (a["id"] in focus or b["id"] in focus) else baseline).append(rec)
    bad.sort(key=lambda x: (-x["exact"], -x["jaccard"]))
    baseline.sort(key=lambda x: (-x["exact"], -x["jaccard"]))

    result = {"cards": len(cards), "files": len(files), "candidates": len(cands),
              "focus_count": len(focus), "violations": bad,
              "baseline_warnings": baseline, "pass": not bad}
    if as_json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"扫描 {len(files)} 个 HTML / {len(cards)} 张卡 / {len(cands)} 个候选对 / focus {len(focus)} 张")
        if bad:
            print(f"FAIL [跨轴去重] 本轮变更卡违规 {len(bad)} 对（点名不截断）：")
            for x in bad:
                print(f"  [{x['a']}] <-> [{x['b']}] 同句={x['exact']} 近似={x['near']} "
                      f"Jaccard={x['jaccard']}  ({x['file_a']} / {x['file_b']})")
        else:
            print("PASS 跨轴去重：本轮变更卡与全库无逐句复制 / 换词照搬")
        if baseline:
            print(f"WARN 历史基线（非本轮变更，不阻断）{len(baseline)} 对；示例：")
            for x in baseline[:5]:
                print(f"  [{x['a']}] <-> [{x['b']}] 同句={x['exact']} Jaccard={x['jaccard']}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
