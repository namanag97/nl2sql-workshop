# P2 — The 2.3× bug

*Handout for participants. Facilitator-only material is below the cut.*

**When you run it:** this *is* the live-workshop core (Arc 1 diagnosis + Arc 2 fix)
**Timebox:** 40 min · **Runs on:** raw, then the team's view
**Cards:** C2 (floor), D1–D3 ticks, C6 + C7 (the fix)

## The story

Someone asked for "monthly revenue by product line by region" and the grand
total came out **more than double** reality. Every join in the query is
individually defensible. Find which joins duplicate rows, declare the rules,
and make the number land.

There are **eight** regions. The envelope has all eight plus the grand total.

## Your tasks

1. Paste card **C2** (it asks for the grand total too). Write it on the scoresheet.
2. Attack each join path separately: ask the agent to count rows at each step
   (order lines → products → line map → region). Where does the row count explode?
3. Fill in your **D1–D3** ticks, then paste **C6** — the agent builds the view
   in *your team schema* (you cannot write to `o2c`).
4. Re-run the same question against `o2c_team<N>.V_REVENUE_GOVERNED`.
   New grand total → scoresheet Arc 2.

## React hints

- "One row per order line — check your row counts before summing."
- "Some reps sell in TWO regions — pick one rule and declare it."
- "Some products sit in TWO product lines — same thing."

## Remember

The fan-outs compound: find one and you're still wrong. The Teams thread in
**Documents** is this exact fight — sales-ops vs finance — with the real numbers.

---

## FACILITATOR ONLY

- **Envelope:** `data/keys/envelopes/Q2_envelope.txt` (8 regions, not 6).
- **The three compounding duplications:** line map (primary-only), dual-region
  reps (QK-06), customer-history rows. Teams that fix one will still be off.
- **Watch for:** ticks other than the default (D1 yes / D2 yes / D3 order-date)
  — their governed total won't match the envelope. That's the lesson: declared ≠ default.
- **Stretch (not the room):** a rule that rejects joining `product_line_map`
  without `is_primary`. Engineer homework.
- **Debrief:** "No single join was illegal. The sum was still fiction."
- **Quirks:** QK-05, QK-06 (primary); QK-08, QK-01 (secondary).
