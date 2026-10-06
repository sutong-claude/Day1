#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> fa;
    DSU(int n=0): fa(n+1) { iota(fa.begin(), fa.end(), 0); }
    int find(int x) { return fa[x]==x ? x : fa[x]=find(fa[x]); }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    freopen("Katheryne.in","r",stdin);
    freopen("Katheryne.out","w",stdout);

    int T;
    cin>>T;
    while(T--){
        int n;
        cin>>n;
        vector<int> p(n+1), active(n+1), leader(n+1), boss(n+1);
        for(int i=1;i<=n;i++) cin>>p[i];

        vector<vector<int>> g(n+1);
        for(int i=1,u,v;i<n;i++){
            cin>>u>>v;
            g[u].push_back(v);
            g[v].push_back(u);
        }

        DSU dsu(n);

        for(int i=n;i>=1;i--){
            int v=p[i];
            active[v]=1;
            dsu.fa[v]=v;
            leader[v]=v;

            // 在树上，v 的不同已激活邻居不可能本来就在同一组件；
            // 这里仍然按 DSU 根处理，写法更稳。
            vector<int> comps;
            for(int to:g[v]) if(active[to])
                comps.push_back(dsu.find(to));

            sort(comps.begin(),comps.end());
            comps.erase(unique(comps.begin(),comps.end()),comps.end());

            for(int r:comps){
                r=dsu.find(r);
                boss[leader[r]]=v;
                dsu.fa[r]=v;
            }
            leader[v]=v;
        }

        boss[p[1]]=0;
        for(int i=1;i<=n;i++)
            cout<<boss[i]<<(i==n?'\n':' ');
    }
    return 0;
}
