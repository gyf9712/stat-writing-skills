# Stat Skills Roadmap

Prioritized improvement list for the `stat-paper-plan`, `stat-paper-write`, `stat-paper-writing`, `stat-polishing` skill family and their shared references. Drafted 2026-05-27 from a Codex MCP review (GPT-5.4 xhigh) by a senior-statistician persona.

This file tracks improvements that were deferred from the initial Codex-review-driven fix pass. Tier A fixes were applied immediately; Tier B and Tier C are tracked here for future iteration.

## Applied in this iteration (May 2026)

The following were fixed in the same session as the Codex review:

- Corrected AOAS venue entry (typical 20 pages, supplement-as-separate, citation-of-supplement, AI disclosure VERIFY flag) in `stat-shared-references/stat-venue-checklists.md`.
- Corrected Biometrika entry (Miscellanea max 8 pages, single-anonymised, alt text, AI disclosure).
- Replaced Biostatistics subentry with a full venue block (D/C/R kite-marks, format-neutral first submission, main-to-supplement cross-references ARE expected, AI disclosure, alt text).
- Updated `MAX_PAGES` line in `stat-paper-plan/SKILL.md` to reflect corrected page norms.
- Introduced `SUPPLEMENT_MODE = separate_self_contained | linked_appendix` with venue-default mapping in `stat-paper-write/SKILL.md` and `stat-paper-plan/SKILL.md`. Removed the implicit global ban on main-to-supplement cross-references.
- Fixed malformed Agent invocations in `stat-paper-write/SKILL.md` (replaced bare-colon-block with canonical `Agent(subagent_type="general-purpose")` form).
- Added required `PRIOR_WORK_MATRIX.md` artifact step (Step 5.5) to `stat-paper-plan/SKILL.md` with column schema and novelty-risk rule.
- Added required `TECHNICAL_RISK_REGISTER.md` artifact step (Step 5.6) to `stat-paper-plan/SKILL.md` with column schema and sign-off rule.

### Follow-up iteration (May 2026, same session)

The Codex review made positioning and technical claim strength the two highest-priority unaddressed risks. The following additions address both, directly in `stat-paper-write` and `stat-polishing`:

- Created `stat-shared-references/stat-positioning-and-claims.md`. This is the centerpiece: a full protocol for the positioning audit and the technical claim strength audit, a schema for `CLAIM_SUPPORT_MAP.md`, common positioning failure modes, common claim failure modes, a Codex MCP prompt template for an independent audit, and the ordering rule that positioning and claim audits must precede style polishing.
- Added Step 2.5 to `stat-paper-write/SKILL.md`: build `CLAIM_SUPPORT_MAP.md` before drafting the front matter. Each prose claim must trace to a `PRIOR_WORK_MATRIX.md` row, a `TECHNICAL_RISK_REGISTER.md` row, and a piece of verified literature support.
- Added Step 5.5 to `stat-paper-write/SKILL.md`: post-drafting positioning and claim audit. Codex can run the independent audit for high-stakes submissions.
- Added positioning and claim audit checks to the final-checks section of `stat-paper-write/SKILL.md`.
- Elevated positioning and claim audit to a Key Rule in `stat-paper-write/SKILL.md`.
- Added a reference-table entry pointing to `stat-positioning-and-claims.md` as the first file to read in `stat-polishing/SKILL.md`.
- Restructured the `stat-polishing/SKILL.md` workflow: positioning audit and claim strength audit now come before style polishing, with the explicit warning that polishing prose on top of an overclaim makes the overclaim more confidently stated.
- Expanded the Codex prompt in `stat-polishing/SKILL.md` to perform a three-level audit (positioning + claim strength, Big Four standards and voice, line-level AI tells), in that order.
- Elevated positioning and claim audit to a Key Rule in `stat-polishing/SKILL.md`, with the literature-support requirement for comparative claims.
- Added a `Read In Full` column to the `PRIOR_WORK_MATRIX.md` schema in `stat-paper-plan/SKILL.md` to surface the most common source of overclaim: citing a paper for what the author assumes it says rather than what it actually proves.
- Linked the planning matrices to `CLAIM_SUPPORT_MAP.md` in `stat-paper-plan/SKILL.md`.

The combined effect: every positioning claim and every comparative technical claim now requires (1) a matched `PRIOR_WORK_MATRIX.md` row with the cited paper actually read in full, (2) a matched `TECHNICAL_RISK_REGISTER.md` row, (3) verified literature support recorded in `CLAIM_SUPPORT_MAP.md`, and (4) a SUPPORTED or SUPPORTED-with-qualification status before the prose can ship.

This directly addresses Codex's diagnosis that the skills had not yet protected against the two things that actually kill top-stat submissions: weak positioning and unverified technical overclaim.

## Roadmap for next iteration (priority order)

These are the items Codex identified as important but that are deferred to a future iteration rather than applied immediately.

### 1. Venue-by-venue compliance refresh with `last_checked` and sources

Add a `last_checked` date and a list of official source URLs to every venue block in `stat-venue-checklists.md`. The Biometrika, Biostatistics, and AOAS blocks now follow this pattern; bring the rest up to the same standard.

Done means: every venue block has (a) a `Last checked:` date, (b) a list of official URLs, (c) explicit `[VERIFY AT SUBMISSION]` flags for any rule that could not be confirmed.

### 2. Submission package skill

Build a new skill `stat-submission-package` covering:

- Cover letter drafting (AE-facing positioning)
- Funding statement
- Conflict-of-interest statement
- AI disclosure statement (venue-specific wording)
- Data availability statement (D/C/R-style or plain prose)
- Code availability statement
- Alt text generation for figures
- Dataset citations and persistent identifiers
- Final upload inventory

This addresses the gap between "writing finished" and "ready to submit".

### 3. PRIOR_WORK_MATRIX and TECHNICAL_RISK_REGISTER as hard gates

The matrices are now required artifacts in `stat-paper-plan` but the writing skill does not yet block on them. Next iteration: `stat-paper-write` should refuse to draft the abstract or introduction until:

- All `Novelty Risk = HIGH` rows in `PRIOR_WORK_MATRIX.md` have been resolved
- All `Severity = CRITICAL` rows in `TECHNICAL_RISK_REGISTER.md` are `CLOSED` or explicitly downgraded

### 4. Reproducibility packaging module

Beyond statements, build the actual artifacts:

- Replication script that reproduces all figures and tables from raw data
- `sessionInfo()` or equivalent output committed
- Figure provenance (which script, which seed, which data version)
- Repository checklist (README, LICENSE, data dictionary, install instructions)
- Reproducibility badge / kite-mark application support (D, C, R for Biostatistics; ACM Artifact Evaluation; etc.)

### 5. Prompt de-duplication

Move repeated style, figure, supplement, and review rules out of SKILL.md files into shared references. Currently, the four SKILL.md files repeat the same style discipline blocks, figure rules, supplement rules, and reviewer checklists. The duplication has two costs:

- Inconsistency risk when one place is updated but not the others
- AI-tell amplification when the same prescriptive blocks are repeated in instruction text

Done means: each rule lives in exactly one shared-reference file; SKILL.md files reference rules by name and section, not by re-stating them.

### 6. PDF-aware review path for figure quality

Currently the figure design rules are enforced through prose review. A PDF-aware review path would:

- Open the compiled PDF
- For each figure: check that no title is inside the figure, captions are self-contained, no legend overlaps the data, fonts are readable at journal column width
- For the bibliography: check entry types, missing fields, duplicate keys
- For page budget: count main-body pages excluding references, compare with venue norm

This requires extending the pipeline to actually open and parse PDFs.

### 7. Domain packs

Build content packs for common statistics paper classes:

- Causal inference (estimands, identification assumptions, sensitivity analysis)
- Survival / event-history (Cox model assumptions, competing risks, time-varying covariates)
- Bayesian computation (prior elicitation, MCMC diagnostics, posterior summaries)
- Missing data (mechanism notation, multiple imputation reporting)
- Spatial-temporal (model structure, covariance specification, projection)
- Longitudinal / multilevel (within/between effects, random-effects structure)
- Multiple testing (FDR vs FWER, dependent test handling)
- Semiparametric (efficient influence function, double robustness)

Each pack would contribute: a section template, an assumption checklist, a simulation DGP template, a comparison-method list.

### 8. Revision workflow

Build a `stat-revision` skill family:

- AE-facing cover letter drafting in response to a decision
- Referee-response drafting with point-by-point matrix
- Revision plan with priority order
- Tracked-changes generation and management
- Resubmission readiness check

This is parallel to but distinct from `nature-response`.

### 9. Claim-boundary auditing (partially addressed in the follow-up iteration)

Largely addressed by `stat-positioning-and-claims.md`, the `CLAIM_SUPPORT_MAP.md` artifact, and the audit steps now in `stat-paper-write` and `stat-polishing`. The remaining work for the next iteration:

- Automate the extraction of positioning and technical claims from the LaTeX source (currently a manual step).
- Build a `stat-claim-audit` slash-command skill that takes a draft and produces `CLAIM_SUPPORT_MAP.md` semi-automatically.
- Add specific detectors for theorem scope drift (abstract claims more than the theorem states), lower-bound mismatch (upper and lower bounds on different function classes), and application overclaim (prediction quality interpreted as causal effect).

### 10. Skill-level prose cleanup

The SKILL.md files themselves use em-dashes heavily, which contradicts the discipline they enforce. Targets per Codex:

- `stat-paper-plan/SKILL.md`: cut from about 94 em-dashes to at most 10
- `stat-paper-write/SKILL.md`: cut from about 64 em-dashes to at most 5
- `stat-paper-writing/SKILL.md`: cut from about 42 em-dashes to at most 5
- `stat-polishing/SKILL.md`: cut from 3 em-dashes to 0 or 1

Hard rule for next iteration: no em-dashes in any example text, template text, sample abstract, sample paragraph, sample theorem discussion, sample reviewer prompt, or sample output that the model may imitate. Soft rule: remove em-dashes from instructional prose as well.

## Honest open questions

These are points where Codex flagged uncertainty and the next reviewer should resolve them:

1. AOAS AI disclosure policy: Codex found no AOAS-specific generative-AI disclosure instruction on the official pages it checked. This may be incomplete coverage. Confirm with the journal at actual submission time and update the venue block.

2. JASA T&M and JASA ACS guidance is currently sourced from prior knowledge rather than from a 2026 reading of the ASA/Taylor & Francis pages. Refresh these against current sources.

3. JRSS-B, Statistica Sinica, EJS, Bernoulli, COLT, ALT, MSL guidance has not been independently verified against current author guidelines in this iteration. They need a refresh pass.

4. The `Default mapping` for `SUPPLEMENT_MODE` was set based on Codex's reading. Biostatistics, COLT, and ALT are `linked_appendix`; everything else is `separate_self_contained`. Confirm at submission time.

## Codex review log

The full Codex MCP dialogue that produced this roadmap is summarized below. Save the threadId (`019e6aea-0a6e-7dd1-9e8b-341e96e6a86e` for the May 2026 review) for resumability.

### Round 1: top-line verdict

> These skills are useful, not decorative. They are strongest for late-stage methodology and application papers, especially AOAS and JASA ACS, where section weighting, EDA emphasis, findings-first framing, and prose discipline matter a lot. They are also useful for Big Four theory papers once the math and novelty are already settled.
>
> They are not a trustworthy end-to-end submission system in their current form. They do not yet protect the user against the two things that actually kill top-stat submissions: weak positioning and unverified technical overclaim. If used as autopilot, they will produce polished risk.

### Top issues raised in Round 1

1. No mandatory novelty/positioning audit (addressed in this iteration via `PRIOR_WORK_MATRIX.md`).
2. Venue layer is partly wrong and too coarse (AOAS, Biometrika, Biostatistics fixed in this iteration; others in next).
3. Supplement policy is over-absolute and internally inconsistent (addressed via `SUPPLEMENT_MODE`).
4. The family lacks a technical-risk layer (addressed via `TECHNICAL_RISK_REGISTER.md`).
5. The orchestrator is too eager for high-stakes work (`AUTO_PROCEED=true` while `REVIEW_MODE=both`); not yet changed.

### Round 2: actionable specifications

Codex provided exact replacement text for the venue entries, the `SUPPLEMENT_MODE` constant, the canonical Agent invocation syntax, and the schemas for `PRIOR_WORK_MATRIX.md` and `TECHNICAL_RISK_REGISTER.md`. All of these were applied in this iteration.

Codex also noted: "stat-polishing models the intended discipline best. The family as a whole does not." This points to the prose cleanup roadmap item.

Sources Codex checked (May 27, 2026):
- AOAS manuscript submission: https://imstat.org/journals-and-publications/annals-of-applied-statistics/annals-of-applied-statistics-manuscript-submission/
- AOAS supplement instructions: https://imstat.org/journals-and-publications/annals-of-applied-statistics/annals-of-applied-statistics-supplement-instructions/
- AOS manuscript preparation: https://imstat.org/journals-and-publications/annals-of-statistics/annals-of-statistics-manuscript-preparation/
- AOS supplement instructions: https://imstat.org/journals-and-publications/annals-of-statistics/annals-of-statistics-supplement-instructions/
- Biometrika author guidelines: https://academic.oup.com/biomet/pages/General_Instructions
- Biostatistics author guidelines: https://academic.oup.com/biostatistics/pages/general_instructions
- Biostatistics supplementary data page: https://academic.oup.com/biostatistics/pages/supp_data

## Versioning

When applying items from this roadmap, mark them as moved from `Roadmap for next iteration` to `Applied in this iteration`, and rebuild the open-items list for the iteration after.
