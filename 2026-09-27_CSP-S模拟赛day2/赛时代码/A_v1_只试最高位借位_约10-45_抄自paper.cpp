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
int a[1000010];
int b[1000010];
int c[1000010];
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
    for (int i = 1; i <= n; i++)
        a[i] = s[n - i + 1] - '0';
//    for (int i = 1; i <= n; i++)
//        cout << a[i] << ' ';
//    cout << '\n';
    int res1 = 0;
    for (int i = n; i >= 1; i--)
        res1 += a[i];
    b[0] = 1;
    for (int i = n; i >= 1; i--) {
        if (b[i] < 0) {
            b[i - 1]--;
            b[i] += 2;
        }
        c[i] = b[i] - a[i];
        if (c[i] < 0) {
            b[i - 1]--;
            c[i] += 2;
        }
    }
    int len = 0;
    while (c[len] != 0)
        len++;
    int res2 = 0;
    for (int i = len; i <= n; i++)
        res2 += c[i];
    int ans = min (2 * res1 - 1, 2 * res2 - 1 + 2);
    cout << ans << '\n';
    return 0;
}
