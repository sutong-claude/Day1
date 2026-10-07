#include <bits/stdc++.h>
using namespace std;

// O(n) 证明版。
// k=1 / k=2 直接精确处理。
// k>=3 时先问得到 3 至少需要多少个段；若不行，再看 bit1/bit0。

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    freopen("game.in", "r", stdin);
    freopen("game.out", "w", stdout);

    int T;
    cin >> T;

    while (T--) {
        int n, k;
        cin >> n >> k;
        vector<int> a(n);
        for (int &x : a) cin >> x;

        if (k == 1) {
            int z = a[0];
            for (int i = 1; i < n; i++) z &= a[i];
            cout << z << '\n';
            continue;
        }

        if (k == 2) {
            vector<int> suf(n);
            suf[n - 1] = a[n - 1];
            for (int i = n - 2; i >= 0; i--)
                suf[i] = suf[i + 1] & a[i];

            int pref = a[0], ans = 0;
            for (int cut = 0; cut < n - 1; cut++) {
                if (cut > 0) pref &= a[cut];
                ans = max(ans, pref | suf[cut + 1]);
            }
            cout << ans << '\n';
            continue;
        }

        bool has1 = false, has2 = false, has3 = false;
        for (int x : a) {
            has1 |= (x == 1);
            has2 |= (x == 2);
            has3 |= (x == 3);
        }

        // 单独一个 3 就能作为同时保留两个 bit 的段。
        // k>=3 时，内部位置也最多只需“前缀 | [3] | 后缀”三段，之后还能继续细分。
        if (has3) {
            cout << 3 << '\n';
            continue;
        }

        if (has1 && has2) {
            int need = 5;

            // 3 段即可：两种 witness 位于两端，或者某个端点 maximal run
            // 紧接着就是另一种值；右端对称。
            if ((a.front() == 1 && a.back() == 2) ||
                (a.front() == 2 && a.back() == 1))
                need = 3;

            int i = 0;
            while (i < n && a[i] == 1) i++;
            if (i > 0 && i < n && a[i] == 2) need = min(need, 3);

            i = 0;
            while (i < n && a[i] == 2) i++;
            if (i > 0 && i < n && a[i] == 1) need = min(need, 3);

            i = n - 1;
            while (i >= 0 && a[i] == 1) i--;
            if (i < n - 1 && i >= 0 && a[i] == 2) need = min(need, 3);

            i = n - 1;
            while (i >= 0 && a[i] == 2) i--;
            if (i < n - 1 && i >= 0 && a[i] == 1) need = min(need, 3);

            // 4 段即可：任意相邻的 1/2 两个 maximal run，
            // 或一种 witness 在端点、另一种在任意位置。
            bool adjacent = false;
            for (int j = 0; j + 1 < n; j++)
                if ((a[j] == 1 && a[j + 1] == 2) ||
                    (a[j] == 2 && a[j + 1] == 1))
                    adjacent = true;

            bool endpoint =
                (((a.front() == 1 || a.back() == 1) && has2) ||
                 ((a.front() == 2 || a.back() == 2) && has1));

            if (adjacent || endpoint) need = min(need, 4);

            // 若都不满足，任取一个 1 和一个 2，各自单独成段，
            // 最坏是 prefix | [1] | middle | [2] | suffix，共5段。
            if (k >= need) {
                cout << 3 << '\n';
                continue;
            }
        }

        // 已知做不到3。
        // k>=3 时，任意一个 2 最多用三段就能隔离成一个 AND 含 bit1 的段。
        if (has2) {
            cout << 2 << '\n';
            continue;
        }

        if (has1) {
            cout << 1 << '\n';
            continue;
        }

        cout << 0 << '\n';
    }

    return 0;
}
