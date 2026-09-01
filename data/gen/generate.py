#!/usr/bin/env python3
"""Meridian Trading Co. O2C dataset generator.

Deterministic (fixed seed, stdlib only). Emits CSVs to data/out/ and a
manifest with row counts. Every planted quirk QK-01..QK-18 is documented in
data/README.md and provable via data/keys/quirk_checks.sql.

Usage: python3 generate.py [--scale 1.0] [--seed 42]
"""
import argparse
import csv
import datetime as dt
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out"
FMT = "%Y-%m-%d"
NEVER = dt.date(9999, 12, 31)

# ---------------------------------------------------------------- parameters
N_CUSTOMERS = 2000
N_SCD2 = 600            # QK-08: customers with a 2nd version -> 2600 rows
N_RESTATE = 40          # QK-09: retroactive restatements, loaded 2026-04-05
CLOSE_DATE = dt.date(2026, 4, 2)
N_PRODUCTS = 400
N_DUAL_LINE = 80        # QK-05: 20% of products in 2 lines (high-price skew)
N_ORDERS = 5000
P_CANCELLED = 0.06      # QK-01
P_EUR = 0.03            # QK-04
P_LATE_INVOICE = 0.12   # QK-03 (median +9 days)
N_RETURNS = 380         # QK-02
N_TICKETS = 6000
N_CONTACTS = 2100
N_CRM_ONLY = 100
N_ORPHAN_SHIP = 60      # QK-16
P_LATE_SHIP = 0.04      # QK-15
P_PARTIAL_SHIP = 0.20   # second shipment event per order (P2 fan-out fodder)
N_SHARED_DOMAIN_COMPANIES = 12   # QK-12
CRM_OVERSTATE = 1.018   # QK-18

REGIONS = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL", "NORTHEAST", "SOUTHEAST", "MIDATLANTIC"]
LINES = ["AUDIO", "DISPLAYS", "POWER", "MOBILITY", "NETWORKING", "STORAGE", "ACCESSORIES", "WEARABLES"]
CO_PREFIX = ["Acme", "Nordic", "Summit", "Harbor", "Beacon", "Crestline", "Juniper", "Redwood",
             "Ironwood", "Bluepeak", "Sterling", "Copperfield", "Lakeside", "Pinnacle", "Vantage",
             "Northgate", "Silverline", "Oakford", "Maplewood", "Granite", "Cedarpoint", "Falcon",
             "Ridgeway", "Westbrook", "Eastvale", "Kingsport", "Millbrook", "Stonebridge", "Torchlight",
             "Windmere", "Aldergate", "Bramble", "Cobblestone", "Driftwood", "Elmwood", "Foxglove",
             "Glenmoor", "Hawthorn", "Ivywood", "Kingsley"]
CO_SUFFIX = ["Trading", "Supply", "Logistics", "Group", "Partners", "Industries", "Distribution", "Wholesale"]
FIRSTS = ["Ava", "Ben", "Clara", "Dev", "Elena", "Frank", "Grace", "Hugo", "Iris", "Jonas", "Kira",
          "Liam", "Mona", "Nadia", "Omar", "Priya", "Quinn", "Rosa", "Sam", "Tara", "Uma", "Viktor",
          "Wendy", "Xavi", "Yara", "Zane", "Leo", "Nora", "Pablo", "Ruth"]
LASTS = ["Adler", "Baker", "Costa", "Dahal", "Egan", "Fischer", "Garcia", "Hansen", "Ibrahim", "Jansen",
         "Keller", "Lindqvist", "Meyer", "Novak", "Okafor", "Petrov", "Quintana", "Ricci", "Schmidt",
         "Tran", "Ueda", "Vargas", "Weber", "Xu", "Yilmaz", "Zhang", "Ahmed", "Bianchi", "Cohen", "Dubois"]
DOMAINS = ["meridian-cust.com", "brightinbox.net", "corpmail.org", "tradehub.io"]
SHARED_DOMAIN = "consultinghub.io"  # QK-12

ACME_ID = "C0001"        # QK-10: two ERP codes, 84/16 split
ACME_PRIMARY = "C-1042"
ACME_SECOND = "C-2217"
DECOY_ID = "C0002"       # QK-11: near-name decoy, its own entity
WHALE_IDS = ["C0003", "C0004", "C0005", "C0006"]


def d(year, month, day):
    return dt.date(year, month, day)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    scale = args.scale
    OUT.mkdir(parents=True, exist_ok=True)

    def n(x):
        return max(1, round(x * scale))

    # ------------------------------------------------------------- customers
    # customer_id, name, region, contract_active, contract_end, valid_from,
    # valid_to, is_current, loaded_at, customer_type
    customers = []
    names = set()
    for i in range(1, N_CUSTOMERS + 1):
        cid = f"C{i:04d}"
        base = f"{rng.choice(CO_PREFIX)} {rng.choice(CO_SUFFIX)}"
        name = base if base not in names else f"{base} {len(names)}"  # serial keeps it finite
        names.add(name)
        if cid == ACME_ID:
            name = "Acme Corp"
        if cid == DECOY_ID:
            name = "Acme Logistics Group"
        signup = d(2020, 1, 1) + dt.timedelta(days=rng.randrange(2000))
        region = REGIONS[(i - 1) % len(REGIONS)]
        ctype = "DISTRIBUTOR" if i % 7 == 0 else ("RETAIL" if i % 3 == 0 else "COMMERCIAL")
        customers.append({
            "customer_id": cid, "name": name, "region": region,
            "contract_active": rng.random() < 0.85,
            "contract_end": None, "valid_from": signup, "valid_to": NEVER,
            "is_current": True, "loaded_at": d(2025, 8, 1), "customer_type": ctype,
        })
    by_id = {c["customer_id"]: c for c in customers}

    # QK-08 SCD2: 600 customers get a second version (region/name change)
    scd2 = rng.sample([c for c in customers if c["customer_id"] not in
                       (ACME_ID, DECOY_ID, *WHALE_IDS)], n(N_SCD2))
    for c in scd2:
        # change stays before March 2026 so dimension loads never cross the
        # close date — only the 40 restatements (QK-09) load post-close
        change = d(2025, 9, 1) + dt.timedelta(days=rng.randrange(180))
        c["valid_to"] = change - dt.timedelta(days=1)
        c["is_current"] = False
        new_region = rng.choice([r for r in REGIONS if r != c["region"]])
        customers.append({
            "customer_id": c["customer_id"], "name": c["name"], "region": new_region,
            "contract_active": c["contract_active"], "contract_end": None,
            "valid_from": change, "valid_to": NEVER, "is_current": True,
            "loaded_at": change + dt.timedelta(days=5), "customer_type": c["customer_type"],
        })

    # QK-09 restatements: 40 customers, backdated reactivation loaded post-close.
    # Exclude SCD2 customers: their two versions would tangle the close-vs-now view.
    scd2_ids = {c["customer_id"] for c in scd2}
    restated = rng.sample([c for c in customers
                           if c["is_current"] and c["customer_id"] not in
                           (ACME_ID, DECOY_ID, *WHALE_IDS, *scd2_ids)], n(N_RESTATE))
    for c in restated:
        base = next(x for x in customers if x["customer_id"] == c["customer_id"]
                    and x["valid_from"] == c["valid_from"])
        base["contract_active"] = False     # pre-close knowledge: inactive
        base["loaded_at"] = d(2026, 1, 10)
        base["is_current"] = False
        base["valid_to"] = NEVER
        customers.append({                  # restated truth, loaded after close
            "customer_id": c["customer_id"], "name": c["name"], "region": c["region"],
            "contract_active": True, "contract_end": None,
            "valid_from": base["valid_from"], "valid_to": NEVER,
            "is_current": True, "loaded_at": d(2026, 4, 5),
            "customer_type": c["customer_type"],
        })

    # ----------------------------------------------------------------- xref
    # QK-10: Acme Corp has two ERP codes; 100 entities have none.
    # Xref maps ENTITIES (customer_id), not SCD2 rows -> dedupe by id.
    seen_ids = set()
    with_erp = []
    for c in customers:
        cid = c["customer_id"]
        if cid not in (ACME_ID,) and cid not in seen_ids:
            seen_ids.add(cid)
            with_erp.append(cid)
    rng.shuffle(with_erp)
    no_erp = set(with_erp[:100])
    xref = []
    code_no = 1000
    RESERVED = {ACME_PRIMARY, ACME_SECOND}
    for cid in with_erp:
        if cid in no_erp:
            continue
        code_no += 1
        while f"C-{code_no}" in RESERVED:   # keep Acme's two codes exclusive (QK-10)
            code_no += 1
        xref.append({"erp_code": f"C-{code_no}", "customer_id": cid,
                     "is_primary": True})
    xref.append({"erp_code": ACME_PRIMARY, "customer_id": ACME_ID, "is_primary": True})
    xref.append({"erp_code": ACME_SECOND, "customer_id": ACME_ID, "is_primary": True})
    code_of = {}
    for x in xref:
        if x["is_primary"] and x["customer_id"] not in code_of:
            code_of[x["customer_id"]] = x["erp_code"]
    acme_codes = {ACME_PRIMARY: 0.84, ACME_SECOND: 0.16}   # QK-10 split
    decoy_code = code_of[DECOY_ID]
    shared_domain_ids = set(rng.sample(
        [cid for cid in code_of],          # must carry an ERP code to emit tickets
        N_SHARED_DOMAIN_COMPANIES))                          # QK-12

    # ------------------------------------------------------------------ reps
    # QK-06: 6 reps hold a second region. Dual-region reps carry ~40-45% of
    # order volume so the Q2 fan-out compounds to ~2.3x with the line-map
    # and SCD2 factors (measured by compute_keys.py, asserted in range).
    dual_reps = {"R03", "R07", "R11", "R14", "R17", "R19"}
    rep_region, rep_home = {}, {}
    for r in range(1, 21):
        rep_id = f"R{r:02d}"
        home = REGIONS[(r - 1) % len(REGIONS)]
        rep_home[rep_id] = home
        rep_region[rep_id] = [(home, True)]
        if rep_id in dual_reps:
            rep_region[rep_id].append(
                (REGIONS[(r + 3) % len(REGIONS)], False))
    rep_weight = {rid: (1.8 if rid in dual_reps else 1.0) for rid in rep_home}

    # -------------------------------------------------------------- products
    products = []
    for i in range(1, N_PRODUCTS + 1):
        pid = f"P{i:04d}"
        price = min(5000, max(20, round(rng.lognormvariate(5.6, 0.9))))
        products.append({"product_id": pid,
                         "product_name": f"{rng.choice(LINES).title()} Unit {i:04d}",
                         "unit_price": price,
                         "unit_cost": round(price * rng.uniform(0.55, 0.75))})
    # QK-05: dual-line products skew to higher-priced items, but not the very
    # top (ranks 50-130) — keeps the Q2 fan-out near the 2.3x story value.
    ranked = sorted(products, key=lambda p: -p["unit_price"])
    dual_products = {p["product_id"] for p in ranked[50:50 + N_DUAL_LINE]}
    line_map = []
    for p in products:
        primary = LINES[int(p["product_id"][1:]) % len(LINES)]  # hash() is salted; index is not
        line_map.append({"product_id": p["product_id"], "line_name": primary,
                         "is_primary": True, "valid_from": d(2023, 1, 1),
                         "valid_to": NEVER})
        if p["product_id"] in dual_products:
            extra = rng.choice([l for l in LINES if l != primary])
            vf = d(2025, rng.randrange(1, 13), 1)
            line_map.append({"product_id": p["product_id"], "line_name": extra,
                             "is_primary": False, "valid_from": vf,
                             "valid_to": NEVER})

    # ----------------------------------------------------------------- fx
    fx = []
    for m in range(2, 20):  # Feb 2025 .. Jul 2026 (invoices lag into July)
        year = 2025 + (m - 1) // 12
        month = (m - 1) % 12 + 1
        base = 1.06 + 0.01 * ((m * 7) % 5)
        fx.append({"rate_date": d(year, month, 1), "currency": "EUR",
                   "rate_usd": round(base, 4)})
        fx.append({"rate_date": d(year, month, 15), "currency": "EUR",
                   "rate_usd": round(base + 0.012, 4)})  # order vs invoice gap (QK-04)

    # ---------------------------------------------------------------- orders
    # Whales: Acme (#1 when merged), decoy (#2), four more. Acme's revenue
    # splits 84/16 across its two ERP codes (QK-10).
    order_pool = []   # (customer_id, weight)
    for c in customers:
        if not c["is_current"]:
            continue
        cid = c["customer_id"]
        if cid == ACME_ID:
            order_pool.append((cid, 120))    # merged: #1 entity (QK-10 split)
        elif cid == DECOY_ID:
            order_pool.append((cid, 75))     # near-name decoy lands #2 (QK-11)
        elif cid in WHALE_IDS:
            order_pool.append((cid, 55))
        else:
            order_pool.append((cid, 1))
    total_w = sum(w for _, w in order_pool)

    orders, order_lines = [], []
    line_no, order_no = 0, 0
    acme_alloc = {"C-1042": 0, "C-2217": 0}
    n_orders = n(N_ORDERS)
    for _ in range(n_orders):
        order_no += 1
        oid = f"O{order_no:05d}"
        # pick customer
        roll = rng.uniform(0, total_w)
        acc = 0.0
        for cid, w in order_pool:
            acc += w
            if roll <= acc:
                break
        if cid == ACME_ID:
            code = ACME_PRIMARY if rng.random() < 0.84 else ACME_SECOND
            acme_alloc[code] += 1
        else:
            code = code_of.get(cid)
            if code is None:   # no-ERP customer: skip (cannot order without ERP)
                continue
        # rep: dual-region reps over-weighted
        weights = [rep_weight[r] for r in rep_home]
        rep_id = rng.choices(list(rep_home), weights=weights)[0]
        odate = d(2025, 2, 1) + dt.timedelta(days=rng.randrange(515))  # ..2026-06-30
        if rng.random() < 0.008:
            odate = d(2026, 3, rng.randrange(1, 31))  # feed March activity
        status = "CANCELLED" if rng.random() < P_CANCELLED else "SHIPPED"
        currency = "EUR" if rng.random() < P_EUR else "USD"
        # cancelled orders skew big (bulk orders killed on credit failure) so
        # the Q5 AOV gap is visible, not a $4 rounding note
        qty_scale = 2.5 if status == "CANCELLED" else 1.0
        orders.append({"order_id": oid, "customer_code": code,
                       "sales_rep_id": rep_id, "order_date": odate,
                       "status": status, "currency": currency,
                       "fx_rate_date": odate})
        price_bump = 1.8 if cid in (ACME_ID, DECOY_ID, *WHALE_IDS) else 1.0
        for _ in range(rng.randrange(2, 6)):
            line_no += 1
            p = rng.choice(products)
            qty = max(1, round(rng.uniform(1, 20) * (price_bump ** 0.5) * qty_scale))
            orders_lines_row = {"line_id": f"L{line_no:06d}", "order_id": oid,
                                "product_id": p["product_id"], "qty": qty,
                                "unit_price": p["unit_price"],
                                "unit_cost": p["unit_cost"],
                                "line_amount": qty * p["unit_price"]}
            order_lines.append(orders_lines_row)

    # 40 restated customers must be active-ordering in March 2026 (QK-09 proof)
    code_by_cid = {c["customer_id"]: code_of.get(c["customer_id"])
                   for c in customers}
    restated_codes = [code_by_cid[c["customer_id"]] for c in restated]
    restated_codes = [c for c in restated_codes if c]
    march = d(2026, 3, 1)
    for k, code in enumerate(restated_codes):
        order_no += 1
        oid = f"O{order_no:05d}"
        orders.append({"order_id": oid, "customer_code": code,
                       "sales_rep_id": f"R{(k % 20) + 1:02d}",
                       "order_date": d(2026, 3, 2 + (k % 26)),
                       "status": "SHIPPED", "currency": "USD",
                       "fx_rate_date": d(2026, 3, 2 + (k % 26))})
        line_no += 1
        p = products[k % len(products)]
        order_lines.append({"line_id": f"L{line_no:06d}", "order_id": oid,
                            "product_id": p["product_id"], "qty": 2,
                            "unit_price": p["unit_price"],
                            "unit_cost": p["unit_cost"],
                            "line_amount": 2 * p["unit_price"]})

    # -------------------------------------------------------------- invoices
    # QK-03: 12% lag ~9 days (month-end straddles); 30 late-arriving rows.
    orders_by_id = {o["order_id"]: o for o in orders}
    non_cancelled = [o for o in orders if o["status"] != "CANCELLED"]
    invoices = []
    for k, o in enumerate(non_cancelled):
        lag = (9 + rng.randrange(-3, 4)) if rng.random() < P_LATE_INVOICE else 2
        loaded = o["order_date"] + dt.timedelta(days=lag)
        row = {"invoice_id": f"I{k+1:05d}", "order_id": o["order_id"],
               "invoice_date": loaded, "invoice_amount": 0, "loaded_at": loaded}
        invoices.append(row)
    for row in rng.sample(invoices, 30):      # late-arriving (March straddle)
        row["loaded_at"] = d(2026, 4, 3 + rng.randrange(5))
    inv_total_by_order = {}
    for ln in order_lines:
        o = orders_by_id[ln["order_id"]]
        if o["status"] == "CANCELLED":
            continue
        inv_total_by_order[ln["order_id"]] = \
            inv_total_by_order.get(ln["order_id"], 0) + ln["line_amount"]
    for row in invoices:
        row["invoice_amount"] = inv_total_by_order.get(row["order_id"], 0)

    # --------------------------------------------------------------- returns
    # QK-02: 380 returns on non-cancelled lines, 5-60% of line amount.
    invoiceable_lines = [ln for ln in order_lines
                         if orders_by_id[ln["order_id"]]["status"] != "CANCELLED"]
    returns = []
    for k, ln in enumerate(rng.sample(invoiceable_lines,
                                      min(n(N_RETURNS), len(invoiceable_lines)))):
        amt = round(ln["line_amount"] * rng.uniform(0.05, 0.60))
        rdate = orders_by_id[ln["order_id"]]["order_date"] + dt.timedelta(
            days=rng.randrange(10, 60))
        returns.append({"return_id": f"RT{k+1:04d}", "line_id": ln["line_id"],
                        "return_date": rdate, "return_amount": amt})

    # -------------------------------------------------------------- payments
    payments = []
    for k, inv in enumerate(invoices):
        if inv["invoice_amount"] <= 0:
            continue
        payments.append({"payment_id": f"PM{k+1:05d}",
                         "invoice_id": inv["invoice_id"],
                         "pay_date": inv["invoice_date"] + dt.timedelta(
                             days=rng.randrange(15, 46)),
                         "pay_amount": inv["invoice_amount"]})

    # ------------------------------------------------------------- shipments
    # P_PARTIAL_SHIP second events; QK-15 4% backdated; QK-16 60 orphans.
    # Lag has a long tail, skewed toward dual-region reps (QK-06) so P6's
    # "why are orders late?" has a findable cause in the data.
    shipments = []
    sno = 0
    for o in non_cancelled:
        if o["order_date"] > d(2026, 6, 20):
            continue
        sno += 1
        u = rng.random()
        if o["sales_rep_id"] in dual_reps:
            u = min(1.0, u / 0.55)         # overlapping-territory reps lag more
        if u < 0.70:
            lag = rng.randrange(2, 5)      # on time: 2-4d
        elif u < 0.90:
            lag = rng.randrange(5, 9)      # standard: 5-8d
        elif u < 0.98:
            lag = rng.randrange(9, 16)     # late: 9-15d
        else:
            lag = rng.randrange(16, 31)    # stalled: 16-30d
        sdate = o["order_date"] + dt.timedelta(days=lag)
        shipments.append({"shipment_id": f"S{sno:05d}", "order_id": o["order_id"],
                          "ship_date": sdate, "is_partial": False,
                          "event_sequence": 1})
        if rng.random() < P_PARTIAL_SHIP:
            sno += 1
            shipments.append({"shipment_id": f"S{sno:05d}",
                              "order_id": o["order_id"],
                              "ship_date": sdate + dt.timedelta(days=2),
                              "is_partial": True, "event_sequence": 2})
    for s in shipments:
        if rng.random() < P_LATE_SHIP:
            back = orders_by_id[s["order_id"]]
            s["ship_date"] = back["order_date"] - dt.timedelta(
                days=rng.randrange(1, 4))          # QK-15
    for k in range(n(N_ORPHAN_SHIP)):              # QK-16
        sno += 1
        shipments.append({"shipment_id": f"S{sno:05d}",
                          "order_id": "ORD-000000",
                          "ship_date": d(2026, 2, 1) + dt.timedelta(days=rng.randrange(120)),
                          "is_partial": False, "event_sequence": 1})

    # --------------------------------------------------------------- tickets
    # QK-12: 12 companies share one domain; 20% NULL customer.
    tickets = []
    # sorted(): set iteration order is hash-salted per process -> non-deterministic
    shared_codes = [code_of[cid] for cid in sorted(shared_domain_ids) if cid in code_of]
    for k in range(n(N_TICKETS)):
        if rng.random() < 0.20:
            code, email = "", ""
        else:
            code = rng.choice(shared_codes) if rng.random() < 0.25 else \
                rng.choice([c for c in code_of.values() if c])
            local = f"{rng.choice(FIRSTS).lower()}.{rng.choice(LASTS).lower()}"
            domain = SHARED_DOMAIN if code in shared_codes and rng.random() < 0.8 \
                else rng.choice(DOMAINS)
            email = f"{local}@{domain}"
        tickets.append({"ticket_id": f"T{k+1:06d}", "customer_code": code,
                        "contact_email": email,
                        "created_date": d(2025, 3, 1) + dt.timedelta(days=rng.randrange(480)),
                        "subject": f"{rng.choice(['Late delivery', 'Damaged item', 'Invoice query', 'Return request', 'Quote request'])} #{k+1}"})

    # -------------------------------------------------------------- contacts
    contacts = []
    for k in range(n(N_CONTACTS)):
        code = rng.choice([c for c in code_of.values() if c])
        first, last = rng.choice(FIRSTS), rng.choice(LASTS)
        domain = SHARED_DOMAIN if code in shared_codes else rng.choice(DOMAINS)
        contacts.append({"contact_id": f"CT{k+1:05d}", "customer_code": code,
                         "person_name": f"{first} {last}",
                         "email": f"{first.lower()}.{last.lower()}@{domain}"})

    # ------------------------------------------------------------------- CRM
    # QK-18: annual_value sums to ERP booked total x 1.018.
    erp_booked = sum(i["invoice_amount"] for i in invoices)
    crm = []
    crm_pool = [c for c in customers if c["is_current"]]
    crm_matched = rng.sample(crm_pool, len(crm_pool) - N_CRM_ONLY)
    raw_vals = [round(rng.lognormvariate(9.5, 1.1)) for _ in range(len(crm_pool))]
    scale_crm = (erp_booked * CRM_OVERSTATE) / max(1, sum(raw_vals))
    for k, row_cust in enumerate(crm_matched):
        crm.append({"crm_account_id": f"A{k+1:05d}",
                    "customer_id": row_cust["customer_id"],
                    "account_name": row_cust["name"],
                    "annual_value": round(raw_vals[k] * scale_crm),
                    "pipeline_stage": rng.choice(
                        ["CLOSED_WON", "CLOSED_WON", "OPEN", "OPEN", "AT_RISK"])})
    for j in range(N_CRM_ONLY):   # CRM-only accounts with no ERP match
        k = len(crm_matched) + j
        name = f"{rng.choice(CO_PREFIX)} {rng.choice(CO_SUFFIX)} Ventures"
        crm.append({"crm_account_id": f"A{k+1:05d}",
                    "customer_id": "",
                    "account_name": name,
                    "annual_value": round(raw_vals[k] * scale_crm),
                    "pipeline_stage": rng.choice(["OPEN", "AT_RISK"])})

    # ------------------------------------------------------------------ emit
    tables = {
        "customers": (customers, ["customer_id", "name", "region", "contract_active",
                                  "contract_end", "valid_from", "valid_to",
                                  "is_current", "loaded_at", "customer_type"]),
        "customer_xref": (xref, ["erp_code", "customer_id", "is_primary"]),
        "accounts_crm": (crm, ["crm_account_id", "customer_id", "account_name",
                               "annual_value", "pipeline_stage"]),
        "customer_contacts": (contacts, ["contact_id", "customer_code",
                                         "person_name", "email"]),
        "products": (products, ["product_id", "product_name", "unit_price", "unit_cost"]),
        "product_line_map": (line_map, ["product_id", "line_name", "is_primary",
                                        "valid_from", "valid_to"]),
        "regions": ([{"region_name": r, "country": "USA"} for r in REGIONS],
                    ["region_name", "country"]),
        "region_assignment": ([{"rep_id": rid, "rep_name": f"Rep {rid}",
                                "region_name": reg, "is_primary": prim}
                               for rid, regs in rep_region.items()
                               for reg, prim in regs],
                              ["rep_id", "rep_name", "region_name", "is_primary"]),
        "orders": (orders, ["order_id", "customer_code", "sales_rep_id",
                            "order_date", "status", "currency", "fx_rate_date"]),
        "order_lines": (order_lines, ["line_id", "order_id", "product_id", "qty",
                                      "unit_price", "unit_cost", "line_amount"]),
        "invoices": (invoices, ["invoice_id", "order_id", "invoice_date",
                                "invoice_amount", "loaded_at"]),
        "payments": (payments, ["payment_id", "invoice_id", "pay_date", "pay_amount"]),
        "returns": (returns, ["return_id", "line_id", "return_date", "return_amount"]),
        "shipments": (shipments, ["shipment_id", "order_id", "ship_date",
                                  "is_partial", "event_sequence"]),
        "support_tickets": (tickets, ["ticket_id", "customer_code", "contact_email",
                                      "created_date", "subject"]),
        "fx_rates": (fx, ["rate_date", "currency", "rate_usd"]),
    }
    manifest = {}
    for name, (rows, cols) in tables.items():
        path = OUT / f"{name}.csv"
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows:
                w.writerow({c: (r[c].strftime(FMT) if isinstance(r[c], dt.date)
                                and r[c] != NEVER else
                                ("9999-12-31" if isinstance(r[c], dt.date) else r[c]))
                            for c in cols})
        manifest[name] = len(rows)

    (OUT / "manifest.json").write_text(str(manifest).replace("'", '"'))
    print(f"seed={args.seed} scale={scale}")
    for name, count in manifest.items():
        print(f"  {name:20s} {count:>7,}")
    print(f"Acme split orders: {acme_alloc}")
    print(f"ERP booked total:  {erp_booked:,}")


if __name__ == "__main__":
    main()
