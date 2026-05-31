"""
Comprehensions Demo
====================
List, Dict, Set comprehensions -- filtering, transformation, nested, conditional.
"""

print("=" * 50)
print("  COMPREHENSIONS DEMO")
print("=" * 50)

# ============================================================
# 1. LIST COMPREHENSIONS
# ============================================================

print("\n--- List Comprehensions ---")

# Basic
squares = [x**2 for x in range(1, 11)]
print(f"Squares 1-10: {squares}")

# With filter
evens = [x for x in range(1, 21) if x % 2 == 0]
print(f"Evens 1-20: {evens}")

# With conditional expression
labels = ["even" if x % 2 == 0 else "odd" for x in range(1, 8)]
print(f"Labels: {labels}")

# Nested -- flatten 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(f"Flattened: {flat}")

# Nested -- create multiplication table
table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
print(f"5x5 table:")
for row in table:
    print(f"  {row}")

# String processing
words = ["  Hello  ", " World ", "  Python  "]
cleaned = [w.strip().lower() for w in words]
print(f"Cleaned: {cleaned}")

# ============================================================
# 2. DICT COMPREHENSIONS
# ============================================================

print("\n--- Dict Comprehensions ---")

# Word lengths
sentence = "the quick brown fox jumps over the lazy dog"
word_lengths = {w: len(w) for w in sentence.split()}
print(f"Word lengths: {word_lengths}")

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(f"Swapped: {swapped}")

# Filter dict
scores = {"Alice": 88, "Bob": 45, "Charlie": 92, "Diana": 67, "Eve": 34}
passed = {name: score for name, score in scores.items() if score >= 50}
print(f"Passed: {passed}")

# Enumerate to dict
fruits = ["apple", "banana", "cherry"]
indexed = {i: fruit for i, fruit in enumerate(fruits)}
print(f"Indexed: {indexed}")

# ============================================================
# 3. SET COMPREHENSIONS
# ============================================================

print("\n--- Set Comprehensions ---")

# Unique lengths
words = ["hello", "world", "hi", "hey", "python", "pie"]
unique_lens = {len(w) for w in words}
print(f"Unique lengths: {unique_lens}")

# Unique first characters
first_chars = {w[0].upper() for w in words}
print(f"First chars: {first_chars}")

# ============================================================
# 4. GENERATOR EXPRESSIONS (bonus)
# ============================================================

print("\n--- Generator Expressions ---")

# Sum of squares (no list created in memory)
total = sum(x**2 for x in range(1, 101))
print(f"Sum of squares 1-100: {total}")

# Any / All with generators
nums = [2, 4, 6, 8, 10]
all_even = all(x % 2 == 0 for x in nums)
any_gt_5 = any(x > 5 for x in nums)
print(f"All even? {all_even}, Any > 5? {any_gt_5}")

# ============================================================
# 5. REAL-WORLD EXAMPLES
# ============================================================

print("\n--- Real-World Examples ---")

# Extract emails from user data
users = [
    {"name": "Alice", "email": "alice@co.com", "active": True},
    {"name": "Bob", "email": "bob@co.com", "active": False},
    {"name": "Charlie", "email": "charlie@co.com", "active": True},
]
active_emails = [u["email"] for u in users if u["active"]]
print(f"Active emails: {active_emails}")

# Create lookup table
products = [
    {"id": "P001", "name": "Laptop", "price": 75000},
    {"id": "P002", "name": "Mouse", "price": 500},
    {"id": "P003", "name": "Monitor", "price": 25000},
]
price_lookup = {p["id"]: p["price"] for p in products}
print(f"Price lookup: {price_lookup}")

# Categorize numbers
nums = range(-5, 6)
categorized = {n: ("positive" if n > 0 else "negative" if n < 0 else "zero") for n in nums}
print(f"Categorized: {categorized}")
