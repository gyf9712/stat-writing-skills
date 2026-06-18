"""
Rule data for review_regression.py. Data only.

Bump RULES_VERSION when the ID patterns change.
"""

import re

RULES_VERSION = "1.0.0"

# Canonical concern-ID patterns. These IDs are owned by project artifacts
# (CLAIM_SUPPORT_MAP -> CS#, PRIOR_WORK_MATRIX -> PW#, TECHNICAL_RISK_REGISTER
# -> TR#) or by the manuscript's theorem-environment labels. They are NOT the
# review's own section numbering, which the model can silently renumber across
# cycles — keying on canonical IDs is what makes the regression check sound.
#
# Each pattern requires a digit or a label separator, so prose words cannot
# match by accident.
CANONICAL_ID_PATTERNS = [
    r"\bCS\d+\b",
    r"\bPW\d+\b",
    r"\bTR\d+\b",
    r"\b(?:thm|lem|prop|cor|defn|def|ass|assumption|asm|eq|sec|fig|tab)[:\-][\w:\-]+",
]

_COMPILED = [re.compile(p) for p in CANONICAL_ID_PATTERNS]


def extract_ids(text: str) -> set:
    """Return the set of canonical IDs appearing in text.

    Trailing separators are stripped so that a disposition line like
    'thm:main: resolved' yields the same ID as a reference '\\ref{thm:main}'.
    """
    ids = set()
    for rx in _COMPILED:
        for m in rx.finditer(text):
            ids.add(m.group(0).rstrip(":-"))
    return ids
