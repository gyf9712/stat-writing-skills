---
name: stat-mock-review
description: Produce an Associate-Editor-style pre-submission mock review for a statistics manuscript targeting the Big Four journals (JASA, Annals of Statistics, JRSS-B, Biometrika) and similar venues (AOAS, EJS, Bernoulli, Statistica Sinica, Biostatistics, JCGS, COLT, ALT). The skill simulates the first read an AE gives a submission and produces a structured report covering synopsis, fatal concerns, major concerns, minor concerns, venue-fit risk, the likely initial editorial action (desk reject / send out / reject after review / major revision / minor revision), and a rescue plan. Unlike conference reviewer simulators, this skill does not assign a 1-10 numerical rating; journal editors do not work in that idiom. Use when the author wants a single-shot self-assessment of submission readiness before invoking the iterative Codex dialogue or before submitting.
version: 1.0.0
author: stat-skills, derived from senior-statistician AE practice
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# AE-Style Pre-Submission Mock Review

## Purpose

Produce one structured artifact, `MOCK_REVIEW.md`, that simulates the read an Associate Editor gives a submission before deciding to desk-reject, send out for review, or invite a major revision. The output is opinionated, terse, and oriented to editorial action, not to a numerical score.

This skill is complementary to, not a replacement for, `stat-polishing` and the iterative Codex MCP dialogue:

- `stat-polishing` improves prose and structure across rounds.
- The Codex MCP dialogue (`stat-codex-dialogue.md`) is a multi-turn senior-reviewer conversation, with three outcomes per criticism (accept, push back, log disagreement).
- `stat-mock-review` is a single-shot pre-submission verdict, written in the editorial voice. It answers: "If I sent this in tomorrow, what would the AE do?"

## When to Use

- After the manuscript is feature-complete and the figures are final
- After `stat-polishing` has run at least one full round
- Before invoking the Codex iterative dialogue for an extended polish, to decide whether the manuscript is in the right ballpark
- One to two weeks before the planned submission date, with enough lead time to act on the verdict
- When the author wants a single-document, shareable assessment for coauthors

Do not run this skill on a half-finished draft. The mock review is calibrated for submission-ready manuscripts; running it on a draft that has not been polished produces noise.

## Output: MOCK_REVIEW.md

The file has seven sections in fixed order. Brevity is the discipline; an AE writes screening notes in fifteen minutes, not a referee report in a week.

```markdown
# MOCK_REVIEW.md

Target venue: [JASA T&M / JASA ACS / AOS / JRSS-B / Biometrika / AOAS / Bernoulli / EJS / Statistica Sinica / Biostatistics / JCGS / COLT / ALT]
Paper type: [theory / methodology / application]
Manuscript: [title]
Reviewer: AE-style mock review, single pass
Date: [YYYY-MM-DD]

## 1. Synopsis

One paragraph (three to five sentences). State the central claim, the technical contribution, and the evidence the paper offers. No evaluation in this section; only the description that the AE would write in their internal notes.

## 2. Fatal Concerns

Issues that would cause a desk reject or a reject without revision invitation. Each item is one sentence. If there are none, write `None identified.` Do not invent fatal concerns to fill the section.

Typical fatal patterns:
- Out of scope for the venue
- Central claim not supported by the theorem or simulation evidence
- Mathematical error in the headline result
- Prior work that anticipates the contribution and is not cited
- Result that is correct but not statistically interesting at the venue's level

## 3. Major Concerns

Issues that would not cause desk reject but would dominate the referee report. Each item: one sentence diagnosis, one sentence recommendation. Order by severity. Aim for three to six items; fewer if the manuscript is strong, more only if the manuscript needs structural work.

Typical major patterns:
- Assumption set restrictive enough that the result does not engage with the practical regime
- Simulation evidence that does not verify the assumed regime
- Application section that does not demonstrate the method's value over existing practice
- Positioning that overstates the delta against the closest prior work
- Notation drift between body and supplement

## 4. Minor Concerns

Items the referees will flag but that do not block acceptance. Each item is one short sentence. Group into bullets. These are line-level: clarity, citation completeness, figure quality, presentation. Cap at ten items; if there are more than ten minor items, the manuscript should go back to `stat-polishing` rather than to submission.

## 5. Venue-Fit Risk

One paragraph. Does the paper match the venue's voice, weight, and audience? Compare with one to three recent papers from the venue (last 1-2 years, same paper type) and name them. State whether the paper is in the venue's normal range or sits at the edge. If the venue is not the right home, name a better fit.

## 6. Likely Initial Editorial Action

Choose one and state the reasoning in one to two sentences. Do not assign a numerical rating.

- `Desk reject` — fundamental fit, scope, or correctness issue; AE returns without sending for review.
- `Reject without invitation to resubmit` — the paper was sent out and the result is irrecoverable; rare at the desk stage but possible.
- `Major revision likely` — sent out, expected to come back with substantial referee work; the rescue plan should target the things that would tip this toward acceptance.
- `Minor revision likely` — sent out, expected to need only line-level revision; rare for a first-time submission and a strong signal of a polished manuscript.
- `Reject and resubmit elsewhere` — the paper is well executed but the venue is wrong; the synopsis section's better-fit recommendation applies.

## 7. Rescue Plan

A focused list of what to change before submission, in priority order. Three to seven items. Each item:

- `Problem`: one sentence diagnosis
- `Action`: one sentence, concrete and bounded
- `Effort`: small / medium / large
- `Recoverability`: high (presentation issue, fixable in one session) / medium (requires new analysis or rewriting a section) / low (structural; the contribution itself needs reframing)

The rescue plan is the actionable output. Everything before it is justification.
```

## Workflow

### Step 1: Read the manuscript end-to-end

Read the abstract, introduction, methodology, theorems, simulations, application section, and discussion in order. Take notes on three things only:

1. The contribution as stated in the abstract and the contribution list.
2. The strongest piece of evidence the paper offers for that contribution.
3. The boundary the paper draws (what it does not claim).

Do not edit, do not annotate, do not check citations on this pass. The job is to form the AE's first impression.

### Step 2: Identify the target venue and recent comparable papers

Read `../stat-shared-references/stat-venue-checklists.md` for the target venue. Identify one to three recent papers from the venue (last 1-2 years, same paper type) and skim their abstracts and introductions. The mock review compares this manuscript with those papers, not with a generic Big Four standard.

### Step 3: Run the positioning and claim audit

Read `../stat-shared-references/stat-positioning-and-claims.md`. Extract the positioning and technical claims from the abstract, introduction, and contribution list. Flag each as `SUPPORTED`, `OVERCLAIMED`, `UNVERIFIED`, or `MISSING REFERENCE FRAME`. Any `OVERCLAIMED` claim in the abstract or introduction promotes its issue to Section 2 (fatal) or Section 3 (major) of the report.

For every claim that names a specific theorem or rate of a cited paper, resolve it to the project's `papers/<project>/cited_results.lock.md` and the global literature cache. Schema and protocol in `../stat-shared-references/citation-purpose-protocol.md` (gate matrix) and the sibling `stat-theory-skills` `literature-cache-protocol.md` router. A fatal-or-major mock-review concern that depends on a specific theorem requires `independently_checked` verification floor; a lower state demotes the concern to a verification-request pending item rather than a load-bearing finding.

This step is **read-only** with respect to the lock manifest. The mock review does not append rows. If a fatal-or-major concern references a citation site not yet in the lock manifest, that itself is flagged as a gap requiring the upstream skill (stat-paper-write or proof-repair) to add the row before submission. The mock-review report's Rescue Plan (Section 7) lists missing lock entries as `Effort: small / Recoverability: high` items.

### Step 4: Write the seven sections in order

Write Section 1 (Synopsis) first; this anchors the rest of the report. Then Sections 2 through 5 in order. Section 6 (likely action) and Section 7 (rescue plan) come last and follow from the preceding diagnosis.

Discipline:
- No emphasis formatting (no manual bold, no italics). Use the section structure to convey priority.
- No 1-10 ratings. The editorial action verb does the work.
- No hedging. An AE-style note is direct.
- No advice that is not actionable in one to two weeks.

### Step 5: Reconcile with `CLAIM_SUPPORT_MAP.md` and `PRIOR_WORK_MATRIX.md`

If the project has these artifacts from `stat-paper-plan` and `stat-paper-write`, cross-check Section 2 and Section 3 against them. A `Severity = CRITICAL` row in `TECHNICAL_RISK_REGISTER.md` that is still open is automatically a fatal concern. A `Novelty Risk = HIGH` row in `PRIOR_WORK_MATRIX.md` that is not yet defused is automatically a major concern.

### Step 6: Optional Codex second-pass

For high-stakes submissions, send `MOCK_REVIEW.md` and the manuscript to Codex MCP for an independent AE-style verdict. Use `model_reasoning_effort: xhigh`. The prompt should ask Codex to write its own Sections 2, 3, 6, and 7 without seeing the author's version; agreement between the two versions is the signal.

The Codex pass follows the dialogue principle in `../stat-shared-references/stat-codex-dialogue.md`. The verdict is not Codex's to dictate; the author evaluates each Codex concern and decides accept, push back, or log disagreement.

### Step 7: Use the rescue plan

The rescue plan in Section 7 is the action artifact. Implement the high-recoverability items first (presentation, citation completeness, claim wording). Medium-recoverability items go to the next polish iteration. Low-recoverability items prompt a venue change or a structural rewrite; do not bury them as minor.

## When Not to Run This Skill

- The manuscript is still in draft and has not been polished. Run `stat-polishing` first.
- The author wants a referee-style report rather than an AE-style screening. The two are different artifacts; this skill produces the latter.
- The author wants an iterative dialogue rather than a single verdict. Use the Codex MCP dialogue directly through `stat-polishing` or `stat-paper-writing`.
- The target is a conference (NeurIPS, ICLR, ICML, COLT, ALT). For COLT and ALT the AE-style framing still applies; for NeurIPS-style venues a different skill family is more appropriate.

## Why No Numerical Rating

Conference reviewer simulators output a 1-10 score because conferences aggregate scores across reviewers. Journal editors do not aggregate scores. The decision an AE makes is a verb (desk reject, send out, invite revision), not a number. Producing a `7/10` from this skill would feel familiar to ML readers but would mislead statistics authors about the editorial process. The skill stays in the editorial idiom on purpose.

## Output Discipline

- One file: `MOCK_REVIEW.md` in the project root.
- No companion files; the rescue plan is in Section 7.
- Plain text, no manual bold or italics (the headings carry structure).
- Captions, theorem statements, and quoted text from the manuscript are reproduced verbatim, not paraphrased.
- The mock review is dated; it is a snapshot, not a living document.

## Key Rules

- The AE voice is direct and terse. Do not soften, do not flatter, do not pad.
- The 1-10 rating is forbidden. Use the editorial action verb.
- The rescue plan is the deliverable. Everything before it justifies the action.
- Fatal concerns are rare; do not invent one to fill the section.
- The verdict should be calibrated against the named recent venue papers, not against a generic standard.
- Run this skill once per submission cycle, not iteratively. For iterative work use `stat-polishing` and the Codex dialogue.
