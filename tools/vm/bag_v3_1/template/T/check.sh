#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "== compile exact main.cpp =="
rm -rf .check; mkdir .check
g++ main.cpp -std=c++17 -O2 -Wall -Wextra -o .check/main
echo "COMPILE: OK"
echo
echo "== active freopen =="
python3 - <<'PY'
from pathlib import Path
import re
s=Path("main.cpp").read_text(encoding="utf-8",errors="replace").splitlines();a=[]
for n,line in enumerate(s,1):
    if line.lstrip().startswith("//"):continue
    if re.search(r'(?:std::)?freopen\s*\(',line):a.append((n,line.strip()))
if not a:print("none (stdin/stdout mode)")
else:
    for n,x in a:print(f"line {n}: {x}")
PY
echo
echo "== samples =="
if bash run.sh; then echo "CHECK: GREEN"; else echo "CHECK: RED"; exit 1; fi
