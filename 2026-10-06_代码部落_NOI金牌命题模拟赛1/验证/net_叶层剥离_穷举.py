from itertools import product, combinations
from collections import deque
import heapq

def prufer_tree(seq):
    n = len(seq) + 2
    deg = [1] * n
    for x in seq:
        deg[x] += 1
    pq = [i for i, d in enumerate(deg) if d == 1]
    heapq.heapify(pq)
    edges = []
    for x in seq:
        y = heapq.heappop(pq)
        edges.append((x, y))
        deg[x] -= 1
        deg[y] -= 1
        if deg[x] == 1:
            heapq.heappush(pq, x)
    a = heapq.heappop(pq)
    b = heapq.heappop(pq)
    edges.append((a, b))
    return edges

def brute(n, m, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    best = 10**9
    for comb in combinations(range(n), m):
        S = set(comb)

        q = [comb[0]]
        seen = {comb[0]}
        for x in q:
            for y in g[x]:
                if y in S and y not in seen:
                    seen.add(y)
                    q.append(y)
        if len(seen) != m:
            continue

        dist = [-1] * n
        dq = deque()
        for x in S:
            dist[x] = 0
            dq.append(x)
        while dq:
            x = dq.popleft()
            for y in g[x]:
                if dist[y] == -1:
                    dist[y] = dist[x] + 1
                    dq.append(y)
        best = min(best, max(dist))
    return best

def peel(n, m, edges):
    if m >= n:
        return 0
    g = [[] for _ in range(n)]
    deg = [0] * n
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
        deg[u] += 1
        deg[v] += 1

    dq = deque(i for i, d in enumerate(deg) if d <= 1)
    alive = [True] * n
    remaining = n
    rounds = 0

    while remaining > m:
        cnt = len(dq)
        rounds += 1
        remaining -= cnt
        for _ in range(cnt):
            x = dq.popleft()
            alive[x] = False
            for y in g[x]:
                if alive[y]:
                    deg[y] -= 1
                    if deg[y] == 1:
                        dq.append(y)
    return rounds

cnt = 0
for n in range(2, 8):
    for seq in product(range(n), repeat=n - 2):
        edges = prufer_tree(seq)
        for m in range(1, n + 1):
            cnt += 1
            a = peel(n, m, edges)
            b = brute(n, m, edges)
            assert a == b, (n, seq, m, a, b, edges)

print("OK", cnt)
