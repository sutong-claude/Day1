#include <bits/stdc++.h>
using namespace std;
int fast(vector<long long>a){sort(a.begin(),a.end());long long s=0;int ans=0;for(int t=1;t<=(int)a.size();++t){s+=a[t-1];long long q=s/t;auto it=upper_bound(a.begin(),a.begin()+t,q);ans=max(ans,(int)(a.begin()+t-it));}return ans;}
int brute(const vector<long long>&a){int n=a.size(),ans=0;for(int m=1;m<(1<<n);++m){long long s=0;int k=0;for(int i=0;i<n;++i)if(m>>i&1){s+=a[i];++k;}int c=0;for(int i=0;i<n;++i)if((m>>i&1)&&a[i]*k>s)++c;ans=max(ans,c);}return ans;}
int main(){uint64_t cnt=0;for(int n=1;n<=7;++n){long long tot=1;for(int i=0;i<n;++i)tot*=4;for(long long code=0;code<tot;++code){long long x=code;vector<long long>a(n);for(int i=0;i<n;++i){a[i]=1+x%4;x/=4;}int f=fast(a),b=brute(a);++cnt;if(f!=b){cerr<<"FAIL exhaustive n="<<n<<" code="<<code<<" f="<<f<<" b="<<b<<"\n";return 1;}}}
mt19937_64 rng(123456789);for(int tc=0;tc<1000000;++tc){int n=1+rng()%10;vector<long long>a(n);for(auto&x:a)x=1+rng()%30;int f=fast(a),b=brute(a);++cnt;if(f!=b){cerr<<"FAIL random tc="<<tc<<" f="<<f<<" b="<<b<<"\n";for(auto x:a)cerr<<x<<' ';cerr<<'\n';return 1;}}
cout<<"PASS "<<cnt<<" cases\n";
}