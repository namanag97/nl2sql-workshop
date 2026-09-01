#!/usr/bin/env python3
"""Assemble the rerun-at-home kit (W5) into kit/.

Acceptance (WP7): a machine that never saw Databricks can run card C0/C1
offline against the bundled DuckDB file.

Usage:  .venv/bin/python scripts/build_kit.py
Output: kit/  (gitignored; distribute as a zip)
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "kit"
KIT.mkdir(exist_ok=True)

shutil.copy(ROOT / "data" / "fallback" / "meridian.duckdb",
            KIT / "meridian.duckdb")

(KIT / "CARDS.md").write_text("""# Prompt cards — offline edition

Your data file: **meridian.duckdb** (schema `o2c`, 16 tables — same estate
you used in the workshop). Point your AI tool (Codex, Claude, Cursor) at
the file, or use the duckdb CLI directly.

### C0 — Smoke
```
List every table in schema o2c with its row count.
```
Expect 16 tables, 2,640 customers / 4,833 orders / 16,874 order lines.

### C1 — Total revenue
```
Sum ORDER_LINES.line_amount across all orders, all time. Show the SQL.
```

### C2 — The fan-out
```
Monthly revenue by product line by region, calendar year 2026, from raw
tables. Give the GRAND TOTAL too.
```
(Governed answer: 27,496,555. If you get ~62.5M, you reproduced the bug.)

### C6 — Govern it (one file, no permissions needed)
```
Create a view V_REVENUE_GOVERNED: exclude CANCELLED, net of RETURNS,
revenue date = order date, grain = one row per order line, carrying the
product's PRIMARY line and the rep's PRIMARY region. Show 5 sample rows.
```

### C8 — The monster
```
Which region's gross margin dropped the most, quarter over quarter, after
the Feb 2026 returns policy change — and by how many points? Show each
step.
```
""")

(KIT / "CHECKLIST.md").write_text("""# The 10-question trap checklist

1. Which definition of the metric did it assume — and who owns the decision?
2. Which date field (order, invoice, payment)?
3. Are cancelled/excluded rows actually excluded?
4. Could any join produce more rows than inputs?
5. What grain is the answer at — and is the question at that grain?
6. Is time as-of-now or as-of-then?
7. Is the entity resolved — two codes, one customer?
8. What would change if data arrived late?
9. Can it cite its sources — tables, filters, rule version?
10. Would it say "I don't know" if it should?
""")

(KIT / "RECIPE.md").write_text("""# Steal this at work — the one-page recipe

1. Pick one metric your teams argue about.
2. Write its definition as 3-5 tick boxes (like D1-D3: returns in/out,
   cancelled in/out, which date, which grain, which region rule).
3. Have your AI tool build ONE view implementing the ticks, with the rules
   in a comment block.
4. Re-run your three most-repeated reports against the view.
5. Put the ticks in version control. That is the seed of a semantic layer.
""")

(KIT / "README.md").write_text("""# Rerun-at-home kit

Offline copy of the workshop estate. No Databricks account needed.

- `meridian.duckdb` — the data (schema `o2c`)
- `CARDS.md` — prompt cards
- `CHECKLIST.md` — the take-home trap checklist
- `RECIPE.md` — the Monday-morning recipe

Run it: install Python, `pip install duckdb`, then `python3 -c "import
duckdb; print(duckdb.connect('meridian.duckdb', read_only=True).execute(
'SELECT COUNT(*) FROM o2c.orders').fetchone())"` — expect (4833,).
Or just point your AI coding tool at this folder and paste the cards.
""")

print("kit assembled:", " ".join(p.name for p in sorted(KIT.iterdir())))
