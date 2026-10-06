#include <bits/stdc++.h>
using namespace std;
#define int long long
int n, m;
vector <int> e[1000010];
int d[1000010];
inline void dfs (int root, int fa) {
    if (e[root].size () == 1)
        d[root] = 1;
    for (auto y : e[root]) {
        if (y != fa) {
            dfs (y, root);
            d[root] = max (d[y] + 1, d[root]);
        }
    }
}
int f[1000010];
int path[1000010];
inline void bfs (int root) {
    for (int i = 1; i <= n; i++)
        f[i] = 0;
    queue <int> p;
    p.push (root);
    f[root] = 1;
    path[root] = 0;
    while (!p.empty ()) {
        int cur = p.front();
        p.pop();
        for (auto y : e[cur]) {
            if (f[y] == 0) {
                p.push (y);
                f[y] = f[cur] + 1;
                path[y] = cur;
            }
        }
    }
}
bool vis[1000010];
int cnt = 0;
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    freopen ("net.in", "r", stdin);
    freopen ("net.out", "w", stdout);
    cin >> n >> m;
    for (int i = 1; i <= n - 1; i++) {
        int x, y;
        cin >> x >> y;
        e[x].push_back (y);
        e[y].push_back (x);
    }
    bfs (1);
    int ma1 = 0, id1;
    for (int i = 1; i <= n; i++) {
        if (f[i] > ma1) {
            ma1 = f[i];
            id1 = i;
        }
    }
    bfs (id1);
    vector <int> road;
    int ma2 = 0, id2;
    for (int i = 1; i <= n; i++) {
        if (f[i] > ma2) {
            ma2 = f[i];
            id2 = i;
        }
    }
    int point = id2;
    road.push_back(0);
    while (point != 0) {
        road.push_back(point);
        point = path[point];
    }
    int len = road.size() - 1;
    int pos = len / 2;
    int root = road[pos];
    dfs (root, 0);
    priority_queue <pair <int, int>> p;
    p.push ({d[root], root});
    while (!p.empty()) {
        pair <int, int> cur = p.top();
        vis[cur.second] = true;
        cnt++;
        if (cnt == m)
            break;
        p.pop();
        for (auto y : e[cur.second])
            if (vis[y] == false)
                p.push ({d[y], y});
    }
    int ans = 0;
    for (int i = 1; i <= n; i++)
        if (vis[i] == true)
            for (auto y : e[i])
                if (vis[y] == false)
                    ans = max (ans, d[y]);
    cout << ans << '\n';
    return 0;
}
