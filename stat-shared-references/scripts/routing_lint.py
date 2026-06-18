"""
routing_lint.py — referential-integrity lint for stat-review-routing.md.

This is the deliberately tiny linter Codex asked for: it checks ONLY that every
owner skill and every artifact named in the routing table exists in the
allowlists. It does NOT check that a route is correct — a wrong-but-existing
route passes. Judging routing correctness is human work; this guards against the
one mechanical failure mode of a hand-maintained table: a route that points at a
skill or artifact that was renamed or removed.

This is the false-authority boundary: the lint emits FAIL only for a broken
reference (mechanical, decidable), never a verdict on routing quality.

Exit codes
----------
    0 : every owner skill and artifact in the table exists
    1 : at least one dangling skill / artifact reference
    2 : invocation or runtime error (e.g. table not found, no table rows)

Usage
-----
    python routing_lint.py --routing ../stat-review-routing.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import routing_lint_rules as rules  # noqa: E402

SCRIPT_VERSION = "1.0.0"

# A markdown table row: | a | b | c | d |
_ROW_RE = re.compile(r"^\|(.+)\|\s*$")


@dataclass
class Finding:
    id: str
    status: str        # FAIL | INFO
    message: str
    evidence: dict = field(default_factory=dict)


def parse_routing_rows(text: str) -> list[dict]:
    """Extract (category, owner, artifact, action) from the routing table.

    Identifies the table by its header row containing 'Primary owner skill' and
    'Artifact touched'. Skips the header and the |---| separator.
    """
    rows = []
    header_cols = None
    for line in text.splitlines():
        m = _ROW_RE.match(line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        # Separator row like |---|---|.
        if all(set(c) <= {"-", ":", " "} and c for c in cells):
            continue
        if header_cols is None:
            # The header is the first table row; lock onto the routing table only.
            if any("owner skill" in c.lower() for c in cells):
                header_cols = cells
            continue
        if len(cells) >= 4:
            rows.append({
                "category": cells[0],
                "owner": cells[1],
                "artifact": cells[2],
                "action": cells[3],
            })
    return rows


def check_rows(rows: list[dict]) -> list[Finding]:
    findings = []
    for r in rows:
        owner = r["owner"]
        if owner not in rules.KNOWN_SKILLS:
            findings.append(Finding(
                "dangling_owner_skill", "FAIL",
                f"Routing row '{r['category']}' names owner skill '{owner}', "
                f"which is not a known skill.",
                {"category": r["category"], "owner": owner},
            ))
        artifact = r["artifact"]
        if artifact != rules.ARTIFACT_NONE and artifact not in rules.KNOWN_ARTIFACTS:
            findings.append(Finding(
                "dangling_artifact", "FAIL",
                f"Routing row '{r['category']}' names artifact '{artifact}', "
                f"which is not a known artifact.",
                {"category": r["category"], "artifact": artifact},
            ))
    return findings


def compute_rules_digest() -> str:
    p = HERE / "routing_lint_rules.py"
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else "unknown"


def run_lint(routing_path: Path) -> tuple[list[Finding], dict]:
    if not routing_path.exists():
        raise FileNotFoundError(f"Routing table not found: {routing_path}")
    text = routing_path.read_text(encoding="utf-8", errors="replace")
    rows = parse_routing_rows(text)
    if not rows:
        raise ValueError("No routing rows found; is this the routing table?")
    findings = check_rows(rows)
    context = {
        "script_version": SCRIPT_VERSION,
        "rules_version": rules.RULES_VERSION,
        "rules_digest": compute_rules_digest(),
        "rows_checked": len(rows),
    }
    return findings, context


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Referential-integrity lint for stat-review-routing.md.")
    default_routing = HERE.parent / "stat-review-routing.md"
    p.add_argument("--routing", default=str(default_routing),
                   help="Path to stat-review-routing.md (defaults to the sibling reference).")
    p.add_argument("--json-out", default=None)
    args = p.parse_args(argv)

    try:
        findings, context = run_lint(Path(args.routing).resolve())
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    payload = {
        "provenance": context,
        "findings": [asdict(f) for f in findings],
        "summary": {"FAIL": sum(1 for f in findings if f.status == "FAIL")},
    }
    out = json.dumps(payload, indent=2)
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(out, encoding="utf-8")
    else:
        print(out)

    return 1 if any(f.status == "FAIL" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
