#include <bits/stdc++.h>
using namespace std;
static const int MOD=998244353;
long long modpow(long long a,long long e){long long r=1;for(;e;e>>=1,a=a*a%MOD)if(e&1)r=r*a%MOD;return r;}
int main(){
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<int> p(n+1), who(n+1);
    for(int i=1;i<=n;i++){cin>>p[i];who[p[i]]=i;}
    vector<vector<int>> g(n+1);
    for(int i=1,u,v;i<n;i++){cin>>u>>v;g[u].push_back(v);g[v].push_back(u);}    
    if(n==1){cout<<1<<'\n';return 0;}
    // up[v] = size reachable from v by following strictly increasing p edges.
    vector<int> up(n+1,1);
    for(int val=n;val>=1;--val){
        int v=who[val];
        long long s=1;
        for(int w:g[v]) if(p[w]>p[v]) s+=up[w];
        up[v]=(int)s;
    }
    vector<int> par(n+1),ord;ord.reserve(n);ord.push_back(1);
    for(size_t i=0;i<ord.size();++i){int v=ord[i];for(int w:g[v])if(w!=par[v]){par[w]=v;ord.push_back(w);}}
    auto factor=[&](int child,int parent)->int{
        if(p[parent]<p[child]) return up[child];
        return up[child]-up[parent];
    };
    long long D1=1;
    for(int v:ord) if(v!=1) D1=D1*factor(v,par[v])%MOD;
    vector<int>D(n+1);D[1]=(int)D1;
    for(size_t i=1;i<ord.size();++i){
        int v=ord[i],u=par[v];
        int oldf=factor(v,u),newf=factor(u,v);
        D[v]=(long long)D[u]*modpow(oldf,MOD-2)%MOD*newf%MOD;
    }
    long long fact=1;for(int i=1;i<=n-1;i++)fact=fact*i%MOD;
    long long ans=0;
    for(int r=1;r<=n;r++){
        bool localMax=true;for(int w:g[r])if(p[w]>p[r]){localMax=false;break;}
        if(localMax) ans=(ans+fact*modpow(D[r],MOD-2))%MOD;
    }
    cout<<ans<<'\n';
}