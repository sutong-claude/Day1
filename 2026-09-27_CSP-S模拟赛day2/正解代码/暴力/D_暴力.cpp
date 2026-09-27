#include <bits/stdc++.h>
using namespace std;
#define int long long
// 子任务 1：枚举 2^n 种分布，照 checker 的规则检查。注意要取满 n 位（i >> k & 1），不能按 i 的二进制位数取
int T, n, b[30], w[30], pre[30];
string d;
inline bool check () {
    for (int i = 2; i <= n; i++)
        if (w[i - 1] && w[i]) return false;
    for (int i = 1; i <= n; i++)
        pre[i] = pre[i - 1] + w[i];
    for (int i = 1; i <= n; i++) {
        if (w[i]) continue;
        int t = (d[i - 1] == 'L') ? pre[i - 1] : pre[n] - pre[i];
        if (t != b[i]) return false;
    }
    return true;
}
inline void solve () {
    cin >> n >> d;
    for (int i = 1; i <= n; i++)
        cin >> b[i];
    for (int mask = 0; mask < (1LL << n); mask++) {
        for (int k = 0; k < n; k++)
            w[k + 1] = mask >> k & 1;
        if (check ()) {
            for (int i = 1; i <= n; i++)
                cout << w[i];
            cout << '\n';
            return;
        }
    }
    cout << -1 << '\n';
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
