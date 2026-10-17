#include <bits/stdc++.h>
using namespace std;
struct FastInput{
 static constexpr int SZ=1<<18;char buf[SZ];int at=0,sz=0;
 inline char gc(){if(at==sz){sz=fread(buf,1,SZ,stdin);at=0;if(!sz)return 0;}return buf[at++];}
 inline int next(){int x=0;char c=gc();while(c<=32)c=gc();while(c>32){x=x*10+c-'0';c=gc();}return x;}
};
struct Frame{int u,phase,h;long long extra;vector<pair<int,long long>>old;};
int main(){
 FastInput in;int tc=in.next(),T=in.next();(void)tc;
 while(T--){
  int n=in.next(),m=in.next();
  vector<int>head(n+1,-1),to(2*m),nxt(2*m);
  int ec=0;
  auto add=[&](int u,int v){to[ec]=v;nxt[ec]=head[u];head[u]=ec++;};
  for(int i=0;i<m;i++){int u=in.next(),v=in.next();add(u,v);add(v,u);}
  vector<int>par(n+1),dep(n+1),it=head,col(n+1),cyroot(n+1),ht(n+1);
  vector<pair<int,int>>back;back.reserve(m-n+1);
  vector<int>ds;ds.reserve(n);ds.push_back(1);col[1]=1;
  while(!ds.empty()){
   int u=ds.back(),&e=it[u];
   if(e==-1){col[u]=2;ds.pop_back();continue;}
   int v=to[e];e=nxt[e];
   if(v==par[u])continue;
   if(!col[v]){par[v]=u;dep[v]=dep[u]+1;col[v]=1;ds.push_back(v);}
   else if(col[v]==1&&dep[v]<dep[u])back.push_back(make_pair(v,u));
  }
  vector<int>seq;
  for(const auto &uv:back){
   int u=uv.first,v=uv.second;
   seq.clear();for(int x=v;x!=u;x=par[x])seq.push_back(x);
   int L=(int)seq.size()+1;
   bool dfsFirst=seq.back()<seq.front();
   for(int q=0;q<(int)seq.size();q++){
    int x=seq[q];cyroot[x]=u;
    int i=dfsFirst?L-1-q:q+1;
    if(i<L-1&&2*i>L)ht[x]=2*i-L;
   }
  }
  vector<int>first(n+1),sib(n+1);
  for(int v=2;v<=n;v++){
   int u=cyroot[v]?cyroot[v]:par[v];
   sib[v]=first[u];first[u]=v;
  }
  map<int,long long>gaps;long long cnt=0,answer=0;
  vector<Frame>st;st.reserve(n);st.push_back({1,0,0,0,{}});
  while(!st.empty()){
   Frame &f=st.back();
   if(f.phase==0){
    if((f.h=ht[f.u])>0){
     auto it=gaps.upper_bound(f.h);
     while(it!=gaps.end()){f.old.push_back(*it);it=gaps.erase(it);}
     f.extra=1;
     for(const auto &dc:f.old){int d=dc.first;long long c=dc.second;gaps[d-f.h]+=c;f.extra+=c;}
     gaps[f.h]+=f.extra;cnt+=f.extra;
    }
    answer+=cnt+1;
    f.phase=first[f.u]?first[f.u]:-1;
   }else if(f.phase>0){
    int v=f.phase;f.phase=sib[v]?sib[v]:-1;
    st.push_back({v,0,0,0,{}});
   }else{
    if(f.h>0){
     auto eraseCount=[&](int d,long long c){
      auto it=gaps.find(d);it->second-=c;if(it->second==0)gaps.erase(it);
     };
     eraseCount(f.h,f.extra);
     for(const auto &dc:f.old)eraseCount(dc.first-f.h,dc.second);
     for(const auto &dc:f.old)gaps[dc.first]+=dc.second;
     cnt-=f.extra;
    }
    st.pop_back();
   }
  }
  printf("%lld\n",answer);
 }
}
