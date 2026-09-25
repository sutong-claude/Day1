#include <bits/stdc++.h>
using namespace std;
#define int long long
int T;
int a[1000010], cur[1000010];
vector <int> ops;
inline void solve () {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    for (int i = 1; i <= n; i++) {
        if (a[i] > i) {
            cout << "NO" << '\n';
            return;
        }
    }
    ops.clear();
    for (int i = 1; i <= n; i++) {
        int prev = i;
        for (int v = a[i]; v <= i - 1; v++) {
            int x = cur[v];
            ops.push_back(cur[x]);
            cur[v] = prev;
            prev = x;
        }
        cur[i] = prev;
    }
    cout << "YES" << '\n' << ops.size() << '\n';
    for (int x : ops)
        cout << x << ' ';
    cout << '\n';
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    cin >> T;
    while (T--)
        solve ();
    return 0;
}
