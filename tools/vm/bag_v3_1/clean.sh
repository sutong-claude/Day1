#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
for t in T1 T2 T3 T4; do
  [ -d "$ROOT/$t" ] || continue
  rm -rf "$ROOT/$t/.work" "$ROOT/$t/.check" "$ROOT/$t/bin" "$ROOT/$t/obj"
  echo "cleaned generated files in $t (sources/samples/failcases untouched)"
done
