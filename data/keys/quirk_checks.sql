-- Quirk proofs — one check per planted quirk QK-01..QK-18.
-- Executed by run_checks.py (SQLite loader, same CSVs as keys).
-- The same statements run on Databricks in WP2 (date arithmetic uses
-- julianday(); swap for datediff() there).
--
-- Directive format parsed by the runner:
--   -- @check <ID> expect <min>:<max>   (inclusive; 'exact' == min==max)

-- @check QK-01 expect 250:350   cancelled orders carry non-zero lines
SELECT COUNT(*) FROM orders o
WHERE o.status = 'CANCELLED'
  AND EXISTS (SELECT 1 FROM order_lines l WHERE l.order_id = o.order_id);

-- @check QK-02 expect 380:380   returns table populated at the documented rate
SELECT COUNT(*) FROM returns;

-- @check QK-03 expect 400:750   invoices lag order date by >= 5 days
SELECT COUNT(*) FROM invoices i JOIN orders o USING(order_id)
WHERE julianday(i.invoice_date) - julianday(o.order_date) >= 5;

-- @check QK-04 expect 36:36     two FX rate dates per month, 18 months
SELECT COUNT(*) FROM fx_rates;

-- @check QK-05 expect 80:80     products sitting in 2 product lines (M:N)
SELECT COUNT(*) FROM (
  SELECT product_id FROM product_line_map GROUP BY product_id HAVING COUNT(*) > 1);

-- @check QK-06 expect 6:6       reps assigned to 2 regions
SELECT COUNT(*) FROM (
  SELECT rep_id FROM region_assignment GROUP BY rep_id HAVING COUNT(*) > 1);

-- @check QK-07 expect 200:350   February (fiscal-year start) order volume exists
SELECT COUNT(*) FROM orders
WHERE order_date >= '2026-02-01' AND order_date < '2026-03-01';

-- @check QK-08 expect 600:600   customers whose history has a closed-off version
-- (600 true SCD2 changes; the 40 QK-09 restatements keep valid_to open by design)
SELECT COUNT(DISTINCT customer_id) FROM customers WHERE valid_to < '9999-12-31';

-- @check QK-09 expect 40:40     post-close restatement loads on 2026-04-05
SELECT COUNT(*) FROM customers WHERE loaded_at = '2026-04-05';

-- @check QK-10 expect 1:1       exactly one entity with two ERP codes (Acme)
SELECT COUNT(*) FROM (
  SELECT customer_id FROM customer_xref GROUP BY customer_id HAVING COUNT(*) > 1);

-- @check QK-11 expect 2:2       the Acme near-name pair (Corp + Logistics Group)
SELECT COUNT(*) FROM customers
WHERE name IN ('Acme Corp', 'Acme Logistics Group');

-- @check QK-12 expect 12:20     distinct customers sharing the consultinghub.io domain
SELECT COUNT(DISTINCT customer_code) FROM support_tickets
WHERE contact_email LIKE '%@consultinghub.io';

-- @check QK-13 expect 2100:2100 contact rows exist (PII surface for P5)
SELECT COUNT(*) FROM customer_contacts;

-- @check QK-14 expect 0:0       orders carry NO region column (P5 structural basis)
-- (structural check: runner inspects the orders schema)

-- @check QK-15 expect 120:300   shipments dated before their order (data-entry glitch)
SELECT COUNT(*) FROM shipments s JOIN orders o USING(order_id)
WHERE s.ship_date < o.order_date;

-- @check QK-16 expect 60:60     orphan shipments referencing ORD-000000
SELECT COUNT(*) FROM shipments WHERE order_id = 'ORD-000000';

-- @check QK-17 expect 1:1       two 'active' definitions produce different counts
SELECT CASE WHEN (SELECT COUNT(DISTINCT customer_code) FROM orders
                  WHERE order_date >= '2026-04-01')
          != (SELECT COUNT(*) FROM customers
              WHERE is_current = 1 AND contract_active = 1)
       THEN 1 ELSE 0 END;

-- @check QK-18 expect 1:1       CRM annual value overstates ERP booked by ~1.8%
SELECT CASE WHEN ABS(
  (SELECT SUM(annual_value) FROM accounts_crm) * 1.0
/ (SELECT SUM(invoice_amount) FROM invoices) - 1.018) < 0.01
  THEN 1 ELSE 0 END;
