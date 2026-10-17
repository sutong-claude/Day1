#!/usr/bin/env python3
# Standalone independent bounded-value oracle for rain hybrid candidate.
# Usage: g++ -O2 -std=c++14 rain_hybrid_738of794_NOT_FULL.cpp -o /tmp/rain
#        python3 verify_rain_hybrid.py /tmp/rain
import itertools, random, subprocess, sys
BIN=sys.argv[1]
INF=10**7
def exact_bounded(a):
    V=a[-1]+1
    f=[INF]*V;f[a[-1]]=0
    for i in range(len(a)-2,-1,-1):
        d=a[i]^a[i+1];suffix=INF;g=[INF]*V
        for v in range(V-1,-1,-1):
            suffix=min(suffix,f[v])
            g[v]=1+suffix
        for v in range(V):
            w=v^d
            if v<=w<V:g[v]=min(g[v],f[w])
        f=g
    return min(f)
def k_bound(a):
    seen={};k=1
    for x,y in zip(a,a[1:]):
        d=x^y
        if not d:continue
        bit=d.bit_length()-1;want=(x>>bit)&1
        if bit in seen and seen[bit]!=want:
            k+=1;seen={}
        else:seen[bit]=want
    return k
def oracle(a):
    return min(exact_bounded(a),k_bound(a))
def run_batch(cases):
    inp="0 "+str(len(cases))+"\n"+"".join(
        str(len(a))+"\n"+" ".join(map(str,a))+"\n" for a in cases)
    cp=subprocess.run([BIN],input=inp,text=True,capture_output=True,check=True,timeout=30)
    return list(map(int,cp.stdout.split()))
random.seed(20261017)
cases=[]
for n in range(1,9):
    for _ in range(320):cases.append(tuple(random.randrange(16) for __ in range(n)))
for n in (9,10,12,17,18,25):
    for _ in range(100):cases.append(tuple(random.randrange(32) for __ in range(n)))
for n in (30,60):
    for _ in range(40):cases.append(tuple(random.randrange(12) for __ in range(n)))
outputs=run_batch(cases)
assert len(outputs)==len(cases)
for a,got in zip(cases,outputs):
    want=oracle(a)
    if got!=want:raise AssertionError((a,got,want))
print("PASS 3240 seeded random cases")
count=0
for n in range(1,8):
    cases=list(itertools.product(range(3),repeat=n))
    outs=run_batch(cases)
    for a,got in zip(cases,outs):
        want=oracle(a)
        if got!=want:raise AssertionError((a,got,want))
    count+=len(cases)
print("PASS",count,"exhaustive ternary cases")
