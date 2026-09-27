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
int n;
string s;
int a[1000010], b[1000010], c[1000010];
int f[1000010];
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    // code
    cin >> n;
    cin >> s;
    s = " " + s;
    for (int i = 1; i <= n; i++) {
        c[i] = (s[i] - '0') % 2;
        b[i] = (s[i] - '0') / 2 % 2;
        a[i] = (s[i] - '0') / 2 / 2 % 2;
    }
    for (int i = 1; i <= n; i++) {
        int tota = 0, totb = 0, totc = 0;
        for (int j = i; j >= 1; j--) {
            tota += a[j];
            totb += b[j];
            totc += c[j];
            if (tota >= totb && tota >= totc) {
                f[i] = max (f[j - 1] + (i - j + 1), f[i]);
            }
            else
                f[i] = max (f[i], f[j - 1]);
        }
    }
    cout << f[n] << '\n';
    return 0;
}
