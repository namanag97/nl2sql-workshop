# Attendee pack — everything printed on the tables

Four sheets per table, black-and-white printable. Nothing here assumes SQL,
Databricks, or agent experience.

## Sheet 1 — Driving the AI (the PIRA cheat sheet)

> You never write SQL today. You **direct** the assistant and **judge** it.

1. **PROMPT** — paste the card's text exactly.
2. **INSPECT** — read the reply. Does it show what the card says under
   "you should see"?
3. **REACT** — if not, tell it *what's wrong in business words*:
   "cancelled orders must not count", "one row per order", "use the March
   snapshot". Then paste again.
4. **ANNOUNCE** — write the number on your scoresheet. Right or wrong, it's
   your number.

Roles: **Pilot** reads and decides · **Copilot** pastes. Swap every question.

## Sheet 2 — Glossary (Meridian Trading Co.)

| Term | Meaning |
|---|---|
| Order | A customer's request to buy; can be cancelled |
| Order line | One product within an order |
| Invoice | What we billed; issued days after the order |
| Return | Goods sent back; reduces revenue |
| Fiscal year | Feb 1 – Jan 31 (not the calendar year!) |
| Product line | Marketing grouping; a product may sit in 2 lines |
| Region | Sales territory; some reps sell in 2 regions |
| Active customer | ⚠ has two definitions in our systems — ask which |
| SCD2 / snapshot | The customer table keeps history; old rows are not wrong |

## Sheet 3 — The trap checklist (your take-home)

Ten questions to ask of **any** AI-generated data answer:

1. Which definition of the metric did it assume — and who owns that decision?
2. Which date field did it use (order, invoice, payment)?
3. Are cancelled/excluded rows actually excluded?
4. Could any join produce more rows than inputs (double counting)?
5. What grain is the answer at — and is the question at that grain?
6. Is time as-of-now or as-of-then (restatements)?
7. Is the entity resolved — could two codes be one customer?
8. What would this answer miss if data arrived late?
9. Can it cite its sources — tables, filters, metric version?
10. Would it say "I don't know" if it should? If not, don't trust it.

## Sheet 4 — Prompt cards

### C0 — Smoke test
```
List every table in schema o2c with its row count. Show as a table.
```
*You should see:* 16 table names, counts matching the handout.

### C0.5 — While you wait (setup stragglers get fixed)
```
Show me 5 cancelled orders: order id, date, and total line amount.
```
*You should see:* 5 rows. If you got 0, something is wrong — red card.

### C1 — Q1 · Total revenue
```
Using raw tables only (no views): what is total revenue across all orders,
all time? Sum the ORDER_LINES.line_amount column. Show the SQL you used
and the number.
```
*You should see:* a number + SQL. Compare with your envelope.

### C2 — Q2 · Monthly by line by region
```
Monthly revenue by product line by region, calendar year 2026, from raw
tables. Show the SQL. Then give me the GRAND TOTAL across the whole
result table as a single number.
```
*Watch for:* a grand total that looks too big (envelope will tell you).

### C3 — Q3 · Active customers March
```
How many active customers did we have in March 2026? State your definition.
```

### C4 — Q4 · Top 5 customers
```
Top 5 customers by all-time revenue, with their revenue.
```

### C5 — Q5 · Average order value
```
What is our average order value?
```

### C6 — Build the governed view (after filling D1–D3)
```
In OUR TEAM SCHEMA (o2c_team<N> — we cannot write to o2c), create a view
V_REVENUE_GOVERNED with these business rules:
[ ] exclude CANCELLED orders: YES/NO        (D1)
[ ] net of RETURNS: YES/NO                  (D2)
[ ] revenue date = ORDER_DATE / INVOICE_DATE (D3)
Grain: one row per order line, sourced from the o2c raw tables. Each row
must carry:
- the product's PRIMARY product line (PRODUCT_LINE_MAP is many-to-many;
  use is_primary = TRUE only)
- the order rep's PRIMARY region (REGION_ASSIGNMENT has two rows for some
  reps; use is_primary = TRUE only)
Add a comment block listing the rules. Then run it and show 5 sample rows.
```
*You should see:* "view created" + 5 rows, with line and region columns.
*When re-running C1/C2 later, read from `o2c_team<N>.V_REVENUE_GOVERNED`.*

### C7 — Teach the platform
```
In OUR TEAM SCHEMA (o2c_team<N>), save a note file listing the PRIMARY KEY
and FOREIGN KEY relationships of the o2c tables (orders→customers via
customer_xref, order_lines→orders, order_lines→products,
order_lines→product_line_map, orders→region_assignment), and write 3
example SQL queries a reporting agent should imitate (revenue, monthly
trend, top customers) using o2c_team<N>.V_REVENUE_GOVERNED.
```
*You should see:* the relationship list + 3 example queries.
*Worth knowing:* Databricks PK/FK constraints are **informational — they
are not enforced**. They teach the agent (and Catalog Explorer) where the
joins belong; the *view* is what actually protects the numbers. Declaration
≠ enforcement.

### C8 — The monster (multi-step)
```
Which region's gross margin dropped the most, quarter over quarter,
after the Feb 2026 returns policy change — and by how many points?
Show each step before the final answer.
```
*Expected:* it must decompose. If it answers in one shot, distrust it and
check against the sub-steps.

### D1–D3 — Decision menus (tick before C6)
These three ticks are your **declared decisions**. Whoever disagrees with
your numbers must disagree with a tick, not with you.

## Rerun-at-home recipe

1. Pick one metric your company argues about.
2. Write its definition as 3–5 tick boxes (like D1–D3).
3. Have your AI tool build ONE view implementing the ticks.
4. Re-run your three most-repeated reports against the view.
5. Keep the ticks in version control. That's a semantic layer seed.
