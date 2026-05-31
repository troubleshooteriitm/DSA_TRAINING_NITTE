"""
Enterprise Employee Database & Attendance Management System
=============================================================
Corporate Use Case: Full CRUD operations with sqlite3 in-memory database.
Tables: employees, attendance. Reports: attendance summary, department-wise, absentees.
"""

import sqlite3
from datetime import datetime, timedelta
import random

random.seed(42)


def create_database():
    """Create in-memory database with employees and attendance tables."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            salary REAL NOT NULL,
            join_date TEXT NOT NULL
        );

        CREATE TABLE attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            check_in TEXT,
            check_out TEXT,
            status TEXT NOT NULL DEFAULT 'present',
            FOREIGN KEY (emp_id) REFERENCES employees(id),
            UNIQUE(emp_id, date)
        );
    """)
    conn.commit()
    return conn


def seed_employees(conn):
    """Insert sample employees."""
    employees = [
        ("Priya Sharma", "Engineering", "Senior Developer", "priya@company.com", 120000, "2023-01-15"),
        ("Rahul Verma", "Engineering", "Developer", "rahul@company.com", 95000, "2023-06-01"),
        ("Sneha Reddy", "Engineering", "Tech Lead", "sneha@company.com", 150000, "2022-03-10"),
        ("Amit Patel", "Finance", "Analyst", "amit@company.com", 85000, "2023-09-01"),
        ("Neha Gupta", "Finance", "Manager", "neha@company.com", 140000, "2021-07-15"),
        ("Vikram Singh", "HR", "HR Manager", "vikram@company.com", 130000, "2022-01-20"),
        ("Meera Nair", "HR", "Recruiter", "meera@company.com", 75000, "2024-01-10"),
        ("Karthik Iyer", "Engineering", "Developer", "karthik@company.com", 90000, "2024-02-01"),
        ("Divya Menon", "Sales", "Sales Lead", "divya@company.com", 110000, "2023-04-15"),
        ("Arjun Kumar", "Sales", "Sales Rep", "arjun@company.com", 70000, "2024-03-01"),
    ]

    conn.executemany(
        "INSERT INTO employees (name, department, role, email, salary, join_date) VALUES (?,?,?,?,?,?)",
        employees
    )
    conn.commit()
    print(f"   Inserted {len(employees)} employees")


def seed_attendance(conn):
    """Generate attendance data for the past 5 workdays."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM employees")
    emp_ids = [row["id"] for row in cursor.fetchall()]

    base_date = datetime(2025, 5, 26)  # Monday
    records = 0

    for day_offset in range(5):  # Mon-Fri
        date = (base_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")

        for emp_id in emp_ids:
            rand = random.random()

            if rand < 0.85:  # 85% present
                hour = random.choice([8, 9, 10])
                minute = random.randint(0, 59)
                check_in = f"{hour:02d}:{minute:02d}"
                check_out_h = hour + random.randint(8, 10)
                check_out = f"{check_out_h:02d}:{random.randint(0, 59):02d}"
                status = "present"
                if hour >= 10:
                    status = "late"
            elif rand < 0.95:  # 10% leave
                check_in, check_out = None, None
                status = "leave"
            else:  # 5% absent
                check_in, check_out = None, None
                status = "absent"

            cursor.execute(
                "INSERT INTO attendance (emp_id, date, check_in, check_out, status) VALUES (?,?,?,?,?)",
                (emp_id, date, check_in, check_out, status)
            )
            records += 1

    conn.commit()
    print(f"   Generated {records} attendance records")


# ============================================================
# CRUD OPERATIONS
# ============================================================

def add_employee(conn, name, department, role, email, salary, join_date):
    """CREATE -- Add a new employee."""
    try:
        conn.execute(
            "INSERT INTO employees (name, department, role, email, salary, join_date) VALUES (?,?,?,?,?,?)",
            (name, department, role, email, salary, join_date)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"   Error: {e}")
        return False


def get_employee(conn, emp_id):
    """READ -- Get employee by ID."""
    row = conn.execute("SELECT * FROM employees WHERE id = ?", (emp_id,)).fetchone()
    return dict(row) if row else None


def update_salary(conn, emp_id, new_salary):
    """UPDATE -- Update employee salary."""
    conn.execute("UPDATE employees SET salary = ? WHERE id = ?", (new_salary, emp_id))
    conn.commit()


def delete_employee(conn, emp_id):
    """DELETE -- Remove employee (with transaction)."""
    try:
        conn.execute("DELETE FROM attendance WHERE emp_id = ?", (emp_id,))
        conn.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"   Rollback: {e}")
        return False


def record_attendance(conn, emp_id, date, check_in, check_out, status):
    """Record attendance for an employee."""
    try:
        conn.execute(
            "INSERT OR REPLACE INTO attendance (emp_id, date, check_in, check_out, status) VALUES (?,?,?,?,?)",
            (emp_id, date, check_in, check_out, status)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"   Error: {e}")


# ============================================================
# REPORTS
# ============================================================

def attendance_summary_report(conn):
    """Per-employee attendance summary."""
    query = """
        SELECT e.name, e.department,
               COUNT(CASE WHEN a.status = 'present' OR a.status = 'late' THEN 1 END) as present_days,
               COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_days,
               COUNT(CASE WHEN a.status = 'leave' THEN 1 END) as leave_days,
               COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent_days,
               COUNT(*) as total_days
        FROM employees e
        LEFT JOIN attendance a ON e.id = a.emp_id
        GROUP BY e.id
        ORDER BY present_days DESC
    """
    return conn.execute(query).fetchall()


def department_report(conn):
    """Department-wise attendance statistics."""
    query = """
        SELECT e.department,
               COUNT(DISTINCT e.id) as headcount,
               ROUND(AVG(e.salary), 2) as avg_salary,
               COUNT(CASE WHEN a.status IN ('present', 'late') THEN 1 END) as present_count,
               COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent_count
        FROM employees e
        LEFT JOIN attendance a ON e.id = a.emp_id
        GROUP BY e.department
        ORDER BY headcount DESC
    """
    return conn.execute(query).fetchall()


def late_arrivals_report(conn):
    """Find employees who were late."""
    query = """
        SELECT e.name, e.department, a.date, a.check_in
        FROM attendance a
        JOIN employees e ON a.emp_id = e.id
        WHERE a.status = 'late'
        ORDER BY a.date, a.check_in DESC
    """
    return conn.execute(query).fetchall()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("   EMPLOYEE DATABASE & ATTENDANCE MANAGEMENT SYSTEM")
    print("=" * 70)

    # Initialize
    print("\n Setting up database...")
    conn = create_database()
    seed_employees(conn)
    seed_attendance(conn)

    # CRUD Demo
    print(f"\n{''*70}")
    print("   CRUD OPERATIONS DEMO")
    print(f"{''*70}")

    emp = get_employee(conn, 1)
    print(f"\n  READ: {emp['name']} -- ₹{emp['salary']:,.2f}")

    update_salary(conn, 1, 130000)
    emp = get_employee(conn, 1)
    print(f"  UPDATE: {emp['name']} salary  ₹{emp['salary']:,.2f}")

    add_employee(conn, "New Hire", "Engineering", "Intern", "newhire@company.com", 40000, "2025-05-30")
    print(f"  CREATE: Added 'New Hire'")

    # Attendance Summary
    print(f"\n{''*70}")
    print("   ATTENDANCE SUMMARY REPORT")
    print(f"{''*70}")
    print(f"  {'Name':<20} {'Dept':<15} {'Present':>8} {'Late':>6} {'Leave':>6} {'Absent':>7}")
    print(f"  {''*62}")
    for row in attendance_summary_report(conn):
        print(f"  {row['name']:<20} {row['department']:<15} "
              f"{row['present_days']:>8} {row['late_days']:>6} "
              f"{row['leave_days']:>6} {row['absent_days']:>7}")

    # Department Report
    print(f"\n{''*70}")
    print("    DEPARTMENT REPORT")
    print(f"{''*70}")
    print(f"  {'Department':<15} {'Headcount':>10} {'Avg Salary':>15} {'Present':>9} {'Absent':>8}")
    print(f"  {''*57}")
    for row in department_report(conn):
        print(f"  {row['department']:<15} {row['headcount']:>10} "
              f"₹{row['avg_salary']:>13,.2f} {row['present_count']:>9} {row['absent_count']:>8}")

    # Late Arrivals
    print(f"\n{''*70}")
    print("   LATE ARRIVALS")
    print(f"{''*70}")
    late = late_arrivals_report(conn)
    if late:
        for row in late[:10]:
            print(f"  {row['name']:<20} {row['department']:<15} {row['date']} at {row['check_in']}")
    else:
        print("  No late arrivals recorded.")

    conn.close()
    print(f"\n{'='*70}")
