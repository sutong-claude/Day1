from vcommon import *

STRS = ['a', 'ab', 'abc', 'abcd']
CS = 0.6
GX, GY = -5.4, 2.2          # 格子 (d=1, j=1) 的中心


def P(d, j):
    return np.array([GX + (j - 1) * CS, GY - (d - 1) * CS, 0])


def simulate():
    """按正解代码跑一遍，记录每个串插入时的事件"""
    ch, cnt, mx, f = [{}], [0], {}, {}
    ans, out = 0, []
    for i, s in enumerate(STRS, 1):
        ev = {'i': i, 'new': (i, ans, ans + (0 ^ i)), 'chg': []}
        ans += 0 ^ i
        u = 0
        for d in range(len(s) + 1):
            if d > 0:
                c = s[d - 1]
                if c not in ch[u]:
                    ch.append({}); cnt.append(0); ch[u][c] = len(ch) - 1
                u = ch[u][c]
            cnt[u] += 1
            if cnt[u] > mx.get(d, 0):
                mx[d] = cnt[u]
                j = mx[d]
                if d > 0:
                    old = f.get(j, 0)
                    if d > old:
                        a0 = ans
                        ans += -(old ^ j) + (d ^ j)
                        f[j] = d
                        ev['chg'].append((d, j, old, d, a0, ans))
        ev['ans'] = ans
        out.append(ev)
    return out


EV = simulate()
assert [e['ans'] for e in EV] == [0, 6, 4, 12]


class BYarn(Base):
    def construct(self):
        self.head('B 毛线：为什么不用每次重算每个 f')
        d1 = T('f(i, j)：前 i 个串里挑 j 个，公共前缀最长能多长', 22).move_to([-6.85, 2.5, 0], aligned_edge=LEFT)
        d2 = T('第 i 行输出：Σ f(i, j) xor j　（j = 1 … i）', 22).next_to(d1, DOWN, buff=0.25, aligned_edge=LEFT)
        for m in (d1, d2):
            if m.width > 7.1:
                m.scale_to_fit_width(7.1)
        self.play(FadeIn(d1), FadeIn(d2))
        self.say('先把题意说清：对每个 i，挑 j 个串，让它们的公共前缀尽量长，这个长度叫 f(i, j)。')
        e1 = VGroup(
            T('i = 2，串是 a、ab：', 22, GREY_B),
            T('挑 1 个：挑 ab，自己和自己，长度 2', 22),
            T('挑 2 个：a 和 ab，公共前缀 a，长度 1', 22),
            T('(2 xor 1) + (1 xor 2) = 3 + 3 = 6 ✓', 22, YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-6.85, 0.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(e1))
        self.say('样例 1 的第二行：挑 1 个时选 ab 最长是 2；挑 2 个只能是 a 和 ab，长度 1。加起来 6，和样例一样。')
        self.step('① f(i, j)：挑 j 个串的最长公共前缀')
        self.play(FadeOut(VGroup(d1, d2, e1)))

        # ② mx[d] 和格子图（i = 4 的最终状态）
        mxf = {1: 4, 2: 3, 3: 2, 4: 1}
        rowlab = VGroup(*[T('第%d层' % d, 19, GREY_B).move_to(P(d, 1) + LEFT * 1.0) for d in range(1, 5)])
        full = VGroup()
        for d in range(1, 5):
            for j in range(1, mxf[d] + 1):
                full.add(Square(CS * 0.9, color=BLUE, fill_color=BLUE, fill_opacity=0.35, stroke_width=2).move_to(P(d, j)))
        strs = T('串：a　ab　abc　abcd', 22, mono=True).move_to([-6.85, 2.85, 0], aligned_edge=LEFT)
        self.play(FadeIn(strs), FadeIn(rowlab))
        self.say('你 11:45 的想法是对的：每一层求个最大值。第 d 层的 mx[d] 就是“前 d 个字母完全一样的串，最多有几个”。')
        for d in range(1, 5):
            row = VGroup(*[m for m in full if abs(m.get_center()[1] - P(d, 1)[1]) < 1e-6])
            self.play(FadeIn(row), run_time=0.5)
        note = VGroup(
            T('第 d 行的格子数 = mx[d]', 20),
            T('第 1 层：a 开头的有 4 个', 20, GREY_B),
            T('第 4 层：abcd 开头的只有 1 个', 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.1, 1.05, 0], aligned_edge=LEFT)
        self.play(FadeIn(note))
        self.say('把 mx[d] 画成一行格子：i = 4 时，第 1 层 4 个，第 2 层 3 个，第 3 层 2 个，第 4 层 1 个。越往下只会越少。')
        self.step('② mx[d]：前 d 个字母一样的串最多几个')
        colbox = SurroundingRectangle(VGroup(*[m for m in full if abs(m.get_center()[0] - P(1, 2)[0]) < 1e-6]), color=YELLOW, buff=0.06)
        self.play(Create(colbox))
        self.say('现在要挑 j = 2 个串：能走到第 d 层，当且仅当这一层的格子数 ≥ 2。所以 f(2) 就是第 2 列有几个格子——3。')
        self.step('③ f(j) = 第 j 列的高度（mx[d] ≥ j 的层数）')
        self.play(FadeOut(VGroup(full, colbox, note, strs, rowlab)))

        # ④ 你的做法
        yc = code_block([
            'for (int i = 1; i <= n; i++) {',
            '    // 插入第 i 个串，更新 mx',
            '    for (int j = 1; j <= i; j++)',
            '        ans += f(j) ^ j;   // 每次全算',
            '}',
        ], size=19, colors={2: RED, 3: RED}).move_to([-6.85, 1.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(yc))
        self.say('你卡在这：11:49 你说“我能算出每一个，但复杂度差得远”。因为每个 i 都要把 j = 1 到 i 全部重算一遍。')
        cost = T('1 + 2 + … + n ≈ n²/2 ≈ 1.25×10¹¹', 22, RED).move_to([-3.4, -0.7, 0])
        self.play(FadeIn(cost))
        self.say('一共 n²/2 次，n = 5×10⁵ 时超过 10¹¹，肯定超时。')
        self.step('④ 你：每个 i 重算 j = 1…i → n²/2')
        k1 = T('关键：和一直存着，只改“变了的那几列”', 22, YELLOW).move_to([-3.4, -1.4, 0])
        if k1.width > 7.1:
            k1.scale_to_fit_width(7.1)
        self.play(FadeIn(k1))
        self.say('其实每个 f 都在数组里存着，不用重求。插入一个串以后，大部分列根本没变，没变的列不碰，它们在和里的那份原样留着。')
        self.play(FadeOut(VGroup(yc, cost, k1)), FadeIn(rowlab))

        # ⑤⑥ 从空开始逐个插入
        colj = {}
        fval = {}
        sumt = T('和 = 0', 30, YELLOW).move_to([-1.3, 2.3, 0])
        logs = VGroup()
        self.play(FadeIn(sumt))
        cells = VGroup()
        mxc = {d: 0 for d in range(1, 5)}
        self.say('现在从空开始，一个一个插入 a、ab、abc、abcd，看格子和和怎么变。')

        def set_sum(v):
            nonlocal sumt
            ns = T('和 = %d' % v, 30, YELLOW).move_to(sumt.get_center())
            return ReplacementTransform(sumt, ns), ns

        def add_log(t, color=WHITE):
            m = T(t, 19, color, mono=True)
            if logs:
                m.next_to(logs[-1], DOWN, buff=0.13, aligned_edge=LEFT)
            else:
                m.move_to([-2.85, 1.65, 0], aligned_edge=LEFT)
            logs.add(m)
            return FadeIn(m)

        def flab(j):
            return VGroup(T('j=%d' % j, 18, GREY_B), T('f=%d' % fval.get(j, 0), 19, YELLOW, mono=True)).arrange(DOWN, buff=0.08).move_to(P(4, j) + DOWN * 0.8)

        for e in EV:
            i = e['i']
            if logs:
                self.play(FadeOut(logs))
                logs = VGroup()
            head = T('插入 %s' % STRS[i - 1], 22, GREEN, mono=True).move_to([-6.85, -1.35, 0], aligned_edge=LEFT)
            fval[i] = 0
            colj[i] = flab(i)
            a1, sumt2 = set_sum(e['new'][2])
            self.play(FadeIn(head), FadeIn(colj[i]), add_log('新列 j=%d：+(0 xor %d)' % (i, i)), a1)
            sumt = sumt2
            slow = (i == 4)
            if i == 1:
                self.say('插入 a：先多出新的一列 j = 1，f 先当 0，和加上 0 xor 1。')
            for (d, j, old, new, a0, a1v) in e['chg']:
                mxc[d] += 1
                sq = Square(CS * 0.9, color=GREEN, fill_color=GREEN, fill_opacity=0.5, stroke_width=2).move_to(P(d, mxc[d]))
                cells.add(sq)
                fval[j] = new
                nl = flab(j)
                an, sumt2 = set_sum(a1v)
                self.play(FadeIn(sq, scale=0.5), ReplacementTransform(colj[j], nl),
                          add_log('f%d: %d→%d  -%d +%d' % (j, old, new, old ^ j, new ^ j)), an, run_time=0.9 if slow else 0.7)
                colj[j] = nl
                sumt = sumt2
                if slow:
                    self.say('第 %d 层多了一格，落在第 %d 列：只有 f%d 从 %d 变成 %d。和减去旧的 %d，加上新的 %d，变成 %d。' % (d, j, j, old, new, old ^ j, new ^ j, a1v))
                sq.set_color(BLUE).set_fill(BLUE, 0.35)
            if i == 1:
                self.say('a 经过第 1 层，第 1 层多一格，落在第 1 列，f1 从 0 变 1。和 = 0，对上样例。')
                self.step('⑤ 插一个串：经过的每层最多多 1 格')
            elif i == 2:
                self.say('ab 经过两层：第 1 层多一格落在第 2 列，第 2 层多一格落在第 1 列。只改了 f2 和 f1，和 = 6。')
                self.step('⑥ 多一格只改一列：和 −旧 +新')
            elif i == 3:
                self.say('abc：三层各多一格，改三列，和 = 4。')
            else:
                self.say('每一行输出都对上样例：0、6、4、12。每插一个串，改动的列数不超过它的长度。', extra=0.5)
            self.play(FadeOut(head))
        self.play(FadeOut(VGroup(cells, logs, *colj.values(), rowlab, sumt)))

        # ⑦ 代码和复杂度
        code = code_block([
            'ans += (0 ^ i);                // 新的一列',
            'for (int d = 0; d <= len; d++) {',
            '    // u 走到第 d 层',
            '    cnt[u]++;',
            '    if (cnt[u] > mx[d]) {       // 这层多一格',
            '        mx[d] = cnt[u];',
            '        int j = mx[d];          // 落在第 j 列',
            '        if (d > f[j]) {',
            '            ans -= (f[j] ^ j);  // 减旧',
            '            f[j] = d;',
            '            ans += (f[j] ^ j);  // 加新',
            '        }',
            '    }',
            '}',
        ], size=17, colors={8: YELLOW, 10: YELLOW}).move_to([-6.85, 0.75, 0], aligned_edge=LEFT)
        if code.width > 7.2:
            code.scale_to_fit_width(7.2)
        self.play(FadeIn(code))
        self.say('代码就是刚才的动画：沿着串往下走，这层的最大值变大了，就是多了一格，只去改那一列的 f，同时减旧加新。')
        self.say('为什么 mx[d] 最多加 1：插一个串，每一层只有它经过的那一个结点 +1。有分叉时这层最大值可能不变，那就一列都不改。')
        self.step('⑦ 总改动 ≤ Σ|s| → O(Σ|s|)，5 个大样例全过')
        self.say('所以总共改动的次数不超过所有串的长度之和，1.5×10⁶ 次。你差的只是“和存着、只改变了的”这一步。', extra=1.0)
