# -*- coding: utf-8 -*-
import subprocess, os
from common import *

SOL = os.path.join(HERE, '..', 'sol')


def run(binname, inp):
    return subprocess.run([os.path.join(SOL, binname)], input=inp, capture_output=True, text=True).stdout.strip()


def brute(a):
    best = 10 ** 9
    for b in range(0, 4 * a + 5):
        best = min(best, bin(a + b).count('1') + bin(b).count('1'))
    return 2 * best - 1


EX2 = open(os.path.join(HERE, '..', 'samples', 'A', 'ex_mul2.in')).read()
OUT = {
    'v1': run('A_v1_paper', EX2), 'v3': run('A_v12-33', EX2), 'v4': run('A_v13-02', EX2),
    'v5': run('A_final', EX2), 'tot': str(EX2.strip().count('1')),
}
assert OUT['v1'] == '947' and OUT['v3'] == '853' and OUT['v4'] == '729' and OUT['v5'] == '671', OUT

# ---------- A1：九个阶段 ----------
STAGES = [
    ('10:25', 'v1 按 1 拆 / 最高位减一次', OUT['v1'], '“10 的 6 次方，说明是有通用的方法的，而不是进行暴力”（10:16）', '只试了两种构造：全部加，或者“高一位的 2ⁿ 减去一个数”。10:48 大样例出来 <b>947</b>，正确是 671。10:49 你自己找到了病根：<span class="qq">“为什么一定要在最高位呢？”</span>'),
    ('11:16', '写出 a + b − (0 + b) = a', '—', '“A 加上 B 减去（0 加上 B）还是等于 A……要使它加上 B 以后一的个数最少”', '<b>这一句就是暴力</b>：b 从 0 往上枚举，数 a+b 和 b 各有几个 1，取最小。你当时把它当成“题目换了个说法”，没意识到它能直接跑。'),
    ('11:30', '数样例里 1 的个数', OUT['tot'], '“474 跟 671 好像没有什么关系”', '想打表的方向是对的，但只打了一个数。<b>暴力能打出几十个数</b>，规律一眼就看出来。中间 7 分钟卡在 Code::Blocks 的 <code>word unexpected</code>（文件夹名带括号）。'),
    ('11:33', '“几个零之间只隔一个一”', '—', '“它一定是长这个样子的，几个零之间肯定只隔一个一”', '这就是答案的结构（非相邻形式）。离做法只差最后一块，可是没有反例，你没法验证。11:39 转去 B。'),
    ('12:22', 'v2 连续 1 算两项', 'RE', '“OK，我会了，第一题我会了，我发现了诀窍”（12:18）', '连续一段 1 用两项、单独的 1 用一项——对了一大半。但 <code>while (point &lt;= n || a[point] != 1)</code> 里 || 应为 &amp;&amp;，越界死循环。<b>12:45 交的正是这份 → RE</b>。'),
    ('12:33', 'v3 改系数', OUT['v3'], '“614 改完之后……594……709”（12:40）', '开始试系数，大样例 <b>853</b>、594、709……<b>止损信号</b>：同一个地方改了三次还不对，说明公式结构错了。'),
    ('13:02', 'v4 修好越界', OUT['v4'], '“好像不是代码问题，是思路有问题。但我认为我的思路没有问题”（13:07）', '大样例 <b>729</b>。13:06 交 → WA。然后你做了对的事：<span class="qq">“我会写暴力吗？”</span>'),
    ('13:17', '暴力：枚举 b', '—', '“等一下，有可能是你生成两个”', '11:16 那个式子回来了。13:22 对拍出错，13:24 手算反例：<span class="qq">“我代码输出 7，我明白哪里出问题了”</span>'),
    ('13:33', 'v5 加 check()', OUT['v5'], '“最多接受中间只有一个 0”（13:28）', '一段 1 中间夹一个 0 时，多花一项就能接着往下；两个 0 就断开。大样例 <b>671</b>，13:35 满分。'),
]


def a_story():
    frames = []
    X0, X1 = 30, 530
    t0, t1 = 10 * 60 + 10, 13 * 60 + 35

    def tx(hm):
        h, m = map(int, hm.split(':'))
        return X0 + (h * 60 + m - t0) / (t1 - t0) * (X1 - X0)
    for k, (tm, name, out, q, note) in enumerate(STAGES):
        b = [L(X0, 40, X1, 40, 'ln s-soft w-m')]
        for hm in ['10:10', '11:00', '12:00', '13:00', '13:35']:
            b.append(L(tx(hm), 34, tx(hm), 46, 'ln s-soft w-t'))
            b.append(Tx(tx(hm), 26, hm, 'ti'))
        for j, st in enumerate(STAGES):
            cls = 'nd nd-y' if j == k else ('nd nd-g' if j < k else 'nd')
            b.append(C(tx(st[0]), 40, 9 if j == k else 6, cls))
        b.append(Tx(tx(tm), 66, tm, 'tlabb'))
        b.append(R(30, 84, 500, 84, 'bx bx-in' if out in ('671',) else ('bx bx-red' if out not in ('—',) else 'bx')))
        b.append(Tx(48, 112, '第 %d 步：%s' % (k + 1, name), 'tlabb', 'start'))
        if out == '—':
            b.append(Tx(48, 146, '（这一步没有代码输出）', 'tso tlab', 'start'))
        else:
            ok = out == '671'
            b.append(Tx(48, 150, '样例 2 输出', 'tlab', 'start'))
            b.append(Tx(200, 152, out, 'big ' + ('tgr' if ok else 'trd'), 'start'))
            b.append(Tx(300, 150, '正确答案 671', 'tlab', 'start'))
            b.append(Tx(470, 150, '✓' if ok else '✗', 'big ' + ('tgr' if ok else 'trd'), 'middle'))
        frames.append((svg(560, 180, b), '<span class="qq">%s</span><br>%s' % (esc(q).replace('&lt;', '<').replace('&gt;', '>'), note)))
    return fp('a_story', '动画 A1 · 你的 A 题：从 10:10 到 13:35 的九步', frames,
              '上面的点是时间轴；红框 = 输出不对，蓝框 = 输出对了。样例 2 的输出都是把当时那份代码原样重跑得到的。')


# ---------- A2：11011 ----------
def v4_terms(bits):
    """按 v4 的逻辑（从高位扫，连续段两项、单独 1 一项）给出每一项。bits 高位在前。"""
    n = len(bits)
    a = [0] + [int(c) for c in bits] + [0, 0]
    terms, i = [], 1
    while i <= n:
        if a[i] == 1:
            if a[i + 1] != 1:
                terms.append(('+', n - i))
            else:
                p = i + 1
                while p <= n and a[p] == 1:
                    p += 1
                terms.append(('+', n - i + 1))
                terms.append(('-', n - (p - 1)))
                i = p
        i += 1
    return terms


def naf_terms(v):
    terms, k = [], 0
    while v:
        if v & 1:
            d = 2 - (v & 3)
            terms.append(('+' if d == 1 else '-', k))
            v -= d
        v >>= 1
        k += 1
    return terms[::-1]


def a_11011():
    bits = '11011'
    v = int(bits, 2)
    t4, tn = v4_terms(bits), naf_terms(v)
    assert sum((1 if s == '+' else -1) * 2 ** k for s, k in t4) == v
    assert sum((1 if s == '+' else -1) * 2 ** k for s, k in tn) == v
    assert 2 * len(t4) - 1 == int(run('A_v13-02', bits)) and 2 * len(tn) - 1 == brute(v)
    n = len(bits)
    W = 560

    def base(hl=()):
        b = []
        for i, c in enumerate(bits):
            x = 170 + i * 56
            cls = 'bx bx-in' if i in hl else 'bx'
            b.append(R(x, 20, 48, 44, cls))
            b.append(Tx(x + 24, 49, c, 'tv'))
            b.append(Tx(x + 24, 80, '2^%d' % (n - 1 - i), 'ti'))
        b.append(Tx(20, 49, 'a = 27 =', 'tlabb', 'start'))
        return b

    def termline(terms, y, label, cls):
        s = ' '.join(('%s 2^%d' % (sg, k)) for sg, k in terms).lstrip('+ ').strip()
        val = sum((1 if sg == '+' else -1) * 2 ** k for sg, k in terms)
        return [Tx(20, y, label, 'tlabb', 'start'), Tx(20, y + 26, '%s = %d' % (s.replace('+ ', '+').replace('- ', '−'), val), 'tvs ' + cls, 'start'),
                Tx(20, y + 50, '%d 项 → 答案 2×%d−1 = %d' % (len(terms), len(terms), 2 * len(terms) - 1), 'tlab ' + cls, 'start')]
    fr = []
    fr.append((svg(W, 200, base()), '反例是 <b>11011</b>（= 27）。你 13:06 交的 v4 输出 7，正确答案 5。把 1～4095 全部和暴力对一遍，v4 错 1085 个，而 27 是最小的那个：1～26 v4 全对，所以你手编的小数据怎么都碰不到它。'))
    fr.append((svg(W, 200, base(hl=(0, 1)) + [Tx(20, 120, 'v4 从高位开始扫：前两个 1 连在一起', 'tlab', 'start'), Tx(20, 146, '→ 用 +2^5 − 2^3 两项搞定这一段', 'tlab', 'start')]),
               'v4 从高位扫，碰到连续的 <b>11</b>（2⁴ 和 2³），用“高一位减最低位”两项：<b>+2⁵ − 2³</b>。'))
    fr.append((svg(W, 200, base(hl=(3, 4)) + [Tx(20, 120, '中间遇到 0，这一段结束；后面又是一段 11', 'tlab', 'start'), Tx(20, 146, '→ 再来两项 +2^2 − 2^0', 'tlab', 'start')]),
               '中间的 0 把这一段断开了。后面又是一段 <b>11</b>，再来两项：<b>+2² − 2⁰</b>。'))
    fr.append((svg(W, 200, base() + termline(t4, 118, 'v4 的拆法：', 'trd')), 'v4 一共 <span class="r">4 项</span>：32 − 8 + 4 − 1 = 27，答案 2×4−1 = <span class="r">7</span>。算式没错，就是项数多了。'))
    fr.append((svg(W, 200, base(hl=(0, 1, 2, 3, 4)) + termline(tn, 118, '更好的拆法：把中间那个 0 也吞进来', 'tgr')),
               '把整个 <b>11011</b> 当成一段：先用 2⁵ 盖住，再减掉多出来的。2⁵ = 32，32 − 27 = 5 = 4 + 1，所以 <b>27 = 2⁵ − 2² − 2⁰</b>，只要 <span class="g">3 项</span>，答案 <span class="g">5</span>。'))
    fr.append((svg(W, 200, base() + [Tx(20, 118, '为什么吞一个 0 更划算：', 'tlabb', 'start'),
                                     Tx(20, 146, '吞进来：多减一项（−2^2），只多 1 项', 'tlab tgr', 'start'),
                                     Tx(20, 172, '断开：后面那段要重新开头，又是 2 项', 'tlab trd', 'start')]),
               '这就是你 13:28 说的：<span class="qq">“中间有个 0，你付出额外代价，但是你会少一次……最多接受中间只有一个 0”</span>。夹一个 0：吞进来多 1 项，断开多 2 项，所以吞。夹两个 0：吞进来要多 2 项，和断开一样，不用吞。'))
    return fp('a_11011', '动画 A2 · 为什么 13:06 那版错了：反例 11011', fr, '两种拆法都是真实程序算出来的：v4 按你 13:02 的代码逻辑拆，更好的拆法由数位 DP 回溯得到。')


# ---------- A3：1～63 ----------
def a_grid():
    cells, bad = [], []
    for a in range(1, 64):
        s = bin(a)[2:]
        r4 = int(run('A_v13-02', s))
        rb = brute(a)
        cells.append((a, r4 == rb))
        if r4 != rb:
            bad.append((a, s, rb, r4))
    b = []
    for idx, (a, ok) in enumerate(cells):
        r, c = divmod(idx, 9)
        x, y = 12 + c * 60, 12 + r * 46
        b.append(R(x, y, 54, 40, 'okc' if ok else 'noc', 5))
        b.append(Tx(x + 27, y + 18, str(a), 'tvs'))
        b.append(Tx(x + 27, y + 34, bin(a)[2:], 'ti'))
    s = '<svg viewBox="0 0 560 340" width="560" height="340" role="img" class="grid64">%s</svg>' % ''.join(b)
    rows = [[str(a), '<code>%s</code>' % bs, str(rb), '<span class="no">%d</span>' % r4] for a, bs, rb, r4 in bad]
    return s, table(['a', '二进制', '暴力（正确）', 'v4 输出'], rows), bad


# ---------- A4：数位 DP 逐行 ----------
DP_CODE = [
    'f[0] = 0, f[1] = INF;',
    'for (int i = n - 1; i >= 0; i--) {',
    '    g[0] = g[1] = INF;',
    '    for (int c = 0; c <= 1; c++) {',
    "        int v = s[i] - '0' + c;",
    '        if (v == 0) g[0] = min (g[0], f[c]);',
    '        else if (v == 1) {',
    '            g[0] = min (g[0], f[c] + 1);',
    '            g[1] = min (g[1], f[c] + 1);',
    '        }',
    '        else g[1] = min (g[1], f[c]);',
    '    }',
    '    f[0] = g[0], f[1] = g[1];',
    '}',
    'int k = min (f[0], f[1] + 1);',
    "cout << 2 * k - 1 << '\\n';",
]


def a_dp():
    s = '11011'
    n = len(s)
    INF = 10 ** 9
    shw = lambda x: '∞' if x >= INF else str(x)
    steps = []
    f = [0, INF]
    g = [INF, INF]
    st = {'i': '-', 's[i]': '-', 'c': '-', 'v': '-'}

    def rec(l, note):
        v = dict(st)
        v['f[0]'], v['f[1]'], v['g[0]'], v['g[1]'] = shw(f[0]), shw(f[1]), shw(g[0]), shw(g[1])
        steps.append({'l': l, 'v': v, 'n': note})
    rec(1, 's = 11011。f[c] 的意思：<b>低位已经处理完，往当前这一位进位 c，最少用了几项</b>。一开始还没处理任何位，进位只能是 0，用了 0 项。')
    for i in range(n - 1, -1, -1):
        st['i'], st['s[i]'], st['c'], st['v'] = str(i), s[i], '-', '-'
        rec(2, '处理第 %d 位（从右往左数第 %d 位），这一位原来是 <b>%s</b>。' % (i, n - i, s[i]))
        g = [INF, INF]
        rec(3, '新的一层先清空。')
        for c in (0, 1):
            st['c'] = str(c)
            if f[c] >= INF:
                rec(4, '进位 c = %d 这条路还没走到过（f[%d] = ∞），跳过。' % (c, c))
                continue
            v = int(s[i]) + c
            st['v'] = str(v)
            rec(5, '这一位 %s 加上进位 %d，得 <b>v = %d</b>。' % (s[i], c, v))
            if v == 0:
                g[0] = min(g[0], f[c])
                rec(6, 'v = 0：这一位填 0，不用新的项，也不往上进位。')
            elif v == 1:
                rec(7, 'v = 1：这一位必须有一项，有两种填法。')
                g[0] = min(g[0], f[c] + 1)
                rec(8, '填 <b>+1</b>（这一项是加）：用掉 1 项，不进位。')
                g[1] = min(g[1], f[c] + 1)
                rec(9, '填 <b>−1</b>（这一项是减）：1 − (−1) = 2，相当于往上进 1。用掉 1 项，进位 1。')
            else:
                g[1] = min(g[1], f[c])
                rec(11, 'v = 2：这一位填 0，往上进 1，不用新的项。')
        f = g[:]
        st['c'], st['v'] = '-', '-'
        rec(13, '这一位做完：进位 0 最少 %s 项，进位 1 最少 %s 项。' % (shw(f[0]), shw(f[1])))
    k = min(f[0], f[1] + 1)
    st['i'], st['s[i]'] = '-', '-'
    rec(15, '最高位也做完了。如果还剩进位 1，要再加一项 +2⁵。k = min(%s, %s + 1) = <b>%d</b>。' % (shw(f[0]), shw(f[1]), k))
    rec(16, '答案 2 × %d − 1 = <b>%d</b>，和暴力一致。这个 DP 只记“进位 0 还是 1”，所以 10⁶ 位也只要 2×10⁶ 个状态。' % (k, 2 * k - 1))
    assert 2 * k - 1 == brute(int(s, 2))
    return codeanim('a_dp', '动画 A3 · 数位 DP 逐行执行（a = 11011）', DP_CODE, steps,
                    '右边变量表里，变了的值会高亮。INF 显示成 ∞。')


def build():
    grid_svg, bad_table, bad = a_grid()
    first_bad = bad[0][0]
    h = []
    h.append('<h2 id="A">A 乘法　<span class="bdg bdg-o">100 分</span><span class="kaodian">有符号二进制 · 数位 DP</span></h2>')
    h.append('<div class="method"><b>一句话题意：</b>用最少几个 ±2ᵏ 凑出 a。每一项要左移一次，项和项之间要加减一次，所以答案 = 2 × 项数 − 1。</div>')
    h.append('<p>这题你拿了满分，而且每一个关键结论都是你自己推出来的。问题只在一件事：<b>用了 2 小时 37 分，占全场 65%</b>。下面先把你的九步走一遍。</p>')
    h.append(a_story())
    h.append('<div class="sq">为什么暴力来得这么晚——你自己说的三条</div>')
    h.append('<div class="mind real">你赛后总结：<span class="qq">“一，我知道代码错了，但我不理解为什么错，也就是我需要一个小数据，而不是大数据。二，我能合理地解释，我认为我的代码非常正确。三，我挖掘了一下，发现我一开始那个等式就是个暴力。”</span></div>')
    h.append('<p>这三条录音里都对得上：</p>')
    h.append(table(['你说的', '录音里', '以后怎么办'], [
        ['① 要的是小数据', '10:48、12:28 大样例只告诉你“错了”；13:02 你手编 10、110、1110，全对，手编的数据太整齐', '让机器找：暴力 + gen 从 n = 1 开始 + 对拍'],
        ['② 我觉得代码没问题', '12:42 <span class="qq">“我这个算法就是这个样子，为什么不对呢？”</span>', '只有反例能说服你，1 分钟跑数据'],
        ['③ 等式就是暴力', '10:16 <span class="qq">“而不是进行暴力”</span>；11:16 写下 <code>a + b - (0 + b) = a</code>；12:13 <span class="qq">“关键我自己也算不出来答案”</span>', '式子长成“在所有 X 里取最好”，X 能列出来 → for 循环'],
    ]))
    h.append('<div class="renhua">三条合起来是一件事：<b>你把暴力当成“数据小的时候骗分用的”</b>，所以 10:16 看到 10⁶ 就不考虑了。可这场暴力真正值钱的是另外两个用处——<b>给你一个小反例</b>，<b>替你算出你算不出的答案</b>。这两件事和数据范围无关。</div>')
    h.append('<p>暴力一跑有多快？下面是 a = 1～63，暴力和你 13:06 那版（v4）的比较。<b>第一个红格就是 %d</b>，也就是下面动画里的反例。</p>' % first_bad)
    h.append('<figure class="one">%s<figcaption>绿 = v4 和暴力一样，红 = 不一样。每格下面是二进制。</figcaption></figure>' % grid_svg)
    h.append('<details class="self"><summary>63 个数里 v4 错了哪几个（点开）</summary>%s</details>' % bad_table)
    h.append(a_11011())
    h.append('<div class="trap"><b>【触发】</b>大样例不对，但你觉得自己把情况都考虑全了；或者想找个“很强的样例”却算不出答案　<b>【判据】</b>立刻写暴力，gen 从 n = 1 开始对拍。对拍出来的第一组就是最小反例，手算一遍就知道哪里漏了。</div>')
    h.append('<div class="sq">不需要灵感的做法：数位 DP</div>')
    h.append('<div class="think">10:59 你想过记忆化：<span class="qq">“记录所有出现过的每一位……位置太多了”</span>。你想记的是“哪些位用过”这种整体状态，确实太多，这个判断没错。换个状态就行：从最低位往高位做，每一位最后填 −1、0、+1，<b>只记“往上一位进位 0 还是 1”</b>。一位两个状态，10⁶ 位也只有 2×10⁶ 个。</div>')
    h.append(a_dp())
    h.append('<div class="trap"><b>【触发】</b>二进制、加减、“最少用几项”　<b>【判据】</b>从低位往高位做，状态 = 进位。</div>')
    return '\n'.join(h)
