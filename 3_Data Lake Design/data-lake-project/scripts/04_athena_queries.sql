CREATE DATABASE IF NOT EXISTS lakehouse_demo;

CREATE EXTERNAL TABLE IF NOT EXISTS lakehouse_demo.orders (
  order_id string,
  customer_id string,
  order_ts timestamp,
  region string,
  status string,
  quantity int,
  unit_price double,
  discount double,
  net_amount double
)
PARTITIONED BY (
  year string,
  month string,
  day string
)
STORED AS PARQUET
LOCATION 's3://natarajan-de-2026-bucket-1/datalake/orders/'
TBLPROPERTIES ('parquet.compress'='SNAPPY');

MSCK REPAIR TABLE lakehouse_demo.orders;

SHOW PARTITIONS lakehouse_demo.orders;

-- Partition filters are mandatory.
SELECT
  year,
  month,
  day,
  COUNT(*) AS order_count,
  ROUND(SUM(net_amount), 2) AS total_sales
FROM lakehouse_demo.orders
WHERE year = '2025'
  AND month = '01'
  AND day BETWEEN '01' AND '07'
GROUP BY year, month, day
ORDER BY year, month, day;

SELECT
  region,
  COUNT(*) AS delivered_orders,
  ROUND(AVG(net_amount), 2) AS avg_order_value
FROM lakehouse_demo.orders
WHERE year = '2025'
  AND month = '02'
  AND day = '14'
  AND status = 'delivered'
GROUP BY region
ORDER BY delivered_orders DESC;

-- Validation query with a single-day partition filter to keep scanned data tiny.
SELECT
  COUNT(*) AS orders_on_day,
  ROUND(SUM(net_amount), 2) AS sales_on_day
FROM lakehouse_demo.orders
WHERE year = '2025'
  AND month = '01'
  AND day = '10';

-- Single Day Analysis (Scans KB)

SELECT 
    category,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM lakehouse_demo.orders
WHERE year = 2025 AND month = 1 AND day = 10
GROUP BY category
ORDER BY total_revenue DESC;

-- Weekly Trend (Scans MB)

SELECT 
    day,
    COUNT(*) as orders,
    SUM(total_amount) as revenue
FROM lakehouse_demo.orders
WHERE year = 2025 AND month = 1 AND day BETWEEN 1 AND 7
GROUP BY day
ORDER BY day;

-- Regional Analysis (Scans KB)

SELECT 
    region,
    COUNT(*) as orders,
    SUM(total_amount) as revenue
FROM lakehouse_demo.orders
WHERE year = 2025 AND month = 2 AND day = 15
GROUP BY region
ORDER BY revenue DESC;