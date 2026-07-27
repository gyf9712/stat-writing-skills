# stat-writing-skills

[![tests](https://github.com/gyf9712/stat-writing-skills/actions/workflows/tests.yml/badge.svg)](https://github.com/gyf9712/stat-writing-skills/actions/workflows/tests.yml)

A family of [Claude Code](https://claude.com/claude-code) skills for writing, polishing, and submitting statistics manuscripts to the Big Four statistics journals (JASA, Annals of Statistics, JRSS-B, Biometrika) and similar venues (AOAS, EJS, Bernoulli, Statistica Sinica, Biostatistics, JCGS, JASA ACS), plus ML theory venues (COLT, ALT).

The skills support three paper types with distinct section structure and theory weight:

- **Theory papers** (AoS, Bernoulli, JRSS-B, EJS, COLT, ALT, MSL)
- **Methodology papers** (JASA T&M, JRSS-B, Biometrika, Statistica Sinica)
- **Application papers** (AOAS, JASA ACS, Biostatistics, Statistics in Medicine, JCGS, JABES)

## Skills

| Skill | Purpose |
|---|---|
| `stat-paper-plan` | Build a structured outline from a narrative report or research notes. Produces `PAPER_PLAN.md`, `PRIOR_WORK_MATRIX.md`, `TECHNICAL_RISK_REGISTER.md` |
| `stat-paper-write` | Draft section-by-section LaTeX from the plan. Builds and audits `CLAIM_SUPPORT_MAP.md`. Handles main/supplement separation per venue. |
| `stat-paper-writing` | Full pipeline orchestrator: plan → figures → write → compile → improvement loop with Claude internal + Codex external review |
| `stat-polishing` | Polish existing prose to Big Four standards. Positioning audit, technical claim strength audit, then style discipline pass. Includes page-fit micro-edit and three-reader pre-submission test modes. |
| `stat-mock-review` | Single-pass AE-style pre-submission mock review. Produces `MOCK_REVIEW.md` with synopsis, fatal / major / minor concerns, venue-fit risk, likely initial editorial action (verb, not number), and a prioritized rescue plan. |

## Shared References

Located in `stat-shared-references/`. These are reusable across the four skills.

| File | What it covers |
|---|---|
| `stat-writing-principles.md` | Narrative arc, paper types, abstract formulas, introduction structure |
| `stat-style-discipline.md` | Punctuation discipline (em-dash, colon, semicolon), emphasis-formatting discipline (no bold/italic in prose, venue table), AI-template removal, AI-vocab watchlist, Biometrika-style house bans (note that, is given by, homemade acronyms), COPSS-style scholar voice, paragraph and bullet discipline |
| `stat-figure-design.md` | No titles in figures, caption discipline with sentence-style + per-venue table, statistical-question-driven figure-type selection, Big Four guardrails (no violins without sample support, no broken axes, no dual-y, no inset legends in Biometrika, no 3D, no pie, no splash framework figures), legend placement, sizing for journal columns, multi-panel rules |
| `stat-theory-writing.md` | Theorem statement patterns, assumption blocks, proof sketches, rate comparison tables, minimax lower bound arguments |
| `stat-application-writing.md` | Application paper structure (data-first narrative), §2 Data and Background, §6 Application section, validation, domain interpretation |
| `stat-positioning-and-claims.md` | Positioning audit, technical claim strength audit, `CLAIM_SUPPORT_MAP.md` artifact, literature search protocol, common overclaim patterns |
| `stat-codex-dialogue.md` | Dialogue discipline for Codex MCP reviews: discuss until convergence rather than apply wholesale; when to accept, when to push back, when to log disagreement |
| `stat-latex-audit.md` | Template conformance (documentclass, packages, font, line spacing, margins, bibliography style, venue-required blocks) and LaTeX integrity (undefined refs, undefined citations, missing images, log warnings, cross-file references) |
| `stat-reproducibility-audit.md` | Code, data, simulation reproducibility, and submission statements per Big Four expectations; per-venue table (JASA ACC, JRSS-B data/code policy, Biometrika code supplement, AOAS replication, Biostatistics D/C/R kite-marks); audit checklist and common failure modes |
| `stat-notation-audit.md` | Two-layer audit: every symbol defined on first use, and every acronym either standard or defined. Discipline for new method names (descriptive phrase preferred over homemade acronym, especially at Biometrika); standard statistics acronym list |
| `stat-venue-checklists.md` | Per-venue formatting, supplement, anonymity, AI disclosure, alt text, reproducibility rules with `Last checked` dates |
| `stat-review-routing.md` | Coarse, human-facing map from a review finding to the owner skill, artifact, and first action. Normalizes the first handoff only; `scripts/routing_lint.py` checks that every named skill/artifact exists |

## Deterministic tooling

Mechanical checks live in tested Python (`stat-shared-references/scripts/`, stdlib only)
so the skill bodies stay focused on judgment. Every script separates **mechanical**
findings, which affect the exit code, from **heuristic** ones, which never do. A script
may flag a candidate; it may not certify correctness it cannot actually check — that
guard is what keeps a green run from being mistaken for a verified manuscript.

| Script | Checks | Exit code |
|---|---|---|
| `latex_audit.py` | Template conformance, `\ref`↔`\label`, `\cite`↔`.bib`, image existence, abstract word count, compile-log scan, cross-file reference leaks, duplicate bib keys | 1 on mechanical failure |
| `stat_consistency.py` | GRIM / GRIMMER / statcheck-style numeric consistency of reported statistics | 1 on inconsistency |
| `routing_lint.py` | Every owner skill and artifact named in `stat-review-routing.md` exists (referential integrity only, never routing correctness) | 1 on dangling reference |
| `review_regression.py` | Canonical concerns (`CS#`/`PW#`/`TR#`/theorem labels) raised in a prior `MOCK_REVIEW.md` are still dispositioned in the current one | 1 on a silently dropped concern |

Preprint and non-standard-year citations are emitted as advisory `CANDIDATE` findings:
the script builds the worklist, and `stat-positioning-and-claims.md` owns the actual
verification of every **load-bearing** citation — all of them, not a sample.

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The sibling [`stat-theory-skills`](https://github.com/gyf9712/stat-theory-skills) repo
ships `skill_lint.py`, which checks that every file reference in a `SKILL.md` resolves
in the *installed* layout. Run it against this repo too:

```bash
python ../stat-theory-skills/stat-shared-references/scripts/skill_lint.py \
    --skills-dir . --shared-dir stat-shared-references --install-root ~/.claude/skills
```

## Maintenance

[`MAINTENANCE.md`](MAINTENANCE.md) holds the rules that keep these skills from
re-growing, and the method for testing a rewritten one.

- **Two budgets.** Hot prefix ≤ 200–250 lines (routing, invariants, state machine, hard
  gates, compact contract) and total ≤ 700–800. Length is not a tidiness concern: the
  model runs the first ~200 lines as hard law and treats the rest as suggestions.
- **A `SKILL.md` grows only when the core state machine changes.** Deterministic check →
  script; fixed table → rule data or reference; worked example or prompt block →
  companion reference.
- **Compact empty contract inline, filled specimen out.**
- **Acceptance-testing a rewrite**: prose has no unit tests, so build a fixture per
  route, write an `EXPECT.md`, run the skill in a **fresh context** three times, check
  mechanically, and pass at ≥ 2 of 3 with no forbidden failure.

Current status against the budgets: `stat-mock-review` (194) and `stat-paper-writing`
(584) are inside; `stat-polishing` (819) sits at the edge; `stat-paper-plan` (843) and
`stat-paper-write` (1216) are over and are the next compression targets.

## Design Philosophy

Three principles shaped the family.

**Positioning and technical claim strength are the highest-priority risks.** Big Four submissions are killed more often by weak positioning or unverified overclaim than by any other problem. `stat-positioning-and-claims.md` requires every comparative claim in the abstract, introduction, contribution list, theorem statements, and discussion to trace through `CLAIM_SUPPORT_MAP.md` to a verified row of `PRIOR_WORK_MATRIX.md` and `TECHNICAL_RISK_REGISTER.md` with a piece of read-in-full literature support.

**The prose should read like a senior statistician wrote it.** `stat-style-discipline.md` is strict about punctuation (no em-dashes for clause connection, colons restricted to lists and captions, reduced semicolons), emphasis formatting (no manual bold or italic for rhetorical importance; reserved for journal-conventional objects like theorem class headers and first-use term definitions), AI-template removal (no formulaic openings, empty connectives, watchwords like "delve" or "pivotal", hedge-stacking), Biometrika-style house bans (`Note that`, `is given by`, homemade method acronyms), and COPSS-style voice (confidence without hype, plain verbs, connective restraint, mathematical precision over praise).

**Figures and tables have one rule above all: no titles inside the figure.** Information moves to the caption. Legends do not overlap data. Captions are self-contained. `stat-figure-design.md` enforces this.

## External Review via Codex MCP

Every skill integrates [Codex MCP](https://github.com/openai/codex) for an independent senior-statistician review at `gpt-5.6` with `model_reasoning_effort: xhigh`. Codex catches positioning and claim-strength issues that Claude polishing misses, because it brings a different model family's judgment.

The default `REVIEW_MODE = both` runs Claude internal review on every round and Codex external review on the final round.

**Codex is a dialogue partner, not an oracle.** The skill family treats Codex review as a conversation toward convergence, not a directive to be applied wholesale. For each Codex criticism, the author decides one of three outcomes: accept (apply the fix), push back via `mcp__codex__codex-reply` (provide context Codex lacked), or log disagreement (document both positions). The dialogue typically runs 2 to 4 rounds before convergence or diminishing returns. `stat-shared-references/stat-codex-dialogue.md` codifies the protocol.

This matters in practice: Codex is reliably right on AI-template detection, vague positioning, and missing assumptions, but reliably less accurate on very recent papers, specific theorem numbers, and numerical constants. The author's job is to evaluate each criticism on its merits, not to apply it on authority.

## Pipeline

```
/stat-paper-plan
    builds PAPER_PLAN.md, PRIOR_WORK_MATRIX.md, TECHNICAL_RISK_REGISTER.md
                ↓
/paper-figure
    EDA figures, simulation tables, rate comparison plots
                ↓
/stat-paper-write
    builds CLAIM_SUPPORT_MAP.md, drafts LaTeX section by section,
    handles main/supplement separation per venue,
    runs positioning + claim audit before cross-review
                ↓
/paper-compile
    compiles main paper and supplement as independent PDFs
                ↓
/auto-paper-improvement-loop  (with Codex MCP)
    Round 1 Claude internal review and fix
    Round 2 Codex external review and fix
                ↓
Optional /stat-polishing pass on any section needing more refinement
```

## Installation

These skills are designed for [Claude Code](https://claude.com/claude-code). Place the skill folders under `~/.claude/skills/`:

```bash
git clone https://github.com/gyf9712/stat-writing-skills.git
cp -r stat-writing-skills/stat-* ~/.claude/skills/
cp stat-writing-skills/STAT_SKILLS_ROADMAP.md ~/.claude/skills/
```

Claude Code will pick up the skills automatically. Invoke them with `/stat-paper-plan`, `/stat-paper-write`, `/stat-paper-writing`, `/stat-polishing`, or `/stat-mock-review`.

If you also install the sibling [`stat-theory-skills`](https://github.com/gyf9712/stat-theory-skills) family, both repos share a single `stat-shared-references/` directory at `~/.claude/skills/stat-shared-references/`. The `cp -r` above merges this repo's shared references into that directory; `stat-theory-skills`' `install.sh` merges its own on top. Do not keep the two `stat-shared-references/` directories separate — several writing-side references (`citation-purpose-protocol.md`, `cited-results-lock-protocol.md`, `equivalence-ledger-protocol.md`, `literature-cache-protocol.md`) are owned by `stat-theory-skills` and must resolve under the same relative path for both families.

For Codex MCP integration, the Codex MCP server must be configured in Claude Code:

```bash
claude mcp add codex -s user -- codex mcp-server
```

## Roadmap

`STAT_SKILLS_ROADMAP.md` tracks improvements deferred from the initial Codex review. Highlights for the next iteration:

1. Venue-by-venue compliance refresh with `last_checked` dates and source URLs for all remaining venues
2. New `stat-submission-package` skill for cover letters, disclosures, statements, alt text, citations, inventory
3. PRIOR_WORK_MATRIX and TECHNICAL_RISK_REGISTER as hard gates in writing
4. Reproducibility packaging module
5. Prompt de-duplication across SKILL files
6. PDF-aware review path for figure quality
7. Domain packs (causal, survival, Bayesian, missing data, spatial-temporal, longitudinal, multiple testing, semiparametric)
8. Revision workflow (cover letter, referee response, point-by-point matrix)
9. Automated claim-extraction for `CLAIM_SUPPORT_MAP.md`
10. Skill-level prose cleanup to model the discipline the SKILL files enforce

## Status

The skills are usable for late-stage methodology and application papers. They are strongest for AOAS and JASA ACS, where section weighting, EDA emphasis, findings-first framing, and prose discipline matter most. For Big Four theory papers they are useful once the math and novelty are already settled.

They are not an autonomous submission system. Human sign-off is required on `CLAIM_SUPPORT_MAP.md`, `PRIOR_WORK_MATRIX.md`, and any `CRITICAL` or `HIGH` row of `TECHNICAL_RISK_REGISTER.md` before submission.

## Credits

The skill family was developed with extensive review by Codex MCP (`gpt-5.4` at xhigh reasoning) acting as a senior-statistician Associate Editor. The Codex review log is summarized in `STAT_SKILLS_ROADMAP.md`.

Some methodology was inspired by the Claude Code skill ecosystem (`paper-plan`, `paper-write`, `paper-writing`, `nature-polishing`, `research-review`), adapted and extended for statistics-specific writing conventions.

## License

MIT. See `LICENSE`.
