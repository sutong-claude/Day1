from vcommon import *

A = 27
BITS = [A >> k & 1 for k in range(5)]          # 低位在前：1 1 0 1 1
INF = 10 ** 9


def dp_table():
    f = [(0, INF)]
    par = []
    for k in range(5):
        f0, f1 = f[-1]
        g = [INF, INF]
        pg = [None, None]
        for c, fc in ((0, f0), (1, f1)):
            if fc >= INF:
                continue
            v = BITS[k] + c
            opts = []
            if v == 0:
                opts = [(0, 0, 0)]
            elif v == 1:
                opts = [(0, 1, +1), (1, 1, -1)]
            else:
                opts = [(1, 0, 0)]
            for nc, add, dg in opts:
                if fc + add < g[nc]:
                    g[nc] = fc + add
                    pg[nc] = (c, dg)
        f.append(tuple(g))
        par.append(pg)
    return f, par


F, PAR = dp_table()
assert min(F[-1][0], F[-1][1] + 1) == 3


def path_cost(digits):
    """digits: {位: ±1}。返回每一列之后的 (进位, 累计项数)"""
    c, cost, out = 0, 0, []
    for k in range(5):
        v = BITS[k] + c
        d = digits.get(k, 0)
        assert (v - d) % 2 == 0
        c = (v - d) // 2
        cost += (d != 0)
        out.append((c, cost))
    return out


class AMul(Base):
    def construct(self):
        self.head('A 乘法：DP 为什么一定对')
        f1 = T('x × 15 = (x << 4) − (x << 0)', 26, mono=True).move_to([-3.4, 2.4, 0])
        f2 = T('2 项：2 次左移 + 1 次减法 = 3', 24).next_to(f1, DOWN, buff=0.3)
        f3 = T('k 项 → 答案 = 2k − 1', 26, YELLOW).next_to(f2, DOWN, buff=0.35)
        self.play(FadeIn(f1))
        self.say('题目：用若干个 ±2ᵏ 凑出 a。每一项要左移一次，项和项之间要加减一次。')
        self.play(FadeIn(f2), FadeIn(f3))
        self.say('所以 k 项的代价是 2k − 1，问题变成：最少用几项。你 10:15 就推出来了。')
        self.step('① 答案 = 2 × 项数 − 1')

        g1 = T('2³ + 2³ = 2⁴　两项并成一项，更少', 23).move_to([-3.4, 0.6, 0])
        g2 = T('2³ − 2³ = 0　　两项都删掉，更少', 23).next_to(g1, DOWN, buff=0.3)
        g3 = T('⇒ 最少的写法里，每个 2ᵏ 最多出现一次', 23, YELLOW).next_to(g2, DOWN, buff=0.4)
        g4 = T('⇒ 每一位只能填 −1、0、+1', 23, YELLOW).next_to(g3, DOWN, buff=0.2)
        self.play(FadeIn(g1), FadeIn(g2))
        self.say('先想清楚“一种写法”长什么样。同一个 2ᵏ 用两次一定不划算：同号可以并成一项，异号可以一起删掉。')
        self.play(FadeIn(g3), FadeIn(g4))
        self.say('所以最少的写法，就是给每一位填 −1、0、+1 中的一个，让总和等于 a，非零的位越少越好。')
        self.step('② 每一位只能填 −1 / 0 / +1')
        self.play(FadeOut(VGroup(f1, f2, f3, g1, g2, g3, g4)))

        # 27 的三行
        xs = {k: -5.9 + (5 - k) * 1.0 for k in range(6)}
        lab_pow = VGroup(*[T('2%s' % '⁰¹²³⁴⁵'[k], 20, GREY_B).move_to([xs[k], 2.7, 0]) for k in range(6)])
        row_a = VGroup(*[box(str(A >> k & 1), 0.7, 0.55, size=24).move_to([xs[k], 2.15, 0]) for k in range(6)])
        la = T('27 =', 22).move_to([-6.75, 2.15, 0])
        self.play(FadeIn(lab_pow), FadeIn(row_a), FadeIn(la))
        self.say('拿你 13:06 那版的反例来看：a = 27，二进制 11011。')
        v4 = {5: 1, 3: -1, 2: 1, 0: -1}
        best = {5: 1, 2: -1, 0: -1}

        def drow(dig, y, color):
            g = VGroup()
            for k in range(6):
                d = dig.get(k, 0)
                s = {1: '+1', -1: '−1', 0: '0'}[d]
                g.add(box(s, 0.7, 0.55, color=color if d else GREY_D, fill=color if d else None, size=22).move_to([xs[k], y, 0]))
            return g
        r4 = drow(v4, 1.2, RED)
        l4 = T('v4', 22, RED).move_to([-6.75, 1.2, 0])
        t4 = T('32 − 8 + 4 − 1 = 27　4 项 → 7 ✗', 22, RED).move_to([-3.4, 0.55, 0])
        self.play(FadeIn(r4), FadeIn(l4), FadeIn(t4))
        self.say('你的 v4：前面一段 11 用 +2⁵ −2³，后面一段 11 用 +2² −2⁰，一共 4 项，输出 7。')
        self.step('③ v4：11011 拆成 4 项，输出 7 ✗')
        rb = drow(best, -0.3, GREEN)
        lb = T('更好', 22, GREEN).move_to([-6.75, -0.3, 0])
        tb = T('32 − 4 − 1 = 27　3 项 → 5 ✓', 22, GREEN).move_to([-3.4, -0.95, 0])
        self.play(FadeIn(rb), FadeIn(lb), FadeIn(tb))
        self.say('更好的写法：整段用 2⁵ 盖住，再减掉 2² 和 2⁰，只要 3 项，答案是 5。中间那个 0 被吞进来了。')
        self.step('④ 更好：2⁵ − 2² − 2⁰，3 项')
        self.say('问题是：怎么保证找到最好的那一种？靠观察规律容易漏，DP 可以把所有填法都试一遍。')
        self.play(FadeOut(VGroup(lab_pow, row_a, la, r4, l4, t4, rb, lb, tb)))

        # DP 表
        cx = [-5.55 + j * 1.0 for j in range(6)]
        hdr = VGroup(T('开始', 19, GREY_B).move_to([cx[0], 2.75, 0]))
        bitv = VGroup(T(' ', 19).move_to([cx[0], 2.35, 0]))
        for k in range(5):
            hdr.add(T('第%d位' % k, 19, GREY_B).move_to([cx[k + 1], 2.75, 0]))
            bitv.add(T('原来 %d' % BITS[k], 19).move_to([cx[k + 1], 2.35, 0]))
        rl = VGroup(T('进位 0', 20).move_to([-6.6, 1.55, 0]), T('进位 1', 20).move_to([-6.6, 0.55, 0]))
        rules = VGroup(
            T('这一位 v = 原来的位 + 进位：', 20, GREY_B),
            T('v = 0 → 填 0，进位 0，不加项', 20),
            T('v = 1 → 填 +1（进位 0）或 −1（进位 1），+1 项', 20),
            T('v = 2 → 填 0，进位 1，不加项', 20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-6.85, -1.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(hdr), FadeIn(bitv), FadeIn(rl))
        self.say('从最低位往高位填。表里每一格记：做到这一位、往上一位进位 0 或 1 时，最少用了几项。')
        self.play(FadeIn(rules))
        self.say('为什么会有进位？填 −1 相当于这一位多借了 2，要往上一位进 1。进位只可能是 0 或 1。')
        self.step('⑤ DP：从低位填，只记进位 0 / 1')
        cells = {}
        all_arrs = VGroup()

        def cell(j, c, val):
            s = '∞' if val >= INF else str(val)
            return box(s, 0.7, 0.6, color=BLUE, size=24).move_to([cx[j], 1.55 - c, 0])
        c0, c1 = cell(0, 0, 0), cell(0, 1, INF)
        cells[(0, 0)], cells[(0, 1)] = c0, c1
        self.play(FadeIn(c0), FadeIn(c1))
        self.say('开始时什么都没填，进位是 0，用了 0 项；进位 1 不可能，记 ∞。')
        notes = {
            0: '第 0 位原来是 1，进位 0：v = 1。填 +1 到“进位 0”，填 −1 到“进位 1”，都是 1 项。',
            1: '第 1 位原来是 1。从进位 0 来：v = 1，两种都 +1 项，得 2；从进位 1 来：v = 2，填 0 进位 1，还是 1 项。',
            2: '第 2 位原来是 0。从进位 0 来：v = 0，不加项；从进位 1 来：v = 1，+1 项。两格都是 2。',
            3: '第 3 位原来是 1。进位 1 这格：从进位 1 来，v = 2，不加项，还是 2。',
            4: '第 4 位原来是 1。同样，进位 1 这格一直是 2。',
        }
        for k in range(5):
            j = k + 1
            a0 = cell(j, 0, F[j][0])
            a1 = cell(j, 1, F[j][1])
            cells[(j, 0)], cells[(j, 1)] = a0, a1
            arrs = VGroup()
            for nc in (0, 1):
                p = PAR[k][nc]
                if p is None:
                    continue
                c, dg = p
                st = cells[(j - 1, c)].get_right()
                en = (a0 if nc == 0 else a1).get_left()
                arrs.add(Arrow(st, en, buff=0.05, stroke_width=3, max_tip_length_to_length_ratio=0.2, color=GREY_B))
            all_arrs.add(arrs)
            self.play(FadeIn(a0), FadeIn(a1), FadeIn(arrs), run_time=0.8)
            self.say(notes[k])
        self.step('⑥ v=0 填 0；v=1 填 ±1；v=2 填 0 进位 1')
        fin = VGroup(T('最后还剩进位 1 → 再补一项 +2⁵', 21, YELLOW),
                     T('min(4, 2 + 1) = 3 项 → 答案 5', 21, YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-6.85, -0.5, 0], aligned_edge=LEFT)
        self.play(FadeOut(rules), FadeIn(fin))
        self.say('做完第 4 位：进位 0 要 4 项；进位 1 要 2 项，但还欠一个 2⁵，所以 3 项。答案 2×3−1 = 5。')
        # 最优路径
        path = [(0, 0)]
        c = 1
        for k in range(4, -1, -1):
            path.append((k + 1, c))
            c = PAR[k][c][0]
        best_boxes = VGroup(*[SurroundingRectangle(cells[p], color=GREEN, buff=0.04) for p in path])
        self.play(Create(best_boxes))
        self.say('绿框是最好的那条路：第 0 位填 −1，第 2 位填 −1，最后进位变成 +2⁵，正好就是 2⁵ − 2² − 2⁰。')
        # v4 路径
        pc = path_cost(v4)
        v4b = VGroup(*[SurroundingRectangle(cells[(k + 1, pc[k][0])], color=RED, buff=0.1) for k in range(5)])
        ann = VGroup(T('v4 走到“第 3 位、进位 1”用了 %d 项' % pc[3][1], 21, RED),
                     T('这一格最少只要 %d 项 → 被比下去' % F[4][1], 21, RED)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-6.85, -0.5, 0], aligned_edge=LEFT)
        self.play(Create(v4b), FadeOut(fin), FadeIn(ann))
        self.say('你的 v4 也是表里的一条路（红框）。走到“第 3 位、进位 1”时它用了 3 项，而这一格最少只要 2 项，所以它被比下去了。')
        why = VGroup(
            T('每一种填法 = 表里从左到右的一条路', 21, YELLOW),
            T('同一格（同一位、同一进位）后面怎么走完全一样', 21, YELLOW),
            T('⇒ 每格只留最少的，不会漏掉最优', 21, YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-6.85, -1.75, 0], aligned_edge=LEFT)
        for m in why:
            if m.width > 7.2:
                m.scale_to_fit_width(7.2)
        self.play(FadeIn(why))
        self.say('为什么 DP 一定对：任何一种写法都是表里的一条路；走到同一格以后，剩下的路一模一样，所以只留项数最少的那条就够了。')
        self.step('⑦ 每种填法都是一条路 ⇒ 一定不漏')
        self.play(FadeOut(VGroup(hdr, bitv, rl, *cells.values(), best_boxes, v4b, ann, fin, why, all_arrs)))

        # 贪心
        gr = VGroup(
            T('你最后 AC 的贪心（从高位往低位扫）：', 21, GREY_B),
            T('单独的 1 → 1 项', 22),
            T('连续的 1 → 2 项（高一位减最低位）', 22),
            T('段中间夹一个 0 → 再 +1 项，接着往下', 22),
            T('遇到 00 → 这一段结束', 22),
            T('11011：2 项 + 中间一个 0 的 1 项 = 3 项 ✓', 22, GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-6.85, 1.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(gr[:5]))
        self.say('你 13:33 最后 AC 的那版是贪心，它其实就是这张表的规律。')
        self.play(FadeIn(gr[5]))
        self.say('一段连续的 1，就是表里“进位一直是 1”的一段；中间夹一个 0，进位 1 走过去只多 1 项；遇到 00 再往上带进位要多花项，所以在这里断开最划算。')
        chk = VGroup(T('对拍：1 ～ 4095 全部 + 随机', 21, YELLOW),
                     T('共 5295 个数，和 DP 答案全部一致', 21, YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-6.85, -1.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(chk))
        self.say('规律是靠观察猜出来的，所以要用 DP 或暴力对拍来确认：5295 个数全部一致。')
        self.step('⑧ 你的贪心 = 这张表的规律，对拍一致')
        self.say('小结：DP 不靠灵感——把每一位的 −1/0/+1 都试一遍，进位只有 0 和 1 两种，所以 10⁶ 位也只要 2×10⁶ 格。', extra=1.0)
