# -*- coding: utf-8 -*-
from common import *


def valid(w, d, b):
    n = len(d)
    if len(w) != n:
        return False, '长度 %d ≠ n = %d，第一句就返回 false' % (len(w), n)
    for i in range(1, n):
        if w[i] and w[i - 1]:
            return False, '第 %d、%d 个人都是狼，挨着了' % (i, i + 1)
    pre = [0]
    for x in w:
        pre.append(pre[-1] + x)
    for i in range(n):
        if w[i]:
            continue
        t = pre[i] if d[i] == 'L' else pre[n] - pre[i + 1]
        if t != b[i]:
            return False, '第 %d 个人是村民，说%s边有 %d 个狼，实际是 %d 个' % (i + 1, '左' if d[i] == 'L' else '右', b[i], t)
    return True, '全部说得通 ✓'


def people(d, b, w, y=40, x0=150, known=True):
    out = []
    for i in range(len(d)):
        x = x0 + i * 110
        if w is None or i >= len(w):
            cls, role = 'bx bx-dim', '？'
        else:
            cls, role = ('bx bx-red', '狼') if w[i] else ('bx bx-grn', '村民')
        out.append(R(x, y, 90, 56, cls))
        out.append(Tx(x + 45, y + 24, '%s  %d' % (d[i], b[i]), 'tvs'))
        out.append(Tx(x + 45, y + 46, role, 'tlab'))
        out.append(Tx(x + 45, y - 8, '第 %d 人' % (i + 1), 'ti'))
    return out


def d_bug():
    d, b = 'LL', [1, 1]
    n = 2
    fr = []
    fr.append((svg(460, 180, people(d, b, None) + [Tx(20, 150, '正确答案：10（第 1 人是狼，第 2 人是村民）', 'tlab tgr', 'start')]),
               '最小反例：n = 2，两人都往左看，都说“左边有 1 个狼”。第 1 人左边没人，说 1 是假话，他只能是狼；第 2 人左边正好 1 个狼，说的是真话。答案 <b>10</b>。'))
    for i in range(0, 1 << n):
        t = i
        w = []
        while t != 0:
            w.append(t % 2)
            t //= 2
        ok, why = valid(w, d, b)
        wtxt = '{' + ', '.join(map(str, w)) + '}'
        body = people(d, b, w if len(w) == n else None) + [
            Tx(20, 20, 'i = %d（二进制 %s）' % (i, bin(i)[2:]), 'tlabb', 'start'),
            Tx(20, 130, 'wolves = %s，长度 %d' % (wtxt, len(w)), 'tvs', 'start'),
            Tx(20, 160, 'isValid：' + why, 'tlab ' + ('tgr' if ok else 'trd'), 'start')]
        note = '你的循环：<code>while (t != 0) { wolves.push_back(t %% 2); t /= 2; }</code>。i = %d 得到 wolves = %s，长度 %d。' % (i, wtxt, len(w))
        if i == 1:
            note += '<span class="r">这正是答案 10</span>（第 1 人是狼），可是只取出了 1 位，长度 1 ≠ 2，<b>isValid 第一句就把它挡掉了</b>。'
        elif len(w) != n:
            note += '长度不够，直接 false。'
        else:
            note += 'isValid：' + why + '。'
        fr.append((svg(460, 180, body), note))
    fr.append((svg(460, 180, people(d, b, None) + [Tx(20, 150, '四个 i 都没通过 → 输出 -1 ✗', 'tlabb trd', 'start')]),
               '四种都没过，你的程序输出 <span class="r">-1</span>。只有最高位是 1 的 i（最后一个人是狼）长度才够 n，所以<b>你只试了“最后一个人是狼”的那一半</b>。题面样例三组答案 001、-1、10101 恰好都是这种，所以样例过了；大样例 sample2 的 1000 组里错 277 组。'))
    w = [1 >> k & 1 for k in range(n)]
    ok, why = valid(w, d, b)
    assert ok
    fr.append((svg(460, 180, people(d, b, w) + [Tx(20, 130, 'for k in 0..n-1: wolves.push_back(i >> k & 1)', 'tvs', 'start'),
                                                Tx(20, 160, 'i = 1 → {1, 0}，长度 2 → ' + why, 'tlab tgr', 'start')]),
               '改一行：<code>for (int k = 0; k &lt; n; k++) wolves.push_back (i &gt;&gt; k &amp; 1);</code>，每个 i 都取满 n 位。i = 1 得到 {1, 0}，通过 ✓。改完就是子任务 1 的 10 分。'))
    return fp('d_bug', '动画 D1 · 14:01 那版暴力为什么 0 分（最小反例 LL 1 1）', fr, '每一帧的 isValid 结果都是把 checker 里的判定函数原样跑出来的。')


def d_dp():
    d = 'LLLLLL'
    b = [3, 1, 1, 0, 2, 2]
    n = len(b)
    # V[i]：第 i 人当村民时前面的狼数（必须 = b[i]）；Wf[i]：第 i 人当狼时，算上他一共几个狼
    V, Wf, pv = [None] * n, [None] * n, [None] * n
    fr = []

    def draw(k, msg_cls=''):
        body = []
        for i in range(n):
            x = 110 + i * 78
            body.append(Tx(x + 34, 22, '第 %d 人' % (i + 1), 'ti'))
            body.append(R(x, 30, 68, 34, 'bx', 4))
            body.append(Tx(x + 34, 53, 'L %d' % b[i], 'tvs'))
            for row, arr, name in ((0, V, '村民'), (1, Wf, '狼')):
                y = 78 + row * 46
                if i > k:
                    cls, txt = 'bx bx-dim', ''
                elif arr[i] is None:
                    cls, txt = 'bx bx-red', '✗'
                else:
                    cls, txt = 'bx bx-grn', ('前面 %d' % arr[i]) if row == 0 else ('共 %d' % arr[i])
                body.append(R(x, y, 68, 36, cls, 4))
                body.append(Tx(x + 34, y + 23, txt, 'ti'))
        body.append(Tx(95, 101, '当村民', 'tlab', 'end'))
        body.append(Tx(95, 147, '当狼', 'tlab', 'end'))
        return svg(590, 180, body)
    fr.append((draw(-1), '子任务 2：所有人都往左看。例子：6 个人，b = 3 1 1 0 2 2。<b>每个人只有两种状态</b>：当村民（那么他前面必须恰好有 b 个狼），或者当狼（那么前一个人必须是村民）。每种状态下“前面有几个狼”都是确定的，所以不用分类讨论，一格一格填就行。'))
    for i in range(n):
        # 当村民：前面狼数必须等于 b[i]
        cand = []
        if i == 0:
            cand.append(0)
        else:
            if V[i - 1] is not None:
                cand.append(V[i - 1])
            if Wf[i - 1] is not None:
                cand.append(Wf[i - 1])
        V[i] = b[i] if b[i] in cand else None
        # 当狼：前一个必须是村民
        if i == 0:
            Wf[i] = 1
        else:
            Wf[i] = V[i - 1] + 1 if V[i - 1] is not None else None
        why = []
        if V[i] is not None:
            why.append('当村民：前面可能有 %s 个狼，其中有 %d = b，<span class="g">可以</span>' % (' 或 '.join(map(str, sorted(set(cand)))) or '0', b[i]))
        else:
            why.append('当村民：前面可能有 %s 个狼，没有 %d，<span class="r">不行</span>' % (' 或 '.join(map(str, sorted(set(cand)))) if cand else '（没有）', b[i]))
        if Wf[i] is not None:
            why.append('当狼：%s，<span class="g">可以</span>，算上他一共 %d 个狼' % ('他是第一个人' if i == 0 else '前一个人能当村民', Wf[i]))
        else:
            why.append('当狼：前一个人当不了村民，狼会挨着，<span class="r">不行</span>')
        fr.append((draw(i), '第 %d 人（L %d）。' % (i + 1, b[i]) + '；'.join(why) + '。'))
    # 回溯
    ans = [None] * n
    state = 'V' if V[-1] is not None else 'W'
    cur = V[-1] if state == 'V' else Wf[-1]
    for i in range(n - 1, -1, -1):
        if state == 'V':
            ans[i] = 0
            if i > 0:
                if V[i - 1] is not None and V[i - 1] == V[i]:
                    state = 'V'
                else:
                    state = 'W'
        else:
            ans[i] = 1
            state = 'V'
    w = ans
    ok, why = valid(w, d, b)
    assert ok, (w, why)
    fr.append((draw(n - 1), '填完了，从最后一个人往回走：第 6 人能当村民；再看谁能接上……得到 <b>%s</b>。用 checker 的规则验一遍：%s' % (''.join(map(str, w)), why)))
    return fp('d_dp', '动画 D2 · 子任务 2（全往左看）不用分类讨论：两状态 DP', fr, '绿格 = 这个状态可以，红格 = 不行。每一格都是程序填的，最后的答案用 checker 的判定函数验过。')


def build():
    h = []
    h.append('<h2 id="D">D 🐺　<span class="bdg bdg-w">0 分：TLE，然后 CE</span><span class="kaodian">小状态 DP · 枚举总狼数</span></h2>')
    h.append('<div class="method"><b>一句话题意：</b>村民说真话、狼随便说、狼不相邻。第 i 个人说“我左边 / 右边有 bᵢ 个狼”。给出任意一种合法的分布，或者判无解。</div>')
    h.append('<div class="mind real">12:12 <span class="qq">“假设所有人说的都是真话……一旦不单调……特殊情况太多了。”</span>12:57 <span class="qq">“列出所有的情况，总共 8 种……还是太复杂了，只能拿个十分三十分。”</span>13:53 <span class="qq">“我用 checker 来写。”</span><br>赛后你说：<span class="qq">“D 题直接搬 checker，但是没搞懂为什么不对。”</span><span class="qq">“情况太多，分类讨论全不对。”</span></div>')
    h.append('<p>搬 checker 的判定函数是非常好的做法。问题出在枚举那一行：</p>')
    h.append(d_bug())
    h.append('<div class="trap"><b>【触发】</b>枚举 n 位的 0/1 分布　<b>【判据】</b><code>for (int k = 0; k &lt; n; k++) w[k] = mask &gt;&gt; k &amp; 1;</code>，每次都取满 n 位。不要用 “while (t != 0)” 按 mask 自己的位数取。</div>')
    h.append('<div class="trap"><b>【触发】</b>题面样例过了　<b>【判据】</b>样例只有几组，恰好测不到很正常。下载了大样例就一定要跑：这题的 sample2 就是子任务 1 的 1000 组数据，一跑就知道。</div>')
    h.append('<div class="sq">14:09 那版为什么 CE</div>')
    h.append('<p><code>solve</code> 里调用了 <code>solve2</code>，可 <code>solve2</code> 写在 <code>solve</code> 下面，没声明，编译错误。桌面上的 <code>T4</code> 可执行文件是 14:00 编译的，<code>T4.cpp</code> 是 14:09 改的，<b>交之前没编译</b>。而且 <code>if (n &gt; 20) solve2 (n);</code> 后面没有 return，就算编译过了也还会接着跑 2ⁿ。新 bag 里的 <code>check.sh</code> 就是防这个的。</p>')
    h.append('<div class="sq">“情况太多，分类讨论全不对”——换一种想法</div>')
    h.append('<div class="think">12:57 你在列“三个人之间有几种情况”，列到 8 种就乱了。分类讨论是在想“一段人整体长什么样”，情况会越列越多。换成 DP 只想“<b>一个人</b>”：他要么是村民，要么是狼；每种情况下“前面有几个狼”是确定的；再看前一个人的状态能不能接上。两种状态，从左到右填一遍。</div>')
    h.append(d_dp())
    h.append('<div class="trap"><b>【触发】</b>分类讨论超过四五种还在长　<b>【判据】</b>停下来，改成“每个位置几种状态 + 前一个状态能不能接过来”的 DP。</div>')
    h.append('<div class="sq">满分做法（供了解）</div>')
    h.append('<div class="think">有人往右看时，“后面有几个狼”要用总狼数 W 换成“前面有 W − b 个狼”。W 不知道怎么办？看相邻两个村民：都往左看、都往右看时，能不能接上和 W 无关；<b>一个往左一个往右时，只有一个 W 能接上</b>（W = 两人的 b 加起来，再加 / 减中间的狼）。所以只有 O(n) 个 W 值得试，每试一个只打开几条边，用线段树维护“能不能从头走到尾”。和穷举对拍 10500 组全对，代码 <code>正解代码/D_狼人.cpp</code>。这是这场最难的一步，现阶段拿到子任务 1、2 的 25 分就够了。</div>')
    return '\n'.join(h)
