#include <bits/stdc++.h>
using namespace std;
#define int long long
int t;
int n;
int p[1000010];
int a[1000010];
vector <int> e[1000010];
bool vis[1000010];
int f[1000010];
inline int dfs (int boss) {
    int mi = p[root];
    vis[root] = true;
    int mi = n + 1;
    for (auto y : e[root]) {
        if (vis[y] == true)
            continue;
        unordered_set <int> mp;
        mi = min (dfs (root), mi);
    }
    int root = p[mi];
    f[root] = boss;
}
inline void solve () {
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> p[i];
    for (int i = 1; i <= n; i++)
        e[i].clear();
    for (int i = 1; i <= n - 1; i++) {
        int x, y;
        cin >> x >> y;
        e[x].push_back (y);
        e[y].push_back (x);
    }
    for (int i = 1; i <= n; i++)
        vis[i] = false;
    for (int i = 1; i <= n; i++)
        a[p[i]] = i;
    dfs (0);
    for (int i = 1; i <= n; i++)
        cout << f[i] << ' ';
    cout << '\n';
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    cin >> t;
    while (t--)
        solve ();
    return 0;
}
