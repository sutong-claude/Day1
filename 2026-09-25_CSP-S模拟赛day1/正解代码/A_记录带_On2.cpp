#include <bits/stdc++.h>
using namespace std;
#define int long long
int T;
int a[1000010], f[1000010];
inline void solve () {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    int tot = 0, ma = 0;
    for (int r = 1; r <= n; r++) {
        int cnt = 0;
        for (int l = r - 1; l >= 1; l--) {
            if (a[l] > a[r])
                cnt++;
            f[l] += cnt;
            int len = r - l + 1;
            ma = max (ma, len * (len - 1) / 2 - 2 * f[l]);
        }
        tot += cnt;
    }
    for (int i = 1; i <= n; i++)
        f[i] = 0;
    cout << tot + ma << '\n';
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
