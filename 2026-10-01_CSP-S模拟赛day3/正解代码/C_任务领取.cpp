#include <bits/stdc++.h>
using namespace std;
static const int MOD = 998244353;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    vector<int> p(n + 1), who(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> p[i];
        who[p[i]] = i;
    }
    vector<vector<int>> g(n + 1);
    for (int i = 1, u, v; i < n; ++i) {
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    if (n == 1) {
        cout << 1 << '\n';
        return 0;
    }

    vector<int> up(n + 1, 1);
    for (int val = n; val >= 1; --val) {
        int v = who[val];
        long long s = 1;
        for (int w : g[v]) if (p[w] > p[v]) s += up[w];
        up[v] = (int)s;
    }

    vector<int> parent(n + 1, 0), order;
    order.reserve(n);
    order.push_back(1);
    for (size_t z = 0; z < order.size(); ++z) {
        int v = order[z];
        for (int w : g[v]) if (w != parent[v]) {
            parent[w] = v;
            order.push_back(w);
        }
    }

    auto hook = [&](int child, int par) -> int {
        if (p[par] < p[child]) return up[child];
        return up[child] - up[par];
    };

    vector<int> inv(n + 1, 1);
    for (int i = 2; i <= n; ++i)
        inv[i] = MOD - (long long)(MOD / i) * inv[MOD % i] % MOD;

    long long fact = 1;
    for (int i = 1; i <= n - 1; ++i) fact = fact * i % MOD;

    vector<int> ways(n + 1);
    long long w1 = fact;
    for (int v : order) if (v != 1) w1 = w1 * inv[hook(v, parent[v])] % MOD;
    ways[1] = (int)w1;

    for (size_t z = 1; z < order.size(); ++z) {
        int v = order[z], u = parent[v];
        int old_h = hook(v, u);
        int new_h = hook(u, v);
        ways[v] = (long long)ways[u] * old_h % MOD * inv[new_h] % MOD;
    }

    long long ans = 0;
    for (int r = 1; r <= n; ++r) {
        bool local_max = true;
        for (int w : g[r]) if (p[w] > p[r]) {
            local_max = false;
            break;
        }
        if (local_max) {
            ans += ways[r];
            if (ans >= MOD) ans -= MOD;
        }
    }
    cout << ans << '\n';
    return 0;
}
