#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, re, resource, shutil, subprocess, time, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent; WORK=HERE/".work"; WORK.mkdir(exist_ok=True); FAIL=HERE/"failcase"; FAIL.mkdir(exist_ok=True)

def cmdrun(cmd,**kw):return subprocess.run(cmd,**kw)

def compile_all():
    for name in ["main_exact","main","ac","gen"]:(WORK/name).unlink(missing_ok=True)
    p=cmdrun(["g++","main.cpp","-std=c++17","-O2","-Wall","-Wextra","-o",str(WORK/"main_exact")],cwd=HERE)
    if p.returncode:raise SystemExit("COMPILE FAIL: main.cpp")
    text=(HERE/"main.cpp").read_text(encoding="utf-8",errors="replace").splitlines(True);pat=re.compile(r'(?:std::)?freopen\s*\([^;]*\)\s*;');out=[]
    for line in text:out.append(line if line.lstrip().startswith("//") else pat.sub("/* [stress disabled freopen] */",line))
    src=WORK/"main_stress.cpp";src.write_text("".join(out),encoding="utf-8")
    for source,name in [(src,"main"),(HERE/"AC.cpp","ac"),(HERE/"gen.cpp","gen")]:
        p=cmdrun(["g++",str(source),"-std=c++17","-O2","-Wall","-Wextra","-o",str(WORK/name)],cwd=HERE)
        if p.returncode:raise SystemExit(f"COMPILE FAIL: {source.name}")

def save_failure(i,seed,inp,mo,ao,me,ae,kind):
    stamp=time.strftime("%Y%m%d_%H%M%S");d=FAIL/f"{stamp}_test{i}_seed{seed}_{kind}";k=1
    while d.exists():d=FAIL/f"{stamp}_test{i}_seed{seed}_{kind}_{k}";k+=1
    d.mkdir(parents=True);(d/"input.txt").write_bytes(inp);(d/"main.out").write_bytes(mo or b"");(d/"ac.out").write_bytes(ao or b"");(d/"main.err").write_bytes(me or b"");(d/"ac.err").write_bytes(ae or b"")
    for f in ["main.cpp","AC.cpp","gen.cpp"]:shutil.copy2(HERE/f,d/f)
    print(f"saved: {d.relative_to(HERE)}");return d

def limiter(memory_mb):
    if memory_mb<=0:return None
    lim=memory_mb*1024*1024
    def pre():resource.setrlimit(resource.RLIMIT_AS,(lim,lim))
    return pre

def run_one(exe,inp,timeout,env=None,memory_mb=0):
    try:return cmdrun([str(exe)],cwd=HERE,input=inp,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,env=env,preexec_fn=limiter(memory_mb))
    except subprocess.TimeoutExpired:return None

def main():
    ap=argparse.ArgumentParser();ap.add_argument("max",nargs="?",type=int,default=0,help="0 = until failure");ap.add_argument("--timeout",type=float,default=float(os.getenv("TIMEOUT","2")));ap.add_argument("--progress",type=int,default=int(os.getenv("PROGRESS","100")));ap.add_argument("--seed",type=int,default=int(os.getenv("SEED","123456789")));ap.add_argument("--memory-mb",type=int,default=0);ap.add_argument("--allow-empty-output",action="store_true");args=ap.parse_args()
    if hashlib.sha256((HERE/"main.cpp").read_bytes()).digest()==hashlib.sha256((HERE/"AC.cpp").read_bytes()).digest():print("WARN: main.cpp and AC.cpp are byte-identical; stress test is not independent.")
    compile_all();i=1;start=time.perf_counter()
    while args.max<=0 or i<=args.max:
        seed=args.seed+i;env=os.environ.copy();env["TEST_ID"]=str(i);env["SEED"]=str(seed)
        g=run_one(WORK/"gen",None,args.timeout,env,args.memory_mb)
        if g is None:print(f"GEN TLE on test {i} seed={seed}");return 2
        if g.returncode!=0:print(f"GEN RE({g.returncode}) on test {i} seed={seed}\n"+g.stderr.decode(errors="replace")[:2000]);return 2
        inp=g.stdout
        if not inp.strip():print(f"GEN EMPTY on test {i}. Write gen.cpp first; refusing fake green stress.");return 2
        a=run_one(WORK/"ac",inp,args.timeout,memory_mb=args.memory_mb)
        if a is None:save_failure(i,seed,inp,b"",b"",b"",b"","oracle_tle");print(f"ORACLE TLE on test {i} seed={seed}");return 3
        if a.returncode!=0:save_failure(i,seed,inp,b"",a.stdout,b"",a.stderr,"oracle_re");print(f"ORACLE RE({a.returncode}) on test {i} seed={seed}");return 3
        m=run_one(WORK/"main",inp,args.timeout,memory_mb=args.memory_mb)
        if m is None:save_failure(i,seed,inp,b"",a.stdout,b"",a.stderr,"main_tle");print(f"MAIN TLE on test {i} seed={seed}");return 4
        if m.returncode!=0:save_failure(i,seed,inp,m.stdout,a.stdout,m.stderr,a.stderr,"main_re");print(f"MAIN RE({m.returncode}) on test {i} seed={seed}");return 4
        if i==1 and not args.allow_empty_output and not m.stdout.strip() and not a.stdout.strip():print("BOTH OUTPUTS EMPTY on test 1. Candidate/oracle are probably unfinished; refusing fake green stress. Use --allow-empty-output only if intentional.");return 2
        if m.stdout.split()!=a.stdout.split():save_failure(i,seed,inp,m.stdout,a.stdout,m.stderr,a.stderr,"wa");print(f"WA on test {i} seed={seed}\nINPUT:\n"+inp.decode(errors="replace"));return 1
        if args.progress>0 and i%args.progress==0:
            dt=time.perf_counter()-start;print(f"OK {i} tests {dt:.2f}s ({i/dt:.1f} tests/s)",flush=True)
        i+=1
    dt=time.perf_counter()-start;print(f"PASS: {args.max} tests in {dt:.2f}s ({args.max/dt:.1f} tests/s)");return 0
if __name__=="__main__":raise SystemExit(main())
