"""
Rule data for schema_lint.py. Data only.

Three rule classes, all mechanical and decidable (same false-authority boundary
as routing_lint.py: the lint flags pattern violations, never content quality).

1. CANONICAL_SCHEMAS — schemas whose column header is copied into more than one
   file by design (emission fixtures). Every copy must match the canonical
   column list exactly, and every file carrying a copy must be registered.
   Policy source: the schema three-class rule (normative schema / emission
   fixture / explanatory exemplar) from the Statlib-review Codex dialogue,
   threadId 019fbdf0-0438-7b62-b22f-75349d01e175.

2. RETIRED_IDENTIFIERS — enum / family names that were renamed or split and
   must not appear outside history files. Motivating incident: the
   `highdim.tail_condition:moment_based` family was split into
   `exponential_concentration` / `moment_bounded` (v1.8.0), but the definitional
   `same_family` example and the syntax example in applicability-axes.md kept
   the dead name for two months. Reading (human + LLM) found 2 of 10 drift
   sites; grep found all 10.

3. BANNED_LOCATION_PHRASES — repo-location claims that rot when files are
   installed locally. Convention: state the local path; keep provenance as
   "maintained in the <X> source repo". The phrase "sibling <repo>" as a
   location claim is banned; "sibling" in other senses (sibling skill, sibling
   branch of a ladder) is fine and is not matched.

   SCOPE CAVEAT (load-bearing): rule 3 is calibrated for a MERGED INSTALL ROOT
   (e.g. ~/.claude/skills), where install.sh flattens stat-theory-skills and
   stat-writing-skills into one directory and cross-repo references become
   same-directory references. Run against a single source-repo checkout
   instead, and rule 3 false-positives on every genuinely cross-repo pointer
   (e.g. stat-writing-skills' stat-polishing correctly calling
   equivalence-ledger-protocol.md, which lives in stat-theory-skills, "the
   sibling repo" — true at the repo level, false only once both repos are
   copied into the same install directory). Do not "fix" those findings in a
   source repo; the phrase is correct there. This is why the Statlib-review
   drift fixes (2026-08-01) were applied to the install directory only and
   deliberately not ported back to either source repo.

Bump RULES_VERSION when any list changes. When retiring an identifier in a
protocol, add it here in the SAME commit — that is what makes the next drift
impossible instead of merely fixed.
"""

RULES_VERSION = "1.0.0"

# Directories (relative to the skills root) scanned for .md files.
SCAN_DIRS = [
    "stat-paper-plan",
    "stat-paper-write",
    "stat-paper-writing",
    "stat-polishing",
    "stat-mock-review",
    "stat-shared-references",
    "proofcheck",
    "proof-repair",
    "proof-writer",
    "theory-design",
    "theory-sharpen",
    "theory-simulation",
]

# Files that record history (reviews, changelogs, roadmaps). They may quote
# retired identifiers and old phrasing verbatim; all checks skip them.
HISTORY_FILENAMES = {
    "STAT_SKILLS_ROADMAP.md",
    "CHANGELOG.md",
    "CODEX_PROOF_WRITER_REVIEW.md",
    "CODEX_PROTOCOL.md",
}

# --- Rule class 1: canonical schema headers -------------------------------
#
# marker: a cell string that identifies a table as an instance of this schema
#         (must be the FIRST column of the canonical header).
# columns: the canonical ordered column list.
# canonical_file: the file that owns the schema definition.
# copy_allowed: files permitted to carry an emission-fixture copy.
#               Any other file containing the marker column is a violation
#               (delete the copy and point to the canonical file instead).
CANONICAL_SCHEMAS = {
    "cited_results_lock_manifest": {
        "marker": "Citation site",
        "columns": [
            "Citation site",
            "Reference",
            "Citation purpose",
            "Role in literature",
            "Role relative to current paper",
            "Source version at decision",
            "Entry hash at decision",
            "Verification level at decision",
            "Axis or lineage bridge recorded",
            "Decision date",
        ],
        "canonical_file": "stat-shared-references/cited-results-lock-protocol.md",
        "copy_allowed": [
            # Exemplar rows live next to the purpose system.
            "stat-shared-references/citation-purpose-protocol.md",
            # Emission fixture: stat-paper-plan Step 5.7 initializes the artifact.
            "stat-paper-plan/SKILL.md",
        ],
    },
}

# --- Rule class 2: retired identifiers ------------------------------------
#
# pattern is a regex (searched per line); hint tells the fixer what replaced it.
RETIRED_IDENTIFIERS = [
    {
        "id": "family_moment_based",
        "pattern": r"tail_condition:moment_based|\bmoment_based\b",
        "hint": ("Family retired in v1.8.0: split into "
                 "`exponential_concentration` (sub_gaussian, sub_exponential) "
                 "and `moment_bounded` (polynomial_p_moment, bounded_variance). "
                 "See applicability-axes.md domain registry."),
    },
]

# --- Rule class 3: banned repo-location phrases ---------------------------
#
# Location claims only. Plain "sibling skill" / "sibling branch" usages do not
# match these patterns.
BANNED_LOCATION_PHRASES = [
    {
        "id": "sibling_repo_location_claim",
        "pattern": r"(?i)(?:lives?|located|hosted)\s+in\s+the\s+sibling\b"
                   r"|in\s+the\s+sibling\s+`?[\w-]+`?\s+repo\b"
                   r"|sibling\s+`?stat-(?:theory|writing)-skills`?",
        "hint": ("State the local path; keep provenance as 'maintained in the "
                 "<X> source repo'. Installed files are local — location claims "
                 "about sibling repos rot silently."),
    },
]
