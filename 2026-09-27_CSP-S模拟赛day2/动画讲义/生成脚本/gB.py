# -*- coding: utf-8 -*-
import subprocess, os
from common import *

SOL = os.path.join(HERE, '..', 'sol')


def solve_trace(strs):
    """真实跑一遍 B 的增量算法，逐层记录。返回 events 和每个 i 的答案。"""
    ch, cnt = [{}], [0]
    mx, f = {}, {}
    ans = 0
    ev, outs = [], []
    for i, s in enumerate(strs, 1):
        ans += (0 ^ i)
        f[i] = 0
        u = 0
        path = [0]
        for d in range(0, len(s) + 1):
            if d > 0:
                c = s[d - 1]
                if c not in ch[u]:
                    ch.append({}); cnt.append(0)
                    ch[u][c] = len(ch) - 1
                u = ch[u][c]
                path.append(u)
            cnt[u] += 1
            e = {'i': i, 's': s, 'd': d, 'u': u, 'path': list(path), 'cnt': list(cnt), 'mx_old': mx.get(d, 0),
                 'fchg': None, 'ans_before': ans, 'new': d == 0}
            if cnt[u] > mx.get(d, 0):
                mx[d] = cnt[u]
                j = mx[d]
                if d > f.get(j, 0):
                    old = f.get(j, 0)
                    ans -= (old ^ j)
                    f[j] = d
                    ans += (d ^ j)
                    e['fchg'] = (j, old, d)
            e['mx'] = dict(mx)
            e['f'] = dict(f)
            e['ans'] = ans
            e['children'] = [dict(x) for x in ch]
            ev.append(e)
        outs.append(ans)
    return ev, outs


def node_label(children):
    lab = {0: ''}
    stack = [0]
    while stack:
        u = stack.pop()
        for c, v in children[u].items():
            lab[v] = lab[u] + c
            stack.append(v)
    return lab


def draw_state(e, pos, maxd, nmax):
    lab = node_label(e['children'])
    b = []
    # 字典树
    b.append(Tx(10, 14, '字典树（圈里 = 经过的串数）', 'ti', 'start'))
    for u, kids in enumerate(e['children']):
        for c, v in kids.items():
            x1, y1 = pos[lab[u]]
            x2, y2 = pos[lab[v]]
            b.append(L(x1, y1, x2, y2, 'ed'))
    for u in range(len(e['children'])):
        x, y = pos[lab[u]]
        cls = 'nd'
        if u == e['u']:
            cls = 'nd nd-y'
        elif u in e['path']:
            cls = 'nd nd-b'
        b.append(C(x, y, 16, cls))
        b.append(Tx(x, y + 5, str(e['cnt'][u]), 'tvs'))
        if lab[u]:
            b.append(Tx(x + 22, y - 18, lab[u], 'ti', 'middle'))
    # mx 柱子
    bx0, by0 = 250, 150
    b.append(Tx(bx0, 14, 'mx[d]', 'ti', 'start'))
    for d in range(0, maxd + 1):
        v = e['mx'].get(d, 0)
        hgt = v * (110 / nmax)
        cls = 'bar-up' if (d == e['d'] and e['mx_old'] != v) else 'bar'
        x = bx0 + d * 34
        b.append(R(x, by0 - hgt, 26, hgt if hgt > 0 else 0.1, cls, 2))
        b.append(Tx(x + 13, by0 - hgt - 4, str(v), 'ti'))
        b.append(Tx(x + 13, by0 + 14, 'd=%d' % d, 'ti'))
    # f 表
    tx0 = 250 + (maxd + 1) * 34 + 20
    b.append(Tx(tx0, 14, 'f[j]', 'ti', 'start'))
    b.append(Tx(tx0, 42, 'j', 'ti', 'start'))
    b.append(Tx(tx0, 72, 'f', 'ti', 'start'))
    b.append(Tx(tx0, 102, 'xor', 'ti', 'start'))
    cw = 30
    for j in range(1, nmax + 1):
        x = tx0 + 26 + (j - 1) * cw
        if j > e['i']:
            b.append(Tx(x + cw / 2 - 2, 42, str(j), 'ti tso'))
            continue
        fj = e['f'].get(j, 0)
        chg = e['fchg'] is not None and e['fchg'][0] == j
        newj = e['new'] and j == e['i']
        b.append(Tx(x + cw / 2 - 2, 42, str(j), 'ti'))
        b.append(R(x, 52, cw - 4, 28, 'bx bx-y' if chg else ('bx bx-in' if newj else 'bx'), 3))
        b.append(Tx(x + cw / 2 - 2, 72, str(fj), 'tvs'))
        b.append(Tx(x + cw / 2 - 2, 102, str(fj ^ j), 'tvs ' + ('trd' if chg else '')))
    b.append(Tx(tx0, 140, '和 = %d' % e['ans'], 'tlabb', 'start'))
    W = int(tx0 + 26 + nmax * cw + 10)
    return svg(W, 190, b)


def note_for(e):
    i, s, d = e['i'], e['s'], e['d']
    parts = []
    if e['new']:
        parts.append('插入第 %d 个串 <b>%s</b>。先把新的一项 j = %d 加进和里：f[%d] 先是 0，0 xor %d = %d，和 %d → <b>%d</b>。' % (
            i, s, i, i, i, i, e['ans_before'] - i, e['ans_before']))
    where = '根' if d == 0 else '第 %d 层的结点“%s”' % (d, s[:d])
    parts.append('走到%s，经过它的串数变成 %d。' % (where, e['cnt'][e['u']]))
    if e['mx_old'] != e['mx'].get(d, 0):
        m1 = e['mx'][d]
        parts.append('这一层的最大值 mx[%d]：%d → <b>%d</b>，所以只有 <b>j = %d</b> 这一格可能变。' % (d, e['mx_old'], m1, m1))
        if e['fchg']:
            j, old, new = e['fchg']
            parts.append('f[%d] = max(%d, %d) = <b>%d</b>，变了：和先减 %d xor %d = %d，再加 %d xor %d = %d，和 = <b>%d</b>。' % (
                j, old, d, new, old, j, old ^ j, new, j, new ^ j, e['ans']))
        else:
            j = e['mx'][d]
            parts.append('但 f[%d] 本来就 ≥ %d，不用改。' % (j, d))
    else:
        parts.append('mx[%d] 还是 %d，<b>没有一格要改</b>。' % (d, e['mx'].get(d, 0)))
    if d == len(s):
        parts.append('这个串插完，输出 <b>%d</b>。' % e['ans'])
    return ''.join(parts)


def b_insert(name, title, strs, expected, pos, cap):
    ev, outs = solve_trace(strs)
    assert outs == expected, (outs, expected)
    maxd = max(len(s) for s in strs)
    nmax = len(strs)
    frames = [(draw_state(e, pos, maxd, nmax), note_for(e)) for e in ev]
    return fp(name, title, frames, cap), ev


def b_stair(strs):
    """样例 2 插完 8 个串以后，mx 和 f 是同一张图的两种读法。"""
    ev, outs = solve_trace(strs)
    last = ev[-1]
    mx = last['mx']
    maxd = max(mx)
    n = len(strs)
    fr = []
    X0, Y0, uw, uh = 70, 250, 70, 26

    def base():
        b = [L(X0 - 10, Y0, X0 + (maxd + 1) * uw + 20, Y0, 'ln s-ink w-m'), L(X0 - 10, Y0, X0 - 10, Y0 - n * uh - 10, 'ln s-ink w-m')]
        for j in range(1, n + 1):
            b.append(Tx(X0 - 18, Y0 - j * uh + 18, str(j), 'ti', 'end'))
        b.append(Tx(X0 - 40, Y0 - n * uh - 16, '串数', 'ti', 'start'))
        for d in range(0, maxd + 1):
            v = mx[d]
            b.append(R(X0 + d * uw, Y0 - v * uh, uw - 10, v * uh, 'bar', 2))
            b.append(Tx(X0 + d * uw + (uw - 10) / 2, Y0 + 18, 'd=%d' % d, 'ti'))
            b.append(Tx(X0 + d * uw + (uw - 10) / 2, Y0 - v * uh - 6, 'mx=%d' % v, 'ti'))
        return b
    fr.append((svg(560, 280, base()), '样例 2 的 8 个串全部插完。每根柱子是一层：<b>mx[d] = 第 d 层经过串数最多的那个结点</b>。第 0 层是根，8 个串都经过它；第 1 层 a 和 b 各有 4 个；第 2 层最多 2 个。'))
    tot = 0
    for j in range(1, n + 1):
        fj = max([d for d in range(maxd + 1) if mx[d] >= j] + [0])
        tot += fj ^ j
        b = base()
        b.append(L(X0 - 10, Y0 - j * uh + uh / 2, X0 + (maxd + 1) * uw + 10, Y0 - j * uh + uh / 2, 'hline'))
        for d in range(0, maxd + 1):
            if mx[d] >= j:
                b.append(R(X0 + d * uw, Y0 - mx[d] * uh, uw - 10, mx[d] * uh, 'bar-up' if d == fj else 'bar', 2))
        b.append(Tx(X0 + (maxd + 1) * uw + 30, Y0 - j * uh + uh / 2 + 5, 'f[%d] = %d' % (j, fj), 'tlabb', 'start'))
        fr.append((svg(560, 280, b), '要选 <b>j = %d</b> 个串：在高度 %d 画一条横线，<b>最右边够得着这条线的柱子</b>是第 %d 层，所以 f[%d] = %d。f xor j = %d，累计和 = %d。' % (
            j, j, fj, j, fj, fj ^ j, tot)))
    assert tot == outs[-1]
    fr.append((svg(560, 280, base()), '8 项加起来是 <b>%d</b>，就是样例 2 最后一行的输出。<b>竖着看柱子是 mx，横着切一刀读出来的就是 f</b>，它们是同一张图。所以柱子只长高一格时，只有“刚好碰到新高度那一刀”的 f 会变。' % tot))
    return fp('b_stair', '动画 B1 · mx 和 f 是同一张图的两种读法（样例 2 插完以后）', fr, '柱子高度就是真实算法跑完样例 2 以后的 mx 数组。')


def build():
    s1 = ['a', 'ab', 'abc', 'abcd']
    s2 = ['ab', 'b', 'ba', 'ab', 'aa', 'ba', 'a', 'bb']
    pos1 = {'': (110, 32), 'a': (110, 66), 'ab': (110, 100), 'abc': (110, 134), 'abcd': (110, 168)}
    pos2 = {'': (120, 40), 'a': (65, 100), 'b': (175, 100), 'aa': (30, 160), 'ab': (100, 160), 'ba': (145, 160), 'bb': (210, 160)}
    h = []
    h.append('<h2 id="B">B 🧶　<span class="bdg bdg-w">0 分，没交</span><span class="kaodian">字典树 · 增量维护</span></h2>')
    h.append('<div class="method"><b>一句话题意：</b>对每个 i，f(i, j) = 从前 i 个串里选 j 个的最长公共前缀。输出 ∑ⱼ f(i, j) xor j。</div>')
    h.append('<div class="mind real">11:45 <span class="qq">“我给每一层求个最大值。”</span>11:48 <span class="qq">“插入一个串，这条路径上全加一，如果这是最大值，上面的每一层都要取一遍最大值。”</span>11:49 <span class="qq">“现在我能高速算出来每一个，但这复杂度差得远了去了。”</span>12:45 <span class="qq">“你不挨个算，你怎么能做到的呢？”</span><br>赛后你又说：<span class="qq">“我解决不了一个问题：我不算出来 f，我是怎么能求出来最后答案的？”</span></div>')
    h.append('<p>前两句是正解的前一半，完全对。卡住你的是后两句。先把这个问题说准：</p>')
    h.append('<div class="renhua"><b>每个 f 都算出来了，都存在数组 f[1..i] 里，只是不重新算。</b>你的做法是每插入一个串，把 j = 1..i 全部重算、再加一遍 xor，一共 1 + 2 + … + n ≈ n²/2 次。正解是：插入一个串以后，<b>f 数组里只有很少几格会变</b>；只改这几格，改的时候把和也跟着改（先减掉旧的 f xor j，再加上新的）。没变的格子一格都不碰，它们对和的贡献原样留着。<br><b>和是一直维护着的，不是每次重新加出来的。</b></div>')
    h.append('<div class="sq">第一步　f 和“每层最大值”是什么关系</div>')
    h.append('<div class="think">选 j 个串的最长公共前缀，就是在字典树里找一个“下面至少挂着 j 个串”的结点，越深越好。第 d 层所有结点里挂串最多的那个，挂了 mx[d] 个。所以 <b>f(j) = mx[d] ≥ j 的最大的 d</b>。这就是你说的“每层求个最大值”。</div>')
    h.append(b_stair(s2))
    h.append('<div class="sq">第二步　插入一个串，到底有几格 f 会变</div>')
    h.append('<div class="think">插入一个串，它经过的每一层只有一个结点 +1，所以每层的 mx 最多 +1。mx[d] 从 m 变成 m + 1 时：j ≤ m 的条件本来就成立，没变；j ≥ m + 2 的还是不成立，没变；<b>只有 j = m + 1 这一格可能变</b>，变成 max(f[m+1], d)。所以插入第 i 个串，最多改 |sᵢ| + 1 格。</div>')
    anim1, _ = b_insert('b_s1', '动画 B2 · 样例 1 逐层插入（a、ab、abc、abcd）', s1, [0, 6, 4, 12], pos1,
                        '黄圈 = 当前走到的结点，蓝圈 = 这个串走过的路；黄柱 = 这一层的 mx 刚变大；黄格 = 这一步改了的 f。')
    h.append(anim1)
    h.append('<p>样例 1 是“最坏”的：每个串都比前一个长一截，每插一个，f 数组整个往上抬一格。但就算这样，改的格数也只是串长。再看样例 2，大部分步骤<b>一格都不用改</b>：</p>')
    anim2, ev2 = b_insert('b_s2', '动画 B3 · 样例 2 逐层插入（8 个串，有分叉、有重复）', s2, [3, 5, 9, 10, 14, 20, 28, 36], pos2,
                          '每一帧的和都是程序算出来的，最后一帧的 36 就是样例 2 最后一行。')
    h.append(anim2)
    nchg = sum(1 for e in ev2 if e['fchg'])
    h.append('<p>样例 2 一共走了 %d 步，只有 <b>%d 步</b>真的改了 f。你的做法要重算 1 + 2 + … + 8 = 36 次。n = 5×10⁵ 时，差别是 <b>1.25×10¹¹ 次</b>对 <b>不到 1.5×10⁶ 次</b>。</p>' % (len(ev2), nchg))
    h.append('<p>完整代码（大样例 5 个全过，最大的 0.25 秒）：</p>')
    code = open('/home/user/Day1/2026-09-27_CSP-S模拟赛day2/正解代码/B_毛线.cpp', encoding='utf-8').read()
    h.append('<pre><code>%s</code></pre>' % esc(code))
    h.append('<div class="trap"><b>【触发】</b>要对每个前缀 i 输出一个和，和里有 i 项　<b>【判据】</b>问自己：从 i−1 到 i，这 i 项里到底有几项变了？变的少，就只改变了的那几项，和随改随维护（减旧的、加新的）。</div>')
    h.append('<div class="trap"><b>【触发】</b>“f(j) = 满足 g(d) ≥ j 的最大 d”　<b>【判据】</b>f 和 g 是同一张柱状图横着读和竖着读。g 的一根柱子长高一格，只有一个 f 会变。</div>')
    h.append('<p><b>稳拿的 10 分：</b>子任务 1（n ≤ 10，|s| ≤ 50）按定义暴力，30 行（<code>正解代码/暴力/B_暴力.cpp</code>）。14:04 你说“第二题十分性价比不高”，转去写的 D 子任务 2 思路不对、最后编译错误；B 的暴力 10 分钟就是稳稳的 10 分。</p>')
    return '\n'.join(h)
