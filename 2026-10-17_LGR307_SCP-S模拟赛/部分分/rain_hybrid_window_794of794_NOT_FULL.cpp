#include <bits/stdc++.h>
using namespace std;
constexpr int INF=1000000000;
// PARTIAL ONLY. Exact in the following cases: already sorted, k=1, k=2,
// a successful constructive certificate,
// a[n]=0, n<=40, bounded-window DP certificate, or (a[n]+1)*n <= 120 million with a[n]<16384.
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
// Constructive certificate (SUFFICIENT, NOT NECESSARY):
// Fix greedily maximal XOR-compatible blocks. Require the final block to be
// already nondecreasing (last XOR mask is zero); traverse earlier blocks
// right-to-left, maximizing feasible first transformed value using 30-bit DP.
// If it succeeds, the answer is provably k-1; if not, remain undecided.
bool certifyGreedyPartition(const vector<int>&a,int k) {
    int n=a.size(),l=0,req[30];fill(req,req+30,-1);
    vector<pair<int,int>>segs;segs.reserve(k);
    for(int i=0;i<n-1;i++){
        unsigned d=a[i]^a[i+1];
        if(!d)continue;
        int b=31-__builtin_clz(d),v=(a[i]>>b)&1;
        if(req[b]>=0&&req[b]!=v){
            segs.emplace_back(l,i);l=i+1;fill(req,req+30,-1);
        } else req[b]=v;
    }
    segs.emplace_back(l,n-1);
    int lastStart=segs.back().first;
    for(int i=lastStart+1;i<n;i++)if(a[i-1]>a[i])return false;
    int bound=a[lastStart];
    for(int j=(int)segs.size()-2;j>=0;--j){
        int x=segs[j].first,y=segs[j].second;
        fill(req,req+30,-1);
        for(int i=x;i<y;i++){
            unsigned d=a[i]^a[i+1];
            if(!d)continue;
            int b=31-__builtin_clz(d),v=(a[i]>>b)&1;
            if(req[b]>=0&&req[b]!=v)return false;
            req[b]=v;
        }
        bound=bestFirst(x,y,bound,a,req);
        if(bound<0)return false;
    }
    return true;
}

// Sound bounded-window frontier DP: explores multiple compatible partitions.
// The budget and window restrictions are deliberate: false negatives are
// possible, but every accepted state witnesses an actual achievable sequence.
bool certifyWindowDP(const vector<int>&a,int k) {
    int n=(int)a.size();
    if(n>120000)return false;
    constexpr int L=8,SLACK=2,INFQ=1000000000;
    struct State{
        int base;
        array<int,SLACK+1>best;
        State(){base=INFQ;best.fill(-1);}
    };
    vector<State> dp(n);
    bool suffixSorted=true;
    for(int i=n-1;i>=0;--i) {
        if(i<n-1&&a[i]>a[i+1])suffixSorted=false;
        int req[30];fill(req,req+30,-1);
        pair<int,int>cand[128];int cnt=0;
        if(suffixSorted)cand[cnt++]={0,a[i]};
        for(int r=i;r<n-1&&r<i+L;r++) {
            if(r>i) {
                unsigned d=a[r-1]^a[r];
                if(d) {
                    int b=31-__builtin_clz(d),v=(a[r-1]>>b)&1;
                    if(req[b]>=0&&req[b]!=v)break;
                    req[b]=v;
                }
            }
            auto &next=dp[r+1];
            if(next.base==INFQ)continue;
            for(int t=0;t<=SLACK;t++)if(next.best[t]>=0) {
                int cost=next.base+t+1;
                int value=bestFirst(i,r,next.best[t],a,req);
                if(value>=0&&cnt<128)cand[cnt++]={cost,value};
            }
        }
        if(!cnt)continue;
        int mn=INFQ;
        for(int j=0;j<cnt;j++)mn=min(mn,cand[j].first);
        dp[i].base=mn;
        for(int j=0;j<cnt;j++) {
            int delta=cand[j].first-mn;
            if(delta<=SLACK)dp[i].best[delta]=max(dp[i].best[delta],cand[j].second);
        }
    }
    return dp[0].base<=k-1;
}

int solve(const vector<int>&a) {
    if(is_sorted(a.begin(),a.end()))return 0;
    int k=blocks(a);
    if(k==1)return 1;
    if(a.back()==0)return k; // Without editing n, all target values must be 0.
    if(k==2)return canOneOperation(a)?1:2;
    if(certifyGreedyPartition(a,k)||certifyWindowDP(a,k))return k-1;
    if((int)a.size()<=40)return exact17(a,k);
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
