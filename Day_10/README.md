# Day 10 -- NumPy, Pandas & Data Analytics

> **Prerequisites:** Python basics (Days 1-9)
> **Install required packages:**
> ```bash
> pip install numpy pandas
> ```

---

## Table of Contents

1. [NumPy Arrays](#1-numpy-arrays)
2. [Indexing & Slicing](#2-indexing--slicing)
3. [Broadcasting](#3-broadcasting)
4. [Array Operations](#4-array-operations)
5. [Reshaping](#5-reshaping)
6. [Pandas DataFrames](#6-pandas-dataframes)
7. [Data Cleaning](#7-data-cleaning)
8. [Aggregation](#8-aggregation)
9. [Filtering](#9-filtering)
10. [GroupBy](#10-groupby)
11. [Merging](#11-merging)
12. [ETL Processing](#12-etl-processing)
13. [Practice Exercises](#13-practice-exercises)

---

## 1. NumPy Arrays

NumPy (Numerical Python) is the foundation of scientific computing in Python.
It provides high-performance multidimensional array objects and tools for working with them.

### Why NumPy?

- **Speed:** NumPy operations are implemented in C, making them 10-100x faster than pure Python lists.
- **Memory Efficiency:** NumPy arrays use contiguous memory blocks.
- **Vectorized Operations:** Apply operations to entire arrays without explicit loops.

### Creating Arrays

```python
import numpy as np

# From a Python list
arr = np.array([1, 2, 3, 4, 5])
print(arr)          # [1 2 3 4 5]
print(type(arr))    # <class 'numpy.ndarray'>

# 2D array (matrix)
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]

# Zeros -- creates array filled with 0s
zeros = np.zeros((3, 4))       # 3 rows, 4 columns of zeros
print(zeros)

# Ones -- creates array filled with 1s
ones = np.ones((2, 3))         # 2 rows, 3 columns of ones
print(ones)

# arange -- like Python's range() but returns an ndarray
sequence = np.arange(0, 20, 2)  # start=0, stop=20, step=2
print(sequence)                  # [ 0  2  4  6  8 10 12 14 16 18]

# linspace -- evenly spaced numbers over an interval
linear = np.linspace(0, 1, 5)  # 5 numbers from 0 to 1 (inclusive)
print(linear)                   # [0.   0.25 0.5  0.75 1.  ]

# Identity matrix
identity = np.eye(3)
print(identity)

# Random arrays
random_arr = np.random.rand(3, 3)      # Uniform [0, 1)
random_int = np.random.randint(1, 100, size=(3, 4))  # Random integers
```

### Array Properties

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)    # (2, 3) -- 2 rows, 3 columns
print(arr.ndim)     # 2 -- number of dimensions
print(arr.size)     # 6 -- total elements
print(arr.dtype)    # int64 -- data type
print(arr.itemsize) # 8 -- bytes per element
```

---

## 2. Indexing & Slicing

### Basic Indexing

```python
arr = np.array([10, 20, 30, 40, 50])

# Single element access (0-indexed)
print(arr[0])    # 10
print(arr[-1])   # 50

# 2D array indexing: arr[row, col]
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[0, 0])   # 1 (first row, first col)
print(matrix[1, 2])   # 6 (second row, third col)
print(matrix[-1, -1]) # 9 (last row, last col)
```

### Slicing

```python
arr = np.array([10, 20, 30, 40, 50, 60, 70])

print(arr[1:4])      # [20 30 40] -- elements at index 1, 2, 3
print(arr[:3])       # [10 20 30] -- first 3 elements
print(arr[4:])       # [50 60 70] -- from index 4 to end
print(arr[::2])      # [10 30 50 70] -- every other element

# 2D slicing
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[:2, :2])   # [[1 2] [4 5]] -- top-left 2x2
print(matrix[1:, :])    # [[4 5 6] [7 8 9]] -- rows 1 and 2
print(matrix[:, 1])     # [2 5 8] -- entire second column
```

### Fancy Indexing

```python
arr = np.array([10, 20, 30, 40, 50])

# Index with a list of indices
indices = [0, 2, 4]
print(arr[indices])   # [10 30 50]

# 2D fancy indexing
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
rows = [0, 2]
cols = [1, 2]
print(matrix[rows, cols])  # [2 9] -- elements at (0,1) and (2,2)
```

### Boolean Indexing

```python
arr = np.array([15, 22, 8, 31, 42, 5, 19])

# Create boolean mask
mask = arr > 20
print(mask)          # [False  True False  True  True False False]

# Apply mask to filter
print(arr[mask])     # [22 31 42]

# One-liner
print(arr[arr > 20])          # [22 31 42]
print(arr[(arr > 10) & (arr < 30)])  # [15 22 19]
```

---

## 3. Broadcasting

Broadcasting allows NumPy to perform operations on arrays of different shapes.
Instead of copying data, NumPy "broadcasts" the smaller array to match the larger one.

### Broadcasting Rules

1. If arrays have different numbers of dimensions, the shape of the smaller array is padded with 1s on the left.
2. Arrays with size 1 along a dimension act as if they have the size of the largest array in that dimension.
3. If sizes don't match and neither is 1, an error is raised.

### Examples

```python
import numpy as np

# Scalar + Array: scalar is broadcast to every element
arr = np.array([1, 2, 3, 4])
print(arr + 10)    # [11 12 13 14]
print(arr * 3)     # [ 3  6  9 12]

# 1D + 2D: row vector broadcast across rows
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
row = np.array([10, 20, 30])
print(matrix + row)
# [[11 22 33]
#  [14 25 36]
#  [17 28 39]]

# Column vector + 2D: column broadcast across columns
col = np.array([[100], [200], [300]])
print(matrix + col)
# [[101 102 103]
#  [204 205 206]
#  [307 308 309]]

# Outer product via broadcasting
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(a[:, np.newaxis] * b)
# [[ 10  20  30]
#  [ 20  40  60]
#  [ 30  60  90]]
```

---

## 4. Array Operations

### Arithmetic Operations (Element-wise)

```python
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

print(a + b)    # [ 6  8 10 12]
print(a - b)    # [-4 -4 -4 -4]
print(a * b)    # [ 5 12 21 32]
print(a / b)    # [0.2  0.333  0.4286  0.5]
print(a ** 2)   # [ 1  4  9 16]
print(np.sqrt(a))  # [1.  1.414  1.732  2.]
```

### Aggregation Functions

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Global aggregation
print(np.sum(arr))     # 45
print(np.mean(arr))    # 5.0
print(np.std(arr))     # 2.581988...
print(np.min(arr))     # 1
print(np.max(arr))     # 9

# Axis-based aggregation
# axis=0  along rows (column-wise operation)
# axis=1  along columns (row-wise operation)
print(np.sum(arr, axis=0))   # [12 15 18] -- sum of each column
print(np.sum(arr, axis=1))   # [ 6 15 24] -- sum of each row
print(np.mean(arr, axis=0))  # [4. 5. 6.] -- mean of each column
print(np.mean(arr, axis=1))  # [2. 5. 8.] -- mean of each row

# Other useful aggregations
print(np.median(arr))        # 5.0
print(np.var(arr))           # 6.666... (variance)
print(np.cumsum(arr))        # [ 1  3  6 10 15 21 28 36 45]
print(np.argmax(arr))        # 8 (index of max element in flattened array)
print(np.argmin(arr))        # 0
```

### Matrix Operations

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# Matrix multiplication
print(np.dot(a, b))       # [[19 22] [43 50]]
print(a @ b)              # Same as np.dot for 2D arrays

# Transpose
print(a.T)                # [[1 3] [2 4]]

# Determinant and inverse
print(np.linalg.det(a))   # -2.0
print(np.linalg.inv(a))   # [[-2.   1. ] [ 1.5 -0.5]]
```

---

## 5. Reshaping

```python
arr = np.arange(12)  # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# reshape -- returns a new view with specified shape
reshaped = arr.reshape(3, 4)
print(reshaped)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Use -1 to auto-calculate one dimension
print(arr.reshape(2, -1))     # shape (2, 6)
print(arr.reshape(-1, 3))     # shape (4, 3)

# ravel -- flattens to 1D (returns a view when possible)
flat = reshaped.ravel()
print(flat)  # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# flatten -- always returns a copy
flat_copy = reshaped.flatten()
print(flat_copy)

# transpose -- swaps axes
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix.shape)       # (2, 3)
print(matrix.T.shape)     # (3, 2)
print(matrix.transpose()) # Same as .T

# Stacking arrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.vstack([a, b]))    # [[1 2 3] [4 5 6]] -- vertical stack
print(np.hstack([a, b]))    # [1 2 3 4 5 6] -- horizontal stack
print(np.column_stack([a, b]))  # [[1 4] [2 5] [3 6]]
```

---

## 6. Pandas DataFrames

Pandas is the go-to library for data manipulation and analysis.
It provides two primary data structures: **Series** (1D) and **DataFrame** (2D).

### Creating DataFrames

```python
import pandas as pd

# From a dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Age': [25, 30, 35, 28],
    'City': ['NYC', 'LA', 'Chicago', 'Houston'],
    'Salary': [70000, 80000, 90000, 75000]
}
df = pd.DataFrame(data)
print(df)
#       Name  Age     City  Salary
# 0    Alice   25      NYC   70000
# 1      Bob   30       LA   80000
# 2  Charlie   35  Chicago   90000
# 3    Diana   28  Houston   75000

# From a list of lists
data_list = [
    ['Alice', 25, 'NYC'],
    ['Bob', 30, 'LA'],
    ['Charlie', 35, 'Chicago']
]
df2 = pd.DataFrame(data_list, columns=['Name', 'Age', 'City'])

# From a CSV file
# df = pd.read_csv('data.csv')
# df = pd.read_csv('data.csv', sep=';', encoding='utf-8')

# Quick exploration
print(df.head())       # First 5 rows
print(df.tail(3))      # Last 3 rows
print(df.info())       # Column types and non-null counts
print(df.describe())   # Statistical summary
print(df.shape)        # (rows, columns)
print(df.columns)      # Column names
print(df.dtypes)       # Data types
```

### Accessing Data

```python
# Single column (returns Series)
print(df['Name'])
print(df.Name)        # Dot notation (if no spaces in name)

# Multiple columns (returns DataFrame)
print(df[['Name', 'Salary']])

# Row access with .loc (label-based) and .iloc (position-based)
print(df.loc[0])         # First row by label
print(df.iloc[0])        # First row by position
print(df.loc[0:2, 'Name':'City'])   # Rows 0-2, columns Name to City
print(df.iloc[0:2, 0:3])            # Same but by position
```

---

## 7. Data Cleaning

Real-world data is messy. Pandas provides powerful tools to clean it.

### Handling Missing Values (NaN)

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [np.nan, 2, 3, 4],
    'C': [1, np.nan, np.nan, 4]
})

# Detect missing values
print(df.isnull())           # Boolean mask of NaN
print(df.isnull().sum())     # Count NaN per column
print(df.isnull().sum().sum())  # Total NaN count

# dropna -- remove rows/columns with NaN
df_dropped = df.dropna()              # Drop rows with ANY NaN
df_dropped_cols = df.dropna(axis=1)   # Drop columns with ANY NaN
df_thresh = df.dropna(thresh=2)       # Keep rows with at least 2 non-NaN

# fillna -- replace NaN with a value
df_filled = df.fillna(0)                 # Fill with 0
df_filled_mean = df.fillna(df.mean())    # Fill with column mean
df_filled_ffill = df.fillna(method='ffill')  # Forward fill
df_filled_bfill = df.fillna(method='bfill')  # Backward fill
```

### Handling Duplicates

```python
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],
    'Score': [85, 90, 85, 95, 90]
})

# Check for duplicates
print(df.duplicated())                # Boolean mask
print(df.duplicated().sum())          # Count duplicates

# Remove duplicates
df_unique = df.drop_duplicates()                    # Remove all duplicates
df_unique2 = df.drop_duplicates(subset='Name')      # Based on 'Name' column
df_unique3 = df.drop_duplicates(keep='last')        # Keep last occurrence
```

### Data Type Conversion

```python
df['Age'] = df['Age'].astype(int)
df['Salary'] = df['Salary'].astype(float)
df['Date'] = pd.to_datetime(df['Date'])
df['Category'] = df['Category'].astype('category')
```

---

## 8. Aggregation

```python
df = pd.DataFrame({
    'Product': ['A', 'B', 'A', 'B', 'A'],
    'Sales': [100, 200, 150, 250, 300],
    'Quantity': [10, 20, 15, 25, 30]
})

# Basic aggregation
print(df['Sales'].sum())       # 1000
print(df['Sales'].mean())      # 200.0
print(df['Sales'].count())     # 5
print(df['Sales'].min())       # 100
print(df['Sales'].max())       # 300
print(df['Sales'].std())       # Standard deviation

# describe() -- comprehensive statistics
print(df.describe())
#            Sales   Quantity
# count    5.0000    5.00000
# mean   200.0000   20.00000
# std     79.0569    7.90569
# min    100.0000   10.00000
# 25%    150.0000   15.00000
# 50%    200.0000   20.00000
# 75%    250.0000   25.00000
# max    300.0000   30.00000

# Multiple aggregations
print(df[['Sales', 'Quantity']].agg(['sum', 'mean', 'max']))
```

---

## 9. Filtering

### Boolean Indexing

```python
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'Age': [25, 30, 35, 28, 22],
    'Salary': [70000, 80000, 90000, 75000, 65000],
    'Dept': ['Engineering', 'Marketing', 'Engineering', 'HR', 'Marketing']
})

# Single condition
print(df[df['Age'] > 28])

# Multiple conditions (use & for AND, | for OR)
print(df[(df['Age'] > 25) & (df['Salary'] > 70000)])
print(df[(df['Dept'] == 'Engineering') | (df['Dept'] == 'Marketing')])

# isin() for multiple values
print(df[df['Dept'].isin(['Engineering', 'HR'])])

# String methods
print(df[df['Name'].str.startswith('A')])
print(df[df['Name'].str.contains('li')])
```

### Query Method

```python
# query() -- SQL-like filtering syntax
print(df.query('Age > 28'))
print(df.query('Age > 25 and Salary > 70000'))
print(df.query('Dept == "Engineering"'))

# Variables in query
min_age = 25
print(df.query('Age > @min_age'))
```

---

## 10. GroupBy

GroupBy follows the **split-apply-combine** pattern:
1. **Split** the data into groups
2. **Apply** a function to each group
3. **Combine** the results

```python
df = pd.DataFrame({
    'Dept': ['Eng', 'Mkt', 'Eng', 'HR', 'Mkt', 'Eng', 'HR'],
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace'],
    'Salary': [90000, 70000, 85000, 75000, 72000, 95000, 78000],
    'Years': [5, 3, 4, 6, 2, 8, 7]
})

# Basic groupby
grouped = df.groupby('Dept')
print(grouped['Salary'].mean())
# Dept
# Eng    90000.0
# HR     76500.0
# Mkt    71000.0

# Multiple aggregations with agg()
print(grouped['Salary'].agg(['mean', 'min', 'max', 'count']))

# Custom aggregation per column
print(grouped.agg({
    'Salary': ['mean', 'sum'],
    'Years': ['min', 'max']
}))

# Named aggregation (cleaner output)
result = grouped.agg(
    avg_salary=('Salary', 'mean'),
    total_salary=('Salary', 'sum'),
    headcount=('Name', 'count'),
    max_years=('Years', 'max')
)
print(result)

# transform -- returns same-shaped result (useful for adding group stats)
df['dept_avg_salary'] = grouped['Salary'].transform('mean')
df['salary_vs_avg'] = df['Salary'] - df['dept_avg_salary']
print(df)

# filter -- filter groups based on a condition
high_salary_depts = grouped.filter(lambda x: x['Salary'].mean() > 75000)
print(high_salary_depts)
```

---

## 11. Merging

### merge() -- SQL-style joins

```python
# Employee table
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'dept_id': [101, 102, 101, 103, 102]
})

# Department table
departments = pd.DataFrame({
    'dept_id': [101, 102, 103, 104],
    'dept_name': ['Engineering', 'Marketing', 'HR', 'Finance']
})

# Inner join (default) -- only matching rows
merged = pd.merge(employees, departments, on='dept_id')
print(merged)

# Left join -- all from left, matching from right
left_merged = pd.merge(employees, departments, on='dept_id', how='left')

# Right join -- all from right, matching from left
right_merged = pd.merge(employees, departments, on='dept_id', how='right')

# Outer join -- all from both
outer_merged = pd.merge(employees, departments, on='dept_id', how='outer')

# Merge on different column names
salaries = pd.DataFrame({
    'employee_id': [1, 2, 3, 4, 5],
    'salary': [90000, 70000, 85000, 75000, 72000]
})
merged = pd.merge(employees, salaries, left_on='emp_id', right_on='employee_id')
```

### join() -- Index-based merging

```python
df1 = pd.DataFrame({'A': [1, 2, 3]}, index=['a', 'b', 'c'])
df2 = pd.DataFrame({'B': [4, 5, 6]}, index=['a', 'b', 'd'])

print(df1.join(df2, how='inner'))   # Only matching indices
print(df1.join(df2, how='outer'))   # All indices
```

### concat() -- Stacking DataFrames

```python
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

# Vertical concatenation (stacking rows)
combined = pd.concat([df1, df2], ignore_index=True)
print(combined)

# Horizontal concatenation (adding columns)
combined_h = pd.concat([df1, df2], axis=1)
print(combined_h)
```

---

## 12. ETL Processing

**ETL** stands for **Extract, Transform, Load** -- a common data pipeline pattern.

### Conceptual Overview

```
          
 EXTRACT      TRANSFORM        LOAD   
                                            
 CSV/DB/        Clean, Join,       DB/CSV/  
 API/JSON       Aggregate          Report   
          
```

### Example ETL Pipeline

```python
import pandas as pd

#  EXTRACT 
# Read from multiple sources
sales_df = pd.read_csv('sales.csv')
customer_df = pd.read_csv('customers.csv')

#  TRANSFORM 
# 1. Clean data
sales_df = sales_df.dropna(subset=['amount'])
sales_df['date'] = pd.to_datetime(sales_df['date'])
sales_df['amount'] = sales_df['amount'].astype(float)

# 2. Join tables
merged = pd.merge(sales_df, customer_df, on='customer_id', how='left')

# 3. Create derived columns
merged['month'] = merged['date'].dt.month
merged['year'] = merged['date'].dt.year

# 4. Aggregate
monthly_summary = merged.groupby(['year', 'month']).agg(
    total_sales=('amount', 'sum'),
    avg_sale=('amount', 'mean'),
    num_transactions=('amount', 'count')
).reset_index()

#  LOAD 
monthly_summary.to_csv('monthly_report.csv', index=False)
print("ETL pipeline complete!")
```

---

## 13. Practice Exercises

1. **NumPy Basics** -- See `practice/numpy_basics.py`
2. **Pandas ETL** -- See `practice/pandas_etl.py`
3. **LeetCode 53** -- Maximum Subarray  `official_questions/01_maximum_subarray.py`
4. **LeetCode 121** -- Best Time to Buy and Sell Stock  `official_questions/02_best_time_to_buy_sell_stock.py`
5. **Corporate Use Case** -- Sales Analytics Dashboard  `Corporate_use_case/sales_analytics_dashboard.py`

---

## Key Takeaways

| Concept | NumPy | Pandas |
|---------|-------|--------|
| Primary Data Structure | ndarray | DataFrame / Series |
| Best For | Numerical computation | Data manipulation & analysis |
| Speed | Very fast (C-backed) | Fast (built on NumPy) |
| Missing Data | Limited (NaN) | Rich support (dropna, fillna) |
| File I/O | np.load, np.save | read_csv, to_csv, read_excel |
| Grouping | Not built-in | groupby, pivot_table |

> **Next:** Day 11 -- Matplotlib, Data Science & Scikit-Learn
