# Day 3: Control Flow -- Conditionals, Loops & Optimization

> **DSA Training -- Day 3**
> Master Python's control flow: conditionals, relational & boolean operators, loops, nesting, optimization techniques, and classic pattern programs.

---

## Table of Contents

1. [Conditional Statements](#1-conditional-statements)
2. [Relational Operators](#2-relational-operators)
3. [Boolean Operators](#3-boolean-operators)
4. [if-else Patterns](#4-if-else-patterns)
5. [for Loops](#5-for-loops)
6. [while Loops](#6-while-loops)
7. [Nested Loops](#7-nested-loops)
8. [Loop Optimization Techniques](#8-loop-optimization-techniques)
9. [Pattern Programs](#9-pattern-programs)

---

## 1. Conditional Statements

Conditional statements allow your program to make decisions and execute different blocks of code depending on whether a condition is `True` or `False`.

### Basic `if` Statement

```python
age = 20
if age >= 18:
    print("You are an adult.")
# Output: You are an adult.
```

### `if-else` Statement

```python
temperature = 35
if temperature > 30:
    print("It's a hot day! Stay hydrated.")
else:
    print("The weather is pleasant.")
# Output: It's a hot day! Stay hydrated.
```

### `if-elif-else` Chain

```python
score = 78

if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'

print(f"Score: {score}, Grade: {grade}")
# Output: Score: 78, Grade: C
```

### Multiple Conditions Example -- Traffic Light

```python
light = "yellow"

if light == "green":
    print("Go!")
elif light == "yellow":
    print("Slow down, prepare to stop.")
elif light == "red":
    print("Stop!")
else:
    print("Invalid signal -- proceed with caution.")
# Output: Slow down, prepare to stop.
```

### Multiple Conditions Example -- BMI Category

```python
weight = 70   # kg
height = 1.75 # meters
bmi = weight / (height ** 2)

if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Normal weight"
elif bmi < 30:
    category = "Overweight"
else:
    category = "Obese"

print(f"BMI: {bmi:.1f} -- {category}")
# Output: BMI: 22.9 -- Normal weight
```

---

## 2. Relational Operators

Relational (comparison) operators compare two values and return a `bool` (`True` or `False`).

| Operator | Meaning                  | Example       | Result  |
|----------|--------------------------|---------------|---------|
| `==`     | Equal to                 | `5 == 5`      | `True`  |
| `!=`     | Not equal to             | `5 != 3`      | `True`  |
| `<`      | Less than                | `3 < 5`       | `True`  |
| `>`      | Greater than             | `5 > 3`       | `True`  |
| `<=`     | Less than or equal to    | `5 <= 5`      | `True`  |
| `>=`     | Greater than or equal to | `4 >= 5`      | `False` |

### Examples

```python
a, b = 10, 20

print(a == b)   # False
print(a != b)   # True
print(a < b)    # True
print(a > b)    # False
print(a <= 10)  # True
print(a >= 15)  # False
```

### Comparing Strings (Lexicographic Order)

```python
print("apple" < "banana")   # True  (a comes before b)
print("cat" == "Cat")       # False (case-sensitive)
print("hello" != "world")   # True
```

### Comparing Different Types

```python
print(10 == 10.0)  # True  (int vs float -- values are equal)
print(10 == "10")  # False (int vs str -- different types)
```

---

## 3. Boolean Operators

Boolean operators combine or modify boolean expressions.

| Operator | Description                          | Example                    | Result  |
|----------|--------------------------------------|----------------------------|---------|
| `and`    | True if BOTH operands are True       | `True and False`           | `False` |
| `or`     | True if AT LEAST ONE operand is True | `True or False`            | `True`  |
| `not`    | Inverts the boolean value            | `not True`                 | `False` |

### Truth Tables

**`and` -- Both must be True:**
```python
print(True and True)    # True
print(True and False)   # False
print(False and True)   # False
print(False and False)  # False
```

**`or` -- At least one must be True:**
```python
print(True or True)    # True
print(True or False)   # True
print(False or True)   # True
print(False or False)  # False
```

**`not` -- Inverts the value:**
```python
print(not True)   # False
print(not False)  # True
```

### Practical Example -- Login Validation

```python
username = "admin"
password = "secret123"

if username == "admin" and password == "secret123":
    print("Login successful!")
else:
    print("Invalid credentials.")
# Output: Login successful!
```

### Practical Example -- Eligibility Check

```python
age = 25
has_license = True
has_insurance = False

if age >= 18 and has_license and has_insurance:
    print("You can rent a car.")
elif age >= 18 and has_license:
    print("You need insurance to rent a car.")
else:
    print("You are not eligible to rent a car.")
# Output: You need insurance to rent a car.
```

### Short-Circuit Evaluation

Python stops evaluating as soon as the result is determined:

```python
# 'and' short-circuits on the first False
x = 0
if x != 0 and 10 / x > 2:  # 10/x is NEVER evaluated (avoids ZeroDivisionError!)
    print("Condition met")
else:
    print("Short-circuited safely!")
# Output: Short-circuited safely!

# 'or' short-circuits on the first True
name = "" or "Default User"
print(name)  # Output: Default User

# Another example -- first truthy value wins
result = None or 0 or "" or "Found it!" or "Backup"
print(result)  # Output: Found it!
```

---

## 4. if-else Patterns

### Ternary / Conditional Expression

A compact one-line `if-else`:

```python
age = 20
status = "adult" if age >= 18 else "minor"
print(status)  # Output: adult

# Ternary in a function
def absolute(n):
    return n if n >= 0 else -n

print(absolute(-7))  # Output: 7
```

### Nested if Statements

```python
num = 15

if num > 0:
    if num % 2 == 0:
        print(f"{num} is positive and even")
    else:
        print(f"{num} is positive and odd")
elif num < 0:
    print(f"{num} is negative")
else:
    print("The number is zero")
# Output: 15 is positive and odd
```

### Chained Comparisons

Python supports mathematical-style chained comparisons -- a unique and elegant feature:

```python
x = 15

# Instead of: x > 10 and x < 20
if 10 < x < 20:
    print(f"{x} is between 10 and 20")
# Output: 15 is between 10 and 20

# Multiple chaining
a, b, c = 1, 2, 3
print(a < b < c)      # True  -- equivalent to (a < b) and (b < c)
print(a < b > c)      # False -- equivalent to (a < b) and (b > c)
print(1 <= 1 < 2)     # True
print(1 == 1 == 1)    # True

# Practical: check if a value is within a range
score = 85
if 0 <= score <= 100:
    print("Valid score")
# Output: Valid score
```

### Guard Clauses (Early Return Pattern)

```python
def process_order(quantity, price):
    if quantity <= 0:
        return "Error: quantity must be positive"
    if price < 0:
        return "Error: price cannot be negative"
    if quantity > 1000:
        return "Error: order too large"

    total = quantity * price
    discount = 0.1 if total > 500 else 0
    return f"Total: ${total * (1 - discount):.2f}"

print(process_order(10, 25))    # Total: $250.00
print(process_order(-1, 25))    # Error: quantity must be positive
print(process_order(100, 10))   # Total: $900.00
```

---

## 5. for Loops

### `range()` with 1 Argument (stop)

```python
# range(stop) -- generates 0, 1, 2, ..., stop-1
for i in range(5):
    print(i, end=" ")
# Output: 0 1 2 3 4
```

### `range()` with 2 Arguments (start, stop)

```python
# range(start, stop) -- generates start, start+1, ..., stop-1
for i in range(3, 8):
    print(i, end=" ")
# Output: 3 4 5 6 7
```

### `range()` with 3 Arguments (start, stop, step)

```python
# range(start, stop, step)
for i in range(0, 20, 3):
    print(i, end=" ")
# Output: 0 3 6 9 12 15 18

# Counting backwards
for i in range(10, 0, -2):
    print(i, end=" ")
# Output: 10 8 6 4 2
```

### Iterating Over Strings

```python
word = "Python"
for char in word:
    print(char, end="-")
# Output: P-y-t-h-o-n-

# With index using enumerate
for i, char in enumerate(word):
    print(f"Index {i}: {char}")
```

### Iterating Over Lists

```python
fruits = ["apple", "banana", "cherry", "date"]
for fruit in fruits:
    print(f"I like {fruit}")

# Summing a list
numbers = [10, 20, 30, 40, 50]
total = 0
for num in numbers:
    total += num
print(f"Sum = {total}")  # Sum = 150
```

### Iterating Over Dictionaries

```python
student = {"name": "Alice", "age": 21, "grade": "A"}

# Keys only (default)
for key in student:
    print(key)

# Values only
for value in student.values():
    print(value)

# Key-value pairs
for key, value in student.items():
    print(f"{key}: {value}")
# Output:
# name: Alice
# age: 21
# grade: A
```

### Iterating Over Tuples

```python
coordinates = [(1, 2), (3, 4), (5, 6)]
for x, y in coordinates:
    print(f"Point: ({x}, {y})")
# Output:
# Point: (1, 2)
# Point: (3, 4)
# Point: (5, 6)
```

### Iterating Over Sets

```python
unique_numbers = {3, 1, 4, 1, 5, 9}  # Duplicates removed automatically
for num in unique_numbers:
    print(num, end=" ")
# Output: order may vary since sets are unordered
```

### `for-else` Clause

The `else` block runs only if the loop completes **without** hitting `break`:

```python
numbers = [2, 4, 6, 8, 10]

for num in numbers:
    if num % 2 != 0:
        print(f"Found an odd number: {num}")
        break
else:
    print("All numbers are even!")
# Output: All numbers are even!
```

---

## 6. while Loops

### Basic while Loop

```python
count = 1
while count <= 5:
    print(count, end=" ")
    count += 1
# Output: 1 2 3 4 5
```

### while Loop with User-Like Input (Countdown)

```python
countdown = 5
while countdown > 0:
    print(f"T-minus {countdown}...")
    countdown -= 1
print("Liftoff! ")
```

### while with `break`

```python
# Find the first number divisible by 7 in a range
num = 50
while num <= 100:
    if num % 7 == 0:
        print(f"First number divisible by 7: {num}")
        break
    num += 1
# Output: First number divisible by 7: 56
```

### while with `continue`

```python
# Print only odd numbers from 1 to 10
num = 0
while num < 10:
    num += 1
    if num % 2 == 0:
        continue  # Skip even numbers
    print(num, end=" ")
# Output: 1 3 5 7 9
```

### while with `else` Clause

The `else` block runs when the condition becomes `False` (not when `break` is used):

```python
n = 5
while n > 0:
    print(n, end=" ")
    n -= 1
else:
    print("-- Loop finished normally (no break)")
# Output: 5 4 3 2 1 -- Loop finished normally (no break)

# Contrast with break:
n = 5
while n > 0:
    if n == 3:
        print("Breaking!")
        break
    print(n, end=" ")
    n -= 1
else:
    print("This will NOT print")
# Output: 5 4 Breaking!
```

### Practical: Guessing Game Logic

```python
secret = 42
guesses = [10, 25, 42, 50]  # Simulated guesses
attempt = 0

while attempt < len(guesses):
    guess = guesses[attempt]
    attempt += 1
    if guess < secret:
        print(f"Guess {guess}: Too low!")
    elif guess > secret:
        print(f"Guess {guess}: Too high!")
    else:
        print(f"Guess {guess}: Correct!  Found in {attempt} attempts.")
        break
```

---

## 7. Nested Loops

### Basic Nested Loop -- Multiplication Table

```python
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:4d}", end="")
    print()

# Output:
#    1   2   3   4   5
#    2   4   6   8  10
#    3   6   9  12  15
#    4   8  12  16  20
#    5  10  15  20  25
```

### Matrix Traversal

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access every element
for row in range(len(matrix)):
    for col in range(len(matrix[row])):
        print(f"matrix[{row}][{col}] = {matrix[row][col]}")

# More Pythonic way
for row in matrix:
    for element in row:
        print(element, end=" ")
    print()
```

### Finding Pairs with a Target Sum

```python
numbers = [2, 4, 6, 8, 10]
target = 12

print(f"Pairs that sum to {target}:")
for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        if numbers[i] + numbers[j] == target:
            print(f"  ({numbers[i]}, {numbers[j]})")
# Output:
# Pairs that sum to 12:
#   (2, 10)
#   (4, 8)
```

### Nested Loop with Break -- Prime Checking

```python
for num in range(2, 20):
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num, end=" ")
# Output: 2 3 5 7 11 13 17 19
```

---

## 8. Loop Optimization Techniques

### 1. List Comprehension vs Traditional Loop

```python
# Traditional loop
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension -- faster and more readable
squares = [x ** 2 for x in range(10)]

# With condition
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]
```

### 2. `enumerate()` Instead of Manual Index

```python
fruits = ["apple", "banana", "cherry"]

#  Bad -- manual index
index = 0
for fruit in fruits:
    print(f"{index}: {fruit}")
    index += 1

#  Good -- enumerate
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Start from a custom index
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
```

### 3. `zip()` for Parallel Iteration

```python
names = ["Alice", "Bob", "Charlie"]
scores = [95, 82, 78]
grades = ["A", "B", "C"]

#  Bad -- manual indexing
for i in range(len(names)):
    print(f"{names[i]}: {scores[i]}, Grade {grades[i]}")

#  Good -- zip
for name, score, grade in zip(names, scores, grades):
    print(f"{name}: {score}, Grade {grade}")
```

### 4. Avoiding Repeated Computation Inside Loops

```python
data = [1, 2, 3, 4, 5]

#  Bad -- len() called every iteration
for i in range(len(data)):
    print(data[i] / len(data))

#  Good -- pre-compute
n = len(data)
for i in range(n):
    print(data[i] / n)
```

### 5. Generator Expressions for Memory Efficiency

```python
# List comprehension -- builds entire list in memory
sum_list = sum([x ** 2 for x in range(1_000_000)])

# Generator expression -- processes one element at a time
sum_gen = sum(x ** 2 for x in range(1_000_000))

# Both give the same result, but generator uses far less memory
```

### 6. Using `break` Effectively

```python
# Stop as soon as you find what you need
large_list = list(range(1_000_000))
target = 99999

for item in large_list:
    if item == target:
        print(f"Found {target}")
        break
# Much faster than scanning the entire list
```

---

## 9. Pattern Programs

### Right Triangle (Stars)

```python
n = 5
for i in range(1, n + 1):
    print('*' * i)
```
**Output:**
```
*
**
***
****
*****
```

### Inverted Right Triangle

```python
n = 5
for i in range(n, 0, -1):
    print('*' * i)
```
**Output:**
```
*****
****
***
**
*
```

### Pyramid (Centered Stars)

```python
n = 5
for i in range(1, n + 1):
    spaces = ' ' * (n - i)
    stars = '*' * (2 * i - 1)
    print(spaces + stars)
```
**Output:**
```
    *
   ***
  *****
 *******
*********
```

### Diamond

```python
n = 5
# Upper half (pyramid)
for i in range(1, n + 1):
    print(' ' * (n - i) + '*' * (2 * i - 1))
# Lower half (inverted pyramid)
for i in range(n - 1, 0, -1):
    print(' ' * (n - i) + '*' * (2 * i - 1))
```
**Output:**
```
    *
   ***
  *****
 *******
*********
 *******
  *****
   ***
    *
```

### Number Triangle

```python
n = 5
for i in range(1, n + 1):
    for j in range(1, i + 1):
        print(j, end="")
    print()
```
**Output:**
```
1
12
123
1234
12345
```

---

## Quick Reference Cheat Sheet

| Concept             | Syntax                                           |
|----------------------|--------------------------------------------------|
| if-elif-else         | `if cond: ... elif cond: ... else: ...`          |
| Ternary              | `value_if_true if condition else value_if_false`  |
| Chained comparison   | `a < b < c`                                     |
| for loop             | `for item in iterable:`                          |
| range (3 args)       | `range(start, stop, step)`                       |
| while loop           | `while condition:`                               |
| break                | Exit the innermost loop immediately              |
| continue             | Skip to the next iteration                       |
| for/while else       | Runs if loop ends without `break`                |
| List comprehension   | `[expr for item in iterable if cond]`            |
| enumerate            | `for i, val in enumerate(iterable):`             |
| zip                  | `for a, b in zip(list1, list2):`                 |

---

**Next up:** Day 4 -- Functions, Scope & Recursion 
