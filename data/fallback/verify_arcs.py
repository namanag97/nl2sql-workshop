#!/usr/bin/env python3
"""Wargame the MAGIC MOMENT against real data (no LLM involved).

Builds V_REVENUE_GOVERNED in a team schema EXACTLY as card C6 instructs
(default ticks D1=yes, D2=yes, D3=order-date, primary line + region
columns), then re-runs the Arc-2 questions the way an attendee would and
compares against keys.json.

If this passes, any correct execution of C6 lands on the envelope numbers;
only model-quirk risk remains for the live rehearsal (watch-item W1).

Usage:  .venv/bin/python data/fallback/verify_arcs.py
"""
import json
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
DB = Path(__file__).resolve().parent / "meridian.duckdb"

# The view exactly as C6 describes it (default tick set).
VIEW_SQL = """
CREATE OR REPLACE VIEW o2c_team1.V_REVENUE_GOVERNED AS
SELECT
  o.order_id,
  o.order_date                                   AS revenue_date,
  plm.line_name                                  AS line_name,
  ra.region_name                                 AS region_name,
  l.qty,
  l.line_amount - COALESCE(r.return_amount, 0)   AS net_amount
FROM o2c.orders o
JOIN o2c.order_lines l USING (order_id)
JOIN o2c.product_line_map plm
  ON plm.product_id = l.product_id AND plm.is_primary = TRUE
JOIN o2c.region_assignment ra
  ON ra.rep_id = o.sales_rep_id AND ra.is_primary = TRUE
LEFT JOIN o2c.returns r ON r.line_id = l.line_id
WHERE o.status != 'CANCELLED'
"""

# Attendee re-runs against the view, mirroring cards C1'/C2'/C5'.
CHECKS = {
    "Q1' governed revenue (all time)":
        ("SELECT SUM(net_amount) FROM o2c_team1.V_REVENUE_GOVERNED", None),
    "Q2' governed by region H1-2026":
        ("""SELECT region_name, SUM(net_amount) FROM o2c_team1.V_REVENUE_GOVERNED
            WHERE revenue_date BETWEEN '2026-01-01' AND '2026-06-30'
            GROUP BY region_name ORDER BY region_name""",
         "Q2.governed_net_revenue_h1_2026_by_region"),
    "Q5' governed AOV (revenue / orders)":
        ("""SELECT CAST(SUM(net_amount) / COUNT(DISTINCT order_id) AS BIGINT)
            FROM o2c_team1.V_REVENUE_GOVERNED""",
         "Q5.governed_aov_non_cancelled"),
}


def main():
    keys = json.loads((ROOT / "data" / "keys" / "keys.json").read_text())
    con = duckdb.connect(str(DB))
    con.execute(VIEW_SQL)

    fails = 0
    for name, (sql, key_path) in CHECKS.items():
        got = con.execute(sql).fetchall()
        if name.startswith("Q1'"):
            # governed all-time total = naive MINUS cancelled minus returns;
            # compare against naive minus booked-ish delta is wrong — compute
            # expected from Q2 window semantics instead: full-history total.
            exp = con.execute(
                "SELECT SUM(l.line_amount - COALESCE(r.return_amount, 0)) "
                "FROM o2c.order_lines l JOIN o2c.orders o USING(order_id) "
                "LEFT JOIN o2c.returns r ON r.line_id = l.line_id "
                "WHERE o.status != 'CANCELLED'").fetchone()[0]
            ok = got[0][0] == exp
            fails += 0 if ok else 1
            print(f"{'PASS' if ok else 'FAIL'}  {name}: view={got[0][0]:,} expected={exp:,}")
        elif isinstance(key_path, str) and key_path.endswith("_by_region"):
            q, field = key_path.split(".", 1)
            exp = keys[q][field]
            got_map = {r: v for r, v in got}
            ok = got_map == exp
            fails += 0 if ok else 1
            print(f"{'PASS' if ok else 'FAIL'}  {name}: "
                  f"{'all 8 regions match envelope' if ok else (got_map, exp)}")
        else:
            q, field = key_path.split(".", 1)
            exp = keys[q][field]
            ok = got[0][0] == exp
            fails += 0 if ok else 1
            print(f"{'PASS' if ok else 'FAIL'}  {name}: view={got[0][0]:,} envelope={exp:,}")

    print("\nMAGIC MOMENT:", "PROVEN — C6 instructions reproduce the envelope"
          if not fails else f"{fails} CHECK(S) FAILED")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
