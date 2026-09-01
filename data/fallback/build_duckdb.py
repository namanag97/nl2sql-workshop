#!/usr/bin/env python3
"""Build the offline fallback database (o2c.duckdb) from the generated CSVs
and PROVE parity with keys.json (WP4 acceptance: identical keys offline).

Usage:  .venv/bin/python data/fallback/build_duckdb.py
Output: data/fallback/o2c.duckdb  (gitignored; regenerate any time)
"""
import csv
import json
import sqlite3  # noqa: F401  (parity diffs against keys.json, not sqlite)
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "out"
DB = Path(__file__).resolve().parent / "meridian.duckdb"  # catalog must not share the schema's name

BOOL_TABLES = {
    "customers": ("contract_active", "is_current"),
    "customer_xref": ("is_primary",),
    "product_line_map": ("is_primary",),
    "region_assignment": ("is_primary",),
    "shipments": ("is_partial",),
}

# Same numbers as compute_keys.py, DuckDB dialect (booleans as TRUE).
PARITY_QUERIES = {
    "Q1.naive_all_time_everything":
        "SELECT SUM(line_amount) FROM o2c.order_lines",
    "Q1.finance_fy26_net_invoice_date":
        """SELECT SUM(l.line_amount) - COALESCE(SUM(r.return_amount), 0)
           FROM o2c.invoices i JOIN o2c.orders o USING(order_id)
           JOIN o2c.order_lines l USING(order_id)
           LEFT JOIN o2c.returns r ON r.line_id = l.line_id
           WHERE o.status != 'CANCELLED'
             AND i.invoice_date >= '2026-02-01' AND i.invoice_date <= '2026-06-30'""",
    "Q2.correct_total":
        """SELECT SUM(l.line_amount - COALESCE(r.return_amount, 0))
           FROM o2c.order_lines l JOIN o2c.orders o USING(order_id)
           JOIN o2c.region_assignment ra
             ON ra.rep_id = o.sales_rep_id AND ra.is_primary = TRUE
           LEFT JOIN o2c.returns r ON r.line_id = l.line_id
           WHERE o.status != 'CANCELLED'
             AND o.order_date BETWEEN '2026-01-01' AND '2026-06-30'""",
    "Q2.naive_fanout_total":
        """SELECT SUM(l.line_amount) FROM o2c.order_lines l
           JOIN o2c.orders o USING(order_id)
           JOIN o2c.customer_xref x ON x.erp_code = o.customer_code
           JOIN o2c.customers c ON c.customer_id = x.customer_id
           JOIN o2c.product_line_map plm ON plm.product_id = l.product_id
           JOIN o2c.region_assignment ra ON ra.rep_id = o.sales_rep_id
           WHERE o.status != 'CANCELLED'
             AND o.order_date BETWEEN '2026-01-01' AND '2026-06-30'""",
    "Q5.governed_aov_numerator":
        """SELECT SUM(l.line_amount - COALESCE(r.return_amount, 0))
           FROM o2c.order_lines l
           JOIN o2c.orders o USING(order_id)
           LEFT JOIN o2c.returns r ON r.line_id = l.line_id
           WHERE o.status != 'CANCELLED'""",
}

DDL = (ROOT / "data" / "ddl" / "o2c_ddl.sql").read_text()


def coerce(table, col, value):
    if col in BOOL_TABLES.get(table, ()):
        return 1 if value == "True" else 0
    return None if value == "" else value


def main():
    con = duckdb.connect(str(DB))
    con.execute("DROP SCHEMA IF EXISTS o2c CASCADE")
    # DDL is Databricks-flavored; DuckDB accepts it once comments are gone —
    # inline comments may contain ';' and would split statements mid-way.
    bare = "\n".join(l.split("--")[0] for l in DDL.splitlines())
    for stmt in [s.strip() for s in bare.split(";") if s.strip()]:
        con.execute(stmt)

    for csv_path in sorted(OUT.glob("*.csv")):
        table = csv_path.stem
        with open(csv_path) as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue
        cols = list(rows[0].keys())
        con.executemany(
            f"INSERT INTO o2c.{table} VALUES ({','.join('?' * len(cols))})",
            [[coerce(table, c, r[c]) for c in cols] for r in rows])

    keys = json.loads((ROOT / "data" / "keys" / "keys.json").read_text())
    expected = {
        "Q1.naive_all_time_everything": keys["Q1"]["naive_all_time_everything"],
        "Q1.finance_fy26_net_invoice_date": keys["Q1"]["finance_fy26_net_invoice_date"],
        "Q2.correct_total": sum(
            keys["Q2"]["governed_net_revenue_h1_2026_by_region"].values()),
        "Q2.naive_fanout_total": keys["Q2"]["naive_fanout_total_h1_2026"],
        "Q5.governed_aov_numerator": None,  # checked via ratio below
    }
    fails = 0
    for name, sql in PARITY_QUERIES.items():
        got = con.execute(sql).fetchone()[0]
        if name.startswith("Q5"):
            continue
        ok = got == expected[name]
        fails += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'}  parity {name}: duckdb={got:,} keys={expected[name]:,}")

    aov_num = con.execute(PARITY_QUERIES["Q5.governed_aov_numerator"]).fetchone()[0]
    aov_den = con.execute(
        "SELECT COUNT(*) FROM o2c.orders WHERE status != 'CANCELLED'").fetchone()[0]
    ok = round(aov_num / aov_den) == keys["Q5"]["governed_aov_non_cancelled"]
    fails += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'}  parity Q5.aov: "
          f"duckdb={round(aov_num / aov_den):,} keys={keys['Q5']['governed_aov_non_cancelled']:,}")

    n_tables = con.execute(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = 'o2c'").fetchone()[0]
    # Team scratch schemas — mirror the Databricks grant model: cards C6/C7
    # create the governed view in o2c_team<N>. Offline mode = one DB copy
    # per table, so schemas never collide across teams.
    for i in range(1, 7):
        con.execute(f"CREATE SCHEMA IF NOT EXISTS o2c_team{i}")
    print(f"tables loaded: {n_tables}/16 (+ 6 team scratch schemas)")
    con.close()
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
