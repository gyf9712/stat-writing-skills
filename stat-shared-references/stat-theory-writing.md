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
Grant Assumptions~\ref{ass:subgauss}--\ref{ass:smooth}. Let
$\hat{f}_n$ be the estimator in~\eqref{eq:est} with tuning
parameter $\lambda = \lambda_n \asymp (n / \log n)^{-s/(2s+d)}$. Then
\[
  \sup_{f_0 \in \mathcal{W}^{s,2}(L)}
  \mathbb{E}\bigl[\|\hat{f}_n - f_0\|_2^2\bigr]
  \leq C \Bigl(\frac{\log n}{n}\Bigr)^{2s/(2s+d)},
\]
where $C$ depends only on $s$, $d$, $L$, and $\sigma$.
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
