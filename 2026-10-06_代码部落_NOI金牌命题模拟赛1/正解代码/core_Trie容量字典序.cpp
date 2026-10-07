#include <bits/stdc++.h>
using namespace std;

struct Node {
    int ch[26];
    int parent = -1;
    int depth = 0;
    int endcnt = 0;       // 有多少个字符串恰好结束在这里（保留重复串）
    int childcnt = 0;
    char parentChar = 0;

    Node() {
        memset(ch, 0, sizeof(ch));
    }
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

    for (int i = 0; i < n; i++) {
        string s;
        cin >> s;

        int u = 0;
        for (char c : s) {
            int z = c - 'a';

            if (tr[u].ch[z] == 0) {
                tr[u].ch[z] = (int)tr.size();
                tr[u].childcnt++;

                Node v;
                v.parent = u;
                v.depth = tr[u].depth + 1;
                v.parentChar = c;
                tr.push_back(v);

                if ((int)nodesAtDepth.size() <= v.depth) {
                    nodesAtDepth.resize(v.depth + 1);
                    terminalAtDepth.resize(v.depth + 1);
                }

                nodesAtDepth[v.depth]++;
                maxDepth = max(maxDepth, v.depth);
            }

            u = tr[u].ch[z];
        }

        tr[u].endcnt++;
        terminalAtDepth[tr[u].depth]++;
    }

    nodesAtDepth.resize(maxDepth + 2);
    terminalAtDepth.resize(maxDepth + 2);

    // globalCapacity[d]：在保证任意两选中字符串 LCP <= d 时，最多能选多少个字符串。
    // = 长度 <= d 的字符串个数（可全部选）
    // + 深度 d+1 的不同前缀节点数（每个前缀类最多选1个）。
    vector<int> globalCapacity(maxDepth + 1);
    vector<int> seenExcess(maxDepth + 1);

    int shortStrings = 0;
    for (int d = 0; d <= maxDepth; d++) {
        shortStrings += terminalAtDepth[d];
        globalCapacity[d] = shortStrings + nodesAtDepth[d + 1];
    }

    // Trie 的 preorder（节点先于子孙，孩子 a..z）就是所有前缀字符串的字典序。
    // 用显式栈避免 2e5 深度递归爆栈。
    vector<int> st;
    st.push_back(0);

    int answerNode = -1;

    while (!st.empty()) {
        int u = st.back();
        st.pop_back();

        int d = tr[u].depth;

        // 在 maxLCP <= d 的前提下，当前前缀 u 内最多可选：
        // - endcnt[u] 个恰好等于 u 的重复字符串；
        // - 每个 child 子树最多1个。
        int localCapacity = tr[u].endcnt + tr[u].childcnt;

        // 若要让 u 成为“字典序最小核心串”，同深度所有字典序更小节点
        // 最多各选1个；seenExcess 记录因此被砍掉的额外容量。
        int allowed = globalCapacity[d] - seenExcess[d];

        if (localCapacity >= 2 && allowed >= k) {
            answerNode = u;
            break;
        }

        // 如果答案还要更靠后，则当前节点也必须限制到最多1个。
        seenExcess[d] += max(0, localCapacity - 1);

        for (int z = 25; z >= 0; z--)
            if (tr[u].ch[z] != 0)
                st.push_back(tr[u].ch[z]);
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
