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
    //freopen ("multiply.in", "r", stdin);
    //freopen ("multiply.out", "w", stdout);
    // code
    cin >> s;
    int n = s.size ();
    s = " " + s;
    int ans = 0;
    for (int i = 1; i <= n; i++)
        ans += (s[i] - '0');
    cout << ans << '\n';
    return 0;
}
