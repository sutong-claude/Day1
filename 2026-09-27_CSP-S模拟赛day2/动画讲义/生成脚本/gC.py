# -*- coding: utf-8 -*-
from common import *

S1 = '4336352375'


def walk(s):
    X, Y = [0], [0]
    for ch in s:
        v = int(ch)
        r, y, b = v >> 2 & 1, v >> 1 & 1, v & 1
        X.append(X[-1] + r - y)
        Y.append(Y[-1] + r - b)
    return X, Y


def dp(s):
    X, Y = walk(s)
    n = len(s)
    f, par = [0] * (n + 1), [None] * (n + 1)
    for i in range(1, n + 1):
        f[i], par[i] = f[i - 1], None
        for j in range(i):
            if X[j] <= X[i] and Y[j] <= Y[i] and f[j] + i - j > f[i]:
                f[i], par[i] = f[j] + i - j, j
    segs, i = [], n
    while i > 0:
        if par[i] is None:
            i -= 1
        else:
            segs.append((par[i] + 1, i))
            i = par[i]
    return f, segs[::-1]


def c_walk():
    s = S1
    X, Y = walk(s)
    f, segs = dp(s)
    assert f[-1] == 7
    xs, ys = range(min(X) - 1, max(X) + 2), range(min(Y) - 1, max(Y) + 2)
    ox, oy, u = 120, 30, 70

    def P(x, y):
        return ox + (x - min(xs)) * u, oy + (max(ys) - y) * u
    W = ox + (len(xs) - 1) * u + 150
    H = oy + (len(ys) - 1) * u + 40

    def grid():
        b = []
        for x in xs:
            b.append(L(P(x, min(ys))[0], P(x, min(ys))[1], P(x, max(ys))[0], P(x, max(ys))[1], 'ln s-soft w-t'))
            b.append(Tx(P(x, min(ys))[0], P(x, min(ys))[1] + 18, 'X=%d' % x, 'ti'))
        for y in ys:
            b.append(L(P(min(xs), y)[0], P(min(xs), y)[1], P(max(xs), y)[0], P(max(xs), y)[1], 'ln s-soft w-t'))
            b.append(Tx(P(min(xs), y)[0] - 10, P(min(xs), y)[1] + 4, 'Y=%d' % y, 'ti', 'end'))
        return b
    seen = {}
    fr = []
    b0 = grid() + [C(*P(0, 0), 7, 'pt-on'), Tx(P(0, 0)[0] + 12, P(0, 0)[1] - 10, 'p0', 'ti', 'start')]
    fr.append((svg(W, H, b0), '把每个格子变成一步：<b>X 加上（红 − 黄），Y 加上（红 − 蓝）</b>。从原点 p0 出发。段 (j, i] 是好的 ⇔ 这段里红 ≥ 黄 且 红 ≥ 蓝 ⇔ <b>X[i] ≥ X[j] 且 Y[i] ≥ Y[j]</b>，也就是 p_i 在 p_j 的右上方（可以重合）。这就是你 12:01 说的“只要知道 A − B”。'))
    arrows = []
    for i in range(1, len(s) + 1):
        v = int(s[i - 1])
        red = v >> 2 & 1
        x1, y1 = P(X[i - 1], Y[i - 1])
        x2, y2 = P(X[i], Y[i])
        if (x1, y1) != (x2, y2):
            arrows.append(arrow(x1, y1, x2, y2, 'r' if red else 'b'))
        else:
            arrows.append(C(x2, y2, 12, 'nd nd-r'))
        b = grid() + arrows[:]
        for k in range(i + 1):
            b.append(C(*P(X[k], Y[k]), 6, 'pt-on' if k == i else 'pt'))
        # 标签：同一点多个编号并在一起
        lab = {}
        for k in range(i + 1):
            lab.setdefault((X[k], Y[k]), []).append('p%d' % k)
        for (x, y), names in lab.items():
            px, py = P(x, y)
            b.append(Tx(px + 10, py - 10, ','.join(names), 'ti', 'start'))
        rgb = ['红' if v >> 2 & 1 else '', '黄' if v >> 1 & 1 else '', '蓝' if v & 1 else '']
        pieces = '、'.join(t for t in rgb if t)
        kind = '有红子：X、Y 都<b>不减</b>（往右上走，或者原地不动）' if red else '没有红子：X、Y 都<b>不增</b>，至少一个减（往左下走）'
        fr.append((svg(W, H, b), '第 %d 格是 %s（%s）。%s，到 p%d = (%d, %d)。' % (i, s[i - 1], pieces, kind, i, X[i], Y[i])))
    for (l, r) in segs:
        b = grid() + arrows[:]
        for k in range(len(s) + 1):
            cls = 'pt-good' if k in (l - 1, r) else 'pt'
            b.append(C(*P(X[k], Y[k]), 7 if k in (l - 1, r) else 5, cls))
        lab = {}
        for k in range(len(s) + 1):
            lab.setdefault((X[k], Y[k]), []).append('p%d' % k)
        for (x, y), names in lab.items():
            px, py = P(x, y)
            b.append(Tx(px + 10, py - 10, ','.join(names), 'ti', 'start'))
        fr.append((svg(W, H, b), '好段 [%d, %d]：起点 p%d = (%d, %d)，终点 p%d = (%d, %d)，终点在起点右上方（或重合）✓。' % (
            l, r, l - 1, X[l - 1], Y[l - 1], r, X[r], Y[r])))
    fr.append((fr[-1][0], '三个好段 [1,2]、[4,6]、[9,10] 总长 2 + 3 + 2 = <b>7</b>，和样例一致。你的 O(n²) DP 就是：对每个 i，看所有 j 能不能“p_i 在 p_j 右上方”，能就用 f[j] + (i − j)。<b>30 分你拿到了</b>。'))
    return fp('c_walk', '动画 C1 · 把棋子变成平面上的一条路（样例 1）', fr, '红箭头 = 有红子的格子，蓝箭头 = 没有红子的格子；红圈 = 原地不动（红黄蓝都有）。')


def build():
    h = []
    h.append('<h2 id="C">C 🔴　<span class="bdg bdg-o">30 分</span><span class="kaodian">前缀差 · 二维偏序 DP</span></h2>')
    h.append('<div class="method"><b>一句话题意：</b>把序列切成若干段，红 ≥ 黄 且 红 ≥ 蓝 的段叫好段，好段总长最大是多少。</div>')
    h.append('<div class="mind real">11:58 <span class="qq">“三个前缀和……所以这个是 N 方的，不满足。”</span>12:01 <span class="qq">“我们只要知道 A − B 的值就行了。”</span>12:04 <span class="qq">“如果我以……I 减去 FI，那最终我只要做一个简单处理。”</span>12:05 <span class="qq">“N 方的分是非常好骗的……30 分手到擒来。”</span><br>赛后你说：<span class="qq">“C 题我解决不了，因为这个 DP 没有办法优化。”</span></div>')
    h.append('<p>你的三个想法方向都对：前缀差、i − f[i]，还有 30 分的 O(n²)。你说“这个 DP 没法优化”——<b>以你现在的工具箱，这个判断是对的</b>，这场拿 30 分就是合理分数。下面只讲清楚“卡在哪”，不要求你现在会。</p>')
    h.append(c_walk())
    h.append('<div class="sq">为什么难优化</div>')
    h.append('<div class="think">转移条件是“X[j] ≤ X[i] 且 Y[j] ≤ Y[i]，并且 j &lt; i”，一共三个方向的限制（时间、X、Y）。只有一个限制时用树状数组 O(n log n)；三个限制的标准做法是 CDQ 分治，O(n log² n)。n = 2×10⁵ 能过（再拿 30 分），2×10⁶ 在 1 秒里过不了，所以满分要找这道题自己的结构。</div>')
    h.append('<div class="think">这道题的结构就在动画里：<b>每一步要么往右上走（有红子），要么往左下走（没红子）</b>，X 和 Y 永远同涨同跌。利用这一点，“往右上走”时只需要查新看得到的一行一列，“往左下走”时答案只会不变或 +1，最后是 O(n log n)。细节在 <code>正解代码/C_棋子.cpp</code> 的注释里，和 O(n²) 随机对拍 900 组全对，2×10⁶ 最慢约 0.4 秒。</div>')
    h.append('<div class="trap"><b>【触发】</b>“段内 A ≥ B 且 A ≥ C”　<b>【判据】</b>写成前缀差，条件变成“两个前缀值都不比起点小”。先把 O(n²) 交上（你这场做到了），再看 n 的大小决定要不要往下想。</div>')
    h.append('<p><b>这题唯一可惜的：</b>12:05 你已经说“30 分手到擒来”，却推迟到 13:36 才写。执行卡新加了一条：<b>自己说出“这 X 分手到擒来”，就立刻去拿</b>。</p>')
    return '\n'.join(h)
