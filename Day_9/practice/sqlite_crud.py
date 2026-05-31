"""
SQLite3 CRUD Operations Practice
==================================
Examples: create database, create table, insert, select, update, delete, transactions.
"""

import sqlite3


def demo_crud():
    """Complete CRUD demonstration with sqlite3."""

    print("=" * 50)
    print("  SQLITE3 CRUD PRACTICE")
    print("=" * 50)

    # Connect to in-memory database
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ============================================================
    # CREATE TABLE
    # ============================================================
    print("\n--- CREATE TABLE ---")
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   Products table created")

    # ============================================================
    # INSERT (Create)
    # ============================================================
    print("\n--- INSERT ---")

    # Single insert
    cursor.execute(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        ("Laptop", "Electronics", 75000, 10)
    )

    # Batch insert with executemany
    products = [
        ("Mouse", "Accessories", 500, 100),
        ("Keyboard", "Accessories", 2500, 50),
        ("Monitor", "Electronics", 25000, 20),
        ("Headphones", "Accessories", 3000, 75),
        ("SSD 1TB", "Storage", 5000, 30),
        ("Webcam", "Accessories", 3500, 40),
        ("USB Hub", "Accessories", 800, 60),
    ]
    cursor.executemany(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        products
    )
    conn.commit()
    print(f"   Inserted {1 + len(products)} products")

    # ============================================================
    # SELECT (Read)
    # ============================================================
    print("\n--- SELECT ---")

    # Select all
    rows = cursor.execute("SELECT * FROM products").fetchall()
    print(f"\n  All products ({len(rows)}):")
    print(f"  {'ID':<4} {'Name':<15} {'Category':<15} {'Price':>8} {'Stock':>6}")
    print(f"  {''*48}")
    for row in rows:
        print(f"  {row['id']:<4} {row['name']:<15} {row['category']:<15} "
              f"₹{row['price']:>7,.0f} {row['stock']:>6}")

    # Select with WHERE
    print("\n  Electronics only:")
    electronics = cursor.execute(
        "SELECT name, price FROM products WHERE category = ? ORDER BY price DESC",
        ("Electronics",)
    ).fetchall()
    for row in electronics:
        print(f"    {row['name']}: ₹{row['price']:,.0f}")

    # Aggregate queries
    print("\n  Aggregate queries:")
    stats = cursor.execute("""
        SELECT 
            COUNT(*) as total,
            ROUND(AVG(price), 2) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            SUM(stock) as total_stock
        FROM products
    """).fetchone()
    print(f"    Total products: {stats['total']}")
    print(f"    Avg price: ₹{stats['avg_price']:,.2f}")
    print(f"    Price range: ₹{stats['min_price']:,.0f} - ₹{stats['max_price']:,.0f}")
    print(f"    Total stock: {stats['total_stock']} units")

    # GROUP BY
    print("\n  Products per category:")
    groups = cursor.execute("""
        SELECT category, COUNT(*) as count, ROUND(AVG(price), 2) as avg_price
        FROM products
        GROUP BY category
        HAVING count >= 1
        ORDER BY count DESC
    """).fetchall()
    for row in groups:
        print(f"    {row['category']}: {row['count']} products (avg ₹{row['avg_price']:,.2f})")

    # ============================================================
    # UPDATE
    # ============================================================
    print("\n--- UPDATE ---")
    cursor.execute("UPDATE products SET price = price * 1.10 WHERE category = 'Electronics'")
    conn.commit()
    print(f"   10% price increase for Electronics ({cursor.rowcount} rows)")

    cursor.execute("UPDATE products SET stock = stock - 5 WHERE name = 'Mouse'")
    conn.commit()
    print(f"   Reduced Mouse stock by 5")

    # ============================================================
    # DELETE
    # ============================================================
    print("\n--- DELETE ---")
    cursor.execute("DELETE FROM products WHERE stock < 15")
    print(f"   Deleted products with stock < 15 ({cursor.rowcount} rows)")
    conn.commit()

    # ============================================================
    # TRANSACTIONS
    # ============================================================
    print("\n--- TRANSACTIONS ---")

    # Successful transaction
    try:
        cursor.execute("INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
                       ("Tablet", "Electronics", 35000, 15))
        cursor.execute("UPDATE products SET stock = stock + 10 WHERE name = 'Monitor'")
        conn.commit()
        print("   Transaction committed successfully")
    except Exception as e:
        conn.rollback()
        print(f"   Transaction rolled back: {e}")

    # Failed transaction (simulated)
    try:
        cursor.execute("INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
                       ("Phone", "Electronics", 50000, 25))
        # Simulate an error
        raise ValueError("Simulated business logic error!")
    except Exception as e:
        conn.rollback()
        print(f"   Transaction rolled back: {e}")

    # Verify Phone was NOT inserted
    phone = cursor.execute("SELECT * FROM products WHERE name = 'Phone'").fetchone()
    print(f"  Phone in DB? {phone is not None}")  # False

    # Final state
    print("\n--- FINAL STATE ---")
    rows = cursor.execute("SELECT * FROM products ORDER BY id").fetchall()
    print(f"  {'ID':<4} {'Name':<15} {'Category':<15} {'Price':>10} {'Stock':>6}")
    print(f"  {''*50}")
    for row in rows:
        print(f"  {row['id']:<4} {row['name']:<15} {row['category']:<15} "
              f"₹{row['price']:>9,.2f} {row['stock']:>6}")

    conn.close()


if __name__ == "__main__":
    demo_crud()
