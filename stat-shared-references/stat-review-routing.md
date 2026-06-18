# Review-Finding Routing

A coarse map from a review finding to the **one skill that owns the first fix**, the
artifact it touches, and the first action. Its only job is to normalize the **first
handoff**. It is deliberately weak:

- It is a human-facing reference, **not** an executable source of truth. A router that
  becomes authoritative rots and starts lying as skills change. When a skill is renamed
  or its scope shifts, edit this table by hand.
- It does **not** override a skill's own internal escalation. `theory-simulation`,
  `proofcheck`, and `stat-polishing` each route their own findings further; this table
  only says where a concern goes *first*.
- Owners are **skills**, never shared references. `stat-style-discipline.md` and
  `stat-figure-design.md` are references the owning skill applies; the owner is
  `stat-polishing`.

A concern may have a secondary owner. Route to the primary first and let that skill
escalate. Findings on the theoretical content cross into the `stat-theory-skills`
repo (`proofcheck`, `proof-repair`, `theory-sharpen`, `theory-simulation`).

## Who uses it

`stat-mock-review` uses this table to turn each Rescue-Plan item into a single owner.
The `stat-paper-writing` pipeline uses it to dispatch review findings to the right
stage instead of re-deriving the mapping each round.

## Routing table

| Finding category | Primary owner skill | Artifact touched | First action |
|---|---|---|---|
| Overclaim / claim exceeds evidence | stat-polishing | CLAIM_SUPPORT_MAP.md | Apply stat-positioning-and-claims.md; soften the verb or restrict scope |
| Prior work missing or mischaracterized | stat-polishing | PRIOR_WORK_MATRIX.md | Apply stat-positioning-and-claims.md; literature search; verify the cited result |
| Weak contribution / unclear positioning | stat-paper-plan | PRIOR_WORK_MATRIX.md | Re-derive the contribution against the prior-work matrix |
| Unaddressed technical risk | stat-polishing | TECHNICAL_RISK_REGISTER.md | Apply stat-positioning-and-claims.md; register the risk or add an explicit disclosure |
| Assumptions too strong | theory-sharpen | — | Relaxation-pathway analysis on the offending assumption |
| Proof gap or incorrect step | proofcheck | — | Audit the affected unit; hand confirmed gaps to proof-repair |
| Repair plan needed for a confirmed gap | proof-repair | — | Generate a literature-backed, ladder-disciplined repair plan |
| Simulation does not verify the theory | theory-simulation | — | Audit mode: map each theoretical claim to a check |
| Missing proof for a stated result | proof-writer | — | Write the proof package or a blockage record |
| Notation undefined or inconsistent | stat-polishing | REVISION_PLAN.md | Apply stat-notation-audit.md |
| Figure or caption problem | stat-polishing | REVISION_PLAN.md | Apply stat-figure-design.md |
| Structure, exposition, or transitions | stat-polishing | REVISION_PLAN.md | Restructure; add inter-section transitions |
| AI-template style (em-dash, colon splices, bullet sprawl) | stat-polishing | REVISION_PLAN.md | Apply stat-style-discipline.md |
| Reproducibility gap | stat-polishing | REVISION_PLAN.md | Apply stat-reproducibility-audit.md |
| Template, format, or page-limit breach | stat-polishing | REVISION_PLAN.md | Run latex_audit.py; apply stat-venue-checklists.md |
| Main / supplement separation broken | stat-polishing | REVISION_PLAN.md | Run latex_audit.py cross-file leak check |

## Maintenance

`scripts/routing_lint.py` checks only that every owner skill and every artifact named in
this table is a real skill / known artifact. It does **not** judge whether the routing is
correct — that is human judgment, and a wrong-but-existing route passes the lint. Run the
lint after editing this table, and after renaming any skill or artifact.
