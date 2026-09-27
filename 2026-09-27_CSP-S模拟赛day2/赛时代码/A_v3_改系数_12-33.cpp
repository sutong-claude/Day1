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
string s;
int a[1000010];
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("multiply.in", "r", stdin);
    //freopen ("multiply.out", "w", stdout);
    // code
    cin >> s;
    int n = s.size ();
    s = " " + s;
    int tot = 0;
    for (int i = 1; i <= n; i++)
        a[i] = s[i] - '0';
    for (int i = 1; i <= n; i++) {
        if (a[i] == 1) {
            if (a[i + 1] != 1)
                tot += 2;
            else if (a[i + 2] != 1)
                tot += 4;
            else {
                tot += 4;
                int point = i + 1;
                while (point <= n && a[point] == 1)
                    point++;
                i = point;
            }
        }
    }
    cout << tot - 1 << '\n';
    return 0;
}
