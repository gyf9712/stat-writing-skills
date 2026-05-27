# stat-writing-skills

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
| `stat-polishing` | Polish existing prose to Big Four standards. Positioning audit, technical claim strength audit, then style discipline pass |

## Shared References

Located in `stat-shared-references/`. These are reusable across the four skills.

| File | What it covers |
|---|---|
| `stat-writing-principles.md` | Narrative arc, paper types, abstract formulas, introduction structure |
| `stat-style-discipline.md` | Punctuation discipline (em-dash, colon, semicolon), AI-template removal, COPSS-style scholar voice, paragraph and bullet discipline |
| `stat-figure-design.md` | No titles in figures, caption discipline, legend placement, sizing for journal columns, multi-panel rules |
| `stat-theory-writing.md` | Theorem statement patterns, assumption blocks, proof sketches, rate comparison tables, minimax lower bound arguments |
| `stat-application-writing.md` | Application paper structure (data-first narrative), §2 Data and Background, §6 Application section, validation, domain interpretation |
| `stat-positioning-and-claims.md` | Positioning audit, technical claim strength audit, `CLAIM_SUPPORT_MAP.md` artifact, literature search protocol, common overclaim patterns |
| `stat-venue-checklists.md` | Per-venue formatting, supplement, anonymity, AI disclosure, alt text, reproducibility rules with `Last checked` dates |

## Design Philosophy

Three principles shaped the family.

**Positioning and technical claim strength are the highest-priority risks.** Big Four submissions are killed more often by weak positioning or unverified overclaim than by any other problem. `stat-positioning-and-claims.md` requires every comparative claim in the abstract, introduction, contribution list, theorem statements, and discussion to trace through `CLAIM_SUPPORT_MAP.md` to a verified row of `PRIOR_WORK_MATRIX.md` and `TECHNICAL_RISK_REGISTER.md` with a piece of read-in-full literature support.

**The prose should read like a senior statistician wrote it.** `stat-style-discipline.md` is strict about punctuation (no em-dashes for clause connection, colons restricted to lists and captions, reduced semicolons), AI-template removal (no formulaic openings, empty connectives, watchwords like "delve" or "pivotal", hedge-stacking), and COPSS-style voice (confidence without hype, plain verbs, connective restraint, mathematical precision over praise).

**Figures and tables have one rule above all: no titles inside the figure.** Information moves to the caption. Legends do not overlap data. Captions are self-contained. `stat-figure-design.md` enforces this.

## External Review via Codex MCP

Every skill integrates [Codex MCP](https://github.com/openai/codex) for an independent senior-statistician review at `gpt-5.4` with `model_reasoning_effort: xhigh`. Codex catches positioning and claim-strength issues that Claude polishing misses, because it brings a different model family's judgment.

The default `REVIEW_MODE = both` runs Claude internal review on every round and Codex external review on the final round.

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

Claude Code will pick up the skills automatically. Invoke them with `/stat-paper-plan`, `/stat-paper-write`, `/stat-paper-writing`, or `/stat-polishing`.

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
