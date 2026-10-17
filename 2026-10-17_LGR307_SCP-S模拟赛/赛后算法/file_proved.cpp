#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,m; if(!(cin>>n>>m)) return 0;
    vector<int> a(n); vector<long long> cnt(m);
    for(int &x:a) cin>>x;
    sort(a.begin(),a.end());
    for(int i=0;i<m;i++){
        int len;cin>>len;
        while(len--){
            int x;cin>>x;
            cnt[i]+=n-(lower_bound(a.begin(),a.end(),x)-a.begin());
        }
    }
    sort(cnt.begin(),cnt.end());
    long long ans=1LL*m*n*(n+1)/2;
    for(int i=0;i<m;i++) ans+=cnt[i]*(m-i);
    cout<<ans<<'\n';
}
