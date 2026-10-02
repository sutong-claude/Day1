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
int a[1000010];
unordered_map <int, int> mp1, mp2;
int ans = 0;
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("Sunder.in", "r", stdin);
    //freopen ("Sunder.out", "w", stdout);
    // code
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    bool special = true;
    for (int i = 1; i <= n - 1; i++) {
        if (a[i + 1] < a[i]) {
            special = false;
            break;
        }
    }
    if (n <= 2000) {
        for (int i = 1; i <= n; i++) {
            for (int j = i + 1; j <= n; j++) {
                mp1.clear(), mp2.clear();
                for (int k = i; k <= j; k++)
                    mp2[a[k]]++;
                for (int k = i; k <= j; k++) {
                    mp1[a[k]]++;
                    mp2[a[k]]--;
                    if (mp2[a[k]] == 0)
                        mp2.erase(a[k]);
                    bool ok = true;
                    for (auto y : mp1) {
                        if (mp2.count(y.first) == false) {
                            ok = false;
                            break;
                        }
                    }
                    for (auto y : mp2) {
                        if (mp1.count(y.first) == false) {
                            ok = false;
                            break;
                        }
                    }
                    if (ok) {
                        ans++;
                        break;
                    }
                }
            }
        }
        cout << ans << '\n';
        return 0;
    }
    else if (special == true) {
        cout << 0 << '\n';
        return 0;
    }
    else {
        int p = a[1];
        int cnt = 0;
        for (int i = 1; i <= n; i++) {
            if (p == a[i])
                cnt++;
            else {
                p = a[i];
                ans += cnt * (cnt - 1) / 2;
            }
        }
        cout << ans << '\n';
    }
    return 0;
}