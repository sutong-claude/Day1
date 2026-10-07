import random
from collections import deque

def prufer_tree(seq):
    n = len(seq) + 2
    deg = [1] * n
    for x in seq:
        deg[x] += 1
    edges = []
    for x in seq:
        y = min(i for i, d in enumerate(deg) if d == 1)
        edges.append((x, y))
        deg[x] -= 1
        deg[y] -= 1
    rem = [i for i, d in enumerate(deg) if d == 1]
    if len(rem) == 2:
        edges.append(tuple(rem))
    return edges

def fast(n, L, R, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    ans = 1
    for s in range(n):
        st = [(s, -1, 1, L[s])]
        while st:
            u, p, length, t = st.pop()
            ans = max(ans, length)
            for v in g[u]:
                if v == p:
                    continue
                nt = max(L[v], t + 1)
                if nt <= R[v]:
                    st.append((v, u, length + 1, nt))
    return ans

def path(g, s, t):
    par = [-1] * len(g)
    par[s] = s
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            break
        for v in g[u]:
            if par[v] == -1:
                par[v] = u
                q.append(v)
    p = []
    x = t
    while x != s:
        p.append(x)
        x = par[x]
    p.append(s)
    return p[::-1]

def feasible_bruteforce(p, L, R):
    def dfs(i, last):
        if i == len(p):
            return True
        v = p[i]
        lo = max(L[v], last + 1)
        for day in range(lo, R[v] + 1):
            if dfs(i + 1, day):
                return True
        return False
    return dfs(0, -10**9)

def brute(n, L, R, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    ans = 1
    for s in range(n):
        for t in range(n):
            p = path(g, s, t)
            if feasible_bruteforce(p, L, R):
                ans = max(ans, len(p))
    return ans

random.seed(0)

for tc in range(20000):
    n = random.randint(1, 8)
    if n == 1:
        edges = []
    else:
        seq = [random.randrange(n) for _ in range(n - 2)]
        edges = prufer_tree(seq)

    L, R = [], []
    for _ in range(n):
        a = random.randint(1, 6)
        b = random.randint(a, 6)
        L.append(a)
        R.append(b)

    a = fast(n, L, R, edges)
    b = brute(n, L, R, edges)
    assert a == b, (n, L, R, edges, a, b)

print("OK 20000")
