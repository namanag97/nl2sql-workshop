-- Meridian Trading Co. — order-to-cash estate
-- Dialect: Databricks SQL (also loads in DuckDB unchanged).
-- Raw state = NO primary/foreign key metadata, NO governed views:
-- attendees add governance themselves in Arc 2 (cards C6/C7).
-- All money columns are whole dollars (BIGINT) — no floats in sums.

CREATE SCHEMA IF NOT EXISTS o2c;

CREATE TABLE IF NOT EXISTS o2c.customers (
  customer_id     STRING,
  name            STRING,
  region          STRING,
  contract_active BOOLEAN,
  contract_end    DATE,
  valid_from      DATE,
  valid_to        DATE,
  is_current      BOOLEAN,
  loaded_at       DATE,      -- transaction time: restatements (QK-09) live here
  customer_type   STRING
);

CREATE TABLE IF NOT EXISTS o2c.customer_xref (
  erp_code    STRING,        -- ORDERS reference this; one entity may have two codes (QK-10)
  customer_id STRING,
  is_primary  BOOLEAN
);

CREATE TABLE IF NOT EXISTS o2c.accounts_crm (
  crm_account_id STRING,
  customer_id    STRING,     -- NULL = CRM-only account (no ERP match)
  account_name   STRING,
  annual_value   BIGINT,     -- pipeline-booked value; total ~1.8% above ERP booked (QK-18)
  pipeline_stage STRING
);

CREATE TABLE IF NOT EXISTS o2c.customer_contacts (
  contact_id   STRING,
  customer_code STRING,     -- ERP code
  person_name  STRING,
  email        STRING       -- PII-ish (QK-13); shared domain across 12 companies (QK-12)
);

CREATE TABLE IF NOT EXISTS o2c.products (
  product_id   STRING,
  product_name STRING,
  unit_price   BIGINT,
  unit_cost    BIGINT
);

CREATE TABLE IF NOT EXISTS o2c.product_line_map (
  product_id  STRING,
  line_name   STRING,
  is_primary  BOOLEAN,
  valid_from  DATE,
  valid_to    DATE          -- 80 products sit in 2 lines (QK-05: many-to-many)
);

CREATE TABLE IF NOT EXISTS o2c.regions (
  region_name STRING,
  country     STRING
);

CREATE TABLE IF NOT EXISTS o2c.region_assignment (
  rep_id      STRING,
  rep_name    STRING,
  region_name STRING,
  is_primary  BOOLEAN       -- 6 reps hold a second, non-primary region (QK-06)
);

CREATE TABLE IF NOT EXISTS o2c.orders (
  order_id      STRING,
  customer_code STRING,    -- ERP code (not customer_id: identity is a join away)
  sales_rep_id  STRING,
  order_date    DATE,
  status        STRING,    -- 6% CANCELLED with non-zero amounts (QK-01)
  currency      STRING,    -- 3% EUR (QK-04)
  fx_rate_date  DATE
);

CREATE TABLE IF NOT EXISTS o2c.order_lines (
  line_id     STRING,
  order_id    STRING,
  product_id  STRING,
  qty         BIGINT,
  unit_price  BIGINT,
  unit_cost   BIGINT,
  line_amount BIGINT
);

CREATE TABLE IF NOT EXISTS o2c.invoices (
  invoice_id     STRING,
  order_id       STRING,
  invoice_date   DATE,     -- 12% lag order date by ~9 days (QK-03)
  invoice_amount BIGINT,
  loaded_at      DATE      -- 30 late-arriving rows (loaded after March close)
);

CREATE TABLE IF NOT EXISTS o2c.payments (
  payment_id   STRING,
  invoice_id   STRING,
  pay_date     DATE,
  pay_amount   BIGINT
);

CREATE TABLE IF NOT EXISTS o2c.returns (
  return_id     STRING,
  line_id       STRING,
  return_date   DATE,
  return_amount BIGINT      -- naive revenue ignores this table (QK-02)
);

CREATE TABLE IF NOT EXISTS o2c.shipments (
  shipment_id    STRING,
  order_id       STRING,   -- 60 rows reference ORD-000000 (QK-16 orphans)
  ship_date      DATE,     -- 4% earlier than order date (QK-15)
  is_partial     BOOLEAN,
  event_sequence BIGINT
);

CREATE TABLE IF NOT EXISTS o2c.support_tickets (
  ticket_id     STRING,
  customer_code STRING,    -- 20% NULL (unknown requester)
  contact_email STRING,    -- 12 companies share one domain (QK-12)
  created_date  DATE,
  subject       STRING
);

CREATE TABLE IF NOT EXISTS o2c.fx_rates (
  rate_date DATE,
  currency  STRING,
  rate_usd  DOUBLE         -- two rate dates per month (QK-04: order- vs invoice-date)
);
