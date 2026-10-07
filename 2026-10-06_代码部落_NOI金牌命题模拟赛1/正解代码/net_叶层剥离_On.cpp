#include <bits/stdc++.h>
using namespace std;

// 赛后独立推导：叶层剥离 O(n)
// 答案 = 最小 R，使同步删除 R 轮当前叶子后，剩余点数 <= M。

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    freopen("net.in", "r", stdin);
    freopen("net.out", "w", stdout);

    int n, m;
    cin >> n >> m;

    vector<vector<int>> g(n + 1);
    vector<int> deg(n + 1);

    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
        deg[u]++;
        deg[v]++;
    }

    if (m >= n) {
        cout << 0 << '\n';
        return 0;
    }

    queue<int> q;
    vector<char> alive(n + 1, true);

    for (int i = 1; i <= n; i++)
        if (deg[i] <= 1)
            q.push(i);

    int remaining = n;
    int rounds = 0;

    while (remaining > m) {
        int cnt = (int)q.size();
        rounds++;
        remaining -= cnt;

        while (cnt--) {
            int x = q.front();
            q.pop();
            alive[x] = false;

            for (int y : g[x]) {
                if (!alive[y])
                    continue;

                deg[y]--;
                if (deg[y] == 1)
                    q.push(y);
            }
        }
    }

    cout << rounds << '\n';
    return 0;
}
