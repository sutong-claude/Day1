#include <bits/stdc++.h>
using namespace std;
#define int long long
// 子任务 1：直接按定义算。f(i, j) = 最大的 d，使得前 i 个串里至少 j 个串长度 >= d 且前 d 个字符相同
int n;
string s[1000010];
signed main () {
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> s[i];
    for (int i = 1; i <= n; i++) {
        int ans = 0;
        for (int j = 1; j <= i; j++) {
            int f = 0;
            for (int d = 1; d <= 50; d++) {
                map <string, int> mp;
                int mx = 0;
                for (int k = 1; k <= i; k++)
                    if ((int)s[k].size () >= d)
                        mx = max (mx, ++mp[s[k].substr (0, d)]);
                if (mx >= j) f = d;
            }
            ans += (f ^ j);
        }
        cout << ans << '\n';
    }
    return 0;
}
