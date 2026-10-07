#include <bits/stdc++.h>
using namespace std;

struct State {
    int u, parent, len;
    long long time;
};

// 精确 O(N^2) partial：覆盖 N<=5000。
// 固定起点 s 后，树上到每个终点的路径唯一。
// 沿路径每次取“最早可行访问日”，若超过 r[v] 则该方向不可能。

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    freopen("tree.in", "r", stdin);
    freopen("tree.out", "w", stdout);

    int n;
    cin >> n;

    vector<long long> l(n + 1), r(n + 1);
    for (int i = 1; i <= n; ++i)
        cin >> l[i] >> r[i];

    vector<vector<int>> g(n + 1);
    for (int i = 1; i < n; ++i) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    int ans = 1;
    vector<State> st;
    st.reserve(n);

    for (int s = 1; s <= n; ++s) {
        st.clear();
        st.push_back({s, 0, 1, l[s]});

        while (!st.empty()) {
            State cur = st.back();
            st.pop_back();

            ans = max(ans, cur.len);

            for (int v : g[cur.u]) {
                if (v == cur.parent) continue;

                long long nextTime = max(l[v], cur.time + 1);
                if (nextTime <= r[v])
                    st.push_back({v, cur.u, cur.len + 1, nextTime});
            }
        }
    }

    cout << ans << '\n';
    return 0;
}
