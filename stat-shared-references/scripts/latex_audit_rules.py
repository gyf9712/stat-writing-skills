"""
latex_audit_rules.py — venue profiles and warning patterns for latex_audit.py.

Data only. No logic except small helpers tightly coupled to the data shape.
Edit this file to add a venue or to refine a regex catalog. Do not move the
rules into the audit script body; that is what `rules_digest` watches.

Rules versioning:
    Bump `RULES_VERSION` (semver) when behavior changes. The script also emits
    a `rules_digest` automatically; the two together pin provenance.
"""

import re

RULES_VERSION = "1.1.0"


# ---------------------------------------------------------------------------
# Citation worklist (item ③): preprint / venue-upgrade and year sanity
# ---------------------------------------------------------------------------
#
# Mechanical bib-hygiene signals. The actual title/author/year/venue
# verification is JUDGMENT owned by stat-positioning-and-claims (web lookup of
# every LOAD-BEARING citation, not a sample). These patterns only surface
# entries worth a human look; preprint flags are heuristic CANDIDATE and never
# affect the exit code.

# An entry whose journal/note/howpublished/series mentions one of these, or
# that carries an eprint field, is likely a preprint that may now have a
# published version (the "venue upgrade").
ARXIV_MARKERS = [
    r"arxiv",
    r"\bpreprint\b",
    r"in preparation",
    r"manuscript in prep",
    r"under review",
    r"submitted\b",
]

# A plausible 4-digit publication year. A present-but-malformed year is flagged
# (heuristic CANDIDATE, because "forthcoming"/"in press" are legitimate).
PLAUSIBLE_YEAR_RE = re.compile(r"^(18|19|20)\d{2}$")


# ---------------------------------------------------------------------------
# Log warning catalog
# ---------------------------------------------------------------------------
#
# Each entry: (regex_pattern, severity, finding_id, fix_hint).
# Severity is one of CRITICAL, HIGH, MEDIUM, LOW.
#
# These match lines in main.log produced by latex/latexmk. Matches are
# emitted as mechanical findings with status WARN (severity MEDIUM/LOW) or
# FAIL (severity HIGH/CRITICAL).

LOG_WARNING_PATTERNS = [
    (
        r"There were undefined references\.",
        "HIGH",
        "log_undefined_references",
        "Run pdflatex twice or fix the unresolved \\ref / \\eqref.",
    ),
    (
        r"Reference `([^']+)' on page (\d+) undefined",
        "HIGH",
        "log_undefined_reference_specific",
        "Add the missing \\label or correct the \\ref key.",
    ),
    (
        r"Citation `([^']+)' on page (\d+) undefined",
        "HIGH",
        "log_undefined_citation_specific",
        "Add the BibTeX entry or correct the \\cite key.",
    ),
    (
        r"There were multiply-defined labels\.",
        "HIGH",
        "log_multiply_defined_labels",
        "Rename or remove the duplicate \\label.",
    ),
    (
        r"Label `([^']+)' multiply defined",
        "HIGH",
        "log_multiply_defined_label_specific",
        "Rename one of the conflicting \\label uses.",
    ),
    (
        r"! LaTeX Error: File `([^']+)' not found",
        "CRITICAL",
        "log_file_not_found",
        "Generate or correctly path the missing file.",
    ),
    (
        r"Overfull \\hbox \(([0-9.]+)pt too wide\)",
        "MEDIUM",
        "log_overfull_hbox",
        "Break the long URL, formula, or word; or accept if <10pt and rare.",
    ),
    (
        r"Missing character: There is no",
        "MEDIUM",
        "log_missing_character",
        "Switch to a Unicode-aware font or escape the offending character.",
    ),
    (
        r"Package natbib Warning: Citation `([^']+)' undefined",
        "HIGH",
        "log_natbib_citation_undefined",
        "Add the BibTeX entry or correct the \\citep / \\citet key.",
    ),
]


# ---------------------------------------------------------------------------
# Venue profiles
# ---------------------------------------------------------------------------
#
# Each venue is a dict with the shape:
#   {
#     "name": str,
#     "documentclass": {
#       "pattern": regex matching the documentclass line,
#       "required_options": list of option substrings that must appear,
#       "forbidden_options": list of option substrings that must not appear,
#     },
#     "required_packages": list of package-name substrings,
#     "spacing": {
#       "required_command": str | None,  # e.g. \doublespacing
#       "forbidden_commands": list[str], # e.g. [\onehalfspacing]
#     },
#     "geometry": {
#       "required_pattern": regex | None,
#     },
#     "citation": {
#       "natbib_required": bool,
#       "forbid_plain_cite": bool,
#     },
#     "abstract_words": {"min": int, "max": int},
#     "bibliographystyle_pattern": regex | None,
#   }

VENUE_PROFILES = {
    "jasa": {
        "name": "JASA (Theory and Methods and Applications and Case Studies)",
        "documentclass": {
            "pattern": r"\\documentclass\[([^\]]*)\]\{article\}",
            "required_options": ["12pt"],
            "forbidden_options": [],
        },
        "required_packages": ["natbib", "setspace", "geometry", "amsmath"],
        "spacing": {
            "required_command": r"\doublespacing",
            "forbidden_commands": [r"\onehalfspacing", r"\singlespacing"],
        },
        "geometry": {
            "required_pattern": r"margin\s*=\s*1\s*in",
        },
        "citation": {
            "natbib_required": True,
            "forbid_plain_cite": True,
        },
        "abstract_words": {"min": 100, "max": 250},
        "bibliographystyle_pattern": None,  # JASA-bundled .bst varies; treat as informational only
    },
}


# ---------------------------------------------------------------------------
# Required-field map for BibTeX entries
# ---------------------------------------------------------------------------
#
# Used by the bib-entry-completeness check. A field is required if it appears
# in the list for the entry type. Unknown entry types are not audited.

BIBTEX_REQUIRED_FIELDS = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "book": ["author", "title", "publisher", "year"],
    "incollection": ["author", "title", "booktitle", "publisher", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
    "misc": [],  # Misc has no required fields; mark only missing year as INFO
    "unpublished": ["author", "title", "note"],
}


# ---------------------------------------------------------------------------
# AI-tell heuristic patterns (CANDIDATE only — never affects exit code)
# ---------------------------------------------------------------------------

AI_TELL_PATTERNS = {
    "em_dash_in_prose": r"(?<!\$)(?<!\\)—(?!\$)",
    "formulaic_opening_in_this_section": r"\bIn this section,? we\b",
    "formulaic_opening_here_we": r"\bHere,? we\b",
    "empty_connective_importantly": r"\bImportantly,",
    "empty_connective_notably": r"\bNotably,",
    "empty_connective_worth_noting": r"\bIt is worth noting that\b",
    "watchword_delve": r"\bdelve\b",
    "watchword_pivotal": r"\bpivotal\b",
    "watchword_landscape": r"\blandscape\b",
    "watchword_underscore": r"\bunderscore\b",
    "watchword_noteworthy": r"\bnoteworthy\b",
    "watchword_leveraging": r"\bleveraging\b",
}
