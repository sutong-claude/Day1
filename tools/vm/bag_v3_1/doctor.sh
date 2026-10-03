#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
echo "bag doctor"
for cmd in g++ python3 timeout unzip zip; do
  if command -v "$cmd" >/dev/null; then echo "  OK $cmd -> $(command -v "$cmd")"; else echo "  MISSING $cmd"; exit 1; fi
done
if command -v codeblocks >/dev/null; then echo "  OK codeblocks -> $(command -v codeblocks)"; else echo "  WARN codeblocks not found (terminal workflow still works)"; fi
for t in T1 T2 T3 T4; do
  echo "-- $t"
  (cd "$ROOT/$t" && g++ main.cpp -std=c++17 -O2 -Wall -Wextra -o /tmp/bag_doctor_main)
  python3 - <<PY
import xml.etree.ElementTree as ET
p=ET.parse("$ROOT/$t/AC.cbp"); units=[u.attrib.get('filename') for u in p.getroot().find('Project').findall('Unit')]
assert units==['main.cpp'], units
print("  project XML/main.cpp: OK")
PY
done
echo "DOCTOR: OK"
echo "Deep environment test: cd T1 && bash selftest.sh"
