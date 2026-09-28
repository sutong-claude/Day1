#include <bits/stdc++.h>
using namespace std;
#define int long long
// 结论：最少项数 = popcount ((3a) xor a)
// 3a = a + 2a，用字符串做高精度加法，再数有几位不一样
string s;
int a[1000010];
signed main () {
    ios::sync_with_stdio (false);
    cin.tie (0);
    cout.tie (0);
    //freopen ("multiply.in", "r", stdin);
    //freopen ("multiply.out", "w", stdout);
    cin >> s;
    int n = s.size ();
    for (int i = 0; i < n; i++)
        a[i] = s[n - 1 - i] - '0';
    int c = 0, k = 0;
    for (int i = 0; i <= n + 1; i++) {
        int x = a[i] + (i > 0 ? a[i - 1] : 0) + c;
        c = x / 2;
        if (x % 2 != a[i])
            k++;
    }
    cout << 2 * k - 1 << '\n';
    return 0;
}
