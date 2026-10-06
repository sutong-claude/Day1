#include <bits/stdc++.h>
using namespace std;
#define int long long
int n;
int l[1000010], r[1000010];
vector <int> e[1000010];
bool vis[1000010];
int d[1000010];
int res = 1;
int ans = 1;
inline void dfs (int root, int time) {
    for (auto y : e[root]) {
        if (vis[y] == true)
            continue;
        int reach = time + 1;
        if (reach > r[y])
            continue;
        d[y] = d[root] + 1;
        ans = max (ans, d[y]);
        vis[y] = true;
        dfs (y, max (l[y], reach));
        vis[y] = false;
    }
}
int f[1000010];
bool d1[1000010], d2[1000010];
bool vst[1000010];
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    freopen ("tree.in", "r", stdin);
    freopen ("tree.out", "w", stdout);
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> l[i] >> r[i];
    for (int i = 1; i <= n - 1; i++) {
        int x, y;
        cin >> x >> y;
        e[x].push_back (y);
        e[y].push_back (x);
    }
    if (n == 1) {
        cout << 1 << '\n';
        return 0;
    }
    if (n <= 5000) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                vis[j] = false;
                d[j] = 0;
            }
            vis[i] = true;
            d[i] = 1;
            ans = 1;
            dfs (i, 0);
            res = max (res, ans);
        }
        cout << res << '\n';
        return 0;
    }
    bool A = true;
    for (int i = 1; i <= n; i++) {
        if (l[i] != r[i]) {
            A = false;
            break;
        }
    }
    if (A) {
        return 0;
    }
    bool B = false;
    int root;
    for (int i = 1; i <= n; i++) {
        if (e[i].size() == n - 1) {
            root = i;
            B = true;
            break;
        }
    }
    if (B) {
        for (int i = 1; i <= n; i++) {
            int reach = l[i] + 1;
            if (reach <= r[root])
                d1[i] = true;
        }
        for (int i = 1; i <= n; i++) {
            int reach = l[root] + 1;
            if (reach <= r[i])
                d2[i] = true;
        }
        int cnt1 = 0;
        for (int i = 1; i <= n; i++)
            if (d1[i] == true)
                cnt1++;
        int cnt2 = 0;
        for (int i = 1; i <= n; i++)
            if (d2[i] == true)
                cnt2++;
        if (cnt1 != 0 && cnt2 != 0) {
            if (cnt1 == 1 && cnt2 == 1) {
                bool ok = true;
                for (int i = 1; i <= n; i++) {
                    if (d1[i] == d2[i] && d1[i] == true) {
                        ok = false;
                        break;
                    }
                }
                if (ok)
                    cout << 3 << '\n';
                else
                    cout << 2 << '\n';
                return 0;
            }
            cout << 3 << '\n';
            return 0;
        }
        if (cnt1 == 0 && cnt2 == 0) {
            cout << 1 << '\n';
            return 0;
        }
        cout << 2 << '\n';
        return 0;
    }
    int cnt1 = 0, cnt2 = 0;
    for (int i = 1; i <= n; i++) {
        if (e[i].size() == 1)
            cnt1++;
        if (e[i].size() == 2)
            cnt2++;
    }
    bool C = false;
    if (cnt1 == 2 && cnt2 == n - 2)
        C = true;
    if (C) {
        int root1 = -1, root2 = -1;
        for (int i = 1; i <= n; i++) {
            if (e[i].size() == 1) {
                if (root1 == -1)
                    root1 = i;
                else
                    root2 = i;
            }
        }
        vector <int> line;
        int point = root1;
        while (point != root2) {
            line.push_back(point);
            vst[point] = true;
            if (point == root1)
                point = e[point][0];
            else {
                if (vst[e[point][0]] == false)
                    point = e[point][0];
                else
                    point = e[point][1];
            }
        }
        line.push_back(root2);
        int L = l[root1], R = r[root1];
        int pos = 0;
        for (int i = 1; i <= n - 1; i++) {
            L = L - 1, R = R - 1;
            L = max (L, l[line[i]]), R = min (R, r[line[i]]);
            if (L > R) {
                pos = i;
                break;
            }
        }
        pos--;
        int pos2 = n;
        L = l[n - 1], R = r[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            L = L - 1, R = R - 1;
            L = max (L, l[line[i]]), R = min (R, r[line[i]]);
            if (L > R) {
                pos2 = i;
                break;
            }
        }
        int res1 = pos - 0 + 1;
        int res2 = n - 1 - pos2 + 1;
        int res = max (res1, res2);
        cout << res << '\n';
        return 0;
    }
    cout << 1 << '\n';
    return 0;
}
