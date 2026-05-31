# Day 9 -- Modules, Packages & Database Connectivity

> **Objective:** Master Python's module system, understand package architecture, manage dependencies with pip, and perform database operations using sqlite3.

---

## Table of Contents

1. [Modules](#1-modules)
2. [Packages](#2-packages)
3. [The import Statement -- How Python Finds Modules](#3-the-import-statement--how-python-finds-modules)
4. [pip Installation & Dependency Management](#4-pip-installation--dependency-management)
5. [sqlite3 Module -- Database Operations](#5-sqlite3-module--database-operations)
6. [Transactions](#6-transactions)
7. [Database Connectivity Concepts](#7-database-connectivity-concepts)
8. [Best Practices for Database Operations](#8-best-practices-for-database-operations)

---

## 1. Modules

### What Are Modules?

A **module** is simply a Python file (`.py`) that contains definitions -- functions, classes, variables -- that you can reuse in other scripts. Modules promote **code reusability**, **organization**, and **namespace separation**.

Every Python file is automatically a module. When you write `helpers.py`, you've created a module named `helpers`.

### Creating a Module

```python
# math_utils.py -- A simple custom module

PI = 3.14159265358979

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def multiply(a, b):
    """Return the product of two numbers."""
    return a * b

def circle_area(radius):
    """Calculate the area of a circle given its radius."""
    return PI * radius ** 2
```

### Importing Modules

Python provides several ways to import modules:

#### 1. `import` -- Import the Entire Module

```python
import math_utils

result = math_utils.add(10, 20)       # 30
area = math_utils.circle_area(5)       # 78.539...
print(math_utils.PI)                   # 3.14159265358979
```

- Access members via **dot notation**: `module.member`
- The full module is loaded into memory

#### 2. `from ... import` -- Import Specific Members

```python
from math_utils import add, circle_area

result = add(10, 20)          # No prefix needed
area = circle_area(5)
# PI is NOT available here -- we didn't import it
```

- Only specified names are brought into the current namespace
- More concise, but can cause name collisions

#### 3. `from ... import *` -- Import Everything (Use Sparingly!)

```python
from math_utils import *

result = add(10, 20)
print(PI)
```

>  **Warning:** Avoid `import *` in production code. It pollutes the namespace and makes it hard to track where names come from. Use `__all__` in your module to control what gets exported.

```python
# In math_utils.py -- control what * exports
__all__ = ['add', 'multiply']  # circle_area and PI won't be exported with *
```

#### 4. `import ... as` -- Aliasing

```python
import math_utils as mu

result = mu.add(10, 20)
area = mu.circle_area(7)
```

```python
from math_utils import circle_area as ca

area = ca(7)
```

- Aliases are useful for long module names (`import numpy as np`)

### The `__name__` Guard

Every module has a built-in `__name__` attribute:
- When run directly: `__name__` equals `"__main__"`
- When imported: `__name__` equals the module's filename (without `.py`)

```python
# math_utils.py

def add(a, b):
    return a + b

if __name__ == "__main__":
    # This block runs ONLY when the file is executed directly
    print("Testing add:", add(3, 4))  # Output: Testing add: 7
```

This pattern lets a file work both as a **reusable module** and a **standalone script**.

---

## 2. Packages

### What Are Packages?

A **package** is a directory that contains multiple modules, organized hierarchically. Packages let you structure large projects into logical groupings.

```
my_project/
 main.py
 utils/                   Package
     __init__.py          Makes 'utils' a package
     string_utils.py      Module
     math_utils.py        Module
     db/                  Sub-package
         __init__.py
         connection.py    Module
```

### `__init__.py` -- The Package Initializer

The `__init__.py` file serves multiple purposes:

1. **Marks a directory as a Python package** (required in Python 2, optional but recommended in Python 3)
2. **Runs initialization code** when the package is imported
3. **Controls the package's public API**

```python
# utils/__init__.py

# Initialization code runs when 'import utils' is executed
print("Initializing utils package...")

# Re-export commonly used items for convenience
from .string_utils import capitalize, trim
from .math_utils import add, multiply

# Control what 'from utils import *' exports
__all__ = ['capitalize', 'trim', 'add', 'multiply']
```

### Absolute vs. Relative Imports

#### Absolute Imports (Recommended)

Specify the full path from the project root:

```python
# In main.py
from utils.math_utils import add
from utils.db.connection import connect
```

- **Pros:** Clear, unambiguous, works everywhere
- **Cons:** Can be verbose for deeply nested packages

#### Relative Imports

Use dots (`.`) to refer to the current or parent package:

```python
# In utils/math_utils.py
from . import string_utils          # Import sibling module
from .string_utils import capitalize  # Import from sibling
from ..config import settings       # Import from parent package (one level up)
```

| Syntax | Meaning |
|--------|---------|
| `.` | Current package |
| `..` | Parent package |
| `...` | Grandparent package |

- **Pros:** Shorter, package-aware
- **Cons:** Only work inside packages, can't be used in scripts run directly

>  **Rule of thumb:** Use **absolute imports** for clarity. Use **relative imports** within a package when it makes the code cleaner.

---

## 3. The import Statement -- How Python Finds Modules

When you write `import something`, Python searches for the module in this order:

### Module Search Order

1. **`sys.modules` cache** -- Already-imported modules (avoids re-importing)
2. **Built-in modules** -- `sys`, `os`, `math`, etc. (compiled into Python)
3. **`sys.path` directories** -- A list of directories Python searches through:
   - The directory of the script being run
   - Directories in the `PYTHONPATH` environment variable
   - Standard library directories
   - `site-packages` (where pip installs third-party packages)

### Inspecting `sys.path`

```python
import sys

# Print all directories Python searches for modules
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")
```

### Modifying `sys.path` at Runtime

```python
import sys

# Add a custom directory to the search path
sys.path.append(r"D:\my_custom_libs")  # Now Python can find modules in this directory

import my_custom_module  # Found in D:\my_custom_libs\my_custom_module.py
```

### Setting `PYTHONPATH` Environment Variable

```bash
# Windows (Command Prompt)
set PYTHONPATH=D:\my_libs;D:\other_libs

# Windows (PowerShell)
$env:PYTHONPATH = "D:\my_libs;D:\other_libs"

# Linux/macOS
export PYTHONPATH="/home/user/my_libs:/home/user/other_libs"
```

### Useful Module Inspection

```python
import os

# Where is this module's file located?
print(os.__file__)  # e.g., C:\Python39\lib\os.py

# What names does this module define?
print(dir(os))      # Lists all attributes and functions

# Get help on a specific function
help(os.path.join)
```

---

## 4. pip Installation & Dependency Management

`pip` is Python's **package installer** -- it downloads and installs packages from the [Python Package Index (PyPI)](https://pypi.org/).

### Essential pip Commands

```bash
# Install a package
pip install requests

# Install a specific version
pip install requests==2.28.0

# Install minimum version
pip install "requests>=2.28.0"

# Upgrade a package
pip install --upgrade requests

# Uninstall a package
pip uninstall requests

# Show installed package info
pip show requests

# List all installed packages
pip list

# List outdated packages
pip list --outdated
```

### `pip freeze` and `requirements.txt`

`pip freeze` outputs all installed packages and their exact versions -- perfect for reproducibility.

```bash
# Generate requirements file
pip freeze > requirements.txt

# Install all packages from requirements file
pip install -r requirements.txt
```

**Example `requirements.txt`:**

```
requests==2.28.2
flask==2.3.1
sqlalchemy>=2.0.0,<3.0.0
pytest~=7.4.0
```

| Operator | Meaning |
|----------|---------|
| `==` | Exact version |
| `>=` | Minimum version |
| `<=` | Maximum version |
| `~=` | Compatible release (e.g., `~=7.4.0` means `>=7.4.0, <7.5.0`) |
| `!=` | Exclude version |

### Virtual Environments (Best Practice)

Always use virtual environments to isolate project dependencies:

```bash
# Create a virtual environment
python -m venv myenv

# Activate it
# Windows:
myenv\Scripts\activate
# Linux/macOS:
source myenv/bin/activate

# Now pip install goes into the virtual environment only
pip install requests

# Deactivate when done
deactivate
```

---

## 5. sqlite3 Module -- Database Operations

`sqlite3` is Python's **built-in** module for working with SQLite databases -- no installation needed! SQLite stores the entire database in a single file (or in memory).

### Connecting to a Database

```python
import sqlite3

# Connect to a file-based database (creates it if it doesn't exist)
conn = sqlite3.connect("company.db")

# OR connect to an in-memory database (data lost when connection closes)
conn = sqlite3.connect(":memory:")

# Create a cursor object to execute SQL
cursor = conn.cursor()

# Always close the connection when done
conn.close()
```

### Using Context Managers (Recommended)

```python
import sqlite3

# 'with' automatically handles commit/rollback
with sqlite3.connect("company.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
```

### Creating Tables

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT    NOT NULL,
        dept    TEXT    NOT NULL,
        salary  REAL    DEFAULT 0.0,
        email   TEXT    UNIQUE
    )
""")

conn.commit()
print("Table created successfully!")
```

### CRUD Operations

#### CREATE (Insert)

```python
# Insert a single row
cursor.execute(
    "INSERT INTO employees (name, dept, salary, email) VALUES (?, ?, ?, ?)",
    ("Alice", "Engineering", 95000.0, "alice@company.com")
)

# Insert multiple rows at once
employees_data = [
    ("Bob", "Marketing", 72000.0, "bob@company.com"),
    ("Charlie", "Engineering", 88000.0, "charlie@company.com"),
    ("Diana", "HR", 65000.0, "diana@company.com"),
]
cursor.executemany(
    "INSERT INTO employees (name, dept, salary, email) VALUES (?, ?, ?, ?)",
    employees_data
)

conn.commit()
print(f"Inserted {cursor.rowcount} rows. Last ID: {cursor.lastrowid}")
```

>  **Always use `?` placeholders** -- NEVER use f-strings or `.format()` to build SQL queries. Parameterized queries prevent SQL injection attacks.

#### READ (Select)

```python
# Fetch all rows
cursor.execute("SELECT * FROM employees")
all_rows = cursor.fetchall()       # Returns list of tuples
for row in all_rows:
    print(row)

# Fetch one row
cursor.execute("SELECT * FROM employees WHERE id = ?", (1,))
single_row = cursor.fetchone()     # Returns one tuple or None
print(single_row)

# Fetch N rows
cursor.execute("SELECT * FROM employees ORDER BY salary DESC")
top_3 = cursor.fetchmany(3)       # Returns list of up to 3 tuples

# Use Row factory for dict-like access
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM employees WHERE id = ?", (1,))
row = cursor.fetchone()
print(row["name"], row["dept"])    # Access by column name!
```

#### UPDATE

```python
cursor.execute(
    "UPDATE employees SET salary = ? WHERE name = ?",
    (100000.0, "Alice")
)
conn.commit()
print(f"Updated {cursor.rowcount} row(s)")
```

#### DELETE

```python
cursor.execute("DELETE FROM employees WHERE dept = ?", ("Marketing",))
conn.commit()
print(f"Deleted {cursor.rowcount} row(s)")
```

---

## 6. Transactions

A **transaction** is a sequence of database operations that are treated as a single unit -- either **all succeed** or **all fail**.

### ACID Properties

| Property | Description |
|----------|-------------|
| **Atomicity** | All operations in a transaction succeed or none do |
| **Consistency** | Database moves from one valid state to another |
| **Isolation** | Concurrent transactions don't interfere |
| **Durability** | Committed changes persist even after crashes |

### commit() and rollback()

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance REAL)")
cursor.execute("INSERT INTO accounts VALUES (1, 'Alice', 1000.0)")
cursor.execute("INSERT INTO accounts VALUES (2, 'Bob', 500.0)")
conn.commit()

# --- Transfer money: Alice  Bob ---
transfer_amount = 200.0

try:
    # Debit Alice
    cursor.execute(
        "UPDATE accounts SET balance = balance - ? WHERE id = ?",
        (transfer_amount, 1)
    )
    # Credit Bob
    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE id = ?",
        (transfer_amount, 2)
    )

    # Verify: no negative balances
    cursor.execute("SELECT balance FROM accounts WHERE id = 1")
    alice_balance = cursor.fetchone()[0]
    if alice_balance < 0:
        raise ValueError("Insufficient funds!")

    conn.commit()  #  Both operations saved
    print("Transfer successful!")

except Exception as e:
    conn.rollback()  #  Undo ALL changes since last commit
    print(f"Transfer failed: {e}")
```

### Autocommit Mode

By default, `sqlite3` operates in **manual commit mode** (`isolation_level` is set to `""`). You can enable autocommit:

```python
# Autocommit mode -- each statement is committed immediately
conn = sqlite3.connect("test.db", isolation_level=None)
cursor = conn.cursor()
cursor.execute("INSERT INTO logs VALUES ('event1')")  # Committed automatically!
```

>  **Autocommit is generally discouraged** for multi-step operations. Use explicit transactions for data integrity.

### Manual Transaction Control

```python
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Explicitly begin a transaction
cursor.execute("BEGIN TRANSACTION")
try:
    cursor.execute("INSERT INTO orders VALUES (1, 'Widget', 10)")
    cursor.execute("INSERT INTO orders VALUES (2, 'Gadget', 5)")
    cursor.execute("COMMIT")
except Exception:
    cursor.execute("ROLLBACK")
```

---

## 7. Database Connectivity Concepts

### Connection Pooling (Concept)

**Connection pooling** maintains a cache of database connections that can be reused, avoiding the overhead of creating a new connection for every request.

```
          
  Application    Connection Pool         Database 
   Thread 1                              
   Thread 2     Conn Conn Conn             
   Thread 3      1    2    3                    
                 
                     
```

**Why pooling matters:**
- **Performance:** Reusing connections is 10-100x faster than creating new ones
- **Resource management:** Limits the number of simultaneous database connections
- **Scalability:** Handles high-concurrency workloads efficiently

**In production Python apps**, use libraries like:
- `SQLAlchemy` (built-in connection pooling)
- `psycopg2.pool` (for PostgreSQL)
- `DBUtils` (generic pooling)

```python
# Conceptual example with SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///app.db",
    pool_size=5,          # Maintain 5 connections
    max_overflow=10,      # Allow up to 10 extra during spikes
    pool_timeout=30,      # Wait 30s for a connection before error
    pool_recycle=3600     # Recycle connections every hour
)
```

### Parameterized Queries & SQL Injection Prevention

**SQL Injection** is a critical security vulnerability where an attacker injects malicious SQL through user input.

####  VULNERABLE -- String Formatting

```python
# NEVER DO THIS -- vulnerable to SQL injection!
username = input("Enter username: ")
query = f"SELECT * FROM users WHERE name = '{username}'"
cursor.execute(query)

# If user enters: ' OR '1'='1
# Query becomes: SELECT * FROM users WHERE name = '' OR '1'='1'
# This returns ALL users!
```

####  SAFE -- Parameterized Queries

```python
# ALWAYS use parameterized queries
username = input("Enter username: ")
cursor.execute("SELECT * FROM users WHERE name = ?", (username,))

# The database engine handles escaping -- injection is impossible
```

**How parameterized queries work:**
1. SQL structure and data are sent **separately** to the database
2. The database **compiles** the SQL template first
3. Data values are **bound** as literal values -- never interpreted as SQL

| Method | Security | Performance | Use? |
|--------|----------|-------------|------|
| f-strings / `.format()` |  Vulnerable | Slow (recompiled) | **NEVER** |
| `?` placeholders (sqlite3) |  Safe | Fast (prepared) | **ALWAYS** |
| `:name` named params |  Safe | Fast (prepared) | **ALWAYS** |

```python
# Named parameters -- more readable for complex queries
cursor.execute(
    "SELECT * FROM employees WHERE dept = :dept AND salary > :min_salary",
    {"dept": "Engineering", "min_salary": 80000}
)
```

---

## 8. Best Practices for Database Operations

### 1. Always Use Context Managers

```python
#  Good -- automatic resource cleanup
with sqlite3.connect("app.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
```

### 2. Always Use Parameterized Queries

```python
#  Safe
cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))

#  Dangerous
cursor.execute(f"INSERT INTO users (name) VALUES ('{name}')")
```

### 3. Handle Errors Gracefully

```python
import sqlite3

try:
    with sqlite3.connect("app.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email) VALUES (?)", (email,))
        conn.commit()
except sqlite3.IntegrityError:
    print("Error: Duplicate email address")
except sqlite3.OperationalError as e:
    print(f"Database error: {e}")
except sqlite3.Error as e:
    print(f"Unexpected database error: {e}")
```

### 4. Use Transactions for Related Operations

```python
try:
    cursor.execute("BEGIN")
    cursor.execute("UPDATE inventory SET qty = qty - ? WHERE item = ?", (qty, item))
    cursor.execute("INSERT INTO orders (item, qty) VALUES (?, ?)", (item, qty))
    conn.commit()
except Exception:
    conn.rollback()
```

### 5. Close Connections and Cursors

```python
# Explicitly close when not using 'with'
cursor.close()
conn.close()
```

### 6. Use `Row` Factory for Readable Code

```python
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM employees")
for row in cursor:
    print(f"{row['name']} -- {row['dept']} -- ${row['salary']:,.2f}")
```

### 7. Index Frequently Queried Columns

```python
cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_dept ON employees(dept)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_email ON employees(email)")
```

### 8. Normalize Your Schema

- Avoid data duplication
- Use foreign keys with `PRAGMA foreign_keys = ON`
- Design tables with clear relationships

```python
conn.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
    CREATE TABLE orders (
        id       INTEGER PRIMARY KEY,
        user_id  INTEGER NOT NULL,
        product  TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")
```

---

## Quick Reference Card

| Concept | Key Syntax |
|---------|-----------|
| Import module | `import module_name` |
| Import specific | `from module import func` |
| Import with alias | `import module as alias` |
| Package marker | `__init__.py` |
| Install package | `pip install package` |
| Freeze deps | `pip freeze > requirements.txt` |
| Connect SQLite | `sqlite3.connect("file.db")` |
| In-memory DB | `sqlite3.connect(":memory:")` |
| Parameterized query | `cursor.execute("... WHERE x=?", (val,))` |
| Commit | `conn.commit()` |
| Rollback | `conn.rollback()` |

---

## Files in This Directory

| File | Description |
|------|-------------|
| `practice/modules_demo.py` | Creating & importing modules, `__name__` guard |
| `practice/sqlite_crud.py` | SQLite CRUD operations & transactions |
| `official_questions/01_rotate_array.py` | LeetCode 189 -- Rotate Array |
| `official_questions/02_majority_element.py` | LeetCode 169 -- Majority Element (Boyer-Moore) |
| `Corporate_use_case/employee_attendance_system.py` | Enterprise attendance management system |

---

*Day 9 of DSA Training -- Modules, Packages & Database Connectivity*
