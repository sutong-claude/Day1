#include <bits/stdc++.h>
using namespace std;

// 16 状态 DP：
// state = (已经结束的段的 OR, 当前最后一段的 AND)
// dp[state] = 得到这个状态所需的最少段数。
// 每来一个 a[i]：要么扩展当前段，要么新开一段。
// 最终求每个答案值 0..3 所需的最少段数。

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    freopen("game.in", "r", stdin);
    freopen("game.out", "w", stdout);

    int T;
    cin >> T;
    const int INF = 1e9;

    while (T--) {
        int n, k;
        cin >> n >> k;

        int x;
        cin >> x;

        array<int, 16> dp, ndp;
        dp.fill(INF);
        dp[x] = 1;  // (or_before=0, last_and=x)

        for (int i = 1; i < n; ++i) {
            cin >> x;
            ndp.fill(INF);

            for (int st = 0; st < 16; ++st) if (dp[st] < INF) {
                int old_or = st >> 2;
                int last_and = st & 3;
                int seg = dp[st];

                // 继续当前段
                int extend = (old_or << 2) | (last_and & x);
                ndp[extend] = min(ndp[extend], seg);

                // 在 x 前切一刀，新开一段
                int split = ((old_or | last_and) << 2) | x;
                ndp[split] = min(ndp[split], seg + 1);
            }

            dp = ndp;
        }

        int need[4] = {INF, INF, INF, INF};
        for (int st = 0; st < 16; ++st) if (dp[st] < INF) {
            int value = (st >> 2) | (st & 3);
            need[value] = min(need[value], dp[st]);
        }

        for (int value = 3; value >= 0; --value) {
            if (need[value] <= k) {
                cout << value << '\n';
                break;
            }
        }
    }

    return 0;
}
