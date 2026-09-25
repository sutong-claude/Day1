#include <bits/stdc++.h>
using namespace std;
#define int long long
int n, q, k;
int m[1000010], w[1000010], dep[1000010], fa[1000010];
int g0[1000010], g1[1000010], cr[1000010], sum[1000010], lay[1000010];
vector <int> e[1000010];
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    cin >> n >> q;
    for (int i = 1; i <= n; i++)
        cin >> m[i];
    for (int i = 1; i <= n; i++)
        cin >> w[i];
    cin >> k;
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        e[u].push_back(v);
        e[v].push_back(u);
    }
    vector <int> ord;
    ord.push_back(k);
    fa[k] = 0;
    for (int h = 0; h < (int)ord.size(); h++) {
        int u = ord[h];
        for (int v : e[u]) {
            if (v == fa[u])
                continue;
            fa[v] = u;
            dep[v] = dep[u] + 1;
            ord.push_back(v);
        }
    }
    for (int h = n - 1; h >= 0; h--) {
        int u = ord[h];
        int s0 = 0, s1 = 0, pen = LLONG_MIN;
        for (int v : e[u]) {
            if (v == fa[u])
                continue;
            s0 += g0[v];
            s1 += g1[v];
            pen = max (pen, cr[v] - g0[v]);
        }
        cr[u] = s1;
        g0[u] = max (cr[u], m[u] + s0);
        if (pen != LLONG_MIN)
            g0[u] = max (g0[u], w[u] + s0 + pen);
        g1[u] = max (cr[u], max (m[u], w[u]) + s0);
    }
    int md = 0;
    for (int i = 1; i <= n; i++) {
        md = max (md, dep[i]);
        sum[dep[i]] += max (m[i], w[i]);
        lay[dep[i]] += g1[i];
    }
    for (int d = 1; d <= md; d++)
        sum[d] += sum[d - 1];
    while (q--) {
        int L;
        cin >> L;
        if (L >= md)
            cout << sum[md] << '\n';
        else
            cout << (L > 0 ? sum[L - 1] : 0) + lay[L] << '\n';
    }
    return 0;
}
