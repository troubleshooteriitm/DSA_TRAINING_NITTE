#  Python DSA Training -- 14-Day Intensive Program

> **Level:** Intermediate to Advanced  
> **Language:** Python 3  
> **Focus:** DSA, Corporate Use Cases, Interview Prep  

A comprehensive 14-day Python training curriculum covering Data Structures & Algorithms, Object-Oriented Programming, Data Analytics, Cloud/DevOps fundamentals, and real-world enterprise projects.

---

##  Curriculum Overview

| Day | Topic | Key Concepts | LeetCode Problems |
|:---:|-------|-------------|-------------------|
| **1** | [Python Introduction & Setup](./Day_1/) | Python Overview, pip, venv, PEP8, Unit Testing | Fizz Buzz, Palindrome Number |
| **2** | [Python Fundamentals](./Day_2/) | Variables, Data Types, Strings, Operators, I/O | Valid Anagram, Reverse Integer |
| **3** | [Flow Control & Loops](./Day_3/) | Conditionals, for/while, Nested Loops, Patterns | Fizz Buzz, Power of Two |
| **4** | [Functions & Functional Programming](./Day_4/) | Lambda, Decorators, Generators, Recursion | Climbing Stairs, Two Sum |
| **5** | [Collections & Comprehensions](./Day_5/) | Lists, Dicts, Sets, Counter, defaultdict, deque | Group Anagrams, Majority Element |
| **6** | [Object-Oriented Programming](./Day_6/) | Classes, Inheritance, Encapsulation, Polymorphism | Design Parking System, Merge Intervals |
| **7** | [Exception Handling & Debugging](./Day_7/) | try-except, Custom Exceptions, Logging | Missing Number, Single Number |
| **8** | [File Handling & Data Processing](./Day_8/) | CSV, JSON, XML, File I/O, Log Parsing | Valid Sudoku, Matrix Diagonal Sum |
| **9** | [Modules, Packages & Database](./Day_9/) | sqlite3, CRUD, Transactions, Modules | Rotate Array, Majority Element |
| **10** | [NumPy, Pandas & Data Analytics](./Day_10/) | DataFrames, ETL, GroupBy, Merging | Maximum Subarray, Buy & Sell Stock |
| **11** | [Matplotlib, Data Science & Scikit-Learn](./Day_11/) | Visualization, ML Basics, Classification | Binary Search, Merge Sorted Array |
| **12** | [Advanced Python & Problem Solving](./Day_12/) | Threading, APIs, Heapq, Performance | Longest Substring, Top K Frequent |
| **13** | [Advanced Coding + RDBMS](./Day_13/) | Sliding Window, SQL, Joins, Normalization | LRU Cache, Valid Parentheses |
| **14** | [Cloud, Docker, K8s & CI/CD](./Day_14/) | Git, Docker, Kubernetes, GitHub Actions | Single Number, Move Zeroes |

---

##  Project Structure

Each day follows a consistent structure:

```
Day_X/
 README.md              #  Detailed theory notes with code examples
 official_questions/     #  LeetCode & HackerRank solutions with tests
 Corporate_use_case/     #  Enterprise-grade runnable projects
 practice/               #  Hands-on exercises and demos
```

---

##  Corporate Use Cases

| Day | Project | Technologies Used |
|:---:|---------|------------------|
| 1 | Excel Report Automation (VBA  Python) | csv, data processing |
| 2 | Employee Data Validation Engine | regex, validation |
| 3 | IT Ticket Routing & Priority System | conditionals, loops |
| 4 | Enterprise Validation Framework | decorators, functional programming |
| 5 | Order Processing Dashboard | Counter, defaultdict, comprehensions |
| 6 | HR Hierarchy & Role Management | OOP, inheritance, RBAC |
| 7 | Payroll Recovery & Transaction Validation | exceptions, logging, retry |
| 8 | Security Audit Log Analyzer | file I/O, CSV, JSON |
| 9 | Employee Attendance Management | sqlite3, CRUD, SQL |
| 10 | Sales Analytics Dashboard | pandas, data analytics |
| 11 | Employee Attrition Predictor | scikit-learn, ML classification |
| 12 | Real-Time Data Processing Pipeline | threading, heapq, deque |
| 13 | Data Warehouse Reporting System | sqlite3, star schema, SQL joins |
| 14 | Microservices Deployment Pipeline | service registry, CI/CD, Docker configs |

---

##  Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup
```bash
# Clone the repository
git clone https://github.com/troubleshooteriitm/DSA_TRAINING_NITTE.git
cd DSA_TRAINING_NITTE

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# Install optional dependencies (for Days 10-11)
pip install numpy pandas matplotlib scikit-learn
```

### Run any Python file
```bash
python Day_3/official_questions/02_power_of_two.py
python Day_6/Corporate_use_case/hr_hierarchy_system.py
```

---

##  Key Libraries

| Library | Usage | Days |
|---------|-------|------|
| `collections` | Counter, defaultdict, deque, OrderedDict | 5, 12, 13 |
| `sqlite3` | Database connectivity, CRUD, SQL | 9, 13 |
| `csv` / `json` | Data processing | 1, 8 |
| `threading` | Multithreading | 12 |
| `logging` | Enterprise logging | 7 |
| `re` | Regular expressions | 2, 4 |
| `heapq` | Priority queues | 12 |
| `numpy` | Numerical computing | 10 |
| `pandas` | Data analysis & ETL | 10 |
| `matplotlib` | Data visualization | 11 |
| `scikit-learn` | Machine learning | 11 |

---

##  Recommended Practice Platforms

- [LeetCode](https://leetcode.com) -- Algorithm challenges
- [HackerRank Python](https://www.hackerrank.com/domains/python) -- Python-specific practice
- [GeeksforGeeks Python](https://www.geeksforgeeks.org/python-programming-language/) -- Concepts & problems
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-Learn Documentation](https://scikit-learn.org/stable/)

---

##  Collections Quick Reference

| Collection | Key Methods | Best For |
|------------|-------------|----------|
| `list` | append, extend, sort, slice | Ordered mutable sequences |
| `tuple` | immutable, packing/unpacking | Fixed data, dict keys |
| `dict` | get, update, items, keys | Key-value mapping |
| `set` | add, discard, union, intersection | Unique elements, O(1) lookup |
| `Counter` | most_common, elements | Frequency counting |
| `defaultdict` | auto-initialize missing keys | Grouping, counting |
| `deque` | appendleft, popleft, rotate | Queues, sliding windows |
| `OrderedDict` | move_to_end, popitem | Ordered key-value (LRU) |
| `heapq` | heappush, heappop, nlargest | Priority queues, top-K |

---

*Built with  for Python learners*
