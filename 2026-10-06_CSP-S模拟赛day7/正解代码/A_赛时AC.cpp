#include <bits/stdc++.h>
using namespace std;
#define int long long
int n;
int f[1000010];
int a[1000010];
priority_queue<int> p1[1000010];
priority_queue<int, vector<int>, greater<int>> p2[1000010];
int ans1=0, ans2=0;
signed main(){
    ios::sync_with_stdio(false);
    cin.tie(0); cout.tie(0);
    freopen("Genshin.in","r",stdin);
    freopen("Genshin.out","w",stdout);
    cin>>n;
    for(int i=2;i<=n;i++) cin>>f[i];
    for(int i=1;i<=n;i++) cin>>a[i];
    for(int i=2;i<=n;i++) if(a[i]>0) p1[f[i]].push(a[i]);
    if(a[1]>0) ans1+=a[1];
    int ma=0;
    for(int i=1;i<=n;i++){
        if(p1[i].empty()) continue;
        if(p1[i].size()==1) ans1+=p1[i].top();
        else{
            int x=p1[i].top(); p1[i].pop();
            int y=p1[i].top();
            ans1+=x;
            ma=max(ma,y);
        }
    }
    ans1+=ma;
    cout<<ans1<<' ';
    for(int i=2;i<=n;i++) if(a[i]<0) p2[f[i]].push(a[i]);
    if(a[1]<0) ans2+=a[1];
    int mi=0;
    for(int i=1;i<=n;i++){
        if(p2[i].empty()) continue;
        if(p2[i].size()==1) ans2+=p2[i].top();
        else{
            int x=p2[i].top(); p2[i].pop();
            int y=p2[i].top();
            ans2+=x;
            mi=min(mi,y);
        }
    }
    ans2+=mi;
    cout<<ans2<<'\n';
}
