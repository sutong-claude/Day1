#include <bits/stdc++.h>
using namespace std;
#define int long long
string s;
int f[2], g[2];
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("multiply.in", "r", stdin);
    //freopen ("multiply.out", "w", stdout);
    cin >> s;
    int n = s.size ();
    // f[c]：低位已经处理完，向当前位进位 c 时，最少用了几项
    f[0] = 0, f[1] = 1e18;
    for (int i = n - 1; i >= 0; i--) {
        g[0] = g[1] = 1e18;
        for (int c = 0; c <= 1; c++) {
            int v = s[i] - '0' + c;
            if (v == 0)
                g[0] = min (g[0], f[c]);
            else if (v == 1) {
                g[0] = min (g[0], f[c] + 1);
                g[1] = min (g[1], f[c] + 1);
            }
            else
                g[1] = min (g[1], f[c]);
        }
        f[0] = g[0], f[1] = g[1];
    }
    int k = min (f[0], f[1] + 1);
    cout << 2 * k - 1 << '\n';
    return 0;
}
