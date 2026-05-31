# Day 4 -- Functions & Functional Programming

> **Objective:** Master Python functions from basics to advanced concepts including
> decorators, generators, and functional programming paradigms.

---

## Table of Contents

1. [Function Definitions](#1-function-definitions)
2. [Parameters](#2-parameters)
3. [Variable Scope](#3-variable-scope--legb-rule)
4. [*args and **kwargs](#4-args-and-kwargs)
5. [Lambda Functions](#5-lambda-functions)
6. [map(), filter(), reduce()](#6-map-filter-reduce)
7. [Decorators](#7-decorators)
8. [Generators](#8-generators)
9. [Recursive Functions](#9-recursive-functions)

---

## 1. Function Definitions

Functions are reusable blocks of code defined using the `def` keyword. They promote
**DRY** (Don't Repeat Yourself) principles and make code modular.

### Basic Syntax

```python
def greet(name):
    """Return a greeting message for the given name."""
    return f"Hello, {name}!"

# Calling the function
message = greet("Alice")
print(message)  # Output: Hello, Alice!
```

### Key Components

| Component   | Description                                     |
|-------------|-------------------------------------------------|
| `def`       | Keyword to define a function                    |
| Name        | Identifier following PEP8 (snake_case)          |
| Parameters  | Inputs listed in parentheses                    |
| Docstring   | Optional documentation string (triple quotes)   |
| `return`    | Statement to send back a value (default: None)  |

### Docstrings

Docstrings document what a function does. They follow the **Google**, **NumPy**, or
**reStructuredText** style conventions.

```python
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.

    Args:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.

    Returns:
        float: The area of the rectangle.

    Raises:
        ValueError: If length or width is negative.
    """
    if length < 0 or width < 0:
        raise ValueError("Dimensions must be non-negative")
    return length * width
```

### Functions Returning Multiple Values

```python
def min_max(numbers):
    """Return both minimum and maximum of a list."""
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 4, 1, 5, 9])
print(f"Min: {lo}, Max: {hi}")  # Min: 1, Max: 9
```

---

## 2. Parameters

Python supports several parameter types that provide flexibility in how functions
accept arguments.

### Positional Parameters

```python
def power(base, exponent):
    """Calculate base raised to exponent."""
    return base ** exponent

print(power(2, 10))  # 1024 -- positional arguments
```

### Keyword Parameters

```python
print(power(exponent=10, base=2))  # 1024 -- keyword arguments (order doesn't matter)
```

### Default Values

```python
def connect(host, port=3306, timeout=30):
    """Simulate a database connection with defaults."""
    return f"Connecting to {host}:{port} (timeout={timeout}s)"

print(connect("localhost"))               # Uses defaults: port=3306, timeout=30
print(connect("localhost", port=5432))     # Override port only
print(connect("db.server.com", 5432, 60)) # Override both
```

>  **Important:** Default values are evaluated once at function definition time.
> Avoid using mutable defaults like lists or dicts.

```python
# BAD -- mutable default (shared across calls)
def append_to(item, target=[]):
    target.append(item)
    return target

# GOOD -- use None as sentinel
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

### Keyword-Only Parameters (after `*`)

```python
def create_user(name, *, email, role="viewer"):
    """Force email and role to be keyword-only arguments."""
    return {"name": name, "email": email, "role": role}

user = create_user("Alice", email="alice@example.com", role="admin")
```

### Positional-Only Parameters (before `/`) -- Python 3.8+

```python
def divide(a, b, /):
    """a and b must be passed positionally."""
    return a / b

print(divide(10, 3))    # OK
# print(divide(a=10, b=3))  # TypeError
```

---

## 3. Variable Scope & LEGB Rule

Python resolves variable names using the **LEGB** rule:

| Scope       | Description                              | Example           |
|-------------|------------------------------------------|--------------------|
| **L**ocal   | Inside the current function              | Function variables |
| **E**nclosing | In the enclosing function (closures)   | Outer function     |
| **G**lobal  | At the module level                      | Module variables   |
| **B**uilt-in | Python's built-in names                 | `print`, `len`     |

### Local vs Global

```python
x = "global"

def outer():
    x = "local"
    print(f"Inside function: {x}")  # local

outer()
print(f"Outside function: {x}")    # global
```

### The `global` Keyword

```python
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)  # 2
```

### The `nonlocal` Keyword (for closures)

```python
def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1
        return count

    return inner

counter = outer()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

### LEGB Resolution Example

```python
x = "built-in level (global)"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)  # Resolves to "local"

    inner()

outer()
```

---

## 4. *args and **kwargs

These special syntax elements allow functions to accept a variable number of arguments.

### *args -- Variable Positional Arguments

`*args` collects extra positional arguments into a **tuple**.

```python
def calculate_average(*args):
    """Calculate the average of any number of values."""
    if not args:
        return 0
    return sum(args) / len(args)

print(calculate_average(85, 90, 78, 92))  # 86.25
print(calculate_average(100))              # 100.0
```

### **kwargs -- Variable Keyword Arguments

`**kwargs` collects extra keyword arguments into a **dictionary**.

```python
def build_profile(name, **kwargs):
    """Build a user profile from keyword arguments."""
    profile = {"name": name}
    profile.update(kwargs)
    return profile

user = build_profile("Alice", age=30, city="NYC", role="Engineer")
print(user)
# {'name': 'Alice', 'age': 30, 'city': 'NYC', 'role': 'Engineer'}
```

### Combining *args and **kwargs

```python
def log_event(event_type, *args, **kwargs):
    """Log an event with optional details and metadata."""
    print(f"Event: {event_type}")
    if args:
        print(f"  Details: {args}")
    if kwargs:
        print(f"  Metadata: {kwargs}")

log_event("LOGIN", "user123", "success", ip="192.168.1.1", duration=0.5)
# Event: LOGIN
#   Details: ('user123', 'success')
#   Metadata: {'ip': '192.168.1.1', 'duration': 0.5}
```

### Unpacking with * and **

```python
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
print(add(*numbers))  # 6 -- unpacking list into positional args

config = {"a": 10, "b": 20, "c": 30}
print(add(**config))  # 60 -- unpacking dict into keyword args
```

---

## 5. Lambda Functions

Lambda functions are small, anonymous functions defined with the `lambda` keyword.

### Syntax

```python
# lambda arguments: expression
square = lambda x: x ** 2
print(square(5))  # 25

# Multi-argument lambda
add = lambda x, y: x + y
print(add(3, 7))  # 10
```

### Common Use Cases

```python
# Sorting with a custom key
students = [("Alice", 88), ("Bob", 95), ("Charlie", 72)]
students.sort(key=lambda s: s[1], reverse=True)
print(students)  # [('Bob', 95), ('Alice', 88), ('Charlie', 72)]

# Conditional expression in lambda
classify = lambda x: "even" if x % 2 == 0 else "odd"
print(classify(7))  # odd
```

### Limitations

- Single expression only (no statements like `if/else` blocks, loops, or assignments)
- Hard to debug (no name in tracebacks)
- Less readable for complex logic -- use `def` instead

```python
# BAD -- overly complex lambda
process = lambda x: x ** 2 if x > 0 else -x if x < 0 else 0

# GOOD -- use a named function
def process(x):
    if x > 0:
        return x ** 2
    elif x < 0:
        return -x
    return 0
```

---

## 6. map(), filter(), reduce()

These built-in functions enable a **functional programming** style.

### map() -- Apply a Function to Every Item

```python
numbers = [1, 2, 3, 4, 5]

# Square every number
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# Convert strings to integers
str_nums = ["10", "20", "30"]
int_nums = list(map(int, str_nums))
print(int_nums)  # [10, 20, 30]

# Multiple iterables
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print(sums)  # [11, 22, 33]
```

### filter() -- Select Items That Match a Condition

```python
numbers = range(1, 21)

# Filter even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# Filter non-empty strings
words = ["hello", "", "world", "", "python"]
non_empty = list(filter(None, words))  # None removes falsy values
print(non_empty)  # ['hello', 'world', 'python']
```

### reduce() -- Accumulate Values into a Single Result

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum all numbers
total = reduce(lambda acc, x: acc + x, numbers)
print(total)  # 15

# Find maximum
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)  # 5

# Flatten a list of lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda acc, lst: acc + lst, nested)
print(flat)  # [1, 2, 3, 4, 5, 6]
```

### Chaining map, filter, reduce

```python
from functools import reduce

# Sum of squares of even numbers from 1 to 10
result = reduce(
    lambda acc, x: acc + x,
    map(
        lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, range(1, 11))
    )
)
print(result)  # 220 (4 + 16 + 36 + 64 + 100)
```

---

## 7. Decorators

Decorators are functions that **modify the behavior** of other functions without
changing their source code. They are a powerful application of closures and
higher-order functions.

### Basic Decorator Pattern

```python
import functools

def my_decorator(func):
    @functools.wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):
        print("Before the function call")
        result = func(*args, **kwargs)
        print("After the function call")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    """Greet someone by name."""
    print(f"Hello, {name}!")

say_hello("Alice")
# Before the function call
# Hello, Alice!
# After the function call
```

### Practical Example: Timing Decorator

```python
import time
import functools

def timer(func):
    """Measure and print the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.5)
    return "Done"

slow_function()  #   slow_function took 0.50xxs
```

### Practical Example: Logging Decorator

```python
import functools
import datetime

def log_calls(func):
    """Log every call to the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Calling {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        print(f"[{timestamp}] {func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(3, 5)
```

### Decorators with Arguments

```python
import functools

def repeat(n):
    """Decorator factory: repeat function call n times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")
    return name

greet("Alice")
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

### Chaining Decorators

```python
@timer
@log_calls
def multiply(a, b):
    return a * b

# Equivalent to: multiply = timer(log_calls(multiply))
multiply(3, 4)
```

---

## 8. Generators

Generators are functions that produce a sequence of values **lazily** using `yield`,
rather than computing all values upfront and returning them in a list.

### Why Generators?

- **Memory efficient** -- values are computed one at a time
- **Lazy evaluation** -- values are produced only when needed
- **Can represent infinite sequences**

### Basic Generator

```python
def countdown(n):
    """Count down from n to 1."""
    while n > 0:
        yield n
        n -= 1

for num in countdown(5):
    print(num, end=" ")  # 5 4 3 2 1
```

### Generator for Fibonacci Sequence

```python
def fibonacci():
    """Generate an infinite Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Get first 10 Fibonacci numbers
fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Generator Expressions

```python
# List comprehension -- creates entire list in memory
squares_list = [x ** 2 for x in range(1000000)]

# Generator expression -- computes values lazily
squares_gen = (x ** 2 for x in range(1000000))

# Memory comparison
import sys
print(f"List size: {sys.getsizeof(squares_list):,} bytes")  # ~8 MB
print(f"Generator size: {sys.getsizeof(squares_gen)} bytes")  # ~200 bytes
```

### yield from (Delegating Generators)

```python
def flatten(nested_list):
    """Flatten a nested list using yield from."""
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

data = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(data)))  # [1, 2, 3, 4, 5, 6, 7]
```

### Generator Pipeline

```python
def read_lines(data):
    """Simulate reading lines from a data source."""
    for line in data:
        yield line.strip()

def filter_comments(lines):
    """Remove comment lines."""
    for line in lines:
        if not line.startswith("#"):
            yield line

def to_uppercase(lines):
    """Convert lines to uppercase."""
    for line in lines:
        yield line.upper()

# Build a pipeline
raw_data = ["  hello  ", "# comment", "  world  ", "# another", "  python  "]
pipeline = to_uppercase(filter_comments(read_lines(raw_data)))

for line in pipeline:
    print(line)  # HELLO, WORLD, PYTHON
```

---

## 9. Recursive Functions

A recursive function calls **itself** to break a problem into smaller sub-problems.

### Two Essential Components

1. **Base Case** -- the condition that stops recursion
2. **Recursive Case** -- the function calling itself with a smaller input

### Factorial

```python
def factorial(n):
    """
    Calculate n! (n factorial).

    Base case: 0! = 1
    Recursive case: n! = n * (n-1)!
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))   # 120 (5 * 4 * 3 * 2 * 1)
print(factorial(10))  # 3628800
```

### Fibonacci (Recursive vs Memoized)

```python
# Naive recursive -- O(2^n) time
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

# Memoized -- O(n) time
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

print(fib_memo(50))  # 12586269025 -- runs instantly
```

### Binary Search (Recursive)

```python
def binary_search(arr, target, low=0, high=None):
    """
    Find target in sorted array using recursion.

    Returns index if found, -1 otherwise.
    """
    if high is None:
        high = len(arr) - 1

    if low > high:
        return -1  # Base case: not found

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid - 1)

sorted_list = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(sorted_list, 7))   # 3
print(binary_search(sorted_list, 10))  # -1
```

### Recursion Depth & Tail Recursion

```python
import sys
print(sys.getrecursionlimit())  # Default: 1000

# Increase if needed (use with caution)
# sys.setrecursionlimit(5000)
```

>  **Tip:** Python does NOT optimize tail recursion. For deep recursion, consider
> converting to an iterative approach or using `@lru_cache` for memoization.

---

## Summary

| Concept            | Key Takeaway                                      |
|--------------------|---------------------------------------------------|
| Functions          | Reusable code blocks with `def` and `return`      |
| Parameters         | Positional, keyword, default, *args, **kwargs     |
| Scope (LEGB)       | Local  Enclosing  Global  Built-in             |
| Lambda             | Anonymous single-expression functions              |
| map/filter/reduce  | Functional programming transforms on iterables    |
| Decorators         | Modify function behavior without changing code     |
| Generators         | Lazy, memory-efficient sequences with `yield`      |
| Recursion          | Self-calling functions with base + recursive case  |

---

## Practice Files

| File | Description |
|------|-------------|
| `practice/decorators_demo.py` | Timer, logging, retry, and auth decorators |
| `practice/generators_demo.py` | Fibonacci, file reader, counter, chunking |
| `practice/lambda_map_filter.py` | Lambda sorting, filtering, mapping, reduce |

## LeetCode Problems

| File | Problem |
|------|---------|
| `official_questions/01_climbing_stairs.py` | LeetCode 70 -- Climbing Stairs |
| `official_questions/02_two_sum.py` | LeetCode 1 -- Two Sum |

## Corporate Use Case

| File | Description |
|------|-------------|
| `Corporate_use_case/enterprise_validation_framework.py` | Enterprise validation using decorators, *args/**kwargs, lambda, map/filter |
