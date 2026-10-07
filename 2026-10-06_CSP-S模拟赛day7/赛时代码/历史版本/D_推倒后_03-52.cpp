#include <bits/stdc++.h>
using namespace std;
#define int long long
int n;
vector <int> e[5010];
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
    for (int i = 1; i <= n; i++) {
        for (int j = i + 1; j <= n; j++) {
        }
    }
    cout << ans << ' ' << cnt << '\n';
    return 0;
}
