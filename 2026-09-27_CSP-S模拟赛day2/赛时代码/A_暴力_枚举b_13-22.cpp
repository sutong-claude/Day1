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
string s;
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    // code
    cin >> s;
    int ans = 0;
    int n = s.size ();
    for (int i = 0; i < n; i++)
        ans = ans * 2 + (s[i] - '0');
    int tot = 1e18;
    for (int i = 0; i <= 1e4; i++) {
        int cnt = 0;
        int t = i;
        while (t != 0) {
            cnt += t % 2;
            t /= 2;
        }
        t = i + ans;
        while (t != 0) {
            cnt += t % 2;
            t /= 2;
        }
        tot = min (tot, cnt);
    }
    cout << 2 * tot - 1 << '\n';
    return 0;
}
