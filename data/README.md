# Dataset — "Meridian Trading Co." order-to-cash estate

Fictional mid-size distributor. One story, 16 tables, ~50k fact rows.
Everything attendee-facing uses **business table names** and whole numbers.

## Schema (catalog `nl2sql_ws`, schema `o2c`)

Row counts below are the **actual** manifest (seed 42, scale 1.0).

| Table | Rows | Purpose / traps |
|---|---|---|
| `CUSTOMERS` | 2,640 | 2,000 entities; `QK-08` SCD2 (+600 versions), `QK-09` restatements (+40) |
| `ACCOUNTS_CRM` | 2,000 | CRM view; `QK-18` totals overstate ERP booked by 1.8% |
| `CUSTOMER_XREF` | 1,901 | ERP codes; `QK-10` Acme Corp holds two codes |
| `PRODUCTS` | 400 | |
| `PRODUCT_LINE_MAP` | 480 | `QK-05` 80 products in 2 lines (validity-dated, M:N) |
| `REGIONS` | 8 | |
| `REGION_ASSIGNMENT` | 26 | `QK-06` 6 reps hold a second region |
| `ORDERS` | 4,833 | `QK-01` 6% cancelled (big orders), `QK-03` date lag |
| `ORDER_LINES` | 16,874 | amounts in whole dollars; `unit_cost` feeds P7 margin |
| `INVOICES` | 4,528 | `QK-03` 12% lag ~9 days; 30 late-arriving loads |
| `PAYMENTS` | 4,528 | |
| `SHIPMENTS` | 5,368 | `QK-15` backdated events, `QK-16` 60 orphans |
| `RETURNS` | 380 | `QK-02` naive revenue ignores them |
| `SUPPORT_TICKETS` | 6,000 | `QK-12` 12 companies share `@consultinghub.io` |
| `CUSTOMER_CONTACTS` | 2,100 | `QK-13` PII-ish surface for P5 |
| `FX_RATES` | 36 | 2 rate dates/month (QK-04), Feb 2025–Jul 2026 |

Measured teaching values (see `keys/keys.json`): naive Q2 fan-out factor
**2.25×** (story: ~2.3×), ERP booked ≈ $76M, Q5 AOV gap ≈ $1,500,
Q3 restatement delta 236-now vs 198-at-close.

## Planted-quirk register (the heart of the dataset)

Every quirk is planted **deliberately, at a documented rate**, and provable
via `data/keys/quirk_checks.sql`. Coverage: quirk → axis → primary problem.

| Quirk | What is planted | Axis | Problem |
|---|---|---|---|
| `QK-01` | 6% of ORDERS have status `CANCELLED` but non-zero amounts | A1/A10 | P1 |
| `QK-02` | RETURNS table, 380 rows; naive revenue ignores them | A1 | P1, P7 |
| `QK-03` | Invoice date ≠ order date for 12% (median +9 days, straddles month-end) | A3 | P1, P7 |
| `QK-04` | 3% FX-denominated orders; two rate dates available | A1 | P1 ceiling |
| `QK-05` | Product↔line M:N; 20% of products in 2 lines, validity-dated | A2 | P2, P7 |
| `QK-06` | 6 reps assigned to 2 regions | A2 | P2 |
| `QK-07` | Fiscal year starts Feb 1 | A3 | P1, P3 |
| `QK-08` | CUSTOMERS is SCD2 (type 2) | A3 | P3 |
| `QK-09` | 40 customer rows restated post-close (March audit) | A3/A10 | P3 |
| `QK-10` | One legal entity has 2 ERP codes (84% / 16% revenue split) | A4 | P4 |
| `QK-11` | Decoy subsidiary "Acme Logistics Group" (unrelated) | A4 | P4 |
| `QK-12` | 12 companies share one email domain (job-board spam) | A4 | P4 |
| `QK-13` | CUSTOMER_CONTACTS holds names + emails | A5 | P5 |
| `QK-14` | Facts carry region codes reachable only via a restricted join | A5 | P5 |
| `QK-15` | 4% of SHIPMENTS logged with earlier event-date than a later status | A7 | P6 |
| `QK-16` | 60 shipment rows reference missing orders | A7/A10 | P6 |
| `QK-17` | "Active" has two registered definitions (purchasing / contract) | A1/A6 | P8 |
| `QK-18` | CRM total ≠ ERP total by 1.8% (pipeline-vs-booked semantics) | A6 | P8 |

## Generation rules

1. Deterministic: fixed RNG seed, committed with the repo; same seed → same
   CSVs byte-for-byte.
2. Round to whole units everywhere; no floats in attendee-visible outputs.
3. Each quirk has a named generation parameter (rate, seed-offset) so WP5 can
   tune difficulty without redesigning.
4. Keys are **computed, never typed**: `data/keys/compute_keys.py` derives
   every number from the CSVs and emits `keys.json` with registers.
5. Scale knob: `SCALE=1` default (numbers above); `SCALE=0.2` for rehearsal.

## Why one estate

P1–P8 all read the same tables — attendees build familiarity once, and every
new problem *compounds* earlier quirks (P7 = P1+P2+P3 stacked). That mirrors
enterprise reality: the traps interact.
