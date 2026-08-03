"""
schema_lint.py — mechanical drift lint for schema copies, retired identifiers,
and repo-location phrases across the stat skill family.

Deliberately separate from routing_lint.py, whose contract is referential
integrity of ONE routing table. This linter has a different contract: it scans
the whole stat family for three drift classes that reading (human or LLM)
demonstrably under-detects — in the Statlib-review incident, linear reading
found 2 of 10 live drift sites; pattern match found all 10.

Same false-authority boundary as routing_lint.py: every check is mechanical and
decidable (a header differs from the canonical column list; a retired name
appears; a banned location phrase appears). The lint never judges whether a
schema is well-designed or a sentence is true.

SCOPE: run this against a MERGED INSTALL ROOT (e.g. ~/.claude/skills), not a
single source-repo checkout. The banned_location_phrase check assumes
stat-theory-skills and stat-writing-skills have been flattened into one
directory by install.sh; inside a single repo, a "sibling repo" reference to
the other repo is often true, not drift. See schema_lint_rules.py's SCOPE
CAVEAT for the incident that motivated this note.

Checks
------
    schema_header_mismatch   : a table with a canonical schema's marker column
                               whose header differs from the canonical columns
    schema_copy_unregistered : a canonical schema header appearing in a file
                               not registered as canonical or copy_allowed
    retired_identifier       : a retired enum/family name outside history files
    banned_location_phrase   : a sibling-repo location claim outside history files

Exit codes
----------
    0 : no findings
    1 : at least one FAIL finding
    2 : invocation or runtime error

Usage
-----
    python schema_lint.py                  # scan from the skills root
    python schema_lint.py --root <dir>     # explicit skills root
    python schema_lint.py --json-out audit/schema_lint.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import schema_lint_rules as rules  # noqa: E402

SCRIPT_VERSION = "1.0.0"

_ROW_RE = re.compile(r"^\|(.+)\|\s*$")


@dataclass
class Finding:
    id: str
    status: str        # FAIL | INFO
    message: str
    evidence: dict = field(default_factory=dict)


def iter_md_files(root: Path):
    for d in rules.SCAN_DIRS:
        base = root / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            yield p


def is_history(path: Path) -> bool:
    return path.name in rules.HISTORY_FILENAMES


def parse_header_cells(line: str) -> list[str] | None:
    m = _ROW_RE.match(line.strip())
    if not m:
        return None
    cells = [c.strip() for c in m.group(1).split("|")]
    # Separator row like |---|---|.
    if all(set(c) <= {"-", ":", " "} and c for c in cells):
        return None
    return cells


def check_schemas(path: Path, rel: str, lines: list[str]) -> list[Finding]:
    findings = []
    for name, spec in rules.CANONICAL_SCHEMAS.items():
        marker, canonical = spec["marker"], spec["columns"]
        registered = {spec["canonical_file"], *spec["copy_allowed"]}
        for i, line in enumerate(lines, start=1):
            cells = parse_header_cells(line)
            # Header rows only: first cell must BE the marker, not merely
            # contain it (data rows repeat the marker's column values, not
            # the marker itself).
            if not cells or cells[0] != marker:
                continue
            if rel not in registered:
                findings.append(Finding(
                    "schema_copy_unregistered", "FAIL",
                    f"'{name}' schema header found in unregistered file {rel}:{i}. "
                    f"Delete the copy and point to {spec['canonical_file']}, or "
                    f"register the file as an emission fixture in schema_lint_rules.py.",
                    {"schema": name, "file": rel, "line": i},
                ))
            if cells != canonical:
                findings.append(Finding(
                    "schema_header_mismatch", "FAIL",
                    f"'{name}' header at {rel}:{i} differs from the canonical "
                    f"column list in {spec['canonical_file']}.",
                    {"schema": name, "file": rel, "line": i,
                     "found": cells, "canonical": canonical},
                ))
    return findings


def check_line_rules(path: Path, rel: str, lines: list[str]) -> list[Finding]:
    findings = []
    line_rules = (
        [("retired_identifier", r) for r in rules.RETIRED_IDENTIFIERS]
        + [("banned_location_phrase", r) for r in rules.BANNED_LOCATION_PHRASES]
    )
    compiled = [(fid, r["id"], re.compile(r["pattern"]), r["hint"]) for fid, r in line_rules]
    for i, line in enumerate(lines, start=1):
        for fid, rid, rx, hint in compiled:
            if rx.search(line):
                findings.append(Finding(
                    fid, "FAIL",
                    f"{rid} at {rel}:{i}. {hint}",
                    {"rule": rid, "file": rel, "line": i, "text": line.strip()[:200]},
                ))
    return findings


def compute_rules_digest() -> str:
    p = HERE / "schema_lint_rules.py"
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else "unknown"


def run_lint(root: Path) -> tuple[list[Finding], dict]:
    if not root.is_dir():
        raise FileNotFoundError(f"Skills root not found: {root}")
    findings, files_scanned = [], 0
    for path in iter_md_files(root):
        rel = path.relative_to(root).as_posix()
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        files_scanned += 1
        # Schema checks run everywhere (history files never carry live schema
        # copies; if one does, that is itself worth a finding). Line rules
        # skip history files, which quote old names verbatim by design.
        findings.extend(check_schemas(path, rel, lines))
        if not is_history(path):
            findings.extend(check_line_rules(path, rel, lines))
    if files_scanned == 0:
        raise ValueError(f"No markdown files found under {root} in SCAN_DIRS.")
    context = {
        "script_version": SCRIPT_VERSION,
        "rules_version": rules.RULES_VERSION,
        "rules_digest": compute_rules_digest(),
        "files_scanned": files_scanned,
    }
    return findings, context


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Mechanical drift lint: schema copies, retired identifiers, location phrases.")
    default_root = HERE.parent.parent  # .../skills
    p.add_argument("--root", default=str(default_root),
                   help="Skills root containing the stat skill directories.")
    p.add_argument("--json-out", default=None)
    args = p.parse_args(argv)

    try:
        findings, context = run_lint(Path(args.root).resolve())
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
