#include <bits/stdc++.h>
using namespace std;
#define int long long
// a = (a + b) - b：正的那些项合起来是 a + b，负的合起来是 b，项数 = 两者 1 的个数之和
// 枚举 b 就行，|a| <= 10 时 b 不会超过 2^11
string s;
signed main () {
    cin >> s;
    int a = 0;
    for (auto c : s)
        a = a * 2 + (c - '0');
    int ans = 1e18;
    for (int b = 0; b <= 4 * a + 4; b++)
        ans = min (ans, (int)(__builtin_popcountll (a + b) + __builtin_popcountll (b)));
    cout << 2 * ans - 1 << '\n';
    return 0;
}
