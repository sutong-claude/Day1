#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
NAME="${1:-contest_$(date +%Y%m%d_%H%M%S)}"
OPEN="${2:-}"
if [[ "$NAME" = /* ]]; then DST="$NAME"; else DST="$HOME/Desktop/$NAME"; fi
[ ! -e "$DST" ] || { echo "already exists: $DST"; exit 1; }
mkdir -p "$DST"
for t in T1 T2 T3 T4; do cp -a "$ROOT/template/T" "$DST/$t"; done
cp -a "$ROOT/README.txt" "$DST/README.txt"
echo "created: $DST"
echo "open: $DST/T1/AC.cbp"
if [ "$OPEN" = "--open" ]; then
    if command -v codeblocks >/dev/null 2>&1; then
        codeblocks "$DST/T1/AC.cbp" >/dev/null 2>&1 &
        echo "Code::Blocks launched."
    else
        echo "WARN: codeblocks not found; workspace is ready."
    fi
fi
