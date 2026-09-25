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
int T;
inline void solve () {
    int n, k;
    cin >> n >> k;
    string s = "";
    for (int i = 1; i <= n; i++)
        s += i + '0';
    string t = s;
    do {
            string f = t;
            unordered_map <string, int> mp;
        for (int i = 1; i <= k; i++) {
            for (int i = 1; i <= n; i++) {
                f = s[f[i - 1] - '0'];
            }
        }

    } while (next_permutation (s.begin(), s.end()));
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    // code
    cin >> T;
    while (T--)
        solve ();
    return 0;
}
