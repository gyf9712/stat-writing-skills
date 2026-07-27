# Skill Maintenance Rules

Skills are markdown instruction files an LLM loads and follows. The failure mode of a
long `SKILL.md` is **priority distortion**: the model runs the first ~200 lines as hard
law and treats the rest as downweighted suggestions, so mid-file checklists get ignored.
These rules keep the skills short where it counts and stop them from re-growing.

## Two budgets

- **Hot prefix ≤ 200-250 lines** (the execution budget). The first ~200 lines must contain
  the true skill: routing, invariants, the core state machine, hard gates, and the compact
  output contract. After any edit, the prefix alone should read like the whole skill.
- **Total ≤ 700-800 lines** (the maintenance budget). Above this needs an explicit written
  justification in the file. Long tails rot, drift, and invite re-inline creep.

The prefix is the execution budget; total length is the maintenance budget. Optimize the
prefix hardest.

## The growth rule

**A `SKILL.md` may grow only when the core state machine changes** (routing, invariants,
terminal states). Everything else goes somewhere else:

- deterministic check → a tested script in `stat-shared-references/scripts/`
- fixed table / list / taxonomy / catalog / venue tier → rule data (a `*_rules.py` module) or a reference `.md`
- worked example / prompt block / filled artifact specimen → a companion reference or template

Operational limit: **no new capability may add more than ~15 hot-body lines** unless it
changes routing, invariants, or terminal states. Otherwise it ships outside the skill and
the skill keeps only a one-line pointer plus the hard gate.

## Specimen vs contract

Keep inline the **compact empty contract** — the section order and typed field names that
define the skill's terminal states and its downstream handoff. Move out the **filled
specimen**.

Keep inline if:
- omitting it would make the terminal states ambiguous, or
- the exact section / field names are consumed by a checker or a downstream skill, or
- the skill must emit the artifact correctly without loading anything else.

Push out if it is only an illustration, a style example, a filled mock artifact, a prompt
block, or a convenience template whose fields are named elsewhere.

One inline contract per artifact family, ≤ 40-60 lines. Past that, contract and example are
mixed again.

## Do not over-cut

After extraction, the skill must still contain the whole control logic and be readable
**without** opening companion files unless a specific detail is needed. A skill that becomes
"go read five references" has been over-cut. The hot file keeps the control logic; the
references hold the detail.

## Acceptance testing a rewritten skill

A script has unit tests; a restructured judgment skill has none, so "it reads better"
and a smaller line count are not evidence that a rewrite worked. Use this instead.

1. **Build a small realistic fixture** per route the skill supports (e.g. one AUDIT
   input with existing work, one DESIGN input with none).
2. **Write an `EXPECT.md`** per fixture: the expected route, the expected per-item
   states, the elements that must appear, and the forbidden failures.
3. **Run the skill in a fresh context** (a subagent that reads only the installed
   `SKILL.md` and the fixture) three times per fixture. Fresh context matters: it tests
   the file, not your memory of what you meant.
4. **Check each output mechanically** with a checker script, and read one by hand for
   what the script cannot judge.
5. **Pass = at least 2 of 3 runs satisfy every hard assertion, with no forbidden
   failure in any run.**

Two lessons from the first real use of this method, both worth expecting:

- **The checker will have false positives.** Its first version flagged `PASS` / `FAIL`
  appearing anywhere, which fired on the skill's own `| Criterion | Status |` contract.
  A term banned as an *item state* is often legitimate elsewhere; scope the assertion to
  where the state actually lives. Add a regression test for each false positive.
- **A run failing for a real reason is the point.** A DESIGN run omitted two adequacy
  dimensions the prose required, because the *contract template* had no field for them.
  Stating a requirement in one section does not enforce it; the template the model fills
  in is what gets followed. Fix the template, then re-run.

Also lint the skill file itself for control characters. Writing `\theta` inside a
non-raw Python string turns it into a TAB — this happened twice during one session.

## Checklist when adding capability

1. Does it change the state machine (routing, invariants, terminal states)? If no, it does not belong in the hot body.
2. Deterministic check → script. Fixed list/table → rule data or reference. Example/prompt/specimen → reference.
3. Leave a one-line pointer plus the hard gate inline.
4. Re-check both budgets after the edit. If the prefix crossed ~250 or the total crossed ~800, extract before committing.
