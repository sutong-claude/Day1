#include <bits/stdc++.h>
using namespace std;
#define int long long
int T;
int a[1000010];
int lst[1000010], rst[1000010];
multiset <int> st1, st2;
inline void solve () {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    st1.clear();
    st2.clear();
    st1.insert(a[1]);
    for (int i = 2; i <= n; i++) {
        int num = distance (st1.upper_bound(a[i]), st1.end());
        lst[i] = lst[i - 1] + num;
        st1.insert (a[i]);
    }
//    for (int i = 1; i <= n; i++)
//        cout << lst[i] << ' ';
//    cout << '\n';
    st2.insert(a[1]);
    for (int i = 2; i <= n; i++) {
        int num = distance (st2.upper_bound(a[i]), st2.end());
        //cout << num << ' ';
        rst[i] = rst[i - 1] + i - num - 1;
        st2.insert (a[i]);
    }
//    for (int i = 1; i <= n; i++)
//       cout << rst[i] << ' ';
//    cout << '\n';
    int ans = 0;
    int ma = (lst[1] - rst[1]);
    for (int i = 2; i <= n; i++) {
        int res = (rst[i] - lst[i]) + ma;
        ans = max (ans, res);
        ma = max (rst[i] - lst[i], ma);
    }
    cout << lst[n] + ans << '\n';
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
