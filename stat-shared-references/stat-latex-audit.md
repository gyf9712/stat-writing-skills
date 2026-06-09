# LaTeX Integrity and Template Conformance

Use this reference when interpreting findings from the mechanical LaTeX audit, when the audit cannot reach a definitive verdict, or when a finding requires venue-specific judgment that the script cannot make alone.

## The script does the mechanical work

```bash
python ../stat-shared-references/scripts/latex_audit.py \
  --main main.tex \
  --supplement supplement.tex \
  --supplement-mode separate-self-contained \
  --venue jasa \
  --md-out audit/LATEX_AUDIT_REPORT.md
```

The script is authoritative for these mechanical checks:

| Check | Mechanical? | Where |
|---|---|---|
| Template conformance (documentclass, packages, spacing, geometry, citation policy) | Yes | venue profile in `latex_audit_rules.py` |
| Abstract word count against venue range | Yes | venue profile |
| `\ref` resolves to a `\label` in the same compilation unit | Yes | follows `\input{}` / `\include{}` |
| `\cite` keys match `.bib` entries | Yes | also flags unused entries (bib bloat) |
| BibTeX entry completeness for required fields | Yes | per entry type |
| `\includegraphics` paths exist on disk | Yes | resolves common extensions and the `figures/` convention |
| Cross-file ref leaks (main ↔ supplement under `separate-self-contained`) | Yes | the canonical JASA / AoS / Biometrika / JRSS-B bug class |
| Compile log scan (undefined refs, citations, multiply-defined labels, missing files, overfull boxes) | Yes | parses `main.log` or `logs/main.compile.log` |

The script splits findings explicitly:

- **Mechanical** (`PASS` / `FAIL` / `WARN` / `INFO`): affects exit code.
- **Heuristic** (`CANDIDATE` / `REVIEW`): never affects exit code.

Exit code `0` only when mechanical `FAIL = 0`. Treat `CANDIDATE` findings as review prompts, not verdicts.

This reference does not duplicate the script's check list. To see what the script audits, read `--help` and `latex_audit_rules.py`.

## When to read this file

- A mechanical `FAIL` requires venue-specific interpretation (e.g., the supplement separation rule does not apply at one specific venue).
- The audit returned all `PASS` but you suspect a real LaTeX issue the script does not cover.
- You are setting up a venue profile and need to know what is mechanically checkable versus what should stay in prose.
- You hit a `[VERIFY AT SUBMISSION]` item that the script intentionally does not check.

## What is mechanical and what is judgment

Mechanical, owned by the script:

- Pattern matching (`\documentclass`, spacing commands, package names)
- Cross-checks (`\ref` ↔ `\label`, `\cite` ↔ `.bib`, `\includegraphics` ↔ file system)
- Word counting against fixed venue ranges
- Compile log warning patterns

Judgment, owned by this file and the calling skills:

- Whether a `FAIL` should block submission or is acceptable under a venue-specific waiver
- Whether the right `--supplement-mode` was chosen (`separate-self-contained` vs `linked-appendix`)
- Whether the venue profile in `latex_audit_rules.py` is current (verify against the live IFA page)
- Whether the abstract finding reflects the venue's hard cap or a soft target
- Whether a `WARN` for unused BibTeX entries should be cleaned up or kept (e.g., entries staged for a planned revision)
- Resolving disagreements between the mechanical audit and the venue checklist in `stat-venue-checklists.md`

## A worked example: the cross-file reference bug

This is the most common LaTeX bug in statistics submissions and the one the script catches as finding id `cross_file_ref_supplement_to_main` (or `..._main_to_supplement`). Including the worked example here so the interpretation stays separate from the mechanical check.

**Pattern that fails.** A supplement file with subsection headings like:

```latex
\subsection{Proof of Theorem~\ref{thm:saturation}}
\begin{proof}
By Theorem~\ref{thm:saturation}, ...
\end{proof}
```

where `thm:saturation` is defined in the main paper, not the supplement. When the supplement compiles standalone (the canonical case for JASA, AoS, JRSS-B, Biometrika under `separate-self-contained`), the `\ref` resolves to `??` and the subsection heading reads "Proof of Theorem ??". Reviewers notice on first read.

**Pattern A: textual reference.**

```latex
\subsection{Proof of Theorem~1 (Post-Policy Saturation)}
\begin{proof}
By Theorem 1 of the main paper, ...
\end{proof}
```

The theorem number is written as text. Standalone-compile-clean. The trade-off is that if the main paper's numbering changes during revision, the supplement's textual references must be updated manually.

**Pattern B: restate the theorem.**

```latex
\subsection{Proof of Theorem 1 (Post-Policy Saturation)}
\textit{Theorem 1 (restated from the main paper).} ...full statement...

\begin{proof}
...
\end{proof}
```

The theorem is restated at the start of its proof. The supplement is readable on its own. This is the most reviewer-friendly pattern and is recommended for theorems whose statements are short.

## Severity semantics

The script's severity grades are calibrated to submission risk, not to typographical aesthetic. Use them to decide what blocks versus what can ship as a known minor issue.

| Severity | Meaning | Recommended action |
|---|---|---|
| `CRITICAL` | The paper will not compile or a referenced file is missing | Block submission; fix before any further audit |
| `HIGH` | The paper compiles but a referee will notice on first read (`??` symbols, missing citations, venue non-conformance) | Block submission until cleared |
| `MEDIUM` | The paper compiles cleanly but contains a visible defect a careful referee will note (overfull box, minor venue conformance) | Fix before submission unless the venue policy is genuinely silent on the item |
| `LOW` | Informational or cosmetic (unused bib entry, alternative-form citation that the venue tolerates) | Optional cleanup |
| `REVIEW` | Heuristic finding requiring author judgment | Read each one; treat as a prompt, never as a verdict |

## Venue profile maintenance

Venue profiles live in `latex_audit_rules.py` as Python dicts. To add or refine a profile:

1. Read the venue's current IFA page. Quote the rule you are encoding.
2. Add or edit the dict entry. Keep fields declarative; no functions in the rules module.
3. Bump `RULES_VERSION` (semver) when behavior changes. The audit emits a `rules_digest` automatically; the two together pin provenance.
4. Add or update test fixtures in `tests/fixtures/latex_audit/` so the new rule is exercised at least once.
5. Run `python -m unittest tests.test_latex_audit` to verify the suite still passes.

Do not extract `[VERIFY AT SUBMISSION]` prose from `stat-venue-checklists.md` into the rules module. Config should not pretend unstable policy is deterministic.

## What the script intentionally does not check (v1)

- Real `latexmk` integration (it parses an existing log if present; it does not invoke a TeX runtime).
- Venue profiles beyond JASA (the architecture supports more; v1 ships JASA only as the proof-of-concept).
- Figure-title detection in Python or R source files.
- Alt text presence, AI disclosure block presence, ACC form presence, full page-limit counting.
- Theorem-import correctness (owned by `proof-writer`'s Cited Results Audit).
- Positioning, novelty, comparative-claim accuracy (owned by `stat-positioning-and-claims.md`).

If you need any of these, run the relevant skill's audit separately; do not extend the LaTeX audit's scope.
