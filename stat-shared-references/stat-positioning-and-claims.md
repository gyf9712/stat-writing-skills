# Positioning and Technical Claims with Literature Support

Use this reference whenever drafting or polishing the abstract, introduction, contribution list, problem-setup-vs-prior-work paragraph, theorem statements, related work, or discussion of a statistics paper.

Two things kill submissions at JASA, Annals of Statistics, JRSS-B, Biometrika, AOAS, JASA ACS, and similar venues more often than any other problem:

1. The paper is positioned weakly relative to an existing close paper.
2. The technical claims are stronger than the evidence and the literature actually support.

Both problems are largely preventable. They require literature work, not better prose. This reference describes how to do that literature work as part of writing and polishing.

## When to Read

- Before drafting the abstract, introduction, or contribution list
- Before drafting a theorem statement that uses comparative language ("first", "weaker assumptions than", "improves the rate from X to Y")
- During the polishing pass on the front matter
- When the Codex external review flags overclaim or weak positioning
- When responding to a reviewer who challenges novelty or claim strength

## The Two Audits

### Positioning Audit

Goal: ensure that every positioning claim in the prose is consistent with the closest existing work.

A positioning claim is any sentence that places the paper relative to the literature. Examples:

- "We are the first to ..."
- "In contrast to existing methods that require X, we ..."
- "Unlike [Smith and Jones, 2023], our framework ..."
- "We close the gap left open by [Zhou et al., 2024]."
- "Existing approaches do not address ..."
- "To the best of our knowledge, this is the first ..."

Every positioning claim is a literature claim. If the claim is wrong, a reviewer who knows the field will catch it immediately. The audit is therefore non-optional.

### Technical Claim Strength Audit

Goal: ensure that every technical claim is correctly described in comparative terms.

A technical claim is any sentence describing a formal property of the paper's contribution. Examples:

- "Our estimator achieves the minimax rate O(n^{-2s/(2s+d)})."
- "Under weaker moment conditions than [Smith, 2023]."
- "The bound is tight up to logarithmic factors."
- "We require only a fourth-moment condition; prior work assumed sub-Gaussianity."
- "Our algorithm runs in O(np log n) time, faster than the O(n^2 p) of [Jones, 2022]."
- "Asymptotically efficient in the semiparametric sense of Bickel et al. (1993)."

Each of these makes a verifiable claim about prior work. If `Smith 2023` actually required sub-exponential (not sub-Gaussian), or `Jones 2022` actually runs in O(np^2), or the cited efficiency notion does not apply to this estimand, the claim is overclaim and the paper will be rejected for it.

## The Workflow

The positioning and claim audits are a single workflow with two outputs: a verified `CLAIM_SUPPORT_MAP.md` and revisions to the underlying `PRIOR_WORK_MATRIX.md` and `TECHNICAL_RISK_REGISTER.md`.

### Step 1: Extract every claim from the front matter

Read the abstract, introduction, contribution list, problem-setup-vs-prior-work paragraph, theorem statements, related work, and discussion. List every positioning claim and every technical claim verbatim.

For each claim, classify:

- Type: positioning, technical, or both
- Location: section and paragraph
- Strength: comparative (against named prior work) or absolute (no reference frame)

If a comparative claim has no reference frame, that is itself a problem. Either name what is being compared with, or weaken the claim. "Achieves a fast rate" without saying fast compared to what is not publishable language.

### Step 2: Map each claim to backing artifacts

For each claim, identify which row of `PRIOR_WORK_MATRIX.md` and which row of `TECHNICAL_RISK_REGISTER.md` backs it. If the matrix or register does not contain a backing row, add one.

Build the `CLAIM_SUPPORT_MAP.md` table:

```md
# CLAIM_SUPPORT_MAP

| Claim ID | Verbatim Claim | Section | Type | Backing PW Rows | Backing TR Rows | Literature Support | Verified | Status |
|----------|----------------|---------|------|-----------------|-----------------|--------------------|----------|--------|
| CS1 | "We are the first to establish a minimax-optimal rate for sparse generalized linear models under heavy-tailed predictors." | abstract; §1 contributions | positioning + technical | PW3, PW4 | TR1, TR2 | Smith 2023 (sub-G only), Zhou 2024 (bounded design only), Negahban et al. 2012 (light-tail) | yes | SUPPORTED |
| CS2 | "Our estimator achieves the rate (s log p / n)^{1/2} up to log factors." | §3 Theorem 1 | technical | -- | TR1 | own proof; matches Wainwright 2019 Chap 7 form | yes | SUPPORTED |
| CS3 | "Our assumptions are weaker than those in [Smith 2023]." | §2 Remark 2; §1 contribution 2 | positioning + technical | PW3 | TR3 | Smith 2023 Assumption (A2): sub-Gaussian noise + bounded fourth moment of design; ours: bounded fourth moment of noise + bounded fourth moment of design | yes | SUPPORTED with qualification (weaker on noise, same on design) |
| CS4 | "To the best of our knowledge, no existing method handles both heavy-tailed predictors and heavy-tailed responses simultaneously." | §1 contribution 3 | positioning | PW5, PW6 (need to add) | -- | not yet searched | no | UNVERIFIED |
```

Columns:

- `Claim ID`: stable identifier (CS for claim).
- `Verbatim Claim`: exactly what the prose says, in quotation marks.
- `Section`: which section and which sentence.
- `Type`: positioning, technical, or both.
- `Backing PW Rows`: rows in `PRIOR_WORK_MATRIX.md` this claim depends on.
- `Backing TR Rows`: rows in `TECHNICAL_RISK_REGISTER.md` this claim depends on.
- `Literature Support`: specific references and what they actually say (not just citations; one-sentence summary of the relevant claim in each reference).
- `Verified`: whether the literature support has been read and confirmed, not just cited.
- `Status`: SUPPORTED, SUPPORTED with qualification, NEEDS WORK, OVERCLAIMED, UNVERIFIED.

### Step 3: Literature search for unverified claims

For any claim with `Status = UNVERIFIED` or for any claim where the supporting `PRIOR_WORK_MATRIX` row's `Citation Verified` is not yes, run a literature search.

Search strategy:

1. Start with the closest paper from `PRIOR_WORK_MATRIX.md` and follow its forward citations through Semantic Scholar (use the `/semantic-scholar` skill or `arxiv` skill where applicable).
2. Search for the specific claim language: "minimax sparse GLM heavy-tail", "robust regression sub-exponential design", etc. Use precise terms, not generic ones.
3. Check at least three sources: Semantic Scholar, arXiv, and DBLP. For statistics papers, also check MathSciNet when accessible.
4. Read the abstracts of the top candidates; read the relevant section of any paper whose abstract looks close.
5. Record what you found in the Literature Support column.

If the search returns no close prior work, the claim "first to" is plausible but still subject to risk. Note in `Status` as SUPPORTED with the qualification "no close prior work identified by [date]" and reduce the strength of language slightly: "to the best of our knowledge" rather than "we are the first to".

If the search returns prior work that already does what the paper claims, the claim is OVERCLAIMED. Either:

- Reposition: find the actual delta from this newly identified prior work and use that as the contribution, or
- Weaken: change "we are the first to" to "we provide a [different angle] on", citing the prior work, or
- Drop: remove the contribution if the delta is too small to support.

### Step 4: For technical claims, verify the comparative claim

For technical claims that say "weaker assumptions than X", "faster rate than Y", "improves upon Z", do the following:

1. Get the exact statement and conditions from the cited paper. Read the theorem, not just the abstract.
2. Compare line by line.
3. Note where the new paper is genuinely better, where it is comparable, and where it is worse.

If the comparison is mixed, the claim must be qualified. Example:

```
Smith (2023, Theorem 2) requires sub-Gaussian noise and a beta-min condition.
Our Theorem 1 requires fourth-moment noise and the same beta-min condition.
Status: SUPPORTED with qualification (weaker on noise, identical on signal strength).
Prose: "We weaken Smith (2023)'s sub-Gaussian noise condition to a bounded
fourth moment, at the cost of an additional log factor in the rate."
```

The qualification belongs in the prose, not hidden in the appendix. Stating it openly is a strength.

### Step 5: For overclaimed claims, draft replacement language

Every OVERCLAIMED claim needs a specific replacement. Options:

- Soften the verb: "establishes" becomes "provides", "proves the first" becomes "to the best of our knowledge, the first".
- Add a qualification: "under conditions (A1)-(A3)" or "for the specific regime where ...".
- Cite the contradicting paper and reposition: "Smith (2023) addresses [X]; we address [Y, distinct from X]."
- Drop and rewrite: remove the claim entirely and rebuild the contribution around what is actually new.

For each overclaim, the audit output must include both the original prose and a proposed replacement. Do not leave a "TODO: fix overclaim" comment.

### Step 6: For UNSUPPORTED claims, decide remediation

A claim can be UNSUPPORTED for three reasons:

1. The supporting work has not been done yet (simulation, real-data analysis, additional theorem). Add to `TECHNICAL_RISK_REGISTER.md` as `Status = OPEN` and downgrade the claim until the work is done.
2. The supporting literature exists but was not searched. Go back to Step 3.
3. The claim is actually wrong. Remove it.

### Step 7: Save and link the artifacts

`CLAIM_SUPPORT_MAP.md` is the centerpiece of the audit. It lives in the project root alongside `PRIOR_WORK_MATRIX.md` and `TECHNICAL_RISK_REGISTER.md`.

The matrices are cross-linked. Editing one usually requires touching the others. Treat them as a connected set.

When the paper is submitted, archive the `CLAIM_SUPPORT_MAP.md` snapshot alongside the submission. If a reviewer challenges a claim, this map is the response.

## Literature Search Tools

Use the existing skill ecosystem.

- `/arxiv` for preprint search and download
- `/semantic-scholar` for forward and backward citation traversal, abstract retrieval, TLDR
- `/research-lit` for synthesis across multiple papers
- `/novelty-check` for the focused question "has this been done"
- `mcp__codex__codex` for a senior-statistician opinion on positioning gaps when search alone is inconclusive

For statistics-specific searches:

- MathSciNet is the canonical source for mathematical statistics; if accessible, prefer it over Semantic Scholar for theorem-level matching.
- DBLP indexes computer science and statistics conferences; useful for COLT, ALT, NeurIPS-style theory.
- Project Euclid hosts IMS journals (AoS, EJS, Bernoulli, AOAS).
- Wiley Online Library hosts JRSS-B, Statistics in Medicine.

When in doubt about a recent paper from the last two years, ask Codex with `mcp__codex__codex` and a specific question; senior-statistician judgment fills the gap when search returns nothing close.

## Common Positioning Failure Modes

The Codex review of a fresh draft tends to surface the same set of failure modes. Watch for them in your own writing.

| Failure mode | Diagnostic | Fix |
|--------------|------------|-----|
| The closest paper is not cited | A senior reader thinks "but isn't this just an extension of [X]?" | Cite X, state the delta from X, add X to PRIOR_WORK_MATRIX |
| "Existing methods do not address" without naming any | Empty reference frame | Name the methods and explain why each is insufficient |
| Claim of "first" without forward-citation check | Recent paper does the same thing | Forward-search the closest paper, restate as "to the best of our knowledge" or reposition |
| "Weaker assumptions" without listing what is weaker | Reviewer expects line-by-line comparison | Add a remark or table comparing each assumption |
| "Improves the rate from O(X) to O(Y)" without checking constants | Constants may favor prior work | State the constant dependence or restrict the claim to rate order |
| Closing the loop on a problem that no one was working on | Reviewer says "so what?" | Reframe to make the gap matter; cite the audience that cares |
| Two contributions that are actually one | Reviewer says "padded" | Merge into one well-supported contribution |
| Contribution list does not match what the paper proves | Abstract and theorems disagree | Rewrite contribution list to match theorems exactly |

## Common Technical Claim Failure Modes

| Failure mode | Diagnostic | Fix |
|--------------|------------|-----|
| "Minimax optimal" without matching lower bound | Theorem 2 is only upper bound | Either prove a lower bound, cite one, or replace "optimal" with "rate-adaptive" |
| "Tight" without proof of tightness | Constants might be loose | Replace with "achieves rate O(...)"; explicit tightness requires a matching lower bound |
| "Efficient" without specifying efficiency notion | What kind of efficiency? | Specify: information-theoretic, semiparametric (Bickel et al. 1993 sense), asymptotic relative efficiency to a named comparator |
| "Robust" without specifying what is being broken | Robust to what? | Specify: heavy tails, outliers, model misspecification, label noise. Cite the formal notion. |
| "Adaptive" without saying to what | Adaptive to smoothness? Sparsity? Both? | Specify the adaptive set; cite the adaptive estimation framework used |
| "Faster" without computational benchmark | Faster in what sense? | Specify: asymptotic complexity, wall-clock at specific n and p, or sample complexity |
| "Generalizable" without showing generalization | Vague | Replace with "we extend to setting X (Theorem 3)" or similar |
| "Significant" used in a non-statistical sense | Ambiguity | Use "important", "substantial", "noticeable"; reserve "significant" for hypothesis tests |
| Claim references a notion that does not apply | E.g., semiparametric efficiency for a parametric setting | Remove the claim or apply the right notion |

## Codex Integration for the Audit

The audit is well-suited to a Codex MCP call because Codex (GPT-5.4 xhigh) can independently bring positioning and claim-strength judgments. Use this prompt template:

```yaml
mcp__codex__codex:
  model: gpt-5.4
  sandbox: read-only
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a senior statistician serving as Associate Editor for [VENUE].

    Below is a manuscript section and the supporting artifacts:
    (a) the prose to audit
    (b) PRIOR_WORK_MATRIX.md
    (c) TECHNICAL_RISK_REGISTER.md (if present)
    (d) CLAIM_SUPPORT_MAP.md draft (if present)

    [paste each artifact]

    Please perform a positioning audit and a technical claim strength audit.

    (1) Positioning audit. For each positioning claim in the prose
        (sentences that place the paper relative to literature),
        evaluate:
        - Is the closest existing work cited?
        - Is the delta stated correctly?
        - Are there obvious recent papers (last 2-3 years) that may
          be missing?
        - For any "first to" or "only" claim, is it plausibly true?
        Flag specific quoted sentences as SUPPORTED, OVERCLAIMED,
        UNVERIFIED, or MISSING REFERENCE FRAME.

    (2) Technical claim strength audit. For each technical claim
        (statements about rates, bounds, assumptions, efficiency,
        complexity), evaluate:
        - Is the claim consistent with what the theorem actually proves?
        - For comparative claims, is the comparison correct against
          the closest prior work named?
        - For "minimax optimal" / "efficient" / "tight" / "robust"
          / "adaptive" claims, is the technical notion specified
          and applied correctly?
        Flag specific quoted sentences.

    (3) For each OVERCLAIMED or UNVERIFIED claim, write a concrete
        proposed replacement sentence that the author can paste into
        the manuscript. The replacement must keep the contribution
        visible but bring it within what the evidence and the
        literature support.

    (4) Suggest specific papers (with full citations, your confidence
        level for each) that the author may have missed. Distinguish
        "definitely should be cited" from "worth checking".

    (5) Score the front matter on positioning strength (1-10) and on
        claim strength (1-10), with the binding constraint named.

    Be ruthless. The job of this audit is to surface what a critical
    reviewer would notice on first read.
```

Follow-up calls with `mcp__codex__codex-reply` can target specific claims:

- "For claim CS4, please search your memory for the closest 2024-2026 papers on `[topic]`. Confidence on each."
- "Please write the exact replacement for the contribution-list bullet that says `[overclaim]`."

## How Positioning and Claims Differ from the Style Pass

The style pass (`stat-style-discipline.md`) fixes punctuation, AI-template patterns, voice. It does not check whether claims are true.

The positioning and claims pass fixes the substance of what the paper says. It should run before the style pass. Polishing punctuation on an overclaim does not make it correct; it makes the overclaim more confidently stated.

Order of operations during polishing:

1. Positioning audit (this file)
2. Technical claim strength audit (this file)
3. Section logic and structure (`stat-writing-principles.md`)
4. Theorem statement precision (`stat-theory-writing.md`)
5. Style discipline (`stat-style-discipline.md`)
6. Figure design (`stat-figure-design.md`)
7. Venue conformance (`stat-venue-checklists.md`)

Doing them in reverse usually produces a polished overclaim.

## Author Sign-Off

Before the paper is submitted, the author must sign off on the `CLAIM_SUPPORT_MAP.md`. Sign-off means:

- Every claim with `Type = positioning` has at least one backing PW row and a literature support note.
- Every claim with `Type = technical` has a backing TR row or a derivation in the paper.
- No claim has `Status = OVERCLAIMED` or `Status = UNVERIFIED`.
- All claims with `Status = SUPPORTED with qualification` have the qualification in the prose, not buried elsewhere.

If those conditions fail, do not submit.
