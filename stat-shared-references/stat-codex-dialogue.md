# Codex Dialogue Discipline

Use this reference whenever a stat skill invokes Codex MCP for review. It applies to `stat-paper-plan` Step 7 Pass B, `stat-paper-write` Step 6 Pass B, `stat-paper-writing` Phase 5, and `stat-polishing` Step 11.

## The Principle

Codex review is a dialogue toward convergence, not a directive. The output of `mcp__codex__codex` is one senior reader's opinion at one point in time. It carries weight because the persona and reasoning budget are appropriate, but it is not authoritative.

The author has expert judgment Codex lacks: knowledge of the data, the proof technique, the experimental constraints, the field's recent moves, and what the paper actually demonstrates. The author also has skin in the game; Codex does not.

The job of the dialogue is to converge on what the paper needs, not to apply whatever Codex says.

## Three Outcomes for Each Codex Point

For every issue Codex raises, the author makes one of three decisions.

### Accept

The criticism is clearly correct. The fix is unambiguous. Apply it and move on.

Examples of clearly accept-worthy criticisms:
- A theorem statement omits an assumption that the proof actually uses.
- A figure has a title inside it that should move to the caption.
- A "first to" claim is contradicted by an actually-cited paper in the bibliography.
- An em-dash is being used to connect clauses.
- A page count exceeds the venue norm.

### Push back

The criticism is incorrect, partially correct, or based on a misunderstanding the author can resolve. Use `mcp__codex__codex-reply` with the same `threadId` to push back. Provide the context Codex lacked.

Examples of pushback:
- Codex says a rate is suboptimal because it does not match a paper Codex has in mind, but the cited paper actually works in a different setting.
- Codex suggests adding an experiment that has already been run and is in the supplement.
- Codex flags a "weaker assumptions" claim as overclaim, but Codex misread the comparison paper's assumption.
- Codex recommends a paper that the author has already cited under a different keyword.
- Codex's proposed replacement sentence introduces a technical inaccuracy.

Pushback prompt pattern:

```
mcp__codex__codex-reply:
  threadId: <from initial review>
  prompt: |
    On issue N: I disagree on this point. [State the disagreement.]

    Context Codex did not have:
    - [the missing context]
    - [the actual content of the comparison paper, with theorem
       statement and page reference]
    - [the existing experiment Codex did not see]

    Please reconsider in light of this. If you still think the
    issue stands, identify what specifically remains wrong; if
    you withdraw the criticism, say so.
```

After Codex replies, re-decide: accept, push back again, or log disagreement.

### Log disagreement

After a round or two of pushback, the author and Codex do not converge. The author still believes their position is correct; Codex still believes its criticism is correct. This is a legitimate outcome.

Record the disagreement in the review log with:
- The criticism Codex raised
- The author's position
- Why the author disagrees
- What evidence would resolve it (a specific reference, a specific calculation, a senior collaborator's opinion)

Do not silently drop unresolved disagreements. Surfacing them is the value.

## When Codex Is Most Likely To Be Wrong

Codex (or any LLM) is more likely to be wrong on these dimensions. Treat its criticism in these areas with extra skepticism.

| Area | Why Codex may be wrong |
|---|---|
| Very recent papers (last 6 months) | Training cutoff or limited memory of edge-of-cutoff work |
| Niche subfields | Less training signal; may project nearby-field intuition |
| Specific numerical constants in cited theorems | Hard to recall exactly |
| Author-attribution of specific results | Misattribution is common |
| The "first to" question in narrow technical areas | Hard to verify exhaustively |
| Proof technique novelty | Codex may not have read the closest technical reference |
| Application-domain norms | If Codex is not familiar with the specific domain |
| Verbatim quotations from cited papers | LLMs frequently paraphrase as if quoting |

When Codex cites a specific paper, theorem number, or numerical constant, verify it. Do not assume Codex is correct just because the format looks confident.

## When Codex Is Most Likely To Be Right

Equally, Codex is likely to be right on these dimensions. Pushback that contradicts these should be supported by specific evidence, not by reflex.

| Area | Why Codex is likely right |
|---|---|
| Detection of AI-template patterns in prose | Strong signal; Codex sees the same patterns |
| Detection of em-dashes, watchwords, hedge-stacking | Mechanical pattern matching |
| Vague positioning ("existing methods do not address" without naming any) | Easy to detect |
| Missing assumption in a theorem | Detectable from the proof structure |
| Caption that depends on the surrounding paragraph | Visible from the text |
| Generic field-background openings | Pattern-matched |
| Imbalance between sections (e.g., 1-paragraph data section in an application paper) | Easy to measure |
| Generic closing phrases | Easy to detect |

If the author wants to push back here, the burden of evidence is on the author.

## The Convergence Test

Stop iterating with Codex when one of the following holds.

1. Both sides agree on the substantive issues and the specific fixes.
2. Remaining disagreements have been documented with the author's reasoning, and the author is willing to defend the position to a reviewer.
3. The dialogue has reached diminishing returns (typically after 2 to 4 rounds).

Do not iterate indefinitely. The point is convergence, not unanimity.

## Documentation

Every Codex review should produce a written log saved alongside the project artifacts. Suggested file names:

- `PAPER_PLAN_REVIEW.md` for the planning-stage Codex pass
- `PAPER_DRAFT_REVIEW.md` for the drafting-stage Codex pass
- `POLISHING_REVIEW.md` for the polishing-stage Codex pass
- `PAPER_IMPROVEMENT_LOG.md` for the pipeline improvement loop

Each log should contain:

- The `threadId` for resumability
- The initial Codex review verbatim
- Round-by-round summary of pushback and Codex's replies
- The final list of accepted criticisms with applied fixes
- The final list of rejected criticisms with the author's reasoning
- Outstanding open issues, if any

When a reviewer challenges the paper after submission, this log is the response.

## Common Failure Modes of the Dialogue

| Failure mode | Diagnosis | Fix |
|---|---|---|
| Author accepts everything Codex says | Deference, not dialogue | Force a re-read of each criticism with the question "is this true?" before accepting |
| Author rejects everything Codex says | Defensive, not dialogue | The Codex pass is wasted; consider whether the project is at the right stage for external review |
| Codex review is single round, applied wholesale | Skipped the dialogue step entirely | Read the initial review carefully; use `mcp__codex__codex-reply` for at least one targeted follow-up before applying anything |
| Codex's suggested replacement sentences applied verbatim without checking | Codex is good at structure but can introduce technical inaccuracies | Read every proposed replacement; verify the technical claims before pasting |
| Disagreements not documented | The log is incomplete and cannot be used for rebuttal | Use the documentation template above for every dialogue |
| The author repeats the same pushback in three different rounds | Codex is not understanding; the author is not providing new context | Provide concrete evidence (theorem statement, page reference, prior result) rather than restating disagreement |

## The Role of the Author

The author is the editor of the dialogue, not its subject. Codex provides input; the author decides.

Three rules of thumb keep this honest:

1. Treat every Codex criticism the same way you would treat a real referee report: take it seriously, but evaluate it on its merits.
2. Where Codex's criticism aligns with a worry you had already, accept it without further dialogue.
3. Where Codex's criticism surprises you, slow down and check; the surprises are often the most valuable findings.

The goal is a paper that survives the actual referee process, not a paper that placates Codex.

## Cross-Reference

For specific Codex prompt templates, see:

- `stat-positioning-and-claims.md` for the positioning and technical claim strength audit prompt
- The individual skill files (`stat-paper-plan`, `stat-paper-write`, `stat-paper-writing`, `stat-polishing`) for the stage-specific review prompts

The dialogue discipline in this file applies to all of them.
