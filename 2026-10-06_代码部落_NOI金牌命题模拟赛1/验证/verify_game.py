#!/usr/bin/env python3
"""
复现本场 game.cpp 的小数据穷举验证。

默认：
1. 编译 ../赛时代码/game.cpp；
2. 枚举 n=1..7、所有 a_i in {0,1,2,3}、所有 k；
3. 暴力枚举恰好 k 段的全部切法求真值；
4. 将全部 case 一次喂给赛时代码；
5. 比较每一行。

预期总 case 数：145636。
"""

from itertools import product, combinations
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "赛时代码" / "game.cpp"


def brute(a, k):
    n = len(a)
    best = -1

    if k == 1:
        cuts_list = [()]
    else:
        cuts_list = combinations(range(1, n), k - 1)

    for cuts in cuts_list:
        pos = (0,) + tuple(cuts) + (n,)
        value = 0
        for i in range(k):
            seg = a[pos[i]]
            for j in range(pos[i] + 1, pos[i + 1]):
                seg &= a[j]
            value |= seg
        best = max(best, value)
    return best


def main():
    cases = []
    truth = []

    for n in range(1, 8):
        for a in product(range(4), repeat=n):
            for k in range(1, n + 1):
                cases.append((n, k, a))
                truth.append(brute(a, k))

    assert len(cases) == 145636

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        exe = td / "game"
        subprocess.run(
            ["g++", "-std=c++17", "-O2", str(SRC), "-o", str(exe)],
            check=True,
        )

        inp = td / "game.in"
        out = td / "game.out"

        with inp.open("w", encoding="utf-8") as f:
            f.write(str(len(cases)) + "\n")
            for n, k, a in cases:
                f.write(f"{n} {k}\n")
                f.write(" ".join(map(str, a)) + "\n")

        subprocess.run([str(exe)], cwd=td, check=True)

        got = [int(x) for x in out.read_text(encoding="utf-8").split()]
        assert len(got) == len(truth)

        for i, (x, y) in enumerate(zip(got, truth)):
            if x != y:
                n, k, a = cases[i]
                raise SystemExit(
                    f"mismatch #{i}: n={n}, k={k}, a={a}, user={x}, brute={y}"
                )

    print(f"PASS: {len(cases)} cases, 0 mismatch")


if __name__ == "__main__":
    main()
