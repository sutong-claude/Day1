#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<long long>a(n);
    for(auto &x:a) cin>>x;
    sort(a.begin(),a.end());
    long long sum=0; int ans=0;
    for(int t=1;t<=n;t++){
        sum+=a[t-1];
        long long q=sum/t; // x > average iff integer x > floor(sum/t)
        int pos=upper_bound(a.begin(),a.begin()+t,q)-a.begin();
        ans=max(ans,t-pos);
    }
    cout<<ans<<'\n';
}