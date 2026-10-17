#include <bits/stdc++.h>
using namespace std;
// INTENTIONAL PARTIAL SOLUTION. Large-value branch returns only a provable
// upper bound k, NOT necessarily the exact answer. NEVER CLAIM FULL AC.
const int INF=100000000;
int solve(const vector<int>&a){
 int n=a.size(),mx=a.back(),V=mx+1;
 if(is_sorted(a.begin(),a.end()))return 0; // Zero ops for already nondecreasing data.
 int blocks=1,req[30];fill(req,req+30,-1);
 for(int i=1;i<n;i++){
  unsigned v=a[i-1]^a[i];
  if(v){
   int j=31-__builtin_clz(v),t=(a[i-1]>>j)&1;
   if(req[j]>=0&&req[j]!=t){blocks++;fill(req,req+30,-1);}
   else req[j]=t;
  }
 }
 if(V>4096||1LL*n*V>70000000LL)return blocks; // NOT EXACT.
 vector<int>cur(V,INF),old(V),suf(V+1);cur[mx]=0;
 for(int i=n-2;i>=0;i--){
  suf[V]=INF;
  for(int x=V-1;x>=0;x--)suf[x]=min(suf[x+1],cur[x]);
  int diff=a[i]^a[i+1];
  for(int x=0;x<V;x++){
   int v=x^diff;
   int no=(v>=x&&v<V)?cur[v]:INF;
   old[x]=min(no,suf[x]+1);
  }
  swap(old,cur);
 }
 return min(blocks,*min_element(cur.begin(),cur.end()));
}
int main(){
 ios::sync_with_stdio(false);cin.tie(nullptr);
 int c,t;cin>>c>>t;
 while(t--){int n;cin>>n;vector<int>a(n);for(int &x:a)cin>>x;cout<<solve(a)<<'\n';}
}
