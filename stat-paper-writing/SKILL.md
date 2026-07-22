---
name: stat-paper-writing
description: "Full statistics paper writing pipeline. Supports theory, methodology, and application paper types. Orchestrates stat-paper-plan → paper-figure → stat-paper-write → paper-compile → auto-paper-improvement-loop with optional Codex MCP external review. Produces a polished statistics, applied statistics, or ML theory paper. Use when user says \"统计论文全流程\", \"stat paper pipeline\", \"statistics paper writing\", \"统计应用论文全流程\", \"application paper pipeline\", \"write stat paper pipeline\", or wants the complete statistics paper workflow for AoS, JASA T&M, JASA ACS, AOAS, JRSS-B, Biometrika, Bernoulli, EJS, Statistica Sinica, Biostatistics, JCGS, COLT, or ALT."
argument-hint: [narrative-report-path-or-topic]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# Statistics Paper Writing Pipeline

Orchestrate a complete statistics, applied statistics, or ML theory paper writing workflow for: **$ARGUMENTS**

## Overview

This skill chains sub-skills into a single automated pipeline:

```
/stat-paper-plan → /paper-figure → /stat-paper-write → /paper-compile → /auto-paper-improvement-loop
    (outline)        (plots)         (LaTeX)              (build PDF)       (review & polish ×2)
```

Each phase builds on the previous one's output. The final deliverable is a polished `paper/` directory with LaTeX source, supplement, and compiled PDF.

The improvement loop uses `/stat-polishing` standards internally to enforce Big Four-style writing (JASA, AoS, JRSS-B, Biometrika): punctuation discipline, AI-template removal, COPSS-style scholar voice, figure design rules, and main-supplement separation. After the pipeline completes, the user can also invoke `/stat-polishing` directly on specific sections that need further refinement.

## Constants

- **VENUE = `AOS`** — Target venue. Options:
  - **Theory/methodology**: `AOS`, `JASA`, `JRSSB`, `BIOMETRIKA`, `BERNOULLI`, `EJS`, `STATSINICA`, `MSL`
  - **Application**: `AOAS`, `JASA_ACS` (alias `JASA_APP`), `BIOSTATISTICS`, `STATMED`, `JCGS`, `JABES`
  - **ML theory conferences**: `COLT`, `ALT`
- **PAPER_TYPE = `auto`** — `theory`, `methodology`, `application`, or `auto`.
- **MAX_IMPROVEMENT_ROUNDS = 2** — Number of review→fix→recompile rounds.
- **CLAUDE_REVIEWER_MODEL = `claude-opus-4-6`** — Claude subagent model for fast internal reviews in each phase.
- **CODEX_REVIEWER_MODEL = `gpt-5.6`** — External LLM for Codex MCP reviews at `model_reasoning_effort: xhigh`.
- **REVIEW_MODE = `both`** — Options: `claude` (fast), `codex` (deep), `both` (Claude every round, Codex on final round). Default `both`. Passed through to plan/write/polish sub-skills.
- **AUTO_PROCEED = true** — Auto-continue between phases. Set `false` to pause after each phase.
- **HUMAN_CHECKPOINT = false** — When `true`, improvement loop pauses after each round's review.

> Theory example: `/stat-paper-writing "NARRATIVE_REPORT.md" — venue: AOS, paper type: theory`
> Methodology example: `/stat-paper-writing "NARRATIVE_REPORT.md" — venue: JASA, paper type: methodology, human checkpoint: true`
> Application example (AOAS): `/stat-paper-writing "APPLICATION_REPORT.md" — venue: AOAS, paper type: application`
> Application example (JASA ACS): `/stat-paper-writing "APPLICATION_REPORT.md" — venue: JASA_ACS, paper type: application`
> COLT example: `/stat-paper-writing "NARRATIVE_REPORT.md" — venue: COLT`

## Inputs

This pipeline accepts one of:

1. **`NARRATIVE_REPORT.md`** (best for theory/methodology) — research narrative with theorems, proofs, simulations, results
2. **`APPLICATION_REPORT.md` + `DATA_DESCRIPTION.md`** (best for application papers) — analysis narrative with dataset description, EDA, scientific findings, validation
3. **Theorem statements + simulation results** — the skill will help structure a theory/methodology paper
4. **Dataset + analysis pipeline + scientific findings** — the skill will help structure an application paper
5. **Existing `PAPER_PLAN.md`** — skip Phase 1, start from Phase 2

The more detailed the input, the better the output:
- For theory/methodology: theorem statements, proof outlines, simulation designs, quantitative results
- For application papers: dataset details (source, size, variables, time period), EDA findings, statistical challenges, comparison methods used by domain practitioners, substantive scientific findings, validation strategy, domain interpretation

## Pipeline

### Phase 1: Paper Plan

Invoke `/stat-paper-plan` to create the structural outline:

```
/stat-paper-plan "$ARGUMENTS"
```

**What this does:**
- Parse input for theorems, claims, evidence, and assumptions
- For application papers: also parse dataset details, scientific question, statistical challenges, findings, validation strategy
- Build matrices:
  - **Theorems-Evidence Matrix** and **Claims-Evidence Matrix** (all paper types)
  - **Findings-Evidence Matrix** and **Data-Challenges Matrix** (application papers)
- Determine paper type (theory / methodology / application)
- Design section structure (5-9 sections, with application papers using the 7-section data-first layout)
- Plan assumption organization (lighter for application papers)
- Plan simulation studies (informed by real data for application papers)
- Plan figures and tables (EDA figures emphasized for application papers)
- Scaffold citations (statistical + domain literature for application papers)
- Claude subagent reviews for completeness

**Output:** `PAPER_PLAN.md` with section plan, matrices, figure plan.

**Checkpoint (theory/methodology):**

```
Paper plan complete:
- Title: [proposed title]
- Type: [theory/methodology]
- Venue: [venue]
- Main theorems: [N]
- Assumptions: [N] ((A1)-(AN))
- Sections: [N] ([list])
- Figures: [N] auto + [M] manual
- Simulations: [N] DGPs × [M] methods

Shall I proceed with figure generation?
```

**Checkpoint (application paper):**

```
Application paper plan complete:
- Title: [proposed title]
- Type: application
- Venue: [AOAS/JASA_ACS/Biostatistics/etc.]
- Scientific question: [one-line summary]
- Dataset: [name, size, time period]
- Statistical challenges identified: [N]
- Main theorems (light): [1-2 max]
- Sections: [N] ([list, with §6 Application as centerpiece])
- EDA figures planned: [N]
- Application figures planned: [N]
- Simulation DGPs (real-data-informed): [N]
- Comparison methods (incl. domain-standard): [N]
- Substantive findings preview: [N findings]

Shall I proceed with figure generation?
```

### Phase 2: Figure Generation

Invoke `/paper-figure` to generate data-driven plots and tables:

```
/paper-figure "PAPER_PLAN.md"
```

**What this does:**
- Read figure plan from PAPER_PLAN.md
- Generate matplotlib/seaborn/ggplot plots:
  - **For theory/methodology papers**:
    - Convergence rate verification (log-log plots)
    - Method comparison (box plots, tables)
    - Coverage probability plots
    - Power curves
    - Rate comparison tables
  - **For application papers** (additionally):
    - EDA figures (data distributions, dependence structure, missingness, time series)
    - Descriptive statistics tables
    - Application main analysis figures (model fits, parameter estimates with CI)
    - Comparison with domain-standard methods
    - Validation plots (holdout, calibration, CV)
    - Sensitivity analysis figures
- Generate LaTeX comparison tables
- Create `figures/latex_includes.tex` (and `latex_includes_eda.tex` for application papers)

**Statistics-specific figure requirements:**
- Log-log plots for rate verification must include theoretical rate line
- Simulation tables must include standard errors
- Confidence interval coverage plots should include nominal level line
- Box plots or violin plots for distribution comparison across methods

**Application-specific figure requirements:**
- EDA figures must reveal the statistical challenges discussed in §2.4
- Every figure in §6 (Application) must have a self-contained caption
- Multi-panel figures should walk the reader through the analysis
- Use colorblind-safe palettes
- Provide both PDF (vector) and high-resolution PNG outputs

**Output:** `figures/` directory with PDFs, generation scripts, and LaTeX snippets.

**Checkpoint:**

```
Figures complete:
- Auto-generated: [list]
- Manual (need your input): [list]
- Rate verification plots: [Y/N]
- Rate comparison table: [Y/N]

[If manual figures needed]: Please add them to figures/ before I proceed.
[If all auto]: Shall I proceed with LaTeX writing?
```

### Phase 3: LaTeX Writing

Invoke `/stat-paper-write` to generate section-by-section LaTeX:

```
/stat-paper-write "PAPER_PLAN.md"
```

**What this does:**
- Write each section with statistics-appropriate style and structure
- Set up venue-specific template (IMS, JASA, Biometrika, COLT, etc.)
- Write assumption blocks with labels and discussion
- Write theorem environments with proof sketches
- Insert rate comparison table
- Write simulation studies with proper DGP specification
- Write supplement with full proofs
- Build `references.bib` with verified entries
- Clarity pass with statistics-specific checks
- Claude subagent reviews quality

**Output:** `paper/` directory with main body + `paper/supplement/` with proofs.

**Checkpoint (theory/methodology):**

```
LaTeX writing complete:
- Main body sections: [N] written
- Supplement sections: [N] written
- Theorems: [N] stated + [N] proof sketches in main body
- Assumptions: [N] labeled (A1)-(AN)
- Rate comparison table: YES
- Citations: [N] unique keys
- Simulation DGPs: [N]

Shall I proceed with compilation?
```

**Checkpoint (application paper):**

```
Application paper LaTeX complete:
- Main body sections: [N] written (§6 Application at [X] pages — centerpiece)
- Supplement sections: [N] written (proofs in supplement)
- §2 Data and Background: [X] pages with [N] EDA figures, [N] tables
- §4 Theory: [1-2] theorems with light discussion
- §5 Simulations: [N] DGPs (informed by §2 data characteristics)
- §6 Application: main analysis + comparison + validation + interpretation
- Comparison methods used: [N] including [N] domain-standard methods
- Data availability statement: present
- Code availability statement: present
- Citations: [N] unique keys (statistical + domain)

Shall I proceed with compilation?
```

### Phase 4: Compilation

Invoke `/paper-compile` to build the PDF:

```
/paper-compile "paper/"
```

**What this does:**
- `latexmk -pdf` with multi-pass compilation
- Auto-fix common errors
- Compile both main paper and supplement
- Post-compilation checks: undefined refs, page count

**Output:** `paper/main.pdf` + `paper/supplement/supplement_main.pdf`

**Checkpoint:**

```
Compilation complete:
- Main paper: SUCCESS ([X] pages)
- Supplement: SUCCESS ([Y] pages)
- Undefined references: [N]
- Undefined citations: [N]

Shall I proceed with the improvement loop?
```

### Phase 5: Auto Improvement Loop with Codex External Dialogue

The improvement loop combines internal Claude review (every round, fast structural fixes) with external Codex MCP dialogue (final round, senior-statistician depth at GPT-5.6 xhigh).

**The dialogue principle applies in Phase 5.** Codex's review is one senior reader's opinion, not a directive. The loop discusses with Codex until both sides converge on what the draft needs, not applies Codex's feedback wholesale. Read `../stat-shared-references/stat-codex-dialogue.md` before starting Round 2.

**Default flow when `REVIEW_MODE = both`:**

Round 1 (Claude internal review):
- Claude subagent reviews the compiled draft.
- Implements CRITICAL and MAJOR fixes.
- Recompiles to `main_round1.pdf` and `supplement_round1.pdf`.

Round 2 (Codex external dialogue):
- Initial Codex MCP review at GPT-5.6 with xhigh reasoning (see stat-paper-write Step 6 Pass B for the prompt template).
- For each Codex criticism, decide per `../stat-shared-references/stat-codex-dialogue.md`: accept, push back via `mcp__codex__codex-reply`, or log disagreement.
- Apply accepted criticisms only (not all criticisms).
- Recompile to `main_round2.pdf` and `supplement_round2.pdf`.

Optional Round 3 (extended Codex dialogue):
- For high-stakes submissions, continue `mcp__codex__codex-reply` on the most important remaining issues from Round 2.
- The goal is convergence, not unanimity. Stop when both sides agree, when disagreements are documented, or after diminishing returns (typically after 2 to 4 dialogue rounds total).
- Apply additional accepted criticisms.
- Recompile to `main_round3.pdf`.

**Codex prompt template for the improvement loop:**

```
mcp__codex__codex:
  model: gpt-5.6
  sandbox: read-only
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a senior statistician reviewing this manuscript at the
    standard of [VENUE]. Paper type: [theory/methodology/application].

    Below is the current draft after one round of automated improvement.

    [paste main body and supplement]

    Please provide:
    1. Top-line verdict: ready to submit, needs minor revision,
       needs major revision, or fundamental problems?
    2. Three to five highest-priority remaining issues, with the
       minimum fix for each
    3. AI-tell audit: count em-dashes, body-prose colons, body-prose
       semicolons, body-prose parentheticals, manual bold or italic in
       body prose, formulaic openings, empty connectives (Importantly,
       Notably), and watchwords (delve, pivotal, landscape, etc.). See
       `../stat-shared-references/stat-style-discipline.md` for the
       whitelisted exceptions per mark.
    4. Main-supplement independence check: any broken cross-references?
       Theorems properly restated in supplement?
    5. Figure design audit: any titles inside figures? Any captions
       not self-contained?
    6. Mock referee report at the venue's standard

    Be direct. Senior statisticians prefer hard feedback in a measured
    voice.
```

After receiving the review, save the threadId and use `mcp__codex__codex-reply` to dig into the highest-priority items:

- "Issue 1 is [X]. Please write the specific replacement text for the affected lines."
- "Please write the mock referee response we should expect at [venue]."
- "If we cannot run [requested additional simulation] before submission, what is the next-best mitigation in writing?"

**Backward-compatible fallback:**

If Codex MCP is unavailable, the loop falls back to `/auto-paper-improvement-loop "paper/"` with Claude subagent reviews for both rounds.

```
/auto-paper-improvement-loop "paper/"
```

**Statistics-specific review focus (passed to reviewer):**

For theory/methodology papers:
- Theorem precision: are statements self-contained and all conditions listed?
- Assumption coverage: are all assumptions used and discussed?
- Rate optimality: is the comparison with prior bounds explicit and fair?
- Proof sketch quality: do they provide genuine insight or just defer?
- Simulation rigor: DGP specification, standard errors, rate verification
- Notation consistency across main body and supplement
- Measured tone: no overclaiming, proper hedging where needed

For application papers (additionally or instead):
- Scientific question clarity in the Introduction
- Data and Background section completeness (EDA, descriptive table, statistical challenges)
- Methodology scoping appropriately for the problem (not over-generalized)
- Theory weight in main body (1-2 theorems max; rest in supplement)
- Simulation DGPs informed by real data characteristics
- Application section depth (multiple sub-analyses, multiple pages, dominant section)
- Substantive findings clarity and interpretation
- Comparison with domain-standard methods
- Validation rigor (holdout, CV, sensitivity)
- Practical recommendations in Discussion
- Data and code availability statements present
- Reproducibility addressed concretely
- Dual-audience accessibility (statisticians + domain readers)
- Self-contained figure captions in §6
- Measured tone, no overclaiming of findings

**Two rounds of review → fix → recompile.**

The reviewer prompt should explicitly invoke `/stat-polishing` standards. The polishing checks the reviewer applies in each round include:

- Punctuation and emphasis discipline (em-dashes cut to at most one; body-prose colons, semicolons, and parentheticals prohibited except for the whitelisted uses; manual bold and italic prohibited except for first-defined technical term and venue-required math bold)
- AI-template removal (no formulaic openings, no empty connectives, no watchwords, no hedge-stacking, no generic conclusions)
- COPSS-style scholar voice (confidence without hype, plain verbs, connective restraint, mathematical precision over praise)
- Paragraph and bullet discipline (4-8 sentence paragraphs, bullets only where appropriate)
- Figure design rules (no titles, self-contained captions, no legend overlap)
- Main-supplement separation (no broken cross-references, supplement is self-contained)

**Output:** PDFs for comparison + `PAPER_IMPROVEMENT_LOG.md`.

**Dispatching review findings.** When a round surfaces a substantive concern (not a line edit), send it to its owner with `../stat-shared-references/stat-review-routing.md` rather than re-deriving the mapping each round. The routing table gives the first handoff only — overclaim and prior-work findings to the positioning/claim audit, assumption and proof findings across to the `stat-theory-skills` repo, style and structure findings to `/stat-polishing`. A finding that maps to a canonical artifact row (CS#, PW#, TR#) carries that ID so the `stat-mock-review` regression check can track it across rounds.

**Anti-churn escalation.** If the same substantive concern survives a pushback or reappears after an accepted repair and recompile, stop running more prose passes on it: the problem is structural. Route it through `stat-review-routing.md` to the owning skill (reframe the contribution, weaken or restrict a claim, repair the theory, restructure the section, or reconsider the venue), then resume. This is the anti-churn rule in `../stat-shared-references/stat-codex-dialogue.md`, not a new stop condition, and it does not bypass author approval.

### Post-pipeline polishing

After the pipeline completes, the user can invoke `/stat-polishing` directly on specific sections that need deeper refinement than two automated rounds can provide. Common cases:

- The introduction still reads as templated. Run `/stat-polishing` on §1 specifically.
- The application section narrative does not flow. Run `/stat-polishing` on §6.
- A theorem statement is precise but its surrounding interpretation is bloated. Run `/stat-polishing` on the relevant subsection.
- Chinese-to-English drafts that need linguistic polishing beyond what the pipeline applies.

### Phase 6: Final Report

For **theory/methodology papers**:

```markdown
# Statistics Paper Writing Pipeline Report

**Input**: [NARRATIVE_REPORT.md or topic]
**Venue**: [AOS/JASA/JRSSB/BIOMETRIKA/BERNOULLI/EJS/STATSINICA/COLT/ALT/MSL]
**Paper type**: [theory/methodology]
**Date**: [today]

## Pipeline Summary

| Phase | Status | Output |
|-------|--------|--------|
| 1. Paper Plan | Done | PAPER_PLAN.md |
| 2. Figures | Done | figures/ ([N] auto + [M] manual) |
| 3. LaTeX Writing | Done | paper/ ([N] sections, [M] citations) |
| 4. Compilation | Done | paper/main.pdf ([X] pages) + supplement ([Y] pages) |
| 5. Improvement | Done | [score0]/10 → [score2]/10 |

## Theory Components
| Component | Count | Status |
|-----------|-------|--------|
| Assumptions | [N] | All labeled and discussed |
| Theorems | [N] | All with proof sketches |
| Rate comparison table | 1 | Present |
| Proofs in supplement | [N] | Complete |

## Simulation Summary
| DGP | Sample sizes | Methods compared | Metrics |
|-----|-------------|-----------------|---------|
| [DGP 1] | [sizes] | [methods] | [metrics] |
| [DGP 2] | [sizes] | [methods] | [metrics] |

## Improvement Scores
| Round | Score | Key Changes |
|-------|-------|-------------|
| Round 0 | X/10 | Baseline |
| Round 1 | Y/10 | [summary] |
| Round 2 | Z/10 | [summary] |

## Deliverables
- paper/main.pdf — Final polished paper
- paper/supplement/supplement_main.pdf — Proofs and additional results
- paper/main_round0_original.pdf — Before improvement
- paper/PAPER_IMPROVEMENT_LOG.md — Full review log

## Remaining Issues (if any)
- [items not addressed]

## Next Steps
- [ ] Visual inspection of PDF
- [ ] Verify all proofs in supplement
- [ ] Check notation consistency main ↔ supplement
- [ ] Add any missing manual figures
- [ ] Prepare cover letter (if venue requires)
- [ ] Submit to [venue]
```

For **application papers**:

```markdown
# Application Paper Writing Pipeline Report

**Input**: [APPLICATION_REPORT.md / DATA_DESCRIPTION.md]
**Venue**: [AOAS/JASA_ACS/BIOSTATISTICS/STATMED/JCGS/JABES]
**Paper type**: application
**Scientific question**: [one-line summary]
**Dataset**: [name, size, time period]
**Date**: [today]

## Pipeline Summary

| Phase | Status | Output |
|-------|--------|--------|
| 1. Paper Plan | Done | PAPER_PLAN.md |
| 2. Figures | Done | figures/ ([N] EDA + [M] application + [K] simulation) |
| 3. LaTeX Writing | Done | paper/ ([N] sections, §6 = [X] pages) |
| 4. Compilation | Done | paper/main.pdf ([X] pages) + supplement ([Y] pages) |
| 5. Improvement | Done | [score0]/10 → [score2]/10 |

## Section Length Allocation

| Section | Pages | Status |
|---------|-------|--------|
| §1 Introduction | [X] | Done |
| §2 Data and Background | [X] | [N] EDA figures, [N] tables |
| §3 Methodology | [X] | Done |
| §4 Theory (light) | [X] | [1-2] theorems |
| §5 Simulations | [X] | [N] DGPs informed by §2 |
| §6 Application | [X] | CENTERPIECE |
| §7 Discussion | [X] | With practical recommendations |

## Application Section Components (§6)
| Component | Status |
|-----------|--------|
| Analysis setup | Done |
| Main analysis with figures | [N] figures |
| Comparison with [N] domain-standard methods | Done |
| Validation (holdout / CV / sensitivity) | Done |
| Substantive interpretation | Done |

## Substantive Findings
1. [Finding 1 with brief evidence]
2. [Finding 2 with brief evidence]
3. [Finding 3 with brief evidence]

## Reproducibility
- [ ] Data availability statement: present
- [ ] Code availability statement: present (repository URL: [URL])
- [ ] Replication script: documented in supplement
- [ ] Computational environment: documented

## Improvement Scores
| Round | Score | Key Changes |
|-------|-------|-------------|
| Round 0 | X/10 | Baseline |
| Round 1 | Y/10 | [summary] |
| Round 2 | Z/10 | [summary] |

## Deliverables
- paper/main.pdf — Final polished application paper
- paper/supplement/supplement_main.pdf — Proofs, additional analyses, software docs
- paper/main_round0_original.pdf — Before improvement
- paper/PAPER_IMPROVEMENT_LOG.md — Full review log

## Remaining Issues (if any)
- [items not addressed]

## Next Steps
- [ ] Visual inspection of PDF
- [ ] Verify dataset name, citations, and domain terminology consistency
- [ ] Verify code repository is public and complete
- [ ] Verify reproducibility script runs end-to-end
- [ ] Prepare cover letter highlighting applied significance
- [ ] Submit to [venue]
```

## Key Rules

### General (all paper types)

- **Large file handling**: If Write fails, use Bash to write in chunks.
- **Don't skip phases.** Each phase builds on the previous one.
- **Checkpoint between phases** when AUTO_PROCEED=false.
- **Manual figures first.** Architecture diagrams or conceptual figures must be provided before Phase 3.
- **Compilation must succeed** before entering the improvement loop.
- **Preserve all PDFs.** User needs round0/round1/round2 for comparison.
- **Supplement is part of the deliverable** — compile it too.
- **Standard errors are mandatory** for all simulation results.
- **Measured tone throughout** — statistics papers are more formal than ML conference papers.

### Theory/methodology rules

- **Rate comparison table is mandatory** for theory papers.
- **Assumptions must be discussed** — not just stated.
- **Proof sketches must provide insight** — not just defer to supplement.

### Application paper rules

- **Application is data-driven** — the entire pipeline must keep the dataset and scientific question central
- **Dataset details must be available upfront** — for Phase 1 to plan §2 properly, the input should specify the data source, structure, key variables, and EDA findings
- **Phase 2 must include EDA figures** — these go in §2 and are often the most-viewed visuals in the paper
- **Simulation DGPs must mirror the real data** — Phase 1 plan must specify how DGPs reflect §2 features
- **§6 Application section is the centerpiece** — it must be planned and written as the largest section
- **Theory is light** — at most 1-2 theorems in main body; the pipeline should default to moving deeper theory to supplement
- **Comparison must include domain-standard methods** — the plan must identify these in Phase 1
- **Validation is mandatory** — holdout/CV/sensitivity must be planned and executed
- **Reproducibility is mandatory** — Phase 3 must produce data and code availability statements; final deliverables should include a working replication path
- **Lead with findings in abstract and intro** — the pipeline's improvement loop should check that what was discovered is named, not just what method was used
- **Both audiences served** — the improvement loop reviewer should check accessibility to both statisticians and domain readers

## Composing with Other Workflows

```
/idea-discovery "direction"              ← find ideas
implement                                ← write code
/run-experiment                          ← run simulations
/auto-review-loop "paper topic"          ← iterate research
/stat-paper-writing "NARRATIVE_REPORT.md"  ← you are here
                                             submit!
```

## Typical Timeline

| Phase | Duration | Notes |
|-------|----------|-------|
| 1. Paper Plan | 5-10 min | Theory planning takes longer |
| 2. Figures | 5-15 min | Rate plots + sim tables |
| 3. LaTeX Writing | 20-40 min | Supplement adds time |
| 4. Compilation | 3-5 min | Main + supplement |
| 5. Improvement | 15-30 min | Statistics-specific review |

**Total: ~50-100 min** for a full paper from narrative to polished PDF + supplement.
