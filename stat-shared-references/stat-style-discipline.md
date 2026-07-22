# Style Discipline for Statistics Papers

Use this reference when writing, polishing, or auditing the prose of a statistics manuscript. The goal is prose that resembles the writing of senior statisticians who publish regularly in the Big Four journals (JASA, Annals of Statistics, JRSS-B, Biometrika), not prose that reads as AI-generated.

## When to Read

- Before drafting any section
- During the clarity pass after a first draft
- Before final submission
- When the user says the paper "reads like AI"
- When the user asks for COPSS-style or scholar-style polishing
- After any LLM-assisted writing pass

## Punctuation Discipline

Statistics papers in the Big Four use a relatively narrow set of punctuation. Each mark has a clear job.

### The Em-Dash Rule

Do not use em-dashes to connect clauses. The em-dash is the single most reliable AI tell in academic prose. Senior statisticians use em-dashes rarely, mostly for inline definitions or single-word interjections in informal writing. In manuscript prose, prefer commas, periods, or restructuring.

Bad (AI-shaped):
```
The estimator is consistent—even under heavy-tailed errors—and achieves the minimax rate.
```

Good:
```
The estimator is consistent under heavy-tailed errors and achieves the minimax rate.
```

Or:
```
The estimator is consistent. Heavy-tailed errors do not change the conclusion, and it still achieves the minimax rate.
```

If you have to use an em-dash, limit yourself to one per paper, and never use a pair of em-dashes around a parenthetical. Use commas or parentheses for that.

### The Colon Rule

**Colons are prohibited in body prose.** Split into two sentences instead. Prose colons are one of the top AI tells and add nothing a period cannot.

Permitted uses are limited to:
- Before a numbered or bulleted list, as in `the assumptions are: (A1) ..., (A2) ..., (A3) ...`
- Before a long quotation, rare in statistics
- After section labels in figure captions, as in `Figure 3: ...`
- In ratios, times, mathematical notation, and code

Any colon in body prose that does not match one of the four cases above must be split into two sentences.

Bad:
```
The result is striking: the estimator achieves the parametric rate even in the nonparametric setting.
```

Good:
```
The result is striking. The estimator achieves the parametric rate even in the nonparametric setting.
```

Or:
```
Strikingly, the estimator achieves the parametric rate even in the nonparametric setting.
```

Acceptable colon uses:
- Before a numbered or bulleted list
- Before a long quotation (rare in statistics)
- After section labels in figure captions: "Figure 3: ..."
- In ratios, times, and mathematical notation

### The Semicolon Rule

**Semicolons are prohibited in body prose.** Split into two sentences instead. Even the traditionally accepted "two closely related independent clauses" case reads as AI-shaped in current statistics prose. A period does the same work without the tell.

Permitted uses are limited to:
- Bibliographic citation clusters, as in `(Talagrand, 1996; van Handel, 2014)`
- Complex lists where the items themselves contain commas
- Code, mathematical notation, or LaTeX macros

Overused semicolon (rewrite):
```
The estimator is consistent; moreover, it is asymptotically normal; furthermore, it achieves the efficiency bound.
```

Rewrite to:
```
The estimator is consistent. It is asymptotically normal and achieves the efficiency bound.
```

### Quotation Marks

Use standard double quotation marks for direct quotation. Avoid scare quotes around technical terms. If a term needs definition, define it inline rather than quoting it. Italics on first use is the preferred convention.

### Parentheses

**Prose parentheses are prohibited.** Restructure the sentence or cut. A parenthetical is almost always evidence that the surrounding sentence tried to carry two ideas.

Permitted uses are limited to:
- Citations `(Author, Year)` and citation clusters
- Equation numbers `(1), (2), (3)` and equation-label references
- Assumption, condition, or step labels `(A1), (i), (a)`
- Standard acronym first-use, as in `MSE (mean squared error)`
- Short purely mathematical annotations, e.g., `(where $n = |D|$)`, provided the annotation is under about six words and carries a formula

Explanatory prose asides — "for example ...", "i.e., ...", "note that ..." — must be restructured into a full sentence or cut. Sentence-length parenthetical clauses are forbidden even when they contain useful content.

## Emphasis Formatting Discipline

**Manual bold, italics, underlining, small caps, color, boxed text, and display styling are prohibited in body prose.** If a point needs emphasis, rewrite the sentence or promote it structurally to a heading, theorem, remark, table, or figure. Emphasis-as-rhetoric is the strongest single AI tell in academic prose. A draft with three bolded sentences in the abstract and two italicized phrases in the introduction has already lost the senior-statistician voice before any other audit runs.

Permitted uses are limited to two:

1. Italics on the first defined use of a technical term, as in `the *propensity score* is defined as ...`. After the first use, plain text. Nothing else earns italics.
2. Bold for mathematical objects where the target journal's convention requires it, typically vectors and matrices at ASA journals. Never invented locally. Biometrika does not use bold vectors at all.

Everything else, including all rhetorical bold and italic, is prohibited. In particular, do not bold or italicize:
- Assumption labels, condition labels, theorem/lemma/corollary claim sentences
- Contribution list items, "key findings," "main result," or "our contribution" markers
- Figure captions and table titles — the class handles typography
- Sentences carrying rhetorical weight, e.g., "this is *crucial*", "we *strongly* emphasize"
- Any content in the abstract, introduction, or discussion, under any pretext

Theorem, lemma, proposition, corollary, definition, assumption, and remark headers typeset by `amsthm` or the journal's class do not count as manual emphasis. The class inserts them. Table column headers produced by the table code do not count either.

### What counts as journal-conventional

- Theorem, lemma, proposition, corollary, definition, assumption, and remark headers as styled by `amsthm` or the journal's class. These are typeset by the class. The author does not insert manual bold.
- Mathematical objects rendered in their canonical typeface: boldface for vectors and matrices when the venue uses that convention, calligraphic for sets, blackboard for number systems. Do not invent a new bold convention.
- Italics on the first defined use of a technical term, as in `the *propensity score* is defined as ...`. After the first use, plain text.
- Table column headers and panel labels when produced by the table or figure code, not by manual emphasis in the prose.

### What is banned regardless of venue

- Bolded sentences or phrases in the body, abstract, introduction, theorem statements, or discussion to convey importance.
- Italicized rhetorical phrases such as "this is *crucial*" or "we *strongly* emphasize".
- Manual bolding of contribution items, claim sentences, or "main result" labels.
- Color in body prose. Color belongs in figures, used for data, not for words.
- Underlining anywhere in the manuscript.
- Bolded text inside figure captions or table titles unless the journal class does it for you.

### Venue-specific notes

| Venue | Emphasis policy |
|---|---|
| Biometrika | Strictest. Verbal phrases in italic or bold are not used. Even vectors and matrices are not set in distinctive bold type by house convention. Use the class's defaults. Captions carry symbol descriptions in plain text. |
| Annals of Statistics | Avoid excessive italics and bold face. Theorem and remark headers are produced by the `imsart` class. Do not add manual bold. |
| JASA and other ASA journals | Italics for emphasis are used sparingly. Vectors and matrices are typeset in bold by ASA convention. |
| JRSS-B, JRSS-A, JRSS-C | Local macros and special formatting are discouraged. Theorem, caption, and heading formatting is left to the journal class. |
| AOAS, Bernoulli, EJS | Follow `imsart` defaults. Do not override with manual emphasis. |
| Biostatistics, JCGS | Class-driven formatting. Rhetorical emphasis is not part of the house voice. |

When in doubt, fall back to the strictest rule: no manual emphasis. The senior-statistician voice carries its own weight. It does not need typography to assert importance.

## AI-Template Patterns to Avoid

The following patterns appear with high frequency in LLM-generated academic prose. Remove them.

### Formulaic Section Openings

Do not start sections with templated meta-commentary.

Avoid:
- "In this section, we ..."
- "This section is organized as follows."
- "Here, we present ..."
- "We now turn to ..."
- "In what follows, ..."

Replace with the content itself. The reader knows they are at the start of a section.

### Empty Connectives

Avoid AI's favorite filler phrases:
- "It is worth noting that"
- "Importantly,"
- "Notably,"
- "Crucially,"
- "Interestingly,"
- "Significantly,"
- "Of particular note"
- "It should be noted that"
- "We emphasize that"

These phrases waste space and do not change the reader's behavior. If something is worth noting, write it. If something is important, the importance should be evident from the content.

### Padding Verbs and Nouns

Watch for these patterns:
- "perform an analysis of" → "analyze"
- "make use of" → "use"
- "in order to" → "to"
- "due to the fact that" → "because"
- "a number of" → "several" or a specific number
- "the majority of" → "most"
- "at this point in time" → "now"
- "the question of whether" → "whether"

### Vague Quantifiers

Replace with specific values when known:
- "extensive simulations" → "1000 Monte Carlo replications across 12 scenarios"
- "a wide range of settings" → "$n \in \{200, 500, 2000, 5000\}$ and $p \in \{20, 100, 500\}$"
- "many existing methods" → "the four methods in Table 2"
- "various applications" → name the applications

### Hedge Stacking

Avoid stacking multiple hedges:
- "may potentially suggest" → "suggests"
- "could possibly indicate" → "indicates"
- "might be able to" → "can"
- "appears to potentially" → "appears to"

Use a single hedge when uncertainty is genuine.

### Generic Conclusions

Avoid generic closing sentences:
- "This work opens exciting new avenues for future research."
- "We hope this work will inspire future investigations."
- "Our contributions push the frontier of ..."
- "This methodology has wide-ranging implications."

Replace with specific statements about what the work enables.

### AI Watchwords (Watchlist, Not Blacklist)

The following words appear with disproportionate frequency in LLM prose. Treat the list as a watchlist, not an automatic ban list. Many of these words have legitimate technical uses. Flag rhetorical uses and keep technically necessary ones.

- delve, delving, delve into
- pivotal, crucial, paramount, vital
- landscape, tapestry, realm
- underscore, underline, illuminate, elucidate
- unveil, unearth, uncover (when no veil or earth was present)
- noteworthy, remarkable, striking, intriguing
- intriguingly, fascinatingly, notably (as a decoration)
- foster, galvanize, harmonize, hone
- paradigm, paradigm shift, transformative
- robust (when no robustness is being tested)
- novel (when no novelty is being established)
- comprehensive (when no comprehensiveness is being demonstrated)
- nuanced, holistic (often vague)
- leveraging, leverage (when "use" works)
- in this paper, our work, our contribution (when redundant with section context)

For each candidate occurrence, ask three questions:

1. Does the word carry information that a reader could not infer from the surrounding sentence?
2. If the word were cut, would the sentence become weaker, or would it just shorten?
3. Is the word doing real technical work, as in `leveraging the asymptotic equivalence in Lemma 3`, or is it rhetorical decoration?

Keep when (1) or (3). Cut otherwise.

### Biometrika-Style House Bans

Biometrika and similar concise-prose venues enforce additional hard bans that are useful Big-Four-wide:

- "Note that" at the start of a sentence. Either the next clause is worth saying, in which case start with the content, or it is not, in which case cut. Replace `Note that the estimator is consistent.` with `The estimator is consistent.`
- "Is given by" in mathematical phrasing. Prefer the direct relation. `The estimator $\hat\theta$ is given by $\hat\theta = (X^\top X)^{-1} X^\top y$.` becomes `The estimator is $\hat\theta = (X^\top X)^{-1} X^\top y$.` or `Define $\hat\theta = (X^\top X)^{-1} X^\top y$.`
- Homemade method acronyms. Big Four journals, and Biometrika most aggressively, discourage acronyms for new methods. A method named `Doubly Robust Adaptive Kernel Estimator (DRAKE)` reads as ML-style branding, not statistics. Prefer a descriptive short name such as `the adaptive kernel estimator` or `the proposed estimator`, and let the formal definition do the work. Acronyms for standard objects such as MLE, MCMC, GLM, MSE, KL, and OLS are fine.
- Unnecessary abbreviations. Avoid in-text abbreviations like `w.r.t.`, `s.t.`, or `i.f.f.` in body prose. Spell them out as `with respect to`, `subject to`, or `if and only if`. Mathematical shorthand inside displayed equations is fine.
- "It can be shown that" without saying where it is shown. Either prove it now, cite a result by number, or remove the claim.
- "In this paper" / "In this work" repeated across sections. The reader knows where they are. Cut on sight in body sections. Use sparingly in the abstract and introduction if at all.

### Hyphenated Noun-Adjective Discipline

Reduce the habit of turning a noun into an attributive adjective by hyphenation. The productive offenders are the `-based`, `-driven`, `-type`, `-induced`, `-dependent`, `-wise`, `-specific` family, and stacked noun premodifiers. Default to a prepositional phrase or the plain noun. Use the hyphenated form only when it is an established term of art or the prepositional rewrite is genuinely clumsier.

The reason is concision and parse cost. A noun-rooted hyphenated adjective compresses a relation into a premodifier, which raises the reader's parse load, and stacks of them read as jargon density. Senior statisticians unpack the relation into a preposition or a verb, which the reader processes in order. This is the word-level analog of the figure rule "move information out of the title and into the caption". Move the relation out of the premodifier and into the sentence.

Reduce (rewrite by default):

| Premodifier | Prefer |
|---|---|
| "a kernel-based estimator" | "an estimator based on kernels", or "a kernel estimator" (standard, no hyphen needed) |
| "a likelihood-based test" | "a test based on the likelihood" |
| "a model-driven procedure" | "a procedure driven by the model" |
| "a tuning-parameter-dependent rate" | "a rate that depends on the tuning parameter" |
| "a simulation-based comparison" | "a comparison using simulation" |
| "a sparsity-induced bias" | "the bias induced by sparsity" |
| "a coordinate-wise update" | "an update over each coordinate" (or keep if standard in the optimization subfield) |
| stacked: "a high-dimensional sparse-regression-based variable-selection procedure" | "a procedure for variable selection in high-dimensional sparse regression" |

Keep the following established terms without rewriting: high-dimensional, finite-sample, large-sample, low-rank, closed-form, real-valued, second-order, worst-case, well-specified, sub-Gaussian, data-driven and model-based where they are the recognized term of art in the subfield. These are read as single lexical units, not as compressed relations.

Before keeping a hyphenated noun-adjective, ask whether it is a standard term the reader expects as one unit, or an ad-hoc nominal compression the author formed to save a few words. Keep the former. Unpack the latter, and unpack on sight when two or more stack before a single noun.

### The Rule-of-Three Tic

LLMs habitually produce three-item lists such as "X, Y, and Z." This becomes a tic when used reflexively. Vary list lengths. Single items, pairs, and quadruples are also valid. Cut items that are duplicative.

Avoid:
```
The method is fast, accurate, and scalable.
```

When all you have evidence for is speed and accuracy, write:
```
The method is fast and accurate.
```

### Excessive Topic Sentences

LLMs often begin every paragraph with a topic sentence that summarizes the paragraph. This is appropriate for some paragraphs but becomes formulaic when applied universally. Vary openings. Some paragraphs should begin with evidence or observation and build to the conclusion.

## Paragraph Discipline

### Length

Statistics papers favor longer paragraphs than ML conference papers. A paragraph of 4 to 8 sentences develops an argument. A one-sentence paragraph almost never belongs in a journal paper.

Avoid:
```
The estimator is consistent.

It is also asymptotically normal.

Furthermore, it achieves the efficiency bound.
```

Use:
```
The estimator is consistent. Under Assumption (A2), it is asymptotically normal at rate $\sqrt{n}$, and the limiting variance achieves the semiparametric efficiency bound of Bickel et al. (1993). The variance is estimable from the data, allowing standard inference.
```

### Internal Structure

Each paragraph should:
- Develop one main idea
- Move from old information to new information
- End on the point that matters most
- Connect to the surrounding paragraphs through content, not connective phrases

A paragraph that needs `Moreover`, `Furthermore`, and `In addition` to connect its sentences usually contains material that should be split or cut.

### Topic Sentence Variation

Not every paragraph needs a topic sentence. Some natural variations:

- Topic sentence first, support after: classical pattern
- Setup first, conclusion last: useful for argument paragraphs
- Question first, answer body: useful for transitions
- Observation first, explanation after: useful for results sections

## Bullet Point Discipline

Statistics papers use bullet points sparingly. Look at any recent JASA or AoS paper. Bullet points are rare outside contribution lists and assumption lists.

When bullets are appropriate:
- Listing 3 to 5 numbered contributions in the introduction
- Listing assumptions
- Listing items in a simulation study setup
- Listing components of an algorithm

When bullets are inappropriate:
- Inside continuous prose where prose would work
- For two-item lists (use a sentence)
- In the discussion to enumerate implications
- As substitutes for argument

Prefer prose by default. The natural unit of statistical writing is the paragraph, not the bullet.

### Contribution Lists

When using a contribution list in the introduction:
- Use a numbered list rather than bullets when there is a meaningful order
- Each contribution should be 1 to 3 lines
- Be specific and falsifiable
- 2 to 4 items, rarely more

```latex
\begin{enumerate}
\item We establish the minimax rate of convergence for estimating $f \in \mathcal{W}^{s,2}(L)$ in the heavy-tailed setting (Theorem~\ref{thm:upper}--\ref{thm:lower}).
\item We propose an estimator that achieves this rate adaptively, without knowledge of the smoothness $s$ (Section~\ref{sec:method}).
\item We verify the theoretical predictions in simulations and apply the method to [dataset], where we find [substantive result] (Section~\ref{sec:application}).
\end{enumerate}
```

## COPSS-Style Scholar Writing Patterns

COPSS Presidents' Award winners and similar senior statisticians write with characteristic patterns. Modeling these helps reduce AI-shaped prose.

### Confidence Without Hype

Senior statisticians make confident claims supported by precise evidence. They do not pile on adjectives.

Avoid:
```
Our remarkable and groundbreaking new estimator achieves unprecedented performance.
```

COPSS-style:
```
Our estimator achieves the minimax rate under weaker conditions than previously available.
```

### Plain Verbs

Prefer plain, active verbs:
- "we propose" rather than "we put forward"
- "we prove" rather than "we provide a rigorous demonstration that"
- "we show" rather than "we present results indicating"
- "the estimator achieves" rather than "the estimator is shown to attain"

### Active Voice, with Restraint

Use active voice for the paper's actions: "We propose," "We prove," "We show." Use passive voice when the agent does not matter: "The data were collected in 2018."

Avoid the AI passive: "It can be shown that ..." This is almost always weaker than naming the agent: "We show that ..." or just stating the result.

### Connective Restraint

Senior statisticians use connectives less than LLMs do. The argument flows through content, not through `However`, `Moreover`, `Furthermore`, `Additionally`, `In addition`, `On the other hand`.

When a connective is needed, prefer the shortest:
- "but" rather than "however"
- "so" or "thus" rather than "therefore" or "consequently"
- "and" rather than "moreover" or "furthermore"

`However` is acceptable at the start of a sentence when introducing genuine contrast. Avoid stacking multiple `However`s in nearby sentences.

### Mathematical Precision Over Adjectival Praise

Compare:

AI-shaped:
```
This is a powerful and elegant result, with far-reaching implications for the field.
```

COPSS-style:
```
This result extends the rate of Bickel and Levina (2008) from $p = O(n)$ to $p = O(n^2)$ under the same moment conditions.
```

The second sentence is specific, falsifiable, and tells the reader what to compare. The first sentence tells the reader to be impressed.

### Modesty With Precision

Senior statisticians are precise about what they have done and modest about what they have not. They tell the reader the boundaries clearly.

Example:
```
Theorem 1 establishes consistency under sub-Gaussian errors. We do not know whether the result extends to sub-exponential errors; the argument in Lemma 3 uses sub-Gaussianity at a critical step. We leave this as an open question.
```

This is stronger writing than either overclaiming or hedging without specifics.

### Sentence Rhythm

Vary sentence length. A paragraph of all short sentences feels choppy. A paragraph of all long sentences feels dense. Senior statisticians mix short, declarative sentences such as "This is the main result." with longer sentences that develop nuance.

A pattern that often works:
- Open with a medium-length sentence stating the point
- Follow with one or two longer sentences that develop it
- Close with a shorter sentence that lands the conclusion

### Reference Restraint in Math

When stating mathematical results, do not over-cite. Cite the predecessor whose result you are improving and the paper whose technique you are using. Do not cite five papers for a single concept.

Acceptable:
```
The argument follows the chaining technique of Talagrand (1996), adapted to handle the dependence in our setting.
```

Less acceptable:
```
The argument follows the chaining technique (Talagrand, 1996; van Handel, 2014; Vershynin, 2018; Wainwright, 2019), adapted to handle the dependence in our setting.
```

The reader can find the secondary references through Talagrand's paper.

## Section-Specific Style Notes

### Abstract

Senior statisticians' abstracts:
- Make a specific claim in the first sentence
- Include one quantitative result
- Avoid the words "novel," "groundbreaking," "comprehensive"
- Are short, often 150 to 200 words even when 250 is allowed
- End with the boundary or implication, not a generic platitude

### Introduction

Senior statisticians' introductions:
- Cite the problem's origin clearly (a foundational paper from decades ago is fine)
- Frame the gap as a specific technical question, not as a vague field-wide need
- State the contribution in plain language before stating it mathematically
- Avoid the AI introduction pattern of "Recent advances in X have led to Y"
- Use 2 to 4 contribution bullets, no more

### Method and Theory Sections

- State definitions before they are used, not interleaved with derivations
- State assumptions before stating theorems that use them
- After the theorem, write 1 to 2 paragraphs of prose discussing the rate, the constants, and the connection to prior work
- Do not bullet-point the implications of a theorem. Develop them in prose

### Simulation Sections

- Start with the design, not with meta-commentary
- Report results as observations, then interpret
- Use tables for primary numerical results, figures for patterns and convergence
- Honest about when the proposed method underperforms

### Discussion

- Statisticians' discussions are measured. No hype, no future-work platitudes
- Specific open problems with technical content
- Honest limitations stated as limitations, not buried in hedges
- No bullet-pointed implications

## How to Audit Your Own Prose

Run this checklist on any section:

- [ ] Read the section aloud. Where do you stumble?
- [ ] Count em-dashes. Cut all but at most one across the paper.
- [ ] Count body-prose colons. Zero permitted except before a list, in a figure/table label `Figure 3: ...`, or in math and code. Split every other colon into two sentences.
- [ ] Count body-prose semicolons. Zero permitted except in bibliographic citation clusters and in commas-within-items lists. Split every other semicolon into two sentences.
- [ ] Count body-prose parentheticals. Zero permitted except for citations, equation numbers, assumption/step labels, standard acronym first-use, and short mathematical annotations under about six words. Restructure or cut every other parenthetical.
- [ ] Count manual `\textbf{...}`, `\emph{...}`, and `\underline{...}` in body prose. Zero permitted except italics on first defined use of a technical term and venue-mandated bold for vectors and matrices. Everything else is cut, including bold on contribution items, "key findings," theorem-claim sentences, and abstract phrases.
- [ ] Count italic phrases used for emphasis rather than for term definition. Cut every one.
- [ ] Count "however," "moreover," "furthermore," "additionally." Cut the unnecessary ones.
- [ ] Look for "It is worth noting that," "Importantly,", "Notably,". Cut them all.
- [ ] Look for "Note that" at sentence start. Cut and rewrite.
- [ ] Look for "is given by". Replace with a direct relation or `Define ...`.
- [ ] Look for "delve," "pivotal," "landscape," "underscore," "unveil." Replace or cut.
- [ ] Look for rule-of-three lists. Are all three items pulling weight?
- [ ] Look for empty section openings. Replace with content.
- [ ] Look for homemade method acronyms. Replace with a descriptive short name.
- [ ] Look for in-text `w.r.t.`, `s.t.`, `i.f.f.`. Spell out in body prose.
- [ ] Look for `-based`, `-driven`, `-type`, `-induced`, `-dependent`, `-wise` premodifiers and stacked noun-adjectives. Unpack to a preposition or verb unless the term is standard. Unpack on sight when two or more stack before one noun.
- [ ] Check that every paragraph develops one idea.
- [ ] Check that bullets only appear in contribution lists, assumption lists, algorithm descriptions, and other places where bullets are genuinely appropriate.
- [ ] Check that each sentence either states a fact, makes an argument, or transitions. Cut sentences that do none of these.

## What Replaces AI Tics

When you cut AI tics, you have to put something in their place. Usually that something is content. If cutting "Importantly, X" leaves "X" and the reader does not appreciate that X is important, the answer is not to add back "Importantly,". The answer is to provide the evidence or context that makes X's importance visible.

This is why audit and revision often shorten a paper. AI-shaped prose hides thin content behind connective machinery. Once the connectives come out, the thinness becomes visible, and the writer either supplies the missing content or cuts the section.

## Final Note: Voice

The voice that comes out of these rules is a confident, plain, mathematical voice. It reads like a researcher who knows the result well and is telling you what they found and why it matters. It does not read like an enthusiastic but vague summary written by someone who has not done the work.

When the voice is right, the reader trusts the paper. When the voice is wrong, the reader doubts even sound results.
