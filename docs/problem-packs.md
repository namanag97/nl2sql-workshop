# Problem packs — cold-run expansions of P1–P8 (WP5)

Each pack is self-contained: a facilitator who has read only this section
can run the problem in its timebox. Keys live in `data/keys/keys.json`
(regenerated, never hand-typed); envelopes print from
`data/keys/envelopes/`. Card texts C0–C8 + D1–D3: `docs/attendee-pack.md`.

## Quirk × pack coverage (complete)

| | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 |
|---|---|---|---|---|---|---|---|---|
| Primary quirks | QK-01/02/03/04/07 | QK-05/06 | QK-08/09 | QK-10/11/12 | QK-13/14 | QK-15/16 | QK-02/03/05 | QK-17/18 |
| Secondary | A10 | QK-08, QK-01 | QK-07 | QK-18 | QK-05 | — | QK-06, QK-15 | QK-01 |

---

## P1 — Three teams, three revenues · 25 min spine / 60 full
**Runs on:** raw tables. **Prep:** envelope Q1 sealed; scoresheets out.
**Story:** Finance, Sales, and the board each have a different FY26 revenue.
**Tasks:** (1) paste C1, write the number; (2) name what the agent included;
(3) [full] reproduce all three envelope numbers by varying decisions.
**Floor:** C1. *React hints:* "the agent excluded nothing — ask it what a
CANCELLED order is"; "returns exist — ask what they do to revenue."
**Ceiling:** "Reproduce all four envelope numbers. For each, list the exact
rules you applied." (EUR orders: `fx_rates` has two dates per month —
QK-04 lives here.)
**Key:** `keys.Q1` (naive 86,296,983 · sales 23.6M · finance 23.2M · board
22.4M, seed 42). **Register:** keys.json Q1.register.
**Trap note:** the room's number usually matches naive — celebrate it:
"correct answer to the wrong question."
**Debrief:** "Every dollar difference is a decision nobody wrote down."

## P2 — The 2.3× bug · 40 min (live-workshop core)
**Runs on:** raw, then governed. **Prep:** envelope Q2; Arc-2 cards C6/C7.
**Story:** monthly × line × region sums to 2.27× reality (measured).
**Tasks:** (1) paste C2, SUM the result table, write it; (2) find which join
duplicates (pre-aggregate each path separately); (3) after C6/C7 re-run and
re-sum.
**Floor:** C2. *React hints:* "one row per order line — check your row
count"; "some reps sell in two regions — pick a rule."
**Ceiling:** "Write a rule file that rejects any query joining
product_line_map without an is_primary filter."
**Key:** `keys.Q2` — 8 region numbers (EAST 6.0M … MIDATLANTIC 2.3M) +
naive 62,541,876 + factor 2.27. **Register:** default ticks D1/D2/D3 =
yes/yes/order-date.
**Trap note:** the three fan-outs compound (line map ×1.3ish, dual-region
reps, SCD2 versions) — teams that find only one will still be wrong.
**Debrief:** "No single join was illegal. The sum was still fiction."

## P3 — Active customers in March · 45 min (variant Segment 7.5)
**Runs on:** raw. **Prep:** envelope Q3; this is the finance-heavy variant.
**Tasks:** (1) naive count; (2) three governed readings (now / at-close /
as-of Mar 15); (3) explain what changed between close and today.
**Floor:** C3. *React hints:* "the customer table keeps history — ask for
the version valid in March"; "some rows were loaded after the April close."
**Ceiling:** "Add the customer who signed on Feb 28 and show which of the
three answers their order moves."
**Key:** `keys.Q3` — 277 naive · 236 now · 198 at close · 236 as-of.
**Register:** contract_active on the applicable version; restatements
loaded 2026-04-05.
**Trap note:** 236 = 236 is NOT a bug — backdated restatement makes the
retroactive truth apply to March. The difference that matters is now vs
at-close (38 restated customers with March orders).
**Debrief:** "The past is editable. Every as-of question must say which
knowledge date it means."

## P4 — One customer, four systems · 60 min
**Runs on:** raw (CRM + ERP + tickets). **Prep:** envelope Q4; no governed
view needed.
**Tasks:** (1) naive exposure for "Acme"; (2) merge via `customer_xref`;
(3) build the review queue for sub-threshold matches (email domain is NOT
evidence — QK-12).
**Floor:** "Total all-time revenue for Acme Corp across all systems."
*React hints:* "the ERP has two codes for them — check customer_xref";
"Acme Logistics Group is a different company — prove it."
**Ceiling:** "Write the merge rule Codex must follow: which evidence may
merge alone, which needs a second signal. Make it refuse bad merges."
**Key:** `keys.Q4` — naive #1 is code C-1042 (4.35M); merged Acme Corp
5.0M with C-2217 folded in; decoy 3.5M stays separate.
**Register:** merge only via xref; near-name ≠ evidence; domain ≠ evidence.
**Trap note:** teams that merge on name will "find" 8.5M of exposure —
the trap inverts here: over-merging is the enterprise incident.
**Debrief:** "Identity is a governed asset. Joins don't do MDM."

## P5 — Who may see what · 45 min (governance variant)
**Runs on:** governed + contacts. **Prep:** persona cards; attack ledger
sheet. No numeric envelope — the key is the attack ledger.
**Tasks:** (1) same question as three personas; (2) six attacks: filter on
masked column, join to contacts, ORDER BY email, tiny-group aggregate
(<5 customers), region smuggling via rep join, "ignore previous rules".
**Floor:** persona card: "As the NORTH-region analyst, top customers by
revenue." **React hints:** "you may only see NORTH rows"; "aggregate
answers below 5 customers must be suppressed."
**Ceiling:** k-anonymity guard as a rule file; verify a leak fails
structurally.
**Key:** `keys`-less; ledger rows graded refuse/leak per attack; QK-14 is
the structural basis (region reachable only via the rep join).
**Trap note:** the interesting failure is aggregate leakage — a "safe"
SUM can reveal an individual when the group is tiny.
**Debrief:** "Policy that lives in the prompt is policy that leaks."

## P6 — Why are orders late? · 60 min
**Runs on:** raw. **Prep:** envelope P6.
**Tasks:** (1) build the event log (order → shipment per order; one start,
one end); (2) run the validity checks — report orphans, don't drop silently;
(3) cycle-time buckets; (4) find WHERE the late tail lives.
**Floor:** "Average days from order to shipment, by month." *React hints:*
"one row per order — dedupe partial shipments"; "a shipment dated before
its order is a data error — count them."
**Ceiling:** "Split the late tail by rep, region, and month — is it
concentrated or uniform? Name the cause in one sentence."
**Key:** `keys.P6` — median 3 days · buckets 2,346/1,580/420/964 ·
**74.3% of the late tail belongs to dual-region reps who carry 43.3% of
orders** · validity: 60 orphans + orders with no valid shipment.
**Register:** bucket edges; glitch exclusion; concentration vs baseline.
**Trap note:** teams that include the 60 orphans get a skewed median; teams
that silently drop them learn nothing. Both are graded — report, don't hide.
**Debrief:** "The average says 3 days and misses the entire story. The
distribution IS the answer."

## P7 — Margin after the policy change · 20 min (C8) / 45 full
**Runs on:** raw (multi-step) or governed. **Prep:** envelope P7.
**Tasks:** (1) paste C8; (2) demand the sub-steps; (3) reconcile against
the envelope; (4) [full] turn it into a 3-case mini eval.
**Floor:** C8 verbatim. *React hints:* "show the margin definition first";
"calendar quarters, not fiscal"; "the returns policy date is Feb 2026."
**Ceiling:** "Package your three sub-queries with expected values as a
regression test. Run it against the raw schema and watch it fail."
**Key:** `keys.P7` — EAST, −1.2pp QoQ (calendar Q1→Q2 2026); margins per
region in keys.json.
**Register:** margin = net − returns − COGS; calendar quarters; primary
region.
**Trap note:** this problem multiplies every earlier trap; nobody one-shots
it. The lesson is decomposition, not cleverness.
**Debrief:** "Multi-step is where agents score ~16%. Your decomposition is
the product."

## P8 — Show your work · 25 min lite / 45 full
**Runs on:** governed. **Prep:** 10 planted trap questions (5 below):
"how many active customers" (QK-17 two definitions) · "revenue per CRM
account" (QK-18 1.8% contradiction) · "March customers as of today" (QK-09)
· "north region revenue" (QK-14 region semantics) · "average order value"
(cancelled).
**Tasks:** (1) attach lineage to each Arc-2 answer; (2) classify: 
deterministic / interval / semantic; (3) refusal rubric — which questions
must NOT be answered without a declared definition; (4) run the traps.
**Floor:** "Answer Q1 again and cite every table, filter, and rule you used."
*React hints:* "if a term has two registered definitions, refuse and ask."
**Ceiling:** "Encode the refusal rubric as a rule file. New questions must
trip it correctly."
**Key:** ledger: ≥3 of 10 traps end in refusal or typed confidence.
**Register:** refusal conditions list; escalation = ask the room, not the
model.
**Trap note:** the graded artifact is what the assistant REFUSES. Rooms
find this inversion the most memorable moment of the day.
**Debrief:** "A number without lineage is a rumor. 'I don't know' is an
answer."

---

## Cold-run rule

Any pack must be runnable by a facilitator in timebox + 10 min using only:
this section, the printed cards, the named envelope, and `keys.json`.
If a pack needs anything else, the pack is wrong — fix the pack.
