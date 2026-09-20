#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向验证「导图 map-card ↔ Mermaid 节点」门禁（check_mind_mermaid.py）。
=================================================================
为什么需要：门禁若恒真（永远 PASS）形同虚设。2026-09-20 把该门禁的取标签范围从
「只认 flowchart 的 `["…"]` 方括号标签」放宽为「方括号标签 + mindmap 裸文本行」，
放宽后**必须**证明它仍能抓出真缺失，否则等于把门禁改废。

与其它 probe 的差异：本探针**不写项目真实文件、不建沙箱目录树**，而是把门禁源码里的
`MI` 常量在内存里重定向到一个 `tempfile` 镜像目录（`exec` + 打补丁），因此无还原动作、
零污染链风险；同时天然规避「脚本按自身层级误解析项目根」的坑。

五轮场景（每轮构造一份 mind-14 副本；断言出口码，FAIL/PASS 两侧都要覆盖）：
  轮 A  原样副本                                → exit 0（当前项目基线，防误杀）
  轮 B  一条卡标题**整条替换**成图上绝无的文案     → exit 1（标题级判定有效）
  轮 C  新增一条两块图都没有的 `<summary>`        → exit 1（守住 2026-09-15 原盲区）
  轮 D  只抹掉 flowchart 节点、mindmap 保留        → exit 0（本轮放宽**有意**生效）
  轮 E  flowchart 与 mindmap 节点都抹掉           → exit 1（两块都缺才算缺）
  轮 A 通过但轮 B/C/E 未 FAIL ⇒ 门禁恒真；轮 D FAIL ⇒ 放宽未生效（改回只认方括号）。

用法：python3 scripts/probe_mind_mermaid_gate.py
退出码：0 = 各轮均符合预期；1 = 任一不符。
"""
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile

B = '/Users/chenjunbing/Develop/Project/Personal/Java Spring AI'
GATE = B + '/.workbuddy/skills/java-kb-expand/scripts/check_mind_mermaid.py'
SRC_PAGE = B + '/java-architect-interview-mind/mind-14-databases.html'
PAGE = 'mind-14-databases.html'

FLOW_NODE = '["慢 SQL 值班动作"]'        # C14.13 的 flowchart 节点
MIND_LINE = 'C14.13 慢 SQL 值班动作'      # C14.13 的 mindmap 裸文本行
MIRROR = 'java-architect-interview-mind'
ANCHOR = "MI = os.path.join(BASE, 'java-architect-interview-mind')"


def run_gate(tmpdir):
    """在内存里把门禁的 MI 重定向到 tmpdir 镜像后执行，返回 (exit_code, stdout)。"""
    src = open(GATE, encoding='utf-8').read()
    if ANCHOR not in src:
        raise AssertionError('门禁常量形态已变，probe 需更新重定向锚点：' + ANCHOR)
    src = src.replace(ANCHOR, 'MI = %r' % os.path.join(tmpdir, MIRROR))
    argv_bak, sys.argv = sys.argv, ['check_mind_mermaid.py', '-v']
    buf = io.StringIO()
    code = 0
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(src, GATE, 'exec'), {'__name__': '__main__', '__file__': GATE})
    except SystemExit as e:
        code = e.code or 0
    finally:
        sys.argv = argv_bak
    return code, buf.getvalue()


def main():
    tmp = tempfile.mkdtemp(prefix='probe_mind_mermaid_')
    try:
        mi = os.path.join(tmp, MIRROR)
        os.makedirs(mi)
        page = os.path.join(mi, PAGE)
        orig = open(SRC_PAGE, encoding='utf-8').read()
        results = []

        def case(label, html, expect_fail):
            if html == orig and expect_fail:
                raise AssertionError('%s：缺陷样例未实际改动' % label)
            open(page, 'w', encoding='utf-8').write(html)
            code, out = run_gate(tmp)
            ok = (code != 0) == expect_fail
            results.append(ok)
            print('%-40s exit=%s 期望%-4s → %s'
                  % (label, code, 'FAIL' if expect_fail else 'PASS', 'OK' if ok else '不符 <<<'))
            for ln in out.strip().splitlines():
                if ln.strip():
                    print('      ' + ln)
            print()

        case('A. 原样副本（防误杀）', orig, False)

        b = re.sub(r'(<summary>C14\.01 )[^<]*', r'\1ZZQ全新文案XYZ', orig, count=1)
        assert b != orig, 'B：未命中替换'
        case('B. 整条替换卡标题为图外文案', b, True)

        c = orig.replace('<summary>C14.01 ',
                         '<summary>C14.99 ZZQ全新卡片ABC</summary>\n        <summary>C14.01 ', 1)
        assert c != orig, 'C：未命中插入'
        case('C. 新增一条两块图都无的卡', c, True)

        d = orig.replace(FLOW_NODE, '["占位节点"]', 1)
        assert d != orig, 'D：未命中 flowchart 节点'
        case('D. 只抹 flowchart 节点（mindmap 保留）', d, False)

        e = d.replace(MIND_LINE, 'C14.13 占位节点', 1)
        assert e != d, 'E：未命中 mindmap 行'
        case('E. flowchart 与 mindmap 节点都抹掉', e, True)

        print('probe_mind_mermaid_gate 结果：%d/%d 轮符合预期 %s'
              % (sum(results), len(results), '✅' if all(results) else '❌'))
        return 0 if all(results) else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
