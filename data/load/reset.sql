-- Reset kit — run between rehearsals/sessions to restore the raw state.
-- Raw = no governed view, no team scratch schemas, no constraint annotations
-- beyond what the C7 card re-declares each time.
-- (Databricks SQL; run as workspace admin on the workshop warehouse.)

-- 1. Drop the governed view attendees build with card C6.
DROP VIEW IF EXISTS nl2sql_ws.o2c.v_revenue_governed;

-- 2. Drop team scratch schemas (pattern per room numbering).
DROP SCHEMA IF EXISTS nl2sql_ws.o2c_team1 CASCADE;
DROP SCHEMA IF EXISTS nl2sql_ws.o2c_team2 CASCADE;
DROP SCHEMA IF EXISTS nl2sql_ws.o2c_team3 CASCADE;
DROP SCHEMA IF EXISTS nl2sql_ws.o2c_team4 CASCADE;
DROP SCHEMA IF EXISTS nl2sql_ws.o2c_team5 CASCADE;
DROP SCHEMA IF EXISTS nl2sql_ws.o2c_team6 CASCADE;

-- 3. Drop constraint annotations left by C7 (informational; re-declared live).
ALTER TABLE nl2sql_ws.o2c.orders DROP CONSTRAINT IF EXISTS pk_orders;
ALTER TABLE nl2sql_ws.o2c.order_lines DROP CONSTRAINT IF EXISTS pk_order_lines;
ALTER TABLE nl2sql_ws.o2c.order_lines DROP CONSTRAINT IF EXISTS fk_order_lines_orders;
ALTER TABLE nl2sql_ws.o2c.products DROP CONSTRAINT IF EXISTS pk_products;
ALTER TABLE nl2sql_ws.o2c.customers DROP CONSTRAINT IF EXISTS pk_customers;

-- 4. Sanity: raw tables untouched (these must NEVER be reset — attendees
--    only read them). Verify counts before declaring the room ready:
SELECT 'orders' t, COUNT(*) n FROM nl2sql_ws.o2c.orders
UNION ALL SELECT 'order_lines', COUNT(*) FROM nl2sql_ws.o2c.order_lines
UNION ALL SELECT 'customers', COUNT(*) FROM nl2sql_ws.o2c.customers;
-- Expected: 4,833 / 16,874 / 2,640 (manifest.json is the authority).
