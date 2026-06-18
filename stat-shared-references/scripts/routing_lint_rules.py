"""
Rule data for routing_lint.py. Data only.

The allowlists are the set of skill names and artifact names that
stat-review-routing.md is permitted to reference. The lint checks referential
integrity ONLY: that every owner skill and artifact named in the routing table
exists here. It never judges whether a route is correct.

Bump RULES_VERSION when the allowlists change. Keep these lists in sync when a
skill is added/renamed in either repo or a new project artifact is introduced.
"""

RULES_VERSION = "1.0.0"

# Skills that may appear in the routing table's "owner" column.
# Writing-repo skills plus the cross-repo theory skills a finding can route to.
KNOWN_SKILLS = {
    # stat-writing-skills
    "stat-paper-plan",
    "stat-paper-write",
    "stat-paper-writing",
    "stat-polishing",
    "stat-mock-review",
    # stat-theory-skills (cross-repo handoff targets)
    "proofcheck",
    "proof-repair",
    "proof-writer",
    "theory-sharpen",
    "theory-simulation",
    "theory-design",
}

# Project artifacts that may appear in the "artifact touched" column.
# "—" means no single artifact and is always allowed.
KNOWN_ARTIFACTS = {
    "CLAIM_SUPPORT_MAP.md",
    "PRIOR_WORK_MATRIX.md",
    "TECHNICAL_RISK_REGISTER.md",
    "MOCK_REVIEW.md",
    "REVISION_PLAN.md",
    "POLISHING_REVIEW.md",
}

# Placeholder allowed in the artifact column.
ARTIFACT_NONE = "—"
