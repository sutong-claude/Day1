from manim import *
import numpy as np

FONT = "WenQuanYi Zen Hei"
MONO = "WenQuanYi Zen Hei Mono"
PANEL_X = 0.72
SUB_W = 13.6


def wrap(t, n=34):
    if len(t) <= n:
        return [t]
    k = -(-len(t) // n)
    target = len(t) / k
    out, start = [], 0
    for _ in range(k - 1):
        ideal = int(start + target)
        best = None
        for d in range(0, 8):
            for p in (ideal + d, ideal - d):
                if start < p < len(t) and t[p - 1] in '，。；：、）」”' and t[p] not in '，。；：、）」”':
                    best = p
                    break
            if best:
                break
        if best is None:
            best = ideal
            while start < best < len(t) - 1 and (t[best - 1].isascii() and t[best - 1].isalnum()) and (t[best].isascii() and t[best].isalnum()):
                best += 1
        out.append(t[start:best])
        start = best
    out.append(t[start:])
    return out


def T(t, size=24, color=WHITE, mono=False, **kw):
    return Text(t, font=MONO if mono else FONT, font_size=size, color=color, **kw)


class Base(Scene):
    def setup(self):
        self.sub = None
        self.items = []
        self.add(Line([0.45, 3.75, 0], [0.45, -2.75, 0], color=GREY_D, stroke_width=1.5))
        self.add(T('步骤', 18, GREY_B).move_to([PANEL_X, 3.62, 0], aligned_edge=LEFT))

    def head(self, t):
        h = T(t, 30, YELLOW).move_to([-6.85, 3.55, 0], aligned_edge=LEFT)
        if h.width > 7.1:
            h.scale_to_fit_width(7.1)
        self.play(Write(h), run_time=1.0)
        return h

    def say(self, t, extra=0.0):
        lines = wrap(t, 34)
        new = VGroup(*[T(l, 25) for l in lines]).arrange(DOWN, buff=0.12)
        if new.width > SUB_W:
            new.scale_to_fit_width(SUB_W)
        new.to_edge(DOWN, buff=0.22)
        anims = [FadeIn(new, run_time=0.45)]
        if self.sub is not None:
            anims.insert(0, FadeOut(self.sub, run_time=0.25))
        self.play(*anims)
        self.sub = new
        self.wait(max(1.6, len(t) * 0.14) + extra)

    def step(self, t):
        m = T(t, 21, YELLOW)
        if m.width > 6.25:
            m.scale_to_fit_width(6.25)
        if not self.items:
            m.move_to([PANEL_X, 3.15, 0], aligned_edge=LEFT)
        else:
            m.next_to(self.items[-1], DOWN, buff=0.27, aligned_edge=LEFT)
        anims = [FadeIn(m, shift=0.2 * RIGHT)] + [x.animate.set_color(GREY_B) for x in self.items]
        self.play(*anims, run_time=0.6)
        self.items.append(m)
        return m


def box(txt, w=0.6, h=0.6, color=WHITE, fill=None, size=26, mono=True, tcolor=None):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.08, color=color, stroke_width=2)
    if fill is not None:
        r.set_fill(fill, opacity=0.35)
    t = T(txt, size, tcolor or WHITE, mono=mono)
    t.move_to(r.get_center())
    return VGroup(r, t)


def code_block(lines, size=21, color=WHITE, colors=None):
    """代码块：按前导空格数手动缩进（Text 会吃掉行首空格）。colors: {行号: 颜色}"""
    cw = T('M' * 20, size, mono=True).width / 20
    g = VGroup()
    for k, ln in enumerate(lines):
        ind = len(ln) - len(ln.lstrip(' '))
        m = T(ln.strip() or '.', size, (colors or {}).get(k, color), mono=True)
        if not ln.strip():
            m.set_opacity(0)
        g.add(m)
    g.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    for k, ln in enumerate(lines):
        ind = len(ln) - len(ln.lstrip(' '))
        g[k].shift(RIGHT * ind * cw)
    return g
