#include <bits/stdc++.h>
using namespace std;
#define int long long
int T;
int a[1000010];
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
    // if the answer is 3
    if (k == 2 && (a[1] == 3 || a[n] == 3)) {
        cout << 3 << '\n';
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
    if (k == 2) {
        int pos = 0;
        for (int i = 1; i <= n; i++) {
            if (a[i] != 1) {
                pos = i;
                break;
            }
        }
        bool ok = (pos != 0);
        for (int i = pos; i <= n; i++) {
            if (a[i] != 2) {
                ok = false;
                break;
            }
        }
        if (ok) {
            cout << 3 << '\n';
            return;
        }
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
    }
    // if the answer is 2
    if (k == 2 && (a[1] == 2 || a[n] == 2)) {
        cout << 2 << '\n';
        return;
    }
    if (k >= 3) {
        for (int i = 1; i <= n; i++) {
            if (a[i] == 2) {
                cout << 2 << '\n';
                return;
            }
        }
    }
    // if the answer is 1
    if (k == 2 && (a[1] == 1 || a[n] == 1)) {
        cout << 1 << '\n';
        return;
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
