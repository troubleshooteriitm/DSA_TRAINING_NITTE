#  Day 1: Python Fundamentals & Environment Setup

> **DSA Training -- Day 1**
> Master the Python ecosystem before diving into Data Structures & Algorithms.

---

## Table of Contents

1. [Python Overview](#1-python-overview)
2. [Python 2 vs Python 3](#2-python-2-vs-python-3)
3. [Advantages & Disadvantages of Python](#3-advantages--disadvantages-of-python)
4. [Installation Guide](#4-installation-guide)
5. [IDE Setup](#5-ide-setup)
6. [Python Interpreter](#6-python-interpreter)
7. [pip -- Python Package Installer](#7-pip--python-package-installer)
8. [Virtual Environments](#8-virtual-environments)
9. [pydoc, help(), and dir()](#9-pydoc-help-and-dir)
10. [Unit Testing Basics](#10-unit-testing-basics)
11. [PEP 8 Coding Standards](#11-pep-8-coding-standards)

---

## 1. Python Overview

### What is Python?

Python is a **high-level, interpreted, general-purpose** programming language created by **Guido van Rossum**. It emphasises code readability with its use of significant indentation and a clean, expressive syntax.

### Brief History

| Year | Milestone |
|------|-----------|
| 1991 | Python 0.9.0 released by Guido van Rossum |
| 2000 | Python 2.0 -- list comprehensions, garbage collection |
| 2008 | Python 3.0 -- backward-incompatible modernisation |
| 2020 | Python 2 officially reaches End of Life (EOL) |
| 2024 | Python 3.12+ -- performance improvements, better error messages |

### Use Cases

- **Web Development** -- Django, Flask, FastAPI
- **Data Science & Machine Learning** -- NumPy, Pandas, Scikit-learn, TensorFlow
- **Automation & Scripting** -- DevOps pipelines, file processing, web scraping
- **Desktop Applications** -- Tkinter, PyQt
- **API Development** -- RESTful services, microservices
- **Competitive Programming & DSA** -- LeetCode, Codeforces, HackerRank

```python
# A taste of Python
def greet(name: str) -> str:
    """Return a personalised greeting."""
    return f"Hello, {name}! Welcome to DSA Training "

print(greet("Student"))
# Output: Hello, Student! Welcome to DSA Training 
```

---

## 2. Python 2 vs Python 3

>  **Python 2 reached End of Life on January 1, 2020.** Always use Python 3 for new projects.

### Key Differences

| Feature | Python 2 | Python 3 |
|---------|----------|----------|
| Print | `print "Hello"` (statement) | `print("Hello")` (function) |
| Integer Division | `5 / 2  2` | `5 / 2  2.5` |
| Unicode | ASCII by default | Unicode by default |
| `range()` | Returns a list | Returns an iterator |
| `input()` | `raw_input()` for strings | `input()` always returns string |
| Syntax | `except Exception, e:` | `except Exception as e:` |

### Code Comparison

```python
# ---- Python 2 (LEGACY -- do NOT use) ----
# print "Hello, World!"
# x = 5 / 2          # Result: 2 (integer division)
# name = raw_input("Enter name: ")

# ---- Python 3 (USE THIS) ----
print("Hello, World!")
x = 5 / 2             # Result: 2.5 (true division)
y = 5 // 2            # Result: 2 (floor division)
name = input("Enter name: ")
```

```python
# range() difference
# Python 2: range(5) returns [0, 1, 2, 3, 4] -- a full list in memory
# Python 3: range(5) returns range(0, 5)     -- a lazy iterator (memory-efficient)

for i in range(5):
    print(i, end=" ")
# Output: 0 1 2 3 4
```

```python
# String handling
# Python 2: strings are bytes by default
# Python 3: strings are Unicode by default

text = "नमस्ते"   # Hindi for "Hello"
print(text)         # Works perfectly in Python 3
print(len(text))    # Correctly counts Unicode characters
```

---

## 3. Advantages & Disadvantages of Python

###  Advantages

| Advantage | Description |
|-----------|-------------|
| **Easy to Learn** | Clean syntax, reads almost like English |
| **Rich Ecosystem** | 400,000+ packages on PyPI |
| **Cross-Platform** | Runs on Windows, macOS, Linux |
| **Community** | Massive community, abundant resources |
| **Versatile** | Web, ML, automation, scripting, and more |
| **Rapid Prototyping** | Write less code, ship faster |
| **Dynamic Typing** | No need to declare variable types explicitly |

###  Disadvantages

| Disadvantage | Description |
|--------------|-------------|
| **Slower Execution** | Interpreted language; slower than C/C++/Java for CPU-intensive tasks |
| **GIL (Global Interpreter Lock)** | Limits true multi-threading in CPython |
| **Memory Consumption** | Higher memory usage compared to lower-level languages |
| **Mobile Development** | Not a first-choice for mobile apps |
| **Runtime Errors** | Dynamic typing means type errors surface at runtime |

```python
# Dynamic typing -- flexible but requires discipline
x = 10          # x is an int
x = "hello"     # x is now a str -- no compiler error!
x = [1, 2, 3]   # x is now a list

# Type hints (Python 3.5+) help mitigate this
def add(a: int, b: int) -> int:
    return a + b
```

---

## 4. Installation Guide

### Windows

1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. ** Check "Add Python to PATH"** during installation
3. Verify:

```bash
python --version
# Python 3.12.x

pip --version
# pip 24.x from ...
```

### macOS

```bash
# Using Homebrew (recommended)
brew install python3

python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

python3 --version
```

### Verify Installation

```python
# Open terminal and type:
python -c "import sys; print(sys.version)"
# 3.12.x (main, ...) [GCC ...] or [MSC ...]

python -c "import this"
# Prints 'The Zen of Python' -- Python's guiding principles
```

---

## 5. IDE Setup

### VS Code (Recommended for this course)

1. **Install VS Code** from [code.visualstudio.com](https://code.visualstudio.com/)
2. **Install the Python Extension**:
   - Open VS Code → Extensions (`Ctrl+Shift+X`)
   - Search "Python" → Install the one by Microsoft
3. **Recommended Extensions**:
   - `Python` -- IntelliSense, linting, debugging
   - `Pylance` -- Fast type checking and auto-completion
   - `Code Runner` -- Run code with a shortcut
   - `Python Indent` -- Correct indentation
4. **Configure Python Interpreter**:
   - `Ctrl+Shift+P`  "Python: Select Interpreter"  Choose your Python 3.x

```json
// .vscode/settings.json (recommended settings)
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.analysis.typeCheckingMode": "basic"
}
```

### PyCharm

1. **Install PyCharm** from [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)
   - **Community Edition** is free and sufficient for this course
2. **Create a New Project**: File → New Project → Select Python interpreter
3. **Key Features**:
   - Built-in debugger with breakpoints
   - Integrated terminal
   - Code inspection and refactoring tools
   - Built-in test runner

---

## 6. Python Interpreter

Python can be run in two modes: **Interactive Mode** and **Script Mode**.

### Interactive Mode (REPL)

REPL = **R**ead → **E**valuate → **P**rint → **L**oop

```bash
# Launch the Python REPL
$ python
Python 3.12.x (main, ...)
>>> 
```

```python
>>> 2 + 3
5
>>> name = "DSA"
>>> f"Welcome to {name} Training"
'Welcome to DSA Training'
>>> type(42)
<class 'int'>
>>> [x**2 for x in range(5)]
[0, 1, 4, 9, 16]
>>> exit()   # or Ctrl+D on Linux/macOS, Ctrl+Z on Windows
```

**When to use interactive mode:**
- Quick calculations and experimentation
- Testing small code snippets
- Exploring modules and functions
- Debugging

### Script Mode

Save code in a `.py` file and execute it:

```python
# hello.py
def main():
    name = input("What is your name? ")
    print(f"Hello, {name}! Let's learn DSA together.")

if __name__ == "__main__":
    main()
```

```bash
$ python hello.py
What is your name? Alice
Hello, Alice! Let's learn DSA together.
```

### The `if __name__ == "__main__"` Guard

```python
# my_module.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# This block runs ONLY when the file is executed directly
# It does NOT run when the file is imported as a module
if __name__ == "__main__":
    print(add(5, 3))        # 8
    print(subtract(10, 4))  # 6
```

```python
# another_file.py
import my_module

# Only the functions are imported; the print statements in
# my_module's __main__ block do NOT execute
result = my_module.add(2, 3)
print(result)  # 5
```

---

## 7. pip -- Python Package Installer

`pip` is the standard package manager for Python. It installs packages from [PyPI](https://pypi.org/) (Python Package Index).

### Basic Commands

```bash
# Install a package
pip install requests

# Install a specific version
pip install requests==2.31.0

# Install minimum version
pip install "requests>=2.25.0"

# Upgrade a package
pip install --upgrade requests

# Uninstall a package
pip uninstall requests

# Show package info
pip show requests

# List all installed packages
pip list
```

### pip freeze & requirements.txt

```bash
# Export all installed packages to a file
pip freeze > requirements.txt

# The file looks like:
# certifi==2024.2.2
# charset-normalizer==3.3.2
# idna==3.6
# requests==2.31.0
# urllib3==2.2.1

# Install all packages from requirements.txt (on another machine)
pip install -r requirements.txt
```

### Practical Example

```python
# After installing: pip install requests
import requests

response = requests.get("https://api.github.com")
print(f"Status Code: {response.status_code}")
print(f"Content Type: {response.headers['content-type']}")
```

### Useful pip Commands

```bash
# Search for outdated packages
pip list --outdated

# Install from a local wheel file
pip install package_name.whl

# Install in editable/development mode (from project root)
pip install -e .

# Check for dependency conflicts
pip check
```

---

## 8. Virtual Environments

A **virtual environment** is an isolated Python environment that has its own set of installed packages, independent of the system-wide Python installation.

### Why Use Virtual Environments?

```
Project A needs requests==2.25.0
Project B needs requests==2.31.0

Without venv  Conflict! Only one version installed globally.
With venv     Each project has its own isolated copy. 
```

### Creating & Using venv

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# Windows (Command Prompt):
venv\Scripts\activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# macOS / Linux:
source venv/bin/activate

# Your prompt changes to show the active environment:
# (venv) $

# Install packages (isolated to this venv)
pip install requests flask

# Check where Python is running from
python -c "import sys; print(sys.executable)"
# Should show a path inside the venv directory

# Freeze dependencies
pip freeze > requirements.txt

# Deactivate the virtual environment
deactivate
```

### Best Practices

```bash
# 1. Always add venv to .gitignore
echo "venv/" >> .gitignore

# 2. Use descriptive names or just 'venv'
python -m venv .venv   # Hidden directory (common convention)

# 3. Recreate from requirements.txt on a new machine
python -m venv venv
venv\Scripts\activate        # or source venv/bin/activate
pip install -r requirements.txt
```

### Complete Workflow Example

```bash
# Start a new project
mkdir my_dsa_project && cd my_dsa_project

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # (or venv\Scripts\activate on Windows)

# Install dependencies
pip install pytest black pylint

# Save dependencies
pip freeze > requirements.txt

# Work on your project...
python my_solution.py

# When done
deactivate
```

---

## 9. pydoc, help(), and dir()

Python has powerful built-in tools for exploring and documenting code.

### help() -- Interactive Help

```python
# Get help on a built-in function
>>> help(len)
# Help on built-in function len in module builtins:
# len(obj, /)
#     Return the number of items in a container.

# Get help on a data type
>>> help(str)
# (Shows full documentation for the str class)

# Get help on a specific method
>>> help(str.split)
# Help on method_descriptor:
# split(self, /, sep=None, maxsplit=-1)
#     Return a list of the substrings ...

# Get help on a module
>>> import os
>>> help(os.path.join)

# Interactive help mode
>>> help()
# Welcome to Python's help utility!
# help> str
# help> quit
```

### dir() -- List Attributes and Methods

```python
# List all attributes/methods of an object
>>> dir(str)
['__add__', '__class__', ..., 'capitalize', 'casefold', 'center',
 'count', 'encode', 'endswith', 'find', 'format', ...]

# Filter out dunder methods to see the "public" API
>>> [m for m in dir(str) if not m.startswith('_')]
['capitalize', 'casefold', 'center', 'count', 'encode', 'endswith',
 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', ...]

# dir() on a list
>>> my_list = [1, 2, 3]
>>> [m for m in dir(my_list) if not m.startswith('_')]
['append', 'clear', 'copy', 'count', 'extend', 'index',
 'insert', 'pop', 'remove', 'reverse', 'sort']

# dir() with no arguments -- shows names in current scope
>>> x = 10
>>> name = "hello"
>>> dir()
['__builtins__', ..., 'name', 'x']
```

### pydoc -- Documentation from the Command Line

```bash
# View documentation for a module
python -m pydoc os

# View documentation for a specific function
python -m pydoc os.path.join

# Search for a keyword across all modules
python -m pydoc -k sort

# Start a local documentation server (opens browser)
python -m pydoc -b

# Generate HTML documentation for a module
python -m pydoc -w my_module
# Creates my_module.html in the current directory
```

### Writing Your Own Docstrings

```python
def binary_search(arr: list[int], target: int) -> int:
    """
    Perform binary search on a sorted array.

    Args:
        arr: A sorted list of integers.
        target: The integer to search for.

    Returns:
        The index of the target if found, otherwise -1.

    Examples:
        >>> binary_search([1, 3, 5, 7, 9], 5)
        2
        >>> binary_search([1, 3, 5, 7, 9], 4)
        -1
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Access the docstring programmatically
print(binary_search.__doc__)

# Or use help()
help(binary_search)
```

---

## 10. Unit Testing Basics

### The `unittest` Module

Python's built-in `unittest` module provides a framework for writing and running tests.

```python
# test_math_operations.py
import unittest


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def divide(a, b):
    """Return a divided by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome (case-insensitive)."""
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


class TestMathOperations(unittest.TestCase):
    """Test suite for math operations."""

    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

    def test_add_zero(self):
        self.assertEqual(add(0, 0), 0)

    def test_divide(self):
        self.assertAlmostEqual(divide(10, 3), 3.3333, places=3)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_palindrome_true(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))

    def test_palindrome_false(self):
        self.assertFalse(is_palindrome("hello"))


if __name__ == "__main__":
    unittest.main()
```

### Running Tests

```bash
# Run all tests in a file
python -m unittest test_math_operations.py

# Run with verbose output
python -m unittest test_math_operations.py -v

# Run a specific test class
python -m unittest test_math_operations.TestMathOperations

# Run a specific test method
python -m unittest test_math_operations.TestMathOperations.test_add_positive_numbers

# Discover and run all tests in a directory
python -m unittest discover -s tests -p "test_*.py"
```

### Common Assert Methods

| Method | Checks |
|--------|--------|
| `assertEqual(a, b)` | `a == b` |
| `assertNotEqual(a, b)` | `a != b` |
| `assertTrue(x)` | `bool(x) is True` |
| `assertFalse(x)` | `bool(x) is False` |
| `assertIs(a, b)` | `a is b` |
| `assertIsNone(x)` | `x is None` |
| `assertIn(a, b)` | `a in b` |
| `assertIsInstance(a, b)` | `isinstance(a, b)` |
| `assertRaises(exc)` | Exception is raised |
| `assertAlmostEqual(a, b)` | `round(a-b, 7) == 0` |

### Test Setup & Teardown

```python
import unittest


class TestWithSetup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Run once before ALL tests in this class."""
        print("Setting up test class...")
        cls.shared_data = [1, 2, 3, 4, 5]

    def setUp(self):
        """Run before EACH test method."""
        self.test_list = self.shared_data.copy()

    def test_append(self):
        self.test_list.append(6)
        self.assertEqual(len(self.test_list), 6)
        self.assertIn(6, self.test_list)

    def test_remove(self):
        self.test_list.remove(3)
        self.assertEqual(len(self.test_list), 4)
        self.assertNotIn(3, self.test_list)

    def tearDown(self):
        """Run after EACH test method."""
        self.test_list = None

    @classmethod
    def tearDownClass(cls):
        """Run once after ALL tests in this class."""
        print("Tearing down test class...")


if __name__ == "__main__":
    unittest.main()
```

---

## 11. PEP 8 Coding Standards

[PEP 8](https://peps.python.org/pep-0008/) is the official style guide for Python code. Following it makes your code consistent, readable, and professional.

### Naming Conventions

```python
#  GOOD -- PEP 8 compliant

# Variables and functions: snake_case
student_name = "Alice"
total_score = 95

def calculate_average(scores: list[float]) -> float:
    return sum(scores) / len(scores)

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DATABASE_URL = "sqlite:///db.sqlite3"
PI = 3.14159

# Classes: PascalCase (CapWords)
class BinarySearchTree:
    pass

class LinkedListNode:
    pass

# Private/internal: leading underscore
_internal_cache = {}

def _helper_function():
    pass

# "Private" (name-mangled): double leading underscore
class MyClass:
    def __init__(self):
        self.__secret = 42   # Becomes _MyClass__secret
```

```python
#  BAD -- NOT PEP 8 compliant

studentName = "Alice"           # camelCase for variables
def CalculateAverage(scores):   # PascalCase for functions
    return sum(scores) / len(scores)

max_retries = 3                 # lowercase for constants
class binary_search_tree:       # snake_case for classes
    pass
```

### Indentation & Spacing

```python
#  Use 4 spaces per indentation level (NEVER tabs)
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


#  Surround top-level definitions with TWO blank lines
class Stack:
    pass


def helper():
    pass


#  Surround method definitions inside a class with ONE blank line
class Queue:

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)
```

### Line Length & Line Breaks

```python
#  Maximum 79 characters per line (72 for docstrings/comments)

# Use implicit line continuation inside brackets
result = (first_value
          + second_value
          - third_value)

# Or use backslash for explicit continuation
total = first_long_variable_name \
        + second_long_variable_name \
        - third_long_variable_name

# Long function calls
output = some_function(
    argument_one,
    argument_two,
    argument_three,
    argument_four,
)

# Long imports
from my_module import (
    ClassOne,
    ClassTwo,
    function_one,
    function_two,
)
```

### Whitespace Rules

```python
#  GOOD
x = 1
y = x + 2
my_list = [1, 2, 3]
my_dict = {"key": "value"}
result = func(arg1, arg2)
my_list[0]

#  BAD
x=1
y = x+2
my_list = [1 , 2 , 3]
my_dict = { "key" : "value" }
result = func( arg1, arg2 )
my_list [0]
```

### Import Guidelines

```python
#  GOOD -- Each import on its own line, grouped and ordered

# 1. Standard library imports
import os
import sys
from collections import defaultdict

# 2. Third-party library imports
import numpy as np
import requests

# 3. Local application imports
from my_module import my_function
from my_package.utils import helper


#  BAD
import os, sys                           # Multiple imports on one line
from os import *                         # Wildcard imports
import requests, numpy as np, flask      # Mixed on one line
```

### Docstring Standards

```python
#  Single-line docstring
def square(n: int) -> int:
    """Return the square of n."""
    return n * n


#  Multi-line docstring (Google style -- recommended for this course)
def merge_sort(arr: list[int]) -> list[int]:
    """
    Sort a list using the merge sort algorithm.

    This implementation uses the divide-and-conquer approach,
    recursively splitting the list and merging sorted halves.

    Args:
        arr: A list of integers to sort.

    Returns:
        A new sorted list of integers.

    Raises:
        TypeError: If input is not a list.

    Examples:
        >>> merge_sort([3, 1, 4, 1, 5])
        [1, 1, 3, 4, 5]
        >>> merge_sort([])
        []
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)
```

### Type Hints (PEP 484)

```python
# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}"

# Collections
def process(items: list[int]) -> dict[str, int]:
    return {"sum": sum(items), "count": len(items)}

# Optional values
from typing import Optional

def find(arr: list[int], target: int) -> Optional[int]:
    """Return index of target or None if not found."""
    try:
        return arr.index(target)
    except ValueError:
        return None
```

### Quick PEP 8 Checklist

- [x] Use 4 spaces for indentation (never tabs)
- [x] Maximum line length: 79 characters
- [x] Use `snake_case` for variables and functions
- [x] Use `PascalCase` for classes
- [x] Use `UPPER_SNAKE_CASE` for constants
- [x] Two blank lines before/after top-level definitions
- [x] One blank line between methods in a class
- [x] Imports at the top, grouped (stdlib → third-party → local)
- [x] Spaces around operators: `x = 1`, not `x=1`
- [x] No trailing whitespace
- [x] End files with a single newline
- [x] Write docstrings for all public modules, classes, and functions

### Enforcing PEP 8

```bash
# Check PEP 8 compliance
pip install pycodestyle
pycodestyle my_script.py

# Auto-format with Black (opinionated formatter)
pip install black
black my_script.py

# Lint with pylint (comprehensive static analysis)
pip install pylint
pylint my_script.py

# Sort imports with isort
pip install isort
isort my_script.py

# All-in-one with flake8
pip install flake8
flake8 my_script.py
```

---

##  Day 1 Practice Exercises

1. **Setup Check**: Install Python 3, create a virtual environment, and install `pytest`.
2. **Interactive Exploration**: Use `help()` and `dir()` to explore the `list` and `dict` types.
3. **Write Tests**: Create a `test_basics.py` file with tests for a simple `is_even()` function.
4. **PEP 8 Audit**: Take any Python file and run `pycodestyle` on it. Fix all issues.
5. **Solve**: Complete the palindrome number problem in `official_questions/02_palindrome_number.py`.

---

>  **Next**: Day 2 -- Data Types, Variables, Operators & Control Flow
