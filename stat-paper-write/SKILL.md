---
name: stat-paper-write
description: "Draft a statistics, applied statistics, or ML theory LaTeX paper section by section from an outline. Supports theory, methodology, and application paper types. Use when user says \"写统计论文\", \"write stat paper\", \"draft statistics LaTeX\", \"统计应用论文写作\", \"write application paper\", or wants to generate LaTeX for AoS, JASA T&M, JASA ACS, AOAS, JRSS-B, Biometrika, Bernoulli, EJS, Statistica Sinica, Biostatistics, JCGS, COLT, or ALT."
argument-hint: [venue-or-section]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Stat Paper Write: Section-by-Section LaTeX Generation

Draft a statistics, applied statistics, or ML theory LaTeX paper based on: **$ARGUMENTS**

## Constants

- **CLAUDE_REVIEWER_MODEL = `claude-opus-4-6`** — Claude model invoked via the Agent tool for internal subagent review.
- **CODEX_REVIEWER_MODEL = `gpt-5.4`** — External LLM invoked via Codex MCP for senior-statistician external review at `model_reasoning_effort: xhigh`.
- **REVIEW_MODE = `both`** — Options: `claude`, `codex`, `both`. Default `both` for journal submissions. Switch to `claude` for quick drafting iteration.
- **SUPPLEMENT_MODE** — controls how the skill writes supplementary material and how the main paper refers to it.
  - `separate_self_contained`: the main paper and supplement are separate submission artifacts. Do not use cross-file LaTeX references. Cite the supplement textually or bibliographically from the main paper. Make the supplement readable on its own.
  - `linked_appendix`: the supplement is expected to be explicitly referenced from the main paper, or the venue normally treats appendix/supplement linkage as part of the workflow. Cross-references from the main paper to the supplement are allowed when the venue supports them.
- **Default `SUPPLEMENT_MODE` mapping used by this skill family**:
  - `separate_self_contained`: AOS, AOAS, BERNOULLI, BIOMETRIKA, EJS, JASA, JASA_ACS, JRSSB, STATSINICA, MSL, JCGS, JABES, STATMED
  - `linked_appendix`: BIOSTATISTICS, COLT, ALT
- **Override rule**: these are defaults, not absolute claims. If the user provides current journal instructions or a venue template that clearly supports a linked appendix, override the default.
- **TARGET_VENUE = `AOS`** — Default venue. Supported:
  - **Theory/methodology**: `AOS`, `JASA`, `JRSSB`, `BIOMETRIKA`, `BERNOULLI`, `EJS`, `STATSINICA`, `MSL`
  - **Application**: `AOAS`, `JASA_ACS` (alias `JASA_APP`), `BIOSTATISTICS`, `STATMED`, `JCGS`, `JABES`
  - **ML theory conferences**: `COLT`, `ALT`
- **PAPER_TYPE = `auto`** — `theory`, `methodology`, `application`, or `auto`.
- **ANONYMOUS = false** — Most stat journals are NOT anonymous. Set `true` for COLT/ALT conference submissions.
- **DBLP_BIBTEX = true** — Fetch real BibTeX from DBLP/CrossRef/MathSciNet.

## Inputs

1. **PAPER_PLAN.md** — outline with Theorems-Evidence Matrix, section plan, assumption map (from `/stat-paper-plan`)
2. **NARRATIVE_REPORT.md** — the research narrative
3. **Generated figures** — PDF/PNG files in `figures/`
4. **LaTeX includes** — `figures/latex_includes.tex` (from `/paper-figure`)
5. **Bibliography** — existing `.bib` file, or will create one

If no PAPER_PLAN.md exists, ask the user to run `/stat-paper-plan` first or provide a brief outline.

## Writing References

Read these shared references when they improve writing quality:

- **Read `../stat-shared-references/stat-positioning-and-claims.md` before drafting the abstract, introduction, contribution list, theorem statements, related work, or discussion.** This is the primary defense against the two most common Big Four rejection drivers: weak positioning and overclaim. The reference describes the positioning audit, the technical claim strength audit, and the `CLAIM_SUPPORT_MAP.md` artifact.
- Read `../stat-shared-references/stat-writing-principles.md` before drafting the Abstract, Introduction, or when prose needs statistics-specific voice.
- **Read `../stat-shared-references/stat-style-discipline.md` during every drafting and clarity pass.** This is the primary defense against AI-shaped prose. It covers punctuation rules (no em-dash, no colon, reduce semicolons), AI-template patterns to remove, paragraph and bullet discipline, and COPSS-style scholar writing patterns.
- **Read `../stat-shared-references/stat-figure-design.md` before generating or polishing any figure.** It covers the no-title rule, caption discipline, legend placement, sizing, and overlap prevention.
- Read `../stat-shared-references/stat-venue-checklists.md` during setup and final checks.
- Read `../stat-shared-references/stat-theory-writing.md` when writing assumptions, theorems, proof sketches, or rate comparison tables (especially for theory and methodology papers).
- Read `../stat-shared-references/stat-application-writing.md` when writing an application paper (PAPER_TYPE = application), especially the Data and Background section and the Application / Real Data Analysis section.
- Read `../shared-references/citation-discipline.md` when the DBLP/CrossRef workflow is insufficient.

## Templates

### Venue-Specific Setup

**AOS / BERNOULLI / EJS / AOAS (IMS journals):**
```latex
\documentclass[aos]{imsart}  % or [bj], [ejs], [aoas]
\usepackage{natbib}
\bibliographystyle{imsart-nameyear}
% Author block:
\begin{aug}
\author{\fnms{First} \snm{Last}\ead[label=e1]{email@univ.edu}}
\address{Department, University, City, Country}
\runauthor{Last et al.}
\runtitle{Short Title}
\end{aug}
```

For **AOAS** (Annals of Applied Statistics), use `\documentclass[aoas]{imsart}` and additionally include subject area classification.

**JASA Theory and Methods and Applications and Case Studies (both tracks):**

Use the official JASA / Taylor & Francis LaTeX template linked from the JASA Instructions for Authors page; check `https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode=uasa20` at submission time. The bibliography style file (`.bst`) should be the one bundled with the official template.

If working from a conservative baseline before the official template is in hand, use:

```latex
\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}         % 1-inch margins
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx,booktabs,natbib,caption,subcaption,setspace}
\usepackage[hidelinks]{hyperref}
\usepackage{bm,xcolor,microtype,threeparttable,multirow,mathtools}

\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}
\theoremstyle{definition}
\newtheorem{definition}{Definition}
\theoremstyle{remark}
\newtheorem{remark}{Remark}

\onehalfspacing            % or \doublespacing for the conservative submission default
\bibliographystyle{agsm}   % ASA-journal helper templates use agsm.bst;
                            % override with the JASA-bundled .bst when available
% Author-year citations: \citet{}, \citep{}
% Submission category: "Theory and Methods" (T&M) or "Applications and Case Studies" (ACS)
```

**Line spacing**: JASA templates in current circulation use either `\onehalfspacing` (1.5) or `\doublespacing` (2.0). The user-supplied templates observed in practice use `\onehalfspacing`; the conservative submission default is `\doublespacing`. Verify on the live IFA page before submitting.

**Length**: 35 double-spaced pages for the main manuscript (roughly 26-27 lines per page) as the operative working limit. Move proofs, technical lemmas, extended simulations, and overflow tables and figures to the supplement. Verify the counting boundary on the live Instructions for Authors page before submission.

**Abstract**: **JASA abstracts target 200-250 words**. Long drafts of 300-400 words should be cut to this range before submission. Drop the second motivating paragraph (the introduction carries that material), and merge result-and-implication sentences.

Reproducibility (JASA, both tracks):

- Complete the Author Contributions Checklist (ACC) form (https://jasa-acs.github.io/repro-guide/pages/acc.html) and upload it as supplementary material at initial submission.
- A reproducibility-package skeleton (https://github.com/jasa-acs/repro-template) is suggested but not required. Using it makes the revision-stage reproducibility review easier.

Public helper templates if useful (treat as convenience, not source of record):

- ASA-journal Quarto template: https://github.com/quarto-journals/jasa

See `../stat-shared-references/stat-venue-checklists.md` for the full JASA block including AI disclosure, peer-review anonymity, alt text, and cover-letter expectations.

**Biostatistics (Oxford):**
```latex
% Use Biostatistics template (oup style)
\documentclass{article}
\usepackage{natbib}
\bibliographystyle{biostatistics}  % or per journal guidelines
% Biomedical / health applications with statistical innovation
```

**Statistics in Medicine (Wiley):**
```latex
% Use Wiley NJD class or basic article
\documentclass{article}
\usepackage{natbib}
\bibliographystyle{wileyNJD-AMA}  % or per journal guidelines
```

**JCGS (Journal of Computational and Graphical Statistics):**
```latex
% Use JCGS / Taylor & Francis template
\documentclass[12pt]{article}
\usepackage{natbib}
\bibliographystyle{asa}
% Strong emphasis on reproducibility — code repository must be linked
```

**JRSS-B:**
```latex
% Use JRSS-B template from journal website
\documentclass[12pt]{article}
\usepackage{natbib}
% Custom JRSS bibliography style
```

**BIOMETRIKA:**
```latex
% Use Biometrika template
\documentclass{article}
\usepackage{natbib}
\bibliographystyle{biometrika}
```

**STATSINICA:**
```latex
% Use Statistica Sinica template
\documentclass[12pt]{article}
\usepackage{natbib}
```

**COLT:**
```latex
\documentclass[anon]{colt2026}  % anonymous submission
\usepackage{natbib}
% Anonymous author block
```

**ALT:**
```latex
% Use ALT/PMLR template
\documentclass{article}
\usepackage{natbib}
```

### Project Structure (Theory/Methodology Paper)

```
paper/
├── main.tex                    # master file
├── imsart.cls                  # or venue-specific class file
├── imsart-nameyear.bst         # or venue-specific bst
├── math_commands.tex           # shared math macros
├── references.bib              # bibliography (only cited entries)
├── sections/
│   ├── 0_abstract.tex
│   ├── 1_introduction.tex
│   ├── 2_setup.tex             # problem setup, model, assumptions
│   ├── 3_main_results.tex      # theorems, rate comparisons
│   ├── 4_method.tex            # estimator/algorithm (if separate)
│   ├── 5_simulations.tex
│   ├── 6_real_data.tex         # optional
│   └── 7_discussion.tex
├── supplement/
│   ├── supplement_main.tex     # master file for supplement
│   ├── A_proofs_main.tex       # proofs of main theorems
│   ├── B_proofs_lemmas.tex     # proofs of technical lemmas
│   ├── C_additional_sims.tex   # additional simulations
│   └── D_additional_data.tex   # additional data analysis
└── figures/
```

### Project Structure (Application Paper)

For application papers, the structure shifts to emphasize data and the application. Section files are renamed and reweighted:

```
paper/
├── main.tex                    # master file
├── imsart.cls                  # or venue-specific class file (use [aoas] for AOAS)
├── math_commands.tex
├── references.bib
├── sections/
│   ├── 0_abstract.tex
│   ├── 1_introduction.tex
│   ├── 2_data.tex              # Data and Scientific Background (2-4 pages)
│   ├── 3_method.tex            # Methodology, scoped to the problem
│   ├── 4_theory.tex            # Light theory (1-2 theorems)
│   ├── 5_simulations.tex       # DGPs informed by the real data
│   ├── 6_application.tex       # Application / Real Data Analysis (4-6 pages — LARGEST)
│   └── 7_discussion.tex        # with practical recommendations
├── supplement/
│   ├── supplement_main.tex
│   ├── A_data_details.tex      # extended data description, preprocessing
│   ├── B_proofs.tex             # proofs (moved to supplement for app papers)
│   ├── C_additional_sims.tex
│   ├── D_additional_analyses.tex  # sensitivity, subgroup, robustness
│   └── E_reproducibility.tex   # software, computation, replication notes
├── figures/                     # rich EDA + analysis figures
└── data/                        # data availability docs or links
```

For application papers, **the figures directory and §2/§6 are where the paper's quality is judged**. Plan accordingly.

**Section files are FLEXIBLE**: Match the paper plan structure. A theory paper may have 6 sections; a methodology paper may have 8; an application paper typically has 7 with §6 dominating.

### Main and Supplement Separation

The handling of the supplement depends on `SUPPLEMENT_MODE` (see Constants above).

For `SUPPLEMENT_MODE = separate_self_contained` (default for JASA, AoS, AOAS, JRSS-B, Biometrika, EJS, Bernoulli, Statistica Sinica, JASA ACS, JCGS, JABES, Statistics in Medicine, MSL):

The main paper and supplement are independent PDFs uploaded separately. The supplement is a self-contained document.

For `SUPPLEMENT_MODE = linked_appendix` (default for Biostatistics, COLT, ALT):

The supplement is part of the same review workflow, and cross-references between the main paper and the supplement are expected. Use `\ref` across files when the venue's submission system supports it.

The rest of this section describes `separate_self_contained`, which is the more demanding case. The `linked_appendix` case relaxes these rules.

**The supplement must be a self-contained document.** It cannot rely on `\ref`, `\eqref`, `\cite` to labels that live only in the main paper, because the main paper is not compiled when the supplement is compiled.

What this means in practice:

1. **The supplement must restate every theorem, lemma, assumption, and equation it proves.** Do not write `Proof of Theorem 1` and assume the reader knows what Theorem 1 says. Restate it.

2. **The supplement must redefine notation and assumptions it uses.** Either redefine inline or include a brief notation section at the start of the supplement.

3. **Avoid cross-references between main and supplement files.** Instead, use textual references that remain readable even when the cross-reference does not resolve:
   - In the main paper: "the full proof is given in Section A of the supplement" rather than `\ref{sec:proof}` to a label in the supplement
   - In the supplement: "Theorem 1 (restated from the main paper)" rather than `\ref{thm:main}` to a label in the main paper

4. **Compile the supplement as a separate document.** Use `\documentclass` again at the start of the supplement file, with the same class as the main paper. The supplement should produce its own title page (e.g., "Supplementary Material for `[paper title]`").

5. **Bibliography**: each file has its own bibliography. They can share the same `.bib` file, but each must `\bibliography{references}` independently.

6. **Page numbering**: the supplement should restart page numbering at 1, often using S1, S2, ... (capital S prefix).

7. **Equation, theorem, figure, table numbering**: prefix with S in the supplement. For example, Theorem S.1, Equation (S.3), Figure S.2.

Recommended supplement preamble pattern:

```latex
\documentclass[aos]{imsart}  % match main paper class
\usepackage{...}             % same packages
\input{math_commands.tex}    % shared math notation

% Renumber with S prefix
\renewcommand{\thesection}{S.\arabic{section}}
\renewcommand{\thetheorem}{S.\arabic{theorem}}
\renewcommand{\theequation}{S.\arabic{equation}}
\renewcommand{\thefigure}{S.\arabic{figure}}
\renewcommand{\thetable}{S.\arabic{table}}
\setcounter{page}{1}

\begin{document}
\title{Supplementary Material for `[Paper Title]'}
\author{[same authors as main paper]}
\maketitle

\section*{Overview}
This supplement contains: (i) full proofs of Theorems 1--3 from the main
paper, restated for convenience; (ii) additional simulation results;
(iii) [...].

\section{Proof of Theorem 1}
\label{sec:supp:thm1}
\textit{Theorem 1 (from main paper).} [restate the theorem statement here]

\textit{Proof.} [...]
```

In the main paper, refer to supplement results textually:
```latex
% In the main paper:
Theorem 1 establishes the rate of convergence; the full proof,
together with additional technical lemmas, is given in Section S.1
of the Supplement.
```

In the supplement, do **not** write subsection headings like `\subsection{Proof of Theorem~\ref{thm:saturation}}` if `thm:saturation` is a label defined in the main paper. When the supplement compiles standalone, that `\ref` becomes `??` and the heading reads "Proof of Theorem ??". Instead, use a textual reference and (recommended) restate the theorem at the start of its proof. See `../stat-shared-references/stat-latex-audit.md` Step L.6 for a worked example of the bug and both correct patterns.

This pattern avoids LaTeX cross-reference fragility and ensures that the supplement can be downloaded and read on its own.

### Cross-Reference Discipline

When working with separated main and supplement files:

- **Within the main paper**: use `\ref`, `\eqref`, `\cite` freely
- **Within the supplement**: use `\ref`, `\eqref`, `\cite` freely (to labels defined within the supplement)
- **Between main and supplement**: use textual references only ("Section S.1 of the Supplement", "Theorem 1 of the main paper")

For some journals (e.g., AoS-style IMS submissions) the supplement is sometimes attached as appendices to the same compiled PDF. In that case standard cross-references work. The pipeline should default to separated compilation since this is the more robust path and works for all venues.

## Workflow

### Step 0: Backup and Clean

If `paper/` exists, back up to `paper-backup-{timestamp}/`. Never silently destroy existing work. Clean stale section files from previous structures.

### Step 1: Initialize Project

1. Create `paper/` and `paper/supplement/` directories
2. Set up venue template (class file, bibliography style)
3. Generate `math_commands.tex` with statistics notation
4. Create section files matching PAPER_PLAN structure

### Step 2: Generate math_commands.tex

Statistics-specific notation:

```latex
% math_commands.tex — statistics paper notation

% Spaces and sets
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Rd}{\mathbb{R}^d}

% Probability and expectation
\newcommand{\E}{\mathbb{E}}
\newcommand{\Prob}{\mathbb{P}}
\newcommand{\Var}{\mathrm{Var}}
\newcommand{\Cov}{\mathrm{Cov}}

% Convergence
\newcommand{\convd}{\xrightarrow{d}}
\newcommand{\convp}{\xrightarrow{p}}
\newcommand{\convas}{\xrightarrow{a.s.}}
\newcommand{\convLp}[1]{\xrightarrow{L^{#1}}}

% Norms
\newcommand{\norm}[1]{\|#1\|}
\newcommand{\abs}[1]{|#1|}
\newcommand{\inprod}[2]{\langle #1, #2 \rangle}

% Operators
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator{\tr}{tr}
\DeclareMathOperator{\diag}{diag}
\DeclareMathOperator{\rank}{rank}
\DeclareMathOperator{\sign}{sign}
\DeclareMathOperator{\supp}{supp}

% Order notation
\newcommand{\Op}{O_p}
\newcommand{\op}{o_p}

% Common distributions
\newcommand{\Normal}{\mathcal{N}}
\newcommand{\Uniform}{\mathrm{Unif}}

% Function classes
\newcommand{\cF}{\mathcal{F}}
\newcommand{\cH}{\mathcal{H}}
\newcommand{\cG}{\mathcal{G}}
\newcommand{\cX}{\mathcal{X}}
\newcommand{\cY}{\mathcal{Y}}
\newcommand{\cP}{\mathcal{P}}

% Vectors and matrices (bold)
\renewcommand{\vec}[1]{\boldsymbol{#1}}
\newcommand{\mat}[1]{\mathbf{#1}}

% Estimators
\newcommand{\htheta}{\hat{\theta}}
\newcommand{\hthetaML}{\hat{\theta}_{\mathrm{ML}}}

% Add paper-specific notation below
```

### Step 2.5: Build CLAIM_SUPPORT_MAP.md before drafting front matter

Before drafting the abstract, introduction, contribution list, theorem statements, or discussion, build `CLAIM_SUPPORT_MAP.md`. Read `../stat-shared-references/stat-positioning-and-claims.md` for the full protocol.

The map binds every positioning and technical claim that will appear in the front matter to:

- a row in `PRIOR_WORK_MATRIX.md` (built in `stat-paper-plan` Step 5.5)
- a row in `TECHNICAL_RISK_REGISTER.md` (built in `stat-paper-plan` Step 5.6)
- specific literature support, read and verified, not just cited
- a `Status` (SUPPORTED, SUPPORTED with qualification, NEEDS WORK, OVERCLAIMED, UNVERIFIED)

Drafting of the abstract, introduction, contribution list, theorem statements, and discussion does not begin until every claim that will appear there has `Status = SUPPORTED` or `SUPPORTED with qualification`. UNVERIFIED claims require literature search; OVERCLAIMED claims require either re-positioning or weakening, with a concrete replacement sentence prepared.

For literature search to verify or refute claims, use:

- `/semantic-scholar` for forward and backward citation traversal
- `/arxiv` for preprints
- `/novelty-check` for the focused "has this been done" question
- `mcp__codex__codex` for senior-statistician judgment on positioning gaps when search alone is inconclusive

Save `CLAIM_SUPPORT_MAP.md` in the project root and reference its `Claim ID` values when drafting (in comments or notes). Each claim in the drafted prose should be traceable back to a row in the map.

### Step 3: Write Each Section

Process sections in order. For each section:

1. **Read the plan** — what theorems, claims, evidence belong here
2. **Read NARRATIVE_REPORT.md** — extract relevant content
3. **Draft content** — write complete LaTeX
4. **Insert figures/tables** — use snippets from `figures/latex_includes.tex`
5. **Add citations** — use `\citet{}` / `\citep{}` (natbib, author-year for most stat journals)

#### Section-Specific Guidelines

**§0 Abstract:**
- Use the 5-6 sentence pattern from stat-writing-principles.md
- State the problem, gap, main result (with rate if applicable), approach, verification, implication
- Include one concrete quantitative result or rate
- 150-250 words, self-contained
- No citations, no undefined notation
- No `\begin{abstract}` wrapper — that goes in main.tex

**§1 Introduction:**
- **Problem statement** (1-2 paragraphs): the statistical problem, why it matters
- **Prior work and gap** (2-3 paragraphs): what is known, existing rates/methods, what remains open
- **Contribution** (1 paragraph): main result(s) in plain language
- **Proof technique overview** (1 paragraph): key insight
- **Contribution bullets**: 2-4 specific, verifiable claims
- **Paper organization** (1 paragraph): roadmap
- Target: 2-3 pages
- Citations should be thorough — stat reviewers check related work carefully

**§2 Problem Setup / Model / Assumptions:**
- Define the model formally: $Y_i = f(X_i) + \varepsilon_i$ or similar
- Fix notation (reference math_commands.tex)
- State all assumptions with labels (A1), (A2), ...
- Use `\begin{assumption}[Name]` environments
- After stating assumptions, discuss: which are standard, which are novel, comparison with prior work
- Include examples of functions/parameters satisfying the assumptions
- Target: 2-3 pages

**§3 Main Results:**
- State theorems with `\begin{theorem}` environments
- List assumptions in the theorem preamble: "Grant Assumptions (A1)-(A3)"
- After each theorem: interpretation paragraph, rate comparison, optimality discussion
- Include **rate comparison table** (mandatory for theory papers)
- Proof sketches: 1-2 paragraphs per main theorem using `\begin{proof}[Proof sketch]`
- Remarks for extensions, special cases, connections
- Corollaries for important special cases
- Target: 3-5 pages

Read `../stat-shared-references/stat-theory-writing.md` before drafting this section.

**§4 Estimation / Method (if separate):**
- Formal definition of the estimator/procedure
- Algorithm pseudocode if applicable
- Tuning parameter selection: oracle vs data-driven
- Computational complexity analysis
- Implementation notes
- Target: 1-3 pages

**§5 Simulation Studies:**
- **Design subsection**: state DGPs, sample sizes, replications, metrics, comparison methods
- Each DGP must specify: model, parameter values, distribution choices, purpose
- **Results subsection(s)**: one per major finding
- Lead with what the reader should notice, not setup details
- Every simulation table/figure must include standard errors
- Include rate verification: log-log plots of error vs n, overlaid with theoretical rate
- Discuss when the proposed method underperforms and why
- Target: 2-4 pages

Simulation table template:
```latex
\begin{table}[t]
\centering
\caption{Estimation error (MSE $\times 10^2$) averaged over 1000 replications.
Standard errors in parentheses. The proposed estimator achieves the lowest
MSE across all settings, with the gap widening as $n$ increases.}
\label{tab:sim1}
\begin{tabular}{lcccc}
\toprule
& $n = 200$ & $n = 500$ & $n = 1000$ & $n = 5000$ \\
\midrule
Proposed  & $\mathbf{4.52}$ (0.31) & $\mathbf{1.23}$ (0.08) & $\mathbf{0.48}$ (0.03) & $\mathbf{0.09}$ (0.01) \\
Method A  & $6.78$ (0.45) & $2.15$ (0.14) & $0.91$ (0.06) & $0.21$ (0.01) \\
Method B  & $8.91$ (0.52) & $3.42$ (0.21) & $1.54$ (0.10) & $0.38$ (0.02) \\
Oracle    & $3.89$ (0.27) & $1.05$ (0.07) & $0.41$ (0.03) & $0.08$ (0.01) \\
\bottomrule
\end{tabular}
\end{table}
```

**§6 Real Data Analysis (if applicable):**
- Dataset description: source, size, variables, preprocessing
- Why this dataset is appropriate
- Results with uncertainty quantification (confidence intervals, bootstrap)
- Compare with the same methods used in simulations
- Domain interpretation
- Target: 2-3 pages

**§7 Discussion:**
- Contribution summary (rephrased, not copied)
- Connections to prior work: how results improve or extend existing theory
- Limitations: which assumptions are restrictive, what settings are not covered
- Open problems: specific technical questions (e.g., "whether the log factor can be removed")
- Extensions: natural generalizations the framework supports
- Target: 1-2 pages
- Tone: measured, honest, specific

**Supplement:**
- Organize proofs to mirror main body section numbers
- Each proof starts with the theorem/lemma statement (restated for convenience)
- Cross-reference main body: "We prove Theorem~\ref{thm:upper} stated in Section~\ref{sec:results}"
- Additional simulations and data analysis go after proofs
- Write the supplement as a standalone document that imports the same math_commands.tex

### Application Paper Section-by-Section Guidelines

For application papers (PAPER_TYPE = `application`), follow these guidelines. **Read `../stat-shared-references/stat-application-writing.md` first** for detailed patterns and examples.

**§0 Abstract (application paper):**
- Use the application abstract pattern from stat-writing-principles.md
- Sentence 1: scientific question + dataset
- Sentence 2: statistical challenge in the data
- Sentence 3: proposed approach
- Sentence 4: the application finding (most important — name it)
- Sentence 5: validation strategy and outcome
- Sentence 6: implication for the domain
- 200-280 words
- An application abstract that does not state what was discovered has failed.

**§1 Introduction (application paper):**
- Open with the scientific question and stakes (1 paragraph)
- Introduce the dataset informally (1 paragraph)
- State the statistical challenges revealed by data characteristics (1-2 paragraphs)
- Discuss limitations of current domain practice (1 paragraph)
- Present the proposed approach at high level (1 paragraph)
- **Preview the substantive findings** (1 paragraph — crucial for application papers)
- List 2-4 specific contributions, spanning methodology and findings
- End with section organization
- Target: 2-3 pages
- Cite both statistical and domain literature

**§2 Data and Scientific Background (application paper):**
- This is a substantial section unique to application papers — plan 2-4 pages
- Organize as subsections:
  - §2.1 Scientific context (domain background, accessible to non-experts)
  - §2.2 Data source and collection
  - §2.3 Data structure and exploratory analysis (with EDA figures)
  - §2.4 Statistical challenges (pivot from data features to methodology need)
- Include at least 2-3 EDA figures and 1 descriptive statistics table
- Use the dataset's actual name consistently throughout the paper
- Cite the data source paper if one exists
- Acknowledge data limitations honestly
- Define domain terminology on first use

Sample LaTeX structure:
```latex
\section{Data and Scientific Background}
\label{sec:data}

\subsection{Scientific context}
\label{sec:data:context}
[1-3 paragraphs of domain background]

\subsection{Data source and collection}
\label{sec:data:source}
[1-2 paragraphs describing the data]

\subsection{Exploratory analysis}
\label{sec:data:eda}
[EDA narrative with reference to Figures and Tables]
\input{../figures/latex_includes_eda.tex}

\subsection{Statistical challenges}
\label{sec:data:challenges}
[Pivot from data features to methodological response]
```

**§3 Methodology (application paper):**
- Scope the methodology to the application — avoid over-generalization
- Connect notation to the data variables introduced in §2
- 3-4 pages typically
- Subsections by component (model, estimation, inference)
- Algorithm pseudocode if applicable

**§4 Theoretical Properties (application paper — LIGHT):**
- Only 1-2 main theorems in main body
- Consistency or asymptotic distribution typically suffice
- All assumptions stated cleanly
- Conditions verified for the specific application
- Brief discussion; refer to supplement for full proofs and extensions
- Target: 1-2 pages

**§5 Simulation Studies (application paper):**
- DGPs **must be informed by the real data** — explicitly cite §2 features
- Sample sizes should include the real data's sample size
- Comparison methods should include those used by domain practitioners
- Metrics aligned with the application's priorities
- Target: 2-3 pages

Example narrative:
```
We design our simulation studies to reflect characteristics
observed in the [dataset name] (Section~\ref{sec:data}).
Specifically, we set the sample size to $n = N$ (matching the
real data), generate covariates from [distribution matching
EDA in Figure~\ref{fig:eda1}], and induce missingness with
rate [matching Figure~\ref{fig:eda2}].
```

**§6 Application / Real Data Analysis (application paper — CENTERPIECE, 4-6 pages):**

This is the longest and most important section. Treat it as a mini-paper with internal structure:

```latex
\section{Analysis of [Dataset Name]}
\label{sec:application}

\subsection{Analysis setup}
\label{sec:app:setup}
[Restate the scientific question; describe the analytic pipeline]

\subsection{Main analysis}
\label{sec:app:main}
[Apply the method; report estimates with uncertainty;
present 2-4 high-quality figures; walk the reader through findings]

\subsection{Comparison with existing approaches}
\label{sec:app:comparison}
[Apply 1-2 domain-standard methods on the same data;
show what the new method reveals]

\subsection{Validation}
\label{sec:app:validation}
[Holdout, cross-validation, sensitivity analyses]

\subsection{Substantive findings and interpretation}
\label{sec:app:interpretation}
[What the results mean for the domain; connect back to
scientific literature]
```

Writing principles for §6:
- Tell the reader what to look at first in every figure
- Tell the reader what they should notice
- Tell the reader why it matters substantively
- Every estimate should have uncertainty quantification
- Be explicit about what the analysis cannot conclude
- Use measured language: "Our analysis suggests..." not "We prove..."

**§7 Discussion (application paper):**
- Substantive findings summary (paragraph 1)
- Methodological summary (paragraph 2)
- **Practical recommendations for practitioners** (paragraph 3 — unique to application papers)
- Data limitations (paragraph 4)
- Methodological limitations and generalizability (paragraph 5)
- Open questions and extensions (paragraph 6)
- Target: 1-2 pages

**Supplement (application paper):**
- Detailed data description and preprocessing (§A) — often substantial
- Full proofs of theorems (§B)
- Additional simulation results (§C)
- Additional analyses: subgroups, alternative specifications, diagnostic plots (§D)
- Software and reproducibility documentation (§E)
- The supplement for an application paper is often substantial (20-40 pages)

**Reproducibility statement (application paper):**

Include in main body or supplement:
```latex
\section*{Data and Code Availability}
The [dataset name] is available at [URL/repository] under [license/access conditions].
Replication code is available at [GitHub URL]. The R/Python package implementing
the proposed method is available at [URL]. Computation was performed in
[environment, key versions]. Full replication instructions are provided in
Supplement Section~\ref{sec:supp:reprod}.
```

### Step 4: Build Bibliography

1. Scan all `\citet{}` and `\citep{}` references across all .tex files
2. Build citation key list
3. For each key:
   - Check existing `.bib` files
   - If not found and DBLP_BIBTEX = true:
     - **Step A: DBLP** — `curl -s "https://dblp.org/search/publ/api?q=TITLE+AUTHOR&format=json&h=3"` then `curl -s "https://dblp.org/rec/{key}.bib"`
     - **Step B: CrossRef DOI** — `curl -sLH "Accept: application/x-bibtex" "https://doi.org/{doi}"`
     - **Step C: Mark `[VERIFY]`** — last resort, do NOT fabricate
   - For statistics: also check MathSciNet (if accessible)
4. Write `references.bib` with ONLY cited entries
5. Use consistent key format: `{firstauthor}{year}{keyword}` (e.g., `bickel2009simultaneous`)

**Key differences from ML bib management:**
- Prefer `@article{}` entries with complete journal metadata (volume, number, pages)
- Statistics journals cite more books — use `@book{}` properly
- Include edition and publisher for textbook references
- Many stat references have DOIs — include them

### Step 5: Clarity Pass

After drafting all sections, run two passes: first content/structure, then style.

**Content and structure pass:**
- All assumptions labeled and referenced correctly
- Theorem preambles list which assumptions are needed
- Rate comparison table present and accurate
- Proof sketches provide genuine insight (not just "see supplement")
- Simulation tables have standard errors
- Notation consistent throughout (check math_commands.tex)
- Convergence symbols used correctly ($\xrightarrow{d}$, $\xrightarrow{p}$, $O_p$, $o_p$)

**Style discipline pass — read `../stat-shared-references/stat-style-discipline.md` first.**

Punctuation discipline:
- Count em-dashes (—). Cut to at most one per paper. Replace with commas, periods, or restructured sentences. **Em-dashes are the single strongest AI-tell in academic prose.**
- Count colons (:). Keep only those introducing numbered lists, bulleted lists, or figure/table captions. Cut all stylistic colons.
- Count semicolons (;). Convert most to periods. Keep only for two closely related short clauses or for complex lists.

AI-template removal:
- Remove formulaic section openings: "In this section, we ...", "Here, we ...", "We now turn to ..."
- Remove empty connectives: "It is worth noting that", "Importantly,", "Notably,", "Crucially,", "Interestingly,", "Significantly,"
- Remove AI watchwords: "delve", "pivotal", "landscape", "tapestry", "underscore", "elucidate", "noteworthy", "intriguingly", "leveraging", "comprehensive" (when nothing is comprehensive), "novel" (when novelty is not established), "robust" (when robustness is not tested)
- Remove padding: "perform an analysis of" → "analyze", "make use of" → "use", "in order to" → "to", "due to the fact that" → "because"
- Remove hedge-stacking: "may potentially suggest" → "suggests"
- Remove generic conclusions: "opens exciting new avenues", "wide-ranging implications"

Paragraph and bullet discipline:
- Statistics papers favor paragraphs of 4-8 sentences. One-sentence paragraphs almost never belong.
- Bullets only in: contribution lists in §1, assumption lists, algorithm pseudocode, simulation-setup item lists. Convert other bullets to prose.
- Vary paragraph openings; not every paragraph needs a topic sentence
- Cut the rule-of-three tic ("X, Y, and Z" used reflexively); use pairs or single items when warranted

COPSS-style scholar voice:
- Confidence without hype: "achieves the minimax rate" not "achieves remarkable performance"
- Plain verbs: "we propose", "we prove", "we show" rather than "we present results indicating" or "it can be shown that"
- Connective restraint: prefer "but" over "however"; prefer "thus" over "consequently"; never stack "however"/"moreover"/"furthermore"
- Mathematical precision over adjectival praise: tell the reader what to compare, not that they should be impressed
- Modest about boundaries: state explicitly what was not done, with specifics

**General clarity:**
- Subject-verb proximity
- Context before new information
- One idea per paragraph
- Precise language: "rate" not "performance", "achieves" not "gets"

**Statistics-specific language:**
- "We establish" / "We prove" (for theoretical results)
- "We propose" / "We introduce" (for new methods)
- "We show" / "We demonstrate" (for empirical findings)
- "Our estimator achieves the rate..." (not "our method performs well")
- "Under Assumptions (A1)-(A3)" (not "under mild conditions")
- "The minimax lower bound shows..." (not "our result is optimal" without proof)

**Application paper-specific language:**
- "Our analysis of [dataset] suggests..." (lead with the data)
- "We find that..." paired with the specific finding
- "In contrast to the standard [domain method], our approach reveals..."
- "These findings indicate..." paired with substantive interpretation
- "We recommend that practitioners..." (in Discussion)
- Avoid: "We prove" (rare in app papers), "minimax optimal" (rarely relevant)
- Acknowledge uncertainty: "consistent with...", "suggests but does not establish..."
- Name the data: use the dataset's actual name throughout, not "the data"
- Tell the reader what to notice: "Figure X shows...; the notable feature is..."

### Step 5.5: Front-matter positioning and claim audit

After drafting all sections, before cross-review, run the positioning and claim audit on the front matter (abstract, introduction, contribution list, theorem statements, related work, discussion).

1. Extract every positioning claim and every technical claim from the drafted prose verbatim.
2. Compare each extracted claim with the corresponding row of `CLAIM_SUPPORT_MAP.md`. Each prose claim should match a SUPPORTED or SUPPORTED-with-qualification row.
3. For any prose claim that does not have a backing row, either:
   - Add it to `CLAIM_SUPPORT_MAP.md` and run the literature search and verification protocol from `../stat-shared-references/stat-positioning-and-claims.md`, or
   - Remove or soften the prose claim until it matches the available support.
4. For any qualification recorded in `CLAIM_SUPPORT_MAP.md` (e.g., "weaker on noise, identical on signal strength"), confirm the qualification appears in the prose, not buried in an appendix remark.
5. Codex MCP can run an independent audit using the prompt template in `../stat-shared-references/stat-positioning-and-claims.md` (the Codex Integration section). For high-stakes submissions, run this independent audit.

Update `CLAIM_SUPPORT_MAP.md` as the audit produces refinements. The map is a living document until submission.

### Step 6: Cross-Review

The draft is reviewed in up to two passes, depending on `REVIEW_MODE`.

#### Pass A: Internal Claude subagent review

Use when `REVIEW_MODE = claude` or `both`. Fast structural check.

For **theory/methodology papers**, invoke the Agent tool with `subagent_type="general-purpose"` and the prompt below.

```yaml
Agent(subagent_type="general-purpose"):
  model: claude-opus-4-6
  prompt: |
    Review this [VENUE] statistics paper draft.
    Paper type: [theory/methodology].

    Focus on:
    1. Are theorem statements precise and self-contained?
    2. Are assumptions clearly stated, labeled, and discussed?
    3. Is the rate comparison with prior work explicit and fair?
    4. Do proof sketches provide genuine insight?
    5. Do simulations verify the theoretical predictions?
    6. Are standard errors reported for all simulation results?
    7. Is notation consistent throughout?
    8. Is the contribution clear by the end of the Introduction?
    9. Are limitations honestly discussed?
    10. For methodology papers: is the real data analysis substantive?

    For each issue: severity (CRITICAL/MAJOR/MINOR), location, fix.

    [paste full draft]
```

If the environment supports continuing the same Agent review thread, reuse it with the revised draft and a short changelog. Otherwise invoke `Agent(subagent_type="general-purpose")` again with the revised draft and the same review rubric.

For **application papers**, invoke the Agent tool with `subagent_type="general-purpose"` and the prompt below.

```yaml
Agent(subagent_type="general-purpose"):
  model: claude-opus-4-6
  prompt: |
    Review this [VENUE] application paper draft.
    Paper type: application
    Target venue: [AOAS / JASA ACS / Biostatistics / etc.]

    Focus on:
    1. Is the scientific question clearly stated in the first paragraph
       of the Introduction?
    2. Does the Data and Background section (§2) provide adequate
       description with EDA?
    3. Are statistical challenges motivated directly from data features?
    4. Is the methodology appropriately scoped to the problem
       (not over-generalized)?
    5. Is theory appropriately light in main body (1-2 theorems max)?
    6. Are simulation DGPs informed by the real data characteristics?
    7. Are domain-standard comparison methods included?
    8. Is the Application section (§6) the longest section with
       multiple analyses?
    9. Are substantive findings clearly identified and interpreted?
    10. Is validation present (holdout, CV, or sensitivity)?
    11. Does the Discussion include practical recommendations?
    12. Are data and code availability statements present?
    13. Is the tone measured (avoiding overclaiming)?
    14. Are both audiences served — statisticians and domain readers?
    15. Are figures self-contained with informative captions?

    For each issue: severity (CRITICAL/MAJOR/MINOR), location, fix.

    [paste full draft]
```

Apply CRITICAL and MAJOR fixes from Pass A before moving to Pass B.

#### Pass B: External senior-statistician dialogue with Codex MCP

Use when `REVIEW_MODE = codex` or `both`. This is the high-stakes pass that brings independent judgment from GPT-5.4 with xhigh reasoning. Recommended before any journal submission.

**The dialogue principle.** Codex's review is one senior reader's opinion, not a directive. The job of Pass B is to discuss with Codex until both sides converge on what the draft needs, not to apply Codex's feedback wholesale. Read `../stat-shared-references/stat-codex-dialogue.md` before starting.

**Step B.1: Initial review call.**

For **theory/methodology papers**:

```
mcp__codex__codex:
  model: gpt-5.4
  sandbox: read-only
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a senior statistician serving as Associate Editor for
    [AoS / JASA Theory and Methods / JRSS-B / Biometrika / etc.].
    Paper type: [theory / methodology].

    Below is the complete draft of a manuscript main body. Please review
    it at the standard of a Big Four statistics journal.

    [paste main body — abstract, intro, setup, results, method,
     simulations, application if applicable, discussion]

    [if separate supplement: also paste the supplement]

    Please provide:

    (1) Top-line verdict: Accept / Minor Revision / Major Revision /
        Reject, with one-paragraph justification naming the binding
        constraint.

    (2) Three to five most important issues, ranked by what would
        change the editorial decision. For each, give the minimum
        concrete fix: which sentence, which assumption, which equation,
        which simulation table, which figure.

    (3) Theorem audit: for each main theorem, check that
        (a) all assumptions used in the proof are stated,
        (b) the rate or bound is correctly compared with the closest
            prior work,
        (c) constants are discussed where they matter,
        (d) the proof sketch in the main body gives genuine insight
            rather than deferring to the supplement.
        Flag any technical claims that look suspicious.

    (4) Writing voice: does this read like a senior statistician wrote
        it, or like an AI-shaped first draft?

        Specifically check for AI tells:
        - em-dashes used to connect clauses
        - colons used outside lists and captions
        - excessive semicolons
        - formulaic openings ("In this section, we ...")
        - empty connectives ("It is worth noting that", "Importantly,",
          "Notably,", "Crucially,")
        - watchwords (delve, pivotal, landscape, underscore,
          noteworthy, leveraging, comprehensive, novel as decoration)
        - hedge-stacking (may potentially, could possibly)
        - rule-of-three tic
        - one-sentence paragraphs
        - excessive bullets outside contribution lists, assumption
          lists, algorithms, simulation setups
        - generic closing phrases ("opens exciting new avenues")

        Count each, and list specific lines where revision is needed.

    (5) Big Four standards check:
        - precision before elegance
        - mathematical rigor (assumptions before theorems, sketches
          with insight)
        - honest scope (boundary stated)
        - substantive contribution
        - measured voice
        - reproducibility
        - main-supplement independence (no broken cross-references;
          theorems restated in supplement; S-prefixed numbering)

    (6) Figures and tables: assess captions for self-containment, check
        that no figure has a title inside it, and check for legend or
        label overlap that you can identify from the prose or LaTeX.

    (7) Mock referee report: write a referee report at the level the
        author should expect from this venue, with Summary, Strengths,
        Weaknesses, Detailed Comments, Recommendation, Confidence.

    Do not soften. Senior statisticians prefer hard feedback delivered
    in a measured voice.
```

For **application papers**:

```
mcp__codex__codex:
  model: gpt-5.4
  sandbox: read-only
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a senior applied statistician serving as Associate Editor
    for [AOAS / JASA Applications and Case Studies / Biostatistics /
    Statistics in Medicine / etc.]. Paper type: application.

    Below is the complete draft of an application paper. Please review
    at the standard of an applied-statistics top venue.

    [paste main body and supplement]

    Please provide:

    (1) Top-line verdict and binding constraint.

    (2) Scientific substance: does the paper answer a substantive
        applied question, or is it a methodology paper with a token
        application? If the latter, recommend repositioning.

    (3) Data and Background (§2): is the section substantive enough?
        Does the EDA reveal the statistical challenges? Is the dataset
        appropriate?

    (4) Methodology scope: is the method appropriately scoped (not
        over-generalized)?

    (5) Theory weight: is theory appropriately light (1-2 theorems
        max in main body)? Should anything move to the supplement?

    (6) Simulation studies: are DGPs informed by real data
        characteristics? Are domain-standard methods compared?

    (7) Application section (§6): is this the longest section? Does it
        have multiple sub-analyses? Are findings substantive and
        interpreted? Is validation present?

    (8) Substantive findings: name them. Are they actually new? Are
        they overstated?

    (9) Reproducibility: data availability, code availability, replication
        scripts. Flag gaps.

    (10) Writing voice: same AI-tell audit as theory/methodology case.

    (11) Mock referee report at the level expected from the venue.

    Do not soften.
```

**Step B.2: Targeted dialogue rounds.**

Use `mcp__codex__codex-reply` with the `threadId` to dig in. The dialogue is the value, not the initial review. Useful patterns:

- "On issue N: I disagree because [specific reason and evidence]. Please reconsider in light of this. If you still think the issue stands, identify what specifically remains wrong; if you withdraw the criticism, say so."
- "Issue 2 is the most important. Please draft three sentences that would replace lines [X-Y] and resolve the criticism."
- "If we move Theorem 3 to the supplement and replace it with a corollary, does the main contribution still hold?"
- "Show me what the rate comparison table should look like if we run it for the closest three prior works."
- "Write a mock author response to your referee report, identifying which points we can address in revision and which require new experiments."

Verify any specific paper, theorem number, page reference, or numerical constant that Codex cites. LLMs are confident even when wrong on these.

**Step B.3: Convergence and documentation.**

For each Codex criticism, the author decides one of three outcomes per `../stat-shared-references/stat-codex-dialogue.md`:

- Accept: the criticism is clearly correct; apply the fix.
- Push back: the criticism is wrong or based on a misunderstanding; use `mcp__codex__codex-reply` to provide the context Codex lacked, then re-decide.
- Log disagreement: after a round or two without convergence, document both positions and move on.

Apply accepted criticisms (not all criticisms). Read any proposed replacement sentence carefully; Codex is good at structure but can introduce technical inaccuracies that need verification before paste.

Where Codex and Claude reviews disagree, surface the disagreement to the user. These disagreements often signal genuine ambiguity that benefits from human judgment.

Save the Codex dialogue to `PAPER_DRAFT_REVIEW.md` in the project root, with the format specified in `../stat-shared-references/stat-codex-dialogue.md`: `threadId`, initial review verbatim, round-by-round pushback log, accepted criticisms with fixes, rejected criticisms with reasoning, outstanding disagreements.

### Step 7: Reverse Outline Test

1. Extract topic sentences of every paragraph
2. Read them in sequence — they should form a coherent argument
3. Check theorem coverage — every theorem from the plan appears
4. Check evidence mapping — every simulation supports a stated claim
5. Fix gaps

### Step 8: Final Checks

**General checks (all paper types):**

For the mechanical compile and reference checks below, read `../stat-shared-references/stat-latex-audit.md` for the full audit protocol including the cross-check scripts and the warning patterns to search for in the log.

- [ ] All `\ref{}` / `\label{}` match within each file (main, supplement)
- [ ] **No cross-references between main and supplement files** when `SUPPLEMENT_MODE = separate_self_contained` (use textual references like "Section S.1 of the Supplement")
- [ ] **Supplement is self-contained**: every theorem, lemma, assumption it proves is restated; notation defined or imported via `math_commands.tex`
- [ ] **Supplement compiles independently** from the main paper
- [ ] **Supplement uses S-prefixed numbering** for theorems, equations, sections (Theorem S.1, Section S.2, etc.)
- [ ] **LaTeX integrity audit passes**: no undefined references, no undefined citations, no missing image files, no HIGH/CRITICAL log warnings (run `latexmk -pdf -interaction=nonstopmode` and search for "Warning|Error|undefined|multiply|missing")
- [ ] **Template conformance audit passes**: `\documentclass`, packages, font, line spacing, margins, bibliography style match the venue requirement (read `../stat-shared-references/stat-latex-audit.md`)
- [ ] All `\citet{}` / `\citep{}` have BibTeX entries in both main and supplement
- [ ] Notation consistent (check math_commands.tex is included in both main and supplement)
- [ ] No TODO/FIXME/VERIFY markers remain
- [ ] Abstract is self-contained
- [ ] Title is specific and informative
- [ ] references.bib contains ONLY cited entries
- [ ] No stale section files
- [ ] Section files match main.tex `\input` paths
- [ ] Venue-specific requirements met (read `../stat-shared-references/stat-venue-checklists.md`)
- [ ] For COLT/ALT: anonymization is correct, main body within page limit
- [ ] For journals: page count within venue norms
- [ ] Keywords / AMS subject classification included (if required)

**Positioning and claim audit checks (read `../stat-shared-references/stat-positioning-and-claims.md`):**

- [ ] `CLAIM_SUPPORT_MAP.md` exists and covers every positioning and technical claim in the abstract, introduction, contribution list, theorem statements, related work, and discussion
- [ ] Every claim in the map is `SUPPORTED` or `SUPPORTED with qualification`; no `UNVERIFIED` or `OVERCLAIMED` rows remain
- [ ] For comparative claims ("weaker assumptions than", "improves the rate from", "first to"), the cited prior work is verified by reading the relevant theorem, not by citation alone
- [ ] Qualifications recorded in the map appear in the prose (not hidden in appendices)
- [ ] Closest prior work is cited; no obvious recent paper (last 2-3 years) is missing
- [ ] Each "first to" or "only" claim has been forward-searched from the closest prior paper
- [ ] Author sign-off recorded on the map before submission

**Style discipline checks (read `../stat-shared-references/stat-style-discipline.md`):**

- [ ] Em-dashes (—) cut to at most one per paper
- [ ] Colons (:) limited to introducing lists, figure/table captions
- [ ] Semicolons (;) reduced; most converted to periods
- [ ] No formulaic section openings ("In this section, we ...")
- [ ] No empty connectives ("It is worth noting that", "Importantly,", "Notably,")
- [ ] No AI watchwords (delve, pivotal, landscape, underscore, noteworthy, comprehensive, leveraging)
- [ ] No hedge-stacking (may potentially, could possibly)
- [ ] No generic conclusions ("opens exciting new avenues")
- [ ] One-sentence paragraphs eliminated
- [ ] Bullets only in contribution lists, assumption lists, algorithms, simulation setups
- [ ] Connectives ("however", "moreover", "furthermore") not stacked

**Figure design checks (read `../stat-shared-references/stat-figure-design.md`):**

- [ ] No titles inside any figure (content moved to caption)
- [ ] Every figure caption is self-contained
- [ ] Legends do not overlap data or extend beyond plot area
- [ ] Axis labels are concise and use main-text notation
- [ ] Tick density is reasonable (5-7 major ticks per axis)
- [ ] Colorblind-safe palette used
- [ ] Method encoding (color, linetype, marker) is consistent across all figures
- [ ] Vector format (PDF/EPS) used for line plots
- [ ] Fonts embedded in PDF outputs
- [ ] Font sizes readable at journal column width
- [ ] Multi-panel figures have panel labels (a, b, c) and unified axes when appropriate
- [ ] Uncertainty (CI bands, error bars) shown for every estimate that matters
- [ ] Figures interpretable in grayscale (do not depend on color alone)
- [ ] Tables use booktabs (\toprule, \midrule, \bottomrule), no vertical rules

**Theory/methodology-specific checks:**

- [ ] All assumptions labeled and cross-referenced correctly
- [ ] Rate comparison table present (theory papers)
- [ ] Proof sketches in main body for all main theorems
- [ ] Supplement organized with restated theorems
- [ ] Simulation tables have standard errors
- [ ] Log-log rate verification plots present (if applicable)

**Application-specific checks:**

- [ ] Scientific question stated in first paragraph of Introduction
- [ ] Specific dataset named throughout the paper
- [ ] Data and Background section (§2) is at least 2 pages
- [ ] §2 includes at least 2-3 EDA figures
- [ ] §2 includes a descriptive statistics table
- [ ] Statistical challenges in §2 are pivoted from data features
- [ ] Theory in main body is light (1-2 theorems max)
- [ ] Simulation DGPs are informed by real data characteristics
- [ ] Comparison methods include those used by domain practitioners
- [ ] Application section (§6) is the longest section in main body
- [ ] §6 has multiple sub-analyses (main, comparison, validation, interpretation)
- [ ] §6 figures have self-contained captions
- [ ] Every estimate has uncertainty quantification
- [ ] Holdout/CV/sensitivity analyses are present
- [ ] Substantive findings are explicit and interpreted
- [ ] Discussion includes practical recommendations
- [ ] Discussion includes data limitations and generalizability
- [ ] Data availability statement is present
- [ ] Code availability statement is present (with repository URL)
- [ ] Reproducibility is addressed concretely
- [ ] Domain terminology is consistent and defined on first use
- [ ] Both audiences (statisticians + domain scientists) are served
- [ ] Tone is measured, no overclaiming

## Key Rules

### General (all paper types)

- **Large file handling**: If Write fails due to size, use Bash to write in chunks.
- **Do NOT generate author information**. Use anonymous or placeholder for COLT/ALT; leave placeholder for journals.
- **Write complete sections, not outlines**. Output should be compilable LaTeX.
- **One file per section**. Modular structure.
- **Author-year citations**. Use natbib `\citet`/`\citep` for all stat journals.
- **Clean bib**. Only cited entries, complete metadata, proper entry types.
- **Measured tone**. Statistics papers are more formal than ML conference papers.
- **Backup before overwrite**. Never destroy existing work.
- **Main and supplement are independent documents**. No cross-references between them; use textual references ("Section S.2 of the Supplement"). Each file compiles standalone. Restate theorems in the supplement.
- **Positioning and claim audit is non-negotiable**. Before drafting front matter, build `CLAIM_SUPPORT_MAP.md`. After drafting, audit it. No positioning or technical claim ships without backing in `PRIOR_WORK_MATRIX.md`, `TECHNICAL_RISK_REGISTER.md`, and verified literature support. Read `../stat-shared-references/stat-positioning-and-claims.md`.
- **Style discipline is non-negotiable**. Read `../stat-shared-references/stat-style-discipline.md` and apply during the clarity pass. Em-dashes, colons, AI templates, watchwords, and excessive bullets must all be removed.
- **Figure discipline is non-negotiable**. Read `../stat-shared-references/stat-figure-design.md`. No titles in figures; legends do not overlap data; captions are self-contained.

### Theory/methodology paper rules

- **Assumptions are first-class** — state, label, discuss, compare
- **Rate comparison table is mandatory** for theory papers
- **Proof sketches must provide insight** — not just "see supplement"
- **Simulations must verify theory** — include rate verification plots
- **Standard errors always** — every simulation metric needs SE

### Application paper rules

- **The dataset is the protagonist** — name it, use it consistently, structure the paper around it
- **§2 Data and Background is substantive** — at least 2 pages with EDA figures and a descriptive table, not a token paragraph
- **§6 Application is the centerpiece** — make it the longest section, with multiple sub-analyses
- **Theory is light in main body** — at most 1-2 theorems; everything else in supplement
- **Simulations must mirror the real data** — sample size, distributions, dependence structure, missingness should be informed by §2
- **Compare with what practitioners use** — not just statistical baselines but domain-standard methods
- **Validate concretely** — holdout, cross-validation, sensitivity analyses are not optional
- **Lead with findings** — abstract and introduction must name what was discovered
- **Tell the reader what to see** — every figure in §6 needs guided narrative
- **Quantify uncertainty for every estimate** — CIs, posterior intervals, bootstrap, etc.
- **Be honest about limits** — explicit "what this analysis cannot conclude" earns credibility
- **Practical recommendations in Discussion** — application papers serve practitioners
- **Reproducibility is non-negotiable** — data availability, code repository, replication script must be addressed
- **Serve both audiences** — statisticians AND domain scientists should follow the paper
- **Domain terminology must be defined on first use** — don't assume statistical readers know clinical/economic/ecological jargon
