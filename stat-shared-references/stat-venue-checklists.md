# Venue Checklists for Statistics and ML Theory Journals/Conferences

Use this reference when setting the target venue in `stat-paper-plan` and during final checks in `stat-paper-write`.

## When to Read

- Read once when setting the target venue.
- Read again before locking the outline.
- Read again during final submission-readiness checks.

## Universal Requirements Across Statistics Journals

- Most statistics journals use author-year citation style (natbib with apalike or similar)
- Papers are typically not anonymous (authors visible from submission)
- No strict page limit for most journals, but strong norms exist
- Supplementary material is expected for proofs and additional results
- Reproducibility: code and data availability statements increasingly required
- Cover letters may be required or strongly recommended

## Annals of Statistics (AoS)

**Publisher:** IMS (Institute of Mathematical Statistics)

**Formatting:**
- Use IMS article style: `\documentclass[aos]{imsart}`
- Author-year citations with `natbib` (`\citet{}`, `\citep{}`)
- `\bibliographystyle{imsart-nameyear}` or `imsart-number`
- No strict page limit; typical papers are 25-40 pages (main) + supplement
- Two-column format is NOT used; single column throughout

**Content expectations:**
- Strong theoretical contribution required (rate-optimal results, minimax theory, new frameworks)
- Proofs must be rigorous and complete (main body proof sketches + full proofs in supplement)
- Simulation studies are valued but secondary to theory
- Real data applications are optional for purely theoretical papers
- Literature comparison should be thorough and precise

**Submission specifics:**
- Submit via IMS journal system
- Supplementary material uploaded separately
- Keywords and AMS subject classification required
- Data availability statement recommended

**Final-check implications:**
- Verify `\documentclass[aos]{imsart}` is used
- Verify citation style matches IMS requirements
- Check that all theorems have complete proofs (main + supplement)
- Ensure assumptions are precisely stated and discussed
- Verify rate comparisons with existing literature are explicit

## Journal of the American Statistical Association (JASA) — Theory and Methods (T&M)

**Publisher:** ASA (American Statistical Association) / Taylor & Francis

**Formatting:**
- Use JASA LaTeX template (available from journal website)
- Author-year citations with `natbib`
- `\bibliographystyle{asa}` (Chicago-style author-year)
- Typically 20-30 pages main + supplement
- Single column format

**Content expectations:**
- Strong methodology with theoretical justification and empirical validation
- Expects simulation studies AND real data analysis
- Code/software availability is strongly encouraged
- Reproducibility statement expected

**Submission specifics:**
- Submit via ScholarOne/Manuscript Central
- Cover letter required
- Supplementary materials uploaded separately
- Associate Editor assignment based on topic
- Submission category: "Theory and Methods"

**Final-check implications:**
- Ensure both simulations AND real data are present
- Check that the methodology has practical value beyond theory
- Verify the real data analysis provides substantive domain insights
- Ensure code/data availability is stated

## JASA — Applications and Case Studies (JASA ACS)

**Publisher:** ASA / Taylor & Francis

**Formatting:**
- Same JASA LaTeX template as T&M
- Author-year citations with `natbib`
- `\bibliographystyle{asa}`
- Typically 20-30 pages main + supplement (similar to T&M)
- Single column format

**Content expectations:**
- **Application paper track** — substantive scientific or applied problem is the primary driver
- A specific dataset and clear scientific question are required
- Methodological contribution can be novel or an adaptation that addresses the problem
- Real data analysis is the centerpiece (4-6+ pages typically)
- Simulation studies should be informed by the real data
- Theory in the main body is light (1-2 theorems max); heavier theory goes to supplement
- Detailed data description with exploratory analysis is expected
- Validation through holdout, cross-validation, or sensitivity is expected
- Substantive scientific findings must be reported and interpreted
- Code and data availability are strongly expected

**Submission specifics:**
- Submit via ScholarOne/Manuscript Central
- Cover letter must explain the applied significance
- Submission category: "Applications and Case Studies"
- ACS has its own editorial team and reviewer pool — applied statisticians and domain experts
- Reproducibility editor may review code/data

**Final-check implications:**
- Verify the scientific question is named in the first paragraph of the Introduction
- Verify a specific dataset is used throughout
- Check that Data and Background section is at least 2 pages with EDA
- Check that Application section is the longest section
- Verify comparison with methods used by the application community (not just statistical baselines)
- Ensure substantive findings are reported, not just method performance
- Verify code and data availability statements are present
- Read `stat-application-writing.md` for detailed application paper guidance

**Note on choosing track:** If the paper would not exist without a specific dataset and scientific question, submit to ACS. If the method is the primary contribution and the data is illustrative, submit to T&M.

## Journal of the Royal Statistical Society, Series B (JRSS-B)

**Publisher:** RSS (Royal Statistical Society) / Wiley

**Formatting:**
- Custom JRSS-B LaTeX class
- Author-year citations
- Single column format
- Typical length: 25-35 pages + supplement
- Read papers may have discussion and rejoinder (invited)

**Content expectations:**
- Among the most prestigious venues; expects foundational contributions
- Strong methodology with deep theoretical analysis
- Novel ideas preferred over incremental improvements
- Discussion papers: selected papers receive invited discussions from other statisticians
- Supplementary material for additional proofs and experiments

**Submission specifics:**
- Submit via ScholarOne
- Cover letter recommended
- Associate Editor system with careful matching

**Final-check implications:**
- Ensure the contribution is substantial enough for JRSS-B's prestige level
- Verify the methodology is general enough (not too niche)
- Check that the theoretical analysis is thorough, not just sketch-level
- Ensure the paper tells a compelling intellectual story

## Biometrika

**Publisher:** Oxford University Press (on behalf of the Biometrika Trust)

**Last checked:** 2026-05-27 against the official Biometrika author-guidelines page.

**Formatting:**
- Biometrika provides a style guide and LaTeX template.
- At first submission, exact house-style conformance is not required, but accepted papers must be revised to match the journal's style.

**Content expectations:**
- Biometrika publishes regular papers, synthesis papers, and miscellanea.
- Regular papers and synthesis papers are normally fewer than 20 pages.
- Miscellanea articles have a maximum length of 8 pages.

**Peer review / anonymity:**
- Biometrika uses single-anonymised peer review.
- Authors are identified to editors and reviewers. Reviewers are anonymous to authors.

**Supplement policy:**
- Submit a PDF of the main paper and a separate PDF file for any Supplementary Material.
- Treat the supplement as a separate submission artifact.
- Do not build the paper around linked cross-file LaTeX references.

**Accessibility and disclosure:**
- Alt text is required for all figures in the main article and should appear in the main manuscript directly under the relevant figure legend, preceded by `Alt text:`.
- If generative AI or AI-assisted technologies were used in the writing process, disclose this in the cover letter and in the manuscript before the Acknowledgement section under the title `Declaration of the use of generative AI and AI-assisted technologies`.

**Data and materials:**
- Where ethically feasible, Biometrika strongly encourages authors to make data and software available.
- Public datasets should be fully cited in the reference list, including the `[dataset]` tag and a persistent identifier when applicable.

**Final-check implications:**
- Treat Biometrika as a short-paper venue.
- Use 8 pages as a hard cap for Miscellanea.
- Add alt text and AI disclosure to the venue-specific final pass.

## Bernoulli

**Publisher:** IMS / Bernoulli Society

**Formatting:**
- IMS article style: `\documentclass[bj]{imsart}`
- Author-year citations with natbib
- `\bibliographystyle{imsart-nameyear}`
- Typical length: 25-40 pages
- Single column format

**Content expectations:**
- Probability and statistics theory
- Strong mathematical rigor required
- Connections to probability theory valued
- Empirical verification through simulations expected
- Clean, precise mathematical writing

**Submission specifics:**
- Submit via IMS journal system
- AMS subject classification required
- Supplementary material for long proofs

**Final-check implications:**
- Verify IMS formatting is correct
- Ensure probability-theory connections are explicit if relevant
- Check that assumptions connect to known probabilistic conditions

## Electronic Journal of Statistics (EJS)

**Publisher:** IMS (open access)

**Formatting:**
- IMS article style: `\documentclass[ejs]{imsart}`
- Author-year citations with natbib
- `\bibliographystyle{imsart-nameyear}`
- No page limit (open access); typical papers are 25-50 pages
- Single column format

**Content expectations:**
- Good venue for solid methodology + theory papers
- More permissive on length than print journals
- Detailed proofs can go in main body
- Comprehensive simulation studies welcome
- Code availability encouraged

**Submission specifics:**
- Submit via IMS system
- Open access (no cost to authors)
- Faster turnaround than some print journals

**Final-check implications:**
- Even though no page limit exists, avoid unnecessary padding
- Use the space for thorough proofs and experiments, not repetition
- Verify IMS formatting

## Annals of Applied Statistics (AOAS)

**Publisher:** IMS (Institute of Mathematical Statistics)

**Last checked:** 2026-05-27 against the official AOAS manuscript-submission and supplement-instructions pages.

**Formatting:**
- Use the IMS/AOAS LaTeX template with `\documentclass[aoas]{imsart}`.
- Use author-year citations.
- Submit the main manuscript as a PDF file.

**Content expectations:**
- AOAS is an application-driven venue. The paper must be framed around substantive scientific or policy questions with real data.
- Most published papers will not exceed 20 pages in the journal's standard style. Anything longer requires unusually compelling subject matter.
- Methodological innovation matters, but the application must carry real weight.

**Supplement policy:**
- The paper and supplement must be separate files.
- Do not use `\ref{}` or other cross-file LaTeX references from the main paper into the supplement.
- Cite the supplementary material in text and add a reference-list entry for it.
- Supplemental files posted with the paper may include data, code, algorithms, and supporting material.

**Reproducibility:**
- AOAS strongly encourages submission of data sets, computer algorithms, and supporting material.
- Applied papers should include a concrete data-availability path and a code-availability path.
- If public release is restricted, state the restriction and the closest feasible access path.

**AI disclosure:**
- No AOAS-specific generative-AI disclosure instruction was visible on the official AOAS submission or supplement pages checked on 2026-05-27.
- Mark this as `[VERIFY AT SUBMISSION]` and check the current journal and submission-portal policy before final submission.

**Final-check implications:**
- Treat 20 pages as the live AOAS norm.
- Keep the application central.
- Treat the supplement as a separate artifact.
- Include a concrete data/code availability path.

**Note on positioning:** AOAS reviewers are sophisticated about both statistics and applications. Papers that hide weak methodology behind an interesting application get rejected; so do papers that bolt a token application onto a methodology paper.

## Statistica Sinica

**Publisher:** Institute of Statistical Science, Academia Sinica

**Formatting:**
- Custom Statistica Sinica template
- Author-year citations
- Typical length: 20-35 pages
- Single column format

**Content expectations:**
- Methodology + theory contributions
- Values both theoretical depth and practical relevance
- Simulation studies and real data expected
- Good venue for papers with strong Asian connections

**Submission specifics:**
- Submit via journal's online system
- Cover letter required

## COLT (Conference on Learning Theory)

**Publisher:** JMLR Proceedings

**Formatting:**
- JMLR/COLT LaTeX style: `\documentclass[anon]{colt20XX}`
- Author-year citations with natbib
- **Anonymous submission** (unlike most stat journals)
- Main body page limit: typically 30 pages + unlimited appendix
- Single column format

**Content expectations:**
- Pure learning theory: generalization bounds, online learning, bandit theory, statistical learning
- Mathematical rigor paramount
- Proofs must be complete (main + appendix)
- Simulations optional but can strengthen the paper
- Connections to statistical theory valued
- Open problems and conjectures appreciated

**Submission specifics:**
- Submit via OpenReview or CMT (varies by year)
- Anonymous review
- Author response period
- Acceptance rate ~25-30%

**Final-check implications:**
- Verify anonymization is correct (no author names, no identifying self-citations)
- Check that the main body stands alone without the appendix
- Ensure the theory contribution is clear in the introduction
- Verify the paper fits COLT's scope (not pure statistics, not pure ML)

## ALT (Algorithmic Learning Theory)

**Publisher:** PMLR (Proceedings of Machine Learning Research)

**Formatting:**
- Custom ALT template based on PMLR style
- Anonymous submission
- Main body page limit: typically 20-25 pages + appendix
- Single column format

**Content expectations:**
- Learning theory, computational learning theory, statistical learning theory
- Mathematical rigor required
- Broader scope than COLT (includes computational aspects, online learning)
- Proofs should be complete

**Submission specifics:**
- Submit via EasyChair or CMT
- Anonymous review

## Biostatistics

**Publisher:** Oxford University Press

**Last checked:** 2026-05-27 against the official Biostatistics author-guidelines and supplementary-data pages.

**Submission format:**
- First submission is format-neutral. A readable PDF or Word file is acceptable; exact house style is not required at first submission.
- Revised manuscripts must follow the journal's formatting and file-organization requirements.

**Reproducible research policy:**
- Biostatistics uses reproducible-research kite-marks:
- `D` = data freely available
- `C` = code freely available
- `R` = both data and code freely available
- Data and code supporting these marks are published electronically as Supplementary Materials.

**Supplement policy:**
- Biostatistics uses a main manuscript plus Supplementary Materials.
- Supplementary material is online-only material associated with the paper.
- The supplementary material should carry the same title, authors, and affiliations as the main manuscript, with `Supplementary Materials` appended to the title.
- Cross-referencing from the main paper to the supplementary material is expected when relevant. Do not enforce a blanket ban on main-to-supplement references for this venue.

**AI disclosure:**
- If AI is used to generate content, images, code, process data, or for translation, disclose this in the cover letter and in the manuscript.
- Put the manuscript disclosure in the Methods or Acknowledgements section.
- AI tools do not qualify as authors.

**Accessibility:**
- Alt text is required for all figures in the main article and should appear in the manuscript directly under the relevant figure legend, preceded by `Alt text:`.

**Editorial implications:**
- The editors may require technical material or extensive simulations to be moved into the Supplementary Materials.
- The main paper should stay focused; heavy technical overflow belongs online.

**Final-check implications:**
- Support the `D/C/R` reproducibility path explicitly.
- Allow main-paper references to the supplementary material.
- Do not force house-style LaTeX on the initial draft if the submission is still at first-submission stage.

## Other Applied Statistics Journals

These are application-paper venues with their own specializations. They share core expectations with AOAS and JASA ACS, with substantive problems, real data, validation, and reproducibility, but each has a domain focus.

### Statistics in Medicine (Wiley)
- Medical statistics applications
- Broader scope than Biostatistics (includes more methodology with medical motivation)
- Typical length: 15-25 pages

### Journal of Computational and Graphical Statistics (JCGS)
- Methods with computational or visualization emphasis
- Application paper track exists; methodology with strong computational implementation also fits
- Software/reproducibility especially important
- Typical length: 20-30 pages

### Journal of Agricultural, Biological, and Environmental Statistics (JABES)
- Applications in agriculture, biology, environment, ecology
- Domain-specific data structures (spatial, longitudinal, ecological)
- Typical length: 15-25 pages

### Annals of Applied Probability (AAP)
- Probability-driven applications
- Different from AOAS — leans more probabilistic than statistical

When in doubt, check the journal's recent issues to confirm fit before submission.

## Mathematical Statistics and Learning (MSL)

**Publisher:** European Mathematical Society (EMS)

**Formatting:**
- EMS journal style
- Author-year or numeric citations (check current guidelines)
- No strict page limit
- Single column format

**Content expectations:**
- Mathematical foundations of statistics and machine learning
- Strong emphasis on mathematical rigor
- Connections between statistics and mathematics
- Newer journal (est. 2018), building reputation

## Statistics-Specific Citation Conventions

### Author-Year Style (Most Stat Journals)

```latex
\usepackage{natbib}
\bibliographystyle{plainnat}  % or apalike, imsart-nameyear, asa, biometrika

% In text:
\citet{bickel2009}  → Bickel et al. (2009)
\citep{bickel2009}  → (Bickel et al., 2009)
\citet[Theorem 3]{bickel2009}  → Bickel et al. (2009, Theorem 3)
```

### Common Statistics References to Include

Depending on the topic, consider citing foundational works:
- Nonparametrics: Tsybakov (2009), Wasserman (2006)
- High-dimensional: Bühlmann & van de Geer (2011), Wainwright (2019)
- Minimax theory: Yang & Barron (1999), Tsybakov (2009)
- Semiparametrics: Bickel et al. (1993), van der Vaart (1998)
- Empirical processes: van der Vaart & Wellner (1996)

## Minimal Submission Checklist

Before submission, verify:

- [ ] Venue-specific LaTeX template is correctly applied
- [ ] Citation style matches venue requirements (author-year vs numeric)
- [ ] Page length is within venue norms
- [ ] All theorems have complete proofs (main + supplement)
- [ ] Assumptions are stated, labeled, and discussed
- [ ] Rate comparisons with prior work are explicit
- [ ] Simulation study includes multiple DGPs, sample sizes, and comparison methods
- [ ] Standard errors from Monte Carlo replications are reported
- [ ] Real data analysis is present (if venue expects it)
- [ ] Code/data availability statement is included
- [ ] Cover letter is prepared (if required)
- [ ] Keywords and subject classification are provided
- [ ] Supplementary material is properly organized and referenced
