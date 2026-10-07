#include <bits/stdc++.h>
using namespace std;
#define int long long
int n;
vector <int> e[5010];
int fa[5010];
int d[5010];
inline void calc (int root, int f) {
    fa[root] = f;
    for (auto y : e[root])
        if (y != f)
            calc (y, root);
}
inline int dfs (int root, int f) {
    int ma = 0;
    for (auto y : e[root]) {
        if (y == f)
            continue;
        d[y] = d[root] + 1;
        ma = max (d[y], ma);
        ma = max (dfs (y, root), ma);
    }
    return ma;
}
int ans = 0, cnt = 0;
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    cin >> n;
    for (int i = 1; i <= n - 1; i++) {
        int x, y;
        cin >> x >> y;
        e[x].push_back (y);
        e[y].push_back (x);
    }
    calc (1, 0);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++)
            d[j] = 0;
        d[fa[i]] = 1;
        dfs (fa[i], i);
        int ma = 1;
        for (int j = 1; j <= n; j++)
            ma = max (ma, d[j]);
        int ma1 = 0, ma2 = 0;
        for (auto y : e[i]) {
            if (y == fa[i])
                continue;
            int c = dfs (y, i) + 1;
            if (c >= ma1) {
                ma2 = ma1;
                ma1 = c;
            }
            else if (c > ma2)
                ma2 = c;
        }
        int tot = ma1 + ma2;
        tot = max (tot, 1LL);
        int res = ma * tot;
        if (res > ans) {
            ans = res;
            cnt = 1;
        }
        else if (res == ans)
            cnt++;
    }
    cout << ans << ' ' << cnt << '\n';
    return 0;
}
