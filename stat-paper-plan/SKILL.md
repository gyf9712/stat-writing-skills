---
name: stat-paper-plan
description: "Generate a structured paper outline for a statistics or ML theory paper. Supports theory, methodology, and application paper types. Use when user says \"统计论文大纲\", \"stat paper outline\", \"plan the stat paper\", \"统计应用论文\", \"application paper outline\", or wants to create a paper plan for AoS, JASA T&M, JASA ACS, AOAS, JRSS-B, Biometrika, Bernoulli, EJS, Statistica Sinica, Biostatistics, JCGS, COLT, or ALT."
argument-hint: [topic-or-narrative-doc]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Stat Paper Plan: From Research Results to Paper Outline

Generate a structured outline for a statistics, applied statistics, or ML theory paper from: **$ARGUMENTS**

## Constants

- **CLAUDE_REVIEWER_MODEL = `claude-opus-4-6`** — Claude model invoked via the Agent tool as a subagent for fast internal review.
- **CODEX_REVIEWER_MODEL = `gpt-5.4`** — External LLM invoked via Codex MCP for senior-statistician external review. Uses `model_reasoning_effort: xhigh`.
- **REVIEW_MODE = `both`** — Options: `claude` (internal only, fast), `codex` (external only, deep), `both` (claude first, then codex on final draft). Default `both` for high-stakes submissions; switch to `claude` for quick iteration.
- **TARGET_VENUE = `AOS`** — Default venue. Supported:
  - **Theory/methodology venues**: `AOS` (Annals of Statistics), `JASA` (JASA Theory & Methods), `JRSSB`, `BIOMETRIKA`, `BERNOULLI`, `EJS`, `STATSINICA`, `MSL`
  - **Application venues**: `AOAS` (Annals of Applied Statistics), `JASA_ACS` (JASA Applications and Case Studies, formerly JASA_APP), `BIOSTATISTICS`, `STATMED` (Statistics in Medicine), `JCGS`, `JABES`
  - **ML theory conferences**: `COLT`, `ALT`
- **PAPER_TYPE = `auto`** — Auto-detect from content. Options:
  - `theory` — main contribution is theoretical results (rates, bounds, characterizations)
  - `methodology` — main contribution is a new method with theory + empirics
  - `application` — main contribution is solving a real scientific problem; data and findings drive the paper
  - `auto` — infer from the input narrative and target venue
- **MAX_PAGES** — Venue-dependent working norm. AOS: about 25 pages in standard journal style before overflow moves to supplement. BERNOULLI / EJS: no hard limit encoded here; size to contribution. AOAS: most published papers will not exceed 20 pages in standard journal style. JASA T&M / JASA ACS: 25-30. JRSSB: 25-35. BIOMETRIKA: regular and synthesis papers are normally fewer than 20 pages; Miscellanea max 8 pages. BIOSTATISTICS: no fixed page rule encoded here; follow recent issues and use supplement aggressively. STATMED: 15-25. JCGS: 20-30. COLT: 30 main-body pages. ALT: 20-25 main-body pages. COLT/ALT: appendix unlimited.
- **Caveat**: these are skill defaults reflecting working norms at the dates the venue entries in `stat-venue-checklists.md` were last checked. Always re-check the current journal author guidelines before submission.

## Inputs

The skill expects one or more of these:

1. **NARRATIVE_REPORT.md** or **STORY.md** — research narrative with claims, theorems, evidence
2. **Theorem statements and proof outlines** — formal results with sketches
3. **Simulation results** — JSON files, tables, figures from experiments
4. **IDEA_REPORT.md** — from idea-discovery pipeline
5. **Existing draft** — partial LaTeX or notes to restructure
6. **For application papers**:
   - **DATA_DESCRIPTION.md** — dataset description, source, variables, exploratory analysis
   - **APPLICATION_REPORT.md** — analysis results, scientific findings, domain interpretation
   - **EDA outputs** — exploratory figures, tables, summary statistics

If none exist, ask the user to describe the paper's main theorem, method, or application in 3-5 sentences.

### Detecting Paper Type

If `PAPER_TYPE = auto`, infer from inputs:

- **Application paper signals**: a specific dataset is named in the narrative; the scientific question precedes the method; substantive findings are emphasized; target venue is AOAS, JASA_ACS, BIOSTATISTICS, STATMED, JCGS, or JABES
- **Theory paper signals**: focus is on rates, bounds, or characterizations; data is secondary or absent; target venue is AOS, BERNOULLI, EJS, COLT, ALT, or MSL
- **Methodology paper signals**: focus is on a new method with both theory and empirics; data analysis is illustrative rather than central; target venue is JASA T&M, JRSSB, BIOMETRIKA, STATSINICA

If signals are mixed, ask the user explicitly. The paper type determines section structure, theory depth, and length allocation.

## Workflow

### Step 1: Extract Claims, Theorems, Data, and Evidence

Read all available documents. What to extract depends on paper type.

**For theory and methodology papers, extract:**

1. **Main theorems** (1-3 primary theoretical results for theory; 2-4 for methodology)
2. **Supporting results** (lemmas, propositions, corollaries)
3. **One-sentence contribution** (what the paper proves or proposes)
4. **Assumptions** needed for each result
5. **Evidence**: which simulations verify which theorems, which real data demonstrates practical value
6. **Known limitations**
7. **Rate comparisons** with existing literature

**For application papers, additionally extract (often this is the dominant input):**

1. **The scientific question** (what substantive question is the paper answering)
2. **The dataset**: source, size, structure, variables, time period, collection method
3. **Key data characteristics**: features of the data that pose statistical challenges (dependence, missingness, dimension, heterogeneity, censoring, mixed types)
4. **Domain context**: what the field currently knows or assumes
5. **Limitations of current domain practice**: what standard methods are used and why they are inadequate
6. **Substantive findings**: what the analysis revealed about the scientific question
7. **Comparison methods**: which methods practitioners use that should be benchmarked
8. **Validation strategy**: holdout, cross-validation, sensitivity analyses
9. **Reproducibility**: data availability, code, computational requirements
10. **Light theoretical results** (typically 1-2 main theorems max)

Build a **Theorems-Evidence Matrix**:

```markdown
| Result | Statement (informal) | Assumptions | Verified by | Status |
|--------|---------------------|-------------|-------------|--------|
| Thm 1 (Upper bound) | Rate n^{-2s/(2s+d)} for estimator | (A1)-(A3) | Sim 1, Fig 2 | Proved |
| Thm 2 (Lower bound) | Minimax lower bound matches | Model only | N/A (information-theoretic) | Proved |
| Thm 3 (CLT) | Asymptotic normality | (A1)-(A4) | Sim 2 (coverage) | Proved |
| Prop 1 (Computation) | O(n log n) algorithm | — | Sim 3 (timing) | Proved |
```

Also build a **Claims-Evidence Matrix** (parallel to the existing paper-plan style):

```markdown
| Claim | Evidence | Status | Section |
|-------|----------|--------|---------|
| Minimax optimal rate | Thm 1 + Thm 2 | Supported | §3 |
| Weaker assumptions than prior work | Assumption comparison | Supported | §2, Remark 1 |
| Practical computational efficiency | Prop 1 + Sim 3 | Supported | §4, §5 |
| Works on real data | Real data analysis | Partially supported | §6 |
```

**For application papers, additionally build a Findings-Evidence Matrix** (this is often the most important planning artifact for application papers):

```markdown
| Finding | Statistical evidence | Validation | Domain significance | Section |
|---------|---------------------|------------|--------------------|---------|
| [Finding 1: specific scientific claim] | [estimates with CI from §6] | [holdout/CV result] | [why this matters to the field] | §6.2 |
| [Finding 2: contrast with prior view] | [comparison with standard method] | [sensitivity analysis] | [implications for practice] | §6.3 |
| [Finding 3: novel pattern] | [exploratory finding with confirmatory test] | [cross-validation] | [opens new questions] | §6.4 |
```

And a **Data-Challenges Matrix**:

```markdown
| Data feature | Statistical challenge | Methodological response |
|--------------|----------------------|------------------------|
| [e.g., spatial dependence] | Standard iid assumption fails | Hierarchical spatial model in §3.1 |
| [e.g., informative missingness] | Complete-case bias | Joint modeling of missingness in §3.2 |
| [e.g., high dimensionality with sparsity] | Curse of dimensionality | Regularized estimation in §3.3 |
```

These matrices ensure that the application paper's structure flows from data → challenge → method → finding, rather than from method → demonstration.

### Step 2: Determine Paper Type and Structure

Before committing to a structure, read `../stat-shared-references/stat-writing-principles.md` for the narrative arc.

**IMPORTANT**: Section count is flexible (5-9 sections). Choose what fits the content.

**Theory paper (main contribution is theorems/bounds):**
```
1. Introduction (2-3 pages)
2. Problem Setup and Assumptions (2-3 pages)
3. Main Results (3-5 pages)
   — theorem statements, rate comparisons, discussion
4. Estimation / Methodology (1-2 pages)
   — the estimator/test/procedure if not already in Setup
5. Simulation Studies (2-3 pages)
6. Discussion (1-2 pages)
— Supplement: full proofs, additional simulations
```

**Theory paper with real data:**
```
1. Introduction (2-3 pages)
2. Problem Setup and Assumptions (2-3 pages)
3. Main Results (3-5 pages)
4. Simulation Studies (2-3 pages)
5. Real Data Analysis (2-3 pages)
6. Discussion (1-2 pages)
— Supplement: full proofs, additional results
```

**Methodology paper:**
```
1. Introduction (2-3 pages)
2. Background and Notation (1-2 pages)
3. Proposed Method (3-4 pages)
   — algorithm, implementation, tuning
4. Theoretical Properties (2-3 pages)
   — consistency, rates, efficiency
5. Computation (1-2 pages)
   — algorithm complexity, practical considerations
6. Simulation Studies (3-4 pages)
7. Application / Real Data Analysis (2-3 pages)
8. Discussion (1-2 pages)
— Supplement: proofs, additional simulations and data analysis
```

**Application paper (AOAS, JASA ACS, Biostatistics, JCGS):**
```
1. Introduction (2-3 pages)
   — scientific question, data, statistical challenges,
     findings preview, contributions
2. Data and Scientific Background (2-4 pages)
   — domain context, dataset description, EDA figures,
     statistical challenges revealed by the data
3. Methodology (3-4 pages)
   — model formulation, estimation, inference (scoped to problem)
4. Theoretical Properties (1-2 pages, LIGHT)
   — 1-2 main theorems only (consistency, asymptotic distribution)
   — heavy theory in supplement
5. Simulation Studies (2-3 pages)
   — DGPs informed by the real data
   — comparison with domain-standard methods
6. Application / Real Data Analysis (4-6 pages) ← LARGEST SECTION
   — analysis setup
   — main analysis with substantive findings
   — comparison with existing approaches in the field
   — validation (holdout, CV, sensitivity)
   — substantive interpretation
7. Discussion (1-2 pages)
   — substantive findings summary
   — methodological summary
   — practical recommendations for practitioners
   — limitations
   — extensions and open questions
— Supplement: detailed data description, full proofs,
  additional simulations, additional analyses, software docs
```

**Application paper alternative (heavily validated):**
```
1. Introduction
2. Data and Background
3. Methodology
4. Theoretical Analysis (light)
5. Computation
6. Simulation Studies
7. Main Application
8. Sensitivity and Validation
9. Discussion
```

Use the alternative when validation is itself a major contribution (e.g., demonstrating robustness across multiple datasets or settings).

Read `../stat-shared-references/stat-application-writing.md` before locking in the application paper structure.

**COLT/ALT theory paper:**
```
1. Introduction (2-3 pages)
2. Problem Setup and Preliminaries (2-3 pages)
3. Main Results (4-6 pages)
4. Proof Techniques / Analysis (3-5 pages)
   — more proof detail in main body since page limit is generous
5. Experiments (2-3 pages, optional for COLT)
6. Discussion and Open Problems (1-2 pages)
— Appendix: complete proofs
```

### Step 3: Section-by-Section Planning

For each section, specify:

```markdown
### §0 Abstract
- **Problem**: [the specific statistical problem addressed]
- **Gap**: [what is unknown or suboptimal]
- **Main result**: [theorem in plain language, with rate]
- **Approach**: [proof technique or method, in one sentence]
- **Verification**: [simulation or data confirmation]
- **Implication**: [what this enables]
- **Estimated length**: 150-250 words
- **Self-contained check**: understandable without the paper?

### §1 Introduction
- **Problem motivation**: [why this problem matters, specific not generic]
- **Prior work and gap**: [what is known, what rates exist, what's open]
- **Contribution**: [main result(s) in plain language]
- **Proof technique overview**: [key insight, novel tools]
- **Contribution bullets**: [2-4 specific, verifiable claims]
- **Results preview**: [strongest result surfaced early]
- **Paper organization**: [roadmap of remaining sections]
- **Key citations**: [5-10 papers to position against]
- **Estimated length**: 2-3 pages

### §2 Problem Setup / Model / Assumptions
- **Model**: [formal model specification]
- **Notation**: [key symbols defined here]
- **Assumptions**: [list with labels (A1), (A2), ...]
- **Assumption discussion**: [which are standard, which are novel, comparison with prior work]
- **Estimated length**: 2-3 pages

### §3 Main Results
- **Theorem statements**: [list each theorem/proposition]
- **Rate comparison table**: [this paper vs prior work]
- **Proof sketches**: [1-2 paragraphs per main theorem]
- **Remarks and corollaries**: [optimality, extensions, special cases]
- **Estimated length**: 3-5 pages

### §4 Estimation / Method (if separate from §2-3)
- **Estimator/procedure definition**: [formal specification]
- **Algorithm**: [pseudocode if applicable]
- **Tuning parameters**: [how chosen, adaptive or oracle]
- **Computational complexity**: [time and space]
- **Estimated length**: 1-3 pages

### §5 Simulation Studies
- **DGP designs**: [list each data generating process]
  - DGP 1: [model, parameter values, purpose]
  - DGP 2: [model, parameter values, purpose]
  - DGP 3: [adversarial/challenging case]
- **Sample sizes**: [e.g., n = 100, 500, 2000, 10000]
- **Number of replications**: [500-1000]
- **Comparison methods**: [3-5 existing methods]
- **Metrics**: [MSE, coverage, power, computation time, etc.]
- **Rate verification**: [log-log plots planned?]
- **Figures planned**:
  - Fig X: [type, what it shows]
  - Table X: [what it shows]
- **Estimated length**: 2-4 pages

### §6 Real Data Analysis (if applicable)
- **Dataset**: [source, size, why appropriate]
- **Preprocessing**: [steps, variables used]
- **Comparison methods**: [same as simulations if possible]
- **Domain interpretation**: [what the results mean substantively]
- **Estimated length**: 2-3 pages

### §7 Discussion
- **Contribution summary**: [rephrased, not copied from intro]
- **Connections to prior work**: [how results relate or improve]
- **Limitations**: [assumptions that may be restrictive]
- **Open problems**: [specific technical questions remaining]
- **Extensions**: [natural generalizations]
- **Estimated length**: 1-2 pages

### Application Paper Section-by-Section Plan

For application papers (PAPER_TYPE = `application`), use the following section plan instead of (or in addition to) the templates above.

```markdown
### §0 Abstract (application paper)
- **Scientific question**: [what substantive question is being asked]
- **Dataset**: [which dataset enables it]
- **Statistical challenge**: [what data feature makes standard analysis inadequate]
- **Proposed approach**: [method developed or adapted]
- **Application finding**: [the most important discovery — name it]
- **Validation**: [how the finding was checked]
- **Implication**: [what this means for the domain]
- **Estimated length**: 200-280 words

### §1 Introduction (application paper)
- **Scientific question and stakes**: [first paragraph hook]
- **Dataset introduction**: [brief, with relevance to the question]
- **Statistical challenges**: [features that demand new methodology]
- **Limitations of current approaches**: [what the domain does today, why it falls short]
- **Proposed approach**: [high-level method description]
- **Substantive findings preview**: [what the analysis discovered — crucial]
- **Contribution bullets**: [2-4 spanning methodology and findings]
- **Organization**: [section roadmap]
- **Estimated length**: 2-3 pages

### §2 Data and Scientific Background (application paper)
- **Domain context**: [1-3 paragraphs accessible to non-experts]
- **Data source and collection**: [study design, time period, sampling]
- **Data structure**: [sample size, variables, hierarchical/temporal structure]
- **EDA figures planned**: [list — these often become key visuals]
  - Fig X: [type, what it reveals]
- **Descriptive table**: [variables, units, summary statistics]
- **Statistical challenges revealed**: [pivot from data features to methodological need]
- **Preprocessing**: [brief; details to supplement]
- **Estimated length**: 2-4 pages

### §3 Methodology (application paper)
- **Model formulation**: [tied to data, not over-generalized]
- **Estimation**: [estimator/algorithm scoped to the problem]
- **Tuning parameter selection**: [practical guidance]
- **Inference / uncertainty quantification**: [bootstrap, asymptotic CI, posterior]
- **Computational considerations**: [implementation notes]
- **Estimated length**: 3-4 pages

### §4 Theoretical Properties (application paper — LIGHT)
- **Main theorem(s)**: [1-2 max, with all assumptions]
- **Conditions verification for the application**: [whether conditions hold for the data]
- **Reference to supplement**: [where full proofs and extensions live]
- **Estimated length**: 1-2 pages

### §5 Simulation Studies (application paper)
- **DGP designs informed by real data**:
  - DGP 1: [mirrors real data characteristics — sample size, distributions, dependence]
  - DGP 2: [stress test — more extreme conditions]
  - DGP 3: [comparison setting matching prior literature]
- **Sample sizes**: [include the real data n]
- **Replications**: [500-1000]
- **Comparison methods**: [methods used by the domain practitioners]
- **Metrics aligned with application**: [prediction error, calibration, coverage, etc.]
- **Estimated length**: 2-3 pages

### §6 Application / Real Data Analysis (application paper — CENTERPIECE)
- **Analysis setup**: [restate question, describe analytic pipeline]
- **Main analysis**:
  - Sub-analysis 1: [what is fit, what is found, figure/table reference]
  - Sub-analysis 2: [additional view or stratification]
- **Comparison with existing approaches**: [domain-standard methods on same data]
- **Validation**:
  - Holdout / cross-validation strategy
  - Sensitivity analyses (model specification, hyperparameters)
  - Robustness across data subsets
- **Substantive interpretation**: [what the findings mean for the domain]
- **Figures planned** (3-6 high-quality figures, each with self-contained captions)
- **Estimated length**: 4-6 pages

### §7 Discussion (application paper)
- **Substantive findings summary**: [what we learned about the scientific question]
- **Methodological summary**: [what the method contributes]
- **Practical recommendations**: [when and how to use, software, computation]
- **Data limitations**: [selection, measurement, missingness]
- **Methodological limitations**: [assumptions that may not hold elsewhere]
- **Generalizability**: [where the method should extend, where it shouldn't]
- **Open questions**: [scientific and methodological]
- **Estimated length**: 1-2 pages
```

### Supplement
- **Proof plan**: [which proofs go where]
  - App A: Proofs of main theorems (Thm 1, 2, ...)
  - App B: Technical lemmas
  - App C: Additional simulations
  - App D: Additional data analysis (if applicable)
- **Estimated length**: 20-40 pages
```

### Step 4: Figure and Table Plan

For **theory and methodology papers**:

```markdown
## Figure Plan (theory/methodology)

| ID | Type | Description | Data Source | Section | Priority |
|----|------|-------------|-------------|---------|----------|
| Fig 1 | Conceptual | Problem illustration or method overview | manual | §1 | HIGH |
| Fig 2 | Line plot | Convergence rate verification (log-log) | sim results | §5 | HIGH |
| Fig 3 | Box/violin | Method comparison across DGPs | sim results | §5 | HIGH |
| Fig 4 | Line/scatter | Real data analysis results | data | §6 | MEDIUM |
| Table 1 | Rate comparison | Prior bounds vs this paper | manual | §3 | HIGH |
| Table 2 | Simulation | MSE/coverage comparison table | sim results | §5 | HIGH |
| Table 3 | Real data | Method comparison on real data | data | §6 | MEDIUM |
```

For **application papers** (figures are weighted toward §2 EDA and §6 application):

```markdown
## Figure Plan (application paper)

| ID | Type | Description | Data Source | Section | Priority |
|----|------|-------------|-------------|---------|----------|
| Fig 1 | EDA overview | Visual summary of the dataset | real data | §2 | HIGH |
| Fig 2 | EDA | Visualization of statistical challenge in data | real data | §2 | HIGH |
| Fig 3 | EDA | Secondary data feature (dependence, missingness, etc.) | real data | §2 | MEDIUM |
| Table 1 | Descriptive | Variables, counts, summary statistics | real data | §2 | HIGH |
| Fig 4 | Sim | Method comparison (informed by real-data DGPs) | sim results | §5 | HIGH |
| Table 2 | Sim | Comparison metrics with SE | sim results | §5 | HIGH |
| Fig 5 | Application main | Primary analysis result | analysis | §6 | HIGH |
| Fig 6 | Application | Comparison with domain-standard method | analysis | §6 | HIGH |
| Fig 7 | Validation | Holdout / cross-validation results | analysis | §6 | HIGH |
| Fig 8 | Sensitivity | Robustness to model choices | analysis | §6 | MEDIUM |
| Table 3 | Application | Estimated parameters with CI | analysis | §6 | HIGH |
```

For application papers, **the EDA figures in §2 and the analysis figures in §6 are the paper's most important visuals**. Plan them carefully with self-contained captions.

### Step 5: Assumption Dependency Map

Create a visual dependency map:

```markdown
## Assumption Dependencies

Theorem 1 (Upper bound) ← (A1) sub-Gaussian noise
                        ← (A2) Sobolev smoothness
                        ← (A3) Design density bounded

Theorem 2 (Lower bound) ← (A2) Sobolev smoothness [only]

Theorem 3 (CLT)         ← (A1)-(A3) [same as Thm 1]
                        ← (A4) Bandwidth condition

Proposition 1 (Computation) ← no statistical assumptions

Note: Thm 2 uses fewer assumptions than Thm 1, confirming
that the lower bound applies to the full class, not just
a restricted setting.
```

### Step 5.5: Build the Prior Work Matrix (required)

Before locking the outline, create `PRIOR_WORK_MATRIX.md` in the project root. Drafting does not begin until the closest 5-10 papers have been compared at the level of problem, assumptions, results, and evidence. This is the primary defense against the most common reason papers are rejected from Big Four venues: the result is real but is not positioned against an existing close paper.

Use this schema:

```md
# PRIOR_WORK_MATRIX

| ID | Reference | Venue/Year | Paper Type | Problem / Estimand / Setting | Closest Overlap With Our Paper | Their Main Result or Claim | Their Assumptions / Scope | Their Evidence | What They Do Not Do | Our Exact Delta | Evidence We Must Show | Read In Full | Citation Verified | Novelty Risk |
|----|-----------|------------|------------|-------------------------------|-------------------------------|----------------------------|---------------------------|----------------|---------------------|-----------------|-----------------------|--------------|------------------|-------------|
| PW1 | Smith and Jones (2024) | JRSS-B / 2024 | methodology | sparse additive regression with clustered errors | same estimand, same high-dimensional regime | adaptive estimator with prediction guarantee | sub-Gaussian noise, iid clusters, known sparsity upper bound | theory + simulations | no valid cluster-robust inference; no asymptotic normality | cluster-robust inference under finite fourth moments, plus Wald intervals | Theorem 1, Theorem 3, Table 1, Sim 2, real-data comparison | Theorem 2 read; Sec. 4 simulations skimmed | yes | HIGH |
```

Rules:
- The matrix must contain 5-10 rows covering the closest existing work.
- For each row, the `Our Exact Delta` column must be a sentence the author can defend in a referee report.
- Any row with `Novelty Risk = HIGH` must be either reframed (so the delta is clearer) or matched to specific evidence the paper will show.
- `Citation Verified` must be `yes` before the row is allowed to influence drafting. Use the DBLP/CrossRef workflow in the writing skill.
- `Read In Full` records which parts of the cited paper were actually read (theorem, abstract, full paper). For comparative claims that depend on the cited paper's assumptions or rates, the relevant theorem must be read in full, not just the abstract. Citing a paper for what we assume it says is the most common source of overclaim in statistics papers.

The matrix feeds directly into `CLAIM_SUPPORT_MAP.md`, built in `stat-paper-write` Step 2.5 from this matrix and from `TECHNICAL_RISK_REGISTER.md`. Every positioning claim and every technical comparative claim in the drafted paper must trace back through `CLAIM_SUPPORT_MAP.md` to a row of `PRIOR_WORK_MATRIX.md`.

Read `../stat-shared-references/stat-positioning-and-claims.md` for the full positioning-audit and claim-strength-audit protocol, including how to search for missing close prior work using `/semantic-scholar`, `/arxiv`, `/novelty-check`, and `mcp__codex__codex`.

### Step 5.6: Build the Technical Risk Register (required)

Also before drafting, create `TECHNICAL_RISK_REGISTER.md` in the project root. This identifies hidden risks in the theorems, simulations, and claims so they are surfaced before language hardens.

```md
# TECHNICAL_RISK_REGISTER

| Risk ID | Component | Claim at Risk | Failure Mode | Why This Might Fail | Severity | Likelihood | Required Check or Mitigation | Owner | Status |
|---------|-----------|---------------|--------------|---------------------|----------|------------|------------------------------|-------|--------|
| TR1 | Theorem 2 lower bound | "The lower bound matches the upper bound on the same function class" | lower bound proved on a smaller class than the upper bound | current construction uses bounded design and excludes heteroskedasticity stated in the main theorem | CRITICAL | medium | either narrow the theorem statement or extend the lower-bound proof before abstract/introduction language is finalized | author + theory reviewer | OPEN |
| TR2 | Application finding 2 | "age modifies treatment effect" | observational confounding may explain the pattern | no sensitivity analysis yet; current evidence is associational only | HIGH | high | add sensitivity analysis or weaken claim to association | author + application reviewer | OPEN |
```

Rules:
- Any claim that appears in the abstract, introduction, contribution list, or discussion must have either `Status = CLOSED` or an explicit written downgrade of the claim.
- `CRITICAL` and `HIGH` rows require human sign-off before the paper proceeds to drafting.
- The register is updated in `stat-paper-write` after the first full draft and reviewed again in the final Codex pass.

### Step 6: Citation Scaffolding

```markdown
## Citation Plan
- §1 Intro: [foundational refs] (problem motivation), [prior work refs] (existing rates)
- §2 Setup: [refs for model class], [refs for assumption conditions]
- §3 Main Results: [refs for rate comparisons], [refs for proof techniques]
- §5 Simulations: [refs for comparison methods]
- §6 Real Data: [refs for dataset], [refs for domain context]
```

**Citation rules:**
1. NEVER generate BibTeX from memory
2. Verify via DBLP/CrossRef/Semantic Scholar
3. Prefer published versions over arXiv when available
4. For statistics references, check MathSciNet as well
5. Flag uncertain citations with `[VERIFY]`

### Step 7: Cross-Review

The plan is reviewed in up to two passes, depending on `REVIEW_MODE`.

#### Pass A: Fast internal review with Claude subagent

Use when `REVIEW_MODE = claude` or `both`. The Claude subagent reviews for structural and content completeness.

For **theory or methodology papers**:

```
Agent(subagent_type="general-purpose"):
  model: claude-opus-4-6
  prompt: |
    Review this paper outline for a [VENUE] statistics paper.
    Paper type: [theory/methodology]

    [full outline including Theorems-Evidence Matrix]

    Score 1-10 on:
    1. Theorem clarity — are results stated precisely enough to evaluate?
    2. Assumption reasonableness — are conditions standard or too restrictive?
    3. Rate optimality — is the rate compared with known optimal rates?
    4. Proof coverage — are key arguments sketched, or is everything deferred?
    5. Simulation design — do simulations verify what the theory predicts?
    6. Positioning — is the contribution clearly distinguished from prior work?
    7. Page budget feasibility
    8. For COLT/ALT: does it fit the venue scope?

    For each weakness, suggest the MINIMUM fix.
```

For **application papers**:

```
Agent(subagent_type="general-purpose"):
  model: claude-opus-4-6
  prompt: |
    Review this paper outline for a [VENUE] application paper.
    Paper type: application
    Target venue: [AOAS / JASA ACS / Biostatistics / etc.]

    [full outline including Findings-Evidence Matrix, Data-Challenges Matrix,
    and section plan]

    Score 1-10 on:
    1. Scientific question — is it clearly stated and substantive?
    2. Dataset clarity — is the data described with enough detail to evaluate fit?
    3. Statistical challenge motivation — do data features genuinely demand new methodology?
    4. Methodology scope — is the method appropriately scoped (not over-generalized)?
    5. Theory weight — is theory appropriately light (1-2 theorems main, rest supplement)?
    6. Simulation design — are DGPs informed by the real data?
    7. Application section weight — is it planned as the largest section (4-6+ pages)?
    8. Substantive findings — are specific findings identified in the plan?
    9. Comparison breadth — are domain-standard methods included for comparison?
    10. Validation strategy — are holdout/CV/sensitivity analyses planned?
    11. Reproducibility — are data and code availability addressed?
    12. Audience balance — does the plan serve both statisticians and domain readers?

    For each weakness, suggest the MINIMUM fix.
```

Apply feedback before moving to Pass B.

#### Pass B: External senior-statistician review with Codex MCP (GPT-5.4, xhigh)

Use when `REVIEW_MODE = codex` or `both`. The external review brings independent judgment from a different model family. This is the recommended final check before drafting begins for serious submissions.

**Step B.1: Initial review call.**

```
mcp__codex__codex:
  model: gpt-5.4
  sandbox: read-only
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a senior statistician serving as Associate Editor for a top
    statistics journal: [AoS / JASA / JRSS-B / Biometrika / AOAS / etc.].
    Paper type: [theory / methodology / application].

    The author has provided a paper plan. Please review it as if it were
    the introduction-and-outline portion of a submission, focused on
    whether the work as planned can clear the bar for this venue.

    Plan:
    [paste full PAPER_PLAN.md including matrices, structure, figures,
     and citation plan]

    Please provide:

    (1) Top-line verdict: is this plan competitive at [VENUE], borderline,
        or below bar? Be specific about which dimension is the binding
        constraint (novelty, depth of theory, application substance,
        positioning, scope).

    (2) Three to five most important issues, ranked by what would change
        the editorial decision. For each, name the minimum fix in
        concrete terms. Avoid generic suggestions like "more experiments";
        instead specify: which simulation under which DGP, which theorem
        with which assumption relaxed, which comparison with which
        existing method on which dataset.

    (3) For theory papers: assess the rate comparison table and whether
        the proposed assumptions are weaker, stronger, or comparable to
        the closest prior work. Identify any rate that is suspicious or
        that should be expected to be tight only up to log factors.

    (4) For methodology papers: assess whether the simulation studies
        will plausibly support the claims given the planned DGPs, and
        whether the real-data analysis carries enough weight.

    (5) For application papers: assess whether the scientific question
        and dataset are substantive enough for [VENUE], whether §2 Data
        and §6 Application together carry enough weight, and whether
        comparison with domain-standard methods is adequate.

    (6) Positioning relative to prior work: are there obvious recent
        papers (within the last 2-3 years) the author may have missed?
        Cite specifically when you can; if you are uncertain, say so.

    (7) Voice and submission-readiness: from the plan, do you expect
        the eventual draft to read like a senior statistician wrote it,
        or like an AI-shaped first draft? Identify any planning signals
        that point to the second outcome.

    Be direct and specific. Conservative reviewers reject more papers
    than aggressive ones do; do not soften.
```

Save the returned `threadId`. The plan author should:
- Accept findings that are clearly correct
- Push back on misunderstandings or factual errors, using `mcp__codex__codex-reply` with the same `threadId`
- Refine the plan based on accepted findings

**Step B.2: Targeted follow-up rounds.**

Use `mcp__codex__codex-reply` to iterate on the most actionable items. Useful patterns:

- "If we add [specific simulation], does that close the gap on issue 2?"
- "Please write the rate comparison table you would expect to see in this paper. We'll compare with what we have."
- "For the application paper, name three domain-standard methods you would expect to see as comparison."
- "Give me a mock referee report at the level of [JASA / AoS] with: Summary, Strengths, Weaknesses, Recommendation."

**Step B.3: Convergence and documentation.**

Stop iterating when:
- Both sides agree on what the plan needs to be competitive
- Specific actionable items are listed
- The author has a clear next step

Save the Codex dialogue summary to `PAPER_PLAN_REVIEW.md` in the project root, including:
- Initial verdict
- Top issues with proposed fixes
- Specific simulations, theorems, or comparisons recommended
- Mock referee report if requested
- Outstanding disagreements between Claude review and Codex review (these often signal genuine ambiguity worth checking with a human supervisor)

Apply the accepted feedback before finalizing the plan.

### Step 8: Output

Save to `PAPER_PLAN.md`:

```markdown
# Statistics Paper Plan

**Title**: [working title]
**One-sentence contribution**: [what the paper proves, proposes, or discovers]
**Venue**: [target venue]
**Type**: [theory / methodology / application]
**Date**: [today]
**Page budget**: [estimated pages main + supplement]

## Theorems-Evidence Matrix
[from Step 1 — present for all paper types]

## Claims-Evidence Matrix
[from Step 1 — present for all paper types]

## Findings-Evidence Matrix (application papers only)
[from Step 1]

## Data-Challenges Matrix (application papers only)
[from Step 1]

## Prior Work Matrix
[from Step 5.5 — saved as separate file `PRIOR_WORK_MATRIX.md` and summarized here]

## Technical Risk Register
[from Step 5.6 — saved as separate file `TECHNICAL_RISK_REGISTER.md` and summarized here. Any `CRITICAL` or `HIGH` rows must be acknowledged before drafting.]

## Structure
[from Steps 2-3, section by section]

## Assumption Dependency Map
[from Step 5]

## Figure and Table Plan
[from Step 4]

## Citation Plan
[from Step 6]

## Reviewer Feedback
[from Step 7, summarized]

## Next Steps
- [ ] /stat-paper-write to draft LaTeX
- [ ] /paper-figure to generate figures (including EDA figures for application papers)
- [ ] /paper-compile to build PDF
```

## Key Rules

### General rules (all paper types)

- **Large file handling**: If the Write tool fails due to file size, retry using Bash to write in chunks.
- **Do NOT generate author information** — leave anonymous or placeholder
- **Theorems-Evidence Matrix is the backbone** — every theorem must map to verification, every simulation must verify a claim
- **Assumptions are first-class citizens** — plan them as carefully as the theorems
- **Simulation DGPs must be specific** — state the model, parameters, and purpose for each
- **Page budget is soft for journals** but respect venue norms. For COLT/ALT (conferences), the main body limit is hard.
- **Proof plan matters** — decide main body vs supplement allocation during planning, not during writing
- **Open problems in Discussion** — statistics reviewers value honest identification of what remains unknown

### Theory/methodology paper rules

- **Rate comparison table is mandatory** for theory papers — plan it in §3
- **Front-load the contribution** — the one-sentence contribution and main rate should be clear by end of Introduction

### Application paper rules

- **Application papers are data-first** — the dataset and scientific question drive the entire paper plan; method serves the application, not vice versa
- **Findings-Evidence Matrix is mandatory** — every claimed finding must map to specific evidence and validation
- **Data-Challenges Matrix is mandatory** — every methodological choice must be motivated by a documented data feature
- **§2 Data and Background must be substantive** — plan 2-4 pages with EDA figures, not a token paragraph
- **§6 Application must be the largest section** — plan 4-6+ pages with multiple analyses
- **Theory must be light** — plan 1-2 theorems max in main body; bulk of theory goes to supplement
- **Simulation DGPs must be informed by the real data** — sample size, distributions, dependence, missingness should mirror what was observed in §2
- **Domain-standard methods must be in the comparison** — not just statistical baselines
- **Validation must be planned upfront** — holdout, cross-validation, sensitivity analyses are not optional
- **Reproducibility must be planned** — data availability, code repository, replication script all need to be addressed in the plan
- **Both audiences must be served** — the plan should be evaluated for clarity to statisticians AND domain scientists
- **Lead with findings** — application paper abstracts and introductions must name what was discovered, not just what method was used

### Reference reading

- For application papers, **read `../stat-shared-references/stat-application-writing.md`** before finalizing the plan
- For theory papers, **read `../stat-shared-references/stat-theory-writing.md`** when planning §3
- For all papers, **read `../stat-shared-references/stat-venue-checklists.md`** before locking the venue
- For all papers, **read `../stat-shared-references/stat-style-discipline.md`** when planning the contribution bullets, abstract structure, and figure plan
- For all papers, **read `../stat-shared-references/stat-figure-design.md`** when planning the figures and tables

### Planning for Main and Supplement Separation

Plan how the main paper and supplement relate, based on `SUPPLEMENT_MODE` defaults (see `stat-paper-write` Constants for the venue mapping).

For `SUPPLEMENT_MODE = separate_self_contained` (default for JASA, AoS, JRSS-B, Biometrika, AOAS, EJS, Bernoulli, Statistica Sinica, JASA ACS, JCGS, JABES, Statistics in Medicine, MSL): the main paper and supplement will be submitted as two independent PDF files with no cross-file LaTeX references. Plan the section split with this constraint in mind.

For `SUPPLEMENT_MODE = linked_appendix` (default for Biostatistics, COLT, ALT): the supplement is part of the same review workflow and cross-references are expected. The planning constraint is lighter.

The rest of this subsection describes the more demanding `separate_self_contained` case.

- Decide what goes in the main body and what goes in the supplement during planning, not during writing. Moving a proof from main to supplement after writing usually requires restating the theorem.
- The supplement must be self-contained. The plan should identify which theorems, assumptions, and notation will need to be restated at the start of the supplement.
- Cross-references between main and supplement are fragile. Plan for textual references ("Section S.2 of the Supplement") rather than `\ref` cross-file links.
- For application papers, the supplement is often substantial (20-40 pages). Plan its organization: §A Detailed data and preprocessing, §B Proofs, §C Additional simulations, §D Additional analyses, §E Reproducibility.
- For theory papers, plan which proof sketches stay in the main body (the novel arguments) and which full proofs go to the supplement.
- For methodology papers, plan which theoretical properties go to the supplement (often full proofs and extensions) and which stay in the main body (typically consistency and asymptotic distribution statements with sketches).

When planning, write down the supplement structure explicitly:

```markdown
## Supplement Structure

| Section | Content | Pages (est.) |
|---------|---------|--------------|
| S.1 | Proofs of main results (Theorems 1-3 restated) | 8-12 |
| S.2 | Proofs of technical lemmas | 5-8 |
| S.3 | Additional simulation studies | 4-6 |
| S.4 | Additional data analysis [for application papers] | 4-6 |
| S.5 | Reproducibility and software details | 2-3 |
```

This planning step prevents the common failure mode of compiling a supplement that depends on main paper labels and breaks when uploaded as a separate file.
