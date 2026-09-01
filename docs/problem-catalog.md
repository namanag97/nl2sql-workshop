# Problem catalog — P1–P8

Live workshop uses **P1+P2 (as Q1–Q5 spine) and P8-lite (Arc 3)**.
P3–P7 are the extended catalog for the 180-min variant, full-day formats, and
self-serve labs. Every problem follows the same contract:

> **Statement** (the business story) · **Planted quirks** (`QK-xx`, see
> `data/README.md`) · **Tasks** · **Floor** (paste-and-run prompt) ·
> **Ceiling** (extension for strong attendees) · **Key** (numeric, sealed) ·
> **Register** (declared decisions behind the key) · **Timebox**.

Key format (all problems): one number or a short ordered list of
numbers/names — DABstep-style, auto-gradable. Every key ships with its
register; a team matching the number must also be able to name the decisions.

---

## P1 — Three teams, three revenues
- **Axes:** A1 semantic · A6 evidence · A9 platform · (secondary A3, A10)
- **Statement:** Finance, Sales, and the board deck each report a different
  FY26 net revenue from the same warehouse (envelope Q1 holds the three
  numbers). Which is "right"?
- **Planted quirks:** `QK-01` cancelled orders included · `QK-02` returns not
  excluded · `QK-03` order-date vs invoice-date recognition · `QK-04` FX rate
  date variant · `QK-07` fiscal year starts Feb 1.
- **Tasks:** reproduce the three numbers; catalog the definitional decisions;
  write the register that reproduces each.
- **Floor:** `C1` — "Total revenue, all time, from raw tables."
- **Ceiling:** have Codex emit the decision register as a table; flip each
  decision and confirm the three board numbers fall out.
- **Key:** 3 numbers + per-number decision tuple.
- **Timebox:** 25 min (spine) / 60 min (extended).

## P2 — The 2.3× bug (grain & fan-out)
- **Axes:** A2 grain · A9 platform · (A1, A4, A6, A10)
- **Statement:** "Monthly revenue by product line by region" sums to 2.3×
  reality. Every join is individually defensible.
- **Planted quirks:** `QK-05` product↔line many-to-many with validity dates ·
  `QK-06` overlapping region assignments (a rep sells in 2 regions).
- **Tasks:** find the fan-outs by pre-aggregating each join path; fix with
  correct-grain selection; write lint rules that would have caught each.
- **Floor:** `C2` — the innocent question verbatim.
- **Ceiling:** write the "query plan lint" as a Codex rule file; make it
  reject the naive query before it runs.
- **Key:** corrected monthly revenue table (6 numbers) + the fan-out factor.
- **Timebox:** 40 min (spine core).

## P3 — Active customers in March (time & bitemporality)
- **Axes:** A3 time · A10 quality · (A1, A6)
- **Statement:** The customer dim is SCD2 and rows are restated after close.
  "How many active customers in March?" has three defensible answers.
- **Planted quirks:** `QK-08` SCD2 dimension · `QK-09` post-close restatement
  · `QK-07` fiscal calendar.
- **Tasks:** produce as-known-now, as-known-at-close, and as-of-an-arbitrary-
  date answers; avoid the SCD2 join fan-out; state which is "the audited one."
- **Floor:** "Count active customers in March 2026."
- **Ceiling:** add a late-arriving customer record and show which answer
  changes (transaction-time vs valid-time).
- **Key:** 3 numbers, one per semantics.
- **Timebox:** 45 min (extended variant).

## P4 — One customer, four systems (identity)
- **Axes:** A4 identity · A6 evidence · (A2, A8)
- **Statement:** "Total exposure to Acme Corp." — CRM has 1 account, ERP has
  2 codes, support matches on email domain, a near-named subsidiary lurks.
- **Planted quirks:** `QK-10` two ERP codes for one legal entity · `QK-11`
  decoy near-name subsidiary · `QK-12` shared email domain (not evidence).
- **Tasks:** deterministic match pass (exact → normalized → scored fuzzy);
  canonical ID map with per-match evidence; exposure answer + review queue
  for below-threshold matches.
- **Floor:** "Total revenue for Acme Corp across all systems."
- **Ceiling:** define the refusal rule: which evidence may never merge
  alone? Make Codex enforce it.
- **Key:** exposure number + merge list with match classes.
- **Timebox:** 60 min (extended).

## P5 — Who may see what (policy-aware answering)
- **Axes:** A5 authority · A6 evidence · (A9)
- **Statement:** Three personas (regional analyst, controller, support agent)
  ask the same questions. Row-level region restriction, masked contact/PII
  columns, aggregates-only on one table.
- **Planted quirks:** `QK-13` PII-ish contact table · `QK-14` region-restricted
  fact rows.
- **Tasks:** express policies declaratively; generate policy-scoped answers
  per persona; then attack: 6 prompt attempts to leak cross-region rows or
  raw PII (filters, joins, ORDER BY masked column, tiny-group aggregates).
- **Floor:** persona card + "answer the same question as each persona."
- **Ceiling:** k-anonymity guard: suppress groups < 5; verify the leak fails
  *structurally*, not because the model behaved.
- **Key:** per-persona answer triple + attack ledger (6 rows: leak y/n).
- **Timebox:** 45 min (180-min variant Segment 7.5).

## P6 — Why are orders late? (events & sequences)
- **Axes:** A7 process · A8 multi-step · (A1, A3, A6)
- **Statement:** Aggregates can't answer "why late." Needs an event log built
  from orders/invoices/shipments, cycle-time distributions, delay variants.
- **Planted quirks:** `QK-15` shipment events out of order · `QK-16` orphan
  events (no order match) — log validity check must catch.
- **Tasks:** build the event log; validity checks (one start/end per order);
  top delay variants; one cohort comparison; "what we can and cannot claim"
  (diagnostic vs causal).
- **Floor:** "Average days from order to shipment, by month."
- **Ceiling:** variant analysis: top 3 delay patterns with counts.
- **Key:** median cycle time + top variant name.
- **Timebox:** 60 min (extended).

## P7 — Margin after the returns policy change (multi-step composition)
- **Axes:** A8 multi-step · A10 quality · (A1, A3, A9)
- **Statement:** DABstep-style: "Which region's gross margin dropped the most
  quarter-over-quarter after the Feb 2026 returns policy change, and by how
  many points?" Requires policy-date lookup, two quarters, joins, and a
  judgment call on margin definition.
- **Planted quirks:** `QK-03` date semantics · `QK-02` returns · `QK-05`
  fan-out — composition multiplies every earlier trap.
- **Tasks:** decompose into sub-queries; sequence them; reconcile; state
  assumptions in the answer.
- **Floor:** card `C8` verbatim (the monster).
- **Ceiling:** turn the answer into a 3-question mini eval with expected
  values; run it against the raw setup and watch it fail.
- **Key:** region name + delta in points.
- **Timebox:** 20 min (Arc 3) / 45 min (extended).

## P8 — Show your work (evidence, uncertainty, refusal)
- **Axes:** A6 evidence · (A5, A8)
- **Statement:** The assistant ships to a skeptical CFO. Every answer needs
  lineage (tables, filters, metric version), typed uncertainty, and honest
  refusal conditions.
- **Planted quirks:** `QK-17` ambiguous term ("active") with two registered
  definitions · `QK-18` cross-source contradiction (CRM vs ERP totals).
- **Tasks:** attach lineage to each answer from Arc 2; classify answers by
  uncertainty type (deterministic / interval / semantic); define refusal
  conditions and an escalation path; run 10 planted trap questions — ≥3 must
  end in refusal or typed-confidence, not confident SQL.
- **Floor:** "Answer Q1 again and cite every table and filter you used."
- **Ceiling:** refusal rubric as a Codex rule file; new questions must trip
  it correctly.
- **Key:** ledger of 10 questions × (answer type, refused?, lineage depth).
- **Timebox:** 25 min lite (Arc 3 evidence harvest) / 45 min full.
