#include <bits/stdc++.h>
using namespace std;
#define int long long
int n, tot;
int ch[1000010][26], cnt[1000010];
int mx[1000010], f[1000010];
string s;
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("string.in", "r", stdin);
    //freopen ("string.out", "w", stdout);
    cin >> n;
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        cin >> s;
        // 新加入 j = i 这一项，f[i] 先是 0
        ans += (0 ^ i);
        // mx[d]：深度 d 的所有结点里，最多有几个串经过
        // f[j]：最大的 d 使得 mx[d] >= j
        int u = 0, len = s.size ();
        for (int d = 0; d <= len; d++) {
            if (d > 0) {
                int c = s[d - 1] - 'a';
                if (!ch[u][c])
                    ch[u][c] = ++tot;
                u = ch[u][c];
            }
            cnt[u]++;
            if (cnt[u] > mx[d]) {
                mx[d] = cnt[u];
                int j = mx[d];
                if (d > f[j]) {
                    ans -= (f[j] ^ j);
                    f[j] = d;
                    ans += (f[j] ^ j);
                }
            }
        }
        cout << ans << '\n';
    }
    return 0;
}
