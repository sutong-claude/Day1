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
int t;
inline void solve () {
    int n;
    cin >> n;
    string s;
    cin >> s;
    s = " " + s;
    int l = 1, r = n;
    while (s[l] == s[r])
        l++, r--;
    string t = "";
    for (int i = l; i <= r; i++)
        t += s[i];
    stack <pair <char, int>> st;
    for (int i = 0; i < r - l + 1; i++) {
        if (!st.empty() && st.top().first == t[i])
            st.pop();
        else
            st.push ({t[i], l + i});
    }
    if (st.empty()) {
        cout << "YES" << ' ' << 1 << ' ' << 1 << '\n';
        return;
    }
    string R = "";
    vector <int> id;
    while (!st.empty()) {
        R += st.top().first;
        id.push_back (st.top().second);
        st.pop();
    }
    id.push_back (0);
    reverse (R.begin(), R.end());
    reverse (id.begin(), id.end());
    int len = R.size();
    R = " " + R;
    int p = len / 2;
    int p1 = 1, p2 = p + 1;
    bool ok = true;
    while (p2 <= len) {
        if (R[p1] != R[p2]) {
            ok = false;
            break;
        }
        p1++, p2++;
    }
    if (ok == true) {
        cout << "YES" << ' ';
        cout << id[p + 1] << ' ' << id[len] << '\n';
    }
    else {
        cout << "NO" << '\n';
        return;
    }
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("Oblivion.in", "r", stdin);
    //freopen ("Oblivion.out", "w", stdout);
    // code
    cin >> t;
    while (t--)
        solve ();
    return 0;
}
