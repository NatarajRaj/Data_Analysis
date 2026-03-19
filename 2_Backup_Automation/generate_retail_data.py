import os
import psycopg2
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv("config.env")

# Read DB config
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

# ----------------------------
# CREATE TABLES
# ----------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100),
    signup_date DATE
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    total_amount NUMERIC,
    order_date DATE
);
""")

conn.commit()

# ----------------------------
# GENERATE MASTER DATA (ONCE)
# ----------------------------

names = ["Arun", "Bala", "Charan", "Deepak", "Elan"]
cities = ["Chennai", "Bangalore", "Hyderabad"]
categories = ["Electronics", "Clothing", "Grocery"]

# Insert customers
cur.execute("SELECT COUNT(*) FROM customers")
if cur.fetchone()[0] == 0:
    for _ in range(50):
        cur.execute(
            "INSERT INTO customers (name, city, signup_date) VALUES (%s, %s, %s)",
            (
                random.choice(names),
                random.choice(cities),
                datetime.now() - timedelta(days=random.randint(1, 365))
            )
        )

# Insert products
cur.execute("SELECT COUNT(*) FROM products")
if cur.fetchone()[0] == 0:
    for i in range(50):
        cur.execute(
            "INSERT INTO products (product_name, category, price) VALUES (%s, %s, %s)",
            (
                f"Product_{i}",
                random.choice(categories),
                random.randint(100, 1000)
            )
        )

conn.commit()

# ----------------------------
# DAILY DATA GENERATION
# ----------------------------

print("Starting daily data generation...")

today = datetime.now().date()

# Check if already inserted (idempotent)
cur.execute("SELECT COUNT(*) FROM orders WHERE order_date = %s", (today,))
existing = cur.fetchone()[0]

if existing > 0:
    print(f"Data already exists for {today}, skipping...")
else:
    print(f"Generating 100,000 records for {today}...")

    batch_size = 5000
    total_records = 100000

    for i in range(0, total_records, batch_size):
        data_batch = []

        for _ in range(batch_size):
            customer_id = random.randint(1, 50)
            product_id = random.randint(1, 50)
            quantity = random.randint(1, 5)
            price = random.randint(100, 1000)
            total_amount = quantity * price

            data_batch.append((
                customer_id,
                product_id,
                quantity,
                total_amount,
                today
            ))

        cur.executemany(
            """INSERT INTO orders 
            (customer_id, product_id, quantity, total_amount, order_date) 
            VALUES (%s, %s, %s, %s, %s)""",
            data_batch
        )

        conn.commit()
        print(f"Inserted {i + batch_size} records...")

    print("✅ Daily data generation completed")

# ----------------------------
# VERIFY
# ----------------------------

cur.execute("SELECT COUNT(*) FROM orders;")
print("Total Orders:", cur.fetchone()[0])

cur.close()
conn.close()

print("Script completed successfully.")