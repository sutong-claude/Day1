// Day7 D：N<=100 的 19 分机械暴力 / oracle。
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    freopen("Tighnari.in","r",stdin);
    freopen("Tighnari.out","w",stdout);

    int n;
    cin>>n;
    vector<vector<int>> g(n);
    for(int i=1,u,v;i<n;i++){
        cin>>u>>v;
        --u; --v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<int> leaves;
    for(int i=0;i<n;i++)
        if(g[i].size()==1)
            leaves.push_back(i);

    vector<vector<int>> dist(n, vector<int>(n,-1));
    for(int s=0;s<n;s++){
        queue<int> q;
        q.push(s);
        dist[s][s]=0;
        while(!q.empty()){
            int x=q.front(); q.pop();
            for(int y:g[x]) if(dist[s][y]==-1){
                dist[s][y]=dist[s][x]+1;
                q.push(y);
            }
        }
    }

    long long best=-1, ways=0;
    for(int ii=0;ii<(int)leaves.size();ii++){
        for(int jj=ii+1;jj<(int)leaves.size();jj++){
            int A=leaves[ii], B=leaves[jj];
            int len=dist[A][B];
            int H=0;

            for(int x=0;x<n;x++){
                int toPath=(dist[x][A]+dist[x][B]-len)/2;
                H=max(H,toPath);
            }

            long long value=1LL*H*len;
            if(value>best){
                best=value;
                ways=1;
            }else if(value==best){
                ways++;
            }
        }
    }

    cout<<best<<' '<<ways<<'\n';
    return 0;
}
