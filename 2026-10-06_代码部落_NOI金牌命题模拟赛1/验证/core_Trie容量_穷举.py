from itertools import product, combinations, combinations_with_replacement

def lcp(a, b):
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return i

def brute(strings, k):
    best = None
    for ids in combinations(range(len(strings)), k):
        S = [strings[i] for i in ids]
        L = 0
        for i in range(k):
            for j in range(i + 1, k):
                L = max(L, lcp(S[i], S[j]))

        if L == 0:
            t = ""
        else:
            cand = set()
            for i in range(k):
                for j in range(i + 1, k):
                    if lcp(S[i], S[j]) >= L:
                        cand.add(S[i][:L])
            t = min(cand)

        if best is None or t < best:
            best = t
    return best

class Node:
    def __init__(self, parent=-1, depth=0, c=""):
        self.ch = {}
        self.parent = parent
        self.depth = depth
        self.c = c
        self.endcnt = 0
        self.childcnt = 0

def solve(strings, k):
    tr = [Node()]
    nodes_at = [1]
    terminal_at = [0]
    max_d = 0

    for s in strings:
        u = 0
        for c in s:
            if c not in tr[u].ch:
                v = len(tr)
                tr[u].ch[c] = v
                tr[u].childcnt += 1
                tr.append(Node(u, tr[u].depth + 1, c))
                d = tr[v].depth
                while len(nodes_at) <= d:
                    nodes_at.append(0)
                    terminal_at.append(0)
                nodes_at[d] += 1
                max_d = max(max_d, d)
            u = tr[u].ch[c]

        tr[u].endcnt += 1
        terminal_at[tr[u].depth] += 1

    nodes_at += [0] * (max_d + 2 - len(nodes_at))
    terminal_at += [0] * (max_d + 2 - len(terminal_at))

    cap = [0] * (max_d + 1)
    short = 0
    for d in range(max_d + 1):
        short += terminal_at[d]
        cap[d] = short + nodes_at[d + 1]

    loss = [0] * (max_d + 1)
    st = [0]

    while st:
        u = st.pop()
        d = tr[u].depth
        local = tr[u].endcnt + tr[u].childcnt
        allowed = cap[d] - loss[d]

        if local >= 2 and allowed >= k:
            if u == 0:
                return ""
            ans = []
            while u:
                ans.append(tr[u].c)
                u = tr[u].parent
            return "".join(reversed(ans))

        loss[d] += max(0, local - 1)

        for c in sorted(tr[u].ch, reverse=True):
            st.append(tr[u].ch[c])

def universe(alpha, max_len):
    return ["".join(p) for L in range(1, max_len + 1)
            for p in product(alpha, repeat=L)]

cnt = 0

for U in (universe("ab", 3), universe("abc", 2)):
    for n in range(2, 7):
        for strings in combinations_with_replacement(U, n):
            for k in range(2, n + 1):
                cnt += 1
                a = solve(strings, k)
                b = brute(strings, k)
                assert a == b, (strings, k, a, b)

print("OK", cnt)
