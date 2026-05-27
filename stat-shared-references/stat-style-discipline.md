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

Reduce colon use. A colon is appropriate for a list ("the assumptions are: (A1) ..., (A2) ..., (A3) ...") or for introducing a numbered structure. It is not appropriate as a stylistic flourish between two clauses.

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

Reduce semicolon use. The semicolon is acceptable when joining two closely related independent clauses, but it is overused in AI-generated text. When in doubt, split into two sentences.

Acceptable semicolon use:
- Joining two short, parallel clauses that share a subject: "The bias decreases with $n$; the variance decreases more slowly."
- In a complex list where items themselves contain commas

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

Use parentheses sparingly. Long parenthetical remarks should usually be sentences in their own right or be cut. A parenthetical citation is fine; a parenthetical clause longer than five words is usually a sign the sentence needs restructuring.

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

### AI Watchwords

The following words appear with disproportionate frequency in LLM prose. Use them only when necessary, and never as decoration:
- delve, delving
- pivotal, crucial, paramount
- landscape, tapestry, realm
- underscore, illuminate, elucidate
- noteworthy, remarkable, striking
- intriguingly, fascinatingly
- robust (when no robustness is being tested)
- novel (when no novelty is being established)
- comprehensive (when no comprehensiveness is being demonstrated)
- nuanced (often vague)
- holistic
- leveraging, leverage

When you find these words, ask whether they carry information. If not, cut.

### The Rule-of-Three Tic

LLMs habitually produce three-item lists: "X, Y, and Z." This becomes a tic when used reflexively. Vary list lengths. Single items, pairs, and quadruples are also valid. Cut items that are duplicative.

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

Statistics papers favor longer paragraphs than ML conference papers. A paragraph of 4 to 8 sentences develops an argument; a one-sentence paragraph almost never belongs in a journal paper.

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

Statistics papers use bullet points sparingly. Look at any recent JASA or AoS paper: bullet points are rare outside contribution lists and assumption lists.

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
- Use a numbered list (1, 2, 3, 4) rather than bullets when there is a meaningful order
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

Vary sentence length. A paragraph of all short sentences feels choppy; a paragraph of all long sentences feels dense. Senior statisticians mix short, declarative sentences ("This is the main result.") with longer sentences that develop nuance.

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
- Are short (often 150 to 200 words even when 250 is allowed)
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
- Do not bullet-point the implications of a theorem; develop them in prose

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
- [ ] Count em-dashes. Cut all but at most one.
- [ ] Count colons. Keep only those introducing lists.
- [ ] Count semicolons. Convert most to periods.
- [ ] Count "however," "moreover," "furthermore," "additionally." Cut the unnecessary ones.
- [ ] Look for "It is worth noting that," "Importantly,", "Notably,". Cut them all.
- [ ] Look for "delve," "pivotal," "landscape," "underscore." Replace or cut.
- [ ] Look for rule-of-three lists. Are all three items pulling weight?
- [ ] Look for empty section openings. Replace with content.
- [ ] Check that every paragraph develops one idea.
- [ ] Check that bullets only appear in contribution lists, assumption lists, algorithm descriptions, and other places where bullets are genuinely appropriate.
- [ ] Check that each sentence either states a fact, makes an argument, or transitions. Cut sentences that do none of these.

## What Replaces AI Tics

When you cut AI tics, you have to put something in their place. Usually that something is content. If cutting "Importantly, X" leaves "X" and the reader does not appreciate that X is important, the answer is not to add back "Importantly,". The answer is to provide the evidence or context that makes X's importance visible.

This is why audit and revision often shorten a paper. AI-shaped prose hides thin content behind connective machinery. Once the connectives come out, the thinness becomes visible, and the writer either supplies the missing content or cuts the section.

## Final Note: Voice

The voice that comes out of these rules is a confident, plain, mathematical voice. It reads like a researcher who knows the result well and is telling you what they found and why it matters. It does not read like an enthusiastic but vague summary written by someone who has not done the work.

When the voice is right, the reader trusts the paper. When the voice is wrong, the reader doubts even sound results.
