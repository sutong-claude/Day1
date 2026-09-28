from vcommon import *

S1 = '4336352375'
N = len(S1)
X, Y = [0], [0]
for ch in S1:
    v = int(ch)
    X.append(X[-1] + (v >> 2 & 1) - (v >> 1 & 1))
    Y.append(Y[-1] + (v >> 2 & 1) - (v & 1))
F = [0] * (N + 1)
for i in range(1, N + 1):
    F[i] = F[i - 1]
    for j in range(i):
        if X[j] <= X[i] and Y[j] <= Y[i]:
            F[i] = max(F[i], F[j] + i - j)
G = [F[j] - j for j in range(N + 1)]
assert F[N] == 7

U = 0.72


def PT(x, y):
    return np.array([-4.3 + x * U, 1.45 + y * U, 0])


class CChess(Base):
    def construct(self):
        self.head('C 棋子：你的 O(n²) DP 怎么优化')
        yc = code_block([
            'for (int i = 1; i <= n; i++) {',
            '    f[i] = f[i - 1];',
            '    for (int j = 0; j < i; j++)',
            '        if (段 (j, i] 是好的)',
            '            f[i] = max (f[i], f[j] + i - j);',
            '}',
        ], size=20, colors={2: RED}).move_to([-6.85, 1.8, 0], aligned_edge=LEFT)
        self.play(FadeIn(yc))
        self.say('先说结论：你的 DP 是对的，拿到 30 分也说明了这一点。慢只慢在一个地方：每个 i 都把前面所有 j 扫一遍。')
        self.step('① 你的 DP 对，慢在“每个 i 扫所有 j”')
        idea = T('优化 DP 的套路：别扫所有 j，把“要找的那个 j”交给数据结构', 21, YELLOW).move_to([-3.4, -0.5, 0])
        if idea.width > 7.1:
            idea.scale_to_fit_width(7.1)
        self.play(FadeIn(idea))
        self.say('优化这种 DP 有个固定套路：先把条件和式子改写，改到“在满足某些条件的 j 里求最大值”，然后交给数据结构。一步一步来。')
        self.play(FadeOut(VGroup(yc, idea)))

        # ② 条件改写
        c1 = T('好段：段内 a 的个数 ≥ b 的个数，且 ≥ c 的个数', 21).move_to([-6.85, 2.5, 0], aligned_edge=LEFT)
        c2 = T('X[i] = 前 i 格 (a − b)，Y[i] = 前 i 格 (a − c)', 21, mono=False).next_to(c1, DOWN, buff=0.3, aligned_edge=LEFT)
        c3 = T('段内 a − b = X[i] − X[j] ≥ 0  ⇔  X[j] ≤ X[i]', 21).next_to(c2, DOWN, buff=0.3, aligned_edge=LEFT)
        c4 = T('好段 (j, i]  ⇔  X[j] ≤ X[i] 且 Y[j] ≤ Y[i]', 23, YELLOW).next_to(c3, DOWN, buff=0.35, aligned_edge=LEFT)
        for m in (c1, c2, c3, c4):
            if m.width > 7.1:
                m.scale_to_fit_width(7.1)
        self.play(FadeIn(c1))
        self.play(FadeIn(c2))
        self.say('第一步改条件。你 12:01 说“只要知道 a − b 的值、a − c 的值”，就是这个：用前缀和 X、Y。')
        self.play(FadeIn(c3))
        self.say('段内 a − b 等于两个前缀相减，它 ≥ 0，就是 X[j] ≤ X[i]。另一个条件同理。')
        self.play(FadeIn(c4))
        self.step('② 好段 ⇔ X[j] ≤ X[i] 且 Y[j] ≤ Y[i]')

        # ③ 式子改写
        e1 = T('f[j] + i − j  =  i + (f[j] − j)', 24, mono=True).move_to([-3.4, -0.45, 0])
        e2 = T('记 g[j] = f[j] − j　（你 12:04 想到的 i − f[i]，差个符号）', 20, GREY_B).next_to(e1, DOWN, buff=0.25)
        for m in (e2,):
            if m.width > 7.1:
                m.scale_to_fit_width(7.1)
        self.play(FadeIn(e1))
        self.say('第二步改式子。i 对所有 j 都一样，拿出来；剩下的 f[j] − j 只和 j 有关，叫它 g[j]。')
        self.play(FadeIn(e2))
        self.say('你 12:04 说“i 减去 f[i]”，已经摸到这一步了。')
        self.step('③ f[j] + i − j = i + g[j]，g[j] = f[j] − j')
        self.play(FadeOut(VGroup(c1, c2, c3, e1, e2)), c4.animate.move_to([-6.85, 2.9, 0], aligned_edge=LEFT))
        goal = VGroup(
            T('f[i] = max( f[i−1],  i + 最大的 g[j] )', 22, YELLOW),
            T('其中 j 满足 X[j] ≤ X[i] 且 Y[j] ≤ Y[i]', 22, YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-6.85, 2.15, 0], aligned_edge=LEFT)
        self.play(FadeIn(goal))
        self.say('现在 DP 变成了：在满足两个条件的 j 里，找最大的 g[j]。这就是“查询”，不再需要一个一个试。')
        self.play(FadeOut(c4))

        # 表
        tx = [-6.2 + k * 0.6 for k in range(N + 1)]
        labs = ['j', 'X', 'Y', 'g']
        vals = [list(range(N + 1)), X, Y, G]
        tab = VGroup()
        for r, (lb, vs) in enumerate(zip(labs, vals)):
            y = 1.05 - r * 0.36
            tab.add(T(lb, 19, GREY_B if r < 3 else YELLOW).move_to([-6.7, y, 0]))
            for k in range(N + 1):
                tab.add(T(str(vs[k]).replace('-', '−'), 19, YELLOW if r == 3 else WHITE, mono=True).move_to([tx[k], y, 0]))
        self.play(FadeIn(tab))
        self.say('用样例 1（4336352375）算出来：每个位置的 X、Y，和 DP 跑完以后的 g。')
        self.play(FadeOut(tab))

        # ④ 平面上的点
        grid = VGroup()
        for x in range(-3, 2):
            grid.add(Line(PT(x, -2.4), PT(x, 1.4), color=GREY_D, stroke_width=1))
            grid.add(T(str(x).replace('-', '−'), 16, GREY_B).move_to(PT(x, -2.4) + DOWN * 0.2))
        for y in range(-2, 2):
            grid.add(Line(PT(-3.4, y), PT(1.4, y), color=GREY_D, stroke_width=1))
            grid.add(T(str(y).replace('-', '−'), 16, GREY_B).move_to(PT(-3.4, y) + LEFT * 0.2))
        grid.add(T('X', 18, GREY_B).move_to(PT(1.4, -2.4) + RIGHT * 0.25), T('Y', 18, GREY_B).move_to(PT(-3.4, 1.4) + UP * 0.2))
        groups = {}
        for j in range(N + 1):
            groups.setdefault((X[j], Y[j]), []).append(j)
        dots, dlab = {}, VGroup()
        for (x, y), js in groups.items():
            d = Dot(PT(x, y), radius=0.08, color=WHITE)
            dots[(x, y)] = d
            dlab.add(T('j=' + ','.join(map(str, js)), 15, GREY_A).next_to(d, UR, buff=0.04))
        self.play(FadeOut(goal), FadeIn(grid))
        self.play(FadeIn(VGroup(*dots.values())), FadeIn(dlab))
        self.say('把每个 j 画成一个点 (X[j], Y[j])。两个条件合起来，在图上就是：点在 i 的左下方。')
        self.step('④ 条件 = 点在 i 的左下方')

        def query(i):
            qi = PT(X[i], Y[i])
            rect = Polygon(PT(-3.4, -2.4), PT(X[i], -2.4), qi, PT(-3.4, Y[i]), color=YELLOW, fill_color=YELLOW, fill_opacity=0.15, stroke_width=2)
            cand = [j for j in range(i) if X[j] <= X[i] and Y[j] <= Y[i]]
            star = Star(n=5, outer_radius=0.17, color=RED, fill_opacity=1).move_to(qi)
            return rect, cand, star

        info = VGroup()
        for i in (6, 10):
            rect, cand, star = query(i)
            best = max(cand, key=lambda j: G[j])
            mm = lambda t: t.replace('-', '−')
            lines = VGroup(
                T(mm('i = %d：点 (%d, %d)' % (i, X[i], Y[i])), 21, RED),
                T('左下方且 j < i：j = ' + ', '.join(map(str, cand)), 21),
                T(mm('最大 g = g[%d] = %d' % (best, G[best])), 21, YELLOW),
                T(mm('f[%d] = max(%d, %d + (%d)) = %d' % (i, F[i - 1], i, G[best], F[i])), 21, YELLOW),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            lines.move_to([-6.85, -0.75, 0], aligned_edge=UL)
            self.play(FadeOut(info), FadeIn(rect), FadeIn(star))
            info = lines
            hl = VGroup(*[Circle(radius=0.17, color=GREEN, stroke_width=3).move_to(PT(X[j], Y[j])) for j in set(cand)])
            self.play(FadeIn(lines[:2]), Create(hl))
            if i == 6:
                self.say('i = 6 在 (−1, −1)，黄色是它的左下方。里面有 j = 3 和 j = 5，g[3] = −1 更大，所以 f[6] = 6 − 1 = 5。')
            else:
                self.say('i = 10 在 (−2, −2)。左下方是 j = 8、9，g 都是 −3，f[10] = 10 − 3 = 7，就是样例答案。')
            self.play(FadeIn(lines[2:]))
            self.wait(1.2)
            self.play(FadeOut(rect), FadeOut(star), FadeOut(hl))
        self.step('⑤ 每个 i：查左下方的最大 g，再把自己的 g 放进去')
        self.say('所以要的是一个结构：能“放进一个点”，能“问某个点左下方的最大 g”。先看简单版。')
        self.play(FadeOut(VGroup(grid, *dots.values(), dlab, info)))

        # ⑥ 一个条件：树状数组
        s1 = T('如果只有一个条件 X[j] ≤ X[i]：', 21).move_to([-6.85, 2.75, 0], aligned_edge=LEFT)
        bit = code_block([
            'void add (int x, int v) {',
            '    for (; x <= m; x += x & -x)',
            '        t[x] = max (t[x], v);',
            '}',
            'int ask (int x) {       // 1..x 里的最大值',
            '    int r = -INF;',
            '    for (; x; x -= x & -x)',
            '        r = max (r, t[x]);',
            '    return r;',
            '}',
            '// X 加上 n 变成正数再当下标',
            'f[i] = max (f[i - 1], i + ask (X[i]));',
            'add (X[i], f[i] - i);',
        ], size=17, colors={10: GREY_B, 11: YELLOW, 12: YELLOW}).next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1), FadeIn(bit))
        self.say('只有一个条件时，“左下方”变成“左边”：用 X 当下标的树状数组，存前缀最大值。i 从小到大做，先问再放，j < i 自动满足。')
        self.step('⑥ 一个条件：树状数组前缀最大，O(n log n)')
        self.play(FadeOut(VGroup(s1, bit)))

        # ⑦ 两个条件：CDQ
        t2 = VGroup(
            T('两个条件 + 只能用 j < i 的点', 22),
            T('= 三维偏序（时间、X、Y）', 22, YELLOW),
            T('CDQ 分治：按时间对半分，左半的点更新右半', 21),
            T('每层按 X 排序，树状数组管 Y', 21),
            T('O(n log²n)：n ≤ 2×10⁵ 能过 → 60 分', 22, GREEN),
            T('练习：洛谷 P3810【模板】三维偏序', 21, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-6.85, 1.3, 0], aligned_edge=LEFT)
        for m in t2:
            if m.width > 7.1:
                m.scale_to_fit_width(7.1)
        self.play(FadeIn(t2[:2]))
        self.say('两个条件时，树状数组只能管一维。再加上“j 要在 i 前面”，一共三个不等式，这就是三维偏序。')
        self.play(FadeIn(t2[2:4]))
        self.say('标准做法是 CDQ 分治：按下标对半分，先算左半，再用左半的点去更新右半，排序管 X、树状数组管 Y。')
        self.play(FadeIn(t2[4:]))
        self.say('复杂度 n log² n，n = 2×10⁵ 的部分分能过，从 30 分到 60 分。先把 P3810 做了，这个模板就会了。')
        self.step('⑦ 两个条件：CDQ + 树状数组 → 60 分')
        self.play(FadeOut(t2))

        t3 = VGroup(
            T('n = 2×10⁶：要用这题特有的性质', 22),
            T('有 a 的格子：X、Y 都不减（往右上走）', 21),
            T('没 a 的格子：X、Y 都不增（往左下走）', 21),
            T('⇒ 每行、每列各维护有序表，O(n log n)', 21, YELLOW),
            T('细节在复盘报告和正解代码里，现阶段拿 60 就够', 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-6.85, 1.5, 0], aligned_edge=LEFT)
        self.play(FadeIn(t3))
        self.say('满分要用这题的特殊结构：点每一步要么往右上走、要么往左下走。这部分难度超过你现在的目标，知道有这回事就行。')
        self.step('⑧ 满分：两维同向走的特殊结构')
        self.play(FadeOut(t3))
        rec = VGroup(
            T('以后遇到 O(n²) 的 DP：', 22, YELLOW),
            T('1. 把式子里只和 j 有关的并成一个量 g[j]', 21),
            T('2. 把“j 能不能转移”写成几个不等式', 21),
            T('3. 几个不等式 → 几维的“求最大值”', 21),
            T('　一维：树状数组 / 单调队列；二维：CDQ', 21),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-6.85, 1.5, 0], aligned_edge=LEFT)
        self.play(FadeIn(rec))
        self.say('总结成套路：拆式子、写条件、数维数。你 12:01 和 12:04 已经做完了前两步，差的是第三步——知道这叫偏序，该用什么结构。', extra=1.0)
