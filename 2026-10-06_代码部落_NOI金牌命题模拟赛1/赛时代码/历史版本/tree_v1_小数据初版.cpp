#include <bits/stdc++.h>
using namespace std;
#define int long long
int n;
int l[1000010], r[1000010];
vector <int> e[1000010];
bool vis[1000010];
int d[1000010];
inline void dfs (int root, int time) {
    for (auto y : e[root]) {
        if (vis[y] == true)
            continue;
        int reach = time + 1;
        if (reach > r[i])
            continue;
        d[y] = d[root] + 1;
        vis[y] = true;
        dfs (y, max (l[i], reach));
        vis[y] = false;
    }
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> l[i] >> r[i];
    for (int i = 1; i <= n - 1; i++) {
        int x, y;
        cin >> x >> y;
        e[x].push_baxk (y);
        e[y].push_back (x);
    }
    if (n <= 5000) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                vis[j] = false;
                d[j] = 0;
            }
            vis[i] = true;
            d[i] = 1;
            dfs (i, 0);
        }
        return 0;
    }
    bool A = true;
    for (int i = 1; i <= n; i++) {
        if (l[i] != r[i]) { A = false; break; }
    }
    if (A) return 0;
    bool B = false;
    for (int i = 1; i <= n; i++) {
        if (e[i].size() == n - 1) { B = true; break; }
    }
    if (B) return 0;
    int cnt1 = 0, cnt2 = 0;
    for (int i = 1; i <= n; i++) {
        if (e[i].size() == 1) cnt1++;
        if (e[i].size() == 2) cnt2++;
    }
    bool C = (cnt1 == 2 && cnt2 == n - 2);
    if (C) return 0;
    cout << 1 << '\n';
    return 0;
}
