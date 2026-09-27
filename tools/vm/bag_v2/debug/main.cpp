#include <bits/stdc++.h>
using namespace std;
#define int long long
const int Base1 = 131, P1 = 1e9 + 7;
const int Base2 = 911, P2 = 1e9 + 9;
random_device rd;
mt19937_64 rnd (rd());
int Rand (int l, int r) {
    return rnd () % (r - l + 1) + l;
}
int s[1000010];
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    int n;
    cin >> n;
    s[0] = 0;
    for (int i = 1; i <= n; i++) {
        int t;
        cin >> t;
        s[i] = s[i - 1] + t;
    }
    int q;
    cin >> q;
    while (q--) { // break point
        int l, r;
        cin >> l >> r;
        cout << s[r] - s[l] << '\n'; // bug point!
    }
    return 0;
}
