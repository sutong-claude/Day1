#include <bits/stdc++.h>
using namespace std;
#define int long long
// O(n^2)，30 分。X、Y 是“红 - 黄”“红 - 蓝”的前缀和，(j, i] 是好段 <=> X[j] <= X[i] 且 Y[j] <= Y[i]
int n;
string s;
int X[1000010], Y[1000010], f[1000010];
signed main () {
    cin >> n >> s;
    for (int i = 1; i <= n; i++) {
        int v = s[i - 1] - '0';
        X[i] = X[i - 1] + (v >> 2 & 1) - (v >> 1 & 1);
        Y[i] = Y[i - 1] + (v >> 2 & 1) - (v & 1);
    }
    for (int i = 1; i <= n; i++) {
        f[i] = f[i - 1];
        for (int j = 0; j < i; j++)
            if (X[j] <= X[i] && Y[j] <= Y[i])
                f[i] = max (f[i], f[j] + i - j);
    }
    cout << f[n] << '\n';
    return 0;
}
