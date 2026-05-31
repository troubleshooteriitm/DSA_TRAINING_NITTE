"""
Lambda, Map, Filter, Reduce Demo
==================================
Practical examples of functional programming constructs in Python.
"""

from functools import reduce


# ============================================================
# 1. LAMBDA BASICS
# ============================================================

print("=" * 50)
print("  LAMBDA, MAP, FILTER, REDUCE DEMO")
print("=" * 50)

# Simple lambda
square = lambda x: x ** 2
print(f"\n--- Lambda Basics ---")
print(f"square(7) = {square(7)}")

# Lambda with multiple args
multiply = lambda a, b: a * b
print(f"multiply(4, 5) = {multiply(4, 5)}")

# Conditional lambda
classify = lambda x: "even" if x % 2 == 0 else "odd"
print(f"classify(7) = {classify(7)}, classify(8) = {classify(8)}")


# ============================================================
# 2. SORTING WITH LAMBDA
# ============================================================

print(f"\n--- Sorting with Lambda ---")

# Sort strings by length
words = ["python", "is", "an", "amazing", "programming", "language"]
sorted_by_len = sorted(words, key=lambda w: len(w))
print(f"By length: {sorted_by_len}")

# Sort tuples by second element
students = [("Alice", 88), ("Bob", 95), ("Charlie", 72), ("Diana", 91)]
sorted_by_grade = sorted(students, key=lambda s: s[1], reverse=True)
print(f"By grade (desc): {sorted_by_grade}")

# Sort dicts by value
inventory = [
    {"item": "Laptop", "price": 75000},
    {"item": "Mouse", "price": 500},
    {"item": "Keyboard", "price": 2500},
    {"item": "Monitor", "price": 25000},
]
sorted_by_price = sorted(inventory, key=lambda d: d["price"])
print(f"By price: {[d['item'] for d in sorted_by_price]}")


# ============================================================
# 3. MAP -- Transform every element
# ============================================================

print(f"\n--- map() Examples ---")

# Square all numbers
nums = [1, 2, 3, 4, 5, 6, 7, 8]
squares = list(map(lambda x: x ** 2, nums))
print(f"Squares: {squares}")

# Convert temperatures: Celsius to Fahrenheit
celsius = [0, 20, 37, 100]
fahrenheit = list(map(lambda c: round(c * 9 / 5 + 32, 1), celsius))
print(f"Celsius {celsius}  Fahrenheit {fahrenheit}")

# Extract names from dicts
employees = [
    {"name": "Alice", "dept": "Engineering"},
    {"name": "Bob", "dept": "Sales"},
    {"name": "Charlie", "dept": "Engineering"},
]
names = list(map(lambda e: e["name"], employees))
print(f"Names: {names}")

# Map with multiple iterables
list_a = [1, 2, 3]
list_b = [10, 20, 30]
sums = list(map(lambda a, b: a + b, list_a, list_b))
print(f"Pairwise sums: {sums}")


# ============================================================
# 4. FILTER -- Keep elements matching condition
# ============================================================

print(f"\n--- filter() Examples ---")

# Filter even numbers
nums = list(range(1, 21))
evens = list(filter(lambda x: x % 2 == 0, nums))
print(f"Evens from 1-20: {evens}")

# Filter strings longer than 4 chars
words = ["hi", "hello", "hey", "greetings", "yo", "welcome"]
long_words = list(filter(lambda w: len(w) > 4, words))
print(f"Words > 4 chars: {long_words}")

# Filter employees by department
engineering = list(filter(lambda e: e["dept"] == "Engineering", employees))
print(f"Engineering team: {[e['name'] for e in engineering]}")

# Filter out None/empty values
mixed = [0, 1, "", "hello", None, [], [1, 2], False, True]
truthy = list(filter(None, mixed))
print(f"Truthy values: {truthy}")


# ============================================================
# 5. REDUCE -- Aggregate to single value
# ============================================================

print(f"\n--- reduce() Examples ---")

# Sum of numbers
nums = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, nums)
print(f"Sum of {nums} = {total}")

# Product of numbers
product = reduce(lambda a, b: a * b, nums)
print(f"Product of {nums} = {product}")

# Find maximum
nums = [34, 12, 89, 45, 67, 23]
maximum = reduce(lambda a, b: a if a > b else b, nums)
print(f"Max of {nums} = {maximum}")

# Flatten nested list
nested = [[1, 2], [3, 4], [5, 6], [7, 8]]
flat = reduce(lambda a, b: a + b, nested)
print(f"Flattened: {flat}")

# Build string
words = ["Python", "is", "awesome"]
sentence = reduce(lambda a, b: a + " " + b, words)
print(f"Sentence: '{sentence}'")


# ============================================================
# 6. COMBINING MAP + FILTER + REDUCE
# ============================================================

print(f"\n--- Combined Pipeline ---")

# Get total salary of senior employees (age > 30)
employees_data = [
    {"name": "Alice", "age": 35, "salary": 85000},
    {"name": "Bob", "age": 25, "salary": 55000},
    {"name": "Charlie", "age": 42, "salary": 95000},
    {"name": "Diana", "age": 28, "salary": 60000},
    {"name": "Eve", "age": 38, "salary": 90000},
]

senior_total = reduce(
    lambda a, b: a + b,                           # reduce: sum
    map(
        lambda e: e["salary"],                     # map: extract salary
        filter(lambda e: e["age"] > 30, employees_data)  # filter: age > 30
    )
)
print(f"Total salary of senior employees (age > 30): ₹{senior_total:,}")

# Equivalent using comprehension (more Pythonic)
senior_total_v2 = sum(e["salary"] for e in employees_data if e["age"] > 30)
print(f"Same result with comprehension: ₹{senior_total_v2:,}")
