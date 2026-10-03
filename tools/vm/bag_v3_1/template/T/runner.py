#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, os, re, shutil, subprocess, tempfile, time, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
WORK=HERE/".work"
WORK.mkdir(exist_ok=True)
SAMPLE_FAIL=HERE/"sample_fail"

BASE_FLAGS=["-std=c++17","-O2","-Wall","-Wextra"]
SAN_FLAGS=["-std=c++17","-O1","-g","-Wall","-Wextra","-fsanitize=address,undefined","-fno-omit-frame-pointer"]

def run(cmd, **kw): return subprocess.run(cmd, **kw)

def compile_cached(src:Path,out:Path,stamp:Path,flags:list[str]):
    data=src.read_bytes()+b"\0"+" ".join(flags).encode()
    h=hashlib.sha256(data).hexdigest()
    if out.exists() and stamp.exists() and stamp.read_text().strip()==h: return out
    out.unlink(missing_ok=True)
    p=run(["g++",str(src),*flags,"-o",str(out)],cwd=HERE)
    if p.returncode: raise SystemExit(f"COMPILE FAIL: {src.name}")
    stamp.write_text(h)
    return out

def make_test_source():
    src=(HERE/"main.cpp").read_text(encoding="utf-8",errors="replace").splitlines(True)
    out=[]; pat=re.compile(r'(?:std::)?freopen\s*\([^;]*\)\s*;')
    for line in src:
        out.append(line if line.lstrip().startswith("//") else pat.sub("/* [runner disabled freopen] */",line))
    p=WORK/"main_test.cpp"; p.write_text("".join(out),encoding="utf-8"); return p

def parse_freopen():
    text=(HERE/"main.cpp").read_text(encoding="utf-8",errors="replace")
    active=[]
    for line in text.splitlines():
        if line.lstrip().startswith("//"): continue
        for m in re.finditer(r'(?:std::)?freopen\s*\(\s*"([^"]+)"\s*,\s*"([^"]+)"',line):
            active.append((m.group(1),m.group(2),line.strip()))
    ins=[x[0] for x in active if "r" in x[1]]
    outs=[x[0] for x in active if any(c in x[1] for c in "wa")]
    return active,(ins[0] if ins else None),(outs[0] if outs else None)

def safe_extract(z:Path,d:Path):
    # Python already normalizes ../ on extraction, but explicitly reject absolute/traversal
    # paths so a contest archive can never escape .work/extracted.
    with zipfile.ZipFile(z) as f:
        for info in f.infolist():
            p=Path(info.filename)
            if p.is_absolute() or ".." in p.parts:
                raise ValueError(f"unsafe zip path: {info.filename}")
        f.extractall(d)

def extract_zips():
    exroot=WORK/"extracted"; exroot.mkdir(exist_ok=True)
    zips=[]
    for base in [HERE,HERE/"samples"]:
        if base.exists(): zips += list(base.glob("*.zip"))
    live=set()
    for z in sorted(set(zips)):
        # Add a short path hash so two zips with the same stem in T/ and samples/ never collide.
        tag=hashlib.sha1(str(z.resolve()).encode()).hexdigest()[:8]
        d=exroot/f"{z.stem}_{tag}"; live.add(d.name)
        stamp=d/".zipstamp"; sig=f"{z.stat().st_size}:{z.stat().st_mtime_ns}"
        if stamp.exists() and stamp.read_text(errors="ignore").strip()==sig: continue
        if d.exists(): shutil.rmtree(d)
        d.mkdir(parents=True,exist_ok=True)
        try:
            safe_extract(z,d); stamp.write_text(sig)
            print(f"[zip] {z.name} -> {d.relative_to(HERE)}")
        except Exception as e:
            print(f"[zip] FAIL {z.name}: {e}")
            shutil.rmtree(d,ignore_errors=True)
    for d in exroot.iterdir():
        if d.is_dir() and d.name not in live: shutil.rmtree(d)
    return exroot

def discover_inputs(exroot):
    roots=[HERE/"samples",exroot,HERE]; seen=set(); arr=[]
    ignored={".work","sample_fail","failcase","bin","obj",".check"}
    for r in roots:
        if not r.exists(): continue
        for p in r.rglob("*.in"):
            if r!=exroot and any(part in ignored for part in p.parts): continue
            rp=p.resolve()
            if rp in seen: continue
            seen.add(rp); arr.append(p)
    return sorted(arr,key=lambda p:str(p))

def expected_for(inp):
    # Prefer exact-case names; then accept common uppercase extensions.
    for ext in [".out",".ans",".answer",".OUT",".ANS",".ANSWER"]:
        p=inp.with_suffix(ext)
        if p.exists(): return p
    return None

def tokens(path:Path):
    with path.open("r",encoding="utf-8",errors="replace") as f:
        for line in f:
            yield from line.split()

def token_diff(a:Path,b:Path):
    ia,ib=tokens(a),tokens(b); idx=0
    while True:
        try: x=next(ia); ax=True
        except StopIteration: x=None; ax=False
        try: y=next(ib); by=True
        except StopIteration: y=None; by=False
        if not ax and not by: return None
        idx+=1
        if ax!=by or x!=y: return idx,x,y

def pretty(p:Path,exroot:Path):
    try:
        rel=p.resolve().relative_to(exroot.resolve())
        parts=rel.parts
        return f"zip:{parts[0]}::{'/'.join(parts[1:])}" if len(parts)>1 else f"zip:{rel}"
    except Exception: pass
    try: return str(p.resolve().relative_to(HERE.resolve()))
    except Exception: return str(p)

def save_sample_failure(inp,exp,got,err,kind):
    SAMPLE_FAIL.mkdir(exist_ok=True)
    stamp=time.strftime("%Y%m%d_%H%M%S")
    d=SAMPLE_FAIL/f"{stamp}_{kind}_{hashlib.sha1(str(inp).encode()).hexdigest()[:8]}"
    k=1
    while d.exists(): d=SAMPLE_FAIL/f"{stamp}_{kind}_{k}"; k+=1
    d.mkdir()
    shutil.copy2(inp,d/"input.in")
    if exp and exp.exists(): shutil.copy2(exp,d/"expected.out")
    if got.exists(): shutil.copy2(got,d/"got.out")
    if err.exists(): shutil.copy2(err,d/"stderr.txt")
    shutil.copy2(HERE/"main.cpp",d/"main.cpp")
    return d

def fileio_smoke(exe,inp,exp,timeout,mode):
    active,inname,outname=parse_freopen()
    if not active:return "NO_FREOPEN",None
    if not inname or not outname:return "BAD_FREOPEN",None
    with tempfile.TemporaryDirectory(prefix="bag_fileio_") as td0:
        td=Path(td0); inpath=td/inname; inpath.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(inp,inpath)
        (td/outname).parent.mkdir(parents=True,exist_ok=True)
        try:p=run([str(exe)],cwd=td,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=timeout)
        except subprocess.TimeoutExpired:return "TLE",None
        if p.returncode!=0:return f"RE({p.returncode})",None
        got=td/outname
        if not got.exists():return "NO_OUTPUT_FILE",None
        if mode=="tokens" and exp:
            d=token_diff(got,exp)
            if d:return "WA",d
        return "OK",None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--timeout",type=float,default=float(os.getenv("TIMEOUT","3")))
    ap.add_argument("--limit",type=int,default=0)
    ap.add_argument("--mode",choices=["tokens","none"],default=os.getenv("COMPARE","tokens"),help="none = run only, useful for SPJ/construction samples")
    ap.add_argument("--sanitize",action="store_true",help="ASan+UBSan sample run")
    args=ap.parse_args()
    flags=SAN_FLAGS if args.sanitize else BASE_FLAGS
    exact=compile_cached(HERE/"main.cpp",WORK/("main_exact_san" if args.sanitize else "main_exact"),WORK/("main_exact_san.sha" if args.sanitize else "main_exact.sha"),flags)
    active,_,_=parse_freopen()
    test=compile_cached(make_test_source(),WORK/("main_test_san" if args.sanitize else "main_test"),WORK/("main_test_san.sha" if args.sanitize else "main_test.sha"),flags) if active else exact
    exroot=extract_zips(); inputs=discover_inputs(exroot)
    if not inputs:
        print("NO SAMPLES: put *.in + matching *.out/.ans into samples/ or this folder, or drop a .zip here.")
        return 2
    if args.limit>0:inputs=inputs[:args.limit]
    got=WORK/"current.out"; err=WORK/"current.err"
    passed=failed=ran=run_only=0; first=None; t_all=time.perf_counter()
    for i,inp in enumerate(inputs,1):
        exp=expected_for(inp); label=pretty(inp,exroot); t=time.perf_counter(); got.unlink(missing_ok=True); err.unlink(missing_ok=True)
        try:
            with inp.open("rb") as fin,got.open("wb") as fout,err.open("wb") as ferr:
                p=run([str(test)],cwd=HERE,stdin=fin,stdout=fout,stderr=ferr,timeout=args.timeout)
            dt=time.perf_counter()-t
            if p.returncode!=0:
                d=save_sample_failure(inp,exp,got,err,"re")
                print(f"[{i:04d}] RE  {label} rc={p.returncode} {dt:.3f}s saved={d.relative_to(HERE)}");failed+=1;continue
        except subprocess.TimeoutExpired:
            dt=time.perf_counter()-t; d=save_sample_failure(inp,exp,got,err,"tle")
            print(f"[{i:04d}] TLE {label} >{args.timeout:.2f}s saved={d.relative_to(HERE)}");failed+=1;continue
        ran+=1
        if first is None:first=(inp,exp)
        if args.mode=="none" or not exp:
            run_only+=1
            keep=WORK/f"run_output_{i}.txt"; shutil.copy2(got,keep)
            why="compare disabled" if args.mode=="none" else "no expected output"
            print(f"[{i:04d}] RUN {label} {why} {dt:.3f}s -> {keep.name}")
        else:
            d=token_diff(got,exp)
            if d:
                idx,x,y=d; saved=save_sample_failure(inp,exp,got,err,"wa")
                print(f"[{i:04d}] WA  {label} token#{idx}: got={x!r} expected={y!r} {dt:.3f}s saved={saved.relative_to(HERE)}");failed+=1
            else:
                print(f"[{i:04d}] OK  {label} {dt:.3f}s");passed+=1
                got.unlink(missing_ok=True); err.unlink(missing_ok=True)
    total=time.perf_counter()-t_all
    print(f"SUMMARY: pass={passed} fail={failed} run_only={run_only} samples={len(inputs)} wall={total:.3f}s mode={args.mode}{' sanitize' if args.sanitize else ''}")
    if active and first:
        st,detail=fileio_smoke(exact,first[0],first[1],args.timeout,args.mode)
        print("FILEIO:",st,"" if detail is None else str(detail))
        if st!="OK":failed+=1
    elif active:print("FILEIO: active freopen detected, but no runnable sample was available.")
    else:print("FILEIO: no active freopen (stdin/stdout mode).")
    return 0 if failed==0 else 1
if __name__=="__main__":raise SystemExit(main())
