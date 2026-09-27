#include <bits/stdc++.h>
using namespace std;
const int N = 2000010;
int n, u;
string s;
int X[N], Y[N];
int cid[2 * N], rid[2 * N], sid[N];
vector <map <int, int> > pool (1);
inline map <int, int> &get (int &id) {
    if (!id) {
        id = pool.size ();
        pool.emplace_back ();
    }
    return pool[id];
}
// col[x]：这一列上的锚点，y -> 层数，y 越大层数越小
inline int ask (map <int, int> &mp, int k) {
    auto it = mp.upper_bound (k);
    if (it == mp.begin ()) return 1e9;
    return prev (it) -> second;
}
inline void put (map <int, int> &mp, int k, int l) {
    auto it = mp.upper_bound (k);
    if (it != mp.begin () && prev (it) -> second <= l) return;
    while (it != mp.end () && it -> second >= l) it = mp.erase (it);
    mp[k] = l;
}
// sid[l] 对应的 map：层数恰好为 l 的锚点的极小点，x 递增 y 递减
inline bool has (int l, int x, int y) {
    if (!sid[l]) return false;
    map <int, int> &mp = pool[sid[l]];
    auto it = mp.upper_bound (x);
    if (it == mp.begin ()) return false;
    return prev (it) -> second <= y;
}
inline void add (int x, int y, int l) {
    put (get (cid[x + n]), y, l);
    put (get (rid[y + n]), x, l);
    map <int, int> &mp = get (sid[l]);
    auto it = mp.lower_bound (x);
    while (it != mp.end () && it -> second >= y) it = mp.erase (it);
    mp[x] = y;
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("chess.in", "r", stdin);
    //freopen ("chess.out", "w", stdout);
    cin >> n >> s;
    for (int i = 1; i <= n; i++) {
        int v = s[i - 1] - '0';
        int r = v >> 2 & 1, y = v >> 1 & 1, b = v & 1;
        X[i] = X[i - 1] + r - y;
        Y[i] = Y[i - 1] + r - b;
    }
    // u：前缀最少有几个格子不在好段里
    add (0, 0, 0);
    for (int i = 1; i <= n; i++) {
        int x = X[i], y = Y[i];
        if (s[i - 1] >= '4') {
            if (x > X[i - 1] && cid[x + n]) u = min (u, ask (pool[cid[x + n]], y));
            if (y > Y[i - 1] && rid[y + n]) u = min (u, ask (pool[rid[y + n]], x));
        }
        else {
            if (has (u, x, y)) continue;
            u++;
            if (!has (u, x, y)) add (x, y, u);
        }
    }
    cout << n - u << '\n';
    return 0;
}
