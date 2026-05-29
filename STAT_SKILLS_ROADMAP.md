# Stat Skills Roadmap

Prioritized improvement list for the `stat-paper-plan`, `stat-paper-write`, `stat-paper-writing`, `stat-polishing` skill family and their shared references. Drafted 2026-05-27 from a Codex MCP review (GPT-5.4 xhigh) by a senior-statistician persona.

This file tracks improvements that were deferred from the initial Codex-review-driven fix pass. Tier A fixes were applied immediately; Tier B and Tier C are tracked here for future iteration.

## Applied in this iteration (May 2026)

The following were fixed in the same session as the Codex review:

- Corrected AOAS venue entry (typical 20 pages, supplement-as-separate, citation-of-supplement, AI disclosure VERIFY flag) in `stat-shared-references/stat-venue-checklists.md`.
- Corrected Biometrika entry (Miscellanea max 8 pages, single-anonymised, alt text, AI disclosure).
- Replaced Biostatistics subentry with a full venue block (D/C/R kite-marks, format-neutral first submission, main-to-supplement cross-references ARE expected, AI disclosure, alt text).
- Updated `MAX_PAGES` line in `stat-paper-plan/SKILL.md` to reflect corrected page norms.
- Introduced `SUPPLEMENT_MODE = separate_self_contained | linked_appendix` with venue-default mapping in `stat-paper-write/SKILL.md` and `stat-paper-plan/SKILL.md`. Removed the implicit global ban on main-to-supplement cross-references.
- Fixed malformed Agent invocations in `stat-paper-write/SKILL.md` (replaced bare-colon-block with canonical `Agent(subagent_type="general-purpose")` form).
- Added required `PRIOR_WORK_MATRIX.md` artifact step (Step 5.5) to `stat-paper-plan/SKILL.md` with column schema and novelty-risk rule.
- Added required `TECHNICAL_RISK_REGISTER.md` artifact step (Step 5.6) to `stat-paper-plan/SKILL.md` with column schema and sign-off rule.

### Follow-up iteration (May 2026, same session)

The Codex review made positioning and technical claim strength the two highest-priority unaddressed risks. The following additions address both, directly in `stat-paper-write` and `stat-polishing`:

- Created `stat-shared-references/stat-positioning-and-claims.md`. This is the centerpiece: a full protocol for the positioning audit and the technical claim strength audit, a schema for `CLAIM_SUPPORT_MAP.md`, common positioning failure modes, common claim failure modes, a Codex MCP prompt template for an independent audit, and the ordering rule that positioning and claim audits must precede style polishing.
- Added Step 2.5 to `stat-paper-write/SKILL.md`: build `CLAIM_SUPPORT_MAP.md` before drafting the front matter. Each prose claim must trace to a `PRIOR_WORK_MATRIX.md` row, a `TECHNICAL_RISK_REGISTER.md` row, and a piece of verified literature support.
- Added Step 5.5 to `stat-paper-write/SKILL.md`: post-drafting positioning and claim audit. Codex can run the independent audit for high-stakes submissions.
- Added positioning and claim audit checks to the final-checks section of `stat-paper-write/SKILL.md`.
- Elevated positioning and claim audit to a Key Rule in `stat-paper-write/SKILL.md`.
- Added a reference-table entry pointing to `stat-positioning-and-claims.md` as the first file to read in `stat-polishing/SKILL.md`.
- Restructured the `stat-polishing/SKILL.md` workflow: positioning audit and claim strength audit now come before style polishing, with the explicit warning that polishing prose on top of an overclaim makes the overclaim more confidently stated.
- Expanded the Codex prompt in `stat-polishing/SKILL.md` to perform a three-level audit (positioning + claim strength, Big Four standards and voice, line-level AI tells), in that order.
- Elevated positioning and claim audit to a Key Rule in `stat-polishing/SKILL.md`, with the literature-support requirement for comparative claims.
- Added a `Read In Full` column to the `PRIOR_WORK_MATRIX.md` schema in `stat-paper-plan/SKILL.md` to surface the most common source of overclaim: citing a paper for what the author assumes it says rather than what it actually proves.
- Linked the planning matrices to `CLAIM_SUPPORT_MAP.md` in `stat-paper-plan/SKILL.md`.

The combined effect: every positioning claim and every comparative technical claim now requires (1) a matched `PRIOR_WORK_MATRIX.md` row with the cited paper actually read in full, (2) a matched `TECHNICAL_RISK_REGISTER.md` row, (3) verified literature support recorded in `CLAIM_SUPPORT_MAP.md`, and (4) a SUPPORTED or SUPPORTED-with-qualification status before the prose can ship.

This directly addresses Codex's diagnosis that the skills had not yet protected against the two things that actually kill top-stat submissions: weak positioning and unverified technical overclaim.

### Literature cache integration + SKILL.md compactification iteration (May 28, 2026, four-commit sequence)

After the earlier token-economy iteration, the user identified literature reading as the dominant remaining cost (~100-300K tokens per session on stat-theory work). A Codex MCP review (threadId `019e70c3-1844-7181-b6a1-0b4041c657df` for rounds 1-2; `019e7112-283e-74b1-97e5-6344592cd820` for round 3 after the original expired) over three rounds shaped a four-commit response.

The companion `gyf9712/stat-theory-skills` repo carries the heavy lifting in CHANGELOG v1.8.0 (commits 612f170, 668cc64, 3bd1e65, plus the round 3 cleanup commit). Stat-writing-skills hosts the protocol consumers.

Applied to `stat-writing-skills` across the four commits:

- `stat-polishing/SKILL.md`: 855 → 783 lines (-72, -8%). Sentence/paragraph/bullet/punctuation rules collapsed to a single 15-line block pointing to `stat-style-discipline.md`. AI-template removal section collapsed to a 13-line headline + pointer to the canonical lists in `stat-style-discipline.md`. (commit 28a3004)
- `stat-shared-references/stat-positioning-and-claims.md`: Step 3 literature search gained a new step 0 cache-consult before the 5-source search strategy. Positioning citations now map to citation purposes (`benchmark_claim` / `lineage_positioning` / `comparative`). Cache hits at `independently_checked` admissible as positioning evidence without re-fetch. Cache write-back to inbox after every fresh fetch. Project lock manifest update at `papers/<project>/cited_results.lock.md`. (commit ea3594d)
- `stat-paper-plan/SKILL.md` Step 5.5 `PRIOR_WORK_MATRIX`: the `Read In Full` column now resolves to a literature cache entry by `paper:<bibkey>#<result_id>`. Cache hits at `independently_checked` satisfy `Read In Full` without re-reading. `Citation Verified = yes` requires the cache entry at `source_checked` or higher. (commit ea3594d)
- `stat-mock-review/SKILL.md` Step 3: fatal-or-major mock review concerns that name a specific theorem of a cited paper now resolve to the project lock manifest and the cache. Required verification floor: `independently_checked` for load-bearing fatal/major; lower states demote to verification-request-pending rather than load-bearing finding. (commit ea3594d)

Cache protocol files (in sibling `stat-theory-skills/stat-shared-references/`, accessible to stat-writing skills via the shared cache infrastructure):

- `literature-cache-protocol.md` (206-line router with Minimum Load Map for 12 use cases)
- `citation-purpose-protocol.md` (7 citation purposes; trigger keyword table forcing explicit declaration on extension / improvement / priority / weakening / lineage / technique-borrow / standard-tool / contrast / match keywords; 2D verification gate matrix; 13+10 methodological roles split into historical and relational dimensions)
- `applicability-axes.md` (8 axes; namespaced families per domain with conservative tightening — `tail_condition` split into `exponential_concentration` vs `moment_bounded` to prevent the `sub_gaussian = polynomial_p_moment` substitution Codex round 3 V9 flagged as too liberal)
- `cache-verification-states.md` (4 evidence-based verification states; F1/F2/F3 workflows; inbox/queue + `/lit-cache verify` promotion; project-side pin manifest mechanics)

Deferred to Commit 5 (next):

- `/lit-cache verify` MVP — currently the protocol references `/lit-cache verify` and `/lit-cache audit` skill workflows but no implementation exists. Codex round 3 V7 marked this as REQUIRES FIX: without verification promotion, entries stay at `unverified_extract` and the strict gate ("background mention requires source_checked") blocks all citation use.
- `cited_results.lock.md` ownership formalization — Codex round 3 V8 marked the absence of a designated owner as REQUIRES FIX. The lock manifest is referenced by every literature-touching skill but no skill currently has the canonical responsibility to create it.

Token-savings update (replacing the prior estimate):

- Cache miss (first time reading paper X): ~5-15K tokens for source fetch + extraction; ~1K tokens for inbox write
- Cache hit at `source_checked` (subsequent project needing paper X): ~1-3K tokens for result-scoped Read
- Cache hit at `independently_checked` (load-bearing use in another project): same ~1-3K; the Codex MCP cost of the original `independently_checked` upgrade was paid once when the entry was promoted
- Compactification savings: instead of inline duplicated content in each SKILL.md, shared refs are loaded only by skills that need them per the Minimum Load Map. Per-invocation context load reduces by 200-300 lines for proof-repair, 70-80 lines for stat-polishing.
- Aggregate target unchanged from prior iteration: 25-30% session-level token reduction with zero compromise on Big Four polish or proof verification quality. Cache hit rate above 30-50% (realistic for projects sharing anchor papers like Talagrand, Bickel-Levina, Tibshirani, van der Vaart) dominates the savings.

### Token economy iteration (May 28, 2026, late session)

User surveyed [rtk-ai/rtk](https://github.com/rtk-ai/rtk) for token-saving strategies and asked which apply. A second Codex MCP review (threadId `019e6ed3-0b5d-7e72-b424-5428423a2276`, `model_reasoning_effort: xhigh`) evaluated seven candidate optimizations across both `stat-writing-skills` and `stat-theory-skills`. After a per-verdict deliberation pass and one round of push-back on OPT7 (Codex honestly self-assessed an anchoring effect on sequential per-repair stress-tests; the protocol now requires fresh threads per logically-independent repair), the converged plan executed the highest-ROI three for both repos and deferred the rest.

Applied to `stat-writing-skills` in this iteration:

- Added the **Reasoning Effort Ladder** to `stat-shared-references/stat-codex-dialogue.md`. Default Codex reasoning effort drops to `medium`; `xhigh` is forced whenever the call's scope includes a theorem / lemma / proposition / corollary statement, assumption block change, proof step, rate, quantifier, probability level, positioning claim against a named prior paper, weakened-claim revision in polish, `CLAIM_SUPPORT_MAP.md` overclaim decision, or `MOCK_REVIEW.md` fatal-or-major-concerns section. Allowed `medium` calls are spelled out: prose polish on non-mathematical sentences, figure caption critique, figure-design audit, reproducibility checklist triage, LaTeX template conformance, citation completeness, style-discipline audit, venue-checklist triage, caption capitalization audit. The trigger is **content-driven, not skill-driven** — `stat-polishing` polishing a theorem statement still forces `xhigh`.
- Added the **Artifact Manifest Header** convention to `stat-shared-references/stat-codex-dialogue.md`. Every artifact generated by a Codex-invoking stat skill begins with `artifact / scope / source_files / sections_covered / venue / claim_ids / commit / generated / generator`. Applies to `PAPER_PLAN.md`, `PRIOR_WORK_MATRIX.md`, `TECHNICAL_RISK_REGISTER.md`, `CLAIM_SUPPORT_MAP.md`, `POLISHING_REVIEW.md`, `MOCK_REVIEW.md`, `codex_discussion.md`, `LATEX_AUDIT_REPORT.md`, `REPRODUCIBILITY_AUDIT.md`, `NOTATION_AUDIT.md`, and every per-section polishing artifact. Enables lazy loading, staleness detection, and token-economic chained calls.
- Installed rtk (`brew install rtk` + `rtk init` writing `~/CLAUDE.md`) for transparent compression of Bash calls inside skill workflows. `git status`, `git diff`, `find`, `grep`, `wc`, `ls`, `tree` get 60-90% compression; `latexmk`, `pytest`, `*.log`-piping commands are passthrough so diagnostic output is not damaged. Failure recovery via rtk's tee mode at `~/.local/share/rtk/tee/`.

Per the dialogue protocol, Codex's seven OPT verdicts: 3 ADOPT, 3 MODIFY-with-scope, 1 SKIP-with-modification-to-fresh-thread-protocol. Push-back on OPT7 produced the three-case distinction (Case A cross-phase fresh thread + manifest; Case B within-phase iterative push-back via `codex-reply`, same thread; Case C within-phase independent units fresh thread per repair or 2-3 cluster). All four refinements I proposed confirmed by Codex.

Deferred items for the next stat-writing-skills iteration:

| OPT | Description | Effort | Session savings | Notes |
|---|---|---|---|---|
| 2 | Per-venue file split (`stat-shared-references/venues/{biometrika,jasa,aos,jrss-b,aoas,bernoulli,ejs,biostatistics,jcgs}.md`) + `venues/INDEX.md` | Half day | ~5% | Codex ADOPT; current venue tables in `stat-style-discipline.md`, `stat-figure-design.md`, `stat-venue-checklists.md` would be split; skills read only the target venue file. |
| 3 | Codex `cwd` + read-receipt protocol for long-manuscript calls (>30 pages) | 1-2 days | ~15% on long papers, near-zero on short | Codex ADOPT with hard protocol (Codex must list files opened, anchors inspected, line ranges read; `INSUFFICIENT CONTEXT` is a valid response). Scoped to long manuscripts only; ~20-page polishing/mock-review stays on paste. |
| 5 | Anchor-then-window Read pattern for `.tex` and shared-reference markdown, gated on relevant context being pre-loaded | Half day | ~10% | Codex MODIFY; permissible when assumption ledger and dependency graph (for theory papers) or the relevant section's TOC (for shared refs) is in scope. Otherwise full file Read. |
| 6 | Canonical store + ID references in audit artifacts | 1-2 days | ~5% + consistency benefit | Codex ADOPT; `CLAIM_SUPPORT_MAP.md` and `PRIOR_WORK_MATRIX.md` become the only sources of truth for their respective objects; other artifacts reference by `CS-N` / `PW-N` IDs with auto-generated compact legend per call. |

Codex thread for the dialogue: `019e6ed3-0b5d-7e72-b424-5428423a2276`. The companion `stat-theory-skills` CHANGELOG v1.7.0 records the same dialogue from its side and applies the parallel changes (per-repair fresh thread in `proof-repair` Step 5C, manifest headers on `proofcheck` artifacts, reasoning ladder in `CODEX_PROTOCOL.md`).

### Leey21 cross-pollination + emphasis discipline iteration (May 28, 2026)

This iteration audited [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) (a Chinese-community prompt and skill library for ML/CV/NLP top conferences) for ideas worth porting into the Big Four stat-writing-skills, and incorporated a new author-supplied style rule against emphasis formatting. A second Codex MCP dialogue (single-pass at `model_reasoning_effort=xhigh`) ranked the candidate additions and rejected several as CV/NLP cargo cult that would damage a Big Four submission.

Codex priority ordering for the candidate set: `page-fit > mock-review > reader-test > figure-selection logic > AI-vocab watchlist > docx (venue-gated) > caption rule fix > splash-figure prompt (rejected)`.

Applied in this iteration:

- Added an `Emphasis Formatting Discipline` section to `stat-shared-references/stat-style-discipline.md`. Bans bold, italics, underlining, color, small caps, and boxed text in body prose. Permits emphasis only for journal-conventional objects (theorem class headers, first-use italic for term definition, vectors and matrices when the venue uses bold notation, table column headers, bibliographic conventions). Includes a per-venue table noting that Biometrika is strictest (no bold for vectors and matrices either), ASA journals are looser (bold OK for vectors and matrices), JRSS-B and IMS journals defer to the class, and Biostatistics and JCGS follow class defaults. Codifies the author's directive: minimize emphasis except where genuinely needed for headline-level content.
- Reframed the `AI Watchwords` subsection as a watchlist rather than a blacklist. Each candidate occurrence is evaluated with three questions (information value, weakening on cut, technical vs rhetorical use). Added `unveil`, `foster`, `galvanize`, `harmonize`, `hone`, `paradigm`, `paradigm shift`, `transformative` to the list. Per Codex: hard bans produce false positives where the word has a legitimate technical use.
- Added a `Biometrika-Style House Bans` subsection covering bans that are useful Big-Four-wide: `Note that` at sentence start, `is given by` in mathematical phrasing, homemade method acronyms, in-text `w.r.t.` / `s.t.` / `i.f.f.`, `It can be shown that` without locator, repeated `In this paper`. Per Codex: Biometrika's actual house bans are higher signal than a generic AI-vocab list.
- Extended the prose audit checklist in `stat-style-discipline.md` with new items for emphasis formatting count, `Note that`, `is given by`, homemade acronyms, and in-text abbreviations.
- Added a `Caption Capitalization and Punctuation` subsection to `stat-shared-references/stat-figure-design.md`. Replaces an earlier (incorrect) proposal of Title Case for noun-phrase captions. Defaults to sentence style with terminal period and includes a per-venue table. Biometrika is noted explicitly: figure captions end with full stop, table titles' last sentence does not. Per Codex: Title case is an ML conference convention and is wrong for the Big Four.
- Added a `Choosing the Figure Type` section to `stat-figure-design.md`. The framing is statistical-question-driven rather than chart-type-menu (the Leey21 source provided a 19-chart taxonomy that was rejected as visualization-fluency tour). Maps common Big Four figure questions (rate verification, estimator distinguishability, distribution shape, trade-off, calibration, EDA, effect plus uncertainty, class-imbalanced classifier, tuning behavior, dependence structure) to default displays.
- Added a `Big Four guardrails` subsection to `stat-figure-design.md`. Bans: violin plots without sufficient replication count, broken axes, dual-y plots (except deterministic transformations), inset legends in tight-layout venues (Biometrika), facet grids over 4-by-4, 3D plots, pie charts in body content. Requires uncertainty for every interpreted estimate and consistent encoding across all figures in the paper.
- Added an `Architecture and splash figures` subsection. Per Codex: the DeepMind-pastel-flat-vector "framework figure" style common at NeurIPS and ICML is rejected outright; AI-generated method-overview figures would damage a Big Four submission and trigger OUP disclosure requirements regardless. TikZ method diagrams with minimal labels are the acceptable substitute when a diagram is genuinely needed.
- Extended the `Common Figure Problems and Fixes` table and the `Pre-Submission Figure Checklist` with new rows covering title-case captions, violin sample size, dual-y, broken axes, inset legends, 3D plots, pie charts, splash figures, AI-figure disclosure.
- Added a `Mode: Page-Fit Micro-Edit` section to `stat-polishing/SKILL.md`. Local paragraph-level compression and expansion when the manuscript is over the venue's page cap by one to three pages. What to preserve (assumptions, citations, numerical values, claim strength, notation). What to cut first (meta-discourse, signposting, soft intensifiers, hedge stacking, supplement-able derivations, restated definitions, redundant bullets). Per Codex: the original `preserve all information` framing was too strong; preserve scientific content, not every word.
- Added a `Mode: Three-Reader Pre-Submission Test` section to `stat-polishing/SKILL.md`. Three simulated readers in sequence: Associate Editor (why should statisticians care?), technical referee (is this correct and useful?), applied statistician (could I use this on my data?). For each, record the first point of friction and the smallest change that clears it. Per Codex: Big Four reading is sequential by reader type, not a single "is this paper good" assessment.
- Created `stat-mock-review/` as a new skill. Produces a single-pass AE-style pre-submission report (`MOCK_REVIEW.md`) with seven fixed sections: synopsis, fatal concerns, major concerns, minor concerns, venue-fit risk, likely initial editorial action (verb, not number), and rescue plan. No 1-10 rating. Per Codex: journal editors decide on verbs (desk reject, send out, invite revision); the conference scoring idiom misleads statistics authors about how journals work. Distinguished from the Codex MCP iterative dialogue (multi-turn) and `stat-polishing` (improvement loop) on the basis that this skill produces a snapshot verdict.
- Created `stat-shared-references/stat-reproducibility-audit.md`. Per Codex (missed-item flag): Big Four expectations on reproducibility have tightened; JRSS-B and Biometrika now expect code and reproducible simulations for new methods; Biostatistics offers D/C/R kite-marks; JASA requires the ACC form. The reference covers code, data, reproducibility report, common failure modes (machine-specific code, undocumented data restrictions, non-reproducible simulations, unpinned dependencies, missing validation pipelines), and an audit checklist. Bundles the three submission statements (data availability, code availability, reproducibility) authors must include.
- Created `stat-shared-references/stat-notation-audit.md`. Per Codex (missed-item flag): undefined notation and homemade acronyms are persistent referee-report items, especially at Biometrika. Two-layer audit: symbol inventory (every symbol defined on first use) and acronym inventory (every acronym standard or defined). Includes a list of standard statistics acronyms that can be used without expansion, discipline for new method names (descriptive phrase preferred over invented acronym), and an audit checklist.

Rejected after Codex review:

- The 19-chart taxonomy as a chart-type menu (replaced with statistical-question-driven selection logic; the menu was a visualization-fluency tour that does not match the Big Four reading style).
- The Title Case caption rule for noun-phrase captions (defaults to sentence style with terminal period per the actual Big Four house styles; the proposed rule was a CV/NLP convention).
- The conference-style 1-10 numerical rating in the mock-review skill (replaced with the editorial action verb; journals do not aggregate scores).
- The DeepMind-pastel-flat-vector splash figure prompt (rejected as CV/NLP cargo cult that would damage a Big Four submission; AI-generated figures also trigger OUP disclosure requirements).
- An automatic AI-vocabulary blacklist (replaced with the watchlist framing; hard bans produce false positives on legitimate technical uses).

Deferred to future iteration:

- A `.docx` mode (venue-gated; relevant for Biostatistics and Statistics in Medicine but not core Big Four since all four Big Four venues prefer or require LaTeX). Track as a low-priority addition.

Codex thread for this iteration: ran as a single `codex exec` non-interactive call rather than as an MCP dialogue. The full prompt and reply are preserved in the author's local notes; the threadId from the MCP-mode follow-up will be recorded here when the next dialogue round begins. The single-pass framing was sufficient because Codex's verdicts and Big Four citations were self-consistent and no point required pushback.

### Dialogue discipline iteration (May 2026, same session)

The initial Codex integration was phrased as if Codex feedback should be applied wholesale ("apply CRITICAL and MAJOR fixes from Codex"). That framing was wrong. Codex is a senior reader, not an oracle, and is frequently mistaken about specific theorem numbers, numerical constants, and very recent papers. The author's job is to evaluate each criticism on its merits.

The following were updated to reflect this:

- Created `stat-shared-references/stat-codex-dialogue.md`. The new file codifies the dialogue principle: discuss with Codex until convergence rather than apply wholesale. Three outcomes per criticism (accept, push back, log disagreement), when Codex is most likely right or wrong, the convergence test, the documentation expectations, common failure modes of the dialogue.
- Updated `stat-paper-plan/SKILL.md` Step 7 Pass B to invoke the dialogue principle and link to the new reference. The closing language changed from "apply the accepted feedback" to "apply accepted criticisms (not all criticisms); carry documented disagreements forward".
- Updated `stat-paper-write/SKILL.md` Step 6 Pass B with the same reframing. The three-outcome decision is now explicit. The closing instruction to verify proposed replacement sentences before pasting is new.
- Updated `stat-paper-writing/SKILL.md` Phase 5 to apply the dialogue principle to the improvement loop. Round 2 is now an "external dialogue" rather than an "external review", and Round 3 is an "extended dialogue" up to 2 to 4 total rounds.
- Updated `stat-polishing/SKILL.md` Step 11 to reframe "apply Codex feedback" as the three-outcome dialogue. Added the new reference to the file's reference table.
- Updated `stat-shared-references/stat-positioning-and-claims.md` Codex integration section. The opening call is now described as starting a conversation; pushback patterns are explicit ("On the criticism of claim CS3: I disagree...").
- Updated `stat-shared-references/stat-writing-principles.md` companion-references list to include the new reference.

The effect: the skills no longer treat Codex as authoritative. They use Codex as a senior dialogue partner whose criticism the author evaluates and decides on, criticism by criticism. Documented disagreements carry forward to the submission and rebuttal stages.

## Roadmap for next iteration (priority order)

These are the items Codex identified as important but that are deferred to a future iteration rather than applied immediately.

### 1. Venue-by-venue compliance refresh with `last_checked` and sources

Add a `last_checked` date and a list of official source URLs to every venue block in `stat-venue-checklists.md`. The Biometrika, Biostatistics, and AOAS blocks now follow this pattern; bring the rest up to the same standard.

Done means: every venue block has (a) a `Last checked:` date, (b) a list of official URLs, (c) explicit `[VERIFY AT SUBMISSION]` flags for any rule that could not be confirmed.

### 2. Submission package skill

Build a new skill `stat-submission-package` covering:

- Cover letter drafting (AE-facing positioning)
- Funding statement
- Conflict-of-interest statement
- AI disclosure statement (venue-specific wording)
- Data availability statement (D/C/R-style or plain prose)
- Code availability statement
- Alt text generation for figures
- Dataset citations and persistent identifiers
- Final upload inventory

This addresses the gap between "writing finished" and "ready to submit".

### 3. PRIOR_WORK_MATRIX and TECHNICAL_RISK_REGISTER as hard gates

The matrices are now required artifacts in `stat-paper-plan` but the writing skill does not yet block on them. Next iteration: `stat-paper-write` should refuse to draft the abstract or introduction until:

- All `Novelty Risk = HIGH` rows in `PRIOR_WORK_MATRIX.md` have been resolved
- All `Severity = CRITICAL` rows in `TECHNICAL_RISK_REGISTER.md` are `CLOSED` or explicitly downgraded

### 4. Reproducibility packaging module

Beyond statements, build the actual artifacts:

- Replication script that reproduces all figures and tables from raw data
- `sessionInfo()` or equivalent output committed
- Figure provenance (which script, which seed, which data version)
- Repository checklist (README, LICENSE, data dictionary, install instructions)
- Reproducibility badge / kite-mark application support (D, C, R for Biostatistics; ACM Artifact Evaluation; etc.)

### 5. Prompt de-duplication

Move repeated style, figure, supplement, and review rules out of SKILL.md files into shared references. Currently, the four SKILL.md files repeat the same style discipline blocks, figure rules, supplement rules, and reviewer checklists. The duplication has two costs:

- Inconsistency risk when one place is updated but not the others
- AI-tell amplification when the same prescriptive blocks are repeated in instruction text

Done means: each rule lives in exactly one shared-reference file; SKILL.md files reference rules by name and section, not by re-stating them.

### 6. PDF-aware review path for figure quality

Currently the figure design rules are enforced through prose review. A PDF-aware review path would:

- Open the compiled PDF
- For each figure: check that no title is inside the figure, captions are self-contained, no legend overlaps the data, fonts are readable at journal column width
- For the bibliography: check entry types, missing fields, duplicate keys
- For page budget: count main-body pages excluding references, compare with venue norm

This requires extending the pipeline to actually open and parse PDFs.

### 7. Domain packs

Build content packs for common statistics paper classes:

- Causal inference (estimands, identification assumptions, sensitivity analysis)
- Survival / event-history (Cox model assumptions, competing risks, time-varying covariates)
- Bayesian computation (prior elicitation, MCMC diagnostics, posterior summaries)
- Missing data (mechanism notation, multiple imputation reporting)
- Spatial-temporal (model structure, covariance specification, projection)
- Longitudinal / multilevel (within/between effects, random-effects structure)
- Multiple testing (FDR vs FWER, dependent test handling)
- Semiparametric (efficient influence function, double robustness)

Each pack would contribute: a section template, an assumption checklist, a simulation DGP template, a comparison-method list.

### 8. Revision workflow

Build a `stat-revision` skill family:

- AE-facing cover letter drafting in response to a decision
- Referee-response drafting with point-by-point matrix
- Revision plan with priority order
- Tracked-changes generation and management
- Resubmission readiness check

This is parallel to but distinct from `nature-response`.

### 9. Claim-boundary auditing (partially addressed in the follow-up iteration)

Largely addressed by `stat-positioning-and-claims.md`, the `CLAIM_SUPPORT_MAP.md` artifact, and the audit steps now in `stat-paper-write` and `stat-polishing`. The remaining work for the next iteration:

- Automate the extraction of positioning and technical claims from the LaTeX source (currently a manual step).
- Build a `stat-claim-audit` slash-command skill that takes a draft and produces `CLAIM_SUPPORT_MAP.md` semi-automatically.
- Add specific detectors for theorem scope drift (abstract claims more than the theorem states), lower-bound mismatch (upper and lower bounds on different function classes), and application overclaim (prediction quality interpreted as causal effect).

### 10. Skill-level prose cleanup

The SKILL.md files themselves use em-dashes heavily, which contradicts the discipline they enforce. Targets per Codex:

- `stat-paper-plan/SKILL.md`: cut from about 94 em-dashes to at most 10
- `stat-paper-write/SKILL.md`: cut from about 64 em-dashes to at most 5
- `stat-paper-writing/SKILL.md`: cut from about 42 em-dashes to at most 5
- `stat-polishing/SKILL.md`: cut from 3 em-dashes to 0 or 1

Hard rule for next iteration: no em-dashes in any example text, template text, sample abstract, sample paragraph, sample theorem discussion, sample reviewer prompt, or sample output that the model may imitate. Soft rule: remove em-dashes from instructional prose as well.

## Honest open questions

These are points where Codex flagged uncertainty and the next reviewer should resolve them:

1. AOAS AI disclosure policy: Codex found no AOAS-specific generative-AI disclosure instruction on the official pages it checked. This may be incomplete coverage. Confirm with the journal at actual submission time and update the venue block.

2. JASA T&M and JASA ACS guidance is currently sourced from prior knowledge rather than from a 2026 reading of the ASA/Taylor & Francis pages. Refresh these against current sources.

3. JRSS-B, Statistica Sinica, EJS, Bernoulli, COLT, ALT, MSL guidance has not been independently verified against current author guidelines in this iteration. They need a refresh pass.

4. The `Default mapping` for `SUPPLEMENT_MODE` was set based on Codex's reading. Biostatistics, COLT, and ALT are `linked_appendix`; everything else is `separate_self_contained`. Confirm at submission time.

## Codex review log

The full Codex MCP dialogue that produced this roadmap is summarized below. Save the threadId (`019e6aea-0a6e-7dd1-9e8b-341e96e6a86e` for the May 2026 review) for resumability.

### Round 1: top-line verdict

> These skills are useful, not decorative. They are strongest for late-stage methodology and application papers, especially AOAS and JASA ACS, where section weighting, EDA emphasis, findings-first framing, and prose discipline matter a lot. They are also useful for Big Four theory papers once the math and novelty are already settled.
>
> They are not a trustworthy end-to-end submission system in their current form. They do not yet protect the user against the two things that actually kill top-stat submissions: weak positioning and unverified technical overclaim. If used as autopilot, they will produce polished risk.

### Top issues raised in Round 1

1. No mandatory novelty/positioning audit (addressed in this iteration via `PRIOR_WORK_MATRIX.md`).
2. Venue layer is partly wrong and too coarse (AOAS, Biometrika, Biostatistics fixed in this iteration; others in next).
3. Supplement policy is over-absolute and internally inconsistent (addressed via `SUPPLEMENT_MODE`).
4. The family lacks a technical-risk layer (addressed via `TECHNICAL_RISK_REGISTER.md`).
5. The orchestrator is too eager for high-stakes work (`AUTO_PROCEED=true` while `REVIEW_MODE=both`); not yet changed.

### Round 2: actionable specifications

Codex provided exact replacement text for the venue entries, the `SUPPLEMENT_MODE` constant, the canonical Agent invocation syntax, and the schemas for `PRIOR_WORK_MATRIX.md` and `TECHNICAL_RISK_REGISTER.md`. All of these were applied in this iteration.

Codex also noted: "stat-polishing models the intended discipline best. The family as a whole does not." This points to the prose cleanup roadmap item.

Sources Codex checked (May 27, 2026):
- AOAS manuscript submission: https://imstat.org/journals-and-publications/annals-of-applied-statistics/annals-of-applied-statistics-manuscript-submission/
- AOAS supplement instructions: https://imstat.org/journals-and-publications/annals-of-applied-statistics/annals-of-applied-statistics-supplement-instructions/
- AOS manuscript preparation: https://imstat.org/journals-and-publications/annals-of-statistics/annals-of-statistics-manuscript-preparation/
- AOS supplement instructions: https://imstat.org/journals-and-publications/annals-of-statistics/annals-of-statistics-supplement-instructions/
- Biometrika author guidelines: https://academic.oup.com/biomet/pages/General_Instructions
- Biostatistics author guidelines: https://academic.oup.com/biostatistics/pages/general_instructions
- Biostatistics supplementary data page: https://academic.oup.com/biostatistics/pages/supp_data

## Versioning

When applying items from this roadmap, mark them as moved from `Roadmap for next iteration` to `Applied in this iteration`, and rebuild the open-items list for the iteration after.
