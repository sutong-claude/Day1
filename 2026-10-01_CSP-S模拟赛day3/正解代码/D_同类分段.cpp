#include <bits/stdc++.h>
using namespace std;

struct AssignSeg {
    int n; vector<int> sum; vector<signed char>tag;
    AssignSeg(int n=0):n(n),sum(4*n+4,0),tag(4*n+4,-1){}
    inline void apply(int o,int l,int r,int v){sum[o]=v?(r-l+1):0;tag[o]=(signed char)v;}
    inline void push(int o,int l,int r){if(tag[o]==-1||l==r)return;int m=(l+r)>>1;apply(o<<1,l,m,tag[o]);apply(o<<1|1,m+1,r,tag[o]);tag[o]=-1;}
    void assignRange(int o,int l,int r,int ql,int qr,int v){
        if(ql>r||qr<l||ql>qr)return;
        if(ql<=l&&r<=qr){apply(o,l,r,v);return;}
        push(o,l,r);int m=(l+r)>>1;
        if(ql<=m)assignRange(o<<1,l,m,ql,qr,v);
        if(qr>m)assignRange(o<<1|1,m+1,r,ql,qr,v);
        sum[o]=sum[o<<1]+sum[o<<1|1];
    }
    void assignRange(int l,int r,int v){if(l<=r)assignRange(1,1,n,l,r,v);}
    int total()const{return sum[1];}
};

int main(){
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n;if(!(cin>>n))return 0;
    vector<int>a(n+1),pre(n+1),last(n+1,0);
    for(int i=1;i<=n;i++){cin>>a[i];pre[i]=last[a[i]];last[a[i]]=i;}
    // sparse table RMQ minimum on pre[]
    vector<int> lg(n+1);for(int i=2;i<=n;i++)lg[i]=lg[i>>1]+1;
    int K=lg[n]+1;
    vector<vector<int>> st(K,vector<int>(n+1));
    for(int i=1;i<=n;i++)st[0][i]=pre[i];
    for(int k=1;(1<<k)<=n;k++){
        int len=1<<k,half=len>>1;
        for(int i=1;i+len-1<=n;i++) st[k][i]=min(st[k-1][i],st[k-1][i+half]);
    }
    auto rmq=[&](int l,int r){int k=lg[r-l+1];return min(st[k][l],st[k][r-(1<<k)+1]);};
    vector<int>Lnk(n+1,0),Rnk(n+1,0);int head=0,tail=0;
    AssignSeg seg(n); long long ans=0;
    for(int r=1;r<=n;r++){
        int p=pre[r],q=0,t=0;
        if(p){q=Lnk[p];t=Rnk[p];}
        // l>p: a[r] is new in [l,r], hence first=last=r => not good
        seg.assignRange(p+1,r,0);
        if(p){
            int newL=t?t:r;
            int mn=rmq(newL,r);
            int cut=min(p,mn);
            if(q+1<=cut) seg.assignRange(q+1,cut,1);
            // positions cut+1..p were already 0 before (since F>=old L=p), so no explicit clearing needed.
            // remove p from chain
            if(q) Rnk[q]=t; else head=t;
            if(t) Lnk[t]=q; else tail=q;
        }
        // append r as the last occurrence of a[r]
        Lnk[r]=tail;Rnk[r]=0;
        if(tail)Rnk[tail]=r;else head=r;
        tail=r;
        ans+=seg.total();
    }
    cout<<ans<<'\n';
}