"""
SQL Concepts Practice (using sqlite3)
=======================================
Examples: table creation with keys, join queries, aggregate queries, transactions.
"""

import sqlite3


def demo_sql_concepts():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=" * 55)
    print("  SQL CONCEPTS PRACTICE (sqlite3)")
    print("=" * 55)

    # ============================================================
    # 1. TABLES WITH KEYS
    # ============================================================
    print("\n--- Table Creation with Keys ---")
    cursor.executescript("""
        CREATE TABLE departments (
            dept_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            budget REAL DEFAULT 0
        );

        CREATE TABLE employees (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dept_id INTEGER,
            salary REAL NOT NULL,
            hire_date TEXT,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        );

        CREATE TABLE projects (
            project_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            dept_id INTEGER,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        );

        CREATE TABLE assignments (
            emp_id INTEGER,
            project_id INTEGER,
            hours_worked REAL DEFAULT 0,
            PRIMARY KEY (emp_id, project_id),
            FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
            FOREIGN KEY (project_id) REFERENCES projects(project_id)
        );
    """)
    print("   Created: departments, employees, projects, assignments")

    # Load data
    cursor.executemany("INSERT INTO departments VALUES (?,?,?)", [
        (1, "Engineering", 5000000), (2, "Sales", 2000000),
        (3, "HR", 1000000), (4, "Marketing", 1500000),
    ])

    cursor.executemany(
        "INSERT INTO employees (name, dept_id, salary, hire_date) VALUES (?,?,?,?)", [
        ("Alice", 1, 120000, "2022-01-15"), ("Bob", 1, 95000, "2023-06-01"),
        ("Charlie", 2, 85000, "2023-09-10"), ("Diana", 2, 110000, "2021-03-20"),
        ("Eve", 3, 90000, "2022-07-15"), ("Frank", 1, 105000, "2024-01-10"),
        ("Grace", 4, 88000, "2023-05-01"), ("Hank", None, 70000, "2024-06-01"),
    ])

    cursor.executemany("INSERT INTO projects VALUES (?,?,?)", [
        (1, "Cloud Migration", 1), (2, "CRM Overhaul", 2),
        (3, "HR Portal", 3), (4, "Marketing AI", 4),
    ])

    cursor.executemany("INSERT INTO assignments VALUES (?,?,?)", [
        (1, 1, 120), (2, 1, 80), (6, 1, 60),
        (3, 2, 100), (4, 2, 90), (1, 4, 30),
        (5, 3, 110), (7, 4, 95),
    ])
    conn.commit()

    # ============================================================
    # 2. JOIN QUERIES
    # ============================================================
    print("\n--- INNER JOIN ---")
    rows = cursor.execute("""
        SELECT e.name, d.name as department, e.salary
        FROM employees e
        INNER JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY e.salary DESC
    """).fetchall()
    for r in rows:
        print(f"  {r['name']:<12} {r['department']:<15} ₹{r['salary']:>10,.2f}")

    print("\n--- LEFT JOIN (includes unassigned) ---")
    rows = cursor.execute("""
        SELECT e.name, COALESCE(d.name, 'Unassigned') as department
        FROM employees e
        LEFT JOIN departments d ON e.dept_id = d.dept_id
    """).fetchall()
    for r in rows:
        print(f"  {r['name']:<12}  {r['department']}")

    print("\n--- Multi-table JOIN ---")
    rows = cursor.execute("""
        SELECT e.name as employee, p.name as project, a.hours_worked,
               d.name as department
        FROM assignments a
        JOIN employees e ON a.emp_id = e.emp_id
        JOIN projects p ON a.project_id = p.project_id
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY a.hours_worked DESC
    """).fetchall()
    print(f"  {'Employee':<12} {'Project':<18} {'Dept':<15} {'Hours':>6}")
    print(f"  {''*51}")
    for r in rows:
        print(f"  {r['employee']:<12} {r['project']:<18} {r['department']:<15} {r['hours_worked']:>6.0f}")

    # ============================================================
    # 3. AGGREGATE QUERIES
    # ============================================================
    print("\n--- Aggregate Queries ---")

    # Department stats
    rows = cursor.execute("""
        SELECT d.name,
               COUNT(e.emp_id) as headcount,
               ROUND(AVG(e.salary), 2) as avg_salary,
               MIN(e.salary) as min_salary,
               MAX(e.salary) as max_salary,
               SUM(e.salary) as total_salary
        FROM departments d
        LEFT JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_id
        HAVING headcount > 0
        ORDER BY avg_salary DESC
    """).fetchall()
    print(f"  {'Dept':<15} {'Count':>6} {'Avg Salary':>12} {'Min':>10} {'Max':>10}")
    print(f"  {''*53}")
    for r in rows:
        print(f"  {r['name']:<15} {r['headcount']:>6} ₹{r['avg_salary']:>10,.2f} "
              f"₹{r['min_salary']:>8,.0f} ₹{r['max_salary']:>8,.0f}")

    # ============================================================
    # 4. SUBQUERY
    # ============================================================
    print("\n--- Subquery: Above-average salary ---")
    rows = cursor.execute("""
        SELECT name, salary
        FROM employees
        WHERE salary > (SELECT AVG(salary) FROM employees)
        ORDER BY salary DESC
    """).fetchall()
    for r in rows:
        print(f"  {r['name']:<12} ₹{r['salary']:>10,.2f}")

    # ============================================================
    # 5. TRANSACTIONS
    # ============================================================
    print("\n--- Transaction Demo ---")

    # Successful transaction: transfer budget
    try:
        cursor.execute("UPDATE departments SET budget = budget - 500000 WHERE dept_id = 1")
        cursor.execute("UPDATE departments SET budget = budget + 500000 WHERE dept_id = 4")
        conn.commit()
        print("   Budget transfer committed (Eng  Marketing: ₹5L)")
    except Exception as e:
        conn.rollback()
        print(f"   Rolled back: {e}")

    # Verify
    rows = cursor.execute("SELECT name, budget FROM departments ORDER BY dept_id").fetchall()
    for r in rows:
        print(f"  {r['name']:<15} Budget: ₹{r['budget']:>12,.2f}")

    conn.close()
    print(f"\n{'='*55}")


if __name__ == "__main__":
    demo_sql_concepts()
