#include <bits/stdc++.h>
using namespace std;
#define int long long
int T;
int a[1000010];
int r[1000010];
inline void solve () {
    int n, k;
    cin >> n >> k;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    if (k == 1) {
        int tot = a[1];
        for (int i = 2; i <= n; i++)
            tot &= a[i];
        cout << tot << '\n';
        return;
    }
    if (k == 2) {
        r[n] = a[n];
        for (int i = n - 1; i >= 1; i--)
            r[i] = (r[i + 1] & a[i]);
        int l = a[1];
        int ans = 0;
        ans = max (ans, (l | r[2]));
        for (int i = 2; i <= n - 1; i++) {
            l &= a[i];
            ans = max (ans, (l | r[i + 1]));
        }
        cout << ans << '\n';
        return;
    }
    bool ok = false;
    for (int i = 1; i <= n; i++) {
        if (a[i] == 3) {
            ok = true;
            break;
        }
    }
    if (k >= 3 && ok) {
        cout << 3 << '\n';
        return;
    }
    if (a[1] == 1 && a[n] == 2) {
        cout << 3 << '\n';
        return;
    }
    if (a[1] == 2 && a[n] == 1) {
        cout << 3 << '\n';
        return;
    }
    if (k >= 3) {
        int id1 = 0, id2 = 0, id3 = 0, id4 = 0;
        for (int i = 1; i <= n; i++) {
            if (a[i] != 1) {
                id1 = i;
                break;
            }
        }
        if (id1 != 1 && a[id1] == 2) {
            cout << 3 << '\n';
            return;
        }
        for (int i = 1; i <= n; i++) {
            if (a[i] != 2) {
                id2 = i;
                break;
            }
        }
        if (id2 != 1 && a[id2] == 1) {
            cout << 3 << '\n';
            return;
        }
        for (int i = n; i >= 1; i--) {
            if (a[i] != 1) {
                id3 = i;
                break;
            }
        }
        if (id3 != n && a[id3] == 2) {
            cout << 3 << '\n';
            return;
        }
        for (int i = n; i >= 1; i--) {
            if (a[i] != 2) {
                id4 = i;
                break;
            }
        }
        if (id4 != n && a[id4] == 1) {
            cout << 3 << '\n';
            return;
        }
    }
    if (k >= 4) {
        for (int i = 1; i <= n - 1; i++) {
            if (a[i] == 1 && a[i + 1] == 2) {
                cout << 3 << '\n';
                return;
            }
        }
        for (int i = 1; i <= n - 1; i++) {
            if (a[i] == 2 && a[i + 1] == 1) {
                cout << 3 << '\n';
                return;
            }
        }
        bool ok1 = false, ok2 = false;
        for (int i = 1; i <= n; i++) {
            if (a[i] == 1)
                ok1 = true;
            if (a[i] == 2)
                ok2 = true;
        }
        if (ok1 == true && (a[1] == 2 || a[n] == 2)) {
            cout << 3 << '\n';
            return;
        }
        if (ok2 == true && (a[1] == 1 || a[n] == 1)) {
            cout << 3 << '\n';
            return;
        }
    }
    if (k >= 5) {
        bool ok1 = false, ok2 = false;
        for (int i = 1; i <= n; i++) {
            if (a[i] == 1)
                ok1 = true;
            if (a[i] == 2)
                ok2 = true;
        }
        if (ok1 == true && ok2 == true) {
            cout << 3 << '\n';
            return;
        }
    }
    if (k >= 3) {
        for (int i = 1; i <= n; i++) {
            if (a[i] == 2) {
                cout << 2 << '\n';
                return;
            }
        }
    }
    if (k >= 3) {
        for (int i = 1; i <= n; i++) {
            if (a[i] == 1) {
                cout << 1 << '\n';
                return;
            }
        }
    }
    cout << 0 << '\n';
    return;
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    freopen ("game.in", "r", stdin);
    freopen ("game.out", "w", stdout);
    cin >> T;
    while (T--)
        solve ();
    return 0;
}
