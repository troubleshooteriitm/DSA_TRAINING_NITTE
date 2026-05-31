"""
Enterprise Data Warehouse & Reporting System
==============================================
Corporate Use Case: Star schema with sqlite3, complex SQL joins,
aggregations, and formatted reports.
"""

import sqlite3
from datetime import datetime, timedelta
import random

random.seed(42)


def setup_data_warehouse():
    """Create star schema and load sample data."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create dimension and fact tables
    cursor.executescript("""
        CREATE TABLE dim_product (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            brand TEXT NOT NULL,
            unit_price REAL NOT NULL
        );

        CREATE TABLE dim_customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            segment TEXT NOT NULL,
            city TEXT NOT NULL,
            region TEXT NOT NULL
        );

        CREATE TABLE dim_date (
            date_id INTEGER PRIMARY KEY,
            full_date TEXT NOT NULL,
            year INTEGER,
            month INTEGER,
            month_name TEXT,
            quarter INTEGER,
            day_of_week TEXT
        );

        CREATE TABLE fact_sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_id INTEGER,
            date_id INTEGER,
            quantity INTEGER NOT NULL,
            revenue REAL NOT NULL,
            discount REAL DEFAULT 0,
            FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
            FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
            FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
        );
    """)

    # Load dimension: Products
    products = [
        (1, "Laptop Pro", "Electronics", "TechBrand", 75000),
        (2, "Wireless Mouse", "Accessories", "PeriphCo", 500),
        (3, "4K Monitor", "Electronics", "DisplayMax", 25000),
        (4, "Mechanical Keyboard", "Accessories", "KeyMaster", 3500),
        (5, "SSD 1TB", "Storage", "DataFast", 5000),
        (6, "USB-C Hub", "Accessories", "ConnectAll", 2000),
        (7, "Webcam HD", "Accessories", "ClearView", 3000),
        (8, "Server Rack", "Infrastructure", "RackPro", 150000),
    ]
    cursor.executemany("INSERT INTO dim_product VALUES (?,?,?,?,?)", products)

    # Load dimension: Customers
    customers = [
        (1, "TechCorp Solutions", "Enterprise", "Mumbai", "West"),
        (2, "DataSoft Inc", "Enterprise", "Bangalore", "South"),
        (3, "InfoSystems Ltd", "Mid-Market", "Delhi", "North"),
        (4, "CloudNet Services", "SMB", "Chennai", "South"),
        (5, "DigiTech Pvt Ltd", "Mid-Market", "Hyderabad", "South"),
        (6, "NorthStar IT", "Enterprise", "Pune", "West"),
        (7, "EastWind Solutions", "SMB", "Kolkata", "East"),
        (8, "GreenLeaf Tech", "SMB", "Jaipur", "North"),
    ]
    cursor.executemany("INSERT INTO dim_customer VALUES (?,?,?,?,?)", customers)

    # Load dimension: Dates (Jan-May 2025)
    base = datetime(2025, 1, 1)
    month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May"}
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    dates = []
    for i in range(150):  # ~5 months
        d = base + timedelta(days=i)
        dates.append((
            i + 1, d.strftime("%Y-%m-%d"), d.year, d.month,
            month_names.get(d.month, d.strftime("%B")),
            (d.month - 1) // 3 + 1, day_names[d.weekday()]
        ))
    cursor.executemany("INSERT INTO dim_date VALUES (?,?,?,?,?,?,?)", dates)

    # Load fact: Sales (40+ records)
    sales = []
    for _ in range(50):
        product_id = random.randint(1, 8)
        customer_id = random.randint(1, 8)
        date_id = random.randint(1, 150)
        qty = random.randint(1, 20)
        price = products[product_id - 1][4]
        discount = random.choice([0, 0, 0, 5, 10, 15])
        revenue = qty * price * (1 - discount / 100)
        sales.append((product_id, customer_id, date_id, qty, round(revenue, 2), discount))

    cursor.executemany(
        "INSERT INTO fact_sales (product_id, customer_id, date_id, quantity, revenue, discount) VALUES (?,?,?,?,?,?)",
        sales
    )
    conn.commit()
    return conn


def run_reports(conn):
    """Execute complex queries and generate reports."""
    cursor = conn.cursor()

    print("=" * 70)
    print("   ENTERPRISE DATA WAREHOUSE & REPORTING SYSTEM")
    print("=" * 70)

    #  Report 1: Sales by Product Category 
    print(f"\n{''*70}")
    print("   SALES BY PRODUCT CATEGORY")
    print(f"{''*70}")
    rows = cursor.execute("""
        SELECT p.category,
               COUNT(*) as num_orders,
               SUM(f.quantity) as total_qty,
               ROUND(SUM(f.revenue), 2) as total_revenue,
               ROUND(AVG(f.revenue), 2) as avg_order_value
        FROM fact_sales f
        JOIN dim_product p ON f.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """).fetchall()

    print(f"  {'Category':<18} {'Orders':>7} {'Qty':>6} {'Revenue':>15} {'Avg Order':>12}")
    print(f"  {''*58}")
    for r in rows:
        print(f"  {r['category']:<18} {r['num_orders']:>7} {r['total_qty']:>6} "
              f"₹{r['total_revenue']:>13,.2f} ₹{r['avg_order_value']:>10,.2f}")

    #  Report 2: Top Customers 
    print(f"\n{''*70}")
    print("   TOP CUSTOMERS BY REVENUE")
    print(f"{''*70}")
    rows = cursor.execute("""
        SELECT c.name, c.segment, c.region,
               COUNT(*) as orders,
               ROUND(SUM(f.revenue), 2) as total_revenue
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        GROUP BY c.customer_id
        ORDER BY total_revenue DESC
        LIMIT 5
    """).fetchall()

    print(f"  {'Customer':<22} {'Segment':<12} {'Region':<8} {'Orders':>7} {'Revenue':>15}")
    print(f"  {''*64}")
    for r in rows:
        print(f"  {r['name']:<22} {r['segment']:<12} {r['region']:<8} "
              f"{r['orders']:>7} ₹{r['total_revenue']:>13,.2f}")

    #  Report 3: Monthly Trends 
    print(f"\n{''*70}")
    print("   MONTHLY REVENUE TRENDS")
    print(f"{''*70}")
    rows = cursor.execute("""
        SELECT d.month_name, d.month,
               COUNT(*) as orders,
               ROUND(SUM(f.revenue), 2) as revenue
        FROM fact_sales f
        JOIN dim_date d ON f.date_id = d.date_id
        GROUP BY d.month
        ORDER BY d.month
    """).fetchall()

    max_rev = max(r["revenue"] for r in rows) if rows else 1
    for r in rows:
        bar_len = int(r["revenue"] / max_rev * 30)
        bar = "" * bar_len
        print(f"  {r['month_name']:<12} {r['orders']:>3} orders  ₹{r['revenue']:>13,.2f}  {bar}")

    #  Report 4: Region-wise Analysis (Complex JOIN) 
    print(f"\n{''*70}")
    print("    REGION-WISE ANALYSIS")
    print(f"{''*70}")
    rows = cursor.execute("""
        SELECT c.region,
               COUNT(DISTINCT c.customer_id) as customers,
               COUNT(*) as orders,
               ROUND(SUM(f.revenue), 2) as revenue,
               ROUND(AVG(f.discount), 1) as avg_discount
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        GROUP BY c.region
        ORDER BY revenue DESC
    """).fetchall()

    print(f"  {'Region':<10} {'Customers':>10} {'Orders':>8} {'Revenue':>15} {'Avg Disc%':>10}")
    print(f"  {''*53}")
    for r in rows:
        print(f"  {r['region']:<10} {r['customers']:>10} {r['orders']:>8} "
              f"₹{r['revenue']:>13,.2f} {r['avg_discount']:>9.1f}%")

    #  Report 5: Best Selling Products 
    print(f"\n{''*70}")
    print("   BEST SELLING PRODUCTS")
    print(f"{''*70}")
    rows = cursor.execute("""
        SELECT p.name, p.brand, p.category,
               SUM(f.quantity) as total_qty,
               ROUND(SUM(f.revenue), 2) as total_revenue
        FROM fact_sales f
        JOIN dim_product p ON f.product_id = p.product_id
        GROUP BY f.product_id
        ORDER BY total_qty DESC
    """).fetchall()

    for i, r in enumerate(rows, 1):
        print(f"  {i}. {r['name']:<22} ({r['brand']})  "
              f"Qty: {r['total_qty']:>4}  Revenue: ₹{r['total_revenue']:>12,.2f}")

    print(f"\n{'='*70}")


if __name__ == "__main__":
    conn = setup_data_warehouse()
    run_reports(conn)
    conn.close()
