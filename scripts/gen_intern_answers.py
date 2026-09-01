#!/usr/bin/env python3
"""Generate the 'intern answers' outage deck (W3): printed agent outputs,
each plausible, several wrong — handed to teams only if the live model dies.
Teams grade them against their envelopes exactly as they would live output.

Each TABLE gets a different variant so reveals stay interesting.

Usage:  .venv/bin/python scripts/gen_intern_answers.py
Output: assets/print/intern-answers.md
"""
import duckdb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "print" / "intern-answers.md"

con = duckdb.connect(str(ROOT / "data" / "fallback" / "meridian.duckdb"),
                     read_only=True)
con.execute("SET search_path = o2c")  # unqualified names resolve to o2c


def one(sql):
    return con.execute(sql).fetchone()[0]


VARIANTS = {
    "A": {
        "C1": ("SELECT SUM(line_amount) FROM order_lines",
               "naive — every line, cancelled in, returns ignored"),
        "C3": ("SELECT COUNT(DISTINCT customer_code) FROM orders "
               "WHERE order_date BETWEEN '2026-03-01' AND '2026-03-31'",
               "distinct ordering accounts — no contract definition applied"),
    },
    "B": {
        "C1": ("SELECT SUM(invoice_amount) FROM invoices",
               "booked revenue — cancelled orders never invoiced"),
        "C3": ("SELECT COUNT(*) FROM customers WHERE contract_active "
               "AND is_current", "current active contracts — no March scope"),
    },
}
C2 = ("SELECT SUM(l.line_amount) FROM order_lines l "
      "JOIN orders o USING(order_id) "
      "JOIN customer_xref x ON x.erp_code = o.customer_code "
      "JOIN customers c ON c.customer_id = x.customer_id "
      "JOIN product_line_map plm ON plm.product_id = l.product_id "
      "JOIN region_assignment ra ON ra.rep_id = o.sales_rep_id "
      "WHERE o.status != 'CANCELLED' "
      "AND o.order_date BETWEEN '2026-01-01' AND '2026-06-30'",
      "joined everything — no grain discipline")
C4 = ("SELECT customer_code, SUM(line_amount) v FROM order_lines "
      "JOIN orders USING(order_id) GROUP BY customer_code "
      "ORDER BY v DESC LIMIT 1",
      "top customer by ERP code — identity not resolved")
C5 = ("SELECT CAST(SUM(line_amount) / COUNT(DISTINCT order_id) AS BIGINT) "
      "FROM order_lines JOIN orders USING(order_id)",
      "every order incl. cancelled, gross of returns")

rows = []
for table, variant in (("Table 1/2", "A"), ("Table 3/4", "B"),
                       ("Table 5/6", "A")):
    v = VARIANTS[variant]
    rows.append({
        "table": table,
        "c1_num": one(v["C1"][0]), "c1_note": v["C1"][1],
        "c2_num": one(C2[0]), "c2_note": C2[1],
        "c3_num": one(v["C3"][0]), "c3_note": v["C3"][1],
        "c4_num": one(C4[0]), "c4_note": C4[1],
        "c5_num": one(C5[0]), "c5_note": C5[1],
    })

parts = ["""# INTERN ANSWERS — outage deck (facilitator only)

If the live model dies room-wide, hand each table ITS printed output and
run the agenda unchanged: teams still Inspect, React (on paper: "what rule
did this intern miss?"), and Announce. Grading is identical.

## Table outputs
"""]
for r in rows:
    parts.append(f"""### {r['table']}
**C1 revenue** — {r['c1_num']:,}
The intern's basis: *{r['c1_note']}*

**C2 grand total (H1 2026)** — {r['c2_num']:,}
The intern's basis: *{r['c2_note']}*

**C3 active customers, March** — {r['c3_num']:,}
The intern's basis: *{r['c3_note']}*

**C4 top customer** — {r['c4_num']}
The intern's basis: *{r['c4_note']}*

**C5 AOV** — {r['c5_num']:,}
The intern's basis: *{r['c5_note']}*
""")
OUT.write_text("\n".join(parts))
print(f"written: {OUT.relative_to(ROOT)}")
