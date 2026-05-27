# Writing Principles for Statistics Papers

Use this reference when `stat-paper-plan` needs help shaping the paper's story or when `stat-paper-write` needs stronger drafting guidance. This complements the general `writing-principles.md` with statistics-specific conventions.

## Companion References

- `stat-style-discipline.md` covers punctuation rules (em-dash, colon, semicolon), AI-template patterns to avoid, COPSS-style scholar writing patterns, and paragraph and bullet discipline. Read it during any drafting or polishing pass.
- `stat-figure-design.md` covers figure design rules (no titles, caption discipline, legend placement, sizing). Read it before generating any figure.
- `stat-theory-writing.md` covers theorem statements, assumption patterns, proof sketches, rate comparison tables. Read it before writing the main results section.
- `stat-application-writing.md` covers application paper structure (data-first narrative, EDA, application section). Read it before writing an application paper.
- `stat-venue-checklists.md` covers venue-specific requirements. Read it when setting the target venue.

## Contents

- [The Statistics Narrative](#the-statistics-narrative)
- [Theory vs Methodology vs Application Papers](#theory-vs-methodology-vs-application-papers)
- [Time Allocation and Reviewer Expectations](#time-allocation-and-reviewer-expectations)
- [Abstract Formulas](#abstract-formulas)
- [Introduction Structure](#introduction-structure)
- [Mathematical Writing for Statistics](#mathematical-writing-for-statistics)
- [Assumption Writing](#assumption-writing)
- [Theorem Statement Craft](#theorem-statement-craft)
- [Proof Organization](#proof-organization)
- [Simulation Study Design](#simulation-study-design)
- [Real Data Analysis](#real-data-analysis)
- [Discussion Section](#discussion-section)
- [Common Mistakes in Statistics Papers](#common-mistakes-in-statistics-papers)

## The Statistics Narrative

### Core Difference from ML Conference Papers

ML conference papers front-load the contribution and sell the story aggressively. Statistics papers build the argument methodically: problem → model → assumptions → result → verification → interpretation.

The narrative arc of a statistics paper is:

1. **The problem**: what statistical question remains open or poorly addressed
2. **The gap**: why existing methods or theory are insufficient (specific, not vague)
3. **The contribution**: what new estimator, theory, or framework this paper provides
4. **The guarantee**: what theoretical properties hold and under what conditions
5. **The verification**: how simulations and/or data confirm the theory
6. **The boundary**: what assumptions are needed and when they might fail

### One-Sentence Contribution Test (Statistics Version)

If you cannot write one of these, the framing is not ready:

- "We establish the minimax optimal rate for estimating f under assumption class F, and propose an estimator that achieves this rate."
- "We propose a new estimator for θ that achieves √n-consistency and asymptotic normality under weaker conditions than existing methods."
- "We develop a hypothesis testing procedure for H₀ that controls Type I error at level α and achieves power 1 against alternatives separated by Δ ≥ n^{-r}."
- "We introduce a computationally efficient method for X that maintains the statistical optimality of the oracle procedure while running in O(n log n) time."

### Audience Awareness

Statistics reviewers typically:

- Read proofs carefully and check technical correctness
- Evaluate whether assumptions are standard or restrictive
- Compare rates and constants with known optimal results
- Value honest discussion of limitations and failure modes
- Expect simulation studies to verify theoretical predictions
- Care about connections to classical results and methods

## Theory vs Methodology vs Application Papers

Three distinct paper types appear in statistics journals. Each has different priorities, structures, and reviewer expectations.

### Theory Paper

Primary contribution is a new theoretical result (rate, bound, characterization, impossibility).

**Key elements:**
- Clean problem formulation with precisely stated model
- Main theorem(s) with all assumptions listed before the statement
- Rate comparison with prior work (table strongly recommended)
- Proof sketches of key arguments in main body
- Simulations that verify the theoretical predictions quantitatively
- Full proofs in supplement

**Writing priorities:**
1. Clarity of the theorem statement (a reader should understand the result without reading the proof)
2. Intuition for why the result holds
3. Precision of assumptions
4. Connection to existing literature

**Typical venues:** AoS, Bernoulli, JRSS-B, EJS, COLT, ALT, MSL.

### Methodology Paper

Primary contribution is a new statistical method with theoretical backing.

**Key elements:**
- Practical problem motivation (often from a domain application)
- Method description with algorithmic detail
- Theoretical properties (consistency, rates, efficiency)
- Computational considerations (algorithm, complexity, scalability)
- Comprehensive simulation study comparing with existing methods
- Real data analysis demonstrating practical value
- Software availability

**Writing priorities:**
1. Clear description of when and why to use this method
2. How the method works (algorithm, implementation)
3. What guarantees it provides
4. How it compares empirically with alternatives

**Typical venues:** JASA Theory and Methods, JRSS-B, Biometrika, Statistica Sinica, JCGS.

### Application Paper

Primary contribution is solving a real scientific problem using a new or adapted statistical method. Method serves the application, not vice versa.

**Key elements:**
- A specific dataset and a substantive scientific question
- Detailed data description with exploratory analysis
- Statistical challenges arising directly from data characteristics
- Methodology section appropriately scoped to the problem
- Light theory in main body (1-2 theorems max)
- Simulation studies designed to mimic the real data
- **Extensive real data analysis as the centerpiece (4-6+ pages)**
- Substantive scientific findings with domain interpretation
- Validation through holdout, cross-validation, sensitivity analyses
- Practical recommendations for domain scientists
- Data and code availability

**Writing priorities:**
1. The scientific problem and its importance
2. Why the data demands new statistical thinking
3. Substantive findings — what the analysis revealed
4. Reproducibility and practical guidance

**Typical venues:** AOAS (Annals of Applied Statistics), JASA Applications and Case Studies, Biostatistics, Statistics in Medicine, JCGS, JABES.

For application papers, read `stat-application-writing.md` for detailed section-by-section guidance.

### Distinguishing the Paper Type

Ask: "What is the paper *really* about?"

- **Theory paper**: "We characterize the rate / impossibility / structure of..."
- **Methodology paper**: "We propose a new method for [class of problems] with these properties..."
- **Application paper**: "We answer this scientific question about this specific dataset by developing..."

If the paper would not exist without a specific dataset and scientific question, it is an application paper. Section structure, theory depth, and length allocations should follow accordingly.

## Time Allocation and Reviewer Expectations

### Where Effort Should Go (Theory Paper)

Roughly equal time on:
1. Problem setup and assumptions (getting these right determines everything)
2. Main results and proof sketches
3. Simulations that validate the theory
4. Introduction and abstract (the pitch)

### Where Effort Should Go (Methodology Paper)

1. Method description and algorithm
2. Simulation study design and execution
3. Theoretical analysis
4. Introduction, abstract, and real data analysis

### Where Effort Should Go (Application Paper)

1. The application section itself — this is the centerpiece
2. Data and Scientific Background — must be thorough and visually rich
3. Substantive interpretation and validation
4. Introduction (especially framing the scientific question)
5. Methodology (kept appropriately scoped)
6. Simulation studies (designed to resemble the real data)

Light theory ranks lower in priority; aim for 1-2 clean theorems in the main body and put the rest in the supplement.

### Reviewer Reading Order (Statistics)

Most statistics reviewers read:

1. Abstract → do I care about this problem?
2. Introduction → is the contribution clear and positioned correctly?
3. Main results / theorems → are the results strong and stated cleanly?
4. Assumptions → are these standard or restrictive?
5. Simulations → do they actually verify what the theory predicts?
6. Proofs (supplement) → is the analysis technically correct?

**Implication:** The assumption list and theorem statements must be polished to a very high standard. A reviewer who cannot quickly parse the main theorem will not engage deeply with the proofs.

## Abstract Formulas

### Theory Paper Abstract (5-6 sentences)

1. Problem context: what statistical problem, in what setting
2. Gap: what is unknown or suboptimal in existing work
3. Main result: the theorem in plain language with the rate or bound
4. Approach: the proof technique or key insight
5. Verification: simulation or data confirmation
6. Implication: what this enables or resolves

### Methodology Paper Abstract (5-6 sentences)

1. Problem motivation: what practical problem, why it matters
2. Limitation of current methods: what fails or is missing
3. Proposed method: what the new approach does
4. Theory: what guarantees it provides
5. Empirical evidence: simulation and/or data results
6. Impact: what practitioners gain

### Application Paper Abstract (5-7 sentences)

1. Scientific question and dataset: what substantive question is being asked and which dataset enables it
2. Statistical challenge: what feature of the data makes standard analysis inadequate
3. Proposed approach: what method is developed or adapted
4. Application result: what the analysis discovered (the most important sentence — name the finding)
5. Validation: how the finding was checked (cross-validation, sensitivity, comparison)
6. Implication: what this means for the domain
7. (Optional) Code/data availability or method generality

An application-paper abstract that does not name a substantive finding has failed. The reviewer must learn what was discovered, not just what method was used.

### Openings to Avoid

- "Statistical inference has attracted increasing attention..." (too vague)
- "High-dimensional data analysis is an important problem..." (tells the reviewer nothing specific)
- "In recent years, many methods have been proposed for..." (every paper can say this)

Instead, open with the specific problem this paper addresses.

## Introduction Structure

### Theory Paper Introduction (2-3 pages)

1. **Problem statement** (1-2 paragraphs): The statistical problem, why it matters, the model or framework
2. **Prior work and gap** (2-3 paragraphs): What is known, what rates/bounds exist, what remains open
3. **Contribution** (1 paragraph): The main result(s) in plain language, numbered if multiple
4. **Proof technique overview** (1 paragraph): Key technical insight, novel tools or arguments
5. **Paper organization** (1 paragraph): Roadmap of remaining sections

### Methodology Paper Introduction (2-3 pages)

1. **Motivation** (1-2 paragraphs): The practical problem, a running example if helpful
2. **Existing approaches and limitations** (2-3 paragraphs): What methods exist, why they are insufficient
3. **Proposed method** (1 paragraph): High-level description of the new approach
4. **Theoretical and empirical highlights** (1 paragraph): Key properties and strongest results
5. **Contribution list** (numbered bullets): 2-4 specific, verifiable contributions
6. **Notation and organization** (1 paragraph): Notation conventions and roadmap

### Application Paper Introduction (2-3 pages)

1. **Scientific question** (1 paragraph): the substantive question, why the domain cares
2. **The dataset** (1 paragraph): brief introduction of the data with stakes-relevant context
3. **Statistical challenges** (1-2 paragraphs): what features of the data make standard analysis inadequate
4. **Limitations of current approaches** (1 paragraph): what is done in the domain today and why it falls short
5. **Proposed approach** (1 paragraph): the method and what it enables
6. **Substantive findings preview** (1 paragraph): what the analysis discovered
7. **Contributions** (numbered): 2-4 contributions spanning method and findings
8. **Organization** (1 paragraph): section roadmap

Application paper introductions differ from theory and methodology introductions in that they **lead with the science and end with the findings**, not with the method.

### Contribution Bullets (Statistics Style)

Good (theory/methodology):
- We establish the minimax optimal rate of convergence O(n^{-2s/(2s+d)}) for estimating f ∈ F_{s,d} and show that our kernel estimator achieves this rate adaptively.
- We prove that the proposed test has exact asymptotic level α and is consistent against all fixed alternatives, with power approaching 1 at rate n^{-1/2}.
- We develop an ADMM algorithm that solves the optimization in O(np) time per iteration and prove convergence to a stationary point.

Good (application):
- We develop a hierarchical spatial-temporal model for [phenomenon] that accommodates [data feature 1] and [data feature 2], previously handled separately or not at all.
- Applied to [specific dataset], our analysis reveals [specific scientific finding] — a pattern that classical [standard method] obscures.
- We provide a publicly available [R/Python] package and complete replication code, lowering the barrier for [domain practitioners] to adopt the approach.

Bad:
- We study the estimation problem. (no specifics)
- We provide theoretical analysis. (what kind?)
- We conduct extensive simulations. (every paper does this)
- We apply our method to real data. (which data? what finding?)

## Mathematical Writing for Statistics

### Notation Conventions

Statistics papers typically use:

```latex
% Scalars: lowercase Greek or Latin
$\theta$, $\beta$, $\sigma$, $n$, $p$, $d$

% Vectors: bold lowercase
$\boldsymbol{\beta}$, $\boldsymbol{\theta}$, $\mathbf{x}$

% Matrices: bold uppercase
$\mathbf{X}$, $\boldsymbol{\Sigma}$, $\mathbf{H}$

% Random variables: uppercase
$X$, $Y$, $Z$, $\varepsilon$

% Spaces and sets: calligraphic or blackboard bold
$\mathcal{F}$, $\mathcal{H}$, $\mathbb{R}^d$, $\mathbb{P}$

% Operators: Roman upright
$\mathbb{E}$, $\mathrm{Var}$, $\mathrm{Cov}$, $\mathrm{tr}$, $\sup$, $\inf$

% Norms: double bars
$\|\cdot\|$, $\|\cdot\|_2$, $\|\cdot\|_{\infty}$

% Probability/expectation: blackboard bold
$\mathbb{P}$, $\mathbb{E}$

% Convergence: specific arrows
$\xrightarrow{d}$, $\xrightarrow{p}$, $\xrightarrow{a.s.}$
```

### Key Mathematical Phrasing

For stating results, prefer precise language:

| Weak | Strong |
|------|--------|
| "the estimator works well" | "the estimator achieves the rate n^{-2s/(2s+d)}" |
| "the bound is tight" | "the bound matches the minimax lower bound up to logarithmic factors" |
| "under mild conditions" | "under Assumptions (A1)-(A3)" |
| "with high probability" | "with probability at least 1 - δ" |
| "for large n" | "for all n ≥ n_0 where n_0 depends only on d and s" |

### Proof Sketch Writing

A proof sketch in the main body should:

1. State the key decomposition or reduction
2. Identify the main technical challenge
3. Explain the novel step that overcomes it
4. Point to the supplement for full details

Template:
```
The proof proceeds in three steps. First, we decompose the risk into 
a bias term and a stochastic term (Lemma X). The bias term is bounded 
by standard approximation theory. The main challenge lies in the 
stochastic term, where we develop a new chaining argument that 
exploits the specific structure of [class F]. This yields [rate]. 
The full proof is given in Section A of the supplement.
```

## Assumption Writing

### Structure

Assumptions should be:
- Labeled consistently: (A1), (A2), ... or (C1), (C2), ...
- Stated formally before the first theorem that uses them
- Grouped logically: model assumptions, then regularity conditions, then identifiability
- Discussed after stating: which are standard, which are novel, which can be relaxed

### Template

```latex
\begin{assumption}[Smoothness]\label{ass:smoothness}
The regression function $f_0$ belongs to the Sobolev ball 
$\mathcal{W}^{s,2}(L) = \{f : \sum_{|\alpha| \leq s} \|\partial^\alpha f\|_2 \leq L\}$
for some $s > d/2$ and $L > 0$.
\end{assumption}
```

### Discussion After Assumptions

Always include a paragraph after the assumptions that:
- Identifies which assumptions are standard in the literature
- Points out which are new or stronger/weaker than usual
- Discusses when they might fail
- Compares with assumptions in key prior works

Example:
```
Assumption (A1) is standard in nonparametric regression and is 
assumed in [refs]. Assumption (A2) is weaker than the sub-Gaussian 
requirement in [ref], as we only require finite fourth moments. 
Assumption (A3) on the design density is needed for uniform 
convergence and can be relaxed to hold locally; see Remark 2 below.
```

## Theorem Statement Craft

### Rules for Clean Theorem Statements

1. **List all assumptions by label** before the theorem, or in the theorem preamble
2. **State the result precisely**: rate, constants (or their dependence), probability
3. **Use standard convergence notation**: O_p, o_p, ≍, ≲, ≳
4. **Separate the statement from interpretation**: the theorem is the formal claim; the discussion after it provides intuition

### Template

```latex
\begin{theorem}[Upper bound]\label{thm:upper}
Suppose Assumptions~\ref{ass:smoothness}--\ref{ass:design} hold. 
Let $\hat{f}_n$ be the estimator defined in~\eqref{eq:estimator} 
with bandwidth $h = h_n \asymp n^{-1/(2s+d)}$. Then
\[
  \sup_{f_0 \in \mathcal{W}^{s,2}(L)} 
  \mathbb{E}\bigl[\|\hat{f}_n - f_0\|_2^2\bigr] 
  \leq C \, n^{-2s/(2s+d)},
\]
where $C > 0$ depends only on $s$, $d$, $L$, and the constants 
in Assumptions~\ref{ass:smoothness}--\ref{ass:design}.
\end{theorem}
```

### After the Theorem

Always follow with:
1. **Interpretation**: what the rate means, how it compares
2. **Rate comparison**: table or inline comparison with prior bounds
3. **Optimality discussion**: is this minimax optimal? Up to what factors?
4. **Remarks**: extensions, special cases, connections

## Proof Organization

### Main Body vs Supplement

**Main body** should contain:
- Proof sketches of main theorems (1-2 paragraphs each)
- Key lemmas that carry the main insight
- Proof of the most novel technical step (if short enough)

**Supplement** should contain:
- Full proofs of all theorems
- Proofs of supporting lemmas
- Verification of technical conditions
- Additional simulation results
- Extended real data analysis

### Proof Hierarchy

Organize proofs in the supplement to mirror the main body:
```
Appendix A: Proofs for Section 3 (Main Results)
  A.1: Proof of Theorem 1
  A.2: Proof of Theorem 2
  A.3: Proof of Corollary 1
Appendix B: Proofs of Technical Lemmas
  B.1: Proof of Lemma 1
  B.2: Proof of Lemma 2
Appendix C: Additional Simulations
Appendix D: Additional Data Analysis
```

## Simulation Study Design

### Purpose

Simulations in statistics papers serve to:
1. Verify theoretical predictions (rates, coverage, power)
2. Compare the proposed method with existing alternatives
3. Investigate finite-sample behavior beyond what theory covers
4. Explore sensitivity to assumption violations

### Data Generating Process (DGP) Design

Every simulation must specify:
- The model: $Y = f(X) + \varepsilon$ or similar
- Distribution of covariates: $X \sim$ what?
- Distribution of errors: $\varepsilon \sim$ what?
- True parameter values or functions
- Sample sizes: multiple (e.g., n = 100, 500, 2000)
- Number of replications: typically 500-1000

### Essential Elements

1. **Multiple DGPs**: at least 2-3 scenarios testing different aspects
2. **Multiple sample sizes**: to verify convergence rates
3. **Comparison methods**: 3-5 existing methods (not just the oracle)
4. **Relevant metrics**: MSE, coverage, power, computation time
5. **Standard errors**: from Monte Carlo replications
6. **Rate verification**: log-log plots of error vs n to verify theoretical rates

### Table Format

Standard simulation table:
```
Method  | n=100      | n=500      | n=2000
        | MSE (SE)   | MSE (SE)   | MSE (SE)
--------|------------|------------|----------
Proposed| 0.045(003) | 0.012(001) | 0.003(000)
Method A| 0.067(004) | 0.018(002) | 0.005(001)
Method B| 0.089(005) | 0.032(003) | 0.011(001)
Oracle  | 0.038(002) | 0.010(001) | 0.003(000)
```

### Writing Simulation Results

- Lead with the main finding, not the setup
- Point the reader to what they should notice in each table/figure
- Compare rates explicitly: "The proposed method's MSE decreases at rate n^{-0.8}, consistent with the theoretical rate n^{-4/5}"
- Discuss when the method underperforms and why

## Real Data Analysis

### Purpose

Real data analysis demonstrates that:
1. The method works on data that was not designed to favor it
2. The results are substantively interpretable
3. The method provides insights that existing methods miss

### Standards

- Describe the dataset: source, size, variables, preprocessing
- Explain why this dataset is appropriate for the method
- Report results with appropriate uncertainty quantification
- Compare with the same methods used in simulations
- Provide domain interpretation when possible
- Discuss limitations specific to this application

### For Application Papers

For application papers, the real data analysis is **not a small demonstration section** — it is the centerpiece of the paper.

Plan for 4-6+ pages of detailed analysis including:
- Multiple analyses or views of the data
- Comparison with the methods practitioners actually use
- Holdout / cross-validation evidence
- Sensitivity to modeling choices
- Substantive interpretation tied to the scientific literature
- Practical recommendations

Read `stat-application-writing.md` for a detailed guide to writing this section in application papers.

### Application Paper Specific Patterns

- Lead with the scientific question, not the method
- Tell the reader what to notice in every figure
- Show what the new method reveals that standard methods miss
- Acknowledge what the analysis cannot conclude
- Provide concrete recommendations to domain scientists

## Discussion Section

Statistics papers typically end with a Discussion (not just Conclusion). This section should cover:

1. **Summary of contributions**: restate in context, not copy-paste
2. **Connections to prior work**: how results relate to or improve upon existing theory
3. **Limitations**: assumptions that may be restrictive, settings not covered
4. **Open problems**: specific technical questions that remain
5. **Extensions**: natural generalizations the current framework supports

### Tone

Statistics discussions are more measured than ML conclusions. Avoid:
- "Our groundbreaking method revolutionizes..."
- "This opens exciting new avenues..."
- "The results are remarkable..."

Prefer:
- "The proposed estimator achieves the minimax rate under conditions (A1)-(A3). Whether the sub-Gaussian assumption (A2) can be relaxed to sub-exponential remains an open question."

## Common Mistakes in Statistics Papers

### Theory Mistakes

| Mistake | Fix |
|---------|-----|
| Assumptions stated after the theorem | Move assumptions before the first theorem that uses them |
| "Under mild/standard conditions" without specifics | List actual assumptions by label |
| Rate comparison buried in text | Add a comparison table |
| No proof sketch in main body | Add 1-2 paragraph sketch for each main theorem |
| Minimax lower bound claimed but not proved | Either prove it or cite the source explicitly |
| Constants hidden in O(·) notation without discussion | Discuss what constants depend on |

### Simulation Mistakes

| Mistake | Fix |
|---------|-----|
| Only one sample size | Use at least 3 sample sizes spanning an order of magnitude |
| No standard errors | Report Monte Carlo standard errors |
| Missing comparison methods | Include 3-5 established alternatives |
| DGP designed to favor proposed method | Include adversarial/challenging DGPs |
| No rate verification | Add log-log plots of error vs n |
| Unstated number of replications | Always state (typically 500-1000) |

### Writing Mistakes

| Mistake | Fix |
|---------|-----|
| Introduction reads like a textbook chapter | Start from the specific problem, not the field |
| Related work is a bibliography dump | Organize by approach/assumption, synthesize and position |
| Notation inconsistent across sections | Define a notation table, use math_commands.tex |
| Discussion is just a summary | Add limitations, open problems, extensions |
| Paper too long for the content | Move secondary results to supplement |
