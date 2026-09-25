#include <bits/stdc++.h>
#include <chrono>
using namespace std;
#define int long long
const int Base1 = 131, P1 = 1e9 + 7;
const int Base2 = 911, P2 = 1e9 + 9;
mt19937_64 rng (chrono::steady_clock::now().time_since_epoch().count());
inline int Rand (int l, int r) {
    return rng () % (r - l + 1) + l;
}
int T;
int a[1000010];
inline void solve () {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    bool ok1 = true, ok2 = true;
    for (int i = 1; i <= n; i++) {
        if (a[i] != i)
            ok1 = false;
        if (a[i] != 1)
            ok2 = false;
    }
    if (ok1) {
        cout << "YES" << '\n';
        cout << 0 << '\n';
        cout << '\n';
    }
    else {
        int cnt = 6;
        //cout << "1 1 1 2 2 2 ";
        for (int i = 3; i <= n - 1; i++) {
            for (int j = 1; j <= i + 1; j++) {
                //cout << i << ' ';
                cnt++;
            }
        }
        //cout << '\n';
        cout << cnt << '\n';
        cout << "1 1 1 2 2 2 ";
        for (int i = 3; i <= n - 1; i++) {
            for (int j = 1; j <= i + 1; j++) {
                cout << i << ' ';
                //cnt++;
            }
        }
        cout << '\n';
    }
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    // code
    cin >> T;
    while (T--)
        solve ();
    return 0;
}
