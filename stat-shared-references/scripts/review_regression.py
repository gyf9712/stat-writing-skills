"""
review_regression.py — cross-cycle regression check for stat-mock-review.

Given the prior MOCK_REVIEW.md and the current one, it flags every canonical
concern raised in the prior review that is not mentioned in the current review.
The point is to stop a previously-raised, artifact-anchored concern from being
silently dropped across a revise-and-resubmit or a later polish cycle.

It keys ONLY on canonical IDs (CS#, PW#, TR#, theorem / assumption labels) that
are owned by project artifacts or the manuscript, never on the review's own
section numbering — that numbering can be silently renumbered, which is exactly
the false-security failure this design avoids.

What it does NOT do
-------------------
- It does not decide whether a dropped concern was genuinely resolved. It detects
  "not mentioned", not "not fixed". The disposition (resolved / still-open /
  regressed) is the human's to record in Section 0 of the current review.

Exit codes
----------
    0 : every prior canonical ID is mentioned in the current review
    1 : at least one prior canonical ID is absent from the current review
    2 : invocation or runtime error

Usage
-----
    python review_regression.py --prior MOCK_REVIEW.prev.md --current MOCK_REVIEW.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import review_regression_rules as rules  # noqa: E402

SCRIPT_VERSION = "1.0.0"


@dataclass
class Finding:
    id: str
    status: str        # DROPPED (affects exit) | CARRIED (info)
    message: str
    evidence: dict = field(default_factory=dict)


def compute_rules_digest() -> str:
    p = HERE / "review_regression_rules.py"
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else "unknown"


def run_check(prior_path: Path, current_path: Path) -> tuple[list[Finding], dict]:
    for p in (prior_path, current_path):
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")
    prior_ids = rules.extract_ids(prior_path.read_text(encoding="utf-8", errors="replace"))
    current_ids = rules.extract_ids(current_path.read_text(encoding="utf-8", errors="replace"))

    findings = []
    for cid in sorted(prior_ids - current_ids):
        findings.append(Finding(
            "regressed_or_dropped_concern", "DROPPED",
            f"Prior canonical concern {cid} is not mentioned in the current review. "
            f"Restate its disposition in Section 0 (resolved / still-open / regressed) "
            f"or explicitly withdraw it.",
            {"id": cid},
        ))
    for cid in sorted(prior_ids & current_ids):
        findings.append(Finding(
            "carried_concern", "CARRIED",
            f"Prior canonical concern {cid} is still referenced in the current review.",
            {"id": cid},
        ))

    context = {
        "script_version": SCRIPT_VERSION,
        "rules_version": rules.RULES_VERSION,
        "rules_digest": compute_rules_digest(),
        "prior_ids": sorted(prior_ids),
        "current_ids": sorted(current_ids),
    }
    return findings, context


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Cross-cycle regression check for MOCK_REVIEW.md.")
    p.add_argument("--prior", required=True, help="Path to the prior MOCK_REVIEW (e.g. MOCK_REVIEW.prev.md).")
    p.add_argument("--current", required=True, help="Path to the current MOCK_REVIEW.md.")
    p.add_argument("--json-out", default=None)
    args = p.parse_args(argv)

    try:
        findings, context = run_check(Path(args.prior).resolve(), Path(args.current).resolve())
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    dropped = [f for f in findings if f.status == "DROPPED"]
    payload = {
        "provenance": context,
        "findings": [asdict(f) for f in findings],
        "summary": {"DROPPED": len(dropped), "CARRIED": len(findings) - len(dropped)},
    }
    out = json.dumps(payload, indent=2)
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(out, encoding="utf-8")
    else:
        print(out)

    return 1 if dropped else 0


if __name__ == "__main__":
    sys.exit(main())
