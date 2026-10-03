#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
STAMP="$(date +%Y%m%d_%H%M%S_%N)"
TARGET="${1:-all}"

restore_one() {
    local t="$1"
    [ -d "$ROOT/$t" ] || { echo "missing $t"; return 1; }
    mkdir -p "$ROOT/backups"
    local b="$ROOT/backups/${STAMP}_${t}"
    # Atomic/cheap on the same filesystem: preserve the WHOLE old task directory,
    # including samples/zips/failcases, without duplicating large sample data.
    mv "$ROOT/$t" "$b"
    if ! cp -a "$ROOT/template/T" "$ROOT/$t"; then
        echo "restore copy failed; rolling back $t" >&2
        rm -rf "$ROOT/$t"
        mv "$b" "$ROOT/$t"
        return 1
    fi
    echo "restored $t; complete old task preserved at: ${b#$ROOT/}"
}

case "$TARGET" in
    all) for t in T1 T2 T3 T4; do restore_one "$t"; done ;;
    T1|T2|T3|T4) restore_one "$TARGET" ;;
    *) echo "usage: bash restore.sh [all|T1|T2|T3|T4]"; exit 2 ;;
esac
