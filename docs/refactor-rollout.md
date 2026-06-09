# Skill Refactor Rollout: Deterministic Mechanics → `scripts/`

This document tracks the principled refactor that began with `latex_audit.py`.

## The diagnosis

The repos grew to 8,242 + 10,297 lines across 37 Markdown files. Eight `SKILL.md` files exceeded 800 lines. The failure mode this introduces is not literal forgetting; it is **priority distortion**: the model downweights mid-file checklists, examples and schemas compete with judgment rules, and duplicated rules drift across skills. A 1,400-line skill is a skill that runs its first 200 lines hard and the rest as suggestions.

## The principle

Five buckets, not two. Each piece of content goes to one bucket and only one:

| Bucket | What belongs here |
|---|---|
| `scripts/` | Deterministic mechanics and extraction. Pattern matching, cross-checks, counting, file existence. |
| Machine-readable rule data | Venue profiles, watchword lists, regex catalogs, severity maps. Python modules for structured data; `.txt` for flat lists. Never `.md` as machine source. |
| Candidate generators | Scripts that flag likely problems plus surrounding evidence. They never decide. They feed model or human judgment. |
| `SKILL.md` | Orchestration, hard gates, escalation, interpretation of findings. 250-500 lines single-mode, 500-800 multi-mode, 800 as hard ceiling. |
| References | Judgment detail, examples, edge cases, architecture. Read when a `SKILL.md` step or a script finding needs interpretation. |

The architecture also reserves PASS/FAIL only for truly mechanical checks. Heuristic finders emit `CANDIDATE` / `REVIEW` and never affect exit code. This prevents false authority: once a script exists, both humans and models start treating `PASS` as correctness. Keeping the two finding kinds visually and structurally separate in every output guards against that.

## What landed in v1

**`stat-shared-references/scripts/latex_audit.py`** (~760 lines of Python, stdlib only).

Mechanical checks the script owns:

- Template conformance for the active venue (`--venue jasa` in v1): documentclass option `12pt`, required packages (`natbib`, `setspace`, `geometry`, `amsmath`), spacing required (`\doublespacing`) and forbidden (`\onehalfspacing`, `\singlespacing`), geometry margin `1in`, citation policy (`\citep` / `\citet`; plain `\cite` flagged).
- Abstract word count against the venue range (JASA: 100-250).
- `\ref{}` resolves to a `\label{}` in the same compilation unit; the script follows `\input{}` and `\include{}` to merge sub-files.
- Cross-file leaks under `separate-self-contained` mode: supplement-to-main and main-to-supplement.
- `\cite{}` matches a `.bib` entry; unused entries flagged as `unused_bib_entry` (bib bloat).
- BibTeX entry completeness for required fields per entry type.
- `\includegraphics` paths exist on disk (resolves common extensions and the `figures/` convention).
- Compile-log scan against the regex catalog in `latex_audit_rules.py`: undefined refs and citations, multiply-defined labels, missing files, overfull boxes, missing characters.

**Provenance.** Every report includes `script_version` (semver), `rules_version` (semver, bumped manually when behavior changes), `rules_digest` (sha256 of the rules module, automatic and catches data-only edits).

**Outputs.** JSON is canonical. Markdown is derived. The Markdown report splits findings into four sections: `Mechanical FAIL`, `Mechanical WARN / INFO`, `Mechanical PASS`, `Review Cues (heuristic)`. Top-line summary counts are split by kind, never reported as a single number.

**Exit codes.** `0` no mechanical FAIL. `1` at least one mechanical FAIL. `2` invocation or runtime error. Heuristic findings never affect the exit code.

**Tests.** 20 stdlib unittest cases pass against a synthetic fixture exercising every check.

## What was deleted from prose

`stat-shared-references/stat-latex-audit.md`: shrunk from 315 lines to 135 lines.

Deleted:
- Shell recipes for label/ref cross-checks (replaced by the script).
- The `awk` abstract word-count snippet.
- The raw `grep`-based log audit workflow.
- The "exactly these patterns to flag" lists.

Kept:
- The two-layer concept (template vs integrity).
- Severity semantics calibrated to submission risk.
- The cross-file ref bug worked example (Patterns A and B).
- Venue profile maintenance guidance.

`stat-polishing/SKILL.md`: Steps 14 (Template conformance) and 15 (LaTeX integrity) collapsed into a single Step 14 that calls the script. The abstract word-count shell snippet in former Step 18 was removed because it now lives inside the script. Step 17 (Final venue check) was rewritten to cover only the items the script cannot mechanically verify (cover letter, AI disclosure, ACC form, alt text, AMS subject classification, anonymization).

## Roll-out plan (deferred)

The single-skill proof of concept landing here is intentional. The following extractions are tracked but not yet implemented:

| Extraction | Target | Skills affected | Notes |
|---|---|---|---|
| AI-tell candidate scanner | candidate generator | `stat-polishing`, `stat-style-discipline.md` | Emits `CANDIDATE` only; never affects exit code |
| Negligibility-closure pattern scan | candidate generator | `proofcheck`, `proof-writer` | ctrl-F for `o_p`, `negligible`, `lower-order`, etc.; flags candidates |
| Symbol / acronym inventory | candidate generator | `stat-notation-audit.md` | Lists candidate first-use undefined symbols |
| Artifact-existence gates | gating script | `stat-paper-write`, `stat-polishing` | Checks `CLAIM_SUPPORT_MAP.md`, `PRIOR_WORK_MATRIX.md` exist and are non-empty |
| Theorem / lemma / assumption index | mechanical | `proofcheck` | Builds a unit inventory from `\begin{theorem}` patterns |
| Section / figure / table inventory | mechanical | `stat-paper-write`, `proofcheck` | Counts and lists structural elements |
| Venue profiles beyond JASA | rule data | (none) | AOS, JRSS-B, Biometrika, AOAS, EJS, Bernoulli profiles |

## Maintenance discipline

- Bump `RULES_VERSION` when venue rule logic changes.
- Bump `SCRIPT_VERSION` when audit behavior changes.
- Add or update a fixture under `tests/fixtures/latex_audit/` for any new rule.
- Run `python -m unittest tests.test_latex_audit` before committing changes to either file.
- Never duplicate the script's check list in prose. If a `SKILL.md` step or a reference file ends up re-stating what the script does, drift is back.

## Risk note: false authority

The most important risk of this refactor is that once a script exists, users and models start trusting `PASS` as correctness. The script architecture protects against this with structural splits (`mechanical` vs `heuristic` finding kinds, `PASS/FAIL/WARN/INFO` vs `CANDIDATE/REVIEW` status sets, summary counts always split by kind). Calling skills should preserve those splits when they report findings to the user. A single top-line "0 issues" obscures the heuristic ones; do not collapse the bookkeeping.
