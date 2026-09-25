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
int a[1000010];
multiset <int> st1, st2;
inline void solve () {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    int ans = 0;
    st1.clear();
    st1.insert(a[1]);
    for (int i = 2; i <= n; i++) {
        int num = distance (st1.upper_bound(a[i]), st1.end());
        ans += num;
        st1.insert (a[i]);
    }
    int tot = ans;
    for (int i = 1; i <= n; i++) {
        st1.clear();
        st2.clear();
        st1.insert(a[i]);
        st2.insert (a[i]);
        int x = 0, y = 0;
        for (int j = i + 1; j <= n; j++) {
            int num = distance (st1.upper_bound(a[j]), st1.end());
            x += num;
            st1.insert (a[j]);
            num = distance (st2.upper_bound(a[j]), st2.end());
            y += j - i - num;
            st2.insert (a[j]);
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
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    // code
    cin >> T;
    while (T--)
        solve ();
    return 0;
}
