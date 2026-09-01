# P4 — One customer, four systems

*Handout for participants. Facilitator-only material is below the cut.*

**When you run it:** take-home lab (60 min). On the live day, card **C4** is
only "top 5 customers" — a 3-minute taste, not this identity hunt.
**Runs on:** raw (CRM + ERP xref + support tickets) · **Cards:** none printed —
ask in business words, PIRA always.

## The story

Leadership asks: **"What's our total exposure to Acme Corp?"** The CRM has
one account. The ERP has — check `CUSTOMER_XREF` — more than one code. The
support system matches companies by email domain. And somewhere in the
customer table there is an *Acme Logistics Group* that nobody is sure about.

The second ERP code is the **small tail**. It will not show up in a "top 5
by code" list. You have to go looking in the cross-reference table.

## Your tasks

1. Ask the agent for Acme's total revenue. Write the number. Then ask it
   to show **which codes/names** it included.
2. Merge codes only through `CUSTOMER_XREF`. Re-ask. New number.
3. Decide: is *Acme Logistics Group* the same company? What evidence would
   convince you? What evidence should **never** be enough on its own?
4. Build the review queue: matches below your evidence threshold go to a
   human list, not into the total.

## React hints

- "The ERP has two codes for this customer — check customer_xref. The second
  one is small; it will not be in the top 5."
- "Acme Logistics Group is a different name — prove it's different (or the
  same) before merging."
- "12 different companies share one email domain — a shared domain is not
  evidence."

## Remember

Identity is a governed asset. Joins don't resolve who a customer is.

---

## FACILITATOR ONLY

- **Envelope:** `data/keys/envelopes/Q4_envelope.txt` (includes Acme's two
  ERP codes; C-2217 is the tail, not in naive top 5).
- **Live day:** C4 = top 5 by code. This pack is the lab that explains why
  the top 5 is still wrong after Arc 2.
- **Trap inverts:** over-merging by name (Corp + Logistics Group) is the
  incident, not the miss. Shared-domain matches (QK-12) go to the review
  queue, never the total.
- **Stretch (not the room):** a merge rule the agent must refuse, not guess.
- **Debrief:** "Identity is a governed asset. Joins don't do that job."
- **Quirks:** QK-10, QK-11, QK-12 (primary); QK-18 (secondary).
