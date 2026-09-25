#include <bits/stdc++.h>
using namespace std;
#define int long long
const int M = 31700000;
bitset <M + 1> vis;
vector <int> pr;
int t;
int n[10010], k[10010];
bool ans[10010];
int dis[100010];
inline int qpow (int a, int b, int p) {
    int res = 1;
    a %= p;
    while (b) {
        if (b & 1)
            res = (__int128)res * a % p;
        a = (__int128)a * a % p;
        b >>= 1;
    }
    return res;
}
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    for (int i = 2; i <= M; i++) {
        if (vis[i])
            continue;
        pr.push_back(i);
        for (int j = i * i; j <= M; j += i)
            vis[j] = 1;
    }
    cin >> t;
    map <int, vector <int> > mp;
    for (int i = 1; i <= t; i++) {
        cin >> n[i] >> k[i];
        mp[k[i]].push_back(i);
    }
    for (auto &it : mp) {
        int x = it.first;
        vector <int> &id = it.second;
        vector <int> p;
        for (int y : pr) {
            if (y * y > x)
                break;
            if (x % y == 0) {
                p.push_back(y);
                while (x % y == 0)
                    x /= y;
            }
        }
        if (x > 1)
            p.push_back(x);
        if (p.empty()) {
            for (int i : id)
                ans[i] = false;
        }
        else if (p.size() == 1) {
            for (int i : id)
                ans[i] = (n[i] % p[0] == 0);
        }
        else if (p.size() == 2) {
            int a = p[0], b = p[1];
            int inv = qpow (b % a, a - 2, a);
            for (int i : id) {
                int c = (__int128)(n[i] % a) * inv % a;
                ans[i] = ((__int128)c * b <= n[i]);
            }
        }
        else {
            int a = p[0];
            for (int r = 0; r < a; r++)
                dis[r] = LLONG_MAX;
            dis[0] = 0;
            priority_queue <pair <int, int>, vector <pair <int, int> >, greater <pair <int, int> > > pq;
            pq.push({0, 0});
            while (!pq.empty()) {
                int d = pq.top().first, u = pq.top().second;
                pq.pop();
                if (d != dis[u])
                    continue;
                for (int j = 1; j < (int)p.size(); j++) {
                    int v = (u + p[j]) % a;
                    if (d + p[j] < dis[v]) {
                        dis[v] = d + p[j];
                        pq.push({dis[v], v});
                    }
                }
            }
            for (int i : id)
                ans[i] = (dis[n[i] % a] <= n[i]);
        }
    }
    for (int i = 1; i <= t; i++)
        cout << (ans[i] ? "YES" : "NO") << '\n';
    return 0;
}
