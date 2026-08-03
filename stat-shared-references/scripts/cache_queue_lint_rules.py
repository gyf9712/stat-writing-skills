"""
Rule data for cache_queue_lint.py. Data only.

Policy sources (this file encodes existing policy; it introduces none):

- Verification floor: cited-results-lock-protocol.md ("Every load-bearing row
  (purpose in {load_bearing, benchmark_claim, comparative}) is at
  `independently_checked` or higher; if not, the row is flagged GAP").
- State order: cache-verification-states.md (4 states).
- Inbox warning thresholds and the hard-fail/warn split: the Statlib-review
  Codex dialogue, threadId 019fbdf0-0438-7b62-b22f-75349d01e175 — current-
  project gate breaches block; global backlog only warns. Rationale: Statlib's
  failure mode was verification WIP exceeding verification capacity (PRs
  unreviewed for months); a cap enforced where nobody passes is decoration, so
  the block attaches to project gates and the global queue merely surfaces.
- Promotion queue order: current-project blockers > canonical-role entries >
  age. Canonical role is LOCAL cache metadata (role_in_literature), never an
  external taxonomy.

Bump RULES_VERSION on any change.
"""

RULES_VERSION = "1.0.0"

# cache-verification-states.md, ascending trust.
STATE_ORDER = [
    "unverified_extract",
    "source_checked",
    "independently_checked",
    "human_signed",
]

# Purposes subject to the verification floor (cited-results-lock-protocol.md).
HIGH_STAKES_PURPOSES = {"load_bearing", "benchmark_claim", "comparative"}

# Default floor for high-stakes rows. --require-signed raises it to
# human_signed at wiring points that demand sign-off (final submission).
DEFAULT_FLOOR = "independently_checked"

# Global inbox backlog: warning-only, never affects exit code.
INBOX_WARN_COUNT = 20
INBOX_WARN_AGE_DAYS = 14

# role_in_literature values that mark an entry as canonical for promotion
# ordering (verification cost amortizes across papers).
CANONICAL_ROLES = {"anchor", "canonical_first", "standard_tool", "technique_source"}
