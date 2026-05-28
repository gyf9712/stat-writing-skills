# Notation and Abbreviation Audit for Statistics Papers

Use this reference when finalizing the notation in a Big Four submission. Undefined notation and homemade acronyms are among the most common minor-concern items in Big Four referee reports, and the easiest to fix before submission. Biometrika is especially hostile to method acronyms; AoS and JRSS-B share the discipline; JASA is somewhat looser but still expects standard notation.

## When to Read

- Before the final compile of any Big Four submission
- When the manuscript has been written by multiple coauthors and notation has drifted
- When the main paper and the supplement have been written at different times
- During `stat-polishing` if the user reports that the paper uses inconsistent symbols
- During `stat-paper-write` if the math is being introduced for the first time and the notation choices have not been audited

## Two Audits

The notation audit has two layers.

### Layer 1: every symbol defined on first use

For every symbol that carries meaning in the paper, the first use must be a definition or an explicit reference to a definition. The audit produces a list of every symbol, the location of its first use, the definition or the reference, and a status (`DEFINED`, `DEFINED LATER`, `UNDEFINED`).

The list is the artifact; reviewers do not see it, but the author uses it to catch every drifted symbol.

### Layer 2: abbreviations and acronyms

Statistics journals accept a small set of standard acronyms (MLE, MCMC, GLM, MSE, OLS, IID, RV, CDF, PDF, KL, ROC, AUC, MAR, MNAR, NPMLE, EM, EE, GEE, ARMA, MA, AR, RKHS, SVD, PCA, ICA, NMF, ANOVA, MANOVA, FDR, FWER). Anything outside this set, and especially method names invented for the paper, should be examined.

Biometrika's house style discourages new method acronyms. AoS, JRSS-B, and JASA are slightly more lenient but still treat method acronyms as a presentation choice, not a default. Application journals (AOAS, Biostatistics) tolerate domain acronyms when they are the standard term in the field.

## The Symbol Inventory

For a typical methodology paper, the inventory has 30 to 80 symbols. Build it once, audit it before each major revision.

| Symbol | Meaning | First use | Defined here | Last use | Status |
|---|---|---|---|---|---|
| $n$ | Sample size | Abstract, second sentence | Section 2.1 | Throughout | DEFINED LATER |
| $p$ | Dimension | Abstract | Section 2.1 | Throughout | DEFINED LATER |
| $X_i$ | $i$-th observation | Section 2.1 eq. (1) | Section 2.1 | Throughout | DEFINED |
| $\hat\theta_n$ | Proposed estimator | Section 3 eq. (5) | Section 3.1 | Throughout | DEFINED |
| $\mathcal{F}$ | Function class | Section 3.2 | Section 3.2 | Theorems | DEFINED |
| $\sigma$ | Noise standard deviation | Section 4 | NEVER | Simulation | UNDEFINED |
| $\rho$ | Correlation | Application section | Implicit | One use | DEFINED LATER |
| $K$ | Kernel | Section 5 | Section 5.1 | Application | DEFINED |
| ... | ... | ... | ... | ... | ... |

A row with `UNDEFINED` is a defect; fix before submission. A row with `DEFINED LATER` (used before defined) is acceptable for genuinely standard symbols introduced in the abstract; for nonstandard symbols, move the definition earlier.

## The Acronym Inventory

A separate table, shorter, that lists every acronym in the paper.

| Acronym | Expansion | Standard? | First use defines it? | Necessary? |
|---|---|---|---|---|
| MLE | Maximum likelihood estimator | Yes | Yes | Yes |
| MSE | Mean squared error | Yes | No (assumed) | Yes |
| DRAKE | Doubly Robust Adaptive Kernel Estimator | No (homemade) | Yes | No |
| KMR | Kernel Mean Regression | No (homemade) | Yes | Maybe |
| FDR | False discovery rate | Yes | Yes | Yes |
| ... | ... | ... | ... | ... |

A row marked `No (homemade)` and `Necessary? No` should be removed. Replace with a descriptive short name (`the proposed estimator`, `the adaptive kernel estimator`) and let the formal definition do the work.

## Discipline for New Method Names

The Big Four naming convention for a new method is:

- A descriptive phrase used consistently throughout the paper (`the adaptive lasso`, `the doubly robust estimator`)
- A formal mathematical definition with a single symbol (`$\hat\theta_n$`, `$\hat{f}_h$`)
- No acronym

If an acronym is unavoidable (the method is the centerpiece, the paper will be cited often, the descriptive phrase is unwieldy), the rule is:

- The acronym is defined on first use in the abstract or introduction
- The full descriptive phrase is also used at the same location
- The acronym is short (three to four letters)
- The acronym is not a contrived backronym

`DRAKE` is contrived; the acronym is doing branding work rather than abbreviation work. `ABKE` (`adaptive boosting kernel estimator`) is also contrived. By contrast, `EM` (`expectation-maximization`), `GEE` (`generalized estimating equations`), and `BART` (`Bayesian additive regression trees`) earned their acronyms by becoming standard.

Until the method is well-established, prefer the descriptive phrase. The acronym is a downstream convention.

## Common Notation Failures

### Drift between body and supplement

The body uses $\hat\theta$; the supplement uses $\widehat{\theta}_n$ or $\tilde\theta$. The reviewer cannot tell whether they are the same object. Fix: lock the symbol in a `math_commands.tex` file imported by both files.

### Reuse of a symbol for two objects

The body uses $X$ for the design matrix and $X$ for a random variable in different sections. The reviewer pauses each time. Fix: rename one (typically the random variable becomes $W$ or $Z$).

### Implicit conventions

`Throughout, $C$ denotes a constant that may change from line to line.` is acceptable in a proof but should not be the convention for a result the reader cares about (a rate, an explicit constant in a theorem statement). State the convention once, near the start of the proof, not at the start of the paper.

### Subscripts that drift

$\hat\theta_n$ in the body, $\hat\theta$ in the abstract, $\hat\theta_{n,p}$ in the theorem. Choose one decoration scheme and stick with it; the subscript carries the dependence the reader needs to track ($n$ for sample size, possibly $h$ for tuning parameter), nothing else.

### Function and number conflicts

$f(x)$ used both as a generic function and as a probability density in different sections. Use $f$ for the function and $p$ for the density, or use a different letter, or be explicit in each section.

### Vectors and matrices

Statistics conventions split: ASA journals (JASA) typically bold vectors and matrices ($\mathbf{X}$, $\boldsymbol\theta$); Biometrika does not use distinctive bold for these (rely on italic upper-case $X$ for a matrix, italic lower-case $x$ for a vector). Match the venue. Set the convention in a comment at the top of the LaTeX source.

### Special characters

Avoid hand-rolled bold or italic for emphasis; rely on the math typeface convention. Do not bold scalar symbols in body prose to make a result feel important; the result either is or is not.

## Audit Checklist

Run after the manuscript is feature-complete and before the final compile.

- [ ] Every symbol used in the abstract is defined in the abstract or is a standard symbol the venue accepts
- [ ] Every symbol used in the introduction is either standard or defined inline
- [ ] Every symbol used in a theorem statement is defined in the preceding assumption block or definition
- [ ] No symbol is reused for two different objects in the same paper
- [ ] The body and the supplement use the same symbol for the same object (via `math_commands.tex` or equivalent)
- [ ] Generic constants in proofs are isolated to the proof; not promoted into theorem statements
- [ ] Subscript scheme is consistent: same decoration carries the same meaning throughout
- [ ] Vector/matrix typeface follows the venue's convention (bold for ASA, plain for Biometrika; check `stat-venue-checklists.md`)
- [ ] Every acronym is either standard (in the list above) or defined on first use with the full phrase
- [ ] No homemade method acronyms remain unless the contribution is the method itself and the acronym is short and non-contrived
- [ ] No in-text `w.r.t.`, `s.t.`, `i.f.f.`, `e.g.`, `i.e.` outside parentheses (spell out in body prose)
- [ ] No undefined symbols introduced in figures or tables that are not in the body
- [ ] Notation introduced in the body is not silently redefined in the supplement
- [ ] The abstract uses no acronyms that are not standard

## Common Standard Acronyms

These acronyms can be used without expansion in a Big Four paper.

`AR`, `ARMA`, `AUC`, `ANOVA`, `BART`, `CDF`, `CV`, `EM`, `EE`, `FDR`, `FWER`, `GEE`, `GLM`, `IID` (or `i.i.d.`), `IPW`, `KL`, `KKT`, `LASSO`, `MA`, `MANOVA`, `MAR`, `MCAR`, `MCMC`, `MLE`, `MSE`, `MAE`, `MNAR`, `NMF`, `NPMLE`, `OLS`, `PCA`, `PDF`, `PMF`, `RKHS`, `ROC`, `RV`, `SDE`, `SGD`, `SVD`, `SVM`, `WLOG`.

Field-specific acronyms (`SNP`, `EHR`, `MEG`, `fMRI`, `RCT`) are acceptable in application papers where the domain audience uses them as primary terms.

When in doubt, expand on first use and explain the acronym. The cost of expansion is small; the cost of an undefined acronym reaching the AE is large.

## Integration with the Skill Family

This reference is consulted by:

- `stat-paper-plan`: when listing the notation conventions in `PAPER_PLAN.md`
- `stat-paper-write`: when introducing notation and method names for the first time
- `stat-polishing`: as part of the final audit pass
- `stat-paper-writing`: bundled into the pre-submission inspection
- `stat-mock-review`: as a routine minor-concern check; an undefined symbol in the abstract is a major concern

When a symbol or acronym audit fails late in the pipeline, the fix is local. The cost of running the audit early is one hour; the cost of skipping it is a referee report point per undefined symbol.
