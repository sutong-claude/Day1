#include <bits/stdc++.h>
using namespace std;

struct Node {
    int ch[26]{};
    int parent = -1;
    int depth = 0;
    int endcnt = 0;
    int childcnt = 0;
    char parentChar = 0;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    freopen("core.in", "r", stdin);
    freopen("core.out", "w", stdout);

    int n, k;
    cin >> n >> k;

    vector<Node> tr(1);
    vector<int> nodesAtDepth(1, 1);
    vector<int> terminalAtDepth(1, 0);
    int maxDepth = 0;

    for (int i = 0; i < n; ++i) {
        string s;
        cin >> s;
        int u = 0;

        for (char c : s) {
            int z = c - 'a';
            if (!tr[u].ch[z]) {
                tr[u].ch[z] = (int)tr.size();
                ++tr[u].childcnt;

                Node v;
                v.parent = u;
                v.depth = tr[u].depth + 1;
                v.parentChar = c;
                tr.push_back(v);

                if ((int)nodesAtDepth.size() <= v.depth) {
                    nodesAtDepth.resize(v.depth + 1);
                    terminalAtDepth.resize(v.depth + 1);
                }
                ++nodesAtDepth[v.depth];
                maxDepth = max(maxDepth, v.depth);
            }
            u = tr[u].ch[z];
        }

        ++tr[u].endcnt;
        ++terminalAtDepth[tr[u].depth];
    }

    nodesAtDepth.resize(maxDepth + 2);
    terminalAtDepth.resize(maxDepth + 2);

    // globalCapacity[d]:
    // 在保证任意两选中字符串 LCP <= d 时，最多能选多少个字符串。
    vector<int> globalCapacity(maxDepth + 1);
    vector<int> earlierLoss(maxDepth + 1);

    int shortStrings = 0;
    for (int d = 0; d <= maxDepth; ++d) {
        shortStrings += terminalAtDepth[d];
        globalCapacity[d] = shortStrings + nodesAtDepth[d + 1];
    }

    // Trie preorder（孩子 a..z）正好是所有前缀字符串的字典序。
    vector<int> st{0};
    int answerNode = -1;

    while (!st.empty()) {
        int u = st.back();
        st.pop_back();

        int d = tr[u].depth;

        // 在 max LCP <= d 时，u 这棵局部区域最多可选：
        // 1) 所有恰好结束于 u 的字符串；
        // 2) 每个孩子子树最多 1 个。
        int localCapacity = tr[u].endcnt + tr[u].childcnt;

        // 为了让 u 成为字典序最小的核心串，
        // 所有更小的同深度前缀区域都必须限制到最多 1 个。
        int allowed = globalCapacity[d] - earlierLoss[d];

        if (localCapacity >= 2 && allowed >= k) {
            answerNode = u;
            break;
        }

        earlierLoss[d] += max(0, localCapacity - 1);

        for (int z = 25; z >= 0; --z)
            if (tr[u].ch[z]) st.push_back(tr[u].ch[z]);
    }

    if (answerNode == 0) {
        cout << "EMPTY\n";
        return 0;
    }

    string ans;
    for (int u = answerNode; u != 0; u = tr[u].parent)
        ans.push_back(tr[u].parentChar);

    reverse(ans.begin(), ans.end());
    cout << ans << '\n';
    return 0;
}
