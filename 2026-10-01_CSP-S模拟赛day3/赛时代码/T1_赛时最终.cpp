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
int n;
double sum = 0;
vector <double> a;
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("Chant.in", "r", stdin);
    //freopen ("Chant.out", "w", stdout);
    // code
    cin >> n;
    for (int i = 1; i <= n; i++) {
        double t;
        cin >> t;
        a.push_back(t);
        sum += t;
    }
    sort (a.begin(), a.end());
    int tot = n;
    int ans;
    auto it = upper_bound (a.begin(), a.end(), sum / tot);
    if (it == a.end())
        ans = 0;
    else {
        int dis = a.end() - it;
        ans = dis;
    }
    while (!a.empty()) {
        sum -= a.back();
        a.pop_back();
        tot--;
        int res;
        auto it = upper_bound (a.begin(), a.end(), sum / tot);
        if (it == a.end())
            res = 0;
        else {
            int dis = a.end() - it;
            res = dis;
        }
        ans = max (ans, res);
    }
    cout << ans << '\n';
    return 0;
}
