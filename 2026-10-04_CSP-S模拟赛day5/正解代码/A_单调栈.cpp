#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int64> d(n + 2), r(n + 2), f(n + 2);
    for (int i = 1; i <= n; ++i) {
        cin >> d[i];
        r[i] = i + d[i];
    }

    // nxt[i] = first j>i with r[j] >= r[i]
    vector<int> nxt(n + 2, n + 1), st;
    st.reserve(n);

    for (int i = n; i >= 1; --i) {
        while (!st.empty() && r[st.back()] < r[i])
            st.pop_back();
        if (!st.empty())
            nxt[i] = st.back();
        st.push_back(i);
    }

    for (int i = n; i >= 1; --i) {
        int j = nxt[i];

        if (j <= n && j <= r[i]) {
            int64 h = j - i;
            f[i] = f[j] + h * (2 * d[i] - h);
        } else {
            int k = (int)min<int64>(r[i], n + 1);
            f[i] = f[k] + d[i] * d[i];
        }
    }

    for (int i = 1; i <= n; ++i)
        cout << f[i] << '\n';

    return 0;
}
