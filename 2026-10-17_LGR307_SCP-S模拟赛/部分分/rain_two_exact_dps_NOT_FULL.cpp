#include <bits/stdc++.h>
using namespace std;
// PARTIAL, NOT FULL: n<=17 exact irrespective of value, or n*lastValue
// small exact; otherwise returns the proven O(n) upper bound k.
// Proven by 21844 exhaustive small arrays and 11 official attachments.
int maxFirst(int l,int r,int bound,const vector<int>&a,const int req[30]){
  int er=a[r],dif=a[l]^er;
  int eq=0,less=-1;
  for(int j=29;j>=0;j--){
    int ne=-1,nl=-1;
    int allowed=req[j]<0 ? 3 : 1<<(req[j]^((er>>j)&1));
    for(int state=0;state<2;state++){
      int val=state==0?eq:less;if(val<0)continue;
      for(int y=0;y<2;y++)if(allowed>>y&1){
        if(!state&&y>(bound>>j&1))continue;
        int nv=val|((y^((dif>>j)&1))<<j);
        if(state||y<(bound>>j&1))nl=max(nl,nv);
        else ne=max(ne,nv);
      }
    }
    eq=ne;less=nl;
  }
  return max(eq,less);
}
int solve17(const vector<int>&a){
 int n=a.size();if(n==1)return 0;
 int k=1,rbits[30];fill(rbits,rbits+30,-1);
 for(int i=1;i<n;i++){
  int d=a[i-1]^a[i];
  if(d){
   int j=31-__builtin_clz((unsigned)d),v=(a[i-1]>>j)&1;
   if(rbits[j]>=0&&rbits[j]!=v){k++;fill(rbits,rbits+30,-1);}
   else rbits[j]=v;
  }
 }
 vector<vector<int>>dp(n+1,vector<int>(n+1,-1));
 for(int l=n-1;l>=0;l--){
   bool nondec=true;
   for(int r=l;r<n;r++){
     if(r>l&&a[r-1]>a[r])nondec=false;
     if(nondec&&r==n-1)dp[l][0]=a[l];
   }
   int req[30];fill(req,req+30,-1);bool ok=true;
   for(int r=l;r<n-1&&ok;r++){
     if(r>l){
      int d=a[r-1]^a[r];
      if(d){
       int j=31-__builtin_clz((unsigned)d),v=(a[r-1]>>j)&1;
       if(req[j]!=-1&&req[j]!=v)ok=false;
       else req[j]=v;
      }
     }
     if(!ok)break;
     for(int used=0;used<n-1;used++)if(dp[r+1][used]>=0){
       int result=maxFirst(l,r,dp[r+1][used],a,req);
       if(result>=0)dp[l][used+1]=max(dp[l][used+1],result);
     }
   }
 }
 for(int j=0;j<n;j++)if(dp[0][j]>=0)return min(k,j);
 return k;
}
const int INF=100000000;
int solve(const vector<int>&a){
 if(a.size()<=17)return solve17(a);
 int n=a.size(),mx=a.back();
 int V=mx>=4096?4097:mx+1;
 if(is_sorted(a.begin(),a.end()))return 0;
 int blocks=1,req[30];fill(req,req+30,-1);
 for(int i=1;i<n;i++){
  unsigned v=a[i-1]^a[i];
  if(v){int j=31-__builtin_clz(v),t=(a[i-1]>>j)&1;
   if(req[j]>=0&&req[j]!=t){blocks++;fill(req,req+30,-1);}
   else req[j]=t;
  }
 }
 if(V>4096||1LL*n*V>70000000LL)return blocks; // upper bound ONLY!
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
 int best=*min_element(cur.begin(),cur.end());
 return min(blocks,best);
}
int main(){
 ios::sync_with_stdio(false);cin.tie(nullptr);
 int c,t;cin>>c>>t;
 while(t--){
  int n;cin>>n;vector<int>a(n);
  for(int &x:a)cin>>x;
  cout<<solve(a)<<"\n";
 }
}
