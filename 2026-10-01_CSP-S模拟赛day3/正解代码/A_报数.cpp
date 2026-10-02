#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());

    long long sum = 0;
    int ans = 0, first_le = 0;
    for (int t = 1; t <= n; ++t) {
        sum += a[t - 1];
        while (first_le < t && (__int128)a[first_le] * t <= sum) ++first_le;
        ans = max(ans, t - first_le);
    }
    cout << ans << '\n';
    return 0;
}
