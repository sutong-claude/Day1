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
bool isValid (const vector<int> &wolves, const string &direction,
                    const vector<int> &b) {
    const int n = direction.size();
    if ((int)wolves.size() != n) return false;
    vector<int> prefix(n + 1);
    for (int i = 0; i < n; ++i) {
        if (wolves[i] != 0 && wolves[i] != 1) return false;
        if (i && wolves[i - 1] && wolves[i]) return false;
        prefix[i + 1] = prefix[i] + wolves[i];
    }
    for (int i = 0; i < n; ++i) {
        if (wolves[i]) continue;
        int truth = direction[i] == 'L'
                        ? prefix[i]
                        : prefix[n] - prefix[i + 1];
        if (truth != b[i]) return false;
    }
    return true;
}
inline void solve () {
    int n;
    cin >> n;
    if (n > 20)
        solve2 (n);
    vector<int> wolves;
    string direction;
    vector<int> b;
    cin >> direction;
    for (int i = 1; i <= n; i++) {
        int t;
        cin >> t;
        b.push_back (t);
    }
    for (int i = 0; i < (1LL << n); i++) {
        int t = i;
        wolves.clear();
        while (t != 0) {
            wolves.push_back(t % 2);
            t /= 2;
        }
        if (isValid(wolves, direction, b)) {
            for (auto y : wolves)
                cout << y;
            cout << '\n';
            return;
        }
    }
    cout << -1 << '\n';
}
inline void solve2 (int n) {
        vector<int> wolves;
    string direction;
    vector<int> b;
    cin >> direction;
    for (int i = 1; i <= n; i++) {
        int t;
        cin >> t;
        b.push_back (t);
    }
    cout << 0;
    for (int i = 1; i < n; i++) {
        if (b[i - 1] > b[i])
            cout << 1 ;
    }
    cout << '\n';
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen (".in", "r", stdin);
    //freopen (".out", "w", stdout);
    // code
    int t;
    cin >> t;
    while (t--)
        solve ();
    return 0;
}
