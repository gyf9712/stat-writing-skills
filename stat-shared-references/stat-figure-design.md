# Figure Design for Statistics Papers

Use this reference when planning, generating, or polishing figures and tables for statistics papers. The standards here apply across theory, methodology, and application papers, with extra emphasis on EDA and application figures in application papers.

## When to Read

- Before generating figures in `stat-paper-figure` or `paper-figure`
- When polishing existing figures
- When the user asks why a figure does not look journal-ready
- When designing EDA figures for §2 of an application paper
- When designing the centerpiece figures in §6 of an application paper

## Core Rule: No Titles Inside Figures

Statistics papers do not use titles inside figures. The reason is that journals already provide a separate Figure caption below the figure, and a redundant title duplicates information, wastes space, and clashes with the journal's typesetting.

What to do:
- Remove every `plt.title(...)` and `ggtitle(...)` call.
- Move the information that would have been in the title into the caption.
- Keep panel labels (a, b, c, d) inside the figure when the figure has subpanels, but no narrative title.

What the caption should carry instead:
- What is shown
- How to read it
- What the reader should notice
- What the conclusion is

Example caption pattern:
```
Figure 3. Estimated regression coefficients across n in [200, 500, 2000, 5000].
Solid lines: proposed estimator; dashed lines: oracle. Shaded bands: 95% Monte
Carlo intervals across 1000 replications. The proposed estimator approaches the
oracle as n grows, with the gap closing at the predicted rate n^{-1/2}.
```

The caption tells the reader the data, the visual encoding, the uncertainty, and the takeaway. The figure itself only carries axis labels, legend, and the data.

## Caption Discipline

A good figure caption in a statistics paper:

- Begins with a short noun phrase identifying what is shown
- States visual encoding (color, linetype, shading)
- States uncertainty quantification when applicable
- Ends with a one-sentence takeaway when space allows
- Does not depend on the surrounding paragraph for essential meaning
- Avoids forward references to undefined notation
- Uses the same variable names as the main text

Caption length:
- Theory/methodology paper simulation figures: 3 to 5 lines
- Application paper EDA figures: 3 to 6 lines
- Application paper main analysis figures in §6: 4 to 8 lines (these often act as standalone units)

What captions should not contain:
- The full methodological background
- Citations except when the data source itself is the citation
- Discussion of why the result matters at length (that goes in the text)

### Caption Capitalization and Punctuation

Capitalization and terminal punctuation are venue-specific, not author preference. Statistics journals overwhelmingly use sentence-style captions, in contrast to the title-case captions common in ML conferences. Default to sentence style: capitalize only the first word and proper nouns; end the caption with a full stop. Do not place a title inside the figure or table; that information moves to the caption.

| Venue | Figure caption | Table title |
|---|---|---|
| Biometrika | Sentence-style, full stop at end. Each subsequent sentence in the caption also ends with a full stop. | Sentence-style; the last sentence of the title does not take a full stop. |
| Annals of Statistics | Sentence-style, full stop at end. | Sentence-style, full stop at end. |
| JASA / ASA journals | Sentence-style, full stop at end. | Sentence-style, full stop at end. |
| JRSS-B (and JRSS-A, JRSS-C) | Sentence-style; brief, clear, self-explanatory; substantive comments belong in the main text, not in the caption. | Sentence-style. |
| AOAS, Bernoulli, EJS | Sentence-style following `imsart` class defaults. | Sentence-style. |
| Biostatistics, JCGS | Sentence-style. | Sentence-style. |

Title case (`Performance Comparison Across Sample Sizes`) is an ML conference convention and is wrong for the Big Four. Convert to sentence style (`Performance comparison across sample sizes.`) before submission.

Symbol descriptions, line type explanations, and abbreviation expansions belong in the caption or table note, written in plain text. Do not bold them, italicize them, or set them as a subtitle inside the figure.

## Legend Discipline

Legends are the most frequent source of figure ugliness. The two killers are:

- Legends that overlap the data
- Legends that take more space than the plot

Default placement strategy in order of preference:

1. Outside the plot area to the right or below the panel
2. Inside the plot area only when there is genuinely empty space and the legend will not move when data are added
3. Replaced by direct labels on the lines or points when there are at most three series

Sizing rules:
- Legend font size must match the axis tick font size, not be larger
- Marker sizes in the legend should match the markers in the data
- One legend per multi-panel figure, not one per panel, unless panels show different sets of series

When a legend is unavoidable inside the plot area:
- Use `loc='best'` only in exploratory work, not in final figures
- Set an explicit `loc` and confirm it does not overlap the data at any sample size
- Use semi-transparent background (`framealpha=0.7` or similar) sparingly, only when the data underneath is not the focus
- Check at every figure size you plan to use, including the two-column journal width

Hard rule: a legend that crosses a line, marker, or band has not been finished.

## Axis Labels

Axis labels should be:
- Short noun phrases or single quantities
- Typeset in the same math notation as the main text
- Free of decorative units when the quantity is unitless
- Unambiguous: `Sample size n` is better than `Sample size`, which is better than `n`

Tick labels:
- Use scientific notation for very large or very small values, not raw zeros
- Use the same number of decimal places across ticks unless the precision genuinely varies
- For log scales, use 10^k labels, not the raw values

Tick density:
- Five to seven major ticks per axis is usually right
- More ticks make the figure look busy
- Fewer ticks make it hard for the reader to read off values

## Color, Linetype, Marker Discipline

Color rules:
- Use a colorblind-safe palette by default
- Avoid pure red and pure green together in any plot
- The proposed method should have a distinct color used consistently across the paper
- Comparison methods should use neutral colors, not bright primaries

Linetype rules:
- Solid for the proposed method
- Dashed or dotted for comparison methods
- Dotted for oracle or theoretical baselines
- Use the same encoding across all figures in the paper

Marker rules:
- Distinct shapes that remain distinguishable in grayscale
- Filled markers for the proposed method, open markers for comparisons
- Marker size should be large enough to read at journal column width but not large enough to overlap on dense plots

The goal is that a printed black-and-white version of the figure is still interpretable.

## Sizing and Aspect Ratio

For two-column journals (most stat journals):
- Single-column figures: typically 3.0 to 3.5 inches wide
- Two-column figures: typically 7.0 to 7.5 inches wide
- Set the figure size before plotting, not after; rescaling stretches fonts and lines

Aspect ratio:
- Time series and convergence plots: usually wider than tall (golden ratio or 4:3)
- Heatmaps: square unless the row and column counts differ substantially
- Scatter plots: usually square unless one axis has much wider range

Font size at final size:
- Axis tick labels: 8 to 10 pt
- Axis labels: 9 to 11 pt
- Legend: 8 to 10 pt
- Panel labels (a, b, c): 10 to 12 pt, bold
- Never use fonts smaller than 7 pt, since they become illegible after PDF compression

## Choosing the Figure Type

Before drawing anything, name the statistical question the figure must answer. Big Four figures are read for content, not for visualization fluency. A figure that does not answer a clean statistical question (estimand, comparison, rate, distribution, calibration, sensitivity, or trade-off) does not belong in the paper.

### Question-driven mapping

| Statistical question | Default display | Notes |
|---|---|---|
| Does $\hat\theta_n$ converge at the predicted rate? | Log-log line plot of error vs $n$ with reference slope | Mark the theoretical slope; do not extrapolate beyond simulated range. |
| Are competing estimators distinguishable across $n$ or signal-to-noise? | Lines with shaded Monte Carlo bands across the design grid | Use the same color and line-type encoding across all figures in the paper. |
| Is the distribution of an estimator non-normal? | Histogram with overlaid density or theoretical reference | Show sample size in the caption. |
| Are the two methods' performance distributions different? | Box plot or strip plot of the replication-level metric | Use box plots when $n_{\text{rep}} \ge 30$; do not use violin plots unless $n_{\text{rep}}$ is large enough to support a stable density estimate. |
| Is there a speed/accuracy or bias/variance trade-off? | Scatter of one metric vs the other with method labels | Avoid the "Pareto frontier" term and the highlighted-frontier line unless the trade-off is the contribution. |
| Is the model well-calibrated? | Calibration plot (predicted vs empirical) with reference line $y=x$ | Show confidence bands or binning bin counts. |
| What is the structure of the data motivating the model? | EDA figures: scatter with smoother, density, KM curves, spatial map, missingness pattern | See the EDA figures section. |
| What is the effect estimate with uncertainty? | Coefficient or effect plot with CI bars; for many parameters, a forest plot | Always show uncertainty; ordering reveals or hides structure, so order intentionally. |
| How does a binary classifier perform under class imbalance? | Precision-recall curve | ROC is acceptable for roughly balanced classes; for severely imbalanced data, PR is the standard. |
| How does the model's behavior change with a tuning parameter? | Line plot vs the parameter, with confidence bands | Plot the metric the reader cares about, not the loss the optimizer minimizes. |
| What is the dependence structure among $p$ variables? | Heatmap of the (estimated) covariance, correlation, or partial correlation matrix | Cluster rows and columns if structure exists; otherwise keep original order. |

### Big Four guardrails

The following defaults exist because they kill more figures than they save.

- **No violin plots unless sample size supports density estimation.** A violin built on 10 or 20 replications is a smooth that lies about the shape. Box plots or strip plots are honest at small replication counts.
- **No broken axes.** Broken y-axes hide the magnitude of effects and invite reviewer suspicion. If two scales differ by orders of magnitude, use a log scale or split the figure into two panels with consistent linear scales within each panel.
- **Log scale for orders of magnitude; normalization for relative improvement.** Choose deliberately. Do not log-transform an axis to make small differences look bigger. Use a $\log_{10}$ scale only when the data span at least one full decade and the multiplicative structure matters.
- **Avoid dual-y plots except for deterministic transformations.** A second y-axis with a different metric on the same plot misleads readers who cannot tell which series belongs to which axis. Two panels, or a single normalized scale, is almost always better. The narrow exception is a deterministic transformation of one axis (e.g., temperature in C and F, probability and log-odds), where the reader is not asked to compare two distinct quantities.
- **No inset legends in Biometrika and similar tight-layout journals.** Move the legend outside the panel or replace it with direct labels on the curves. Some journals enforce this explicitly; treat it as a default everywhere.
- **No facet grids over more than a 4-by-4 layout.** Beyond that, individual panels become unreadable at journal column width. Use small multiples sparingly and prioritize the comparison the paper actually makes.
- **No 3D plots in statistics papers.** 3D wireframes, 3D bars, and 3D pie charts hide rather than reveal. Use a 2D heatmap, contour plot, or pairs plot instead.
- **No pie charts in body content.** Pie charts compare angles, which readers do poorly. Use a horizontal bar chart for category proportions.
- **Show uncertainty for every estimate that the reader is invited to interpret.** Bands, error bars, or posterior intervals. A point estimate without uncertainty is a half-finished figure.
- **Use the same encoding across all figures in the paper.** Color, linetype, marker for each method must be fixed in Figure 1 and reused everywhere. Inconsistent encoding forces the reader to relearn the legend at every figure.

### Architecture and splash figures

Statistics papers rarely use the architecture-diagram-as-splash-figure style common at NeurIPS and ICML. A method-overview figure is acceptable only when it clarifies the statistical object, the data flow between stages, or the inferential target, and only when the verbal description alone is insufficient. Pastel flat-vector "framework figures" generated by image models are a CV/NLP convention and look like marketing in a Big Four manuscript. Avoid them. If the method genuinely benefits from a diagram, render it with TikZ or a vector drawing tool, use minimal labels, and let the caption carry the explanation.

When AI image generation is used to draft figures, check the venue's AI disclosure policy. OUP journals (Biometrika, Biostatistics, JRSS-B) require disclosure of generative-AI tools used in the manuscript or its figures.

## Multi-Panel Figures

When a figure has multiple panels:
- Label panels (a), (b), (c) in the top-left corner of each panel
- Use the same axis ranges across panels when comparable, different ranges only when necessary
- Share axis labels across rows or columns to reduce redundancy
- One overall legend, not one per panel, unless panels show different series
- The reading order is left-to-right, top-to-bottom; arrange panels accordingly
- Caption identifies what each panel shows: `(a) ...; (b) ...; (c) ...`

A 2x2 multi-panel figure is often more effective than four separate figures, because it forces the reader to compare what is shown across panels.

## File Format and Resolution

Format:
- Vector (PDF or EPS) for all line plots, bar plots, and tables-as-figures
- Raster (PNG at 300 dpi or higher) only when the figure has many overlapping elements (e.g., dense scatter)
- TIFF when the journal explicitly requires it

Compression:
- For PDF, embed all fonts using `\usepackage{pdfpages}` workflow or matplotlib's `pdf.fonttype = 42`
- For raster, use lossless compression in PNG, not lossy JPEG

File naming:
- `figure1_main_comparison.pdf`
- `figure2_rate_verification.pdf`
- `figure3_application_main.pdf`
- Avoid spaces, use lowercase, use a number prefix matching the figure number

## EDA Figures (Application Papers §2)

EDA figures in application papers carry exceptional weight, since they motivate the methodology. Standards:

- One figure per data feature that motivates methodology
- The figure should answer a question the reader will ask
- Captions should explicitly connect the visual to the statistical challenge: "Figure 2 shows X, motivating the model component introduced in Section 3.2."
- Include enough detail that a domain reader can verify the data structure
- For spatial data, include a map with appropriate projection
- For time series, show at least one example trajectory plus an aggregate
- For multivariate data, consider a pairs plot or correlation heatmap for key variables
- For survival data, show Kaplan-Meier estimates with confidence bands
- For missingness, a missingness pattern matrix or proportion plot

Common EDA figures and what they reveal:
- Histogram with overlaid density: distribution shape, multimodality, heavy tails
- Scatter plot with smoother: relationship form, heteroscedasticity, nonlinearity
- Box plot by group: between-group variation, outliers, group sample sizes
- Trajectory plot: temporal pattern, individual variability
- Map: spatial structure, hotspots, design boundaries
- Heatmap: pairwise structure, block patterns

## Application Section Figures (§6)

Figures in the application section are the paper's centerpiece visuals. Standards:

- Each figure must add insight, not duplicate a table
- Captions should be self-contained: a reader reading only the figures should follow the analysis
- Estimates should be shown with uncertainty (CI bands, error bars, posterior intervals)
- When comparing the proposed method with a domain-standard method, use side-by-side panels or overlays that make the comparison direct
- Reference figures in the text with a guided tour: `Figure 5 shows ... The notable feature is ... This indicates ...`
- The figure should encode the substantive finding, not just the model output

## Tables

Tables follow the same no-title rule. Information moves to the caption.

Table formatting:
- Use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) for horizontal rules
- No vertical rules
- Three-line table style is standard in statistics
- Significant digits should be consistent within a column
- Standard errors in parentheses below or beside the estimate
- The proposed method's row in bold or marked with a clear indicator
- Column headers should be short and unambiguous

Example:
```latex
\begin{table}[t]
\centering
\caption{Mean squared error (multiplied by $10^2$) averaged over 1000 Monte
Carlo replications. Standard errors in parentheses. The proposed estimator
achieves the lowest MSE at all sample sizes, with the improvement growing
with $n$.}
\label{tab:mse}
\begin{tabular}{lcccc}
\toprule
Method   & $n = 200$ & $n = 500$ & $n = 1000$ & $n = 5000$ \\
\midrule
Proposed & \textbf{4.52} (0.31) & \textbf{1.23} (0.08) & \textbf{0.48} (0.03) & \textbf{0.09} (0.01) \\
Method A & 6.78 (0.45) & 2.15 (0.14) & 0.91 (0.06) & 0.21 (0.01) \\
Method B & 8.91 (0.52) & 3.42 (0.21) & 1.54 (0.10) & 0.38 (0.02) \\
Oracle   & 3.89 (0.27) & 1.05 (0.07) & 0.41 (0.03) & 0.08 (0.01) \\
\bottomrule
\end{tabular}
\end{table}
```

## Common Figure Problems and Fixes

| Problem | Fix |
|---------|-----|
| Title inside the figure | Remove and move content to caption |
| Legend overlapping data | Move outside the plot area or use direct labels |
| Title-case caption | Convert to sentence style with terminal period |
| Tiny fonts at journal size | Recompute font sizes at final figure size |
| Tick labels colliding | Reduce tick density or rotate labels 45 degrees |
| Caption requires the main text | Rewrite to be self-contained |
| Same color used for multiple methods | Use distinct hues with consistent encoding across all figures |
| Red and green together | Switch to a colorblind-safe palette |
| Estimates without uncertainty | Add CI bands, error bars, or posterior intervals |
| Raster output for line plots | Switch to PDF or EPS |
| Multi-panel figure without panel labels | Add (a), (b), (c) in top-left of each panel |
| Different axis ranges across comparable panels | Unify ranges so the visual comparison is direct |
| Violin plot built on small replication count | Replace with a box plot or strip plot |
| Broken y-axis | Use a log scale or split into two panels with consistent linear scales |
| Dual-y plot comparing two distinct quantities | Split into two panels or use one normalized scale |
| Inset legend in a tight-layout venue (e.g., Biometrika) | Move legend outside the panel or use direct labels |
| 3D plot, pie chart in body content | Replace with a 2D heatmap, contour plot, or horizontal bar chart |
| Pastel flat-vector "framework figure" | Remove or replace with a TikZ method diagram with minimal labels |
| AI-generated figure not disclosed | Add to the venue's AI disclosure block |

## Pre-Submission Figure Checklist

- [ ] No titles inside any figure
- [ ] Every figure has a self-contained caption
- [ ] Captions are sentence-style with terminal period (or venue equivalent)
- [ ] No title-case captions; no manual bold or italic inside captions
- [ ] Legends do not overlap data or extend beyond the plot area
- [ ] No inset legends if the target venue forbids them (Biometrika)
- [ ] Axis labels are concise and use main-text notation
- [ ] Tick density is reasonable (5 to 7 major ticks)
- [ ] Colorblind-safe palette
- [ ] Method encoding is consistent across all figures
- [ ] Vector format for line plots, 300+ dpi raster only when necessary
- [ ] Fonts are embedded in PDF outputs
- [ ] Font sizes are readable at journal column width
- [ ] Multi-panel figures have panel labels and unified axes when appropriate
- [ ] Uncertainty is shown for every estimate that matters
- [ ] No violin plots without sufficient replication count
- [ ] No broken axes, no dual-y axes (except deterministic transformations), no 3D plots, no pie charts
- [ ] Figure references in the text guide the reader to what to notice
- [ ] No figures depend on color alone for distinction (grayscale check)
- [ ] AI-generated figures are disclosed per venue policy
