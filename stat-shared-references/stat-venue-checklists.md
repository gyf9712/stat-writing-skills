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

## Journal of the American Statistical Association (JASA)

**Publisher:** American Statistical Association / Taylor & Francis

**Tracks covered here:**
- `JASA` = Theory and Methods (T&M)
- `JASA_ACS` = Applications and Case Studies (ACS)

**Last checked:** 2026-05-27 using accessible ASA-adjacent and Taylor & Francis sources. The live Taylor & Francis Instructions for Authors page for JASA was not directly retrievable (HTTP 403), so items marked `[VERIFY AT SUBMISSION]` must be confirmed on the live journal page or in the submission portal.

**Official journal home:** https://www.tandfonline.com/journals/uasa20

**Official Instructions for Authors URL to check at submission time:** https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode=uasa20

### Formatting and template

- If submitting in LaTeX, use the journal's official JASA / Taylor & Francis template linked from the JASA Instructions for Authors page. `[VERIFY AT SUBMISSION]`
- Public helper templates exist but should be treated as convenience tools rather than the binding source of record:
  - ASA-journal Quarto template: https://github.com/quarto-journals/jasa
  - Taylor & Francis author-template guidance: https://authorservices.taylorandfrancis.com/publishing-your-research/writing-your-paper/formatting-and-templates/
- Use a conservative review-manuscript format unless the live JASA page says otherwise:
  - 12-point Times New Roman
  - **double line spacing** for the manuscript
  - margins of at least 2.5 cm (1 inch)

### Length

- Use **35 double-spaced pages** as the operative JASA main-manuscript working limit.
- The accessible source citing JASA standards defines this as roughly **26-27 lines of text per page**.
- `[VERIFY AT SUBMISSION]` what exactly counts toward the 35-page limit. Because the live JASA instructions page was blocked at last check, use the **conservative assumption** that the counted manuscript runs **from abstract through references**, and move long appendices, proofs, extra simulations, and overflow tables and figures to supplementary material.

### Citation style

- Use **author-year citations**.
- Use the bibliography style file bundled with the official JASA template. `[VERIFY AT SUBMISSION]`
- Public ASA-journal helper templates currently use `agsm.bst`. This is a useful clue but should not override the official journal package if it differs.

### Supplementary material

- Treat supplementary material as **separate uploaded file(s)** for both T&M and ACS.
- Keep the main manuscript within the page limit and move overflow material to the supplement:
  - T&M: long proofs, technical lemmas, extended simulations
  - ACS: extended data description, additional validation, software / reproducibility documentation, extra analyses
- Do not assume cross-file LaTeX linking will be preserved in production. Prefer textual references to supplementary sections.

### Reproducibility

JASA has an established reproducibility-review workflow covering **all original research manuscripts**.

- As of September 1, 2021, all original research manuscripts submitted to JASA undergo reproducibility review. Authors are required to provide reproducibility materials when invited to revise.
- Authors must complete the **Author Contributions Checklist (ACC)** form. The ACC documents the data and code artifacts supporting computational findings.
  - ACC guide: https://jasa-acs.github.io/repro-guide/pages/acc.html
  - The ACC form is submitted as supplementary material at initial submission; the final version is published online with the article.
- A separate **reproducibility-package template** (not a LaTeX manuscript template) is suggested by the JASA Associate Editors of Reproducibility, providing a skeletal directory structure for `manuscript/`, `data/`, `code/`, `output/`, plus environment management (renv, conda, Docker).
  - Repository: https://github.com/jasa-acs/repro-template
  - Use is suggested but not required.

### AI disclosure

The Taylor & Francis publisher-level AI policy applies unless the live JASA instructions state a stricter journal-specific rule.

- AI tools must not be listed as authors.
- Authors must clearly disclose any generative-AI use within the article.
- The disclosure should include the tool name, version, how it was used, and why it was used.
- Authors remain fully responsible for accuracy, originality, references, and integrity.
- Generative AI must not be used to create or manipulate research results, clinical images, or other research-output figures.
- Official policy: https://taylorandfrancis.com/our-policies/ai-policy/
- `[VERIFY AT SUBMISSION]` whether JASA asks for the disclosure in a specific section or also requires a cover-letter statement.

### Peer review and anonymity

- No accessible official source retrieved confirmed double-anonymized review at JASA.
- Do not assume anonymous submission.
- `[VERIFY AT SUBMISSION]` whether the current JASA submission portal requests named or anonymized files. Until confirmed, treat JASA as non-double-anonymous.

### Cover letter

Prepare a cover letter for first submission even if the portal labels it optional. At minimum include:

- manuscript title
- target track (Theory and Methods or Applications and Case Studies)
- statement that the work is original and not under review elsewhere
- brief fit argument for JASA
- note any preprint, conference abstract, or prior public dissemination
- note any restricted-data or reproducibility constraints
- AI-use disclosure if requested by the journal or portal

For ACS, state the applied significance clearly.

### Track-specific editorial expectations

**JASA Theory and Methods (T&M):**
- Strong methodological contribution
- Real theoretical content (proofs in the supplement if necessary to stay within the page limit)
- Empirical validation through simulation studies
- Real-data analysis expected in most cases

**JASA Applications and Case Studies (ACS):**
- Application-driven paper
- Specific scientific question and dataset required
- Application section must carry real weight
- Reproducibility and practical utility matter heavily
- ACS has its own editorial team and reviewer pool of applied statisticians and domain experts
- Reproducibility editor may review code and data

### Other first-submission checks

- JASA is a hybrid open-access journal under Taylor & Francis Open Select.
- Add a concrete data-availability path and code-availability path.
- `[VERIFY AT SUBMISSION]` whether JASA currently requires author-supplied alt text at submission. Taylor & Francis is rolling out alt-text support across journals starting in early 2026.
- If using figures, follow Taylor & Francis image and artwork rules:
  - images and figures policy: https://authorservices.taylorandfrancis.com/editorial-policies/images-and-figures/
  - manuscript layout guide: https://authorservices.taylorandfrancis.com/publishing-your-research/writing-your-paper/journal-manuscript-layout-guide/

### Final-check implications

- Verify the LaTeX template comes from the live JASA Instructions for Authors page or its linked Taylor & Francis template.
- Confirm 35 double-spaced pages and what is counted; if in doubt, treat the limit as inclusive (abstract through references).
- Confirm `12pt`, double-spaced, 1-inch margins as the first-submission baseline.
- Author Contributions Checklist completed and uploaded as supplementary material at initial submission.
- Code repository prepared in the reproducibility-template structure if practical; even when not strictly required, this matches the form the reproducibility editors expect at revision.
- AI disclosure prepared per the Taylor & Francis policy.
- Verify the current JASA peer-review anonymity setting on the live submission portal.

### Note on choosing track

If the paper would not exist without a specific dataset and scientific question, submit to ACS. If the method is the primary contribution and the data is illustrative, submit to T&M.

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
