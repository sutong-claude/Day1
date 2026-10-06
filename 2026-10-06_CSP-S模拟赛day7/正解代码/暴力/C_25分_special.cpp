// Day7 C：只用于子任务 2 + 3（共 25 分性质），不是满分代码。
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
const int MOD=998244353;

long long qpow(long long a, unsigned long long e){
    long long r=1;
    while(e){
        if(e&1) r=r*a%MOD;
        a=a*a%MOD;
        e>>=1;
    }
    return r;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    freopen("Sucrose.in","r",stdin);
    freopen("Sucrose.out","w",stdout);

    int T;
    cin>>T;
    const long long inv100=qpow(100,MOD-2);
    const long long inv2=(MOD+1)/2;

    while(T--){
        unsigned long long r,L,R;
        int v;
        cin>>r>>L>>R>>v;

        if(v==50){
            cout<<qpow(inv2,r)<<'\n';
            continue;
        }

        long long p=1LL*v*inv100%MOD;
        long long q=1LL*(100-v)*inv100%MOD;

        if(L==R && L==1){
            cout<<qpow(p,r)<<'\n';
            continue;
        }

        // r<=60，所以 2^r 可安全放入 unsigned long long。
        if(L==R && L==(1ULL<<r)){
            cout<<qpow(q,r)<<'\n';
            continue;
        }

        // 其他数据不属于这份 partial 的保证范围。
        cout<<0<<'\n';
    }
    return 0;
}
