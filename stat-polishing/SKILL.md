---
name: stat-polishing
description: Polish, restructure, or refine statistics manuscript prose to meet the standards of the Big Four statistics journals (JASA, Annals of Statistics, JRSS-B, Biometrika) plus AOAS, EJS, Bernoulli, Statistica Sinica, Biostatistics, and similar venues. Apply to abstracts, introductions, problem setups, methodology, theory, simulation studies, application sections, discussions, theorem statements, proof sketches, and Chinese-to-English statistics drafts. Optionally invokes Codex MCP (GPT-5.4 at xhigh reasoning) as a senior-statistician second-pass reviewer. Use when the user asks to polish, refine, rewrite, or restructure a statistics manuscript section for publication-quality English at top statistics journals.
version: 1.1.0
author: stat-skills based on stat-writing-principles, stat-style-discipline, stat-figure-design, and curated COPSS-awardee writing patterns
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Statistics-Style Academic Polishing

## Constants

- **CLAUDE_REVIEWER_MODEL = `claude-opus-4-6`** — Internal Claude review (when used as part of a pipeline).
- **CODEX_REVIEWER_MODEL = `gpt-5.4`** — External LLM via Codex MCP for the senior-statistician second-pass review, at `model_reasoning_effort: xhigh`.
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
- Avoid em-dashes for sentence connection. Prefer commas, periods, or restructuring. The em-dash is the strongest AI-tell in academic prose.
- Reduce colon use. Keep colons only for introducing lists or figure/table captions.
- Reduce semicolon use. Convert most to periods.
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
| `../shared-references/citation-discipline.md` | Auditing citations, fabricated references, citation key consistency |
| `../stat-shared-references/stat-codex-dialogue.md` | **Read before any Codex MCP call.** Dialogue discipline: when to accept, when to push back via `mcp__codex__codex-reply`, when to log disagreement, common areas where Codex is right or wrong, convergence test, documentation expectations. |

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
8. Punctuation discipline (em-dashes, colons, semicolons)
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

## Sentence and paragraph control

### Sentence rules

- Aim for sentences in the 10 to 30 word range
- Keep every sentence at no more than 30 words
- If a sentence exceeds 20 words, check whether it contains more than one main proposition
- Split overloaded sentences rather than polishing them cosmetically
- The last sentence of a paragraph often becomes the longest and weakest. Check it explicitly.
- Prefer one core subject-verb proposition per sentence
- Do not use em-dashes as sentence-connecting punctuation. Use commas, periods, or parentheses instead.
- Use colons only to introduce lists or in figure/table captions.
- Convert most semicolons to periods.

### Paragraph rules

- Statistics paragraphs are typically 4 to 8 sentences
- Each paragraph should develop one main idea
- Move from old information to new information
- End on the point that matters most
- Vary paragraph openings; not every paragraph needs an explicit topic sentence
- Avoid one-sentence paragraphs except in rare emphatic contexts
- Avoid stacked connectives ("Moreover, ...", "Furthermore, ...", "Additionally, ...")

### Bullet point rules

- Bullets only in: contribution lists in §1, assumption lists, algorithm pseudocode, simulation-setup item lists
- Convert other bullets to prose
- For contribution lists: use a numbered list (1, 2, 3) of 2 to 4 items
- Each contribution should be 1 to 3 lines, specific and falsifiable

### Results vs Discussion sentence types

Results sentences usually report:
- "was estimated"
- "increased by"
- "showed"
- "achieved"
- "the coverage rate was"

Discussion sentences usually interpret:
- "suggests that"
- "is consistent with"
- "may reflect"
- "could indicate"
- "is likely due to"

Do not let a Results paragraph drift into Discussion syntax unless the transition is intentional.

## Punctuation discipline (priority)

Read `../stat-shared-references/stat-style-discipline.md` for full guidance. The headline rules:

1. **Em-dashes**: cut to at most one per paper. Replace with commas, periods, or restructured sentences.
2. **Colons**: keep only those introducing lists, figure captions, or table captions. Cut stylistic colons that connect clauses.
3. **Semicolons**: convert most to periods. Keep only for joining two short, closely related parallel clauses.

## AI-template removal (priority)

Cut the following on sight.

Section openings:
- "In this section, we ..."
- "This section is organized as follows."
- "Here, we present ..."
- "We now turn to ..."

Empty connectives:
- "It is worth noting that"
- "Importantly,"
- "Notably,"
- "Crucially,"
- "Interestingly,"
- "Of particular note,"

Watchwords:
- delve, pivotal, landscape, tapestry, underscore, elucidate, noteworthy, intriguingly, leveraging, holistic, robust (when no robustness tested), novel (when no novelty established), comprehensive (when nothing comprehensive)

Padding phrases:
- "perform an analysis of" → "analyze"
- "make use of" → "use"
- "in order to" → "to"
- "due to the fact that" → "because"
- "at this point in time" → "now"
- "the question of whether" → "whether"

Hedge stacking:
- "may potentially suggest" → "suggests"
- "could possibly indicate" → "indicates"

Generic conclusions:
- "opens exciting new avenues"
- "wide-ranging implications"
- "we hope this work will inspire"

The rule-of-three tic: vary list lengths. Single items, pairs, and quadruples are fine. Cut items that do not pull weight.

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
2. **Identify paper type and venue.** Apply the corresponding standards.
3. **Positioning audit.** Read `../stat-shared-references/stat-positioning-and-claims.md`. Extract every positioning claim from the prose, especially the abstract, introduction, contribution list, related work, and discussion. For each claim, verify it against `PRIOR_WORK_MATRIX.md` (if available) and against the literature. Flag OVERCLAIMED, UNVERIFIED, MISSING REFERENCE FRAME claims. Run a literature search for unverified claims using `/semantic-scholar`, `/arxiv`, `/novelty-check`, or `mcp__codex__codex`. Update or build `CLAIM_SUPPORT_MAP.md`.
4. **Technical claim strength audit.** Same reference. Extract every technical claim (rates, bounds, "weaker assumptions", "first to", "minimax optimal", "efficient", "tight", "robust", "adaptive", computational complexity). Verify each against the theorem statements and the cited prior work. Flag the same statuses. For each OVERCLAIMED claim, draft a specific replacement sentence rather than leaving a TODO.
5. **Diagnose at the paper level.** Are claims and evidence aligned? Is the supplement separated correctly per `SUPPLEMENT_MODE`?
6. **Diagnose at the section level.** Is each section doing its job?
7. **Polish at the paragraph level.** Does each paragraph develop one idea?
8. **Polish at the sentence level.** Apply punctuation discipline and AI-template removal.
9. **Polish at the word level.** Cut watchwords; replace with precise alternatives or remove.
10. **Audit figures and tables.** Apply the figure design rules.
11. **Audit citations.** Verify that no fabricated citations exist; verify cited claims match cited papers.
12. **Final venue check.** Read the venue checklist; confirm format conformance.
13. **Optional Codex second-pass.** Invoke external senior-statistician review via Codex MCP (see next section). The Codex pass should include an independent positioning and claim strength audit, even when the polisher has already run one. Disagreements between the two audits signal genuine ambiguity worth surfacing to the author.

## Optional Codex MCP second-pass dialogue

When `CODEX_PASS` is `optional` or `mandatory`, or whenever the polished text is destined for a Big Four submission, run an external senior-statistician dialogue via Codex MCP. The polisher's job is to produce text that *passes* this review; Codex provides the test.

This second-pass is independent of Claude. It frequently catches AI-shaped patterns that Claude polishing misses, since Claude and the polished text share a common authorial fingerprint.

**The dialogue principle.** Codex's review is one senior reader's opinion, not a directive. The job of the second-pass is to discuss with Codex until both sides converge on what the prose needs, not to apply Codex's feedback wholesale. Read `../stat-shared-references/stat-codex-dialogue.md` before starting.

### Step 11.1: Send polished text to Codex

```yaml
mcp__codex__codex:
  model: gpt-5.4
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

    (C) Line-level AI-tell audit.

    Count and quote (with line numbers when available):
    - em-dashes used to connect clauses
    - colons outside lists and captions
    - excessive semicolons
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
- **Do not invent**. Polishing improves prose, not content. Flag content concerns; do not paper over them.
- **Punctuation discipline is non-negotiable**. Em-dashes cut, colons restricted, semicolons reduced.
- **AI templates and watchwords must be removed**.
- **COPSS-style voice**: confident, plain, precise, measured.
- **Main and supplement independence must be preserved**. Flag broken cross-file references as CRITICAL.
- **Figure no-title rule**: every figure should move titles to captions during polishing.
- **Big Four standards apply** to JASA, AoS, JRSS-B, Biometrika. Similar standards apply (with venue-specific adjustments) to AOAS, EJS, Bernoulli, Statistica Sinica, Biostatistics, JCGS.
- **The polished paper should read like a senior statistician wrote it**, not like an enthusiastic but vague summary.
