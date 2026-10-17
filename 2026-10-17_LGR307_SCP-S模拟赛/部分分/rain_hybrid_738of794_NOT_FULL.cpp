#include <bits/stdc++.h>
using namespace std;
constexpr int INF=1000000000;
// PARTIAL ONLY. Exact in the following cases: already sorted, k=1, k=2,
// a[n]=0, n<=17, or (a[n]+1)*n <= 120 million with a[n]<16384.
// Other cases return a proven upper bound k, possibly one too large.
int blocks(const vector<int>& a) {
    int k=1,req[30]; fill(req,req+30,-1);
    for(int i=1;i<(int)a.size();++i) {
        unsigned d=a[i-1]^a[i];
        if(!d)continue;
        int b=31-__builtin_clz(d),v=(a[i-1]>>b)&1;
        if(req[b]>=0&&req[b]!=v) {++k;fill(req,req+30,-1);}
        else req[b]=v; // IMPORTANT: conflicting edge belongs to neither block.
    }
    return k;
}
int bestFirst(int l,int r,int limit,const vector<int>&a,const int req[30]) {
    int d=a[l]^a[r],eq=0,lo=-1;
    for(int b=29;b>=0;--b) {
        int neq=-1,nlo=-1;
        int allowed=req[b]<0?3:(1<<(req[b]^((a[r]>>b)&1)));
        for(int state=0;state<2;state++) {
            int cur=state?lo:eq;if(cur<0)continue;
            for(int y=0;y<2;y++)if(allowed&(1<<y)) {
                if(!state&&y>((limit>>b)&1))continue;
                int target=cur|((y^((d>>b)&1))<<b);
                if(state||y<((limit>>b)&1))nlo=max(nlo,target);
                else neq=max(neq,target);
            }
        }
        eq=neq;lo=nlo;
    }
    return max(eq,lo);
}
// Exact interval / bit-DP for n<=17, values <2^30.
int exact17(const vector<int>&a,int upper) {
    int n=a.size(); if(n==1)return 0;
    vector<vector<int>>dp(n+1,vector<int>(n,-1));
    bool sorted=true;
    for(int l=n-1;l>=0;--l) {
        if(l<n-1&&a[l]>a[l+1])sorted=false;
        if(sorted)dp[l][0]=a[l];
        int req[30];fill(req,req+30,-1);
        for(int r=l;r<n-1;r++) {
            if(r>l) {
                unsigned d=a[r-1]^a[r];
                if(d) {
                    int b=31-__builtin_clz(d),v=(a[r-1]>>b)&1;
                    if(req[b]>=0&&req[b]!=v)break;
                    req[b]=v;
                }
            }
            for(int used=0;used<n-1;used++)if(dp[r+1][used]>=0) {
                int v=bestFirst(l,r,dp[r+1][used],a,req);
                if(v>=0)dp[l][used+1]=max(dp[l][used+1],v);
            }
        }
    }
    for(int used=0;used<n;used++)if(dp[0][used]>=0)return min(used,upper);
    return upper;
}
// Exact value DP: target last value is fixed, and all earlier target values <= a[n].
int exactBounded(const vector<int>&a,int upper) {
    int n=a.size(),V=a.back()+1;
    vector<int>f(V,INF),g(V),suffix(V+1);f[a.back()]=0;
    for(int i=n-2;i>=0;--i) {
        suffix[V]=INF;
        for(int x=V-1;x>=0;--x)suffix[x]=min(suffix[x+1],f[x]);
        int d=a[i]^a[i+1];
        for(int v=0;v<V;v++) {
            int w=v^d;
            g[v]=min(w>=v&&w<V?f[w]:INF,1+suffix[v]);
        }
        f.swap(g);
    }
    return min(*min_element(f.begin(),f.end()),upper);
}
// Exact one-operation test for k=2: one edited prefix + unchanged sorted suffix.
bool canOneOperation(const vector<int>&a) {
    int n=a.size();
    vector<unsigned char>rightGood(n+1);
    rightGood[n]=1;
    if(n)rightGood[n-1]=1;
    for(int i=n-2;i>=0;--i)rightGood[i]=rightGood[i+1]&&(a[i]<=a[i+1]);
    int req[30];fill(req,req+30,-1);
    for(int p=1;p<n;p++) {
        if(p>1) {
            unsigned d=a[p-2]^a[p-1];
            if(d) {
                int j=31-__builtin_clz(d),v=(a[p-2]>>j)&1;
                if(req[j]>=0&&req[j]!=v)return false;
                req[j]=v;
            }
        }
        if(!rightGood[p])continue;
        unsigned minEnd=0;
        for(int b=0;b<30;b++)if(req[b]>=0)
            minEnd|=(unsigned)(req[b]^((a[p-1]>>b)&1))<<b;
        if(minEnd<=(unsigned)a[p])return true;
    }
    return false;
}
int solve(const vector<int>&a) {
    if(is_sorted(a.begin(),a.end()))return 0;
    int k=blocks(a);
    if(k==1)return 1;
    if(a.back()==0)return k; // Without editing n, all target values must be 0.
    if(k==2)return canOneOperation(a)?1:2;
    if((int)a.size()<=17)return exact17(a,k);
    if(a.back()<16384&&1LL*a.size()*(a.back()+1)<=120000000LL)
        return exactBounded(a,k);
    return k; // NOT ALWAYS EXACT!
}
int main() {
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int c,t;cin>>c>>t;
    while(t--) {
        int n;cin>>n;vector<int>a(n);
        for(int &x:a)cin>>x;
        cout<<solve(a)<<'\n';
    }
}
