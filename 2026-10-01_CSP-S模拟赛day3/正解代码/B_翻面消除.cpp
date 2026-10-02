#include <bits/stdc++.h>
using namespace std;

static void solve_one() {
    int n;
    string s;
    cin >> n >> s;

    vector<pair<char,int>> st;
    st.reserve(n);
    for (int i = 0; i < n; ++i) {
        if (!st.empty() && st.back().first == s[i]) st.pop_back();
        else st.push_back({s[i], i + 1});
    }

    if (st.empty()) {
        cout << "YES 1 1\n";
        return;
    }

    int L = 0, R = (int)st.size() - 1;
    while (L < R && st[L].first == st[R].first) {
        ++L; --R;
    }

    int len = R - L + 1;
    if (len & 1) {
        cout << "NO\n";
        return;
    }
    int h = len / 2;
    for (int i = 0; i < h; ++i) {
        if (st[L + i].first != st[L + h + i].first) {
            cout << "NO\n";
            return;
        }
    }

    cout << "YES " << st[L + h].second << ' ' << st[R].second << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; cin >> T;
    while (T--) solve_one();
    return 0;
}
