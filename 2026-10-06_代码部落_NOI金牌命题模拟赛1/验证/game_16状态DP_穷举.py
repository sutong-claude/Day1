from itertools import product, combinations

INF = 10**9

def brute(a, k):
    n = len(a)
    best = 0
    for cuts in combinations(range(1, n), k - 1):
        last = 0
        value = 0
        for r in cuts + (n,):
            z = 3
            for x in a[last:r]:
                z &= x
            value |= z
            last = r
        best = max(best, value)
    return best

def solve(a, k):
    dp = [INF] * 16
    dp[a[0]] = 1

    for x in a[1:]:
        ndp = [INF] * 16
        for st, seg in enumerate(dp):
            if seg >= INF:
                continue
            old_or = st >> 2
            last_and = st & 3

            e = (old_or << 2) | (last_and & x)
            ndp[e] = min(ndp[e], seg)

            s = ((old_or | last_and) << 2) | x
            ndp[s] = min(ndp[s], seg + 1)
        dp = ndp

    need = [INF] * 4
    for st, seg in enumerate(dp):
        if seg < INF:
            value = (st >> 2) | (st & 3)
            need[value] = min(need[value], seg)

    for value in (3, 2, 1, 0):
        if need[value] <= k:
            return value

cnt = 0
for n in range(1, 9):
    for a in product(range(4), repeat=n):
        for k in range(1, n + 1):
            cnt += 1
            x = solve(a, k)
            y = brute(a, k)
            assert x == y, (a, k, x, y)

print("OK", cnt)
