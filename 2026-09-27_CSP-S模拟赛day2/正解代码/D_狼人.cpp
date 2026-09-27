#include <bits/stdc++.h>
using namespace std;
const int N = 2000010;
int T, n, sz;
char d[N];
int b[N], f1[N], f2[N], fw[N], bw[N], reach[N], par[N];
int tr[N * 4], mul[16][16];
vector <pair <int, int> > lab[N];
// 把 0 号和 n + 1 号看成两个虚拟村民，村民 i -> 村民 j（j = i + 1 或 i + 2，中间那个是狼）
// 返回 -2：不能走；-1：能走，和狼的总数 W 无关；>= 0：只有 W 等于这个数时能走
inline int edge (int i, int j) {
    int g = j - i - 1;
    if (i == 0 && j == n + 1) return -1;
    if (i == 0) {
        if (d[j] == 'L') return b[j] == g ? -1 : -2;
        return b[j] + g;
    }
    if (j == n + 1) {
        if (d[i] == 'R') return b[i] == g ? -1 : -2;
        return b[i] + g;
    }
    if (d[i] == 'L' && d[j] == 'L') return b[j] == b[i] + g ? -1 : -2;
    if (d[i] == 'R' && d[j] == 'R') return b[j] == b[i] - g ? -1 : -2;
    if (d[i] == 'L') return b[i] + g + b[j];
    int w = b[i] + b[j] - g;
    return w >= 0 ? w : -2;
}
// 位置 j 的 2x2 布尔矩阵，4 个二进制位：(到 j, 到 j - 1) <- (到 j - 1, 到 j - 2)
inline int leaf (int j) {
    return f1[j] | (f2[j] << 1) | (1 << 2);
}
inline void update (int j) {
    int p = j - 1 + sz;
    tr[p] = leaf (j);
    for (p >>= 1; p >= 1; p >>= 1)
        tr[p] = mul[tr[p * 2 + 1]][tr[p * 2]];
}
inline bool ok (int i, int j, int W) {
    int t = edge (i, j);
    return t == -1 || t == W;
}
inline void solve () {
    scanf ("%d %s", &n, d + 1);
    for (int i = 1; i <= n; i++)
        scanf ("%d", &b[i]);
    if (n == 1) {
        puts ("1");
        return;
    }
    // 先不管 W，看哪些点从起点能到、能走到终点，没用的边直接扔掉
    fw[0] = 1;
    for (int j = 1; j <= n + 1; j++)
        fw[j] = (fw[j - 1] && edge (j - 1, j) != -2) || (j >= 2 && fw[j - 2] && edge (j - 2, j) != -2);
    bw[n + 1] = 1, bw[n + 2] = 0;
    for (int i = n; i >= 0; i--)
        bw[i] = (bw[i + 1] && edge (i, i + 1) != -2) || (i + 2 <= n + 1 && bw[i + 2] && edge (i, i + 2) != -2);
    for (int w = 0; w <= n; w++)
        lab[w].clear ();
    for (int j = 1; j <= n + 1; j++) {
        f1[j] = f2[j] = 0;
        for (int k = 1; k <= 2; k++) {
            int i = j - k;
            if (i < 0 || !fw[i] || !bw[j]) continue;
            int t = edge (i, j);
            if (t == -1) (k == 1 ? f1[j] : f2[j]) = 1;
            else if (t >= 0 && t <= n) lab[t].push_back ({j, k});
        }
    }
    sz = 1;
    while (sz < n + 1) sz <<= 1;
    for (int j = 1; j <= sz; j++)
        tr[j - 1 + sz] = (j <= n + 1) ? leaf (j) : 9;
    for (int p = sz - 1; p >= 1; p--)
        tr[p] = mul[tr[p * 2 + 1]][tr[p * 2]];
    int W = -1;
    for (int w = 0; w <= n && W == -1; w++) {
        if (lab[w].empty ()) continue;
        for (auto e : lab[w]) {
            (e.second == 1 ? f1[e.first] : f2[e.first]) = 1;
            update (e.first);
        }
        if (tr[1] & 1) W = w;
        for (auto e : lab[w]) {
            (e.second == 1 ? f1[e.first] : f2[e.first]) = 0;
            update (e.first);
        }
    }
    if (W == -1) {
        puts ("-1");
        return;
    }
    // W 定了，普通 DP 找一条路
    reach[0] = 1;
    for (int j = 1; j <= n + 1; j++) {
        reach[j] = 0;
        if (reach[j - 1] && ok (j - 1, j, W)) reach[j] = 1, par[j] = j - 1;
        else if (j >= 2 && reach[j - 2] && ok (j - 2, j, W)) reach[j] = 1, par[j] = j - 2;
    }
    string s (n, '1');
    for (int j = par[n + 1]; j > 0; j = par[j])
        s[j - 1] = '0';
    puts (s.c_str ());
}
signed main () {
    //freopen ("wolf.in", "r", stdin);
    //freopen ("wolf.out", "w", stdout);
    for (int x = 0; x < 16; x++)
        for (int y = 0; y < 16; y++) {
            int a = x & 1, bb = x >> 1 & 1, c = x >> 2 & 1, dd = x >> 3 & 1;
            int e = y & 1, f = y >> 1 & 1, g = y >> 2 & 1, h = y >> 3 & 1;
            mul[x][y] = ((a & e) | (bb & g)) | (((a & f) | (bb & h)) << 1) | (((c & e) | (dd & g)) << 2) | (((c & f) | (dd & h)) << 3);
        }
    scanf ("%d", &T);
    while (T--)
        solve ();
    return 0;
}
