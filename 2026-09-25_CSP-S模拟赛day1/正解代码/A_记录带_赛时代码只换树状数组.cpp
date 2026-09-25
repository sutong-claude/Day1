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
int T, n;
int a[1000010], c[1000010];
inline void add (int x) {
    for (; x <= n; x += x & -x)
        c[x]++;
}
inline int ask (int x) {
    int res = 0;
    for (; x; x -= x & -x)
        res += c[x];
    return res;
}
inline void solve () {
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    int ans = 0;
    for (int i = 1; i <= n; i++)
        c[i] = 0;
    add (a[1]);
    for (int i = 2; i <= n; i++) {
        int num = (i - 1) - ask (a[i]);
        ans += num;
        add (a[i]);
    }
    int tot = ans;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++)
            c[j] = 0;
        add (a[i]);
        int x = 0, y = 0;
        for (int j = i + 1; j <= n; j++) {
            int num = (j - i) - ask (a[j]);
            x += num;
            y += j - i - num;
            add (a[j]);
            int now = ans - x + y;
            tot = max (now, tot);
        }
    }
    cout << tot << '\n';
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
