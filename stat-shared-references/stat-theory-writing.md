# Theory Writing Guide for Statistics Papers

Use this reference when writing or reviewing the theoretical components of a statistics paper: assumptions, theorem statements, proof sketches, rate comparisons, and minimax arguments.

## When to Read

- Before writing the Problem Setup / Model section
- Before stating theorems and assumptions
- When organizing proofs between main body and supplement
- When writing rate comparison tables
- When drafting minimax lower bound arguments

## Assumption Organization

### Taxonomy of Assumptions

Statistics papers typically need these categories of assumptions:

**Model assumptions** — what is the data-generating process:
- Distribution family (Gaussian, sub-Gaussian, sub-exponential, bounded)
- Model structure (linear, additive, single-index, nonparametric)
- Noise structure (homoscedastic, heteroscedastic, dependent)

**Regularity conditions** — smoothness, boundedness, identifiability:
- Smoothness of unknown functions (Sobolev, Hölder, Besov)
- Eigenvalue conditions on design matrices (restricted eigenvalue, compatibility)
- Density bounds on covariates (bounded away from 0 and ∞)
- Identifiability conditions (injectivity, rank conditions)

**Structural conditions** — sparsity, dimension, sample size:
- Sparsity level: $s = o(n / \log p)$ or similar
- Dimension scaling: $p = O(n^\alpha)$ for some $\alpha$
- Minimum signal strength: $\min_{j \in S} |\beta_j| \geq \lambda$ (beta-min condition)
- Sample size requirements: $n \geq C \cdot s \log p$ or similar

### Assumption Presentation Rules

1. **Number assumptions consistently**: (A1), (A2), (A3) or (C1), (C2), (C3)
2. **Give each assumption a descriptive name**: \begin{assumption}[Sub-Gaussian noise]
3. **State before the first theorem that needs them**
4. **Separate model assumptions from technical conditions**: readers want to distinguish the statistical model from the proof machinery
5. **Discuss after stating**: which are standard, which are novel, which can be relaxed

### Standard Assumption Patterns

**Sub-Gaussian noise:**
```latex
\begin{assumption}[Sub-Gaussian noise]\label{ass:subgauss}
The noise variables $\varepsilon_1, \ldots, \varepsilon_n$ are independent,
mean-zero, and $\sigma$-sub-Gaussian: for all $t \in \mathbb{R}$,
$\mathbb{E}[\exp(t\varepsilon_i)] \leq \exp(\sigma^2 t^2 / 2)$.
\end{assumption}
```

**Restricted eigenvalue:**
```latex
\begin{assumption}[Restricted eigenvalue]\label{ass:RE}
The design matrix $\mathbf{X} \in \mathbb{R}^{n \times p}$ satisfies
the restricted eigenvalue condition $\mathrm{RE}(s_0, c_0)$: for all
$\boldsymbol{\delta} \in \mathbb{R}^p$ with
$\|\boldsymbol{\delta}_{S^c}\|_1 \leq c_0 \|\boldsymbol{\delta}_S\|_1$
for any $|S| \leq s_0$,
\[
  \frac{1}{n}\|\mathbf{X}\boldsymbol{\delta}\|_2^2
  \geq \kappa \|\boldsymbol{\delta}\|_2^2.
\]
\end{assumption}
```

**Sobolev smoothness:**
```latex
\begin{assumption}[Smoothness]\label{ass:smooth}
The regression function $f_0$ belongs to the Sobolev ball
$\mathcal{W}^{s,2}(L) = \{f \in L^2[0,1]^d :
\sum_{|\boldsymbol{\alpha}| \leq s}
\|D^{\boldsymbol{\alpha}} f\|_2 \leq L\}$
for some known smoothness $s > 0$ and radius $L > 0$.
\end{assumption}
```

## Theorem Statement Patterns

### Upper Bound (Estimation)

```latex
\begin{theorem}[Risk upper bound]\label{thm:upper}
Grant Assumptions~\ref{ass:subgauss}--\ref{ass:smooth}, and let
$\hat{f}_n$ be the estimator in~\eqref{eq:est} with
\[
  \lambda = \lambda_n \asymp (n / \log n)^{-s/(2s+d)}.
\]
Then, as $n \to \infty$,
\[
  \sup_{f_0 \in \mathcal{W}^{s,2}(L)}
  \mathbb{E}\bigl[\|\hat{f}_n - f_0\|_2^2\bigr]
  \leq C \Bigl(\frac{\log n}{n}\Bigr)^{2s/(2s+d)},
\]
where $C$ depends only on $s$, $d$, $L$, and $\sigma$.
\end{theorem}
```

The tuning condition sits on its own display line (a load-bearing rate condition), the
regime `as $n\to\infty$` immediately precedes the conclusion, and the conclusion is
displayed — so the eye lands on the two key formulas and the "Then" between them. See
"Statement layout for at-a-glance reading" for when to display a condition versus keep
it inline. Contrast the compact inline form, appropriate when the tuning choice is not
the point of the theorem:

```latex
\begin{theorem}[Risk upper bound]\label{thm:upper-compact}
Under Assumptions~\ref{ass:subgauss}--\ref{ass:smooth}, the estimator
$\hat{f}_n$ in~\eqref{eq:est} with $\lambda \asymp (n/\log n)^{-s/(2s+d)}$
satisfies, as $n \to \infty$,
\[
  \sup_{f_0 \in \mathcal{W}^{s,2}(L)}
  \mathbb{E}\bigl[\|\hat{f}_n - f_0\|_2^2\bigr]
  \leq C \Bigl(\frac{\log n}{n}\Bigr)^{2s/(2s+d)}.
\]
\end{theorem}
```

### Minimax Lower Bound

```latex
\begin{theorem}[Minimax lower bound]\label{thm:lower}
Under the model~\eqref{eq:model}, for all $n$ sufficiently large,
\[
  \inf_{\hat{f}} \sup_{f_0 \in \mathcal{W}^{s,2}(L)}
  \mathbb{E}\bigl[\|\hat{f} - f_0\|_2^2\bigr]
  \geq c \, n^{-2s/(2s+d)},
\]
where $c > 0$ depends only on $s$, $d$, $L$, and $\sigma$, and
the infimum is over all estimators $\hat{f}$ measurable with
respect to $(X_1, Y_1), \ldots, (X_n, Y_n)$.
\end{theorem}
```

### Asymptotic Normality

```latex
\begin{theorem}[Asymptotic normality]\label{thm:clt}
Under Assumptions~\ref{ass:model}--\ref{ass:moment},
as $n \to \infty$,
\[
  \sqrt{n}(\hat{\theta}_n - \theta_0)
  \xrightarrow{d}
  \mathcal{N}\bigl(0, \, I(\theta_0)^{-1}\bigr),
\]
where $I(\theta_0)$ is the Fisher information matrix at $\theta_0$.
\end{theorem}
```

### Uniform Convergence / Concentration

```latex
\begin{theorem}[Uniform concentration]\label{thm:concentration}
Under Assumption~\ref{ass:subgauss}, for any $\delta \in (0,1)$,
with probability at least $1 - \delta$,
\[
  \sup_{f \in \mathcal{F}}
  \bigl|\hat{R}_n(f) - R(f)\bigr|
  \leq C \left(
    \frac{\mathcal{R}_n(\mathcal{F})}{\sqrt{n}}
    + \sqrt{\frac{\log(1/\delta)}{n}}
  \right),
\]
where $\mathcal{R}_n(\mathcal{F})$ is the Rademacher complexity
of $\mathcal{F}$.
\end{theorem}
```

### Hypothesis Testing

```latex
\begin{theorem}[Power guarantee]\label{thm:power}
Under Assumptions~\ref{ass:null}--\ref{ass:alt}, the test
$\phi_n$ defined in~\eqref{eq:test} satisfies:
\begin{enumerate}[(i)]
\item (Size control) $\sup_{P \in \mathcal{P}_0}
  \mathbb{E}_P[\phi_n] \leq \alpha + o(1)$.
\item (Power) For any $P \in \mathcal{P}_1(\rho_n)$ with
  $\rho_n \geq C \sqrt{(\log p) / n}$,
  $\mathbb{E}_P[\phi_n] \to 1$ as $n \to \infty$.
\end{enumerate}
\end{theorem}
```

## Rate Comparison Tables

### Why They Matter

Reviewers expect to see how your rate compares with prior work. A comparison table is often the most efficient way to communicate this.

### Template

```latex
\begin{table}[t]
\centering
\caption{Comparison of estimation rates for $f_0 \in \mathcal{W}^{s,2}(L)$.
Our rate matches the minimax lower bound up to logarithmic factors
and holds under weaker noise assumptions than prior work.}
\label{tab:rates}
\begin{tabular}{lccc}
\toprule
Reference & Rate & Noise & Adaptive? \\
\midrule
\citet{stone1982} & $n^{-2s/(2s+d)}$ & Gaussian & No \\
\citet{donoho1998} & $n^{-2s/(2s+d)}$ & Gaussian & Yes \\
\citet{prior_work2020} & $(n/\log n)^{-2s/(2s+d)}$ & sub-Gaussian & No \\
\textbf{This paper} & $\boldsymbol{(n/\log n)^{-2s/(2s+d)}}$ & \textbf{sub-exponential} & \textbf{Yes} \\
\midrule
Minimax lower bound & $n^{-2s/(2s+d)}$ & — & — \\
\bottomrule
\end{tabular}
\end{table}
```

### What to Compare

- Convergence rate (exact expression)
- Noise/distribution assumptions
- Whether the method is adaptive (tuning-parameter-free)
- Whether the result is uniform or pointwise
- Computational complexity (if relevant)
- Whether constants are explicit

## Minimax Lower Bound Arguments

### Common Proof Techniques

1. **Fano's inequality**: for metric entropy / packing arguments
2. **Assouad's lemma**: for hypercube-based constructions
3. **Le Cam's method**: two-point testing, simplest to apply
4. **Fano-Assouad hybrid**: for structured problems

### Proof Sketch Template (Fano's Method)

```
The lower bound follows from Fano's inequality. We construct a 
finite subset {f_1, ..., f_M} ⊂ F such that:
(i) the functions are well-separated: ||f_j - f_k||_2 ≥ δ for 
    all j ≠ k,
(ii) the Kullback-Leibler divergences are controlled: 
     KL(P_{f_j} || P_{f_k}) ≤ β for all j, k,
(iii) log M ≥ 2nβ + log 2.

Choosing δ ∝ n^{-s/(2s+d)} and verifying conditions (i)-(iii) 
yields the minimax lower bound. The construction uses a 
standard wavelet basis; see Supplement Section A.3 for details.
```

## Proof Sketch Best Practices

### What a Main-Body Proof Sketch Should Contain

1. **Key decomposition**: how the error or quantity of interest is split
2. **Main technical challenge**: which term is hard and why
3. **Novel ingredient**: what new tool, idea, or technique is used
4. **Result**: how the pieces combine to give the final bound
5. **Pointer**: where the full proof lives in the supplement

### Template

```latex
\begin{proof}[Proof sketch of Theorem~\ref{thm:upper}]
The proof proceeds in three steps.

\emph{Step 1: Bias-variance decomposition.}
We decompose the integrated squared error into a deterministic
bias term $B_n$ and a stochastic variance term $V_n$
(Lemma~\ref{lem:decomp}).

\emph{Step 2: Bias bound.}
Standard approximation theory gives
$B_n \leq C_1 h^{2s}$ for bandwidth $h$
(Lemma~\ref{lem:bias}).

\emph{Step 3: Variance bound.}
The key technical contribution is a new chaining argument that
exploits [specific structural property]. This yields
$V_n \leq C_2 (nh^d)^{-1} \log n$ with probability at least
$1 - n^{-2}$ (Lemma~\ref{lem:variance}; full proof in
Supplement~\ref{app:variance}).

Balancing $B_n$ and $V_n$ by choosing $h \asymp (n/\log n)^{-1/(2s+d)}$
gives the stated rate.
\end{proof}
```

The staged `\emph{Step k}` labels above are a **main-body-sketch** navigation device for a short three-step overview; they are not the model for full appendix proofs (see the register section below), and the manual emphasis is tolerated only because a sketch is compressed. In a full proof, prefer prose transitions with semantic content.

## Mathematical Register and Readability (Big Four)

This section governs theorem statements and full proofs. It complements
`stat-style-discipline.md`; it does not relax the bans on bullet sprawl,
"Note that" openers, "is given by", em-dashes, over-signposting, or
rule-of-three padding. Readability at the Big Four is dense-but-navigable prose
carried by displays, never fragmentation into bullet lists or ML-conference
"Step 1 / Step 2" scaffolding.

### Statements

Define every symbol before the statement uses it. Refer to hypotheses by label,
as in `Under Assumptions~\ref{ass:model} and~\ref{ass:moment}`. Do not restate
registered assumptions inside the theorem unless no assumption registry exists
(see `assumptions-lock-protocol.md`).

Put the mathematical conclusion in a display when it is a rate, limiting law,
probability bound, optimization characterization, or nontrivial inequality.
Short qualitative consequences may remain inline.

Use one conceptual result per theorem environment. If the result has inseparable
parts under the same hypotheses (size and power; consistency and asymptotic
normality), label the parts `(i)`, `(ii)`, ... inside the same theorem and prove
them by those labels.

### Statement layout for at-a-glance reading

Every theorem statement should let a reader see, in one glance, *under what* and
*what follows*. The mechanism is line breaks that put load-bearing mathematics on
its own display line — not a rigid two-block "hypothesis/conclusion" skeleton with
headers, which is over-structuring. Big Four statements are running prose in which
the eye lands on the displayed conclusion; readability comes from displaying the
right things, not from sectioning the statement.

**Single-flow form, not two-block.** The dominant Big Four shape is a lead clause
(hypotheses by label + regime) followed by the displayed conclusion:
`Under Assumptions~\ref{...}, as $n\to\infty$, [display].` Use the explicit
`Suppose that ... . Then ... .` If/Then skeleton when a theorem-specific condition
must be foregrounded; use the compact `Under Assumptions 1--3, [display]` when every
condition is registered. AoS/JASA T&M lean If/Then; Biometrika/JRSS-B lean compact.

**What goes on its own display line vs inline vs by-label.**

- **By-label** — any assumption registered in an Assumption/Condition environment.
  Never restated in the theorem (see `assumptions-lock-protocol.md`).
- **Display (own line)** — theorem-specific *load-bearing* mathematics the reader
  needs to parse the conclusion: a rate/order condition (`\lambda_n \asymp \cdots`,
  `nh^d \to \infty`), a signal-strength / separation condition
  (`\rho_n \ge C\sqrt{(\log p)/n}`), a tuning choice the rate depends on, or a
  moment/bandwidth condition that sizes the result. The conclusion is always
  displayed.
- **Inline** — scoping qualifiers that carry no load: `\delta \in (0,1)`,
  `n \ge 1`, fixed-constant declarations, and pointers to earlier-defined objects
  (`the estimator $\hat f_n$ in~\eqref{eq:est}`, `the test $\phi_n$`).

Operational test: if a reader needs the condition to understand *what the
conclusion says or how strong it is*, display it; if it only scopes the statement,
inline it. Keep at most one or two displayed conditions before the conclusion; if
more accumulate, move them into a labeled Condition environment immediately before
the theorem — that cluster of labeled, individually displayed conditions is the
primary at-a-glance mechanism, and it keeps the theorem itself compact.

**Supporting conventions.** Define the estimator / test in the text (as a numbered
equation) *before* the theorem and reference it by label; do not define it inside
the statement. Put the regime clause (`as $n\to\infty$`, `for $n$ sufficiently
large`, `with probability at least $1-\delta$`) immediately before the conclusion
display. For a compound result, write `Then the following hold:` and give each part
as a labeled, displayed `(i)`/`(ii)` line.

**Per-theorem readability micro-check** (run theorem by theorem): (a) is the
conclusion displayed? (b) is every substantive condition either displayed or
by-label, with none buried inline? (c) could a reader restate the hypotheses and
the conclusion after a single glance? (d) are multi-part results labeled `(i)`/`(ii)`?
(e) is every symbol defined before the statement uses it? A "no" on (a) or (b)
means re-lay-out the statement.

Venue calibration: AoS and JASA T&M tolerate a lead clause carrying one or two
displayed conditions; JRSS-B is moderate; Biometrika is the most compact but still
displays the conclusion and any substantive rate/signal condition. Displaying a
theorem-specific load-bearing condition on its own line is standard at all four —
it is dumping *registered* assumptions back into the theorem that is non-standard.

### Full proofs

Full proofs are written in paragraphs, not bullets. Dense Big Four prose is
acceptable when each paragraph has one logical role and algebra is carried by
displays. A paragraph has become a **wall of text** — split it or display the
math — if any of these fire: it closes more than one proof obligation; it exceeds
about eight prose sentences without a display; it contains two consecutive
sentences that each carry multiple mathematical relations; or it leaves no stable
display, lemma, or equation reference for the bound it claims.

Open with one sentence fixing the reduction or strategy: `It suffices to prove
\eqref{eq:linear} and \eqref{eq:remainder}.` Do not restate the theorem inside
its proof.

Use a display for every nontrivial algebraic, probabilistic, or asymptotic
transition the reader may need to inspect; do not bury a multi-line derivation
inside prose. Connect displays with short prose giving the reason: `by
Cauchy--Schwarz`, `by Lemma~\ref{lem:entropy}`, or `combining \eqref{eq:bias}
and \eqref{eq:variance}`.

**At a glance for proofs, too.** A proof is read the way a statement is: the reader
should be able to skim the displayed formulas and the short connectives between them
and recover the reasoning skeleton without parsing every sentence. So the key steps
go on their own display lines (line breaks highlight the mathematics that carries the
argument), and each connective must name the logical move that links one display to
the next — `it suffices to bound`, `hence`, `by \eqref{eq:bias}`, `on the event
$\mathcal{E}_n$`, `combining the two bounds`. Displays carry the *what*; connectives
carry the *why*. If a reader scanning only the displays and their one-line
justifications cannot follow the logic, the reasoning is buried in prose — pull the
load-bearing step into a display and make the connective explicit.

Use **one logical unit per display**, not one microscopic inference per display.
A single `align`/`aligned` display may chain primitive transformations while the
object, event, norm, and proof tool stay fixed. Start a new display when the
argument changes object, changes probability mode or norm, moves from an event to
an unconditional statement, invokes a new theorem or lemma, begins a case, or
closes a named obligation.

Number only displays referred to later or that close a named obligation. Use
`\label`/`\eqref`; never type equation numbers manually. In an `align` chain,
number only the line that will be cited and `\notag` the rest. Use `equation` for
one numbered display, `equation`+`aligned` for one numbered multi-line
derivation, `align` when several lines need separate numbers, and `\[...\]` /
`align*` for local unnumbered algebra. Never `eqnarray`.

Break long proofs by **logical stage**, not cosmetic de-blocking. Prefer prose
transitions (`We first control the empirical term`; `It remains to remove the
localization`) over `Step 1` labels. Numbered stages are acceptable only for
genuinely long multi-stage proofs, and they must carry semantic titles, not
generic labels. Venue calibration: AoS and technical supplements tolerate staged
proofs; JRSS-B tolerates restrained staging; JASA T&M prefers compact prose with
staged appendices acceptable; Biometrika is strictest — prefer prose transitions
or appendix subsectioning.

Displayed mathematics is part of the sentence: punctuate it (comma or period at
the end where grammar requires), and use a colon before a display only when the
preceding clause grammatically announces it. Use a `where` clause after a display
only for local definitions or constant dependence; if it would hold assumptions,
several definitions, or a full sentence, define those objects before the display.

Capitalize numbered formal objects in cross-references (`Theorem~\ref{thm:main}`,
`Lemma~\ref{lem:linear}`, `Assumption~\ref{ass:tail}`), lowercase for generic
references (`the next lemma`, `the display above`), and `\eqref{...}` for
equations. Let the venue class handle the proof environment: `\begin{proof}`,
`Proof of Theorem~\ref{thm:main}` only when separated from the statement,
`\qedhere` only when the proof ends in a display, and never a second manual QED
marker. Keep prose words out of displays; put explanations in the surrounding
prose; `\,` for standard thin spacing, `\quad` for short side conditions, `\;`
sparingly and never as padding.

## Remark Patterns

Remarks after theorems serve important functions. Common types:

### Rate Optimality Remark
```latex
\begin{remark}[Optimality]
Comparing Theorems~\ref{thm:upper} and~\ref{thm:lower}, the
estimator $\hat{f}_n$ is minimax rate-optimal up to a
$(\log n)^{s/(2s+d)}$ factor. Whether this logarithmic factor
is necessary remains an open question.
\end{remark}
```

### Assumption Discussion Remark
```latex
\begin{remark}[On Assumption~\ref{ass:subgauss}]
The sub-Gaussian condition can be relaxed to polynomial tails
$\mathbb{E}[|\varepsilon|^q] < \infty$ for $q > 4$ at the cost
of a slower rate; see Supplement~\ref{app:heavy-tail}. The
Gaussian assumption in \citet{prior_work} is strictly stronger.
\end{remark}
```

### Extension Remark
```latex
\begin{remark}[Extension to random design]
Theorem~\ref{thm:upper} is stated for fixed design. The result
extends to random design under Assumption~\ref{ass:design} via
a standard conditioning argument; see Supplement~\ref{app:random}.
\end{remark}
```

### Connection to Prior Work
```latex
\begin{remark}[Comparison with \citet{prior_work}]
When specialized to the Gaussian case ($\sigma$-sub-Gaussian with
$\psi_2$ norm), our bound recovers the rate of \citet{prior_work}
as a special case. The improvement lies in the relaxation from
sub-Gaussian to sub-exponential noise.
\end{remark}
```

## Corollary Patterns

Use corollaries to specialize the main theorem to important cases:

```latex
\begin{corollary}[Parametric rate for smooth functions]
\label{cor:parametric}
Under the conditions of Theorem~\ref{thm:upper}, if $s > d/2$,
then the estimator $\hat{f}_n$ with appropriately chosen $\lambda$
achieves the parametric rate:
$\mathbb{E}[\|\hat{f}_n - f_0\|_2^2] = O(n^{-1})$.
\end{corollary}
```

## LaTeX Theorem Environments

### Recommended Setup for Statistics Papers

```latex
\usepackage{amsthm}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}

\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{assumption}{Assumption}  % separate counter
\newtheorem{example}[theorem]{Example}
\newtheorem{condition}{Condition}

\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}

% For Assumptions with labels like (A1), (A2):
% \renewcommand{\theassumption}{A\arabic{assumption}}
```

## Common Theory-Writing Pitfalls

| Pitfall | Fix |
|---------|-----|
| Theorem stated without referencing assumptions | "Grant Assumptions (A1)-(A3)" in the preamble |
| Rate has implicit constants but claims optimality | State what constants depend on; discuss tightness |
| "By standard arguments" for a non-standard step | Either give the argument or cite a precise reference (theorem number) |
| Lower bound proved for a different function class | Ensure upper and lower bounds match the same class |
| Adaptive result claimed but tuning depends on unknowns | Specify what the tuning parameter depends on |
| Proof uses an assumption not listed | Add the assumption or weaken the proof to avoid it |
| "The proof is similar to [ref]" for a novel setting | Explain what changes and why the argument still works |

## Formalizing Statements (the formal-statement-pass mode)

`stat-polishing`'s `--formal-statement-pass` mode rewrites assumptions, definitions, theorem and lemma statements, and displayed conditions into more formal, more conventional, equivalence-preserving forms aligned with the target venue's published register. The governing protocol is `equivalence-ledger-protocol.md` (in the sibling `stat-theory-skills` repo). This section is the statement-pattern reference the mode draws from. **Read the protocol's standing refusal condition first**: never formalize to increase apparent depth; precision over notational sophistication.

### Precision-increasing formalization patterns (apply)

These resolve a referee-checkable ambiguity. Each "before" leaves a question the "after" answers.

| Vague / informal | Formalized | Ambiguity resolved |
|---|---|---|
| "$p$ is large" | "$\log p / n \to 0$ as $n \to \infty$" | with respect to what limit |
| "the estimator is consistent" | "$\hat\theta_n \to \theta_0$ in probability as $n \to \infty$" | probability mode + limit |
| "uniformly good over the class" | "$\sup_{f \in \mathcal{F}} \mathbb{E}\,\ell(\hat f, f) \le C r_n$" | uniform over which class, in which loss |
| "the error is small" | "$\|\hat\theta_n - \theta_0\|_2 = O_P(n^{-1/2})$" | in which norm, what stochastic order |
| "holds with high probability" | "with probability at least $1 - 2 p^{-c}$ for a constant $c > 0$" | what probability level, in what regime |
| "the design is regular" | (only if the author confirms the intended condition) "$\lambda_{\min}(n^{-1} X^\top X) \ge \kappa > 0$" | which regularity, uniform or per-$n$ — SEMANTIC, ledger it |

The last row is the cautionary one: it is a semantic rewrite (touches conditioning / constants / uniformity) and must go through the per-atomic-claim gate with an equivalence-ledger row, not applied silently. "Regular" might mean only per-$n$ invertibility, not a uniform lower bound.

### Decoration patterns (refuse or flag)

These raise the reading barrier without resolving any ambiguity.

| Decoration | Why it is theater | What to do |
|---|---|---|
| Measure-theoretic dress on an elementary i.i.d. argument | The probability space is never used beyond the elementary statement | Keep the elementary statement |
| Operator notation for a scalar quantity | The "operator" acts on a one-dimensional space | Use the scalar |
| Empirical-process language ($\mathbb{G}_n$, Donsker) for a plain sample mean | The process structure is never exploited | Use the sample mean |
| Introducing a function space the paper never revisits | Fails the use-test | Withdraw the space |
| Bourbaki-style maximal generality with no downstream payoff | Generality is not used by any theorem | State the case actually proved |

### Notation formalism: legitimate only when the object lives in the structure

Introducing operators, function spaces, measure-theoretic objects, or processes is legitimate only when the object already lives in that structure AND is used downstream (use-test): stochastic-process convergence, operator norms, function classes, empirical measures, RKHS objects, semiparametric tangent spaces. Otherwise it is decoration.

### Venue formalism register

Target the venue's actual register, not maximum formalism.

| Venue | Register |
|---|---|
| AoS / Bernoulli / EJS | High formalism native; measure-theoretic and empirical-process language expected when the object is used |
| JRSS-B | Middle; formal where precision demands, not gratuitously heavy |
| Biometrika | Concise and readable; excess formalism penalized; compact assumptions with verbal interpretation |
| JASA T&M | Compact assumptions plus verbal interpretation; formalism for precision, not display |
| JASA ACS / AOAS | Application-facing; formalism that hurts readability is wrong |
| Biostatistics / JCGS | Readable; formalism subordinate to the applied narrative |

### Cross-reference drift after a formalization

Rewriting a labeled object (an assumption's name, number, or verbal handle) silently breaks later references: "the boundedness condition", "the compatibility condition", "Assumption 3(ii)" in prose and proofs. After any such rewrite, audit every downstream reference and update or flag it. Reuse `stat-notation-audit.md`. This is the most common first-pass failure of the formal-statement pass.
