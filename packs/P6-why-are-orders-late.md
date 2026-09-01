# P6 — Why are orders late?

*Handout for participants. Facilitator-only material is below the cut.*

**When you run it:** take-home lab (60 min). Not on the 150-min spine.
**Runs on:** raw tables · **Cards:** none printed — build the log in business words.

## The story

Someone in ops says "we ship in about three days" and the room shrugs: that
doesn't match the complaints. The *average* is hiding the story. Build the
order-to-shipment event log, check it, and find out **where the lateness
actually lives**.

The cause you are looking for is a cousin of the 2× bug: some reps cover
**two regions**. You already met that shape in P2. Here it shows up as delay,
not as a multiplied total.

## Your tasks

1. Build the event log: for each order, the earliest shipment with a
   `ship_date` **on or after** the order date. One start, one end.
2. **Validity checks before any averages:**
   - how many shipments reference an order that doesn't exist?
   - how many orders have *no* valid shipment?
   Report them. Don't silently drop them.
3. Bucket the cycle times: on-time ≤3d · standard 4–7d · late 8–14d ·
   stalled >14d.
4. Now the real question: **is the late tail spread evenly, or concentrated?**
   Split late + stalled orders by rep, region, month. Name the cause in one
   sentence. (If your sentence is "the biggest bucket is on-time," you have
   described the average, not the complaints.)

## React hints

- "One row per order — partial shipments must not duplicate it."
- "A shipment dated BEFORE its order is a data error — count them first."
- "Show me the late orders grouped by sales rep."
- "Do dual-region reps show up more in the late tail than in all orders?"

## Remember

Report what you excluded. Silent drops are how data lies politely.
Averages answer nothing. The distribution plus a validity ledger answer.

---

## FACILITATOR ONLY

- **Envelope:** `data/keys/envelopes/P6_envelope.txt`
  (median is **4** days, not 3; cause = dual-region reps / QK-06, not `on_time`).
- **Watch for:** teams that include the orphans skew the median; teams that
  silently drop invalid shipments learn nothing. Grade the *reported* validity ledger.
- **The cause sentence:** "Late orders concentrate on reps who hold two
  overlapping regions — territory overlap, not randomness." Same quirk as P2.
- **Stretch (not the room):** does the concentration survive median vs mean,
  and after dropping glitches?
- **Debrief:** "Ops quoted 'about 3 days' and missed the entire story.
  The distribution IS the answer."
- **Quirks:** QK-15, QK-16 (primary); QK-06 gives the cause.
