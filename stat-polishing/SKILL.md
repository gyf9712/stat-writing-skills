---
name: stat-polishing
description: Polish, restructure, or refine statistics manuscript prose to meet the standards of the Big Four statistics journals (JASA, Annals of Statistics, JRSS-B, Biometrika) plus AOAS, EJS, Bernoulli, Statistica Sinica, Biostatistics, and similar venues. Apply to abstracts, introductions, problem setups, methodology, theory, simulation studies, application sections, discussions, theorem statements, proof sketches, and Chinese-to-English statistics drafts. Optionally invokes Codex MCP (GPT-5.6 at xhigh reasoning) as a senior-statistician second-pass reviewer. Use when the user asks to polish, refine, rewrite, or restructure a statistics manuscript section for publication-quality English at top statistics journals.
version: 1.1.0
author: stat-skills based on stat-writing-principles, stat-style-discipline, stat-figure-design, and curated COPSS-awardee writing patterns
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Statistics-Style Academic Polishing

## Constants

- **CLAUDE_REVIEWER_MODEL = `claude-opus-4-6`** — Internal Claude review (when used as part of a pipeline).
- **CODEX_REVIEWER_MODEL = `gpt-5.6`** — External LLM via Codex MCP for the senior-statistician second-pass review, at `model_reasoning_effort: xhigh`.
- **CODEX_PASS = `optional`** — Options: `off` (Claude polishing only), `optional` (offer Codex second-pass and ask user), `mandatory` (always invoke Codex). For high-stakes journal submissions, default is `optional`; for routine polishing, `off` is appropriate.

Use this skill to improve statistics writing at three levels.

- Paper-level: paper-type recognition, hourglass structure, claim-evidence alignment, supplement separation
- Section-level: section job, paragraph logic, argument flow
- Sentence-level: punctuation discipline, AI-template removal, COPSS-style scholar voice

The skill is designed for the Big Four and similar statistics venues. It is not a Nature-style polisher and is not an ML conference polisher. The conventions, voice, and structural expectations are specific to statistics.

## Default stance

- Language serves argument. Do not polish sentences while leaving the reasoning broken.
- Write for the statistical reader: precise, measured, evidence-anchored.
- Do not invent results, theorems, citations, simulations, or claims.
- Do not let the polisher draft the paper's core scientific argument from scratch. If the argument is weak or unclear, expose the weakness rather than hiding it under polished language.
- Body-prose em-dashes: at most one per paper. Prefer commas, periods, or restructuring.
- Body-prose colons: prohibited except before a list, in a figure/table label, or in math and code. Split every other colon into two sentences.
- Body-prose semicolons: prohibited except in bibliographic citation clusters and in commas-within-items lists. Split every other semicolon into two sentences.
- Body-prose parentheses: prohibited except for citations, equation numbers, assumption/step labels, standard acronym first-use, and short mathematical annotations. Restructure or cut every other parenthetical.
- Manual bold and italic in body prose: prohibited except italics on the first defined use of a technical term and venue-mandated bold for vectors and matrices. Cut every other case.
- Reduce paragraph fragmentation. Statistics paragraphs are longer than ML conference paragraphs.
- Reduce bullet point use. Bullets belong in contribution lists, assumption lists, algorithm pseudocode, and simulation-setup item lists. Otherwise use prose.

## When to open extra files

These files are reference support. Open them after the section's rhetorical job is clear.

| File | Open when |
|---|---|
| `../stat-shared-references/stat-positioning-and-claims.md` | **Read first on every polishing pass that touches the abstract, introduction, contribution list, theorem statements, related work, or discussion.** Covers the positioning audit, the technical claim strength audit, the `CLAIM_SUPPORT_MAP.md` artifact, and literature search protocol. This is the primary defense against the two most common Big Four rejection drivers: weak positioning and overclaim. Polishing prose without running this audit produces polished overclaim. |
| `../stat-shared-references/stat-style-discipline.md` | Sentence-level polishing, AI-template removal, COPSS-style scholar voice, punctuation discipline. Read after the positioning and claim audit. |
| `../stat-shared-references/stat-writing-principles.md` | Paper-level framing, paper type identification, narrative arc, abstract structure |
| `../stat-shared-references/stat-theory-writing.md` | Polishing theorem statements, assumption blocks, proof sketches, rate comparison tables |
| `../stat-shared-references/stat-application-writing.md` | Polishing application papers, especially Data and Background section, EDA, application section |
| `../stat-shared-references/stat-figure-design.md` | Auditing figures and tables, caption discipline, legend placement |
| `../stat-shared-references/stat-venue-checklists.md` | Final-pass venue conformance check |
| `../stat-shared-references/stat-codex-dialogue.md` | **Read before any Codex MCP call.** Dialogue discipline: when to accept, when to push back via `mcp__codex__codex-reply`, when to log disagreement, common areas where Codex is right or wrong, convergence test, documentation expectations. |
| `../stat-shared-references/stat-latex-audit.md` | **Read before the mechanical audit pass.** Template conformance check (documentclass, packages, font, line spacing, margins, bibliography style, venue-required blocks, anonymization) and LaTeX integrity check (undefined references, undefined citations, missing image files, broken cross-file references, log warnings). |
| `../stat-shared-references/stat-reproducibility-audit.md` | Read before final submission. Big Four expectations on data and code availability, reproducible simulations, venue-specific reproducibility artifacts (JASA ACC, Biostatistics D/C/R, AOAS replication code, Biometrika supplementary code). Includes the three submission statements (data availability, code availability, reproducibility). |
| `../stat-shared-references/stat-notation-audit.md` | Read before final compile. Two-layer audit: every symbol defined on first use, every acronym either standard or defined. Discipline against homemade method acronyms, especially for Biometrika. Also the cross-reference drift audit for the formal-statement pass. |
| `../stat-shared-references/equivalence-ledger-protocol.md` | **Read before the formal-statement pass.** Governs equivalence-preserving formalization of assumptions, definitions, theorem/lemma statements: the standing refusal condition (never formalize to look deeper), the precision-vs-decoration discriminator, the use-test, venue-register calibration, the two-tier gate (cosmetic cluster vs semantic per-atomic-claim), the equivalence ledger schema, and the proofcheck depth split. Lives in the sibling `stat-theory-skills` repo (shares the silent-semantic-change ontology). |

## Big Four Standards

The Big Four statistics journals (JASA, Annals of Statistics, JRSS-B, Biometrika) share core expectations:

1. **Precision before elegance.** Every claim is precise enough to be checked; elegance follows from clarity.
2. **Mathematical rigor.** Theorems are stated with all assumptions; proof sketches are in the main body; full proofs in the supplement; notation is consistent.
3. **Honest scope.** What the paper does not show is named explicitly; assumptions are discussed, not just stated.
4. **Substantive contribution.** A result that is technically novel but practically uninteresting is hard to publish; a result that is practically interesting but technically vague is also hard to publish.
5. **Measured voice.** No hype, no inflation. Achievements are stated in technical terms.
6. **Reproducibility.** Methods sections are detailed enough for replication; data and code availability are addressed.
7. **Independent supplement.** Main and supplement are independent PDFs; the supplement is self-contained.

When polishing, evaluate the prose against these standards. Polishing is not just sentence smoothing; it is alignment with the venue's expectations.

## Core architecture

### 1. Identify the paper type first

Before editing, determine what kind of paper or section this is.

- `Theory paper`: primary contribution is a new theoretical result (rate, bound, characterization). Polishing emphasizes precision of theorem statements, assumption discussion, proof sketch quality, rate comparison tables.
- `Methodology paper`: primary contribution is a new method with theoretical backing. Polishing balances method description, theoretical properties, simulation rigor, real data analysis.
- `Application paper`: primary contribution is solving a real scientific problem. Polishing emphasizes data description, EDA, statistical challenge motivation, application section depth, substantive findings, validation, practical recommendations.

A theory-paper polish applied to an application paper will produce a paper that is technically precise but unreadable for the application audience. An application-paper polish applied to a theory paper will produce a paper that reads as informal. Match the polish to the type.

### 2. Use the hourglass structure

Strong statistics papers mirror an hourglass.

- `Introduction`: open broadly with the problem, narrow to the specific gap, state the contribution.
- `Body`: develop the contribution with method, theory, simulation, application.
- `Discussion`: widen again, connecting findings back to the literature, stating limitations and open questions.

If a paragraph or section violates this architecture, rebuild it before polishing wording.

### 3. Reader workflow

Statistics reviewers typically read in this order.

1. Abstract: do I care about this problem?
2. Introduction: is the contribution clear and positioned correctly?
3. Main results: are the theorems clean and strong?
4. Assumptions: are they standard or restrictive?
5. Simulations: do they verify what the theory predicts?
6. Proofs (supplement): is the analysis correct?

Polishing should help the paper answer these questions in this order. The most polishing effort goes to the abstract, introduction, theorem statements, and assumption discussion.

### 4. Protect the core argument

The paper's core argument includes:

- the statistical question or problem the paper actually addresses
- the contribution: what is proven, proposed, or discovered
- the evidence: theorems, simulations, real data
- the boundary: conditions under which the result holds and where it does not

The polisher may improve wording, structure, transitions, and clarity. The polisher must not invent results, fabricate citations, alter the meaning of theorems, or change the boundary of claims.

### 5. Diagnose failure modes before editing

Before rewriting, identify the main problems. Prioritize in this order.

1. Wrong paper type framing (e.g., theory framing for an application paper)
2. Missing or unstated assumptions used in a theorem
3. Claim without evidence; evidence without a clear claim
4. Cross-reference broken between main and supplement
5. Section-level structure problems (Methodology mixed with Theory; Discussion mixed with Results)
6. Paragraph-level argument problems (one paragraph carrying two ideas)
7. Sentence-level AI-template patterns
8. Punctuation and emphasis discipline (em-dashes, colons, semicolons, prose parentheticals, rhetorical bold and italic)
9. Word-level watchwords (delve, pivotal, noteworthy)

The earlier in this list a problem appears, the more important it is to fix first. Polishing sentence punctuation while a theorem is missing an assumption is a misallocation of effort.

## Section responsibilities

### Abstract

A polished statistics abstract:

- States the specific problem in the first sentence
- States the contribution in plain language with at least one quantitative result
- Is self-contained (no undefined notation, no citations, no acronyms that are not standard)
- Ends with the boundary or implication, not a generic platitude
- For theory papers: 5 to 6 sentences (problem, gap, main result, approach, verification, implication)
- For methodology papers: 5 to 6 sentences (motivation, limitation of current methods, proposed method, theory, empirics, impact)
- For application papers: 5 to 7 sentences leading with the scientific question and naming the substantive finding

A polished abstract avoids:
- Generic openings ("Statistical inference has attracted increasing attention...")
- Vague phrases ("we propose a novel method")
- Hype words ("groundbreaking", "remarkable", "comprehensive")
- Acronyms not defined or not standard

### Introduction

A polished statistics introduction:

- States the problem with specificity, citing its origin in the literature
- Frames the gap as a specific technical question, not as a field-wide vague need
- Reviews prior work organized by approach or assumption class, not paper-by-paper
- States the contribution in plain language, then in formal terms
- Lists 2 to 4 contributions in a numbered list when warranted; otherwise in prose
- Previews the strongest result early
- Ends with a brief paper organization paragraph

A polished introduction avoids:
- Templated openings ("Recent advances in X have led to Y")
- Bibliography dumps without synthesis
- Five-or-more contribution bullets (suggests unfocused paper)
- Forward references to undefined notation

### Problem Setup / Model / Assumptions

A polished setup section:

- Defines the statistical model formally and cleanly
- Introduces notation in one place, then uses it consistently
- States assumptions with labels ((A1), (A2), ...) before they are used
- Discusses each assumption: is it standard, novel, weaker, stronger; when might it fail
- Compares the assumption set with prior work

A polished setup avoids:
- Long meandering definitions that mix notation with motivation
- Assumptions stated after the theorem (or worse, embedded inside the theorem statement)
- "Under mild conditions" without enumerating
- Notation that drifts across sections

### Main Results

A polished main results section:

- States each theorem cleanly with `\begin{theorem}` and proper assumptions in the preamble
- Follows each theorem with 1 to 2 paragraphs of interpretation: what the rate means, how it compares, when it is tight
- Includes a rate comparison table when the contribution is a rate (theory papers)
- Provides proof sketches in the main body that give genuine insight into the technical novelty
- Uses corollaries for important special cases
- Uses remarks for extensions, optimality discussion, and connections

A polished results section avoids:
- Theorems stated without preamble assumptions
- "By standard arguments" hiding non-standard steps
- Proof sketches that say "see supplement" without telling the reader what the supplement does
- Tables comparing rates without explaining what differs

### Simulation Studies

A polished simulation section:

- States the design first: DGPs, sample sizes, replications, metrics, comparison methods
- Reports results as observations, then interprets
- Includes standard errors with every metric
- Includes log-log rate verification plots for theory papers
- Honest when the proposed method does not dominate

For application papers, the DGPs must be informed by the real data; the polisher should verify this is explicit.

### Application / Real Data Analysis (application papers)

A polished application section:

- Restates the scientific question at the start
- Describes the analytic pipeline
- Reports estimates with uncertainty
- Includes 3 to 6 high-quality figures with self-contained captions
- Compares with methods used by domain practitioners
- Includes validation: holdout, cross-validation, sensitivity
- Provides substantive interpretation that connects to the domain literature
- Is the longest section in the paper for application papers (4 to 6 pages typically)

### Discussion

A polished statistics discussion:

- Summarizes the substantive contribution (rephrased, not copied from intro)
- States honest limitations as limitations, not buried in hedges
- Identifies specific open problems with technical content
- For application papers: includes practical recommendations for practitioners
- Avoids generic future-work platitudes
- Avoids bullet-pointing the implications

### Title

A polished statistics title:

- Tells the reader what the paper does
- Combines the statistical method, the setting, and (when applicable) the application
- Avoids slogans, grant-style aims, and field-wide overclaims
- Is searchable: contains terms a reviewer would search for

## Sentence, paragraph, bullet, and punctuation discipline (priority)

Read `../stat-shared-references/stat-style-discipline.md` for the full rules. Headline items, in priority order.

1. Em-dashes. At most one per paper. Replace others with commas, periods, or restructured sentences.
2. Colons. Prohibited in body prose. Permitted only before a list, in a figure/table label, or in math and code. Split every other colon into two sentences.
3. Semicolons. Prohibited in body prose. Permitted only in bibliographic clusters and commas-within-items lists. Split every other semicolon into two sentences.
4. Parentheses. Prohibited in body prose. Permitted only for citations, equation numbers, assumption/step labels, standard acronym first-use, and short mathematical annotations. Restructure or cut every other parenthetical.
5. Manual bold and italic. Prohibited in body prose. Permitted only for italics on first-defined technical term and venue-mandated bold for vectors and matrices. Cut every other case, including bold on contribution items, "key findings," and theorem claim sentences.
6. Sentence length. 10 to 30 words. Check any sentence over 20 words for multiple propositions.
7. Paragraph length. 4 to 8 sentences. One idea per paragraph. Old-info to new-info movement. End on the load-bearing point.
8. Bullets. Only in contribution lists, assumption lists, algorithm pseudocode, and simulation setups. Convert other bullets to prose.
9. Results vs Discussion register. Results sentences report, as in "was estimated", "increased by", "showed". Discussion sentences interpret, as in "suggests that", "is consistent with", "may reflect". Do not let a Results paragraph drift into Discussion syntax unless the transition is intentional.

## AI-template removal (priority)

Read `../stat-shared-references/stat-style-discipline.md` "AI-Template Patterns to Avoid" + "AI Watchwords (Watchlist, Not Blacklist)" + "Biometrika-Style House Bans" for the full lists. Cut on sight:

- Templated section openings ("In this section, we ...", "Here, we present ...")
- Empty connectives ("It is worth noting that", "Importantly,", "Notably,", "Crucially,")
- AI watchwords (delve / pivotal / underscore / unveil / leveraging / etc.) used as decoration
- Biometrika-style hard bans ("Note that" at sentence start; "is given by"; homemade method acronyms; in-text `w.r.t.` / `s.t.` / `i.f.f.`)
- Hyphenated noun-adjectives ("kernel-based", "model-driven", "simulation-based", stacked premodifiers) — unpack to a preposition or verb unless the term is standard; unpack on sight when two or more stack before one noun
- Padding phrases ("in order to" → "to"; "perform an analysis of" → "analyze")
- Hedge stacking ("may potentially" → "suggests")
- Generic conclusions ("opens exciting new avenues", "wide-ranging implications")
- Rule-of-three tic when all three items are not pulling weight

## COPSS-style scholar voice

Senior statisticians who publish regularly in the Big Four write with characteristic patterns. Modeling these helps reduce AI-shaped prose.

- Confident claims supported by precise evidence, not by adjectives
- Plain, active verbs ("we propose", "we prove", "we show")
- Connective restraint (prefer "but" over "however"; prefer "thus" over "consequently")
- Mathematical precision over adjectival praise
- Modesty with specificity (name what was not done, with technical content)
- Sentence rhythm variation (mix short declaratives with longer developmental sentences)
- Reference restraint in math (cite the predecessor whose result you are improving, the technique you are using; do not cite five papers for one concept)

For detail, read `../stat-shared-references/stat-style-discipline.md`, especially the COPSS-Style Scholar Writing Patterns section.

## Main and supplement separation

For most statistics journals (JASA, AoS, JRSS-B, Biometrika, AOAS), main and supplement are independent PDFs. The polisher should check:

- The supplement does not depend on `\ref` to labels in the main paper
- Theorems proved in the supplement are restated at the start of the proof
- Notation used in the supplement is either redefined or imported via `math_commands.tex`
- Cross-references between files are textual ("Section S.2 of the Supplement", "Theorem 1 of the main paper") not LaTeX cross-refs

If the polisher finds broken cross-file references, flag them as CRITICAL issues.

## Chinese-to-English mode

When the source is Chinese or strongly Chinese-influenced English:

- Extract the core propositions first
- Do not translate clause-by-clause mechanically
- Reconstruct explicit logical links: contrast, cause, implication, limitation
- Verify terminology, causality, hedging
- Keep key statistical terms stable across sections
- Apply the same punctuation discipline and AI-template removal

Common Chinese-to-English issues in statistics drafts:
- Overuse of passive voice
- Long sentences chaining multiple propositions
- "It can be seen that ..." patterns that should be cut
- Mismatched verb tenses across sections
- Inconsistent notation between sections written at different times

## Citation, ethics, and AI boundaries

### Intellectual debt

Acknowledge contributions of prior work openly. The polisher should not minimize others' contributions to make the polished paper seem more original.

### Position attribution clearly

The polisher should ensure that:
- How the paper builds on prior work is explicit
- Who was responsible for earlier ideas is named
- Citations match what the cited paper actually says

### Cite the source you actually read

- Cite paper A for A's own results
- Cite paper B for B's commentary or improvement on A
- Avoid leaning on secondary sources when the source can be cited directly

### What needs citation

- Others' ideas, data, methods, wording, structure, distinctive interpretations

### AI boundary

`Green` (acceptable for the polisher to do):
- Improve grammar, clarity, concision, tone
- Reorganize paragraphs and sentences
- Suggest alternative phrasings
- Audit punctuation, watchwords, AI templates
- Audit figure captions for self-containment
- Audit theorem statements for precision
- Translate from Chinese with terminology checks

`Yellow` (the polisher should flag for the author):
- Mathematical results that need verification
- Citations that need verification
- Substantive claims that may need revision
- Cross-file references that may break

`Red` (the polisher must not do):
- Invent results, theorems, lemmas
- Fabricate citations
- Alter the meaning of theorems
- Change the boundary of claims
- Insert claims the author did not make

## Output format

Default output:

1. The polished text as plain prose, not in a code block.
2. `Revision notes:` with 3 to 6 short bullets on the major structural and stylistic changes.
3. If the rewrite changed section logic, say so explicitly.
4. If issues require author attention (Yellow items), list them under `Author check needed:`.

If the user asks for side-by-side revision, provide:

- `Original`
- `Polished`
- `Why changed`

If the user asks for an audit without rewriting:

- List issues by severity (CRITICAL / MAJOR / MINOR)
- Group by location (section, paragraph)
- Recommend specific changes

## Workflow for polishing a manuscript

The order matters. Polishing prose on top of an overclaim makes the overclaim more confidently stated; polishing prose on top of a weak positioning hides the weakness rather than fixing it. The audits come first.

1. **Read the document end-to-end first.** Do not polish sentence-by-sentence on a first pass.
2. **Identify paper type, venue, and journal voice.** Apply the corresponding standards from `stat-venue-checklists.md`. Then calibrate to the target journal's voice by reading 2 or 3 recent papers from that venue (last 1-2 years, same paper type). Note their paragraph length, sentence rhythm, math display density, theorem density, figure density, citation density, and tone. The polished prose should feel at home alongside those papers. A draft that reads like a Bernoulli theory paper will not pass at JASA ACS, and vice versa.
3. **Positioning audit.** Read `../stat-shared-references/stat-positioning-and-claims.md`. Extract every positioning claim from the prose, especially the abstract, introduction, contribution list, related work, and discussion. For each claim, verify it against `PRIOR_WORK_MATRIX.md` (if available) and against the literature. Flag OVERCLAIMED, UNVERIFIED, MISSING REFERENCE FRAME claims. Run a literature search for unverified claims using `/semantic-scholar`, `/arxiv`, `/novelty-check`, or `mcp__codex__codex`. Update or build `CLAIM_SUPPORT_MAP.md`.
4. **Technical claim strength audit.** Same reference. Extract every technical claim (rates, bounds, "weaker assumptions", "first to", "minimax optimal", "efficient", "tight", "robust", "adaptive", computational complexity). Verify each against the theorem statements and the cited prior work. Flag the same statuses. For each OVERCLAIMED claim, draft a specific replacement sentence rather than leaving a TODO.
5. **Story spine audit.** Write a one-sentence spine for the paper or section in the form: "We study [problem], address the gap that [gap], contribute [contribution], support it with [evidence], under [boundary]." Then audit whether that spine stays visible throughout the manuscript. The goal is not verbal repetition. The goal is stable problem-gap-contribution-evidence-boundary alignment across the paper.

    Checks:
    - **Matching test.** Check that the abstract, the introduction's contribution paragraph, the first interpretation of the main result, and the opening of the discussion all instantiate the same spine, with differences in emphasis allowed but no drift in the actual contribution or boundary.
    - **Section classification.** Classify each major section after the introduction as primarily `claim`, `evidence`, or `scaffold`. If a long section is only scaffold, or if the claim-bearing sections are hard to locate, flag that the story is buried.
    - **Contribution traceability.** Check that each advertised contribution is tied to a specific theorem, method section, simulation result, figure, table, or application finding. If a contribution cannot be traced to supporting material, flag it.
    - **Decisive-evidence placement.** Check that the paper reveals decisive evidence early enough for its type: the first main theorem early in a theory paper, the first decisive result table or figure early in a methodology or application paper, and the substantive finding early in an application paper. Flag when the reader must wait too long to see what carries the paper.
    - **Unadvertised-claim test.** Flag claims that appear in the discussion, conclusion, or late-section interpretation but were not visible in the abstract or introduction, unless they are explicitly marked as secondary observations rather than central contributions.

6. **Mathematical expression economy audit.** Audit theorem statements, displayed mathematics, definitions, and surrounding explanatory prose for local cognitive load. This is a soft-flag audit, not a hard-threshold audit. The goal is not to enforce a house notion of elegance, but to catch avoidable compression, fragmentation, and symbol overload that make correct mathematics harder to read.

    Soft flags:
    - **Object before symbol.** Flag sentences or displays that introduce notation before naming the mathematical object, quantity, map, or event the symbol denotes.
    - **Dormant symbol introduction.** Flag symbols that are introduced and then not used again until much later, or that appear only once. Delay or remove them unless they are needed immediately.
    - **Local notation load.** Flag theorem statements, definition blocks, or paragraphs that introduce too many fresh objects at once, bury the main conclusion under qualifiers, or force the reader to hold several new symbols before the claim is visible.
    - **Display purpose clarity.** Flag displayed equations that mix multiple jobs at once. Each major display should have a clear role, such as definition, assumption, decomposition, update rule, or main claim. Long or multi-line displays are acceptable when the structure is visually clear; flag only when the display should be split, aligned differently, or partly converted to prose.
    - **Theorem packaging.** Flag theorems whose assumptions, quantifiers, regimes, or special cases are scattered across the statement instead of being packaged cleanly in an assumption block, theorem preamble, or short remark.
    - **Interpretive handoff.** Flag definitions, lemmas, and theorems that are left without a brief prose handoff telling the reader what the mathematical object or result buys them, how it should be read, or why it matters for the paper's contribution.

7. **REVISION_PLAN.md gate (author approval required before applying changes).** Before applying any nontrivial edits, write `REVISION_PLAN.md` and obtain author approval. Approval is cluster-level by default, not line-level. Do not apply a cluster until its status is `APPROVED`.

    Clustering rules:
    - Each cluster contains a tightly related set of changes, typically 5 to 25 individual edits.
    - A cluster may be organized by one issue type within one section, or by one cross-section consistency issue that must be changed together.
    - Use a cross-section cluster only when the edits are logically coupled (e.g., abstract + introduction + discussion alignment).
    - The governing rule: one rationale, one expected effect, one accept/reject decision.
    - If partial acceptance within a cluster is likely, split before submitting for approval.

    Schema (see also section "REVISION_PLAN.md schema" below for the full template):

    ```md
    # REVISION_PLAN

    ## Approval Rule
    No manuscript edits are applied until the author approves one or more clusters below.
    Approval is cluster-level by default. If the author requests partial acceptance inside a cluster, mark that cluster `SPLIT_REQUESTED`, re-cluster it, and resubmit it for approval.

    ## Cluster 1: [short action-oriented header]
    - Scope: [section(s), theorem(s), figure(s), bib entries, or files affected]
    - Severity: [CRITICAL | MAJOR | MINOR]
    - Expected effect on the paper: [1-2 sentences on what improves and what risk is addressed]
    - Proposed changes:
      1. [specific proposed change]
      2. [specific proposed change]
    - Approval status: [PENDING | APPROVED | REJECTED | SPLIT_REQUESTED | APPLIED]
    - Application notes: [dependencies, ordering constraints, "must apply with Cluster N"]
    ```

8. **Diagnose at the paper level.** Are claims and evidence aligned? Is the supplement separated correctly per `SUPPLEMENT_MODE`?
9. **Diagnose at the section level.** Is each section doing its job?
10. **Polish at the paragraph level.** Does each paragraph develop one idea?
11. **Polish at the sentence level.** Apply punctuation discipline and AI-template removal.
12. **Polish at the word level.** Cut watchwords; replace with precise alternatives or remove.
13. **Audit figures and tables.** Apply the figure design rules in `../stat-shared-references/stat-figure-design.md`.
14. **Mechanical LaTeX audit (script).** Run `latex_audit.py` for template conformance, ref/label cross-check, cite/bib cross-check, image-file existence, cross-file leaks under the active `SUPPLEMENT_MODE`, abstract word count against the venue range, and compile-log scan.

    ```bash
    python ../stat-shared-references/scripts/latex_audit.py \
      --main main.tex \
      --supplement supplement.tex \
      --supplement-mode separate-self-contained \
      --venue jasa \
      --md-out audit/LATEX_AUDIT_REPORT.md
    ```

    The script is authoritative for mechanical checks (`PASS` / `FAIL` / `WARN` / `INFO`). Every `FAIL` is a hard gate — polishing is not complete until they are zero. `WARN` findings should be cleared unless the venue's live IFA page has an explicit waiver. `CANDIDATE` findings (heuristic) are review prompts, never verdicts; they never affect the exit code.

    Read `../stat-shared-references/stat-latex-audit.md` for interpretation, severity semantics, the cross-file ref bug worked example, and venue-profile maintenance guidance. Do not duplicate the script's check list in prose; if a finding is unclear, consult the file.

    Exit code `0` = no mechanical FAIL. Exit code `1` = at least one mechanical FAIL. Exit code `2` = invocation error. The audit's report file `audit/LATEX_AUDIT_REPORT.md` includes provenance (`script_version`, `rules_version`, `rules_digest`) for traceability.
15. **Citation identity and bibliography hygiene audit.** This is the polishing-time citation audit; the checks below are self-contained. It does **not** replace the literature-relative novelty and comparative-claim audit in `../stat-shared-references/stat-positioning-and-claims.md`, the theorem-import checks in `proof-writer`'s `## Cited Results Audit`, or the undefined-citation and template checks in the script run in Step 14.

    Checks:
    - **Canonical version discipline.** For works that exist as both preprint and published versions, choose the canonical version deliberately and use it consistently unless there is a clear reason to cite both.
    - **Citation identity consistency.** Check that the same work is not represented under multiple keys, multiple year variants, or mixed preprint/published identities, and that author names and years are consistent across prose and bibliography.
    - **Metadata sufficiency and cleanliness.** Check that cited entries contain enough metadata to identify the source unambiguously and look submission-ready: authors, year, title, venue or journal, and pages / volume / DOI / arXiv information when available and appropriate.
    - **Surface citation discipline.** Check author-year surface form, `\citet{}` / `\citep{}` usage where the venue requires it, `et al.` usage, author-name spelling in prose, and local citation punctuation and grouping.
    - **Direct-source and restraint discipline.** Prefer citing the direct source of a theorem, method, or empirical claim when that source is available, and flag citation clusters that look padded rather than informative, especially in theorem interpretation and related-work synthesis.

    **Not in scope**: this step does not decide novelty, adjudicate whether a comparative claim is true in the literature, verify that an imported theorem justifies a proof step, or repair compile-level citation failures.

16. **Journal-style match check.** Compare the polished prose against the 2-3 recent venue papers identified in Step 2. Does the polished draft match their voice, density, and structural choices? If not, identify the specific deltas (e.g., "this introduction is much longer than typical Biometrika introductions; consider compressing"). For JASA, JRSS-B, AOS, AOAS, this check is usually done by Codex in the optional second-pass; for first-pass polishing, a quick comparison by the polisher is sufficient.
17. **Final venue check.** Read `stat-venue-checklists.md` for the target venue and confirm every venue-specific requirement Step 14 cannot mechanically verify:
    - **Cover letter** is ready (separate file or portal text box per the venue)
    - **AI disclosure** block is present in the manuscript
    - **Data and code availability statements** are present
    - **Reproducibility artifacts** for JASA: the Author Contributions Checklist (ACC) form is filled in and uploaded as supplementary material
    - **Alt text** under each figure for Biometrika and Biostatistics (preceded by `Alt text:`)
    - **AMS subject classification** for IMS venues (AOS, AOAS, EJS, Bernoulli)
    - **Author anonymization** matches the venue's peer-review setting

    Abstract word count, template conformance, and citation/ref/label/image cross-checks are already covered by Step 14's mechanical audit; if the script's exit code is `0` and there are no `WARN` findings outstanding, those items have passed.

18. **Optional Codex second-pass.** Invoke external senior-statistician review via Codex MCP (see next section). The Codex pass should include an independent positioning and claim strength audit, a story-spine assessment, a journal-style-match assessment against the venue, and an AI-tell line-level audit. Disagreements between the two audits signal genuine ambiguity worth surfacing to the author.

## Optional Codex MCP second-pass dialogue

When `CODEX_PASS` is `optional` or `mandatory`, or whenever the polished text is destined for a Big Four submission, run an external senior-statistician dialogue via Codex MCP. The polisher's job is to produce text that *passes* this review; Codex provides the test.

This second-pass is independent of Claude. It frequently catches AI-shaped patterns that Claude polishing misses, since Claude and the polished text share a common authorial fingerprint.

**The dialogue principle.** Codex's review is one senior reader's opinion, not a directive. The job of the second-pass is to discuss with Codex until both sides converge on what the prose needs, not to apply Codex's feedback wholesale. Read `../stat-shared-references/stat-codex-dialogue.md` before starting.

### Step 11.1: Send polished text to Codex

```yaml
mcp__codex__codex:
  model: gpt-5.6
  sandbox: read-only
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a senior statistician serving as Associate Editor for
    [JASA / AoS / JRSS-B / Biometrika / AOAS / etc.].

    Below is a polished section/manuscript draft. Audit it on three
    levels in order:
    (A) positioning and technical claim strength,
    (B) Big Four standards and voice,
    (C) line-level AI-tell discipline.

    Paper type: [theory / methodology / application]
    Target venue: [VENUE]
    Section(s): [abstract / intro / setup / results / method / sims /
                 application / discussion / full draft]

    Polished text:
    [paste polished text]

    Supporting artifacts (paste if available):
    - PRIOR_WORK_MATRIX.md
    - TECHNICAL_RISK_REGISTER.md
    - CLAIM_SUPPORT_MAP.md

    (A) Positioning and technical claim strength audit.

    For each positioning claim in the prose (sentences placing the
    paper relative to literature):
    - Is the closest existing work cited?
    - Is the delta stated correctly?
    - Are there obvious recent papers (last 2-3 years) that may be
      missing?
    - For any "first to" or "only" claim, is it plausibly true given
      the literature you know?
    Flag specific quoted sentences as SUPPORTED, OVERCLAIMED,
    UNVERIFIED, or MISSING REFERENCE FRAME.

    For each technical claim (rates, bounds, comparative assumptions,
    efficiency, complexity, "minimax optimal", "tight", "robust",
    "adaptive"):
    - Is the claim consistent with the theorem the paper proves?
    - For comparative claims, is the comparison correct against the
      named prior work?
    - Is the technical notion specified and applied correctly?
    Flag specific quoted sentences.

    For each OVERCLAIMED or UNVERIFIED claim, write a concrete
    proposed replacement sentence that the author can paste in. The
    replacement must keep the contribution visible while bringing it
    within what the evidence and the literature support.

    Suggest specific papers (with full citations and your confidence
    level) that the author may have missed. Distinguish "definitely
    should be cited" from "worth checking".

    Score: positioning strength (1-10), claim strength (1-10), and
    name the binding constraint.

    (B) Big Four standards and voice.

    - Precision before elegance
    - Mathematical rigor (assumptions before theorems, proof sketches
      with insight)
    - Honest scope (boundary stated)
    - Substantive contribution
    - Measured voice
    - Reproducibility addressed
    - Main-supplement independence respected (per the venue's
      SUPPLEMENT_MODE)

    For each of the top three remaining issues here, write a concrete
    revision.

    (C) Journal-style match.

    The author identified [VENUE] as the target. From your knowledge of
    recent papers published there (last 1-2 years, same paper type),
    assess whether the polished prose matches the venue's voice and
    structural conventions:
    - Paragraph length, sentence rhythm
    - Math display vs inline density
    - Theorem density and statement style
    - Figure density and caption style
    - Citation density
    - Use of section headings and subsections
    - Tone (measured / dense / elegant / data-first)

    For each significant mismatch, name a specific recent paper from
    the venue that the polished draft should resemble more closely,
    and identify the specific delta. If you are uncertain about a
    recent paper, mark your confidence.

    (D) Template conformance.

    From the LaTeX preamble and front matter included below, identify
    any obvious deviation from the venue's required template:
    - `\documentclass` and class options
    - Required packages (line spacing, geometry, font)
    - Bibliography style file
    - Venue-required blocks (keywords, AMS classification, alt text,
      AI disclosure)
    - Author / anonymization block

    [paste preamble + first 50 lines]

    (E) LaTeX integrity (summary).

    From the manuscript and the compile log excerpt below, identify
    undefined references, undefined citations, missing image files,
    and broken cross-file references. List with file:line and the fix.

    [paste compile log warnings or note that no log was provided]

    (F) Line-level AI-tell audit.

    Count and quote (with line numbers when available):
    - em-dashes used to connect clauses
    - body-prose colons outside lists, figure/table labels, math, and code
    - body-prose semicolons outside bibliographic clusters and commas-within-items lists
    - body-prose parentheticals outside the citation, equation-number, label, acronym-first-use, and short-math-annotation cases
    - manual bold or italic outside first-defined technical term and venue-mandated math bold
    - formulaic openings ("In this section, we ...", "Here, we ...")
    - empty connectives ("It is worth noting that", "Importantly,",
      "Notably,", "Crucially,", "Interestingly,")
    - watchwords (delve, pivotal, landscape, underscore, noteworthy,
      leveraging, holistic, robust as decoration, novel as
      decoration, comprehensive as decoration)
    - hedge-stacking ("may potentially", "could possibly")
    - rule-of-three tics
    - one-sentence paragraphs in non-emphatic positions
    - bullets outside contribution lists, assumption lists,
      algorithm pseudocode, simulation setups
    - generic closing platitudes

    COPSS-style scholar voice score: 1 (heavy AI fingerprint) to 10
    (indistinguishable from a senior statistician's prose).

    Do not soften. Senior statisticians prefer direct feedback.
    The job of this audit is to surface what a critical reviewer
    would notice on first read.
```

### Step 11.2: Run the dialogue with Codex

For each issue Codex raises, decide one of three per `../stat-shared-references/stat-codex-dialogue.md`:

- **Accept**: the criticism is clearly correct and the fix is unambiguous. Apply it.
- **Push back**: the criticism is wrong, partial, or based on a misunderstanding. Use `mcp__codex__codex-reply` with the `threadId` to provide the context Codex lacked, then re-decide. Example: "On issue N: I disagree because [the cited paper actually states X, not Y]. Please reconsider; if you still think the issue stands, identify what specifically remains wrong."
- **Log disagreement**: after a round or two without convergence, document both positions in `POLISHING_REVIEW.md` and move on.

Special cases:
- If the fix requires altering the meaning of a claim, flag for author attention rather than applying.
- If Codex proposes a replacement sentence, read it before pasting; Codex is good at structure but can introduce technical inaccuracies.
- If Codex cites a specific paper, theorem number, or numerical constant, verify it; LLMs are confident even when wrong on these.

### Step 11.3: Optional second iteration

For abstracts and introductions especially, consider one follow-up round:

```
mcp__codex__codex-reply:
  threadId: [from Step 11.1]
  prompt: |
    Here is the revised version after applying your feedback.

    [paste revised text]

    Two questions:
    1. Have the issues you flagged been resolved?
    2. What is the score now on the COPSS-style scale, and what is
       the single next change that would raise it most?
```

### Step 11.4: Document the dialogue

Stop iterating when both sides converge, or when remaining disagreements are documented with the author's reasoning, or when the dialogue reaches diminishing returns (typically 2 to 4 rounds). Do not iterate indefinitely.

Save to `POLISHING_REVIEW.md` in the project root, in the format from `../stat-shared-references/stat-codex-dialogue.md`:
- `threadId` for resumability
- Initial Codex review verbatim
- Round-by-round summary of pushback and Codex's replies
- Final list of accepted criticisms with applied fixes
- Final list of rejected criticisms with the author's reasoning
- Initial voice verdict and COPSS-style score
- Final voice verdict and COPSS-style score
- AI-tell audit counts before and after
- Outstanding disagreements between Claude polishing and Codex review

### Mode: Page-Fit Micro-Edit

When the manuscript is over the venue's page limit by a small amount (one to three pages), or when a single section needs to be trimmed to fit a column-balanced layout, run a page-fit micro-edit pass rather than restructuring.

Big Four page caps that commonly trigger this pass:

- JASA T&M: 35 pages, double-spaced, 12 pt
- JASA ACS: 35 pages, double-spaced, 12 pt
- AoS: 30 pages double-spaced
- Biometrika main paper: 25 pages typeset (Miscellanea: 8 pages)
- JRSS-B: no hard cap but length is screened editorially; papers over 30 typeset pages face headwinds
- AOAS: typically 20-25 pages

The pass is local, reversible compression or expansion with a target word or page delta. Apply paragraph by paragraph.

What to preserve:

- Assumptions, quantifiers, caveats, and theorem conditions verbatim
- Every cited paper and bibliographic reference
- Numerical values, rates, and constants in theorems and tables
- The strength of every claim (do not weaken `we prove` to `we show`; do not weaken `minimax optimal` to `near-optimal`)
- Notation introduced earlier and used later

What to cut first:

- Meta-discourse ("In this section, we ...", "As discussed above, ...", "We now turn to ...")
- Duplicated signposting ("This result, which we prove in Section 4, ...")
- Soft intensifiers ("very", "quite", "rather", "particularly", "especially" used as decoration)
- Hedge stacking ("may potentially", "could possibly")
- Derivations that belong in the supplement (a four-line algebraic manipulation in the body that the reader will skip)
- Restatements of definitions already given
- Bullet items that repeat the surrounding prose

What to expand only when needed:

- An assumption that the reader cannot follow without an extra sentence
- A theorem statement whose contribution is unclear from the formal claim alone
- A figure caption whose takeaway is not stated

After the pass, recompute the page count. Do not loop endlessly: if two passes have removed less than half a page each, the manuscript is at its natural length and the cut must come from structure, not from prose.

### Mode: Three-Reader Pre-Submission Test

Run this pass after the line-level polish is complete and before the Codex external pass, or as a final standalone read before submission. The goal is to find the first point where each of three intended readers stops trusting or following the paper.

Simulate three readers in sequence. For each reader, read the manuscript end-to-end and stop at the first point of friction.

**Reader 1: the Associate Editor.** They are screening the paper in fifteen minutes for desk-reject or send-out-for-review. They ask: "Why should statisticians care?" Mark the first place where the answer is not on the page. Likely failure modes:

- Abstract that does not state the contribution in the first two sentences
- Introduction that frames the problem too narrowly or too vaguely for the venue
- Contribution list whose items are not distinguishable from prior work
- Theorem statement that requires reading the assumption block to understand the claim
- Application section that does not name the substantive scientific finding

**Reader 2: the technical referee.** They are reading the math carefully and ask: "Is this correct and useful?" Mark the first place where the math, the proof sketch, or the simulation does not support the prose claim. Likely failure modes:

- Theorem that uses an assumption introduced two pages later
- Proof sketch that says "by standard arguments" for a step that is the technical novelty
- Simulation design that does not match the assumption set in the theorem (e.g., heavy-tailed errors claimed in theory, Gaussian errors in simulation)
- Rate in the abstract that does not match the rate in the theorem
- Citation that does not say what the paper claims it says

**Reader 3: the applied statistician.** For methodology and application papers, they ask: "Could I use this on my data?" Mark the first place where the method becomes inaccessible. Likely failure modes:

- Method introduced before the problem it solves is motivated by data
- Tuning parameter without a recommendation or default
- Implementation not described or not pointed at
- Simulation evidence that does not cover the data regime the reader works in
- Validation that does not include a comparison with the method the domain currently uses

For each reader, record the first-friction location, the diagnosis, and the smallest change that would clear the friction. Fix in order of severity, not in order of reader; an AE-level friction blocks all three readers.

Do not try to satisfy all three readers in the same paragraph. The introduction belongs to the AE; the main results to the referee; the application section to the applied statistician. Each reader gets a section where their needs dominate.

### Mode: Formal-Statement Pass

A polishing pass that targets only the mathematical FORM in the body: assumptions, definitions, theorem and lemma statements, and displayed conditions. It rewrites each into a more formal, more conventional, equivalence-preserving form aligned with how the target venue's published papers state such objects. Invoke when the math is settled and the author wants the statements to read at the venue's register.

This mode is governed by `../stat-shared-references/equivalence-ledger-protocol.md` (in the sibling `stat-theory-skills` repo, which owns the silent-semantic-change ontology this mode reuses). Read it before running this pass. The mode is **as much a refusal engine as a formalization engine**; its standing refusal condition is:

> Never formalize to increase apparent depth. Apparent depth is only ever a side effect of a genuine precision-or-register gain. The moment a rewrite raises the reading barrier without resolving a referee-checkable ambiguity, matching the venue's register, or removing notation clutter, refuse it.

The math-form analog of this skill's prose rule "mathematical precision over adjectival praise" is **"precision over notational sophistication."**

Operational summary (full protocol in `equivalence-ledger-protocol.md`):

1. For each candidate object, draft the formalized form, then apply the discriminator: does it resolve a referee-checkable ambiguity (with respect to what limit? uniform over which class? in which norm? what probability mode? what conditioning?), match the venue register, or remove clutter? If none, it is decoration; withdraw it.
2. Apply the **use-test**: every introduced symbol, space, operator, topology, or process must be used downstream in a theorem, proof, rate, or assumption cross-reference. A symbol introduced only to restate an elementary scalar/vector condition is withdrawn.
3. Apply the **simpler-equivalent challenge**: if a simpler conventional statement is equally falsifiable, choose it.
4. Apply the **venue-register exemplar check**: would this object look normal in two recent accepted or similar papers from the target venue, and does it reduce or increase the modal reader's burden? Biometrika and JASA prefer compact assumptions with verbal interpretation; AoS, Bernoulli, EJS allow native technical objects when used downstream. Calibrate against the 2-3 recent venue papers identified in Step 2 of the workflow.
5. Classify each rewrite. **Cosmetic / packaging** rewrites (formatting, labeling, ordering, environment cleanup) go through the normal `REVISION_PLAN.md` cluster gate. **Semantic** rewrites — any rewrite touching quantifier, probability mode, uniformity, constants, asymptotic regime, conditioning set, norm or topology, dependence structure, or parameter space — get a **per-atomic-claim gate** (one atomic claim, one approval, never clustered) with an `EQUIVALENCE_LEDGER.md` row attached. A six-part assumption produces up to six approval items.
6. For each semantic rewrite, fill the ledger row, including the honest "possible silent strengthening / weakening" column and the downstream consumers.
7. Apply the **proofcheck depth split**: a semantic rewrite not on the main dependency chain gets a targeted dependency check (does any downstream unit consume the changed property?); a rewrite on the path to a headline theorem, rate theorem, or main-chain lemma gets a full `/proofcheck --post-repair` on the affected sub-DAG. Unclear dependency status is treated as load-bearing.
8. Run the **cross-reference drift audit** (reuse `../stat-shared-references/stat-notation-audit.md`): after rewriting any labeled object, audit every later prose and proof reference to it ("the boundedness condition", "Assumption 3(ii)") and update or flag.
9. Run the Step 6 Mathematical Expression Economy self-check on the output; any formalization that trips an economy flag without a precision gain is withdrawn.

This mode never silently changes a statement's meaning. A formalization that strengthens or weakens an assumption, even by adding a single quantifier or pinning a single constant, is a semantic rewrite and is gated and ledgered as one. A formalization that cannot be justified as equivalent (or as a documented intended correction) is not applied by this mode; it is flagged for the author and, if it affects a proof, routed to `/proof-repair`.

### When to skip the Codex pass

- Quick local edits to a single paragraph
- Polishing of internal notes or memos not destined for journal submission
- When the user explicitly says `polish only` or `do not call codex`
- When Codex MCP is not available in the environment

## Key Rules

- **Large file handling**: If Write fails due to size, use Bash to write in chunks.
- **Match the polish to the paper type**. Theory polishing emphasizes theorem and assumption precision. Methodology polishing balances method and empirics. Application polishing emphasizes data description, application depth, and substantive findings.
- **Positioning and claim audit before style**. Every polishing pass that touches the abstract, introduction, contribution list, theorem statements, or discussion must run the positioning audit and the technical claim strength audit first. Polishing prose on top of an overclaim makes the overclaim more confidently stated; polishing prose on top of a weak positioning hides the weakness. Read `../stat-shared-references/stat-positioning-and-claims.md`.
- **Literature support for every comparative claim**. Comparative claims ("weaker assumptions than", "first to", "improves the rate from") require verified literature support. If the support is not in `PRIOR_WORK_MATRIX.md` or `CLAIM_SUPPORT_MAP.md`, search for it before polishing.
- **Template conformance is non-negotiable**. Read `../stat-shared-references/stat-latex-audit.md`. The `\documentclass`, packages, line spacing, margins, font, and `.bst` must match the venue requirement before polishing is declared complete. JASA requires double-spaced manuscript; Biometrika and Biostatistics require alt text under each figure legend; IMS journals use the `imsart` class with the right option.
- **LaTeX integrity is non-negotiable**. The manuscript must compile cleanly with no undefined references, no undefined citations, no missing image files, and no fatal log warnings. For `SUPPLEMENT_MODE = separate_self_contained`, the supplement and main paper must each compile independently with no cross-file `\ref` or `\cite`.
- **Journal-style match**. The polished prose should feel at home alongside 2-3 recent papers from the target venue. The polisher (and Codex) calibrate to those papers, not to a generic "statistics paper" voice.
- **Do not invent**. Polishing improves prose, not content. Flag content concerns; do not paper over them.
- **Punctuation and emphasis discipline is non-negotiable**. Em-dashes cut to at most one. Body-prose colons, semicolons, and parentheticals prohibited except for the whitelisted uses. Manual bold and italic prohibited except for first-defined technical term and venue-required math bold.
- **AI templates and watchwords must be removed**.
- **COPSS-style voice**: confident, plain, precise, measured.
- **Main and supplement independence must be preserved**. Flag broken cross-file references as CRITICAL.
- **Figure no-title rule**: every figure should move titles to captions during polishing.
- **Big Four standards apply** to JASA, AoS, JRSS-B, Biometrika. Similar standards apply (with venue-specific adjustments) to AOAS, EJS, Bernoulli, Statistica Sinica, Biostatistics, JCGS.
- **The polished paper should read like a senior statistician wrote it**, not like an enthusiastic but vague summary.
