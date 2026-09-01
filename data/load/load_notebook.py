# Databricks load notebook — paste each COMMAND block into a notebook cell.
# WP2: cold-start target < 15 min from empty workspace to "C0 card passes".
#
# Prereqs (workspace admin, one-time):
#   1. A UC Volume for the CSVs, e.g. /Volumes/nl2sql_ws/staging/data
#      — upload the contents of data/out/ there (manifest.json included).
#   2. A Serverless SQL warehouse (Small, auto-stop 30 min); note its ID.
#   3. Attendee group with READ on catalog nl2sql_ws, WRITE only on
#      o2c_team* schemas.

# COMMAND ----------
dbutils.widgets.text("catalog", "nl2sql_ws")
dbutils.widgets.text("volume_path", "/Volumes/nl2sql_ws/staging/data")
CATALOG = dbutils.widgets.get("catalog")
VOL = dbutils.widgets.get("volume_path")

# COMMAND ----------
spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.o2c")

# COMMAND ----------
DATE_COLS = {
    "customers": ["contract_end", "valid_from", "valid_to", "loaded_at"],
    "product_line_map": ["valid_from", "valid_to"],
    "orders": ["order_date", "fx_rate_date"],
    "invoices": ["invoice_date", "loaded_at"],
    "payments": ["pay_date"],
    "returns": ["return_date"],
    "shipments": ["ship_date"],
    "support_tickets": ["created_date"],
    "fx_rates": ["rate_date"],
}
BOOL_COLS = {
    "customers": ["contract_active", "is_current"],
    "customer_xref": ["is_primary"],
    "product_line_map": ["is_primary"],
    "region_assignment": ["is_primary"],
    "shipments": ["is_partial"],
}
INT_COLS = {
    "accounts_crm": ["annual_value"],
    "products": ["unit_price", "unit_cost"],
    "orders": [],
    "order_lines": ["qty", "unit_price", "unit_cost", "line_amount"],
    "invoices": ["invoice_amount"],
    "payments": ["pay_amount"],
    "returns": ["return_amount"],
    "shipments": ["event_sequence"],
}

TABLES = ["customers", "customer_xref", "accounts_crm", "customer_contacts",
          "products", "product_line_map", "regions", "region_assignment",
          "orders", "order_lines", "invoices", "payments", "returns",
          "shipments", "support_tickets", "fx_rates"]

# COMMAND ----------
for table in TABLES:
    df = (spark.read
          .option("header", "true")
          .option("nullValue", "")
          .csv(f"{VOL}/{table}.csv"))
    exprs = []
    for c in df.columns:
        if c in DATE_COLS.get(table, []):
            t = "DATE"
        elif c in BOOL_COLS.get(table, []):
            t = "BOOLEAN"
        elif c in INT_COLS.get(table, []):
            t = "BIGINT"
        else:
            t = "DOUBLE" if (table == "fx_rates" and c == "rate_usd") else "STRING"
        exprs.append(f"CAST(`{c}` AS {t}) AS `{c}`")
    df.selectExpr(*exprs).write.mode("overwrite").saveAsTable(
        f"{CATALOG}.o2c.{table}")
    print(f"loaded {table}: {df.count():,} rows")

# COMMAND ----------
# Verify against the generator manifest — fail loudly on any drift.
import json
manifest = json.loads(dbutils.fs.head(f"{VOL}/manifest.json"))
bad = []
for table, expected in manifest.items():
    got = spark.table(f"{CATALOG}.o2c.{table}").count()
    status = "OK " if got == expected else "DRIFT"
    if got != expected:
        bad.append(table)
    print(f"{status} {table:20s} {got:>8,} (expected {expected:,})")
assert not bad, f"row-count drift in: {bad}"
print("\nALL 16 TABLES VERIFIED — room is ready for card C0.")

# COMMAND ----------
# Facilitator probe before doors: the Arc-1 baseline number.
spark.sql(f"SELECT SUM(line_amount) AS naive_all_time FROM {CATALOG}.o2c.order_lines").show()
