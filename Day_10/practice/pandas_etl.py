"""
Pandas ETL Practice -- DataFrame Operations & Pipeline
======================================================

Covers:
    - DataFrame creation (from dict, list)
    - Data cleaning (NaN handling, type conversion, duplicates)
    - Filtering (boolean indexing, query)
    - GroupBy (agg, transform)
    - Merging (merge, concat)
    - Simple ETL pipeline

Requirements:
    pip install pandas numpy
"""

import sys

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("=" * 50)
    print("Pandas/NumPy is not installed.")
    print("Install with: pip install pandas numpy")
    print("=" * 50)
    sys.exit(1)


def section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'' * 55}")
    print(f"  {title}")
    print(f"{'' * 55}")


#  1. DataFrame Creation 

section("1. DataFrame Creation")

# From a dictionary
employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve',
             'Frank', 'Grace', 'Hank'],
    'department': ['Engineering', 'Marketing', 'Engineering', 'HR',
                   'Marketing', 'Engineering', 'HR', 'Marketing'],
    'salary': [95000, 72000, 88000, 78000, 71000, 92000, 76000, 69000],
    'years_exp': [5, 3, 4, 6, 2, 7, 5, 1],
    'rating': [4.5, 3.8, 4.2, 4.0, 3.5, 4.8, 4.1, 3.2],
})

print("Employee DataFrame:")
print(employees)
print(f"\nShape: {employees.shape}")
print(f"Columns: {list(employees.columns)}")
print(f"Dtypes:\n{employees.dtypes}")

# From a list of dicts
projects = pd.DataFrame([
    {'project_id': 'P001', 'name': 'Alpha', 'department': 'Engineering', 'budget': 50000},
    {'project_id': 'P002', 'name': 'Beta', 'department': 'Marketing', 'budget': 30000},
    {'project_id': 'P003', 'name': 'Gamma', 'department': 'HR', 'budget': 20000},
    {'project_id': 'P004', 'name': 'Delta', 'department': 'Engineering', 'budget': 45000},
])
print(f"\nProjects DataFrame:\n{projects}")


#  2. Data Cleaning 

section("2. Data Cleaning")

# Create messy data
messy = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', None, 'Eve', 'Alice', 'Bob'],
    'score': [85, np.nan, 92, 78, np.nan, 85, 88],
    'grade': ['A', 'B', 'A', 'C', None, 'A', 'B'],
    'date': ['2024-01-15', '2024-02-20', '2024-01-15',
             '2024-03-10', '2024-04-05', '2024-01-15', '2024-02-20'],
})

print("Messy data:")
print(messy)
print(f"\nMissing values:\n{messy.isnull().sum()}")

# Fill NaN with appropriate values
cleaned = messy.copy()
cleaned['score'] = cleaned['score'].fillna(cleaned['score'].mean())
cleaned['name'] = cleaned['name'].fillna('Unknown')
cleaned['grade'] = cleaned['grade'].fillna('N/A')
print(f"\nAfter fillna:\n{cleaned}")

# Remove duplicates
print(f"\nDuplicates: {cleaned.duplicated().sum()}")
cleaned = cleaned.drop_duplicates()
print(f"After drop_duplicates:\n{cleaned}")

# Type conversion
cleaned['date'] = pd.to_datetime(cleaned['date'])
print(f"\nDtypes after conversion:\n{cleaned.dtypes}")


#  3. Filtering 

section("3. Filtering")

print("Original employees:")
print(employees[['name', 'department', 'salary', 'rating']])

# Boolean indexing
high_salary = employees[employees['salary'] > 80000]
print(f"\nSalary > $80,000:\n{high_salary[['name', 'salary']]}")

# Multiple conditions
eng_experienced = employees[
    (employees['department'] == 'Engineering') &
    (employees['years_exp'] >= 4)
]
print(f"\nEngineering + 4+ years exp:\n{eng_experienced[['name', 'years_exp']]}")

# isin()
target_depts = ['Engineering', 'HR']
filtered = employees[employees['department'].isin(target_depts)]
print(f"\nIn {target_depts}:\n{filtered[['name', 'department']]}")

# query() method
result = employees.query('salary > 75000 and rating >= 4.0')
print(f"\nquery('salary > 75k and rating >= 4.0'):\n{result[['name', 'salary', 'rating']]}")

# String filtering
a_names = employees[employees['name'].str.startswith('A')]
print(f"\nNames starting with 'A':\n{a_names[['name']]}")


#  4. GroupBy 

section("4. GroupBy")

# Basic groupby
dept_stats = employees.groupby('department')['salary'].agg(
    ['mean', 'min', 'max', 'count']
).round(2)
print(f"Salary stats by department:\n{dept_stats}")

# Named aggregation
dept_summary = employees.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    total_salary=('salary', 'sum'),
    headcount=('name', 'count'),
    avg_rating=('rating', 'mean'),
    avg_experience=('years_exp', 'mean'),
).round(2)
print(f"\nDepartment summary:\n{dept_summary}")

# Transform -- add group-level stats back to original
employees['dept_avg_salary'] = employees.groupby('department')['salary'].transform('mean')
employees['salary_vs_dept_avg'] = (employees['salary'] - employees['dept_avg_salary']).round(2)
print(f"\nWith department average comparison:")
print(employees[['name', 'department', 'salary', 'dept_avg_salary',
                 'salary_vs_dept_avg']])

# Clean up temp columns
employees.drop(columns=['dept_avg_salary', 'salary_vs_dept_avg'], inplace=True)


#  5. Merging 

section("5. Merging")

# Inner merge
merged = pd.merge(employees, projects,
                  left_on='department', right_on='department',
                  suffixes=('_emp', '_proj'))
print(f"Inner merge (employees + projects):")
print(merged[['name_emp', 'department', 'salary', 'name_proj', 'budget']].head(8))

# Left merge
dept_info = pd.DataFrame({
    'department': ['Engineering', 'Marketing', 'HR', 'Finance'],
    'location': ['Building A', 'Building B', 'Building C', 'Building D'],
    'manager': ['Dr. Smith', 'Ms. Lee', 'Mr. Patel', 'Ms. Garcia'],
})

left_merged = pd.merge(employees, dept_info, on='department', how='left')
print(f"\nLeft merge (employees + dept_info):")
print(left_merged[['name', 'department', 'location', 'manager']])

# Concat
q1 = pd.DataFrame({'month': ['Jan', 'Feb', 'Mar'], 'revenue': [100, 120, 110]})
q2 = pd.DataFrame({'month': ['Apr', 'May', 'Jun'], 'revenue': [130, 140, 125]})
yearly = pd.concat([q1, q2], ignore_index=True)
print(f"\nConcatenated Q1 + Q2:\n{yearly}")


#  6. Simple ETL Pipeline 

section("6. ETL Pipeline Example")

#  EXTRACT 
print("Step 1: EXTRACT -- Loading raw data")
raw_sales = pd.DataFrame({
    'date': ['2024-01-15', '2024-01-20', '2024-02-10', '2024-02-28',
             '2024-03-05', '2024-03-15', '2024-01-15', None,
             '2024-04-10', '2024-04-22'],
    'product': ['Widget A', 'Widget B', 'Widget A', 'Widget C',
                'Widget B', 'Widget A', 'Widget A', 'Widget B',
                'Widget C', 'Widget A'],
    'quantity': [10, np.nan, 8, 15, 12, 20, 10, 5, 18, 7],
    'price': [25.0, 35.0, 25.0, 45.0, 35.0, 25.0, 25.0, 35.0, 45.0, 25.0],
    'region': ['North', 'South', 'North', 'East', 'West',
               'North', 'North', None, 'East', 'South'],
})
print(f"  Raw records: {len(raw_sales)}")
print(f"  Missing values: {raw_sales.isnull().sum().sum()}")

#  TRANSFORM 
print("\nStep 2: TRANSFORM -- Cleaning & enriching")
# Clean
transformed = raw_sales.copy()
transformed = transformed.dropna(subset=['date'])       # Drop rows without date
transformed['quantity'] = transformed['quantity'].fillna(
    transformed['quantity'].median()
)
transformed['region'] = transformed['region'].fillna('Unknown')
transformed = transformed.drop_duplicates()

# Enrich
transformed['date'] = pd.to_datetime(transformed['date'])
transformed['revenue'] = transformed['quantity'] * transformed['price']
transformed['month'] = transformed['date'].dt.strftime('%Y-%m')

print(f"  Cleaned records: {len(transformed)}")
print(f"  Missing values: {transformed.isnull().sum().sum()}")

# Aggregate
monthly_report = transformed.groupby('month').agg(
    total_revenue=('revenue', 'sum'),
    total_quantity=('quantity', 'sum'),
    num_orders=('product', 'count'),
    avg_order_value=('revenue', 'mean'),
).round(2)

product_report = transformed.groupby('product').agg(
    total_revenue=('revenue', 'sum'),
    total_quantity=('quantity', 'sum'),
).sort_values('total_revenue', ascending=False).round(2)

#  LOAD 
print("\nStep 3: LOAD -- Generating reports")

print(f"\n   Monthly Report:")
for month, row in monthly_report.iterrows():
    print(f"    {month}: Revenue=${row['total_revenue']:>8,.2f} | "
          f"Qty={row['total_quantity']:>4.0f} | "
          f"Orders={row['num_orders']:>2} | "
          f"Avg=${row['avg_order_value']:>7,.2f}")

print(f"\n   Product Report:")
for product, row in product_report.iterrows():
    print(f"    {product}: Revenue=${row['total_revenue']:>8,.2f} | "
          f"Qty={row['total_quantity']:>4.0f}")

print("\n   ETL pipeline complete!")


#  Summary 

section("Summary")
print("""
  Pandas Key Concepts:
   DataFrame -- 2D labeled data structure
   Data cleaning -- fillna, dropna, drop_duplicates
   Filtering -- boolean indexing, query, isin
   GroupBy -- split-apply-combine pattern
   Merging -- merge (SQL joins), concat (stacking)
   ETL -- Extract, Transform, Load pipeline
""")

print(" All examples completed successfully!")
