#include <bits/stdc++.h>
using namespace std;
// Addition in unsigned long long is exactly modulo 2^64.
int main(){
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n;cin>>n;vector<int>a(n);
    for(int &x:a)cin>>x;
    unsigned long long ans=0;
    int last[30]={};
    for(int r=1;r<=n;r++){
        unsigned x=a[r-1];
        while(x){int k=__builtin_ctz(x);last[k]=r;x&=x-1;}
        for(int k=0;k<30;k++)ans+=(1ULL<<k)*(unsigned long long)last[k];
    }
    // Only MEX=2^k can introduce a bit not already in OR.
    for(int k=0;(1LL<<k)<=n;k++){
        int need=1<<k,got=0,l=0,start=0,epoch=1;
        vector<int>freq(need),stamp(need);
        for(int r=0;r<n;r++){
            int x=a[r];
            if(x&need){++epoch;got=0;l=start=r+1;continue;}
            if(x<need){
                if(stamp[x]!=epoch){stamp[x]=epoch;freq[x]=0;}
                if(++freq[x]==1)++got;
            }
            while(got==need){
                int v=a[l++];
                if(v<need&&--freq[v]==0)--got;
            }
            ans+=(1ULL<<k)*(unsigned long long)(l-start);
        }
    }
    cout<<ans<<'\n';
}
