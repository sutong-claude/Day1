#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$ROOT/dist}"
rm -rf "$OUT"
mkdir -p "$OUT/bag"
for f in README.txt doctor.sh new_contest.sh restore.sh reset.sh clean.sh; do cp -a "$ROOT/$f" "$OUT/bag/$f"; done
mkdir -p "$OUT/bag/template"
cp -a "$ROOT/template/T" "$OUT/bag/template/T"
for t in T1 T2 T3 T4; do cp -a "$ROOT/template/T" "$OUT/bag/$t"; done
printf 'BAG_V3.1\nBuilt %s\n' "$(date -Is)" > "$OUT/bag/VERSION.txt"
(cd "$OUT" && zip -qr bag_v3_1.zip bag)
echo "release: $OUT/bag_v3_1.zip"
