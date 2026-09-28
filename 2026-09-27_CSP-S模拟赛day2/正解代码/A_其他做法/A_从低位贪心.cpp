#include <bits/stdc++.h>
using namespace std;
#define int long long
// 从低位往高位扫（这种写法叫 NAF，非相邻形式）：
// 当前位 v = 原来的位 + 进位
// v = 1 时看高一位：高一位是 1（末两位 11）就填 -1、往上进 1；否则填 +1
// v = 2 就填 0、往上进 1；v = 0 填 0
string s;
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("multiply.in", "r", stdin);
    //freopen ("multiply.out", "w", stdout);
    cin >> s;
    int n = s.size ();
    reverse (s.begin (), s.end ());
    int c = 0, k = 0;
    for (int i = 0; i < n; i++) {
        int v = s[i] - '0' + c;
        int nxt = (i + 1 < n) ? s[i + 1] - '0' : 0;
        if (v == 1) {
            k++;
            c = nxt;
        }
        else
            c = v / 2;
    }
    k += c;
    cout << 2 * k - 1 << '\n';
    return 0;
}
