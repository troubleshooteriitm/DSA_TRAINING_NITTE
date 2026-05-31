"""
NumPy Basics -- Practice Examples
=================================

Covers:
    - Array creation (array, zeros, ones, arange, linspace)
    - Arithmetic & element-wise operations
    - Broadcasting
    - Reshaping (reshape, ravel, flatten, transpose)
    - Aggregation (sum, mean, std, min, max)
    - Boolean & fancy indexing

Requirements:
    pip install numpy
"""

import sys

try:
    import numpy as np
except ImportError:
    print("=" * 50)
    print("NumPy is not installed.")
    print("Install it with: pip install numpy")
    print("=" * 50)
    sys.exit(1)


def section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'' * 50}")
    print(f"  {title}")
    print(f"{'' * 50}")


#  1. Array Creation 

section("1. Array Creation")

# From a list
arr = np.array([1, 2, 3, 4, 5])
print(f"From list:     {arr}")
print(f"  dtype: {arr.dtype}, shape: {arr.shape}")

# 2D array
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n2D array:\n{matrix}")
print(f"  shape: {matrix.shape}, ndim: {matrix.ndim}")

# Zeros and ones
print(f"\nzeros(3, 4):\n{np.zeros((3, 4))}")
print(f"\nones(2, 3):\n{np.ones((2, 3))}")

# arange -- like range() but for NumPy
print(f"\narange(0, 10, 2): {np.arange(0, 10, 2)}")
print(f"arange(5):        {np.arange(5)}")

# linspace -- evenly spaced numbers
print(f"\nlinspace(0, 1, 5):  {np.linspace(0, 1, 5)}")
print(f"linspace(0, 100, 6): {np.linspace(0, 100, 6)}")

# Identity matrix
print(f"\neye(3):\n{np.eye(3)}")

# Random arrays
print(f"\nrandom.rand(2, 3):\n{np.random.rand(2, 3).round(3)}")
print(f"\nrandom.randint(1, 100, (2, 4)):\n{np.random.randint(1, 100, (2, 4))}")


#  2. Arithmetic & Element-wise Operations 

section("2. Arithmetic Operations")

a = np.array([10, 20, 30, 40])
b = np.array([1, 2, 3, 4])

print(f"a = {a}")
print(f"b = {b}")
print(f"a + b = {a + b}")
print(f"a - b = {a - b}")
print(f"a * b = {a * b}")
print(f"a / b = {a / b}")
print(f"a ** 2 = {a ** 2}")
print(f"np.sqrt(a) = {np.sqrt(a).round(3)}")
print(f"np.log(a)  = {np.log(a).round(3)}")

# Comparison (returns boolean array)
print(f"\na > 20:  {a > 20}")
print(f"a == 30: {a == 30}")


#  3. Broadcasting 

section("3. Broadcasting")

# Scalar + array
arr = np.array([1, 2, 3, 4])
print(f"arr = {arr}")
print(f"arr + 100 = {arr + 100}")
print(f"arr * 5   = {arr * 5}")

# Row vector + matrix
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
row = np.array([10, 20, 30])
print(f"\nmatrix:\n{matrix}")
print(f"row: {row}")
print(f"matrix + row:\n{matrix + row}")

# Column vector + matrix
col = np.array([[100], [200], [300]])
print(f"\ncol:\n{col}")
print(f"matrix + col:\n{matrix + col}")


#  4. Reshaping 

section("4. Reshaping")

arr = np.arange(12)
print(f"Original: {arr}  (shape: {arr.shape})")

# Reshape to 3x4
reshaped = arr.reshape(3, 4)
print(f"\nreshaped(3, 4):\n{reshaped}")

# Reshape with -1 (auto-calculate)
print(f"\nreshaped(2, -1):\n{arr.reshape(2, -1)}")
print(f"reshaped(-1, 6):\n{arr.reshape(-1, 6)}")

# Ravel (flatten to 1D -- returns view)
print(f"\nravel(): {reshaped.ravel()}")

# Flatten (always returns copy)
print(f"flatten(): {reshaped.flatten()}")

# Transpose
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\nOriginal {matrix.shape}:\n{matrix}")
print(f"Transposed {matrix.T.shape}:\n{matrix.T}")

# Stacking
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(f"\nvstack:\n{np.vstack([a, b])}")
print(f"hstack: {np.hstack([a, b])}")
print(f"column_stack:\n{np.column_stack([a, b])}")


#  5. Aggregation 

section("5. Aggregation")

data = np.array([[10, 20, 30],
                 [40, 50, 60],
                 [70, 80, 90]])
print(f"Data:\n{data}")

print(f"\nGlobal aggregation:")
print(f"  sum:  {np.sum(data)}")
print(f"  mean: {np.mean(data)}")
print(f"  std:  {np.std(data):.2f}")
print(f"  min:  {np.min(data)}")
print(f"  max:  {np.max(data)}")

print(f"\nAxis=0 (column-wise):")
print(f"  sum:  {np.sum(data, axis=0)}")
print(f"  mean: {np.mean(data, axis=0)}")

print(f"\nAxis=1 (row-wise):")
print(f"  sum:  {np.sum(data, axis=1)}")
print(f"  mean: {np.mean(data, axis=1)}")

print(f"\nOther:")
print(f"  median:  {np.median(data)}")
print(f"  var:     {np.var(data):.2f}")
print(f"  cumsum:  {np.cumsum(data)}")
print(f"  argmax:  {np.argmax(data)} (index of max)")
print(f"  argmin:  {np.argmin(data)} (index of min)")


#  6. Boolean & Fancy Indexing 

section("6. Boolean & Fancy Indexing")

scores = np.array([45, 78, 92, 55, 88, 33, 71, 96, 60, 82])
print(f"Scores: {scores}")

# Boolean indexing
passing = scores >= 60
print(f"Passing (>=60): {scores[passing]}")
print(f"High scores (>85): {scores[scores > 85]}")
print(f"Range (60-90): {scores[(scores >= 60) & (scores <= 90)]}")

# Fancy indexing
indices = [0, 3, 7]
print(f"\nFancy indexing [{indices}]: {scores[indices]}")

# Where
print(f"\nnp.where(scores >= 60, 'Pass', 'Fail'):")
print(f"  {np.where(scores >= 60, 'Pass', 'Fail')}")


#  Summary 

section("Summary")
print("""
  NumPy Key Concepts:
   ndarray -- fast, typed, fixed-size arrays
   Vectorized operations -- no explicit loops needed
   Broadcasting -- operations on different-shaped arrays
   Reshaping -- change array dimensions without copying
   Aggregation -- sum, mean, std, min, max along axes
   Boolean indexing -- filter with conditions
""")

print(" All examples completed successfully!")
