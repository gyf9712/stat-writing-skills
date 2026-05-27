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
| Tiny fonts at journal size | Recompute font sizes at final figure size |
| Tick labels colliding | Reduce tick density or rotate labels 45 degrees |
| Caption requires the main text | Rewrite to be self-contained |
| Same color used for multiple methods | Use distinct hues with consistent encoding across all figures |
| Red and green together | Switch to a colorblind-safe palette |
| Estimates without uncertainty | Add CI bands, error bars, or posterior intervals |
| Raster output for line plots | Switch to PDF or EPS |
| Multi-panel figure without panel labels | Add (a), (b), (c) in top-left of each panel |
| Different axis ranges across comparable panels | Unify ranges so the visual comparison is direct |

## Pre-Submission Figure Checklist

- [ ] No titles inside any figure
- [ ] Every figure has a self-contained caption
- [ ] Legends do not overlap data or extend beyond the plot area
- [ ] Axis labels are concise and use main-text notation
- [ ] Tick density is reasonable (5 to 7 major ticks)
- [ ] Colorblind-safe palette
- [ ] Method encoding is consistent across all figures
- [ ] Vector format for line plots, 300+ dpi raster only when necessary
- [ ] Fonts are embedded in PDF outputs
- [ ] Font sizes are readable at journal column width
- [ ] Multi-panel figures have panel labels and unified axes when appropriate
- [ ] Uncertainty is shown for every estimate that matters
- [ ] Figure references in the text guide the reader to what to notice
- [ ] No figures depend on color alone for distinction (grayscale check)
