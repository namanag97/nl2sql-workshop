# P1 — You got 86 million. Finance got 23.

*Handout for participants. Facilitator-only material is below the cut —
remove before printing for attendees, or print `packs/participant/` instead.*

**When you run it:** live day = 25 min (card **C1** only) · take-home lab = 60 min
**Runs on:** raw tables · **Cards:** C1 · **Documents:** CFO email + wiki

## The story

Paste card **C1**. You will get a number near **86 million**. Finance's sealed
FY26 number is about **23 million** — invoice-date, net of returns, cancelled
orders out. Same warehouse. Nobody is lying.

Your job in 25 minutes: name the *decisions* that make the gap. Then open
**Documents**. The CFO's email and the wiki disagree. Who wins?

## Your tasks (live 25 min)

1. Paste card **C1**. Write the number on the scoresheet.
2. Inspect the SQL. Name one thing it counted that the **CFO's email** would not.
3. Open **Documents**. CFO vs wiki — who wins, and what would you tell the board?

## Full lab (60 min) — take-home / extra hour only

The three FY26 registers are *not* the live opening. Reproduce them by changing
one decision at a time:

- **Sales:** cancelled out, order-date, gross of returns, FY26 (starts Feb 1)
- **Finance:** cancelled out, invoice-date, net of returns, FY26
- **Board:** finance rules + US (USD) orders only

For each, list the exact rules. EUR orders exist: `FX_RATES` has **two** rate
dates per month — which one did you use, and what would the other change?

## React hints (what to say to the agent when something looks off)

- "Cancelled orders exist — should they count as revenue?"
- "Customers sent things back — where are returns in your number?"
- "Invoices are dated days after orders — which date is 'the' date?"

## Remember

PIRA: Prompt → Inspect → React → Announce. A number without its rules is a rumor.

---

## FACILITATOR ONLY — do not print for attendees

- **Envelope (source of truth — never retype):** `data/keys/envelopes/Q1_envelope.txt`
- **Live beat:** C1 is all-time `SUM(line_amount)`. Celebrate the naive match:
  "correct SQL, wrong question." Then point at finance's FY26 line in the envelope.
- **Watch for:** a team landing on the *booked* (invoice) number — different
  decision, not an error; the envelope covers it.
- **Do not** ask the room to reproduce Sales/Finance/Board in 25 minutes.
- **Debrief:** "Every dollar of the gap is a decision nobody wrote down."
- **Quirks:** QK-01, QK-02, QK-03, QK-04, QK-07.
