#include <bits/stdc++.h>
using namespace std;
#define int long long
int n;
int l[1000010], r[1000010];
vector <int> e[1000010];
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> l[i] >> r[i];
    for (int i = 1; i <= n - 1; i++) {
        int x, y;
        cin >> x >> y;
        e[x].push_baxk (y);
        e[y].push_back (x);
    }

    return 0;
}
