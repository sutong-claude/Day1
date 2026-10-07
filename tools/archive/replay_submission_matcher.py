#!/usr/bin/env python3
"""
Match official/OJ submitted source files back to Replay v3 file_changes snapshots.

Why:
- VM final workspace can differ from the file actually submitted.
- file_changes preserves observed saved states, but filenames alone do not tell
  which one was uploaded.
- Exact normalized source matching gives a strong bridge:
      OJ record source -> one/more Replay snapshots -> capture-relative time.

Usage:
  python replay_submission_matcher.py \
      --file-changes file_changes.jsonl \
      --source "A=record_A.cpp" \
      --source "B=record_B.cpp"

Optional:
  --path-hint "A=T1/main.cpp" --path-hint "B=T2/main.cpp"
  --start-iso 2026-10-05T10:11:01
  --json

The script does not infer a submission when there is no exact content match.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional


def normalize_source(text: str) -> str:
    """Normalize only newline representation and terminal newlines.

    Deliberately do NOT strip internal whitespace/comments: an exact source
    identity claim should remain conservative.
    """
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")


def normalized_sha256(text: str) -> str:
    return hashlib.sha256(normalize_source(text).encode("utf-8")).hexdigest()


@dataclass
class Snapshot:
    seq: int
    t: float
    path: str
    size: int
    event_sha256: str
    normalized_sha256: str
    content: str


@dataclass
class Match:
    label: str
    source_path: str
    replay_seq: int
    replay_path: str
    t: float
    wall_clock: Optional[str]
    size: int
    event_sha256: str
    normalized_sha256: str


def load_snapshots(path: Path) -> List[Snapshot]:
    out: List[Snapshot] = []
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            if not raw.strip():
                continue
            obj = json.loads(raw)
            content = obj.get("content")
            if not isinstance(content, str):
                continue
            out.append(
                Snapshot(
                    seq=len(out) + 1,
                    t=float(obj.get("t", 0.0)),
                    path=str(obj.get("path", "")),
                    size=int(obj.get("bytes", len(content.encode("utf-8")))),
                    event_sha256=str(obj.get("sha256", "")),
                    normalized_sha256=normalized_sha256(content),
                    content=content,
                )
            )
    return out


def parse_kv(items: Iterable[str], flag: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"{flag} expects LABEL=VALUE, got: {item!r}")
        k, v = item.split("=", 1)
        k, v = k.strip(), v.strip()
        if not k or not v:
            raise SystemExit(f"{flag} expects non-empty LABEL=VALUE: {item!r}")
        result[k] = v
    return result


def wall_clock(start_iso: Optional[str], t: float) -> Optional[str]:
    if not start_iso:
        return None
    start = datetime.fromisoformat(start_iso)
    return (start + timedelta(seconds=t)).isoformat(timespec="seconds")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file-changes", required=True, type=Path)
    ap.add_argument(
        "--source",
        action="append",
        default=[],
        metavar="LABEL=FILE",
        help="Official/OJ source to locate. Repeatable.",
    )
    ap.add_argument(
        "--path-hint",
        action="append",
        default=[],
        metavar="LABEL=REPLAY_PATH",
        help="Optional exact file_changes path filter for a label.",
    )
    ap.add_argument(
        "--start-iso",
        help="Capture start ISO datetime; only used to print derived wall clock.",
    )
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    sources = parse_kv(args.source, "--source")
    hints = parse_kv(args.path_hint, "--path-hint")
    if not sources:
        ap.error("at least one --source LABEL=FILE is required")

    snapshots = load_snapshots(args.file_changes)
    all_results = []

    for label, source_file in sources.items():
        source_path = Path(source_file)
        source_text = source_path.read_text(encoding="utf-8")
        target = normalized_sha256(source_text)
        hint = hints.get(label)

        candidates = [
            s for s in snapshots
            if s.normalized_sha256 == target and (hint is None or s.path == hint)
        ]

        matches = [
            Match(
                label=label,
                source_path=str(source_path),
                replay_seq=s.seq,
                replay_path=s.path,
                t=s.t,
                wall_clock=wall_clock(args.start_iso, s.t),
                size=s.size,
                event_sha256=s.event_sha256,
                normalized_sha256=s.normalized_sha256,
            )
            for s in candidates
        ]

        all_results.append(
            {
                "label": label,
                "source": str(source_path),
                "source_normalized_sha256": target,
                "path_hint": hint,
                "match_count": len(matches),
                "matches": [asdict(m) for m in matches],
            }
        )

    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    else:
        for item in all_results:
            print(
                f"[{item['label']}] {item['source']} "
                f"matches={item['match_count']}"
            )
            if not item["matches"]:
                print("  NO EXACT MATCH")
                continue
            for m in item["matches"]:
                clock = f" wall={m['wall_clock']}" if m["wall_clock"] else ""
                print(
                    f"  seq={m['replay_seq']} t={m['t']:.3f}{clock} "
                    f"path={m['replay_path']} bytes={m['size']} "
                    f"sha={m['event_sha256'][:12]}"
                )

    # Non-zero is useful in automation: any unmatched source means the bridge
    # is incomplete and should not silently be treated as identified.
    return 0 if all(x["match_count"] > 0 for x in all_results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
