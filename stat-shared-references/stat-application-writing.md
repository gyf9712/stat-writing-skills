# Application Paper Writing Guide for Statistics

Use this reference for **application papers** — those targeting JASA Applications and Case Studies (JASA ACS), Annals of Applied Statistics (AOAS), Biostatistics, Statistics in Medicine, JCGS, JABES, and similar applied-statistics venues.

Application papers differ fundamentally from theory and methodology papers. The paper is anchored in a real problem and a specific dataset; the method exists to serve the application; theory is minimal in the main text; the real-data analysis section is the centerpiece.

## When to Read

- Before drafting the Introduction for an application paper
- Before writing the Data and Background section
- Before designing the simulation study (which must mirror the real data)
- Before writing the Application / Real Data Analysis section
- When deciding what theory belongs in the main body vs supplement
- When the paper is being repositioned from theory/methodology to application

## What Makes an Application Paper Different

### The Three Paper Types

| Aspect | Theory Paper | Methodology Paper | Application Paper |
|--------|--------------|-------------------|-------------------|
| Primary contribution | New rate, bound, characterization | New method with theory | Solving a real scientific problem |
| Driver | A theoretical gap | A methodological limitation | A specific dataset and scientific question |
| Theorems in main text | 3-6+ | 2-4 | 1-2 (or none) |
| Simulation studies | Verify theory | Compare with alternatives | Mimic real data characteristics |
| Real data analysis | Optional | Recommended (1 dataset) | Central, often multiple analyses |
| Length of application section | 0-2 pages | 2-3 pages | 4-6+ pages (largest section) |
| Reviewer focus | Proof correctness, rate optimality | Method properties + empirics | Substantive insights + reproducibility |
| Tone | Mathematical, precise | Methodological, balanced | Scientific, interpretive |

### The Two Audiences

Application papers must serve two audiences simultaneously:

1. **Statisticians** evaluating the methodological contribution
2. **Domain scientists** (biologists, economists, climatologists, etc.) who want to use or replicate the analysis

The writing must satisfy both without alienating either. The Introduction and Application sections especially need careful balance.

## The Application Paper Narrative Arc

The story flows as:

```
Real problem
    → Real data
        → Data characteristics that pose statistical challenges
            → Why existing methods fail or are inadequate
                → Proposed method as a response
                    → Method works (theory + simulation)
                        → Method illuminates the real problem
                            → Scientific implications + recommendations
```

The method does **not** drive the paper. The problem drives the paper, and the method is the solution.

### One-Sentence Contribution Test (Application Version)

If you cannot write one of these, the framing is not ready:

- "We develop a new spatial model for [application] that accommodates [data feature], and use it to discover [scientific finding] in [specific dataset]."
- "We propose a method for [problem] that addresses [data challenge], enabling [practical capability] previously unavailable, illustrated by analysis of [dataset]."
- "We provide the first [method-type] framework for [application]; applied to [data], it reveals [insight] that classical approaches miss."

Notice that all of these:
- Name the application explicitly
- Reference a specific dataset
- Highlight what the analysis *finds*, not just what the method *does*

## Application Paper Structure

### Default Section Layout (8 sections, ~25-35 pages)

```
1. Introduction (2-3 pages)
2. Data and Scientific Background (2-4 pages)   ← unique to application papers
3. Methodology (3-4 pages)
4. Theoretical Properties (1-2 pages)           ← light: 1-2 theorems max
5. Simulation Studies (2-3 pages)
6. Application / Real Data Analysis (4-6 pages) ← LARGEST SECTION
7. Discussion (1-2 pages)
— Supplement: heavier theory, additional simulations, additional data analysis
```

### Alternative Layout (Method-light Application, 6-7 sections)

```
1. Introduction
2. The [Scientific] Problem and Data
3. Statistical Model and Estimation
4. Simulation Studies
5. Application: [Specific Analysis Name]
6. Application: [Second Analysis or Validation]
7. Discussion
```

This layout is common when two related analyses or two datasets are presented.

### Alternative Layout (Heavily Validated Application, with strong methodology)

```
1. Introduction
2. Motivating Data
3. Methodology
4. Theoretical Analysis
5. Computation
6. Simulation Studies
7. Application
8. Sensitivity and Validation
9. Discussion
```

The "Sensitivity and Validation" section is more common in AOAS-style papers where holdout validation, cross-validation, and stress-testing are critical.

## Section-by-Section Guidance

### §1 Introduction

The Introduction must accomplish more than in theory papers:

1. **Hook with the scientific problem** (1 paragraph)
   - State the substantive scientific or applied question
   - Name the domain and stakes
   - Examples: "Understanding how species respond to climate warming...", "Detecting anomalies in critical infrastructure networks...", "Predicting patient survival under different treatment regimens..."

2. **Introduce the data informally** (1 paragraph)
   - "We study a dataset of [size, scope] collected from [source]..."
   - Mention 1-2 key data characteristics that pose challenges
   - Do NOT do full data description here — that comes in §2

3. **Statistical challenges from the data** (1-2 paragraphs)
   - What features of this data make standard analysis inadequate
   - Examples: spatial dependence, missing not-at-random, mixed data types, dimension, censoring, irregular sampling
   - This is where the methodological gap is established

4. **Limitations of existing approaches** (1 paragraph)
   - What current methods are used in this domain
   - Why they fall short for this problem
   - Cite both statistical and domain literature

5. **Proposed approach** (1 paragraph)
   - High-level description of the method
   - What it does differently
   - What new analyses it enables

6. **Substantive findings preview** (1 paragraph)
   - What did the analysis discover?
   - Why is this scientifically interesting?
   - This is what distinguishes application papers — preview the *insight*, not just the rate

7. **Contributions and organization** (final paragraph)
   - 2-4 specific bullets (methodological + applied)
   - Section roadmap

**Target: 2-3 pages.**

#### Application Paper Contribution Bullets

Good:
- We develop a hierarchical spatial point process model that accommodates non-stationary intensity and dependence between species occurrence and habitat covariates.
- Applied to 12 years of bird survey data from the North American Breeding Bird Survey, our analysis reveals that [specific finding] — a pattern obscured by classical CAR models.
- We provide an efficient MCMC algorithm and release an R package, enabling ecologists to fit the model on standard hardware.

Bad:
- We propose a new spatial model. (no specifics)
- We apply our method to bird data. (no scientific finding)
- We provide theoretical analysis. (theory is rarely the main contribution here)

### §2 Data and Scientific Background

This section is unique to application papers and is often underweighted by statisticians used to writing theory.

#### Required Elements

1. **Scientific/domain context** (1-3 paragraphs)
   - Why this question matters in the field
   - Brief history or current state of knowledge
   - What domain scientists want to know

2. **Data source and collection** (1-2 paragraphs)
   - Where the data comes from (study, registry, survey, sensor network)
   - Collection methodology, sampling design, time period
   - Inclusion/exclusion criteria
   - Provenance and access information

3. **Data structure** (1 paragraph)
   - Sample size, dimensions, observation units
   - Variable types (continuous, categorical, time-to-event, spatial coordinates)
   - Hierarchical or temporal structure

4. **Exploratory data analysis (EDA)** (2-4 figures/tables, 1-2 pages)
   - Visual summaries showing the key data features
   - Tables of descriptive statistics
   - Anything that motivates the methodological choices
   - **These figures often become the most-cited visuals in the paper**

5. **Statistical challenges revealed by EDA** (1 paragraph)
   - "From Figure 2 we observe..."
   - "Table 1 shows that..."
   - Connect specific data features to specific methodological needs
   - This bridges to the Methodology section

6. **Preprocessing** (optional, 1 paragraph or push to supplement)
   - Cleaning, harmonization, missing data handling
   - Be transparent — reproducibility matters
   - Detail can go to supplement

#### Writing Standards

- **Use the dataset's actual name** consistently (e.g., "the MIMIC-III ICU database", "the North American BBS")
- **Cite the data source paper** if one exists
- **Acknowledge data limitations** honestly — these may motivate sensitivity analyses later
- **Domain terminology** should be defined on first use for statistical readers

#### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Data described in a single dense paragraph | Break into structured subsections with EDA figures |
| EDA figures buried in supplement | Put key EDA visuals in the main text |
| Statistical challenges asserted without evidence from the data | Show the challenge via EDA, then state it |
| Domain context too sparse for non-experts | Add 1-2 paragraphs of accessible background |
| Domain context dominates and loses the statistician | Keep stats relevance front and center |

### §3 Methodology

In an application paper, the methodology section is leaner than in a methodology paper.

#### Structure

1. **Model formulation** (1-2 pages)
   - Connect notation to the data (use the variable names from §2)
   - State the model carefully but without excessive generality
   - Use domain-natural parameterization where possible

2. **Estimation** (1-2 pages)
   - The estimator/algorithm
   - Tuning parameter selection (often a key practical contribution)
   - Computational notes

3. **Inference** (often a short subsection)
   - How uncertainty is quantified (bootstrap, asymptotic CI, Bayesian credible intervals)
   - Why this approach is appropriate for the application

#### Avoid

- Long sections of pure mathematical setup divorced from the data
- Notation that doesn't connect to the data variables
- Lengthy proofs in the methodology section (move them to §4 or supplement)
- Excessive generality (state the model for the application's setting, not for an abstract class)

### §4 Theoretical Properties (Optional, Light)

Application papers should have **1-2 main theorems at most** in the main text.

#### What to Include

- **Consistency or convergence rate** for the proposed estimator
- **Asymptotic distribution** if used for inference
- **Identifiability** if it is non-trivial for this setting
- Connection to a known framework (e.g., "Theorem 1 establishes that our estimator falls within the framework of [class] and inherits its asymptotic normality")

#### What to Move to Supplement

- Detailed proofs (always)
- Auxiliary lemmas
- Extensions to general settings
- Minimax considerations (usually not the main concern for application papers)

#### Writing Style

The 1-2 theorems should be stated cleanly with all assumptions, but discussion can be brief. A typical pattern:

```
Theorem 1 (Consistency). [statement]

This result confirms that our estimator is asymptotically consistent
under standard regularity conditions. The conditions are mild and
satisfied in our application; see Remark 1 for verification.
The proof, given in Supplement Section B, follows the framework
of [classical reference] adapted to handle [feature specific to
this setting].
```

### §5 Simulation Studies

Simulations in application papers serve a different purpose than in theory papers.

#### Purpose

1. Verify the method works on data **resembling the real data**
2. Compare with alternative methods that practitioners might use
3. Stress-test under conditions that approximate or exceed the real data's challenges
4. Provide finite-sample evidence the theory does not (since theory is light)

#### Design Principles

- **DGPs should mimic the real data**: sample size, covariate distributions, missingness patterns, dependence structures should be informed by what was observed in §2
- **Include the "scientifically realistic" scenario**: parameters set near those estimated from the real data
- **Include extreme scenarios**: stronger missingness, smaller sample, higher dimension — to probe robustness
- **Compare with methods used in the domain**: not just statistical baselines, but methods the application community currently uses
- **Match metrics to the application**: if the application cares about prediction, measure prediction error; if calibration, measure calibration

#### Reporting

- Tables with Monte Carlo standard errors
- Figures showing distributions across replications, not just means
- If the application has a critical metric (e.g., calibration for clinical prediction), prioritize it

### §6 Application / Real Data Analysis

**This is the longest, most important section of the paper.**

Treat this section like a mini-paper of its own with its own narrative arc.

#### Recommended Internal Structure

1. **Analysis setup** (0.5 pages)
   - Reiterate the scientific question (now specific)
   - Describe the analytic pipeline at high level
   - State what would constitute a meaningful finding

2. **Main analysis** (2-3 pages)
   - Apply the method to the data
   - Report parameter estimates with uncertainty
   - Present 2-4 high-quality figures showing key results
   - Walk the reader through the findings

3. **Comparison with existing approaches** (0.5-1 page)
   - Apply 1-2 standard methods used in the domain to the same data
   - Show what the new method reveals that they miss
   - Be fair — acknowledge what the alternatives do well

4. **Validation** (1-1.5 pages)
   - Holdout or cross-validation
   - Out-of-sample prediction (if applicable)
   - Sensitivity to modeling choices
   - Robustness across data subsets

5. **Substantive interpretation** (0.5-1 page)
   - What do the results mean for the domain?
   - Connect findings back to the scientific literature
   - State explicitly what is new

#### Quality Standards

- **Every figure must add insight** — not redundant with tables
- **Captions must be self-contained** — a reviewer reading only figures should follow the analysis
- **Domain terminology** should be precise and consistent
- **Uncertainty quantification** for every estimate that matters
- **Be explicit about what the analysis cannot conclude** — overclaiming is fatal in application papers

#### Showing the Reader What to See

Application sections often have multi-panel figures or complex tables. Always:

1. Tell the reader **what to look at first**: "Figure 5 shows..."
2. Tell the reader **what they should notice**: "The notable feature is..."
3. Tell the reader **why it matters**: "This pattern indicates..."

Without this guided tour, complex visualizations become noise.

#### Example Narrative Pattern

```
We applied the proposed method to [data]. Figure 5 displays the
estimated [quantity] across [units]. Three features stand out.
First, [observation 1] — this is consistent with [prior knowledge]
but estimated with substantially tighter uncertainty than in
[prior analysis]. Second, [observation 2] — a previously
unreported pattern. Third, [observation 3] is at odds with
[hypothesis from literature]; we explore this further in Section 6.3.

To validate these findings, we compare with the [standard method]
commonly used in [domain]. Figure 6 (top panel) shows that the
standard method [behavior], whereas the proposed method
[behavior]. Holdout validation (Section 6.4) confirms that the
proposed method achieves [metric] [comparison].
```

### §7 Discussion

Application paper discussions should cover:

1. **Substantive findings summary** (1-2 paragraphs)
   - What we learned about the scientific problem
   - How this changes or refines the field's understanding

2. **Methodological summary** (1 paragraph)
   - What the new method contributes
   - When practitioners should consider using it

3. **Practical recommendations** (1 paragraph) — *unique to application papers*
   - For domain scientists: when and how to use the method
   - Computing requirements, software availability
   - Data requirements

4. **Limitations** (1-2 paragraphs)
   - Data limitations (selection, measurement, missingness)
   - Modeling assumptions that may not hold elsewhere
   - Generalizability

5. **Extensions and open questions** (1 paragraph)
   - Where the method could go next
   - Related applications worth pursuing

### Supplement

For application papers, the supplement typically contains:

```
Appendix A: Detailed data description (variables, preprocessing)
Appendix B: Proofs of theoretical results
Appendix C: Additional simulations
  C.1: Extended simulation results
  C.2: Sensitivity to model misspecification
Appendix D: Additional data analysis
  D.1: Subgroup analyses
  D.2: Alternative model specifications
  D.3: Diagnostic plots
Appendix E: Software documentation and reproducibility
```

## Reproducibility Standards for Application Papers

Application papers have particularly stringent reproducibility expectations. Plan for:

- **Code availability**: provide a public repository (GitHub, OSF) at submission
- **Data availability statement**: explicitly state where data can be obtained, including any restrictions
- **Computational environment**: software versions, key dependencies
- **Random seeds**: for any stochastic component (MCMC, bootstrap)
- **Computational requirements**: rough wall-clock and memory needs
- **Replication script**: a single script that reproduces all figures and tables

Many journals (AOAS, Biostatistics, JCGS) now have explicit reproducibility editors.

## Data Description Patterns

### High-Quality EDA Tables

A descriptive statistics table for an application paper might include:

```latex
\begin{table}[t]
\centering
\caption{Characteristics of the [dataset name]. Continuous variables
shown as median (IQR); categorical variables as count (\%).
Stratification by [primary grouping variable].}
\label{tab:demographics}
\begin{tabular}{lccc}
\toprule
                          & Overall      & Group A      & Group B \\
                          & (n = N)      & (n = n_A)    & (n = n_B) \\
\midrule
Age                       & 64 (52, 73)  & 62 (50, 71)  & 68 (55, 76) \\
Sex (female)              & 421 (52\%)   & 215 (51\%)   & 206 (53\%) \\
[Other variables]         &              &              & \\
\midrule
Outcome incidence         & 187 (23\%)   & 75 (18\%)    & 112 (29\%) \\
Median follow-up (months) & 18 (6, 36)   & 22 (8, 42)   & 14 (5, 30) \\
\bottomrule
\end{tabular}
\end{table}
```

### High-Quality EDA Figures

Common application-paper EDA visuals:

- **Spatial data**: map of observations colored by primary outcome
- **Time series**: trajectories with mean overlay
- **Survival**: Kaplan-Meier curves
- **Multivariate**: pairs plots, correlation heatmaps
- **Missingness**: missingness pattern matrix
- **Network**: graph visualization with node attributes

### Linking EDA to Method

The key skill in application paper writing: pivot smoothly from "what we see in the data" to "what we need from a method."

```
Figure 3 reveals two features of the data that pose challenges for
standard analysis. First, [feature 1] is incompatible with the
independence assumption of generalized linear models. Second,
[feature 2] suggests substantial heterogeneity that pooled estimation
would obscure. These observations motivate the [method type]
introduced in Section 3.
```

## Voice and Tone

Application papers are typically written with a **measured, scientific tone** that balances precision with accessibility.

### Avoid

- ML-style hype: "groundbreaking", "revolutionary", "state-of-the-art"
- Pure-theory abstraction without grounding
- Domain jargon without definition
- Overclaiming what the analysis can conclude

### Prefer

- "Our analysis suggests..." over "We prove..."
- "Consistent with [prior work]..." or "In contrast to [prior work]..."
- "This finding implies..." paired with explicit limitations
- "Practitioners should consider..." in the discussion

## Common Failure Modes

| Failure | Diagnosis | Fix |
|---------|-----------|-----|
| Application section is short and superficial | Authors treated it as an obligatory demo | Make application the largest section; develop multiple analyses |
| No clear scientific finding | Method is in search of a problem | Reframe around what was actually discovered |
| Data described too briefly | Stat-paper habit of compression | Expand §2; add EDA figures |
| Theory dominates the paper | Wrong paper type chosen | Move theory to supplement; refocus on application |
| Simulations don't resemble real data | DGP designed in isolation | Re-design DGPs using parameters from real data |
| No comparison with domain-standard methods | Compared only to statistical baselines | Add comparison with methods used by the application community |
| Validation is missing or shallow | Statistical paper habits | Add holdout, cross-validation, sensitivity analyses |
| Reproducibility unclear | Code and data not addressed | Add data/code availability statement and repository link |
| Findings overclaim | Excitement about results | Add explicit "what this analysis cannot conclude" |

## Application Paper Submission Checklist

Before submitting:

- [ ] The scientific question is stated in the first paragraph of the Introduction
- [ ] A specific dataset is named in the Introduction and used throughout
- [ ] Data and Scientific Background section is at least 2 pages with EDA figures
- [ ] Methodology is appropriately scoped (not over-generalized)
- [ ] Theory is light in main body (1-2 theorems max), heavier results in supplement
- [ ] Simulation DGPs are informed by the real data
- [ ] Application section is the longest section (4-6 pages)
- [ ] Comparison includes methods used by domain practitioners
- [ ] Validation includes holdout/cross-validation/sensitivity
- [ ] Substantive findings are explicit and interpreted
- [ ] Discussion includes practical recommendations
- [ ] Limitations are honestly discussed
- [ ] Data availability statement is included
- [ ] Code availability statement is included
- [ ] Reproducibility is addressed concretely
- [ ] Domain terminology is consistent and defined
- [ ] Two audiences (statisticians + domain scientists) are both served
