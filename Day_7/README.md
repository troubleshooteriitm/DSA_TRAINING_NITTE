# Day 7 -- Exception Handling & Debugging in Python

## Table of Contents

1. [Standard Exception Hierarchy](#1-standard-exception-hierarchy)
2. [try-except-finally](#2-try-except-finally)
3. [Catching Specific vs Generic Exceptions](#3-catching-specific-vs-generic-exceptions)
4. [Custom Exceptions](#4-custom-exceptions)
5. [Raising Exceptions](#5-raising-exceptions)
6. [Assertions](#6-assertions)
7. [Logging Module](#7-logging-module)
8. [Debugging Techniques](#8-debugging-techniques)
9. [PEP8 Compliance Tools](#9-pep8-compliance-tools)
10. [Best Practices for Exception Handling](#10-best-practices-for-exception-handling)

---

## 1. Standard Exception Hierarchy

Python has a rich hierarchy of built-in exceptions. Understanding this hierarchy is crucial for writing robust error-handling code.

### The Root: `BaseException`

`BaseException` is the root of **all** exceptions in Python. You should almost never catch it directly -- doing so would also catch `KeyboardInterrupt`, `SystemExit`, and `GeneratorExit`, which are not "errors" in the usual sense.

```
BaseException
 BaseExceptionGroup
 GeneratorExit
 KeyboardInterrupt
 SystemExit
 Exception
     ArithmeticError
        FloatingPointError
        OverflowError
        ZeroDivisionError
     AssertionError
     AttributeError
     BufferError
     EOFError
     ImportError
        ModuleNotFoundError
     LookupError
        IndexError
        KeyError
     MemoryError
     NameError
        UnboundLocalError
     OSError
        FileExistsError
        FileNotFoundError
        IsADirectoryError
        NotADirectoryError
        PermissionError
        TimeoutError
     RuntimeError
        NotImplementedError
        RecursionError
     StopIteration
     StopAsyncIteration
     SyntaxError
        IndentationError
            TabError
     TypeError
     ValueError
        UnicodeError
     Warning
         DeprecationWarning
         FutureWarning
         RuntimeWarning
         UserWarning
```

### Commonly Encountered Exceptions

| Exception             | When It Occurs                                           |
|-----------------------|----------------------------------------------------------|
| `ValueError`          | Function receives argument of correct type but wrong value |
| `TypeError`           | Operation applied to wrong type                          |
| `KeyError`            | Dictionary key not found                                 |
| `IndexError`          | Sequence index out of range                              |
| `FileNotFoundError`   | Trying to open a file that doesn't exist                 |
| `ZeroDivisionError`   | Division or modulo by zero                               |
| `AttributeError`      | Attribute reference or assignment fails                  |
| `ImportError`         | Import statement fails                                   |
| `NameError`           | Local or global name not found                           |
| `RuntimeError`        | Generic error that doesn't fit other categories          |

```python
# Quick examples of common exceptions
try:
    int("hello")          # ValueError
except ValueError as e:
    print(f"ValueError: {e}")

try:
    my_list = [1, 2, 3]
    print(my_list[10])    # IndexError
except IndexError as e:
    print(f"IndexError: {e}")

try:
    my_dict = {"a": 1}
    print(my_dict["z"])   # KeyError
except KeyError as e:
    print(f"KeyError: {e}")
```

---

## 2. try-except-finally

The `try-except-finally` block is Python's primary mechanism for exception handling.

### Basic Syntax

```python
try:
    # Code that might raise an exception
    result = 10 / 0
except ZeroDivisionError:
    # Handles the specific exception
    print("Cannot divide by zero!")
```

### Multiple `except` Blocks

You can catch different exception types with separate `except` blocks. Python checks them **top to bottom**, so always list more specific exceptions first.

```python
def parse_and_divide(text, divisor):
    """Demonstrates multiple except blocks."""
    try:
        number = int(text)
        result = number / divisor
        return result
    except ValueError:
        print(f"Cannot convert '{text}' to an integer.")
    except ZeroDivisionError:
        print("Cannot divide by zero.")
    except TypeError:
        print(f"Invalid type for divisor: {type(divisor)}")

parse_and_divide("abc", 2)   # ValueError
parse_and_divide("10", 0)    # ZeroDivisionError
parse_and_divide("10", None) # TypeError
```

### Catching Multiple Exceptions in One Block

```python
try:
    # some risky operation
    value = int("not_a_number")
except (ValueError, TypeError) as e:
    print(f"Caught an error: {type(e).__name__}: {e}")
```

### The `else` Clause

The `else` block runs **only if no exception was raised** in the `try` block. This is useful for code that should run only on success.

```python
def safe_divide(a, b):
    """Demonstrates try-except-else."""
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Division by zero!")
        return None
    else:
        # Runs only if no exception occurred
        print(f"Division successful: {a} / {b} = {result}")
        return result

safe_divide(10, 2)   # else block executes
safe_divide(10, 0)   # except block executes
```

### The `finally` Clause

The `finally` block **always runs**, whether an exception occurred or not. It is ideal for cleanup operations (closing files, releasing locks, etc.).

```python
def read_file_safely(filepath):
    """Demonstrates try-except-finally for resource cleanup."""
    file = None
    try:
        file = open(filepath, 'r')
        content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
        return None
    except PermissionError:
        print(f"Permission denied for '{filepath}'.")
        return None
    finally:
        # Always runs -- ensures the file handle is closed
        if file is not None:
            file.close()
            print("File handle closed.")
```

### Complete try-except-else-finally

```python
def complete_example(filename):
    """Shows all four clauses together."""
    try:
        f = open(filename, 'r')
        data = f.read()
    except FileNotFoundError:
        print("File not found!")
    else:
        print(f"Read {len(data)} characters successfully.")
    finally:
        print("Execution complete -- cleanup done.")
```

**Execution order:** `try`  `except` (if error) OR `else` (if no error)  `finally` (always).

---

## 3. Catching Specific vs Generic Exceptions

### Why Specificity Matters

```python
#  BAD -- catches EVERYTHING, including bugs you'd want to see
try:
    result = process_data(data)
except Exception:
    pass  # Silently swallows all errors -- very dangerous!

#  GOOD -- catches only the expected failure mode
try:
    result = process_data(data)
except ValueError as e:
    print(f"Invalid data: {e}")
except FileNotFoundError as e:
    print(f"Data file missing: {e}")
```

### The `as` Keyword

Always use `as` to capture the exception object for logging or re-raising:

```python
try:
    config = load_config("settings.yaml")
except FileNotFoundError as e:
    print(f"Config file missing: {e}")
    config = load_defaults()
```

### Re-raising Exceptions

Use bare `raise` to re-raise the current exception after logging or partial handling:

```python
try:
    connect_to_database()
except ConnectionError as e:
    log_error(f"Database connection failed: {e}")
    raise  # Re-raises the same exception with original traceback
```

---

## 4. Custom Exceptions

Custom exceptions let you define domain-specific error types that make your code more readable and your error handling more precise.

### Creating a Basic Custom Exception

```python
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the account balance."""

    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.deficit = amount - balance
        super().__init__(
            f"Cannot withdraw ₹{amount}. "
            f"Balance: ₹{balance}, Deficit: ₹{self.deficit}"
        )
```

### Building an Exception Hierarchy

```python
class ApplicationError(Exception):
    """Base exception for the application."""
    pass


class DatabaseError(ApplicationError):
    """Raised for database-related errors."""
    pass


class ConnectionError(DatabaseError):
    """Raised when database connection fails."""
    pass


class QueryError(DatabaseError):
    """Raised when a database query fails."""
    pass


class ValidationError(ApplicationError):
    """Raised when input validation fails."""
    pass
```

### Using Custom Exceptions

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance


# Usage
account = BankAccount("Alice", 1000)
try:
    account.withdraw(1500)
except InsufficientFundsError as e:
    print(f"Transaction failed: {e}")
    print(f"You need ₹{e.deficit} more.")
```

---

## 5. Raising Exceptions

The `raise` statement lets you explicitly trigger an exception.

### Basic `raise`

```python
def set_age(age):
    """Sets age with validation."""
    if not isinstance(age, int):
        raise TypeError(f"Age must be an integer, got {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValueError(f"Age must be between 0 and 150, got {age}")
    return age
```

### Chaining Exceptions with `from`

Use `raise ... from ...` to chain exceptions, preserving the original cause:

```python
def load_user_config(user_id):
    """Demonstrates exception chaining."""
    try:
        with open(f"config_{user_id}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigurationError(
            f"Config for user {user_id} not found"
        ) from e
    except json.JSONDecodeError as e:
        raise ConfigurationError(
            f"Invalid config format for user {user_id}"
        ) from e
```

### Suppressing Exception Context

Use `from None` to suppress the original exception context:

```python
try:
    value = int("not_a_number")
except ValueError:
    raise RuntimeError("Failed to parse input") from None
```

---

## 6. Assertions

Assertions are a debugging aid that tests a condition. If the condition is `False`, an `AssertionError` is raised.

### Syntax

```python
assert condition, "Optional error message"

# Example
def calculate_average(numbers):
    assert len(numbers) > 0, "Cannot calculate average of empty list"
    return sum(numbers) / len(numbers)
```

### When to Use Assertions

| Use Assertions For                        | Do NOT Use Assertions For          |
|-------------------------------------------|------------------------------------|
| Internal invariants                       | User input validation              |
| Preconditions in private methods          | Security checks                    |
| Postconditions (verifying results)        | Data from external sources         |
| Debugging during development              | Production error handling          |

> ** Important:** Assertions can be disabled globally with `python -O` (optimize flag). Never use them for critical validation!

```python
#  Good use -- internal sanity check
def _merge_sorted_lists(list_a, list_b):
    assert all(list_a[i] <= list_a[i+1] for i in range(len(list_a)-1)), \
        "list_a must be sorted"
    # ... merge logic ...

#  Bad use -- user input (can be bypassed with -O flag)
def transfer_money(amount):
    assert amount > 0  # NEVER do this for real validation!
```

---

## 7. Logging Module

Python's built-in `logging` module is far superior to `print()` for production code.

### Logging Levels

| Level      | Numeric Value | Purpose                                      |
|------------|---------------|----------------------------------------------|
| `DEBUG`    | 10            | Detailed diagnostic information              |
| `INFO`     | 20            | Confirmation that things work as expected    |
| `WARNING`  | 30            | Something unexpected, but program continues  |
| `ERROR`    | 40            | Serious problem, some function failed        |
| `CRITICAL` | 50            | Program may not be able to continue          |

### Basic Configuration

```python
import logging

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

logger.debug("This is a debug message")
logger.info("Application started successfully")
logger.warning("Disk space running low")
logger.error("Failed to connect to database")
logger.critical("System is shutting down!")
```

### Logging to a File

```python
import logging

logging.basicConfig(
    filename='app.log',
    filemode='a',            # 'a' = append, 'w' = overwrite
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("This message goes to the file.")
```

### Formatters

Format strings support many attributes:

| Attribute       | Format            | Description                          |
|-----------------|-------------------|--------------------------------------|
| `asctime`       | `%(asctime)s`     | Human-readable time                  |
| `levelname`     | `%(levelname)s`   | Logging level (DEBUG, INFO, etc.)    |
| `name`          | `%(name)s`        | Logger name                          |
| `message`       | `%(message)s`     | The log message                      |
| `filename`      | `%(filename)s`    | Source file name                     |
| `lineno`        | `%(lineno)d`      | Line number in source                |
| `funcName`      | `%(funcName)s`    | Function name                        |

```python
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

### Handlers

Handlers send log records to different destinations:

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# Console handler -- shows WARNING and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# File handler -- logs everything
file_handler = logging.FileHandler("debug.log")
file_handler.setLevel(logging.DEBUG)

# Rotating file handler -- prevents huge log files
rotating_handler = RotatingFileHandler(
    "app.log",
    maxBytes=5_000_000,    # 5 MB per file
    backupCount=3          # Keep 3 backup files
)

# Apply formatters
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
rotating_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(rotating_handler)

logger.debug("Debug message -- goes to file only")
logger.warning("Warning -- goes to console AND file")
```

### Logging Exceptions

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("An error occurred during division")
    # logger.exception() automatically includes the traceback!
```

---

## 8. Debugging Techniques

### Print Debugging

The simplest (but least efficient) debugging technique:

```python
def buggy_function(data):
    print(f"[DEBUG] Input data: {data}")             # Check input
    processed = [x * 2 for x in data]
    print(f"[DEBUG] After processing: {processed}")  # Check intermediate state
    result = sum(processed)
    print(f"[DEBUG] Final result: {result}")          # Check output
    return result
```

> **Tip:** Use f-strings with descriptive labels. Remove or convert to `logging` before production.

### Using `pdb` -- The Python Debugger

`pdb` is Python's built-in interactive debugger.

```python
import pdb

def complex_calculation(x, y):
    result = x + y
    pdb.set_trace()  # Execution pauses here -- you get an interactive prompt
    result = result * 2
    return result
```

#### Essential `pdb` Commands

| Command     | Short | Description                                  |
|-------------|-------|----------------------------------------------|
| `next`      | `n`   | Execute next line (step over)                |
| `step`      | `s`   | Step into a function call                    |
| `continue`  | `c`   | Continue until next breakpoint               |
| `print`     | `p`   | Print value of an expression                 |
| `list`      | `l`   | Show source code around current line         |
| `break`     | `b`   | Set a breakpoint                             |
| `where`     | `w`   | Show the call stack                          |
| `quit`      | `q`   | Quit the debugger                            |
| `up`        | `u`   | Move up one frame in the call stack          |
| `down`      | `d`   | Move down one frame in the call stack        |

### Using `breakpoint()` (Python 3.7+)

`breakpoint()` is the modern, recommended way to enter the debugger:

```python
def process_order(order):
    total = sum(item['price'] * item['qty'] for item in order)
    breakpoint()  # Drops into pdb by default
    tax = total * 0.18
    return total + tax
```

**Advantages of `breakpoint()` over `pdb.set_trace()`:**
- Can be disabled via `PYTHONBREAKPOINT=0` environment variable
- Can switch debuggers via `PYTHONBREAKPOINT=ipdb.set_trace`
- Cleaner and more Pythonic

### Post-Mortem Debugging

Debug an exception **after** it has occurred:

```python
import pdb

try:
    result = broken_function()
except Exception:
    pdb.post_mortem()  # Opens debugger at the point of failure
```

---

## 9. PEP8 Compliance Tools

PEP8 is Python's official style guide. These tools help enforce it:

### `flake8` -- Linter

Checks code for PEP8 violations and common errors.

```bash
# Install
pip install flake8

# Run on a file
flake8 my_script.py

# Run with specific settings
flake8 --max-line-length=120 --ignore=E501 my_script.py

# Run on a directory
flake8 src/
```

### `pylint` -- Advanced Linter

More comprehensive than flake8 -- checks style, errors, refactoring suggestions, and code smells.

```bash
# Install
pip install pylint

# Run on a file
pylint my_script.py

# Generate a config file
pylint --generate-rcfile > .pylintrc
```

### `black` -- Auto-Formatter

Automatically reformats code to be PEP8 compliant. Opinionated -- no configuration needed.

```bash
# Install
pip install black

# Format a file
black my_script.py

# Check without modifying (dry run)
black --check my_script.py

# Format with specific line length
black --line-length 120 my_script.py
```

### Comparison

| Tool     | Type          | Auto-fixes? | Configurability |
|----------|---------------|-------------|-----------------|
| `flake8` | Linter        | No          | High            |
| `pylint` | Linter        | No          | Very High       |
| `black`  | Formatter     | Yes         | Minimal         |

> **Recommended workflow:** Use `black` to auto-format, then `flake8` or `pylint` to catch remaining issues.

---

## 10. Best Practices for Exception Handling

### 1. Be Specific with Exceptions

```python
#  Bad
try:
    do_something()
except Exception:
    pass

#  Good
try:
    do_something()
except SpecificError as e:
    handle_error(e)
```

### 2. Don't Use Exceptions for Flow Control

```python
#  Bad -- using exceptions as control flow
try:
    value = my_dict[key]
except KeyError:
    value = default

#  Good -- LBYL (Look Before You Leap) or EAFP with intent
value = my_dict.get(key, default)
```

### 3. Always Clean Up Resources

```python
#  Best -- use context managers
with open("data.txt", "r") as f:
    data = f.read()
# File is automatically closed, even if an exception occurs
```

### 4. Log Before Re-raising

```python
try:
    process_payment(order)
except PaymentError as e:
    logger.error(f"Payment failed for order {order.id}: {e}")
    raise
```

### 5. Use Custom Exceptions for Business Logic

```python
# Define domain-specific exceptions
class OrderError(Exception): pass
class OutOfStockError(OrderError): pass
class PaymentDeclinedError(OrderError): pass

# Handle them specifically
try:
    place_order(cart)
except OutOfStockError as e:
    notify_user_restock(e.product)
except PaymentDeclinedError:
    prompt_alternative_payment()
```

### 6. Don't Catch `BaseException`

```python
#  Dangerous -- catches KeyboardInterrupt, SystemExit
try:
    main()
except BaseException:
    pass

#  Safe
try:
    main()
except Exception as e:
    logger.exception("Unexpected error")
```

### 7. Keep `try` Blocks Small

```python
#  Bad -- too much code in try block
try:
    data = load_data()
    processed = transform(data)
    result = compute(processed)
    save(result)
except Exception:
    print("Something went wrong")

#  Good -- only the risky operation in try
try:
    data = load_data()
except FileNotFoundError:
    data = get_defaults()

processed = transform(data)
result = compute(processed)
save(result)
```

### 8. Use `logging.exception()` in Except Blocks

```python
try:
    risky_operation()
except SomeError:
    # Automatically includes the full traceback
    logger.exception("Operation failed")
```

---

## Practice Files

| File | Description |
|------|-------------|
| `practice/custom_exceptions.py` | Creating and using custom exception hierarchies |
| `practice/logging_demo.py` | Logging basics, file logging, formatters, rotating handlers |

## LeetCode Problems

| File | Problem | Key Concept |
|------|---------|-------------|
| `official_questions/01_missing_number.py` | LeetCode 268 -- Missing Number | Sum formula, XOR, Sorting |
| `official_questions/02_single_number.py` | LeetCode 136 -- Single Number | XOR bit manipulation |

## Corporate Use Case

| File | Description |
|------|-------------|
| `Corporate_use_case/payroll_recovery_system.py` | Payroll failure recovery with retry logic, custom exceptions, and logging |

---

> **Next:** Day 8 -- continue building on these foundations with more advanced topics!
