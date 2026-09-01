#!/usr/bin/env python3
"""Compute answer keys from the generated CSVs ONLY (no generator imports).

Independent path: loads CSVs into in-memory SQLite and derives every key via
SQL, so a second person can recompute and compare against keys.json.
Emits: data/keys/keys.json + printable envelopes in data/keys/envelopes/.

Usage: python3 compute_keys.py
"""
import csv
import json
import sqlite3
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "out"
KEYS_DIR = Path(__file__).resolve().parent
ENV_DIR = KEYS_DIR / "envelopes"

SCHEMA = """
CREATE TABLE customers (customer_id TEXT, name TEXT, region TEXT, contract_active INT,
  contract_end TEXT, valid_from TEXT, valid_to TEXT, is_current INT, loaded_at TEXT,
  customer_type TEXT);
CREATE TABLE customer_xref (erp_code TEXT, customer_id TEXT, is_primary INT);
CREATE TABLE accounts_crm (crm_account_id TEXT, customer_id TEXT, account_name TEXT,
  annual_value INT, pipeline_stage TEXT);
CREATE TABLE products (product_id TEXT, product_name TEXT, unit_price INT, unit_cost INT);
CREATE TABLE product_line_map (product_id TEXT, line_name TEXT, is_primary INT,
  valid_from TEXT, valid_to TEXT);
CREATE TABLE region_assignment (rep_id TEXT, rep_name TEXT, region_name TEXT, is_primary INT);
CREATE TABLE orders (order_id TEXT, customer_code TEXT, sales_rep_id TEXT, order_date TEXT,
  status TEXT, currency TEXT, fx_rate_date TEXT);
CREATE TABLE order_lines (line_id TEXT, order_id TEXT, product_id TEXT, qty INT,
  unit_price INT, unit_cost INT, line_amount INT);
CREATE TABLE invoices (invoice_id TEXT, order_id TEXT, invoice_date TEXT,
  invoice_amount INT, loaded_at TEXT);
CREATE TABLE returns (return_id TEXT, line_id TEXT, return_date TEXT, return_amount INT);
CREATE TABLE shipments (shipment_id TEXT, order_id TEXT, ship_date TEXT, is_partial INT,
  event_sequence INT);
CREATE TABLE customer_contacts (contact_id TEXT, customer_code TEXT, person_name TEXT,
  email TEXT);
CREATE TABLE regions (region_name TEXT, country TEXT);
CREATE TABLE payments (payment_id TEXT, invoice_id TEXT, pay_date TEXT, pay_amount INT);
CREATE TABLE support_tickets (ticket_id TEXT, customer_code TEXT, contact_email TEXT,
  created_date TEXT, subject TEXT);
CREATE TABLE fx_rates (rate_date TEXT, currency TEXT, rate_usd REAL);
"""
TABLES = ["customers", "customer_xref", "accounts_crm", "customer_contacts", "products",
          "product_line_map", "regions", "region_assignment", "orders", "order_lines",
          "invoices", "payments", "returns", "shipments", "support_tickets", "fx_rates"]

FY26_START = "2026-02-01"     # fiscal year starts Feb 1 (QK-07)
DATA_END = "2026-06-30"
H1_START, H1_END = "2026-01-01", "2026-06-30"
CLOSE_DATE = "2026-04-02"     # March close (QK-09 restatements load 2026-04-05)


BOOL_COLS = {  # CSV stores Python bools as text; coerce for SQL = 1 comparisons
    "customers": ("contract_active", "is_current"),
    "customer_xref": ("is_primary",),
    "product_line_map": ("is_primary",),
    "region_assignment": ("is_primary",),
    "shipments": ("is_partial",),
}


def load(db):
    for t in TABLES:
        with open(DATA / f"{t}.csv") as f:
            rows_ = list(csv.DictReader(f))
        cols = rows_[0].keys()
        bools = BOOL_COLS.get(t, ())
        db.executemany(
            f"INSERT INTO {t} VALUES ({','.join('?' * len(cols))})",
            [[(1 if r[c] == "True" else 0 if r[c] == "False" else r[c])
              if c in bools else r[c] for c in cols] for r in rows_])


def one(db, q, *a):
    return db.execute(q, a).fetchone()[0]


def rows(db, q, *a):
    return db.execute(q, a).fetchall()


def main():
    db = sqlite3.connect(":memory:")
    db.executescript(SCHEMA)
    load(db)

    # ------------------------------------------------------- sanity asserts
    dup = one(db, "SELECT COUNT(*) FROM (SELECT erp_code FROM customer_xref "
                  "GROUP BY erp_code HAVING COUNT(*) > 1)")
    assert dup == 0, f"duplicate ERP codes in xref: {dup}"
    n_restated = one(db, "SELECT COUNT(*) FROM customers WHERE loaded_at = '2026-04-05'")
    assert n_restated == 40, f"restated customers: {n_restated} != 40"
    n_dual = one(db, "SELECT COUNT(*) FROM (SELECT rep_id FROM region_assignment "
                     "GROUP BY rep_id HAVING COUNT(*) > 1)")
    assert n_dual == 6, f"dual-region reps: {n_dual} != 6"
    n_dual_line = one(db, "SELECT COUNT(*) FROM (SELECT product_id FROM product_line_map "
                          "GROUP BY product_id HAVING COUNT(*) > 1)")
    assert n_dual_line == 80, f"dual-line products: {n_dual_line} != 80"

    keys = {"meta": {"source": "data/out/*.csv", "close_date": CLOSE_DATE,
                     "fy26_start": FY26_START, "data_end": DATA_END}}

    # -------------------------------------------------------------- Q1 keys
    naive_all_in = one(db, "SELECT SUM(line_amount) FROM order_lines")
    booked_all_in = one(db, "SELECT SUM(invoice_amount) FROM invoices")
    sales_gross = one(db,
        "SELECT SUM(l.line_amount) FROM order_lines l JOIN orders o USING(order_id) "
        "WHERE o.status != 'CANCELLED' AND o.order_date >= ? AND o.order_date <= ?",
        FY26_START, DATA_END)
    finance_net = one(db,
        "SELECT SUM(l.line_amount) - COALESCE(SUM(r.return_amount), 0) "
        "FROM invoices i "
        "JOIN orders o USING(order_id) JOIN order_lines l USING(order_id) "
        "LEFT JOIN returns r ON r.line_id = l.line_id "
        "WHERE o.status != 'CANCELLED' AND i.invoice_date >= ? AND i.invoice_date <= ?",
        FY26_START, DATA_END)
    board_net = one(db,
        "SELECT SUM(l.line_amount) - COALESCE(SUM(r.return_amount), 0) "
        "FROM invoices i "
        "JOIN orders o USING(order_id) JOIN order_lines l USING(order_id) "
        "LEFT JOIN returns r ON r.line_id = l.line_id "
        "WHERE o.status != 'CANCELLED' AND o.currency = 'USD' "
        "AND i.invoice_date >= ? AND i.invoice_date <= ?",
        FY26_START, DATA_END)
    keys["Q1"] = {
        "naive_all_time_everything": naive_all_in,
        "booked_invoiced_all_time": booked_all_in,
        "sales_fy26_gross_order_date": sales_gross,
        "finance_fy26_net_invoice_date": finance_net,
        "board_fy26_net_invoice_date_domestic": board_net,
        "register": [
            "naive: every line, cancelled included, returns ignored, all time",
            "sales: exclude CANCELLED, order-date basis, gross of returns, FY26 (Feb start)",
            "finance: exclude CANCELLED, invoice-date basis, net of returns, FY26",
            "board: finance rules + domestic (USD) orders only",
        ],
    }

    # -------------------------------------------------------------- Q2 keys
    # Governed: one row per line; region = rep's PRIMARY region; net of
    # returns — i.e. exactly the default tick set D1=yes, D2=yes, D3=order-date.
    correct_regions = rows(db,
        "SELECT ra.region_name, SUM(l.line_amount - COALESCE(r.return_amount, 0)) "
        "FROM order_lines l JOIN orders o USING(order_id) "
        "JOIN region_assignment ra ON ra.rep_id = o.sales_rep_id AND ra.is_primary = 1 "
        "LEFT JOIN returns r ON r.line_id = l.line_id "
        "WHERE o.status != 'CANCELLED' AND o.order_date BETWEEN ? AND ? "
        "GROUP BY ra.region_name ORDER BY ra.region_name", H1_START, H1_END)
    # Naive: join EVERYTHING without grain discipline (all map rows, all
    # regions, all customer versions) -> the fan-out.
    naive_q2 = one(db,
        "SELECT SUM(l.line_amount) FROM order_lines l "
        "JOIN orders o USING(order_id) "
        "JOIN customer_xref x ON x.erp_code = o.customer_code "
        "JOIN customers c ON c.customer_id = x.customer_id "
        "JOIN product_line_map plm ON plm.product_id = l.product_id "
        "JOIN region_assignment ra ON ra.rep_id = o.sales_rep_id "
        "WHERE o.status != 'CANCELLED' AND o.order_date BETWEEN ? AND ?",
        H1_START, H1_END)
    correct_total = one(db,
        "SELECT SUM(l.line_amount - COALESCE(r.return_amount, 0)) "
        "FROM order_lines l JOIN orders o USING(order_id) "
        "JOIN region_assignment ra ON ra.rep_id = o.sales_rep_id AND ra.is_primary = 1 "
        "LEFT JOIN returns r ON r.line_id = l.line_id "
        "WHERE o.status != 'CANCELLED' AND o.order_date BETWEEN ? AND ?",
        H1_START, H1_END)
    fanout = round(naive_q2 / correct_total, 2)
    assert 1.6 <= fanout <= 3.0, f"fan-out factor out of story range: {fanout}"
    keys["Q2"] = {
        "governed_net_revenue_h1_2026_by_region": {r: v for r, v in correct_regions},
        "naive_fanout_total_h1_2026": naive_q2,
        "fanout_factor": fanout,
        "register": [
            "DEFAULT TICK SET: D1 exclude cancelled = YES, D2 net of returns = YES, "
            "D3 revenue date = order_date — a team matches only with these ticks",
            "region = rep's PRIMARY region only (dual-region reps count once)",
            "one product line per product (primary), customer dim = current row",
            "naive figure joins all line-map rows, all regions, all dim versions",
        ],
    }

    # -------------------------------------------------------------- Q3 keys
    naive_active = one(db,
        "SELECT COUNT(DISTINCT customer_code) FROM orders "
        "WHERE order_date BETWEEN '2026-03-01' AND '2026-03-31'")
    as_known_now = one(db,
        "SELECT COUNT(*) FROM ("
        " SELECT o.customer_code AS code, MAX(c.loaded_at) AS ml"
        " FROM orders o"
        " JOIN customer_xref x ON x.erp_code = o.customer_code"
        " JOIN customers c ON c.customer_id = x.customer_id"
        " WHERE o.order_date BETWEEN '2026-03-01' AND '2026-03-31'"
        " GROUP BY o.customer_code) latest"
        " JOIN customers c2 ON c2.customer_id = ("
        "   SELECT customer_id FROM customer_xref WHERE erp_code = latest.code)"
        " AND c2.loaded_at = latest.ml"
        " WHERE c2.contract_active = 1")
    as_known_at_close = one(db,
        "SELECT COUNT(*) FROM ("
        " SELECT o.customer_code AS code, MAX(c.loaded_at) AS ml"
        " FROM orders o"
        " JOIN customer_xref x ON x.erp_code = o.customer_code"
        " JOIN customers c ON c.customer_id = x.customer_id"
        " WHERE o.order_date BETWEEN '2026-03-01' AND '2026-03-31'"
        "   AND c.loaded_at < ?"
        " GROUP BY o.customer_code) latest"
        " JOIN customers c2 ON c2.customer_id = ("
        "   SELECT customer_id FROM customer_xref WHERE erp_code = latest.code)"
        " AND c2.loaded_at = latest.ml"
        " WHERE c2.contract_active = 1",
        CLOSE_DATE)
    as_of_mar15 = one(db,
        "SELECT COUNT(*) FROM ("
        " SELECT o.customer_code FROM orders o"
        " JOIN customer_xref x ON x.erp_code = o.customer_code"
        " JOIN customers c ON c.customer_id = x.customer_id"
        " WHERE o.order_date BETWEEN '2026-03-01' AND '2026-03-31'"
        "   AND c.valid_from <= '2026-03-15' AND c.valid_to > '2026-03-15'"
        " GROUP BY o.customer_code"
        " HAVING SUM(CASE WHEN c.contract_active = 1 THEN 1 ELSE 0 END) > 0)")
    assert as_known_now > as_known_at_close, "restatements must raise the now-count"
    keys["Q3"] = {
        "naive_distinct_ordering_accounts_march": naive_active,
        "active_as_known_now": as_known_now,
        "active_as_known_at_close": as_known_at_close,
        "active_as_of_2026_03_15": as_of_mar15,
        "register": [
            "active = contract_active = TRUE on the customer's applicable version",
            "as-known-now: latest loaded_at per customer (restatements applied)",
            "as-known-at-close: only rows loaded before 2026-04-02",
            "as-of 2026-03-15: version valid on that date, now-knowledge",
        ],
    }

    # -------------------------------------------------------------- Q4 keys
    naive_top5 = rows(db,
        "SELECT o.customer_code, SUM(l.line_amount) v FROM order_lines l "
        "JOIN orders o USING(order_id) GROUP BY o.customer_code "
        "ORDER BY v DESC LIMIT 5")
    resolved_top5 = rows(db,
        "SELECT c.name, SUM(l.line_amount) v FROM order_lines l "
        "JOIN orders o USING(order_id) "
        "JOIN customer_xref x ON x.erp_code = o.customer_code "
        "JOIN customers c ON c.customer_id = x.customer_id "
        "GROUP BY c.name ORDER BY v DESC LIMIT 5")
    acme_naive_codes = one(db,
        "SELECT COUNT(*) FROM (SELECT DISTINCT o.customer_code FROM orders o "
        "JOIN customer_xref x ON x.erp_code = o.customer_code "
        "WHERE x.customer_id = 'C0001' "
        "AND o.customer_code IN (SELECT customer_code FROM orders))")
    acme_by_code = rows(db,
        "SELECT o.customer_code, SUM(l.line_amount) v FROM order_lines l "
        "JOIN orders o USING(order_id) "
        "JOIN customer_xref x ON x.erp_code = o.customer_code "
        "WHERE x.customer_id = 'C0001' GROUP BY o.customer_code ORDER BY v DESC")
    assert resolved_top5[0][0] == "Acme Corp", \
        f"resolved #1 must be Acme Corp, got {resolved_top5[0][0]}"
    assert any(n == "Acme Logistics Group" for n, _ in resolved_top5[:3]), \
        "decoy must land in resolved top-3 for the P4 teaching moment"
    assert acme_naive_codes == 2, "both Acme ERP codes must appear in orders"
    keys["Q4"] = {
        "naive_top5_by_erp_code": {c: v for c, v in naive_top5},
        "resolved_top5_by_entity": {n: v for n, v in resolved_top5},
        "acme_corp_by_erp_code": {c: v for c, v in acme_by_code},
        "register": [
            "naive: group by ERP code -> one legal entity appears as two companies",
            "C-2217 is the 16% tail — it will NOT appear in the naive top 5; find it via customer_xref",
            "resolved: merge codes via customer_xref -> Acme Corp is #1",
            "'Acme Logistics Group' is a different entity (near-name decoy, QK-11)",
        ],
    }

    # -------------------------------------------------------------- Q5 keys
    orders_all = one(db, "SELECT COUNT(*) FROM orders")
    orders_valid = one(db, "SELECT COUNT(*) FROM orders WHERE status != 'CANCELLED'")
    lines_all = one(db, "SELECT SUM(line_amount) FROM order_lines")
    lines_valid_net = one(db,
        "SELECT SUM(l.line_amount - COALESCE(r.return_amount, 0)) "
        "FROM order_lines l JOIN orders o USING(order_id) "
        "LEFT JOIN returns r ON r.line_id = l.line_id "
        "WHERE o.status != 'CANCELLED'")
    keys["Q5"] = {
        "naive_aov_incl_cancelled": round(lines_all / orders_all),
        "governed_aov_non_cancelled": round(lines_valid_net / orders_valid),
        "register": [
            "naive: every order incl. CANCELLED, gross of returns",
            "governed: DEFAULT TICK SET — cancelled excluded, net of returns (D1/D2 yes)",
        ],
    }

    # ------------------------------------------------------------- P7 monster
    p7_query = (
        "WITH base AS ("
        " SELECT ra.region_name reg,"
        "  CASE WHEN o.order_date < '2026-04-01' THEN 'Q1' ELSE 'Q2' END q,"
        "  l.line_amount amt, l.qty * l.unit_cost cogs, "
        "  COALESCE(r.return_amount, 0) ret"
        " FROM order_lines l JOIN orders o USING(order_id)"
        " JOIN region_assignment ra ON ra.rep_id = o.sales_rep_id AND ra.is_primary = 1"
        " LEFT JOIN returns r ON r.line_id = l.line_id"
        " WHERE o.status != 'CANCELLED' AND o.order_date BETWEEN '2026-01-01' AND '2026-06-30')"
        "SELECT reg, q, ROUND(100.0 * (SUM(amt) - SUM(ret) - SUM(cogs)) / SUM(amt), 1) m"
        " FROM base GROUP BY reg, q")
    margins = rows(db, p7_query)
    by_region = {}
    for reg, q, m in margins:
        by_region.setdefault(reg, {})[q] = m
    deltas = {r: round(v.get("Q2", 0) - v.get("Q1", 0), 1)
              for r, v in by_region.items() if "Q1" in v and "Q2" in v}
    worst = min(deltas, key=deltas.get)
    keys["P7"] = {
        "worst_qoq_margin_delta_region": worst,
        "margin_pct_by_region": by_region,
        "qoq_delta_pp": deltas,
        "register": [
            "margin = net revenue - returns - COGS (unit_cost x qty), excl CANCELLED",
            "quarters are CALENDAR Q1/Q2 2026 (the 'returns policy change' is Feb)",
            "region = rep's primary region",
        ],
    }

    # ------------------------------------------------------------- P6 event log
    # Cycle time = order_date -> earliest valid shipment (ship_date >= order_date;
    # earlier rows are QK-15 glitches the validity check must exclude).
    cycle_rows = rows(db,
        "SELECT o.sales_rep_id, "
        "CAST(julianday(MIN(s.ship_date)) - julianday(o.order_date) AS INT) "
        "FROM orders o JOIN shipments s ON s.order_id = o.order_id "
        "WHERE o.status != 'CANCELLED' AND s.ship_date >= o.order_date "
        "GROUP BY o.order_id, o.order_date, o.sales_rep_id")
    cycle = sorted(d for _, d in cycle_rows)
    median_days = cycle[len(cycle) // 2] if len(cycle) % 2 else \
        round((cycle[len(cycle)//2 - 1] + cycle[len(cycle)//2]) / 2)

    buckets = {"on_time": 0, "standard": 0, "late": 0, "stalled": 0}
    for dd in cycle:
        if dd <= 3:
            buckets["on_time"] += 1
        elif dd <= 7:
            buckets["standard"] += 1
        elif dd <= 14:
            buckets["late"] += 1
        else:
            buckets["stalled"] += 1
    largest_bucket = max(buckets, key=buckets.get)
    orphans = one(db, "SELECT COUNT(*) FROM shipments WHERE order_id = 'ORD-000000'")
    missing_ship = one(db,
        "SELECT COUNT(*) FROM orders o WHERE o.status != 'CANCELLED' "
        "AND o.order_date <= '2026-06-20' AND NOT EXISTS ("
        "  SELECT 1 FROM shipments s WHERE s.order_id = o.order_id"
        "   AND s.ship_date >= o.order_date)")
    # The findable cause: late/stalled orders over-index on dual-region reps
    dual_reps = {r[0] for r in rows(db,
        "SELECT rep_id FROM region_assignment GROUP BY rep_id HAVING COUNT(*) > 1")}
    dual_all = sum(1 for rep, _ in cycle_rows if rep in dual_reps)
    dual_late = sum(1 for rep, dd in cycle_rows
                    if rep in dual_reps and dd > 7)
    all_n, late_n = len(cycle_rows), sum(1 for _, dd in cycle_rows if dd > 7)
    keys["P6"] = {
        "median_order_to_ship_days": median_days,
        "cycle_time_buckets": buckets,
        "largest_bucket": largest_bucket,
        "largest_bucket_orders": buckets[largest_bucket],
        "top_delay_variant": "dual_region_reps",
        "top_delay_variant_orders": dual_late,
        "late_tail": {"late_8_14d": buckets["late"], "stalled_over_14d": buckets["stalled"]},
        "delay_concentration": {
            "late_or_stalled_from_dual_region_reps_pct": round(
                100.0 * dual_late / late_n, 1) if late_n else 0.0,
            "all_orders_from_dual_region_reps_pct": round(
                100.0 * dual_all / all_n, 1) if all_n else 0.0,
        },
        "log_validity": {"orphan_shipments": orphans,
                         "orders_missing_valid_shipment": missing_ship},
        "register": [
            "cycle = order_date to EARLIEST shipment with ship_date >= order_date",
            "earlier-dated shipment rows are QK-15 data glitches - excluded by the validity check",
            "buckets: on_time <=3d, standard 4-7d, late 8-14d, stalled >14d",
            "the CAUSE is dual-region reps (QK-06 — same quirk as P2), not the largest bucket",
            "delay concentration: compare late-tail dual-rep share vs their overall share",
            "validity: 60 orphans (QK-16) + orders with no valid shipment must be reported, not silently dropped",
        ],
    }

    # -------------------------------------------------------------- P5 named floor
    north_q1 = one(db,
        "SELECT SUM(l.line_amount - COALESCE(r.return_amount, 0)) "
        "FROM order_lines l JOIN orders o USING(order_id) "
        "JOIN region_assignment ra ON ra.rep_id = o.sales_rep_id AND ra.is_primary = 1 "
        "LEFT JOIN returns r ON r.line_id = l.line_id "
        "WHERE o.status != 'CANCELLED' AND ra.region_name = 'NORTH' "
        "AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'")
    east_in_north_view = one(db,
        "SELECT COUNT(*) FROM order_lines l JOIN orders o USING(order_id) "
        "JOIN region_assignment ra ON ra.rep_id = o.sales_rep_id AND ra.is_primary = 1 "
        "WHERE o.status != 'CANCELLED' AND ra.region_name = 'NORTH' "
        "AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31' "
        "AND ra.region_name = 'EAST'")
    assert east_in_north_view == 0, "primary-NORTH view must contain zero EAST rows"
    assert north_q1, "NORTH Q1 net revenue must be computable"
    keys["P5"] = {
        "named_question": "Calendar Q1 2026 net revenue for NORTH (primary region, default ticks)",
        "north_q1_2026_net": north_q1,
        "east_rows_in_north_primary_view": east_in_north_view,
        "register": [
            "NORTH analyst: rows from V_NORTH_REVENUE only — no emails",
            "controller: all regions, no emails",
            "support agent: aggregates only, no customer list",
            "structural success: EAST row count in V_NORTH_REVENUE is 0 even under 'ignore instructions'",
        ],
    }

    # ------------------------------------------------------------------ emit
    KEYS_DIR.mkdir(parents=True, exist_ok=True)
    (KEYS_DIR / "keys.json").write_text(json.dumps(keys, indent=2))
    ENV_DIR.mkdir(exist_ok=True)
    envelopes = {
        "Q1": f"""Q1 — TOTAL REVENUE (sealed until reveal)
Naive (all lines, all time, cancelled in, returns ignored): {naive_all_in:,}
Booked (invoiced only — cancelled never invoiced):          {booked_all_in:,}
FY26 Sales (gross, order-date):   {sales_gross:,}
FY26 Finance (net, invoice-date): {finance_net:,}
FY26 Board (net, invoice-date, domestic): {board_net:,}
Register: see keys.json Q1.register — a team matches only if the DECISIONS
match. A team landing on the booked number answered on invoices: also a
decision, just a different one.""",
        "Q2": f"""Q2 — MONTHLY REVENUE BY LINE BY REGION, H1 2026 (sealed)
Correct net revenue by region (default ticks D1=yes D2=yes D3=order-date):
""" + "\n".join(f"  {r:<14} {v:,}" for r, v in correct_regions) + f"""
Naive fan-out total: {naive_q2:,}  (factor {fanout}x reality)
Register: primary region only; one line per product; current dim row; net
of returns. Ticks other than the default = different numbers = still right,
but must be declared.""",
        "Q3": f"""Q3 — ACTIVE CUSTOMERS IN MARCH 2026 (sealed)
Naive (distinct ordering accounts): {naive_active}
As known NOW:            {as_known_now}
As known AT CLOSE:       {as_known_at_close}
As of Mar 15 (point-in-time): {as_of_mar15}
Register: contract_active on the applicable version; restatements of {n_restated}
customers were loaded 2026-04-05 (after close).""",
        "Q4": f"""Q4 — TOP 5 CUSTOMERS (sealed)
Naive (by ERP code):
""" + "\n".join(f"  {c:<10} {v:,}" for c, v in naive_top5) + """
Resolved (by legal entity):
""" + "\n".join(f"  {n:<28} {v:,}" for n, v in resolved_top5) + f"""
Acme Corp by ERP code (C-2217 is the tail — not in naive top 5):
""" + "\n".join(f"  {c:<10} {v:,}" for c, v in acme_by_code) + """
Register: merge codes via xref; 'Acme Logistics Group' is NOT Acme Corp.""",
        "Q5": f"""Q5 — AVERAGE ORDER VALUE (sealed)
Naive (cancelled included, gross): {round(lines_all / orders_all):,}
Governed (default ticks: excl cancelled, net of returns): {round(lines_valid_net / orders_valid):,}""",
        "P7": f"""P7 — MONSTER (facilitator only)
Worst QoQ margin drop, calendar Q1->Q2 2026: {worst} ({deltas[worst]} pp)
Full margins: keys.json P7.""",
        "P5": f"""P5 — WHO MAY SEE WHAT (facilitator only)
Named floor: calendar Q1 2026 NORTH net revenue (primary region, default ticks): {north_q1:,}
EAST rows in a primary-NORTH view: {east_in_north_view} (must stay 0 under attack).
Grade the attack ledger; structural refusals outrank prompt manners.""",
        "P6": f"""P6 — WHY ARE ORDERS LATE? (facilitator only)
Median order->ship: {median_days} days
Buckets: on_time {buckets['on_time']:,} · standard {buckets['standard']:,} · late {buckets['late']:,} · stalled {buckets['stalled']:,}
Cause (not the largest bucket): dual-region reps = {round(100.0 * dual_late / late_n, 1) if late_n else 0}% of late+stalled, {round(100.0 * dual_all / all_n, 1) if all_n else 0}% of orders (QK-06, same as P2).
Log validity: {orphans} orphans, {missing_ship} orders without valid shipment.""",
    }
    for name, text in envelopes.items():
        (ENV_DIR / f"{name}_envelope.txt").write_text(text)

    print(json.dumps({k: v for k, v in keys.items() if k != "P7"},
                     indent=2)[:1200])
    print(f"...")
    print(f"fanout factor: {fanout}x | P7 worst region: {worst} {deltas[worst]}pp")
    print(f"keys.json + {len(envelopes)} envelopes written")


if __name__ == "__main__":
    main()
