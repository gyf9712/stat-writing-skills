"""
cache_queue_lint.py — verification-WIP gate for the literature cache and the
project citation lock manifest.

Two jobs, both mechanical:

1. GATE (default): read a project's cited_results.lock.md and hard-fail any
   high-stakes row (purpose in {load_bearing, benchmark_claim, comparative})
   whose recorded verification level is below the floor. This enforces the
   existing GAP rule of cited-results-lock-protocol.md at the places a paper
   actually passes through (stat-paper-write pre-review and final checklist,
   proofcheck convergence, stat-mock-review submission readiness). Global
   inbox backlog is reported as WARN only — a cap with no gate attached is
   decoration, but a global block would let unrelated backlog stop a paper.

2. QUEUE (--list-queue): print the inbox promotion queue for /lit-cache
   verify, ordered by: current-project blockers first (inbox bibkey matches a
   below-floor lock row), then canonical-role entries (role_in_literature in
   CANONICAL_ROLES — local metadata, never an external taxonomy), then age
   (oldest first).

The false-authority boundary applies: the script checks recorded states
against a recorded floor. It never judges whether a verification was done
well, and it never performs promotion itself.

Exit codes
----------
    0 : no gate breach (warnings allowed)
    1 : at least one below-floor high-stakes row in the lock manifest
    2 : invocation or runtime error

Usage
-----
    python cache_queue_lint.py --lock papers/<project>/cited_results.lock.md
    python cache_queue_lint.py --lock ... --require-signed   # floor = human_signed
    python cache_queue_lint.py --list-queue                  # promotion queue only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cache_queue_lint_rules as rules  # noqa: E402

SCRIPT_VERSION = "1.0.0"

_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
_BIBKEY_RE = re.compile(r"paper:([\w.-]+)#")
_ROLE_RE = re.compile(r"^role_in_literature:\s*(\S+)", re.M)


@dataclass
class Finding:
    id: str
    status: str        # FAIL | WARN | INFO
    message: str
    evidence: dict = field(default_factory=dict)


def state_rank(state: str) -> int:
    """Rank of a verification state; unknown/empty states rank below all."""
    s = state.strip().strip("`")
    return rules.STATE_ORDER.index(s) if s in rules.STATE_ORDER else -1


def parse_lock_rows(text: str) -> list[dict]:
    """Extract rows from the 10-column lock manifest table (marker column
    'Citation site'). Returns dicts with site, reference, purpose, level."""
    rows, in_table = [], False
    for line in text.splitlines():
        m = _ROW_RE.match(line.strip())
        if not m:
            in_table = False
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if all(set(c) <= {"-", ":", " "} and c for c in cells):
            continue
        if cells and cells[0] == "Citation site":
            in_table = True
            continue
        if in_table and len(cells) >= 8:
            rows.append({
                "site": cells[0].strip("`"),
                "reference": cells[1].strip("`"),
                "purpose": cells[2].strip("`"),
                "level": cells[7].strip("`"),
            })
    return rows


def check_lock(lock_path: Path, floor: str) -> list[Finding]:
    findings = []
    rows = parse_lock_rows(lock_path.read_text(encoding="utf-8", errors="replace"))
    if not rows:
        findings.append(Finding(
            "empty_lock_manifest", "WARN",
            f"No manifest rows parsed from {lock_path}. If the project has "
            f"citations, the lock manifest has not been initialized "
            f"(stat-paper-plan Step 5.7).", {"lock": str(lock_path)}))
        return findings
    floor_rank = state_rank(floor)
    for r in rows:
        if r["purpose"] not in rules.HIGH_STAKES_PURPOSES:
            continue
        if state_rank(r["level"]) < floor_rank:
            findings.append(Finding(
                "below_floor_high_stakes_row", "FAIL",
                f"Lock row '{r['site']}' ({r['reference']}) has purpose "
                f"'{r['purpose']}' at level '{r['level']}', below the required "
                f"floor '{floor}'. Verify (promote the cache entry), downgrade "
                f"the claim, or remove the citation site.",
                {"site": r["site"], "reference": r["reference"],
                 "purpose": r["purpose"], "level": r["level"], "floor": floor}))
    return findings


def scan_inbox(cache_root: Path) -> tuple[list[dict], list[Finding]]:
    findings = []
    inbox = cache_root / "inbox"
    if not inbox.is_dir():
        findings.append(Finding(
            "no_inbox", "INFO",
            f"No inbox at {inbox}; global backlog is zero.", {}))
        return [], findings
    entries = []
    now = time.time()
    for p in sorted(inbox.glob("*.md")):
        if not (p.name.endswith(".draft.md") or p.name.endswith(".update.md")):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        role_m = _ROLE_RE.search(text)
        entries.append({
            "file": p.name,
            "bibkey": p.name.split(".")[0],
            "role": role_m.group(1).strip("`") if role_m else None,
            "age_days": round((now - p.stat().st_mtime) / 86400, 1),
        })
    if len(entries) > rules.INBOX_WARN_COUNT:
        findings.append(Finding(
            "inbox_backlog_count", "WARN",
            f"Inbox holds {len(entries)} pending entries "
            f"(> {rules.INBOX_WARN_COUNT}). Run /lit-cache verify.",
            {"count": len(entries)}))
    oldest = max((e["age_days"] for e in entries), default=0)
    if oldest > rules.INBOX_WARN_AGE_DAYS:
        findings.append(Finding(
            "inbox_backlog_age", "WARN",
            f"Oldest inbox entry is {oldest} days old "
            f"(> {rules.INBOX_WARN_AGE_DAYS}). Run /lit-cache verify.",
            {"oldest_days": oldest}))
    return entries, findings


def promotion_queue(entries: list[dict], blocking_bibkeys: set[str]) -> list[dict]:
    """Order: current-project blockers > canonical roles > age (oldest first)."""
    def key(e):
        return (
            0 if e["bibkey"] in blocking_bibkeys else 1,
            0 if e["role"] in rules.CANONICAL_ROLES else 1,
            -e["age_days"],
        )
    return [dict(e, blocking=e["bibkey"] in blocking_bibkeys) for e in sorted(entries, key=key)]


def compute_rules_digest() -> str:
    p = HERE / "cache_queue_lint_rules.py"
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else "unknown"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Verification-WIP gate: lock-manifest floor check + inbox backlog scan.")
    p.add_argument("--lock", default=None,
                   help="Path to the project's cited_results.lock.md. Omit to "
                        "run only the global inbox scan.")
    p.add_argument("--cache-root", default=str(Path.home() / ".claude" / "literature_cache"))
    p.add_argument("--require-signed", action="store_true",
                   help="Raise the floor for high-stakes rows to human_signed "
                        "(final-submission sign-off).")
    p.add_argument("--list-queue", action="store_true",
                   help="Print the ordered inbox promotion queue and exit 0.")
    p.add_argument("--json-out", default=None)
    args = p.parse_args(argv)

    findings: list[Finding] = []
    floor = "human_signed" if args.require_signed else rules.DEFAULT_FLOOR

    try:
        blocking: set[str] = set()
        if args.lock:
            lock_path = Path(args.lock).resolve()
            if not lock_path.exists():
                print(f"ERROR: lock manifest not found: {lock_path}", file=sys.stderr)
                return 2
            lock_findings = check_lock(lock_path, floor)
            findings.extend(lock_findings)
            blocking = {m.group(1) for f in lock_findings if f.status == "FAIL"
                        for m in [_BIBKEY_RE.search(f.evidence.get("reference", ""))] if m}
        entries, inbox_findings = scan_inbox(Path(args.cache_root).resolve())
        findings.extend(inbox_findings)
        queue = promotion_queue(entries, blocking)
    except OSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    payload = {
        "provenance": {
            "script_version": SCRIPT_VERSION,
            "rules_version": rules.RULES_VERSION,
            "rules_digest": compute_rules_digest(),
            "floor": floor,
        },
        "findings": [asdict(f) for f in findings],
        "promotion_queue": queue,
        "summary": {
            "FAIL": sum(1 for f in findings if f.status == "FAIL"),
            "WARN": sum(1 for f in findings if f.status == "WARN"),
            "inbox_pending": len(entries),
        },
    }
    out = json.dumps(payload, indent=2)
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(out, encoding="utf-8")
    else:
        print(out)

    if args.list_queue:
        return 0
    return 1 if any(f.status == "FAIL" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
