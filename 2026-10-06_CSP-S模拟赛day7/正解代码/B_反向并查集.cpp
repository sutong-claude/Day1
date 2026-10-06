#include <bits/stdc++.h>
using namespace std;

const int N = 1000010;

int T, n;
int p[N], fa[N], ans[N];
bool on[N];
vector <int> e[N];

int find (int x) {
    if (fa[x] == x)
        return x;
    return fa[x] = find (fa[x]);
}

void solve () {
    cin >> n;

    for (int i = 1; i <= n; i++) {
        cin >> p[i];
        e[i].clear();
        on[i] = false;
        ans[i] = 0;
        fa[i] = i;
    }

    for (int i = 1; i < n; i++) {
        int x, y;
        cin >> x >> y;
        e[x].push_back (y);
        e[y].push_back (x);
    }

    // 倒着看删除过程：
    // 原来是“按 p 的顺序删除，连通块不断分裂”；
    // 倒放后是“按 p 的逆序加点，连通块不断合并”。
    //
    // 当前 DSU 根始终维护这个活跃连通块中
    // 在 p 里最靠前（优先级最高）的点，也就是这个块的负责人。
    for (int i = n; i >= 1; i--) {
        int v = p[i];
        on[v] = true;
        fa[v] = v;

        for (int u : e[v]) {
            if (!on[u])
                continue;

            int r = find (u);

            // 正向删除 v 时，r 所在的连通块会成为 v 的一个下级组。
            // 这个下级组的负责人 r 直接向 v 汇报。
            ans[r] = v;

            // v 的优先级比所有当前活跃点更高，
            // 合并后整个新连通块的负责人就是 v。
            fa[r] = v;
        }
    }

    // 全局最高负责人 p[1] 没有上级，ans[p[1]] 保持 0。
    for (int i = 1; i <= n; i++)
        cout << ans[i] << (i == n ? '\n' : ' ');
}

int main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);

    freopen ("Katheryne.in", "r", stdin);
    freopen ("Katheryne.out", "w", stdout);

    cin >> T;
    while (T--)
        solve ();
    return 0;
}
