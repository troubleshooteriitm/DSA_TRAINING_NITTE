#  Day 13 -- Advanced Coding + RDBMS Concepts

> **Objective:** Master advanced Python coding patterns for interviews and build a strong foundation in relational database management systems.

---

##  Table of Contents

### First Half -- Advanced Coding
1. [Mock Coding Interview Tips](#-mock-coding-interview-tips--strategies)
2. [Pandas-Based Optimization](#-pandas-based-optimization-patterns)
3. [Collections-Based Coding](#-collections-based-coding-patterns)
4. [Dictionary & Set Optimization](#-dictionary--set-optimization)
5. [Sliding Window Problems](#-sliding-window-problems)
6. [Debugging & Refactoring](#-debugging--refactoring)

### Second Half -- RDBMS
7. [DBMS vs RDBMS](#-dbms-vs-rdbms)
8. [ER Model](#-er-model)
9. [Keys](#-keys-in-rdbms)
10. [Normalization](#-normalization)
11. [SQL Queries](#-sql-queries)
12. [Joins](#-joins)
13. [Aggregate Functions](#-aggregate-functions)
14. [Transactions](#-transactions)

---

#  FIRST HALF -- Advanced Coding

---

##  Mock Coding Interview Tips & Strategies

### The UMPIRE Method
A structured approach to solving coding problems:

| Step | Action | Example |
|------|--------|---------|
| **U**nderstand | Clarify the problem, ask questions | "Can the array be empty?" |
| **M**atch | Identify patterns/data structures | "This looks like a sliding window problem" |
| **P**lan | Write pseudocode | Step-by-step algorithm |
| **I**mplement | Write clean code | Actual Python solution |
| **R**eview | Walk through with examples | Trace through test cases |
| **E**valuate | Analyze complexity | Time: O(n), Space: O(1) |

### Time Management Strategy
- **0-5 min:** Understand the problem, ask clarifying questions
- **5-10 min:** Identify approach, discuss trade-offs
- **10-30 min:** Implement the solution
- **30-35 min:** Test with examples, handle edge cases

### Common Interview Patterns

```python
# Pattern 1: Two Pointers
def two_sum_sorted(nums, target):
    """Two pointers for sorted array."""
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

# Pattern 2: Hash Map for O(1) Lookup
def two_sum(nums, target):
    """Hash map approach for unsorted array."""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Pattern 3: Frequency Count
from collections import Counter

def top_k_frequent(nums, k):
    """Find k most frequent elements."""
    count = Counter(nums)
    return [num for num, _ in count.most_common(k)]
```

### Key Tips
-  **Think aloud** -- Communicate your thought process
-  **Start with brute force** -- Then optimize
-  **Handle edge cases** -- Empty input, single element, duplicates
-  **Write clean code** -- Meaningful variable names, proper indentation
-  **Don't jump to code** -- Plan first
-  **Don't stay silent** -- Interviewers want to hear your reasoning

---

##  Pandas-Based Optimization Patterns

### Vectorization Over Loops

```python
import pandas as pd
import numpy as np

#  SLOW: Using loops
def slow_calculation(df):
    results = []
    for _, row in df.iterrows():
        results.append(row['price'] * row['quantity'] * 0.9)
    df['total'] = results
    return df

#  FAST: Vectorized operations
def fast_calculation(df):
    df['total'] = df['price'] * df['quantity'] * 0.9
    return df
```

### Efficient Filtering

```python
#  Use .query() for complex filters
df_filtered = df.query('age > 25 and salary > 50000 and department == "Engineering"')

#  Use .isin() for membership testing
valid_depts = ['Engineering', 'Marketing', 'Sales']
df_filtered = df[df['department'].isin(valid_depts)]

#  Use categorical dtypes for memory optimization
df['department'] = df['department'].astype('category')
```

### GroupBy Optimization

```python
#  Use agg() with named aggregations
result = df.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    total_employees=('employee_id', 'count'),
    max_salary=('salary', 'max')
).reset_index()

#  Use transform() for group-level calculations
df['dept_avg'] = df.groupby('department')['salary'].transform('mean')
df['salary_ratio'] = df['salary'] / df['dept_avg']
```

### Memory Optimization

```python
# Check memory usage
print(df.info(memory_usage='deep'))

# Downcast numeric types
df['age'] = pd.to_numeric(df['age'], downcast='integer')
df['salary'] = pd.to_numeric(df['salary'], downcast='float')

# Read large files in chunks
chunks = pd.read_csv('large_file.csv', chunksize=10000)
result = pd.concat([chunk[chunk['status'] == 'active'] for chunk in chunks])
```

---

##  Collections-Based Coding Patterns

### Counter -- Frequency Analysis

```python
from collections import Counter

# Basic counting
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
word_count = Counter(words)
print(word_count)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# Most common elements
print(word_count.most_common(2))  # [('apple', 3), ('banana', 2)]

# Counter arithmetic
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2}) -- only keeps positive counts

# Check if anagram
def is_anagram(s1, s2):
    """Check if two strings are anagrams using Counter."""
    return Counter(s1) == Counter(s2)

print(is_anagram("listen", "silent"))  # True
```

### defaultdict -- Auto-Initialization

```python
from collections import defaultdict

# Group items by key
students = [
    ('Math', 'Alice'), ('Science', 'Bob'),
    ('Math', 'Charlie'), ('Science', 'Diana'),
    ('Math', 'Eve')
]

groups = defaultdict(list)
for subject, student in students:
    groups[subject].append(student)

print(dict(groups))
# {'Math': ['Alice', 'Charlie', 'Eve'], 'Science': ['Bob', 'Diana']}

# Build adjacency list for graph
edges = [(1, 2), (1, 3), (2, 4), (3, 4)]
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

# Nested defaultdict for multi-level grouping
nested = defaultdict(lambda: defaultdict(int))
sales = [('Q1', 'ProductA', 100), ('Q1', 'ProductB', 200), ('Q2', 'ProductA', 150)]
for quarter, product, amount in sales:
    nested[quarter][product] += amount
```

### deque -- Double-Ended Queue

```python
from collections import deque

# BFS traversal
def bfs(graph, start):
    """Breadth-First Search using deque."""
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []

    while queue:
        node = queue.popleft()  # O(1) -- vs list.pop(0) which is O(n)
        result.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return result

# Sliding window maximum using deque
def max_sliding_window(nums, k):
    """Find maximum in each sliding window of size k."""
    dq = deque()  # Stores indices
    result = []

    for i, num in enumerate(nums):
        # Remove elements outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Remove smaller elements from back
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

# Recent history / circular buffer
recent_actions = deque(maxlen=5)
for action in ['open', 'edit', 'save', 'close', 'new', 'edit', 'save']:
    recent_actions.append(action)
print(list(recent_actions))  # ['close', 'new', 'edit', 'save'] -- auto-evicts oldest
```

---

##  Dictionary & Set Optimization

### O(1) Lookup Patterns

```python
#  Use dict/set for membership testing instead of list
# O(1) average vs O(n) for list
valid_ids = {1001, 1002, 1003, 1004, 1005}  # set -- O(1) lookup
if user_id in valid_ids:
    print("Valid user")

#  Dictionary for fast key-value lookup
price_lookup = {
    'AAPL': 150.25, 'GOOGL': 2800.50,
    'MSFT': 300.75, 'AMZN': 3400.00
}
stock_price = price_lookup.get('AAPL', 0)  # O(1) with default

#  Use setdefault() to avoid KeyError
inventory = {}
inventory.setdefault('electronics', []).append('laptop')
inventory.setdefault('electronics', []).append('phone')
```

### Set Operations for Efficiency

```python
# Set operations are highly optimized in Python
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# Union -- O(len(a) + len(b))
print(set_a | set_b)        # {1, 2, 3, 4, 5, 6, 7, 8}

# Intersection -- O(min(len(a), len(b)))
print(set_a & set_b)        # {4, 5}

# Difference -- O(len(a))
print(set_a - set_b)        # {1, 2, 3}

# Symmetric Difference -- elements in either but not both
print(set_a ^ set_b)        # {1, 2, 3, 6, 7, 8}

# Practical: Find common friends
user1_friends = {'Alice', 'Bob', 'Charlie', 'Diana'}
user2_friends = {'Bob', 'Diana', 'Eve', 'Frank'}
common = user1_friends & user2_friends        # {'Bob', 'Diana'}
suggestions = user2_friends - user1_friends   # {'Eve', 'Frank'}
```

### Dictionary Comprehensions

```python
# Invert a dictionary
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}

# Filter dictionary
scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78, 'Diana': 95}
high_scorers = {k: v for k, v in scores.items() if v >= 90}

# Merge dictionaries (Python 3.9+)
defaults = {'color': 'blue', 'size': 'medium', 'weight': 10}
custom = {'color': 'red', 'weight': 15}
merged = defaults | custom  # {'color': 'red', 'size': 'medium', 'weight': 15}
```

---

##  Sliding Window Problems

The sliding window technique is used to solve problems involving contiguous subarrays/substrings efficiently.

### Fixed-Size Sliding Window

```python
def max_sum_subarray(nums, k):
    """
    Find the maximum sum of a subarray of size k.
    Time: O(n), Space: O(1)
    """
    if len(nums) < k:
        return 0

    # Calculate sum of first window
    window_sum = sum(nums[:k])
    max_sum = window_sum

    # Slide the window: add right element, remove left element
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum

# Example
print(max_sum_subarray([2, 1, 5, 1, 3, 2], 3))  # 9 (5+1+3)
```

### Variable-Size Sliding Window

```python
def longest_substring_no_repeat(s):
    """
    Find length of longest substring without repeating characters.
    Time: O(n), Space: O(min(m, n)) where m is charset size
    """
    char_set = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        # Shrink window until no duplicates
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)

    return max_length

# Example
print(longest_substring_no_repeat("abcabcbb"))  # 3 ("abc")
```

### Sliding Window Pattern Template

```python
def sliding_window_template(arr, condition):
    """
    General template for variable-size sliding window.

    Pattern:
    1. Use two pointers: left and right
    2. Expand window by moving right
    3. Shrink window by moving left when condition is violated
    4. Update answer at each valid window
    """
    left = 0
    result = 0  # or float('inf') for minimum problems
    window_state = {}  # Track window contents

    for right in range(len(arr)):
        # 1. Add arr[right] to window state
        # window_state[arr[right]] = ...

        # 2. Shrink window while condition is violated
        while not condition(window_state):
            # Remove arr[left] from window state
            left += 1

        # 3. Update result
        result = max(result, right - left + 1)

    return result
```

---

##  Debugging & Refactoring

### Common Code Smells

| Code Smell | Description | Solution |
|-----------|-------------|----------|
| **Long Function** | Function > 20 lines | Extract into smaller functions |
| **Magic Numbers** | Unexplained numeric literals | Use named constants |
| **Deep Nesting** | 3+ levels of indentation | Early returns, extract methods |
| **Duplicate Code** | Same logic in multiple places | Extract common function |
| **God Class** | Class doing too many things | Split into focused classes |
| **Long Parameter List** | Function with 5+ params | Use dataclass or dict |

### Refactoring Examples

```python
#  BEFORE: Code smell -- long function, magic numbers, deep nesting
def process_order(order):
    if order:
        if order['quantity'] > 0:
            if order['price'] > 0:
                total = order['quantity'] * order['price']
                if total > 1000:
                    total = total * 0.9
                if total > 5000:
                    total = total * 0.85
                tax = total * 0.18
                return total + tax
    return 0

#  AFTER: Refactored -- clean, readable, maintainable
BULK_DISCOUNT_THRESHOLD = 1000
BULK_DISCOUNT_RATE = 0.9
PREMIUM_DISCOUNT_THRESHOLD = 5000
PREMIUM_DISCOUNT_RATE = 0.85
TAX_RATE = 0.18

def calculate_discount(total):
    """Apply tiered discounts based on order total."""
    if total > PREMIUM_DISCOUNT_THRESHOLD:
        return total * PREMIUM_DISCOUNT_RATE
    elif total > BULK_DISCOUNT_THRESHOLD:
        return total * BULK_DISCOUNT_RATE
    return total

def calculate_order_total(order):
    """Calculate final order total with discounts and tax."""
    if not order or order.get('quantity', 0) <= 0 or order.get('price', 0) <= 0:
        return 0

    subtotal = order['quantity'] * order['price']
    discounted = calculate_discount(subtotal)
    return discounted * (1 + TAX_RATE)
```

### Debugging Techniques

```python
import logging

# Setup structured logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_pair_with_sum(nums, target):
    """Find pair that sums to target with debug logging."""
    logger.debug(f"Input: nums={nums}, target={target}")
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num
        logger.debug(f"Index {i}: num={num}, complement={complement}, seen={seen}")

        if complement in seen:
            result = [seen[complement], i]
            logger.info(f"Found pair: {result}")
            return result
        seen[num] = i

    logger.warning("No pair found")
    return []

# Using breakpoint() for interactive debugging (Python 3.7+)
def complex_function(data):
    result = []
    for item in data:
        processed = item ** 2
        # breakpoint()  # Uncomment to enter pdb debugger
        result.append(processed)
    return result
```

---

#  SECOND HALF -- RDBMS (Relational Database Management Systems)

---

##  DBMS vs RDBMS

| Feature | DBMS | RDBMS |
|---------|------|-------|
| **Data Storage** | Files (hierarchical/network) | Tables (rows & columns) |
| **Relationships** | No formal relationships | Foreign key relationships |
| **Normalization** | Not supported | Supported (1NF  BCNF) |
| **ACID Compliance** | Usually not | Yes |
| **Data Integrity** | Limited | Strong constraints |
| **Examples** | File systems, XML DBs | MySQL, PostgreSQL, Oracle, SQLite |
| **Scalability** | Limited | Highly scalable |
| **SQL Support** | Limited or none | Full SQL support |

### RDBMS Key Concepts
- **Table (Relation):** Collection of related data organized in rows and columns
- **Row (Tuple):** A single record in a table
- **Column (Attribute):** A field in a table
- **Schema:** The structure/blueprint of a database

---

##  ER Model

The **Entity-Relationship (ER) Model** is used to design the logical structure of a database.

### Components

#### 1. Entities
An entity represents a real-world object or concept:
- **Strong Entity:** Exists independently (e.g., `Student`, `Employee`)
- **Weak Entity:** Depends on another entity (e.g., `Dependent` depends on `Employee`)

#### 2. Attributes
Properties that describe an entity:

| Attribute Type | Description | Example |
|---------------|-------------|---------|
| **Simple** | Cannot be divided further | `first_name` |
| **Composite** | Can be divided into sub-parts | `address`  street, city, zip |
| **Derived** | Computed from other attributes | `age` from `date_of_birth` |
| **Multi-valued** | Can hold multiple values | `phone_numbers` |
| **Key** | Uniquely identifies an entity | `student_id` |

#### 3. Relationships
Associations between entities:

| Cardinality | Description | Example |
|------------|-------------|---------|
| **1:1** (One-to-One) | One entity relates to exactly one | Person  Passport |
| **1:N** (One-to-Many) | One entity relates to many | Department  Employees |
| **M:N** (Many-to-Many) | Many relate to many | Students  Courses |

### ER Diagram Notation
```
         
   STUDENT                 COURSE    
         
 student_id(PKM:N course_id(PK)
 name                   title        
 email                  credits      
         
                                
        
           
            ENROLLMENT 
           
            student_id 
            course_id  
            grade      
            date       
           
```

---

##  Keys in RDBMS

```python
import sqlite3

# Demonstration of different key types
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# PRIMARY KEY -- Uniquely identifies each row
# FOREIGN KEY -- References primary key of another table
# COMPOSITE KEY -- Two or more columns together form the key
# UNIQUE KEY -- Ensures all values in a column are distinct
cursor.execute('''
    CREATE TABLE departments (
        dept_id INTEGER PRIMARY KEY,           -- Primary Key
        dept_name TEXT UNIQUE NOT NULL          -- Unique Key
    )
''')

cursor.execute('''
    CREATE TABLE employees (
        emp_id INTEGER PRIMARY KEY,            -- Primary Key
        name TEXT NOT NULL,
        email TEXT UNIQUE,                     -- Unique Key (Candidate Key)
        dept_id INTEGER,                       -- Foreign Key
        FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
    )
''')

# COMPOSITE KEY example
cursor.execute('''
    CREATE TABLE enrollments (
        student_id INTEGER,
        course_id INTEGER,
        grade TEXT,
        PRIMARY KEY (student_id, course_id)    -- Composite Key
    )
''')
```

### Key Types Summary

| Key Type | Definition | Example |
|----------|-----------|---------|
| **Primary Key** | Uniquely identifies each record | `emp_id` |
| **Foreign Key** | References primary key of another table | `dept_id` in employees |
| **Candidate Key** | Column(s) that could be primary key | `email`, `emp_id` |
| **Composite Key** | Two+ columns forming a primary key | `(student_id, course_id)` |
| **Unique Key** | Ensures uniqueness but allows NULL | `email` |
| **Super Key** | Any set of columns that uniquely identifies | `{emp_id, name}` |
| **Alternate Key** | Candidate key not chosen as primary | `email` (if `emp_id` is PK) |

---

##  Normalization

Normalization eliminates data redundancy and ensures data integrity.

### 1NF -- First Normal Form
**Rule:** Each column must contain atomic (indivisible) values. No repeating groups.

```
 Before 1NF:

 ID   Name     Phone Numbers        

 1    Alice    111-1111, 222-2222      Multiple values!
 2    Bob      333-3333             


 After 1NF:

 ID   Name     Phone        

 1    Alice    111-1111        Atomic values
 1    Alice    222-2222     
 2    Bob      333-3333     

```

### 2NF -- Second Normal Form
**Rule:** Must be in 1NF + no partial dependency (non-key columns must depend on the entire primary key).

```
 Before 2NF (Composite PK: student_id + course_id):

 student_id  course_id  student_name  grade 

 1           101        Alice         A     

               student_name depends only on student_id (partial dependency!)

 After 2NF: Split into two tables
Students: (student_id PK, student_name)
Enrollments: (student_id, course_id, grade) -- composite PK
```

### 3NF -- Third Normal Form
**Rule:** Must be in 2NF + no transitive dependency (non-key column depending on another non-key column).

```
 Before 3NF:

 emp_id  name     dept_id  dept_name    

 1       Alice    10       Engineering  

           dept_name depends on dept_id, not emp_id (transitive!)

 After 3NF:
Employees: (emp_id PK, name, dept_id FK)
Departments: (dept_id PK, dept_name)
```

### BCNF -- Boyce-Codd Normal Form
**Rule:** Must be in 3NF + every determinant must be a candidate key.

```
 Before BCNF:
Professor teaches Subject in Room
- (Professor, Subject)  Room
- Room  Professor  (determinant Room is not a candidate key!)

 After BCNF:
Table 1: (Room PK, Professor)
Table 2: (Professor, Subject, Room FK)
```

---

##  SQL Queries

### Basic SELECT Queries

```sql
-- Select all columns
SELECT * FROM employees;

-- Select specific columns
SELECT name, salary FROM employees;

-- WHERE clause -- filtering
SELECT * FROM employees WHERE department = 'Engineering';
SELECT * FROM employees WHERE salary > 50000 AND age < 30;
SELECT * FROM employees WHERE name LIKE 'A%';    -- Starts with 'A'
SELECT * FROM employees WHERE dept_id IN (1, 2, 3);

-- ORDER BY -- sorting
SELECT * FROM employees ORDER BY salary DESC;
SELECT * FROM employees ORDER BY department ASC, salary DESC;

-- LIMIT -- restrict number of rows
SELECT * FROM employees ORDER BY salary DESC LIMIT 5;

-- DISTINCT -- unique values
SELECT DISTINCT department FROM employees;
SELECT COUNT(DISTINCT department) FROM employees;
```

### Python sqlite3 Example

```python
import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create and populate table
cursor.execute('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT,
        salary REAL,
        hire_date TEXT
    )
''')

employees = [
    (1, 'Alice', 'Engineering', 95000, '2020-01-15'),
    (2, 'Bob', 'Marketing', 65000, '2019-06-01'),
    (3, 'Charlie', 'Engineering', 105000, '2018-03-20'),
    (4, 'Diana', 'Sales', 72000, '2021-09-10'),
    (5, 'Eve', 'Marketing', 68000, '2020-11-05'),
]
cursor.executemany('INSERT INTO employees VALUES (?,?,?,?,?)', employees)

# Query examples
cursor.execute('SELECT name, salary FROM employees WHERE salary > 70000 ORDER BY salary DESC')
for row in cursor.fetchall():
    print(f"{row[0]}: ${row[1]:,.2f}")

conn.close()
```

---

##  Joins

Joins combine rows from two or more tables based on a related column.

### Visual Representation

```
Table A          Table B
   
 id  name     id  dept 
   
 1   Alice    1   Eng  
 2   Bob      3   Sales
 3   Carol    4   HR   
   
```

### Join Types

```sql
-- INNER JOIN: Only matching rows from both tables
-- Result: Alice(1,Eng), Carol(3,Sales)
SELECT a.name, b.dept
FROM table_a a INNER JOIN table_b b ON a.id = b.id;

-- LEFT JOIN: All rows from left table + matching from right
-- Result: Alice(Eng), Bob(NULL), Carol(Sales)
SELECT a.name, b.dept
FROM table_a a LEFT JOIN table_b b ON a.id = b.id;

-- RIGHT JOIN: All rows from right table + matching from left
-- Result: Alice(Eng), Carol(Sales), NULL(HR)
SELECT a.name, b.dept
FROM table_a a RIGHT JOIN table_b b ON a.id = b.id;

-- FULL OUTER JOIN: All rows from both tables
-- Result: Alice(Eng), Bob(NULL), Carol(Sales), NULL(HR)
SELECT a.name, b.dept
FROM table_a a FULL OUTER JOIN table_b b ON a.id = b.id;

-- CROSS JOIN: Cartesian product (every row x every row)
SELECT a.name, b.dept FROM table_a a CROSS JOIN table_b b;

-- SELF JOIN: Table joined with itself
-- Example: Find employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;
```

### Python Example with Joins

```python
import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT)')
cursor.execute('CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER)')

cursor.executemany('INSERT INTO departments VALUES (?,?)',
    [(1, 'Engineering'), (2, 'Marketing'), (3, 'Sales')])
cursor.executemany('INSERT INTO employees VALUES (?,?,?)',
    [(1, 'Alice', 1), (2, 'Bob', 2), (3, 'Charlie', 1), (4, 'Diana', None)])

# INNER JOIN
cursor.execute('''
    SELECT e.name, d.name as department
    FROM employees e INNER JOIN departments d ON e.dept_id = d.id
''')
print("INNER JOIN:", cursor.fetchall())
# [('Alice', 'Engineering'), ('Bob', 'Marketing'), ('Charlie', 'Engineering')]

# LEFT JOIN -- includes Diana with NULL department
cursor.execute('''
    SELECT e.name, d.name as department
    FROM employees e LEFT JOIN departments d ON e.dept_id = d.id
''')
print("LEFT JOIN:", cursor.fetchall())
# [('Alice', 'Engineering'), ('Bob', 'Marketing'), ('Charlie', 'Engineering'), ('Diana', None)]

conn.close()
```

---

##  Aggregate Functions

```sql
-- COUNT -- number of rows
SELECT COUNT(*) FROM employees;
SELECT COUNT(DISTINCT department) FROM employees;

-- SUM -- total of numeric column
SELECT SUM(salary) FROM employees;

-- AVG -- average value
SELECT AVG(salary) FROM employees;

-- MIN / MAX -- smallest / largest value
SELECT MIN(salary), MAX(salary) FROM employees;

-- GROUP BY -- aggregate by groups
SELECT department, COUNT(*) as emp_count, AVG(salary) as avg_salary
FROM employees
GROUP BY department;

-- HAVING -- filter groups (like WHERE but for aggregated data)
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 70000;
```

### Python Example

```python
import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        category TEXT,
        amount REAL,
        quantity INTEGER
    )
''')

sales_data = [
    (1, 'Laptop', 'Electronics', 1200, 2),
    (2, 'Phone', 'Electronics', 800, 5),
    (3, 'Desk', 'Furniture', 350, 3),
    (4, 'Chair', 'Furniture', 200, 8),
    (5, 'Tablet', 'Electronics', 600, 4),
    (6, 'Bookshelf', 'Furniture', 150, 6),
]
cursor.executemany('INSERT INTO sales VALUES (?,?,?,?,?)', sales_data)

# Aggregation with GROUP BY
cursor.execute('''
    SELECT category,
           COUNT(*) as num_products,
           SUM(amount * quantity) as total_revenue,
           AVG(amount) as avg_price,
           MIN(amount) as min_price,
           MAX(amount) as max_price
    FROM sales
    GROUP BY category
    HAVING total_revenue > 1000
    ORDER BY total_revenue DESC
''')

print(f"{'Category':<15} {'Products':<10} {'Revenue':<12} {'Avg Price':<10}")
print("-" * 50)
for row in cursor.fetchall():
    print(f"{row[0]:<15} {row[1]:<10} ${row[2]:<11,.2f} ${row[3]:<9,.2f}")

conn.close()
```

---

##  Transactions

A **transaction** is a sequence of operations performed as a single logical unit of work.

### ACID Properties

| Property | Description | Example |
|----------|-------------|---------|
| **Atomicity** | All or nothing -- either all operations succeed or none | Bank transfer: debit AND credit must both succeed |
| **Consistency** | Database moves from one valid state to another | Total balance remains the same after transfer |
| **Isolation** | Concurrent transactions don't interfere | Two transfers happening simultaneously |
| **Durability** | Committed changes survive system failures | Data persists after power outage |

### Transaction Commands

```sql
-- Start a transaction (implicit in most RDBMS)
BEGIN TRANSACTION;

-- Perform operations
UPDATE accounts SET balance = balance - 500 WHERE id = 1;
UPDATE accounts SET balance = balance + 500 WHERE id = 2;

-- Save intermediate point
SAVEPOINT before_fee;

-- More operations
UPDATE accounts SET balance = balance - 10 WHERE id = 1;  -- Service fee

-- Rollback to savepoint if needed
ROLLBACK TO SAVEPOINT before_fee;

-- Commit all changes
COMMIT;

-- Or rollback everything
ROLLBACK;
```

### Python Transaction Example

```python
import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE accounts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        balance REAL
    )
''')
cursor.executemany('INSERT INTO accounts VALUES (?,?,?)',
    [(1, 'Alice', 1000), (2, 'Bob', 500)])
conn.commit()

def transfer_funds(conn, from_id, to_id, amount):
    """Transfer funds between accounts with transaction safety."""
    try:
        cursor = conn.cursor()

        # Check sufficient balance
        cursor.execute('SELECT balance FROM accounts WHERE id = ?', (from_id,))
        balance = cursor.fetchone()[0]

        if balance < amount:
            raise ValueError(f"Insufficient funds: {balance} < {amount}")

        # Perform transfer
        cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?',
                       (amount, from_id))
        cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?',
                       (amount, to_id))

        conn.commit()
        print(f" Transferred ${amount} from Account {from_id} to Account {to_id}")

    except Exception as e:
        conn.rollback()
        print(f" Transaction failed: {e}")

# Successful transfer
transfer_funds(conn, 1, 2, 300)

# Failed transfer (insufficient funds)
transfer_funds(conn, 1, 2, 5000)

# Verify balances
cursor.execute('SELECT * FROM accounts')
for row in cursor.fetchall():
    print(f"Account {row[0]} ({row[1]}): ${row[2]:.2f}")

conn.close()
```

---

##  Summary

### First Half -- Advanced Coding
| Topic | Key Takeaway |
|-------|-------------|
| Mock Interviews | Use UMPIRE method, think aloud, handle edge cases |
| Pandas Optimization | Vectorize operations, avoid loops, use `.query()` |
| Collections | Counter for frequency, defaultdict for grouping, deque for BFS |
| Dict & Set | O(1) lookup, set operations for efficient comparisons |
| Sliding Window | Fixed-size and variable-size patterns for subarray problems |
| Debugging | Use logging, refactor code smells, write testable code |

### Second Half -- RDBMS
| Topic | Key Takeaway |
|-------|-------------|
| DBMS vs RDBMS | RDBMS uses tables, supports SQL, ACID, normalization |
| ER Model | Entities, attributes, relationships define database structure |
| Keys | PK uniquely identifies, FK creates relationships |
| Normalization | 1NF2NF3NFBCNF eliminates redundancy progressively |
| SQL Queries | SELECT, WHERE, ORDER BY, LIMIT for data retrieval |
| Joins | INNER, LEFT, RIGHT, FULL OUTER for combining tables |
| Aggregates | COUNT, SUM, AVG with GROUP BY, HAVING for analytics |
| Transactions | ACID ensures data integrity; COMMIT/ROLLBACK for safety |

---

##  Day 13 Files
- `official_questions/01_lru_cache.py` -- LeetCode 146: LRU Cache
- `official_questions/02_valid_parentheses.py` -- LeetCode 20: Valid Parentheses
- `official_questions/03_contains_duplicate_ii.py` -- LeetCode 219: Contains Duplicate II
- `Corporate_use_case/data_warehouse_reporting.py` -- Enterprise Data Warehouse System
- `practice/sliding_window.py` -- Sliding Window Pattern Examples
- `practice/sql_concepts.py` -- SQL Concepts with sqlite3
