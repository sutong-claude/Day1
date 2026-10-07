#include <bits/stdc++.h>
using namespace std;

// Day7 D: N <= 100 的完整 19 分算法。
// 枚举无序叶子对 A,B；恢复 A-B 主路径；多源 BFS 求全树到主路径最大距离 H。
// 复杂度 O(L^2 * N)，L<=N，N<=100 足够。

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    freopen("Tighnari.in", "r", stdin);
    freopen("Tighnari.out", "w", stdout);

    int n;
    cin >> n;

    vector<vector<int>> g(n + 1);
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<int> leaves;
    for (int i = 1; i <= n; i++)
        if ((int)g[i].size() == 1)
            leaves.push_back(i);

    long long best = -1, ways = 0;
    vector<int> par(n + 1), dist(n + 1), onPath(n + 1);

    for (int ia = 0; ia < (int)leaves.size(); ia++) {
        int A = leaves[ia];
        fill(par.begin(), par.end(), -1);
        queue<int> q;
        q.push(A);
        par[A] = 0;
        while (!q.empty()) {
            int x = q.front(); q.pop();
            for (int y : g[x]) {
                if (par[y] != -1) continue;
                par[y] = x;
                q.push(y);
            }
        }

        for (int ib = ia + 1; ib < (int)leaves.size(); ib++) {
            int B = leaves[ib];
            fill(onPath.begin(), onPath.end(), 0);
            int pathLength = 0;
            for (int x = B; x != A; x = par[x]) {
                onPath[x] = 1;
                pathLength++;
            }
            onPath[A] = 1;

            fill(dist.begin(), dist.end(), -1);
            queue<int> mq;
            for (int i = 1; i <= n; i++) {
                if (onPath[i]) {
                    dist[i] = 0;
                    mq.push(i);
                }
            }

            int H = 0;
            while (!mq.empty()) {
                int x = mq.front(); mq.pop();
                H = max(H, dist[x]);
                for (int y : g[x]) {
                    if (dist[y] != -1) continue;
                    dist[y] = dist[x] + 1;
                    mq.push(y);
                }
            }

            long long value = 1LL * H * pathLength;
            if (value > best) { best = value; ways = 1; }
            else if (value == best) ways++;
        }
    }

    cout << best << ' ' << ways << '\n';
    return 0;
}
