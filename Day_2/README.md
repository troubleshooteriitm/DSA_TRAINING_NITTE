#  Day 2: Python Fundamentals -- Variables, Data Types, Operators & Strings

> **DSA Training -- Day 2**
> Master the building blocks of Python before diving into data structures and algorithms.

---

## Table of Contents

1. [Variables](#1-variables)
2. [Keywords](#2-keywords)
3. [Built-in Functions](#3-built-in-functions)
4. [Data Types](#4-data-types)
5. [Numeric Literals](#5-numeric-literals)
6. [Strings](#6-strings)
7. [Operators](#7-operators)
8. [Expressions & Operator Precedence](#8-expressions--operator-precedence)
9. [Type Conversion](#9-type-conversion)
10. [Input / Output](#10-input--output)
11. [String Manipulation](#11-string-manipulation)

---

## 1. Variables

A **variable** is a name that refers to a value stored in memory. Python variables are created the moment you assign a value -- no explicit declaration is needed.

### 1.1 Naming Rules

| Rule | Valid | Invalid |
|------|-------|---------|
| Must start with a letter or `_` | `name`, `_count` | `2name` |
| Can contain letters, digits, `_` | `my_var2` | `my-var` |
| Case-sensitive | `Age`  `age` | -- |
| Cannot be a Python keyword | `total` | `class` |

```python
# Valid variable names
first_name = "Alice"
_age = 25
student1 = "Bob"
MAX_SIZE = 100        # Convention: UPPER_CASE for constants

# Invalid variable names (uncomment to see errors)
# 2name = "error"     # SyntaxError: starts with a digit
# my-var = 10         # SyntaxError: hyphen not allowed
# class = "keyword"   # SyntaxError: 'class' is a keyword
```

### 1.2 Dynamic Typing

Python is **dynamically typed** -- a variable's type is determined at runtime and can change.

```python
x = 10          # x is an int
print(type(x))  # <class 'int'>

x = "hello"     # x is now a str -- no error!
print(type(x))  # <class 'str'>

x = [1, 2, 3]   # x is now a list
print(type(x))  # <class 'list'>
```

### 1.3 Multiple Assignment

```python
# Assign the same value to multiple variables
a = b = c = 0
print(a, b, c)  # 0 0 0

# Assign different values in one line (tuple unpacking)
x, y, z = 1, 2.5, "three"
print(x)  # 1
print(y)  # 2.5
print(z)  # three

# Unpack from a list
first, second, third = [10, 20, 30]
print(first, second, third)  # 10 20 30

# Star unpacking (Python 3)
head, *tail = [1, 2, 3, 4, 5]
print(head)  # 1
print(tail)  # [2, 3, 4, 5]
```

### 1.4 Variable Swapping

```python
# Traditional swap (using a temp variable)
a, b = 5, 10
temp = a
a = b
b = temp
print(a, b)  # 10 5

# Pythonic swap -- no temp variable needed!
a, b = 5, 10
a, b = b, a
print(a, b)  # 10 5
```

---

## 2. Keywords

Keywords are **reserved words** that have special meaning in Python. You cannot use them as variable names.

### 2.1 How to List All Keywords

```python
import keyword

print(keyword.kwlist)
print(f"Total keywords: {len(keyword.kwlist)}")  # 35 in Python 3.12+
```

### 2.2 Complete Keyword Reference

| Keyword | Description |
|---------|-------------|
| `False` | Boolean false value |
| `True` | Boolean true value |
| `None` | Represents the absence of a value (null) |
| `and` | Logical AND operator |
| `as` | Create an alias (e.g., `import numpy as np`) |
| `assert` | Debugging aid -- test if a condition is true |
| `async` | Declare an asynchronous function |
| `await` | Wait for an async operation to complete |
| `break` | Exit the nearest enclosing loop |
| `class` | Define a new class |
| `continue` | Skip the rest of the current loop iteration |
| `def` | Define a function |
| `del` | Delete a variable, item, or attribute |
| `elif` | Else-if -- additional condition in an if chain |
| `else` | Executes if the preceding conditions are false |
| `except` | Handle an exception in a try block |
| `finally` | Executes code after try/except, regardless of outcome |
| `for` | Create a for loop |
| `from` | Import a specific part of a module |
| `global` | Declare a global variable inside a function |
| `if` | Conditional statement |
| `import` | Import a module |
| `in` | Membership test / iteration keyword |
| `is` | Identity test (checks if two variables refer to the same object) |
| `lambda` | Create a small anonymous function |
| `nonlocal` | Declare a variable from an enclosing scope |
| `not` | Logical NOT operator |
| `or` | Logical OR operator |
| `pass` | Null statement -- does nothing (placeholder) |
| `raise` | Raise an exception |
| `return` | Return a value from a function |
| `try` | Start a try/except block for error handling |
| `while` | Create a while loop |
| `with` | Simplify resource management (context manager) |
| `yield` | Return a generator value from a function |

```python
# Examples of keyword usage
import keyword

# Check if a word is a keyword
print(keyword.iskeyword("for"))      # True
print(keyword.iskeyword("hello"))    # False

# You can't use keywords as variable names
# for = 10        # SyntaxError
# class = "math"  # SyntaxError
```

---

## 3. Built-in Functions

Python provides many **built-in functions** available without any import. Here are the most commonly used ones.

### 3.1 Output & Type Inspection

```python
# print() -- output to console
print("Hello, World!")
print(1, 2, 3, sep="-")        # 1-2-3
print("no newline", end=" ")    # no trailing newline

# type() -- get the type of an object
print(type(42))         # <class 'int'>
print(type("hello"))    # <class 'str'>
print(type([1, 2]))     # <class 'list'>

# id() -- get the unique identity (memory address) of an object
x = 42
print(id(x))  # e.g., 140234866357520

# isinstance() -- check if an object is an instance of a type
print(isinstance(42, int))        # True
print(isinstance("hi", str))      # True
print(isinstance(3.14, (int, float)))  # True (tuple of types)
```

### 3.2 Length & Collection Info

```python
# len() -- get the length of a sequence
print(len("hello"))      # 5
print(len([1, 2, 3]))    # 3
print(len({"a": 1}))     # 1

# min(), max(), sum()
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(min(numbers))  # 1
print(max(numbers))  # 9
print(sum(numbers))  # 31

# min/max with key
words = ["banana", "apple", "cherry"]
print(min(words, key=len))  # apple
print(max(words, key=len))  # cherry
```

### 3.3 Math Functions

```python
# abs() -- absolute value
print(abs(-7))      # 7
print(abs(-3.14))   # 3.14

# round() -- round a number
print(round(3.14159))       # 3
print(round(3.14159, 2))    # 3.14
print(round(2.5))           # 2 (banker's rounding)
print(round(3.5))           # 4

# pow() -- exponentiation
print(pow(2, 10))       # 1024
print(pow(2, 10, 1000)) # 24  (2^10 % 1000 -- modular exponentiation)

# divmod() -- quotient and remainder
print(divmod(17, 5))  # (3, 2)  17 = 5*3 + 2
```

### 3.4 Iterators & Ranges

```python
# range() -- generate a sequence of numbers
print(list(range(5)))         # [0, 1, 2, 3, 4]
print(list(range(2, 8)))      # [2, 3, 4, 5, 6, 7]
print(list(range(0, 10, 2)))  # [0, 2, 4, 6, 8]
print(list(range(10, 0, -1))) # [10, 9, 8, ..., 1]

# enumerate() -- loop with index
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip() -- combine multiple iterables
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
# Alice: 85
# Bob: 92
# Charlie: 78

# zip with unequal lengths -- stops at shortest
print(list(zip([1, 2, 3], ['a', 'b'])))  # [(1, 'a'), (2, 'b')]
```

### 3.5 Functional Programming

```python
# map() -- apply a function to every element
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# filter() -- keep elements that satisfy a condition
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# sorted() -- return a new sorted list
data = [3, 1, 4, 1, 5, 9]
print(sorted(data))              # [1, 1, 3, 4, 5, 9]
print(sorted(data, reverse=True))  # [9, 5, 4, 3, 1, 1]

# Sort by custom key
words = ["banana", "apple", "cherry", "date"]
print(sorted(words, key=len))  # ['date', 'apple', 'banana', 'cherry']

# reversed() -- reverse an iterable
print(list(reversed([1, 2, 3])))       # [3, 2, 1]
print(list(reversed("hello")))         # ['o', 'l', 'l', 'e', 'h']
print("".join(reversed("hello")))      # olleh
```

### 3.6 Input & File Operations

```python
# input() -- read user input (always returns a string)
name = input("Enter your name: ")
age = int(input("Enter your age: "))  # cast to int

# open() -- open a file
# Reading a file
with open("example.txt", "r") as f:
    content = f.read()

# Writing to a file
with open("output.txt", "w") as f:
    f.write("Hello, file!\n")
```

### 3.7 Other Useful Built-ins

```python
# any() and all()
print(any([False, False, True]))   # True (at least one True)
print(all([True, True, True]))     # True (all True)
print(all([True, False, True]))    # False

# chr() and ord() -- character/Unicode conversions
print(chr(65))    # 'A'
print(chr(97))    # 'a'
print(ord('A'))   # 65
print(ord('Z'))   # 90

# bin(), oct(), hex() -- number base conversions
print(bin(10))   # '0b1010'
print(oct(10))   # '0o12'
print(hex(255))  # '0xff'

# hash() -- get hash value
print(hash("hello"))  # deterministic integer
print(hash(42))       # 42

# dir() -- list attributes
print(dir(str))  # all string methods
```

---

## 4. Data Types

Python has several **built-in data types**. Everything in Python is an object.

### 4.1 `int` -- Integer

```python
x = 42
y = -7
big = 999_999_999_999  # underscores for readability

print(type(x))   # <class 'int'>
print(x + y)     # 35

# Python integers have unlimited precision!
huge = 10 ** 100
print(huge)  # prints a 101-digit number
```

### 4.2 `float` -- Floating Point

```python
pi = 3.14159
negative = -0.001
scientific = 2.5e10   # 25000000000.0

print(type(pi))       # <class 'float'>
print(0.1 + 0.2)      # 0.30000000000000004 (floating-point precision!)
print(round(0.1 + 0.2, 1))  # 0.3

# Special float values
print(float('inf'))    # inf
print(float('-inf'))   # -inf
print(float('nan'))    # nan
```

### 4.3 `complex` -- Complex Numbers

```python
z = 3 + 4j
print(type(z))     # <class 'complex'>
print(z.real)      # 3.0
print(z.imag)      # 4.0
print(abs(z))      # 5.0 (magnitude: sqrt(3² + 4²))

z2 = complex(1, 2)  # 1 + 2j
print(z + z2)       # (4+6j)
print(z * z2)       # (-5+10j)
```

### 4.4 `str` -- String

```python
s1 = 'single quotes'
s2 = "double quotes"
s3 = '''triple quotes
can span multiple lines'''
s4 = """also triple quotes"""

print(type(s1))  # <class 'str'>
print(len(s2))   # 13

# Strings are immutable
# s1[0] = 'S'    # TypeError: 'str' object does not support item assignment
```

### 4.5 `bool` -- Boolean

```python
a = True
b = False

print(type(a))    # <class 'bool'>
print(a + b)      # 1 (True=1, False=0)
print(a * 10)     # 10

# Truthy and Falsy values
print(bool(0))       # False
print(bool(""))      # False
print(bool([]))      # False
print(bool(None))    # False
print(bool(1))       # True
print(bool("hello")) # True
print(bool([1, 2]))  # True
```

### 4.6 `None` -- NoneType

```python
x = None
print(type(x))     # <class 'NoneType'>
print(x is None)   # True (use 'is', not '==')

# Common use: default function argument
def greet(name=None):
    if name is None:
        print("Hello, stranger!")
    else:
        print(f"Hello, {name}!")

greet()          # Hello, stranger!
greet("Alice")   # Hello, Alice!
```

### 4.7 Quick Type Summary

| Type | Example | Mutable? |
|------|---------|----------|
| `int` | `42` | No |
| `float` | `3.14` | No |
| `complex` | `3+4j` | No |
| `str` | `"hello"` | No |
| `bool` | `True` | No |
| `NoneType` | `None` | No |
| `list` | `[1, 2, 3]` | Yes |
| `tuple` | `(1, 2, 3)` | No |
| `dict` | `{"a": 1}` | Yes |
| `set` | `{1, 2, 3}` | Yes |
| `frozenset` | `frozenset({1, 2})` | No |

---

## 5. Numeric Literals

### 5.1 Integer Literals

```python
# Decimal (base 10) -- default
decimal = 255

# Binary (base 2) -- prefix 0b or 0B
binary = 0b11111111   # 255
print(binary)          # 255
print(bin(255))        # '0b11111111'

# Octal (base 8) -- prefix 0o or 0O
octal = 0o377          # 255
print(octal)           # 255
print(oct(255))        # '0o377'

# Hexadecimal (base 16) -- prefix 0x or 0X
hexadecimal = 0xFF     # 255
print(hexadecimal)     # 255
print(hex(255))        # '0xff'

# Underscores for readability (Python 3.6+)
million = 1_000_000
phone = 0xDEAD_BEEF
binary_byte = 0b1010_1010
```

### 5.2 Float Literals

```python
# Standard
f1 = 3.14
f2 = .5       # 0.5
f3 = 10.      # 10.0

# Scientific notation
f4 = 1.5e3    # 1500.0
f5 = 2.5e-4   # 0.00025
f6 = 1E10     # 10000000000.0
```

### 5.3 Complex Literals

```python
c1 = 3 + 4j
c2 = 2j         # pure imaginary
c3 = 0j          # zero complex
c4 = complex(3, 4)  # equivalent to 3+4j
```

---

## 6. Strings

### 6.1 Creating Strings

```python
# Single quotes
s1 = 'Hello, World!'

# Double quotes
s2 = "Hello, World!"

# Triple quotes (multi-line)
s3 = '''This is
a multi-line
string.'''

s4 = """Another
multi-line string."""

# Single vs double -- use the other to include quotes
s5 = "It's a beautiful day"
s6 = 'She said "hello"'
s7 = "She said \"hello\""  # or use escape
```

### 6.2 String Indexing

```python
s = "Python"
#    P  y  t  h  o  n
#    0  1  2  3  4  5     positive index
#   -6 -5 -4 -3 -2 -1    negative index

print(s[0])    # P
print(s[5])    # n
print(s[-1])   # n  (last character)
print(s[-2])   # o  (second from last)
```

### 6.3 String Slicing

```python
s = "Hello, World!"

# s[start:end]  -- from start up to (not including) end
print(s[0:5])    # Hello
print(s[7:12])   # World

# s[start:end:step]
print(s[::2])    # Hlo ol!   (every 2nd character)
print(s[::-1])   # !dlroW ,olleH  (reverse string)

# Omit start or end
print(s[:5])     # Hello      (from beginning)
print(s[7:])     # World!     (to end)
print(s[:])      # Hello, World!  (full copy)

# More slicing examples
s = "0123456789"
print(s[2:8:2])  # 246
print(s[8:2:-1]) # 876543
```

### 6.4 Escape Characters

| Escape | Meaning |
|--------|---------|
| `\\` | Backslash |
| `\'` | Single quote |
| `\"` | Double quote |
| `\n` | Newline |
| `\t` | Tab |
| `\r` | Carriage return |
| `\b` | Backspace |
| `\0` | Null character |
| `\uXXXX` | Unicode (16-bit) |
| `\UXXXXXXXX` | Unicode (32-bit) |

```python
print("Hello\tWorld")     # Hello	World
print("Line1\nLine2")     # Two lines
print("Path: C:\\Users")  # Path: C:\Users
print("She said \"hi\"")  # She said "hi"
print("\u03C0 = pi")      #  = pi
```

### 6.5 Raw Strings

```python
# Raw strings treat backslashes as literal characters
path = r"C:\Users\new_folder\test"
print(path)  # C:\Users\new_folder\test

regex = r"\d+\.\d+"
print(regex)  # \d+\.\d+
```

### 6.6 Common String Methods

```python
s = "  Hello, World!  "

# Case methods
print(s.upper())         # "  HELLO, WORLD!  "
print(s.lower())         # "  hello, world!  "
print(s.title())         # "  Hello, World!  "
print(s.capitalize())    # "  hello, world!  "
print(s.swapcase())      # "  hELLO, wORLD!  "

# Whitespace
print(s.strip())         # "Hello, World!"
print(s.lstrip())        # "Hello, World!  "
print(s.rstrip())        # "  Hello, World!"

# Splitting and joining
csv = "apple,banana,cherry"
print(csv.split(","))           # ['apple', 'banana', 'cherry']
print("Hello World".split())    # ['Hello', 'World']

words = ['Hello', 'World']
print(" ".join(words))          # "Hello World"
print("-".join(words))          # "Hello-World"

# Replacing
s = "Hello, World!"
print(s.replace("World", "Python"))  # "Hello, Python!"
print(s.replace("l", "L", 1))       # "HeLlo, World!" (replace first only)

# Finding and counting
s = "Hello, World! Hello, Python!"
print(s.find("Hello"))      # 0  (first occurrence index)
print(s.find("Java"))       # -1 (not found)
print(s.rfind("Hello"))     # 14 (last occurrence index)
print(s.index("World"))     # 7  (like find, but raises ValueError if not found)
print(s.count("Hello"))     # 2
print(s.count("l"))         # 4

# Checking content
print("hello123".isalnum())    # True
print("hello".isalpha())      # True
print("12345".isdigit())      # True
print("hello".islower())      # True
print("HELLO".isupper())      # True
print("  \t\n".isspace())     # True

# startswith / endswith
print("Hello".startswith("He"))     # True
print("Hello".endswith("lo"))       # True
print("test.py".endswith((".py", ".txt")))  # True (tuple of suffixes)

# center, ljust, rjust, zfill
print("Hello".center(20, "-"))    # -------Hello--------
print("Hello".ljust(20, "."))     # Hello...............
print("Hello".rjust(20, "."))     # ...............Hello
print("42".zfill(5))              # 00042
```

### 6.7 F-Strings (Python 3.6+)

```python
name = "Alice"
age = 30

# Basic f-string
print(f"My name is {name} and I am {age} years old.")

# Expressions inside f-strings
print(f"2 + 3 = {2 + 3}")             # 2 + 3 = 5
print(f"Name uppercased: {name.upper()}")  # ALICE

# Formatting numbers
pi = 3.14159265
print(f"Pi: {pi:.2f}")        # Pi: 3.14
print(f"Pi: {pi:.4f}")        # Pi: 3.1416

# Padding and alignment
print(f"{'left':<20}")        # left                 (left-aligned)
print(f"{'center':^20}")      #       center         (centered)
print(f"{'right':>20}")       #                right  (right-aligned)

# Number formatting
big = 1000000
print(f"{big:,}")              # 1,000,000
print(f"{big:_}")              # 1_000_000
print(f"{0.75:.1%}")           # 75.0%
print(f"{255:#x}")             # 0xff
print(f"{255:#b}")             # 0b11111111
print(f"{42:#010x}")           # 0x0000002a

# Debugging (Python 3.8+)
x = 42
print(f"{x = }")               # x = 42
print(f"{x * 2 = }")           # x * 2 = 84
```

### 6.8 `format()` Method

```python
# Positional arguments
print("{} is {} years old".format("Alice", 30))

# Indexed arguments
print("{0} likes {1}, but {1} doesn't like {0}".format("Alice", "Bob"))

# Named arguments
print("{name} scored {score}%".format(name="Alice", score=95))

# Number formatting
print("{:.2f}".format(3.14159))    # 3.14
print("{:,}".format(1000000))      # 1,000,000
print("{:>10}".format("hello"))    #      hello
print("{:0>5}".format(42))         # 00042
```

---

## 7. Operators

### 7.1 Arithmetic Operators

```python
a, b = 17, 5

print(a + b)    # 22   Addition
print(a - b)    # 12   Subtraction
print(a * b)    # 85   Multiplication
print(a / b)    # 3.4  Division (float)
print(a // b)   # 3    Floor division (integer)
print(a % b)    # 2    Modulus (remainder)
print(a ** b)   # 1419857  Exponentiation (17^5)

# Floor division with negatives
print(-17 // 5)   # -4 (rounds toward negative infinity)
print(17 // -5)   # -4
```

### 7.2 Comparison Operators

```python
a, b = 10, 20

print(a == b)   # False   Equal
print(a != b)   # True    Not equal
print(a < b)    # True    Less than
print(a > b)    # False   Greater than
print(a <= b)   # True    Less than or equal
print(a >= b)   # False   Greater than or equal

# Chained comparisons (Pythonic!)
x = 15
print(10 < x < 20)     # True
print(1 <= x <= 100)   # True
```

### 7.3 Logical Operators

```python
a, b = True, False

print(a and b)   # False (both must be True)
print(a or b)    # True  (at least one True)
print(not a)     # False (negation)

# Short-circuit evaluation
print(False and print("won't print"))   # False
print(True or print("won't print"))     # True

# Logical operators with non-boolean values
print(0 or "default")       # "default" (0 is falsy)
print("hello" and "world")  # "world" (both truthy, returns last)
print("" or "fallback")     # "fallback" (empty string is falsy)
print(None or 42)           # 42
```

### 7.4 Bitwise Operators

```python
a, b = 0b1010, 0b1100   # a=10, b=12

print(bin(a & b))    # 0b1000   AND (8)
print(bin(a | b))    # 0b1110   OR (14)
print(bin(a ^ b))    # 0b0110   XOR (6)
print(bin(~a))       # -0b1011  NOT (bitwise complement: -11)
print(bin(a << 2))   # 0b101000 Left shift (40)
print(bin(a >> 1))   # 0b101    Right shift (5)

# Practical uses of bitwise operators
# Check if a number is even/odd
n = 7
print(n & 1)  # 1  odd
n = 8
print(n & 1)  # 0  even

# Swap two numbers without temp
a, b = 5, 3
a ^= b; b ^= a; a ^= b
print(a, b)  # 3 5

# Multiply/divide by powers of 2
print(5 << 1)   # 10  (5 * 2)
print(5 << 3)   # 40  (5 * 8)
print(20 >> 1)  # 10  (20 / 2)
```

### 7.5 Assignment Operators

```python
x = 10

x += 5     # x = x + 5   15
x -= 3     # x = x - 3   12
x *= 2     # x = x * 2   24
x /= 4     # x = x / 4   6.0
x //= 2    # x = x // 2  3.0
x %= 2     # x = x % 2   1.0
x **= 3    # x = x ** 3  1.0

# Bitwise assignment operators
y = 0b1010
y &= 0b1100   # y = y & 0b1100   0b1000
y |= 0b0011   # y = y | 0b0011   0b1011
y ^= 0b1111   # y = y ^ 0b1111   0b0100
y <<= 1       # y = y << 1       0b1000
y >>= 2       # y = y >> 2       0b0010
```

### 7.6 Identity Operators

```python
# 'is' checks if two variables point to the SAME OBJECT (same memory)
# '==' checks if two variables have the SAME VALUE

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)      # True  (same value)
print(a is b)      # False (different objects)
print(a is c)      # True  (same object)
print(a is not b)  # True

# Common use: checking for None
x = None
print(x is None)      # True  (preferred)
print(x == None)      # True  (works but not recommended)

# Small integer caching (-5 to 256)
x = 256
y = 256
print(x is y)   # True (cached)

x = 257
y = 257
print(x is y)   # May be False (not cached -- implementation dependent)
```

### 7.7 Membership Operators

```python
# 'in' checks if a value exists in a sequence

# Lists
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits)      # True
print("grape" not in fruits)   # True

# Strings
print("hell" in "hello")      # True
print("xyz" not in "hello")   # True

# Dictionaries (checks keys)
student = {"name": "Alice", "age": 25}
print("name" in student)      # True
print("grade" not in student)  # True
print(25 in student)           # False (checks keys, not values)
print(25 in student.values())  # True

# Sets (very efficient -- O(1) lookup)
primes = {2, 3, 5, 7, 11}
print(5 in primes)     # True
print(4 in primes)     # False
```

---

## 8. Expressions & Operator Precedence

### 8.1 Arithmetic Expressions

An expression is a combination of values, variables, and operators that evaluates to a result.

```python
# Simple expressions
result = 2 + 3 * 4        # 14 (not 20! -- * before +)
result = (2 + 3) * 4      # 20 (parentheses override)
result = 2 ** 3 ** 2      # 512 (right-to-left: 3**2=9, then 2**9=512)

# Mixed type expressions
result = 5 + 3.0     # 8.0 (int + float  float)
result = True + 5    # 6   (bool is subclass of int)
```

### 8.2 Operator Precedence Table (Highest to Lowest)

| Precedence | Operator | Description |
|------------|----------|-------------|
| 1 (highest) | `()` | Parentheses |
| 2 | `**` | Exponentiation |
| 3 | `+x`, `-x`, `~x` | Unary plus, minus, bitwise NOT |
| 4 | `*`, `/`, `//`, `%` | Multiplication, Division, Floor div, Modulus |
| 5 | `+`, `-` | Addition, Subtraction |
| 6 | `<<`, `>>` | Bitwise shifts |
| 7 | `&` | Bitwise AND |
| 8 | `^` | Bitwise XOR |
| 9 | `\|` | Bitwise OR |
| 10 | `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `is not`, `in`, `not in` | Comparisons, identity, membership |
| 11 | `not` | Logical NOT |
| 12 | `and` | Logical AND |
| 13 (lowest) | `or` | Logical OR |

```python
# Precedence examples
print(2 + 3 * 4)          # 14 (multiplication first)
print((2 + 3) * 4)        # 20 (parentheses first)
print(2 ** 3 ** 2)        # 512 (** is right-associative)
print(-2 ** 2)            # -4 (** before unary -)
print((-2) ** 2)          # 4

print(True or False and False)    # True (and before or)
print((True or False) and False)  # False

print(not True or False)         # False (not before or)
print(not (True or False))       # False

# Comparison chaining
x = 5
print(1 < x < 10)        # True (equivalent to 1 < x and x < 10)
print(1 < x > 3)         # True
```

---

## 9. Type Conversion

### 9.1 Implicit (Automatic) Conversion

Python automatically converts types in mixed-type operations.

```python
# int  float (widening)
result = 5 + 3.2
print(result)        # 8.2
print(type(result))  # <class 'float'>

# bool  int
result = True + 5
print(result)        # 6
print(type(result))  # <class 'int'>

# int  complex
result = 5 + 2j
print(result)        # (5+2j)
print(type(result))  # <class 'complex'>

# Hierarchy: bool  int  float  complex
```

### 9.2 Explicit Conversion (Type Casting)

```python
# int() -- convert to integer
print(int(3.7))        # 3 (truncates, doesn't round)
print(int(-3.7))       # -3
print(int("42"))       # 42
print(int("0b1010", 2))  # 10 (binary string)
print(int("0xff", 16))   # 255 (hex string)
print(int(True))       # 1
print(int(False))      # 0

# float() -- convert to float
print(float(42))       # 42.0
print(float("3.14"))   # 3.14
print(float("inf"))    # inf
print(float(True))     # 1.0

# str() -- convert to string
print(str(42))         # "42"
print(str(3.14))       # "3.14"
print(str(True))       # "True"
print(str([1, 2, 3]))  # "[1, 2, 3]"

# bool() -- convert to boolean
print(bool(0))         # False
print(bool(1))         # True
print(bool(-1))        # True (any non-zero is True)
print(bool(""))        # False
print(bool("hello"))   # True
print(bool([]))        # False
print(bool([1]))       # True
print(bool(None))      # False

# list() -- convert to list
print(list("hello"))          # ['h', 'e', 'l', 'l', 'o']
print(list((1, 2, 3)))        # [1, 2, 3]
print(list({1, 2, 3}))        # [1, 2, 3] (order may vary)
print(list(range(5)))         # [0, 1, 2, 3, 4]
print(list({"a": 1, "b": 2}))  # ['a', 'b'] (keys)

# tuple() -- convert to tuple
print(tuple([1, 2, 3]))       # (1, 2, 3)
print(tuple("hello"))         # ('h', 'e', 'l', 'l', 'o')

# set() -- convert to set (removes duplicates)
print(set([1, 2, 2, 3, 3]))   # {1, 2, 3}
print(set("hello"))            # {'h', 'e', 'l', 'o'}
```

### 9.3 Common Conversion Errors

```python
# These will raise ValueError
# int("hello")        # ValueError: invalid literal
# int("3.14")         # ValueError: invalid literal (use float() first)
# float("abc")        # ValueError: could not convert

# Safe conversion
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

print(safe_int("42"))      # 42
print(safe_int("hello"))   # 0 (default)
print(safe_int(None, -1))  # -1
```

---

## 10. Input / Output

### 10.1 `input()` -- Reading User Input

`input()` always returns a **string**. You need explicit type casting for numbers.

```python
# Basic input
name = input("What is your name? ")
print(f"Hello, {name}!")

# Input with type casting
age = int(input("Enter your age: "))
height = float(input("Enter your height in meters: "))
print(f"You are {age} years old and {height}m tall.")

# Reading multiple values
x, y = input("Enter two numbers separated by space: ").split()
x, y = int(x), int(y)
print(f"Sum: {x + y}")

# One-liner: map for multiple typed inputs
a, b, c = map(int, input("Enter three integers: ").split())
print(f"Sum: {a + b + c}")

# Reading a list of numbers
numbers = list(map(int, input("Enter numbers: ").split()))
print(f"Numbers: {numbers}, Sum: {sum(numbers)}")
```

### 10.2 `print()` -- Output

```python
# Basic print
print("Hello, World!")

# Multiple arguments (separated by space by default)
print("Hello", "World", "Python")  # Hello World Python

# sep parameter -- custom separator
print("2025", "05", "31", sep="-")   # 2025-05-31
print("a", "b", "c", sep=" | ")      # a | b | c
print(1, 2, 3, sep="")               # 123

# end parameter -- what to print at the end (default: \n)
print("Loading", end="")
print("...", end="")
print("Done!")
# Output: Loading...Done!

# Print to a file
with open("output.txt", "w") as f:
    print("Hello, File!", file=f)
    print("Line 2", file=f)

# flush parameter -- force immediate output
import time
for i in range(5):
    print(f"\rProgress: {i+1}/5", end="", flush=True)
    time.sleep(0.5)
print()  # final newline
```

### 10.3 Formatted Output

```python
name = "Alice"
age = 30
gpa = 3.8567

# f-strings (recommended)
print(f"{name} is {age} and has a GPA of {gpa:.2f}")
# Alice is 30 and has a GPA of 3.86

# format() method
print("{} is {} and has a GPA of {:.2f}".format(name, age, gpa))

# %-formatting (old style, still works)
print("%s is %d and has a GPA of %.2f" % (name, age, gpa))

# Aligned output
for item, price in [("Apple", 1.50), ("Banana", 0.75), ("Cherry", 3.20)]:
    print(f"{item:<10} ${price:>6.2f}")
# Apple      $  1.50
# Banana     $  0.75
# Cherry     $  3.20

# Printing a table
header = f"{'Name':<15} {'Age':>5} {'Score':>8}"
separator = "-" * len(header)
print(header)
print(separator)
for name, age, score in [("Alice", 25, 92.5), ("Bob", 30, 88.0), ("Charlie", 28, 95.3)]:
    print(f"{name:<15} {age:>5} {score:>8.1f}")
```

---

## 11. String Manipulation

### 11.1 Common String Operations Recap

```python
s = "Hello, World!"

# Length
print(len(s))              # 13

# Concatenation
greeting = "Hello" + " " + "World"
print(greeting)            # Hello World

# Repetition
print("Ha" * 3)            # HaHaHa
print("-" * 40)            # ----------------------------------------

# Membership
print("World" in s)        # True
print("Python" not in s)   # True

# Iteration
for char in "Python":
    print(char, end=" ")   # P y t h o n
```

### 11.2 String Formatting Deep Dive

#### Method 1: `%`-Formatting (Old Style)

```python
name = "Alice"
age = 30
pi = 3.14159

# %s = string, %d = integer, %f = float
print("Name: %s" % name)
print("Age: %d" % age)
print("Pi: %.2f" % pi)
print("Pi: %10.3f" % pi)      #      3.142 (width 10)
print("Name: %-10s|" % name)   # Alice     | (left-aligned)

# Multiple values (use tuple)
print("Name: %s, Age: %d, GPA: %.1f" % (name, age, 3.85))

# Common format specifiers
# %s  -- string
# %d  -- integer
# %f  -- float
# %e  -- scientific notation
# %x  -- hexadecimal
# %o  -- octal
# %%  -- literal %
print("Discount: %d%%" % 20)  # Discount: 20%
```

#### Method 2: `.format()` Method

```python
# Positional
print("{} {} {}".format("Hello", "Beautiful", "World"))

# Indexed
print("{2} {0} {1}".format("World", "Beautiful", "Hello"))

# Named
print("{greeting}, {name}!".format(greeting="Hello", name="Alice"))

# Formatting spec
print("{:.3f}".format(3.14159))       # 3.142
print("{:10d}".format(42))            #         42
print("{:<10d}".format(42))           # 42
print("{:^10d}".format(42))           #     42
print("{:0>5d}".format(42))           # 00042
print("{:,}".format(1000000))         # 1,000,000
print("{:.2%}".format(0.75))          # 75.00%
print("{:#x}".format(255))            # 0xff
print("{:#b}".format(10))             # 0b1010

# Access attributes and items
person = {"name": "Alice", "age": 30}
print("Name: {p[name]}, Age: {p[age]}".format(p=person))

import math
print("Pi: {m.pi:.4f}".format(m=math))
```

#### Method 3: F-Strings (Recommended -- Python 3.6+)

```python
name = "Alice"
scores = [85, 92, 78, 95]

# Expressions
print(f"Average: {sum(scores)/len(scores):.1f}")

# Conditionals
status = "pass" if sum(scores)/len(scores) >= 60 else "fail"
print(f"Status: {status}")

# Calling functions
print(f"{'hello'.upper()}")   # HELLO

# Multi-line f-strings
message = (
    f"Student: {name}\n"
    f"Scores: {scores}\n"
    f"Average: {sum(scores)/len(scores):.1f}\n"
)
print(message)

# Dictionary access in f-strings
data = {"x": 10, "y": 20}
print(f"x={data['x']}, y={data['y']}")  # x=10, y=20

# Nesting (Python 3.12+)
print(f"{'hello':{'>'}{10}}")  #      hello
```

### 11.3 Useful String Recipes

```python
# Check if string is a palindrome
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(is_palindrome("racecar"))     # True
print(is_palindrome("A Santa at NASA"))  # True

# Count vowels
def count_vowels(s):
    return sum(1 for c in s.lower() if c in "aeiou")

print(count_vowels("Hello World"))  # 3

# Remove duplicates while preserving order
def remove_duplicates(s):
    seen = set()
    return "".join(c for c in s if not (c in seen or seen.add(c)))

print(remove_duplicates("programming"))  # proaming

# Caesar cipher
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

print(caesar_encrypt("Hello, World!", 3))  # Khoor, Zruog!
```

---

##  Quick Reference

```python
# Variables
x, y = 10, 20      # Multiple assignment
x, y = y, x        # Swap

# Type checking
type(x)             # Get type
isinstance(x, int)  # Check type

# Type conversion
int("42")           # String to int
float("3.14")       # String to float
str(42)             # Int to string
bool(0)             # Any to bool

# String operations
s = "Hello"
s.upper()           # "HELLO"
s.lower()           # "hello"
s.split(",")        # Split by delimiter
",".join(list)      # Join with delimiter
s.strip()           # Remove whitespace
s.replace("H","J")  # Replace
s.find("lo")        # Find index
f"{var:.2f}"        # F-string formatting

# I/O
name = input("? ")         # Read input
x = int(input("? "))       # Read integer
print(a, b, sep="-")       # Custom separator
print(a, end="")           # No newline
```

---

> **Next:** Day 3 -- Lists, Tuples, Dictionaries & Sets
