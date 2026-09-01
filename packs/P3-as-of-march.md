# P3 — Active customers in March

*Handout for participants. Facilitator-only material is below the cut.*

**When you run it:** take-home / 180-min lab (45 min). On the live day, card
**C3** is only a 3-minute taste — you will not finish this pack in Arc 1.
**Runs on:** raw tables · **Cards:** C3 · **Documents:** wiki "active customer"
vs the CFO's postscript about restatements

## The story

March closed in April. Since then, some customer records were **edited
retroactively**. So: how many active customers did we have in March?
Depending on when you ask — and which version of history you trust — the
answer moves.

The customer table keeps history. Old rows are not wrong.

## Your tasks

1. Paste card **C3**. Write the number *and* the definition the agent used.
2. Ask for three readings:
   - **as known now** — using today's customer records;
   - **as known at close** — using only what was loaded before 2026-04-02;
   - **as of March 15** — the version of each customer valid on that date.
3. Explain in one sentence: *what changed between close and today?*

If two of the three readings come back **the same**, that is not a bug —
say *why* they match before you assume you failed.

## React hints

- "The CUSTOMERS table keeps history — use the version valid in March."
- "Some rows were loaded after the close — check the loaded_at column."
- "State which definition of 'active' you are applying."

## Remember

The past is editable. Every "as of" question must say which **knowledge
date** it means.

---

## FACILITATOR ONLY

- **Envelope:** `data/keys/envelopes/Q3_envelope.txt`
- **Live day:** C3 is an appetizer. Do not try to teach bitemporality in 3 minutes.
  Residuals after Arc 2 are the sell for this lab.
- **236 = 236 is not a bug:** restatements are backdated, so today's truth
  *applies* to March. The reveal-worthy delta is now vs at-close.
- **Trap:** teams may find 38 ≠ 40 and think they failed — two restated
  customers have no ERP code (they cannot order). Good catch, not an error.
- **Stretch (not the room):** add a Feb 28 signup and show which of the three
  answers move.
- **Debrief:** "The past is editable. Say which knowledge date you mean."
- **Quirks:** QK-08, QK-09 (primary); QK-07 (secondary).
