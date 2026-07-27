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

## Checklist when adding capability

1. Does it change the state machine (routing, invariants, terminal states)? If no, it does not belong in the hot body.
2. Deterministic check → script. Fixed list/table → rule data or reference. Example/prompt/specimen → reference.
3. Leave a one-line pointer plus the hard gate inline.
4. Re-check both budgets after the edit. If the prefix crossed ~250 or the total crossed ~800, extract before committing.
