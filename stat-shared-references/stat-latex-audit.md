# LaTeX Integrity and Template Conformance Audit

Use this reference whenever a stat skill compiles or polishes a LaTeX manuscript. It covers two related but distinct checks.

1. **Template conformance**: the manuscript uses the venue's required document class, packages, font, line spacing, margins, and bibliography style.
2. **LaTeX integrity**: no undefined references, no broken citations, no missing image files, no fatal warnings in the compile log.

Both are mechanical. Both are cheap. Both are non-optional for any manuscript headed to submission.

## When to Read

- Before any compile in `stat-paper-write` Step 4 (Bibliography) and Step 8 (Final Checks)
- During the polishing pass in `stat-polishing` for any manuscript with a working LaTeX source
- Before submission, as part of the final venue conformance check

## Template Conformance Audit

### Goal

Verify the manuscript matches the venue's required LaTeX template at the level of document class, packages, font, spacing, margins, and bibliography style.

### Step T.1: Identify the venue template requirement

From `stat-venue-checklists.md`, look up the target venue. Note:

- The required `\documentclass` and any required class options
- The required `.bst` (bibliography style) file
- Required packages (e.g., IMS journals use `imsart`, IEEE uses `IEEEtran`)
- Required font (often Times Roman for JASA, default for IMS)
- Required line spacing (JASA: double-spaced)
- Required margins (typically 1 inch for JASA, venue-specific for others)
- Whether anonymized author block is required at first submission

### Step T.2: Compare the manuscript preamble

Open `main.tex` and check:

- `\documentclass{...}` matches the venue requirement
- All required packages are loaded
- No conflicting packages are loaded (e.g., loading `natbib` while the venue uses `cite`)
- `\bibliographystyle{...}` matches the venue's `.bst`
- Line spacing is set correctly (e.g., `\usepackage[doublespacing]{setspace}` for JASA)
- Margins are set correctly (e.g., `\usepackage[margin=1in]{geometry}` for JASA)
- Font is correct (e.g., `\usepackage{times}` for JASA)

For IMS venues specifically:
- `\documentclass[aoas|aos|bj|ejs]{imsart}` with the right option per venue
- The IMS class manages line spacing, margins, and font internally; do not override

For IEEE venues:
- `\documentclass[journal|conference]{IEEEtran}` with the right option
- Use `\cite{}` (`cite` package), not `\citet`/`\citep` (natbib)

For Biometrika, Biostatistics, and other Oxford journals:
- First submission is typically format-neutral; exact style is required only at acceptance

### Step T.3: Check for venue-required blocks

Some venues require specific blocks in the preamble or front matter:

- **IEEE**: `\begin{IEEEkeywords} ... \end{IEEEkeywords}` after the abstract
- **JASA**: keywords, AMS subject classification
- **AOS / AOAS / EJS / Bernoulli (IMS)**: AMS subject classification, keywords block via `\begin{keyword}` / `\kwd{...}` in `imsart`
- **Biometrika**: keywords; alt text under each figure legend prefaced by `Alt text:`
- **Biostatistics**: keywords; alt text under each figure legend prefaced by `Alt text:`

Check that any block the venue requires is present.

### Step T.4: Check author / anonymization block

For first submission at venues that use double-anonymized review, the author block should be anonymized; self-citations should be re-phrased; acknowledgments should be removed. For venues that use single-anonymized or open review, the full author block is included.

For JASA, AOS, AOAS, Biometrika, Biostatistics, JRSS-B, EJS, Bernoulli, Statistica Sinica: the current peer-review setting should be verified on the live submission portal. `stat-venue-checklists.md` records what was last known.

For COLT and ALT: anonymized submission is required.

### Step T.5: Report findings

Produce a `TEMPLATE_CONFORMANCE_REPORT.md` (or include in the polishing review log) with:

- Venue and template requirement
- Each conformance check: PASS / FAIL / NEEDS VERIFY
- Specific fixes for each FAIL (the exact LaTeX line to change)
- Items flagged NEEDS VERIFY for the user

## LaTeX Integrity Audit

### Goal

Verify the manuscript compiles cleanly and contains no undefined references, broken citations, missing image files, or fatal warnings.

### Step L.1: Compile and capture the log

Compile twice (or use `latexmk`) so cross-references resolve:

```bash
latexmk -pdf -interaction=nonstopmode main.tex 2>&1 | tee main.compile.log
```

If `latexmk` is not available, compile manually twice:

```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Both the captured compile output and `main.log` should be searched for issues.

### Step L.2: Audit the log for known warnings

Search the log (`main.log` and the captured compile output) for these patterns:

| Pattern | What it means | Severity |
|---|---|---|
| `LaTeX Warning: There were undefined references.` | At least one `\ref` or `\cite` did not resolve | HIGH |
| `LaTeX Warning: Reference 'xxx' on page yyy undefined` | Specific `\ref{xxx}` or `\eqref{xxx}` has no matching `\label{xxx}` | HIGH |
| `LaTeX Warning: Citation 'xxx' on page yyy undefined` | Specific `\cite{xxx}` has no `.bib` entry | HIGH |
| `LaTeX Warning: There were multiply-defined labels.` | Same `\label{...}` used twice | HIGH |
| `LaTeX Warning: Label 'xxx' multiply defined.` | Specific duplicate label | HIGH |
| `Package natbib Warning: Citation 'xxx' undefined` | natbib-specific citation miss | HIGH |
| `! LaTeX Error: File 'xxx' not found.` | Missing image, included file, or class | CRITICAL |
| `Missing character: There is no ...` | Glyph missing in current font, often a Unicode or math symbol issue | MEDIUM |
| `Overfull \hbox` (>10pt) | Content exceeds the margin; usually a long URL, formula, or word | MEDIUM |
| `Underfull \hbox` | Loose horizontal spacing; usually cosmetic | LOW |
| `Underfull \vbox` | Loose vertical spacing; usually cosmetic | LOW |
| `LaTeX Warning: ...font shape ... undefined, using ...` | Missing font shape, fallback used | MEDIUM |
| `Package hyperref Warning: Token not allowed in a PDF string` | Math or special character in section title or caption | LOW-MEDIUM |
| `pdfTeX warning: ... destination ... has been referenced but does not exist` | Internal hyperlink target missing | MEDIUM |

A clean compile shows none of the HIGH or CRITICAL patterns. All HIGH and CRITICAL findings must be fixed before submission. MEDIUM findings should be fixed where straightforward.

### Step L.3: Cross-check `\ref` and `\label`

For each `\ref{key}`, `\eqref{key}`, `\autoref{key}`, `\cref{key}`, `\Cref{key}` in the source, verify a matching `\label{key}` exists. Conversely, list orphan `\label{...}` that are defined but never referenced; these are usually harmless but can indicate a forgotten section reference.

Quick command pattern (search the source tree):

```bash
# All labels defined
grep -rEn '\\label\{[^}]+\}' . | sed -E 's/.*\\label\{([^}]+)\}.*/\1/' | sort -u > labels.txt

# All references used
grep -rEn '\\(eq|auto|c|C)?ref\{[^}]+\}' . | sed -E 's/.*\\(eq|auto|c|C)?ref\{([^}]+)\}.*/\2/' | sort -u > refs.txt

# References without labels (UNDEFINED — must fix)
comm -23 refs.txt labels.txt

# Labels without references (orphan — usually OK, sometimes a forgotten ref)
comm -13 refs.txt labels.txt
```

### Step L.4: Cross-check `\cite` and the .bib file

For each `\cite{key}`, `\citep{key}`, `\citet{key}` in the source, verify a matching entry exists in the `.bib` file.

```bash
# All citation keys used (handle comma-separated lists)
grep -rEn '\\cite[tp]?\{[^}]+\}' . \
  | sed -E 's/.*\\cite[tp]?\{([^}]+)\}.*/\1/' \
  | tr ',' '\n' \
  | sed 's/^ *//; s/ *$//' \
  | sort -u > cites.txt

# All bib entry keys
grep -EnH '^@[a-zA-Z]+\{[^,]+,' *.bib \
  | sed -E 's/.*@[a-zA-Z]+\{([^,]+),.*/\1/' \
  | sort -u > bibkeys.txt

# Citations without entries (UNDEFINED — must fix)
comm -23 cites.txt bibkeys.txt

# Entries without citations (bib bloat — should be removed for clean bib)
comm -13 cites.txt bibkeys.txt
```

### Step L.5: Cross-check `\includegraphics` and image files

For each `\includegraphics[...]{path}` in the source, verify the file exists at that path with a valid extension (`.pdf`, `.png`, `.jpg`, `.eps`).

```bash
grep -rEn '\\includegraphics\[?[^]]*\]?\{[^}]+\}' . \
  | sed -E 's/.*\\includegraphics\[?[^]]*\]?\{([^}]+)\}.*/\1/' \
  | sort -u > images.txt

# For each path, check existence (with common extensions)
while read -r img; do
  if [ -z "$img" ]; then continue; fi
  found=""
  for ext in "" ".pdf" ".png" ".jpg" ".jpeg" ".eps"; do
    if [ -f "$img$ext" ] || [ -f "figures/$img$ext" ]; then
      found="1"; break
    fi
  done
  if [ -z "$found" ]; then echo "MISSING: $img"; fi
done < images.txt
```

### Step L.6: Audit cross-file references (supplement)

If `SUPPLEMENT_MODE = separate_self_contained` (default for JASA, AoS, AOAS, etc.), the supplement must not reference labels defined in the main paper, and the main paper must not reference labels defined in the supplement.

For each file, run the label/ref audit independently, treating the main paper and the supplement as separate compilation units. Any `\ref{}` that resolves only by reading both files at once is a broken cross-file reference and must be replaced with a textual reference (e.g., "Section S.2 of the Supplement").

**A worked example of the bug.** A common pattern in supplement files looks like this:

```latex
% supplementary_proofs.tex
\documentclass[12pt]{article}
% ... preamble ...
\renewcommand{\thetheorem}{S\arabic{theorem}}

\section{Proofs of Main Results}

\subsection{Proof of Theorem~\ref{thm:saturation}}     % <-- BUG
\begin{proof}
By Theorem~\ref{thm:saturation}, ...                    % <-- BUG
...
\end{proof}

\subsection{Proof of Corollary~\ref{cor:prepolicy}}     % <-- BUG
```

The labels `thm:saturation` and `cor:prepolicy` are defined in the main paper, not in the supplement. When the supplement compiles standalone, every `\ref{thm:saturation}` and `\ref{cor:prepolicy}` becomes `??`. The submitted PDF then shows "Proof of Theorem ??" in subsection headings, which a reviewer notices immediately.

Two correct patterns:

**Pattern A: textual reference (simple, robust).**
```latex
\subsection{Proof of Theorem~1 (Post-Policy Saturation)}
\begin{proof}
By Theorem 1 of the main paper, ...
...
\end{proof}
```
The theorem number is written as text. The supplement compiles standalone with no missing references. The downside is that if the main paper's theorem numbering changes, the supplement's textual references must be updated manually.

**Pattern B: restate the theorem (more verbose, fully self-contained).**
```latex
\subsection{Proof of Theorem 1 (Post-Policy Saturation)}
\textit{Theorem~1 (restated from the main paper).} ...full statement...

\begin{proof}
...
\end{proof}
```
Restating the theorem at the start of its proof makes the supplement readable on its own. This is the most reviewer-friendly pattern and is recommended for theorems whose statements are short. For long theorem statements, Pattern A is acceptable.

Detect this bug by compiling the supplement standalone and grepping for `Reference 'thm:`, `Reference 'cor:`, `Reference 'lem:`, `Reference 'prop:`, `Reference 'eq:`, `Reference 'sec:` in the log. Any unresolved reference in the supplement that points to a main-paper-style label is the bug.

### Step L.7: Report findings

Produce a `LATEX_INTEGRITY_REPORT.md` (or include in the polishing review log) with:

- Compile status: SUCCESS / WARNINGS / FAILED
- HIGH and CRITICAL warnings with file:line
- Undefined references with file:line
- Undefined citations with file:line
- Missing image files
- Orphan labels (informational)
- Bib bloat (informational)
- Cross-file reference violations
- For each finding, the exact fix

Fix all HIGH and CRITICAL findings before declaring the polishing pass complete.

## Quick One-Shot Audit

For routine polishing, a fast audit looks like:

```bash
cd paper/
latexmk -C                                                # clean build artifacts
latexmk -pdf -interaction=nonstopmode main.tex 2>&1 \
  | grep -E "Warning|Error|undefined|multiply|missing" \
  > main.compile.issues
cat main.compile.issues
```

If the output is empty, the manuscript compiles cleanly. If not, work through each issue.

Run the same for `supplement/supplement_main.tex` (or whatever the supplement entry point is).

## Common Causes and Fixes

| Symptom | Common cause | Fix |
|---|---|---|
| `Citation 'foo2024bar' undefined` | Bib entry not loaded into `references.bib`, or key typo | Add entry; fix typo |
| `Reference 'thm:upper' undefined` | Label `\label{thm:upper}` not yet placed, or section file not `\input`-ed | Add label; verify `\input` paths in main.tex |
| `multiply-defined labels` | Same theorem environment counter used twice, or same `\label{}` pasted twice | Rename one of them |
| `File 'figures/fig1.pdf' not found` | Figure not generated yet, or path differs | Generate figure; correct path |
| `Missing character: ... no glyph` | Unicode character or math symbol the current font lacks | Switch to a Unicode-aware font, or escape the character |
| `Overfull \hbox (10.5pt too wide)` | Long URL or formula | Break the URL with `\url{}` and `\PassOptionsToPackage{hyphens}{url}`; break formula with `\\` |
| `Undefined control sequence \xxx` | Package missing or command misspelled | Load the package; fix the spelling |
| `LaTeX Error: Environment ... undefined` | Theorem/algorithm environment not declared | Add `\newtheorem{...}` or load `algorithm` |

## Integration

This audit is invoked by:

- `stat-paper-write` Step 8 (Final Checks) and is part of the LaTeX-compile-and-fix workflow
- `stat-polishing` Step 11 (mechanical audits before the optional Codex pass)
- `paper-compile` / `auto-paper-improvement-loop` from the broader skill ecosystem, which apply automated multi-pass compilation and error-fixing

The audit is mechanical and can run unattended once the compile environment is set up. Make it part of every polishing pass; the cost is low and the payoff at submission time is high.
