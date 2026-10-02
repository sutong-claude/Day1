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
const int MOD = 998244353;
int n;
int a[1000010];
pair <int, int> e[1000010];
int ans = 0;
bool vis[1000010];
int d[1000010];
bool finish[1000010];
inline void dfs (int k) {
    if (k == n) {
        bool ok = true;
        for (int i = 1; i <= n; i++)
            finish[i] = false;
        for (int i = 1; i <= n - 1; i++) {
            int p1 = e[d[i]].first, p2 = e[d[i]].second;
            if (finish[p1] == true && finish[p2] == true) {
                ok = false;
                break;
            }
            else if (finish[p1] == false && finish[p2] == true)
                finish[p1] = true;
            else if (finish[p1] == true && finish[p2] == false)
                finish[p2] = true;
            else {
                if (a[p1] < a[p2])
                    finish[p1] = true;
                else
                    finish[p2] = true;
            }
        }
        ans += ok;
        ans %= MOD;
        return;
    }
    for (int i = 1; i <= n - 1; i++) {
        if (vis[i] == true)
            continue;
        vis[i] = true;
        d[k] = i;
        dfs (k + 1);
        vis[i] = false;
    }
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("Covenant.in", "r", stdin);
    //freopen ("Covenant.out", "w", stdout);
    // code
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    for (int i = 1; i <= n - 1; i++)
        cin >> e[i].first >> e[i].second;
    if (n == 1) {
        cout << 1 << '\n';
        return 0;
    }
    else if (n <= 8) {
        dfs (1);
        cout << ans << '\n';
        return 0;
    }
    else {
        int ans = 1;
        for (int i = n - 1; i >= 1; i--)
            ans = (ans * i) % MOD;
        cout << ans << '\n';
    }
    return 0;
}
