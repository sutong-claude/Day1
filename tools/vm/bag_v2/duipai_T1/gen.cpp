#include <bits/stdc++.h>
using namespace std;
#define int long long
mt19937_64 rng;
inline int Rand (int l, int r) {
    return rng () % (r - l + 1) + l;
}
signed main (signed argc, char *argv[]) {
    // duipai.sh 会把组号传进来当种子，哪组错了就能用 ./gen 组号 重现
    rng.seed (argc >= 2 ? atoll (argv[1]) : time (0));
    // 下面是例子，按题目改；数据要小，暴力才跑得动
    int n = Rand (1, 10);
    cout << n << '\n';
    for (int i = 1; i <= n; i++)
        cout << Rand (1, 10) << " \n"[i == n];
    return 0;
}
