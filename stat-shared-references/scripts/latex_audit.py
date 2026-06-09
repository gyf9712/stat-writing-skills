"""
latex_audit.py — mechanical LaTeX audit for statistics manuscripts.

Authoritative only for mechanical checks (refs, cites, images, template
conformance, abstract word count, compile-log warnings, cross-file leaks).
Heuristic checks (AI tells) emit CANDIDATE findings only and never affect
the exit code.

Usage
-----
    python latex_audit.py \\
        --main main.tex \\
        --supplement supplement.tex \\
        --supplement-mode separate-self-contained \\
        --venue jasa \\
        --compile auto \\
        --json-out audit/latex_audit.json \\
        --md-out audit/LATEX_AUDIT_REPORT.md

Exit codes
----------
    0 : no mechanical FAIL findings
    1 : at least one mechanical FAIL finding
    2 : invocation or runtime error

Design
------
Findings are split into two kinds:

    mechanical  : PASS / FAIL / WARN / INFO   (affects exit code)
    heuristic   : CANDIDATE / REVIEW           (never affects exit code)

Run `--help` for the full CLI.

Versioning
----------
This script's behavior is pinned by `SCRIPT_VERSION` below.
The rule data lives in `latex_audit_rules.py`; its digest is emitted at run
time as `rules_digest`. The two together pin provenance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# Local import (data-only rules module).
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import latex_audit_rules as rules  # noqa: E402

SCRIPT_VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# Finding dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    id: str
    kind: str  # "mechanical" or "heuristic"
    status: str  # mechanical: PASS|FAIL|WARN|INFO  heuristic: CANDIDATE|REVIEW
    severity: str  # CRITICAL|HIGH|MEDIUM|LOW|REVIEW
    message: str
    evidence: dict = field(default_factory=dict)
    fix_hint: Optional[str] = None
    review_question: Optional[str] = None


def is_mechanical_fail(f: Finding) -> bool:
    return f.kind == "mechanical" and f.status == "FAIL"


# ---------------------------------------------------------------------------
# LaTeX scanning utilities
# ---------------------------------------------------------------------------

# Strip line comments (% to EOL) but preserve escaped \%.
_COMMENT_RE = re.compile(r"(?<!\\)%.*?$", re.MULTILINE)


_INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")


def read_tex_source(path: Path, _seen: Optional[set] = None) -> str:
    """Read a .tex file, strip line comments, and inline \\input{...} / \\include{...}.

    Following inputs is necessary to see all \\label, \\ref, \\cite, and
    \\includegraphics in the compilation unit, not just those in the root file.

    Cycles are guarded by `_seen`. Missing inputs are silently elided (a
    separate check could flag them, but here we focus on cross-checks).
    """
    if _seen is None:
        _seen = set()
    if not path.exists():
        return ""
    resolved = path.resolve()
    if resolved in _seen:
        return ""
    _seen.add(resolved)
    text = path.read_text(encoding="utf-8", errors="replace")
    text = _COMMENT_RE.sub("", text)

    def _resolve_input(match: re.Match) -> str:
        sub_name = match.group(1).strip()
        # LaTeX \input may omit the .tex extension.
        candidates = [path.parent / sub_name]
        if not sub_name.endswith(".tex"):
            candidates.append(path.parent / (sub_name + ".tex"))
        for cand in candidates:
            if cand.exists():
                return "\n" + read_tex_source(cand, _seen) + "\n"
        return ""  # silently elide missing input

    return _INPUT_RE.sub(_resolve_input, text)


def find_labels(source: str) -> list[tuple[str, int]]:
    """Return list of (label_name, line_number) defined via \\label{...}."""
    out = []
    for m in re.finditer(r"\\label\{([^}]+)\}", source):
        line = source[: m.start()].count("\n") + 1
        out.append((m.group(1), line))
    return out


def find_refs(source: str) -> list[tuple[str, int]]:
    """Return list of (ref_target, line_number) used via \\ref{}, \\eqref{}, \\cref{}, \\autoref{}."""
    out = []
    for m in re.finditer(r"\\(?:eq|auto|c|C|name|page)?ref\{([^}]+)\}", source):
        line = source[: m.start()].count("\n") + 1
        out.append((m.group(1), line))
    return out


def find_cites(source: str) -> list[tuple[str, int]]:
    """Return list of (citation_key, line_number) from \\cite{}, \\citep{}, \\citet{}.

    Handles comma-separated keys: \\cite{a, b, c} → three entries.
    """
    out = []
    for m in re.finditer(r"\\cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]+)\}", source):
        line = source[: m.start()].count("\n") + 1
        for raw_key in m.group(1).split(","):
            key = raw_key.strip()
            if key:
                out.append((key, line))
    return out


def find_includegraphics(source: str) -> list[tuple[str, int]]:
    """Return list of (image_path, line_number) from \\includegraphics."""
    out = []
    for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source):
        line = source[: m.start()].count("\n") + 1
        out.append((m.group(1), line))
    return out


def find_plain_cites(source: str) -> list[tuple[str, int]]:
    """Find plain \\cite{} usage (not natbib \\citet/\\citep). Used for citation policy."""
    out = []
    for m in re.finditer(r"\\cite\{[^}]+\}", source):
        line = source[: m.start()].count("\n") + 1
        out.append((m.group(0), line))
    return out


# ---------------------------------------------------------------------------
# BibTeX scanning
# ---------------------------------------------------------------------------

_BIB_ENTRY_RE = re.compile(
    r"@(?P<type>[a-zA-Z]+)\s*\{\s*(?P<key>[^,]+),(?P<body>.*?)\n\s*\}",
    re.DOTALL,
)
_BIB_FIELD_RE = re.compile(r"(\w+)\s*=\s*[\{\"]", re.IGNORECASE)


def parse_bib(path: Path) -> dict[str, dict]:
    """Parse a .bib file into {key: {"type": str, "fields": set[str]}}.

    Lightweight; does not extract field values. Used for completeness checks.
    """
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    entries = {}
    for m in _BIB_ENTRY_RE.finditer(text):
        key = m.group("key").strip()
        body = m.group("body")
        fields = {fm.group(1).lower() for fm in _BIB_FIELD_RE.finditer(body)}
        entries[key] = {"type": m.group("type").lower(), "fields": fields}
    return entries


# ---------------------------------------------------------------------------
# Abstract extraction
# ---------------------------------------------------------------------------

_ABSTRACT_RE = re.compile(
    r"\\begin\{abstract\}(.*?)\\end\{abstract\}", re.DOTALL
)


def extract_abstract(source: str) -> Optional[str]:
    m = _ABSTRACT_RE.search(source)
    if not m:
        return None
    return m.group(1)


def count_abstract_words(abstract: str) -> int:
    """Count words in an abstract, stripping LaTeX commands and math.

    Heuristic but mechanical: drops $...$ and $$...$$ math, drops \\command,
    drops braces, then splits on whitespace.
    """
    text = re.sub(r"\$\$.*?\$\$", " MATH ", abstract, flags=re.DOTALL)
    text = re.sub(r"\$[^$]*\$", " MATH ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    text = re.sub(r"[{}]", " ", text)
    return len([w for w in text.split() if w.strip()])


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_ref_label_consistency(
    main_source: str,
    supplement_source: str,
    main_path: Path,
    supplement_path: Optional[Path],
    supplement_mode: str,
) -> list[Finding]:
    """Check \\ref{} resolves to a \\label{} in the same compilation unit.

    For separate-self-contained supplement mode, also detect cross-file leaks:
    the supplement uses \\ref{key} where key is defined only in main, or vice
    versa.
    """
    findings = []

    main_labels = {name for name, _ in find_labels(main_source)}
    main_refs = find_refs(main_source)
    supp_labels = {name for name, _ in find_labels(supplement_source)} if supplement_source else set()
    supp_refs = find_refs(supplement_source) if supplement_source else []

    # Main paper internal consistency.
    for target, line in main_refs:
        if target in main_labels:
            continue
        # In linked-appendix mode, allow main → supplement.
        if supplement_mode == "linked-appendix" and target in supp_labels:
            findings.append(Finding(
                id="ref_resolved_via_supplement",
                kind="mechanical",
                status="INFO",
                severity="LOW",
                message=f"Main \\ref{{{target}}} resolves only via supplement (linked-appendix mode).",
                evidence={"file": str(main_path), "line": line, "target": target},
            ))
            continue
        if supplement_mode == "separate-self-contained" and target in supp_labels:
            findings.append(Finding(
                id="cross_file_ref_main_to_supplement",
                kind="mechanical",
                status="FAIL",
                severity="HIGH",
                message=(
                    f"Main paper uses \\ref{{{target}}} but the label is "
                    f"defined only in the supplement; this resolves to '??' "
                    f"when the main paper compiles standalone."
                ),
                evidence={"file": str(main_path), "line": line, "target": target},
                fix_hint="Replace with a textual reference (e.g., 'Section S.2 of the Supplement').",
            ))
            continue
        findings.append(Finding(
            id="undefined_ref",
            kind="mechanical",
            status="FAIL",
            severity="HIGH",
            message=f"\\ref{{{target}}} has no matching \\label.",
            evidence={"file": str(main_path), "line": line, "target": target},
            fix_hint="Add the \\label or correct the \\ref key.",
        ))

    # Supplement internal consistency.
    if supplement_source and supplement_path is not None:
        for target, line in supp_refs:
            if target in supp_labels:
                continue
            if supplement_mode == "linked-appendix" and target in main_labels:
                continue
            if supplement_mode == "separate-self-contained" and target in main_labels:
                findings.append(Finding(
                    id="cross_file_ref_supplement_to_main",
                    kind="mechanical",
                    status="FAIL",
                    severity="HIGH",
                    message=(
                        f"Supplement uses \\ref{{{target}}} but the label is "
                        f"defined only in the main paper; this resolves to '??' "
                        f"when the supplement compiles standalone (the canonical "
                        f"JASA / AoS / Biometrika / JRSS-B case)."
                    ),
                    evidence={"file": str(supplement_path), "line": line, "target": target},
                    fix_hint=(
                        "Use a textual reference (e.g., 'Theorem 1 of the main paper') "
                        "or restate the theorem in the supplement at the start of its proof."
                    ),
                ))
                continue
            findings.append(Finding(
                id="undefined_ref_supplement",
                kind="mechanical",
                status="FAIL",
                severity="HIGH",
                message=f"Supplement \\ref{{{target}}} has no matching \\label.",
                evidence={"file": str(supplement_path), "line": line, "target": target},
            ))

    return findings


def check_cite_bib_consistency(
    main_source: str,
    supplement_source: str,
    bib_entries: dict,
    main_path: Path,
    supplement_path: Optional[Path],
) -> list[Finding]:
    findings = []
    bib_keys = set(bib_entries.keys())
    used_keys: set[str] = set()

    for key, line in find_cites(main_source):
        used_keys.add(key)
        if key not in bib_keys:
            findings.append(Finding(
                id="missing_citation_key",
                kind="mechanical",
                status="FAIL",
                severity="HIGH",
                message=f"\\cite{{{key}}} has no matching .bib entry.",
                evidence={"file": str(main_path), "line": line, "citation_key": key},
                fix_hint="Add the BibTeX entry or correct the \\cite key.",
            ))

    if supplement_source and supplement_path is not None:
        for key, line in find_cites(supplement_source):
            used_keys.add(key)
            if key not in bib_keys:
                findings.append(Finding(
                    id="missing_citation_key_supplement",
                    kind="mechanical",
                    status="FAIL",
                    severity="HIGH",
                    message=f"Supplement \\cite{{{key}}} has no matching .bib entry.",
                    evidence={"file": str(supplement_path), "line": line, "citation_key": key},
                ))

    # Bib bloat: entries defined but never cited.
    for key in sorted(bib_keys - used_keys):
        findings.append(Finding(
            id="unused_bib_entry",
            kind="mechanical",
            status="WARN",
            severity="LOW",
            message=f"BibTeX entry '{key}' is defined but never cited.",
            evidence={"citation_key": key},
            fix_hint="Remove from .bib or add a citation.",
        ))

    return findings


def check_bib_entry_completeness(bib_entries: dict, bib_path: Path) -> list[Finding]:
    findings = []
    for key, entry in bib_entries.items():
        required = rules.BIBTEX_REQUIRED_FIELDS.get(entry["type"], [])
        missing = [r for r in required if r not in entry["fields"]]
        if missing:
            findings.append(Finding(
                id="incomplete_bib_entry",
                kind="mechanical",
                status="FAIL" if entry["type"] != "misc" else "WARN",
                severity="HIGH" if entry["type"] != "misc" else "LOW",
                message=(
                    f"BibTeX entry '{key}' (@{entry['type']}) is missing required "
                    f"fields: {', '.join(missing)}."
                ),
                evidence={"file": str(bib_path), "citation_key": key,
                          "type": entry["type"], "missing_fields": missing},
                fix_hint="Add the missing field(s) or change the entry type.",
            ))
    return findings


def check_image_files(
    main_source: str,
    supplement_source: str,
    main_path: Path,
    supplement_path: Optional[Path],
) -> list[Finding]:
    findings = []
    common_exts = ["", ".pdf", ".png", ".jpg", ".jpeg", ".eps"]

    def _check_one(path_str: str, src_file: Path, line: int) -> Optional[Finding]:
        # Resolve relative to the .tex file's directory.
        src_dir = src_file.parent
        for ext in common_exts:
            candidate = src_dir / (path_str + ext)
            if candidate.exists():
                return None
            # Also try the figures/ convention.
            candidate2 = src_dir / "figures" / (path_str + ext)
            if candidate2.exists():
                return None
        return Finding(
            id="missing_image_file",
            kind="mechanical",
            status="FAIL",
            severity="CRITICAL",
            message=f"\\includegraphics references '{path_str}' but the file is not found.",
            evidence={"file": str(src_file), "line": line, "image_path": path_str},
            fix_hint="Generate the figure or correct the path.",
        )

    for path_str, line in find_includegraphics(main_source):
        f = _check_one(path_str, main_path, line)
        if f:
            findings.append(f)
    if supplement_source and supplement_path is not None:
        for path_str, line in find_includegraphics(supplement_source):
            f = _check_one(path_str, supplement_path, line)
            if f:
                findings.append(f)
    return findings


def check_template_conformance(
    main_source: str, main_path: Path, venue: str
) -> list[Finding]:
    findings = []
    if venue == "none" or venue not in rules.VENUE_PROFILES:
        return findings
    profile = rules.VENUE_PROFILES[venue]

    # Documentclass
    docclass_re = profile["documentclass"]["pattern"]
    docclass_match = re.search(docclass_re, main_source)
    if not docclass_match:
        findings.append(Finding(
            id="venue_documentclass_missing",
            kind="mechanical",
            status="FAIL",
            severity="HIGH",
            message=f"{profile['name']} requires \\documentclass[...]{{article}} but the pattern was not found.",
            evidence={"file": str(main_path), "venue": venue},
            fix_hint=r"Use \documentclass[12pt]{article}.",
        ))
    else:
        options_str = docclass_match.group(1) if docclass_match.groups() else ""
        for req in profile["documentclass"]["required_options"]:
            if req not in options_str:
                findings.append(Finding(
                    id=f"venue_documentclass_missing_option_{req}",
                    kind="mechanical",
                    status="FAIL",
                    severity="HIGH",
                    message=f"{profile['name']} requires documentclass option '{req}'; found options '{options_str}'.",
                    evidence={"file": str(main_path), "venue": venue, "required": req,
                              "found_options": options_str},
                    fix_hint=fr"Add '{req}' to the \documentclass options, e.g. \documentclass[12pt]{{article}}.",
                ))

    # Required packages
    for pkg in profile["required_packages"]:
        if not re.search(r"\\usepackage(?:\[[^\]]*\])?\{[^}]*\b" + re.escape(pkg) + r"\b[^}]*\}", main_source):
            findings.append(Finding(
                id=f"venue_missing_package_{pkg}",
                kind="mechanical",
                status="WARN",
                severity="MEDIUM",
                message=f"{profile['name']} expects \\usepackage{{{pkg}}}; not found.",
                evidence={"file": str(main_path), "venue": venue, "package": pkg},
                fix_hint=fr"Add \usepackage{{{pkg}}} to the preamble.",
            ))

    # Spacing: required command must be present; forbidden commands must not be.
    spacing = profile["spacing"]
    if spacing.get("required_command"):
        cmd = spacing["required_command"]
        if cmd not in main_source:
            findings.append(Finding(
                id="venue_missing_required_spacing",
                kind="mechanical",
                status="FAIL",
                severity="HIGH",
                message=f"{profile['name']} requires {cmd}; not found in the source.",
                evidence={"file": str(main_path), "venue": venue, "required": cmd},
                fix_hint=fr"Add {cmd} (from \usepackage{{setspace}}) to the preamble.",
            ))
    for forbidden in spacing.get("forbidden_commands", []):
        if forbidden in main_source:
            findings.append(Finding(
                id=f"venue_forbidden_spacing_{forbidden.strip(chr(92))}",
                kind="mechanical",
                status="FAIL",
                severity="HIGH",
                message=f"{profile['name']} does not allow {forbidden}; the manuscript must be fully double-spaced.",
                evidence={"file": str(main_path), "venue": venue, "forbidden": forbidden},
                fix_hint=fr"Replace {forbidden} with \doublespacing.",
            ))

    # Geometry
    geom = profile["geometry"].get("required_pattern")
    if geom and not re.search(geom, main_source):
        findings.append(Finding(
            id="venue_geometry_margin_fail",
            kind="mechanical",
            status="FAIL",
            severity="MEDIUM",
            message=f"{profile['name']} requires geometry margin=1in; pattern not found.",
            evidence={"file": str(main_path), "venue": venue, "expected": geom},
            fix_hint=r"Add \usepackage[margin=1in]{geometry}.",
        ))

    # Citation policy
    if profile["citation"].get("forbid_plain_cite"):
        plain_cites = find_plain_cites(main_source)
        for raw, line in plain_cites:
            findings.append(Finding(
                id="venue_plain_cite_used",
                kind="mechanical",
                status="FAIL",
                severity="MEDIUM",
                message=f"{profile['name']} uses author-year citations; plain \\cite is not appropriate.",
                evidence={"file": str(main_path), "line": line, "match": raw},
                fix_hint=r"Use \citep{} or \citet{} from natbib.",
            ))

    return findings


def check_abstract_word_count(main_source: str, main_path: Path, venue: str) -> list[Finding]:
    abstract = extract_abstract(main_source)
    if abstract is None:
        return [Finding(
            id="abstract_not_found",
            kind="mechanical",
            status="WARN",
            severity="MEDIUM",
            message=r"No \begin{abstract}...\end{abstract} block found in the main source.",
            evidence={"file": str(main_path)},
            fix_hint="Add an abstract block or pass a sub-file that contains it via --main.",
        )]
    word_count = count_abstract_words(abstract)
    if venue == "none" or venue not in rules.VENUE_PROFILES:
        return [Finding(
            id="abstract_word_count",
            kind="mechanical",
            status="INFO",
            severity="LOW",
            message=f"Abstract word count: {word_count}.",
            evidence={"file": str(main_path), "word_count": word_count},
        )]
    profile = rules.VENUE_PROFILES[venue]
    rng = profile["abstract_words"]
    if word_count > rng["max"]:
        return [Finding(
            id="abstract_too_long",
            kind="mechanical",
            status="FAIL",
            severity="HIGH",
            message=(
                f"{profile['name']} expects abstract length {rng['min']}-{rng['max']} words; "
                f"counted {word_count}."
            ),
            evidence={"file": str(main_path), "venue": venue,
                      "word_count": word_count, "range": rng},
            fix_hint="Cut the second motivating paragraph or merge result-and-implication sentences.",
        )]
    if word_count < rng["min"]:
        return [Finding(
            id="abstract_too_short",
            kind="mechanical",
            status="WARN",
            severity="MEDIUM",
            message=(
                f"{profile['name']} expects abstract length {rng['min']}-{rng['max']} words; "
                f"counted {word_count}."
            ),
            evidence={"file": str(main_path), "venue": venue,
                      "word_count": word_count, "range": rng},
        )]
    return [Finding(
        id="abstract_word_count",
        kind="mechanical",
        status="PASS",
        severity="LOW",
        message=f"Abstract word count {word_count} is within {rng['min']}-{rng['max']}.",
        evidence={"file": str(main_path), "word_count": word_count, "range": rng},
    )]


def check_compile_log(log_path: Optional[Path]) -> list[Finding]:
    if log_path is None or not log_path.exists():
        return []
    text = log_path.read_text(encoding="utf-8", errors="replace")
    findings = []
    for pattern, severity, fid, fix_hint in rules.LOG_WARNING_PATTERNS:
        for m in re.finditer(pattern, text):
            status = "FAIL" if severity in ("HIGH", "CRITICAL") else "WARN"
            findings.append(Finding(
                id=fid,
                kind="mechanical",
                status=status,
                severity=severity,
                message=m.group(0).strip(),
                evidence={"file": str(log_path), "match": m.group(0).strip(),
                          "groups": list(m.groups())},
                fix_hint=fix_hint,
            ))
    return findings


# ---------------------------------------------------------------------------
# Output rendering
# ---------------------------------------------------------------------------

def render_json(findings: list[Finding], context: dict) -> str:
    return json.dumps(
        {
            "provenance": context,
            "summary": _summarize(findings),
            "findings": [asdict(f) for f in findings],
        },
        indent=2,
        sort_keys=False,
    )


def render_markdown(findings: list[Finding], context: dict) -> str:
    mech_fail = [f for f in findings if f.kind == "mechanical" and f.status == "FAIL"]
    mech_warn = [f for f in findings if f.kind == "mechanical" and f.status in ("WARN", "INFO")]
    mech_pass = [f for f in findings if f.kind == "mechanical" and f.status == "PASS"]
    heuristic = [f for f in findings if f.kind == "heuristic"]

    lines = ["# LaTeX Audit Report", ""]
    lines.append(f"- Script version: `{context['script_version']}`")
    lines.append(f"- Rules version: `{context['rules_version']}`")
    lines.append(f"- Rules digest: `{context['rules_digest']}`")
    lines.append(f"- Venue: `{context['venue']}`")
    lines.append(f"- Supplement mode: `{context['supplement_mode']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    summary = _summarize(findings)
    lines.append(f"- Mechanical FAIL: {summary['mechanical']['FAIL']}")
    lines.append(f"- Mechanical WARN: {summary['mechanical']['WARN']}")
    lines.append(f"- Mechanical INFO: {summary['mechanical']['INFO']}")
    lines.append(f"- Mechanical PASS: {summary['mechanical']['PASS']}")
    lines.append(f"- Heuristic CANDIDATE: {summary['heuristic']['CANDIDATE']}")
    lines.append("")
    lines.append("**Exit code**: 0 only when mechanical FAIL = 0.")
    lines.append("")

    if mech_fail:
        lines.append("## Mechanical FAIL")
        lines.append("")
        for f in mech_fail:
            lines.extend(_render_finding(f))
            lines.append("")
    if mech_warn:
        lines.append("## Mechanical WARN / INFO")
        lines.append("")
        for f in mech_warn:
            lines.extend(_render_finding(f))
            lines.append("")
    if mech_pass:
        lines.append("## Mechanical PASS")
        lines.append("")
        for f in mech_pass:
            lines.extend(_render_finding(f))
            lines.append("")
    if heuristic:
        lines.append("## Review Cues (heuristic, never affects exit code)")
        lines.append("")
        for f in heuristic:
            lines.extend(_render_finding(f))
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_finding(f: Finding) -> list[str]:
    lines = [f"### `{f.id}` [{f.status} / {f.severity}]"]
    lines.append("")
    lines.append(f.message)
    if f.evidence:
        lines.append("")
        lines.append("Evidence:")
        for k, v in f.evidence.items():
            lines.append(f"- `{k}`: `{v}`")
    if f.fix_hint:
        lines.append("")
        lines.append(f"Fix: {f.fix_hint}")
    if f.review_question:
        lines.append("")
        lines.append(f"Review question: {f.review_question}")
    return lines


def _summarize(findings: list[Finding]) -> dict:
    summary = {
        "mechanical": {"PASS": 0, "FAIL": 0, "WARN": 0, "INFO": 0},
        "heuristic": {"CANDIDATE": 0, "REVIEW": 0},
    }
    for f in findings:
        if f.kind == "mechanical":
            summary["mechanical"][f.status] = summary["mechanical"].get(f.status, 0) + 1
        else:
            summary["heuristic"][f.status] = summary["heuristic"].get(f.status, 0) + 1
    return summary


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def compute_rules_digest() -> str:
    """Hash the rules module source file. Catches data-only edits."""
    rules_path = HERE / "latex_audit_rules.py"
    if not rules_path.exists():
        return "unknown"
    return hashlib.sha256(rules_path.read_bytes()).hexdigest()[:16]


def discover_bib(main_path: Path, main_source: str) -> Optional[Path]:
    """Find the .bib file from \\bibliography{...} or default to refs.bib next to main."""
    m = re.search(r"\\bibliography\{([^}]+)\}", main_source)
    if m:
        names = [name.strip() for name in m.group(1).split(",")]
        for name in names:
            candidate = (main_path.parent / name).with_suffix(".bib")
            if candidate.exists():
                return candidate
    # Fallbacks.
    for cand in ["refs.bib", "references.bib"]:
        candidate = main_path.parent / cand
        if candidate.exists():
            return candidate
    return None


def run_audit(args: argparse.Namespace) -> tuple[list[Finding], dict]:
    main_path = Path(args.main).resolve()
    if not main_path.exists():
        raise FileNotFoundError(f"Main file not found: {main_path}")
    main_source = read_tex_source(main_path)

    supplement_path = Path(args.supplement).resolve() if args.supplement else None
    supplement_source = read_tex_source(supplement_path) if supplement_path else ""

    findings: list[Finding] = []

    # Template conformance
    findings.extend(check_template_conformance(main_source, main_path, args.venue))

    # Abstract word count
    findings.extend(check_abstract_word_count(main_source, main_path, args.venue))

    # ref / label
    findings.extend(check_ref_label_consistency(
        main_source, supplement_source, main_path, supplement_path, args.supplement_mode,
    ))

    # cite / .bib
    bib_path = discover_bib(main_path, main_source)
    bib_entries = parse_bib(bib_path) if bib_path else {}
    findings.extend(check_cite_bib_consistency(
        main_source, supplement_source, bib_entries, main_path, supplement_path,
    ))
    if bib_path:
        findings.extend(check_bib_entry_completeness(bib_entries, bib_path))

    # Images
    findings.extend(check_image_files(main_source, supplement_source, main_path, supplement_path))

    # Compile log
    if args.compile != "never":
        log_path = main_path.parent / "logs" / "main.compile.log"
        if not log_path.exists():
            log_path = main_path.with_suffix(".log")
        findings.extend(check_compile_log(log_path if log_path.exists() else None))

    # Provenance
    context = {
        "script_version": SCRIPT_VERSION,
        "rules_version": rules.RULES_VERSION,
        "rules_digest": compute_rules_digest(),
        "venue": args.venue,
        "supplement_mode": args.supplement_mode,
        "main": str(main_path),
        "supplement": str(supplement_path) if supplement_path else None,
        "bib": str(bib_path) if bib_path else None,
    }
    return findings, context


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="Mechanical LaTeX audit for statistics manuscripts.",
    )
    p.add_argument("--main", required=True, help="Path to main .tex file.")
    p.add_argument("--supplement", default=None, help="Optional path to supplement .tex.")
    p.add_argument(
        "--supplement-mode",
        choices=["separate-self-contained", "linked-appendix", "none"],
        default="none",
    )
    p.add_argument(
        "--venue",
        choices=["none", "jasa"],
        default="none",
        help="Venue profile for template conformance checks. v1: jasa only.",
    )
    p.add_argument(
        "--compile",
        choices=["auto", "never"],
        default="auto",
        help="auto: parse existing main.log if present. never: skip log parsing.",
    )
    p.add_argument("--json-out", default=None, help="Path to write structured JSON.")
    p.add_argument("--md-out", default=None, help="Path to write Markdown report.")

    args = p.parse_args(argv)

    try:
        findings, context = run_audit(args)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"ERROR: unexpected: {e}", file=sys.stderr)
        return 2

    json_payload = render_json(findings, context)
    md_payload = render_markdown(findings, context)

    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(json_payload, encoding="utf-8")
    if args.md_out:
        Path(args.md_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.md_out).write_text(md_payload, encoding="utf-8")
    if not args.json_out and not args.md_out:
        print(json_payload)

    return 1 if any(is_mechanical_fail(f) for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
