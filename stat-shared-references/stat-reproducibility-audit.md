# Reproducibility Audit for Statistics Papers

Use this reference when preparing a Big Four submission for which data and code availability, simulation reproducibility, or a journal-level reproducibility kite-mark is in scope. Big Four expectations on this front have tightened in the last five years; a submission that meets the methodological bar but fails the reproducibility audit will be held at the AE stage or sent back at the proof stage. This audit catches that.

## When to Read

- Before the final compile of any Big Four submission
- When preparing the supplement (which usually holds the replication artifacts)
- When filling out a journal-specific reproducibility form (JASA ACC, Biostatistics D/C/R)
- When the author plans to release a software package or dataset alongside the paper
- During `stat-mock-review`, before deciding on the rescue plan

## What Big Four Journals Now Expect

The journals differ in the strictness of their policy and the artifact they require. The substance is similar: data and code that produce the figures, tables, and main numerical results must be available unless there is a documented restriction.

| Venue | Code availability | Data availability | Reproducibility artifact |
|---|---|---|---|
| JASA | Required for new methods; encouraged otherwise. ACM-style policy. | Required unless restricted; restrictions must be stated. | Author Contributions Checklist (ACC) form filled in and uploaded as supplementary material. |
| Annals of Statistics | Encouraged for new methods; required for empirical claims that depend on data. | Required for empirical claims. | No journal-level kite-mark; ACC-style narrative in the supplement is good practice. |
| JRSS-B | Strong expectation. Code and data must be available unless restricted. New methods require reproducible simulations. | Required unless restricted. | RSS data and code policy; D/C/R-style statement in the manuscript. |
| Biometrika | Code for new methods is expected; reproducible simulations are required. | Required unless restricted. | Supplementary file containing code or a link to a versioned repository. |
| AOAS | Reproducibility is the IMS norm; AOAS supplement instructions require replication artifacts for the main analysis. | Required unless restricted. | AAS reproducibility review for select papers; supplementary file with replication code. |
| Biostatistics | D (Data), C (Code), R (Reproducible) kite-marks awarded by the journal after a separate review. | Required unless restricted. | Kite-mark application is voluntary but strongly encouraged. |
| JCGS | Code for new methods; numerical experiments must be reproducible. | Required unless restricted. | Reproducibility supplement standard. |
| Bernoulli, EJS, Statistica Sinica | Encouraged; not all enforce. | Required for empirical claims. | Policies vary; check the venue at submission time. |
| COLT, ALT | Code for empirical experiments encouraged; theory papers exempt. | Required for empirical claims. | No journal-level artifact. |

All policies are subject to change. The `Last checked` discipline in `stat-venue-checklists.md` applies here too: verify against the journal's current author guidelines at submission time.

## What the Reproducibility Artifact Must Contain

For a methodology or application paper, the replication artifact should be sufficient to regenerate every figure, every table, and every numerical claim in the main paper from the supplied data and the supplied code, on a fresh machine, in a documented runtime.

### Code

- A `README.md` at the repository root that names the paper, lists the contents of the repository, and describes the steps to reproduce the results
- A script (or sequence of scripts) that runs the simulation studies and produces the simulation figures and tables
- A script that runs the data analysis and produces the application figures and tables
- A script that produces the LaTeX figure files (or a workflow that emits them as a side effect)
- A `requirements.txt`, `environment.yml`, `renv.lock`, `DESCRIPTION`, or equivalent that pins package versions
- A `LICENSE` file (MIT, GPL, BSD, or the venue's preferred license)
- A `CITATION.cff` or `inst/CITATION` entry that gives the paper as the canonical citation

For R-based work, the convention is an R package with vignettes, or a project directory using `renv` for environment isolation. For Python, a `pyproject.toml` with pinned dependencies and a `make reproduce` target.

### Data

- The data files used in the application section, with a clear license or use restriction stated
- A data dictionary describing each column, its type, and its units
- The preprocessing script that converts raw data into the analysis-ready form
- If the data are restricted, a `DATA_ACCESS.md` describing how a reader can obtain the data and what level of access the authors have

If the data are simulated, the seed and the data-generating process must be in the code so that the simulated dataset can be regenerated bit-identical.

### Reproducibility report

- A short narrative (one to two pages, included in the supplement) listing each figure and table in the paper, the script that produces it, the seed used, the runtime, and any non-determinism caveats
- A `sessionInfo()` output (R) or `pip freeze` output (Python) or equivalent, recording the environment in which the artifacts were produced
- Hash sums or git commit IDs that identify the exact code version that produced the included results

The reproducibility report is the document a kite-mark reviewer reads first.

## Common Failure Modes

These are the patterns that cost reproducibility points without the author noticing.

### Code that runs only on the author's machine

- Hard-coded paths to the author's home directory
- Dependencies on private packages, internal forks, or institution-only data servers
- Missing seed-setting calls; results not bit-identical across runs
- Implicit dependencies on operating-system-specific behavior (path separators, locale, line endings)

Fix: run the code in a fresh container or virtual machine before submission. If a colleague at another institution cannot reproduce the figures with the supplied artifact, the artifact is not yet ready.

### Data with undocumented restrictions

- Application data described as "publicly available" but actually requiring institutional access
- Data used under a data-use agreement that prohibits redistribution
- Sensitive data (health records, geolocation, demographics) shared without proper anonymization

Fix: distinguish between data that is genuinely public (with a permanent URL or DOI), data that requires application (describe the process), and data that cannot be redistributed (provide a synthetic dataset that mimics the structure and explain the path to the real data).

### Simulation results that are not reproducible

- Seed set inside a loop, with no recovery if the loop is re-entered
- Random number generator changed between R versions, between Python versions, or between `numpy.random` and `numpy.random.Generator`
- Multi-core simulations whose seed scheme depends on the number of cores

Fix: set seeds explicitly per replication, use a stateless RNG when possible, and record the RNG version in the reproducibility report.

### Software dependencies not pinned

- `requirements.txt` with `numpy` rather than `numpy==1.26.4`
- R script with `library(glmnet)` but no recorded version
- Reliance on a development branch that may change

Fix: pin exact versions of every dependency in the lockfile. For R, `renv::snapshot()` is the canonical tool; for Python, `pip freeze > requirements.txt` after testing in a clean environment.

### Application paper without the validation pipeline

- Cross-validation results reported but the CV code not included
- A holdout test mentioned but the split not reproducible
- Sensitivity analyses described in prose but not in code

Fix: every numerical result in the paper traces to a line of code in the artifact. If a number appears in the abstract, the artifact regenerates it.

## Audit Checklist

Run before final compile.

- [ ] Code repository exists and is accessible (private mirror is acceptable during review; public release before publication)
- [ ] `README.md` describes how to reproduce the results in fewer than ten steps
- [ ] All package and library dependencies are pinned to exact versions
- [ ] All data files are documented with a data dictionary
- [ ] All seeds are set explicitly and recorded
- [ ] Simulation studies regenerate the published figures and tables bit-identical
- [ ] Application analyses regenerate the published figures and tables bit-identical, or the source of non-determinism is documented
- [ ] Runtime for each major artifact is recorded
- [ ] Code has a license file
- [ ] Citation file references the paper as the canonical citation
- [ ] Reproducibility report is included in the supplement
- [ ] `sessionInfo()` or `pip freeze` output is included in the reproducibility report
- [ ] No hard-coded paths, no institutional dependencies, no private forks
- [ ] Data availability statement is in the manuscript and accurate
- [ ] Code availability statement is in the manuscript and accurate
- [ ] For JASA: ACC form completed
- [ ] For Biostatistics: D/C/R application prepared if pursuing the kite-mark
- [ ] For Biometrika: supplementary code or repository link is in the supplement
- [ ] For AOAS: replication code is in the supplement; consider applying for AAS reproducibility review

## Statements in the Manuscript

A reproducibility-aware manuscript includes three short statements, usually at the end of the discussion or in a clearly labeled section before the acknowledgments.

### Data availability statement

State whether the data are public, restricted, or simulated. If public, give the URL or DOI. If restricted, name the data provider and the access process. If simulated, point to the script.

### Code availability statement

State the location of the code (repository URL, DOI of a release, or supplementary file). State the license. State that the code regenerates the figures, tables, and numerical results in the paper.

### Reproducibility statement

For application papers, a one-sentence statement that the application results are reproducible from the supplied data and code, or that the application is reproducible from a synthetic dataset with the path to the restricted real data documented separately.

These three statements are typeset in plain prose without bullets in body sections. They are a Big Four convention, not an ML conference checklist.

## Integration with the Skill Family

This reference is consulted by:

- `stat-paper-plan`: when filling in the data availability and code availability columns of `PROJECT_PLAN.md`
- `stat-paper-write`: when drafting the data and code availability statements
- `stat-paper-writing`: as part of the final pre-submission audit
- `stat-polishing`: when the manuscript is polished but the reproducibility statements have not been verified
- `stat-mock-review`: when the AE-style verdict includes a reproducibility risk; missing artifacts can be a fatal or major concern depending on the venue

When the artifact is not yet ready, the reproducibility risk goes into `TECHNICAL_RISK_REGISTER.md` with `Severity = HIGH` until it is closed.
