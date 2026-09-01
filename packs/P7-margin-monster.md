# P7 — Margin after the policy change

*Handout for participants. Facilitator-only material is below the cut.*

**When you run it:** live day = **10-minute demo** (card C8: watch a one-shot
fail). Take-home lab = 45 min (decompose and land the envelope).
**Runs on:** raw or the team's view · **Cards:** C8

## The story

In February 2026 the returns policy changed. Leadership wants to know:
**which region's gross margin dropped the most, quarter over quarter —
and by how many points?** This question cannot be answered with one query.
It decomposes.

On the live day you are not expected to finish. The lesson is: demand the
sub-steps *before* you believe the answer.

## Your tasks (live demo)

1. Paste card **C8**. Before accepting the answer, demand the sub-steps:
   - what is the margin definition?
   - which quarters — calendar or fiscal?
   - which date identifies "after the policy change"?
2. If it answered in one shot, distrust it.

## Full lab (45 min)

1. Run each sub-step separately. Do the pieces agree with the final answer?
2. State your assumptions in the answer, exactly like an envelope would:
   margin = net − returns − COGS; cancelled out; calendar quarters; primary region.
3. This question secretly contains P1 (dates), P2 (fan-out), and P3 (which
   quarter). Name which trap bit you.

## React hints

- "Define gross margin before computing it: net revenue − returns − COGS."
- "Calendar quarters, not fiscal."
- "Show margin per region per quarter before ranking."

## Remember

Agents score poorly on multi-step data analysis. Your decomposition is the
product — not the one-shot number.

---

## FACILITATOR ONLY

- **Envelope:** `data/keys/envelopes/P7_envelope.txt`
- **Live day:** 10 minutes at S28. Cut it before you cut the P8 refusal beat.
  Nobody one-shots this; if an agent does, make the team verify each step.
- **Watch for:** fiscal quarters (Feb start, QK-07) get a different winner —
  a register mismatch, not an error. Grade the declaration, then the number.
- **Stretch (not the room):** package the three sub-queries as a failing
  regression test against the raw schema — first eval case.
- **Debrief:** "Multi-step is where agents break. The decomposition is the product."
- **Quirks:** QK-02, QK-03, QK-05 (primary); QK-06, QK-15 (secondary).
