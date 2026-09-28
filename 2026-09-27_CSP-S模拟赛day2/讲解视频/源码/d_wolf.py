from vcommon import *

COLX = [-6.55, -5.45, -3.75, -2.05, -0.85]


def their_array(i):
    t, w = i, []
    while t != 0:
        w.append(t % 2)
        t //= 2
    return w


def row(cells, y, colors=None, size=20):
    g = VGroup()
    for k, (x, c) in enumerate(zip(COLX, cells)):
        g.add(T(c, size, (colors or {}).get(k, WHITE), mono=(k in (1, 2))).move_to([x, y, 0]))
    return g


class DWolf(Base):
    def construct(self):
        self.head('D 狼人：枚举了所有 i，为什么还错')
        code = code_block([
            'for (int i = 0; i < (1LL << n); i++) {',
            '    int t = i; wolves.clear();',
            '    while (t != 0) {',
            '        wolves.push_back(t % 2); t /= 2;',
            '    }',
            '    if (isValid (wolves, direction, b)) ...',
        ]).move_to([-6.85, 1.95, 0], aligned_edge=LEFT)
        self.play(FadeIn(code))
        self.say('你的暴力：i 从 0 到 2ⁿ−1，把 i 变成“谁是狼”的数组，再用 checker 里的 isValid 检查。')
        self.step('① i 取遍 0 … 2ⁿ−1：枚举本身没错 ✓')
        hl = SurroundingRectangle(VGroup(code[2], code[3], code[4]), color=RED, buff=0.06)
        self.play(Create(hl))
        self.say('问题在这个 while：它只取到 i 最高位的那个 1 为止，前面的 0 不会放进数组。')
        self.step('② i → 数组 这一步：前导 0 被丢掉了')

        # n = 3 的表
        y0 = 0.72
        head = row(['i', '二进制', '你得到的数组', '长度', '检查了？'], y0, {k: GREY_B for k in range(5)}, 19)
        mini = T('while (t != 0) { wolves.push_back(t % 2); t /= 2; }', 19, RED, mono=True).move_to([-6.85, 1.3, 0], aligned_edge=LEFT)
        self.play(FadeOut(hl), ReplacementTransform(code, mini), FadeIn(head))
        rows = VGroup()
        checked = []
        for i in range(8):
            w = their_array(i)
            ok = len(w) == 3
            checked.append(ok)
            r = row([str(i), format(i, '03b'), '{' + ','.join(map(str, w)) + '}', str(len(w)), '✓ 检查' if ok else '✗ 扔掉'],
                    y0 - 0.4 * (i + 1), {3: GREEN if ok else RED, 4: GREEN if ok else RED}, 20)
            rows.add(r)
        self.say('n = 3，8 个 i 逐个看。注意数组是从最低位开始放的：i = 2（二进制 010）变成 {0,1}，只有两位。')
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.35), run_time=3.2)
        self.step('③ n = 3：只有 i = 4…7 的长度是 3')
        self.say('isValid 第一句就是“长度不等于 n 就返回 false”。i = 0 到 3 这 4 种分布，还没开始检查就被扔掉了。')
        bad = VGroup(*[rows[i] for i in range(8) if not checked[i]])
        self.play(Indicate(bad, color=RED, scale_factor=1.03), run_time=1.5)
        good_last = VGroup(*[rows[i][1] for i in range(8) if checked[i]])
        self.say('被检查的 4 个，二进制最高位都是 1，也就是第 3 个人都是狼。你只试了“最后一个人是狼”的那一半。')
        self.play(*[Indicate(rows[i][1], color=YELLOW) for i in range(8) if checked[i]], run_time=1.5)
        self.step('④ 只试了“最后一个人是狼”的那一半')

        # 反例
        self.play(FadeOut(VGroup(head, rows, mini)))
        p1 = box('L 1', 1.5, 0.9, color=RED, fill=RED, size=28)
        p2 = box('L 1', 1.5, 0.9, color=GREEN, fill=GREEN, size=28)
        ppl = VGroup(p1, p2).arrange(RIGHT, buff=0.6).move_to([-3.6, 2.2, 0])
        lab = VGroup(T('第 1 人：狼', 20, RED).next_to(p1, DOWN, buff=0.15), T('第 2 人：村民', 20, GREEN).next_to(p2, DOWN, buff=0.15))
        self.play(FadeIn(ppl), FadeIn(lab))
        self.say('最小反例：两个人都往左看，都说“左边有 1 个狼”。第 1 人左边没人，他在说谎，只能是狼；第 2 人说的是真话。答案 10。')
        self.step('⑤ 反例 n=2，LL，b = 1 1，答案 10')
        l1 = T('答案 10：第 1 人是狼 → i 的第 0 位是 1 → i = 1', 21).move_to([-3.4, 0.6, 0])
        l2 = T('你的循环：i = 1 → 数组 {1}，长度 1 ≠ 2', 21, RED).next_to(l1, DOWN, buff=0.3)
        l3 = T('→ 还没检查就扔掉 → 4 个 i 全不过 → 输出 −1', 21, RED).next_to(l2, DOWN, buff=0.3)
        for m in (l1, l2, l3):
            if m.width > 7.1:
                m.scale_to_fit_width(7.1)
        self.play(FadeIn(l1))
        self.say('答案 10 对应的正是 i = 1。')
        self.play(FadeIn(l2))
        self.play(FadeIn(l3))
        self.say('可你的循环把 i = 1 变成了只有 1 位的 {1}，长度不对，被扔掉。于是输出 −1。')
        self.step('⑥ 答案对应 i = 1，被长度检查扔掉 → −1')
        self.play(FadeOut(VGroup(ppl, lab, l1, l2, l3)))
        s1 = T('题面样例的答案：001　−1　10101', 22).move_to([-3.4, 2.0, 0])
        s2 = T('最后一位都是 1（或者无解）', 22, YELLOW).next_to(s1, DOWN, buff=0.3)
        s3 = T('大样例 sample2（1000 组）：错 277 组', 22, RED).next_to(s2, DOWN, buff=0.5)
        self.play(FadeIn(s1), FadeIn(s2))
        self.say('为什么样例过了？题面样例的答案恰好最后一个都是狼，正好落在你检查的那一半里。')
        self.play(FadeIn(s3))
        self.say('大样例 sample2 就是子任务 1 的 1000 组数据，一跑就错 277 组。')
        self.step('⑦ 样例恰好测不出，大样例错 277 / 1000')
        self.play(FadeOut(VGroup(s1, s2, s3)))
        fix = code_block([
            'for (int i = 0; i < (1LL << n); i++) {',
            '    wolves.clear();',
            '    for (int k = 0; k < n; k++)',
            '        wolves.push_back(i >> k & 1);',
            '    if (isValid (wolves, direction, b)) ...',
        ], colors={2: GREEN, 3: GREEN}).move_to([-6.85, 2.05, 0], aligned_edge=LEFT)
        self.play(FadeIn(fix))
        rows2 = VGroup()
        head2 = row(['i', '二进制', '改后的数组', '长度', '检查了？'], 0.8, {k: GREY_B for k in range(5)}, 19)
        for i in range(8):
            w = [i >> k & 1 for k in range(3)]
            rows2.add(row([str(i), format(i, '03b'), '{' + ','.join(map(str, w)) + '}', '3', '✓ 检查'], 0.8 - 0.37 * (i + 1), {3: GREEN, 4: GREEN}, 20))
        self.play(FadeIn(head2), LaggedStart(*[FadeIn(r) for r in rows2], lag_ratio=0.2), run_time=2.2)
        self.say('改成每次都取满 n 位：k 从 0 到 n−1，取 i >> k & 1。8 个 i 全都变成长度 3 的数组，全部被检查。')
        self.step('⑧ 改：k 从 0 到 n−1 取 i >> k & 1')
        self.say('所以“枚举了所有 i”不等于“检查了所有情况”：中间“把 i 翻译成数组”这一步丢了东西。')
        self.step('⑨ 自检：数 isValid 真正检查了几次，应是 2ⁿ')
        self.say('以后写这种暴力，加一行计数：数一数 isValid 真正走完检查的次数，应该正好是 2ⁿ。', extra=1.0)
