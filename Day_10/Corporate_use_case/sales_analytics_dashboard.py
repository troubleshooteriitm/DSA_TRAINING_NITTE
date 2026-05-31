"""
Enterprise Sales & Customer Analytics Dashboard
================================================

A comprehensive sales analytics dashboard that demonstrates real-world
Pandas usage for business intelligence:

- Sample data generation (50+ rows)
- Data cleaning & type fixing
- Monthly sales trends analysis
- Top products & regional comparisons
- Sales representative performance metrics
- Customer data merging
- Formatted dashboard output

Requirements:
    pip install pandas numpy
"""

import sys
import random
from datetime import datetime, timedelta

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("=" * 60)
    print("ERROR: Required libraries not installed.")
    print("Please run: pip install pandas numpy")
    print("=" * 60)
    sys.exit(1)


#  Configuration 

random.seed(42)
np.random.seed(42)

PRODUCTS = {
    'Laptop Pro': ('Electronics', 1299.99),
    'Wireless Mouse': ('Electronics', 29.99),
    'USB-C Hub': ('Electronics', 49.99),
    'Standing Desk': ('Furniture', 599.99),
    'Ergonomic Chair': ('Furniture', 449.99),
    'Monitor 27"': ('Electronics', 349.99),
    'Keyboard Mech': ('Electronics', 89.99),
    'Desk Lamp': ('Furniture', 39.99),
    'Webcam HD': ('Electronics', 69.99),
    'Cable Kit': ('Accessories', 19.99),
}

REGIONS = ['North', 'South', 'East', 'West']
SALES_REPS = ['Alice Johnson', 'Bob Smith', 'Charlie Brown',
              'Diana Prince', 'Eve Williams', 'Frank Miller']


#  Step 1: Generate Sample Sales Data (60 rows) 

def generate_sales_data(num_rows: int = 60) -> pd.DataFrame:
    """Generate realistic sales data with intentional data quality issues."""
    start_date = datetime(2024, 1, 1)
    records = []

    for i in range(num_rows):
        product = random.choice(list(PRODUCTS.keys()))
        category, unit_price = PRODUCTS[product]
        quantity = random.randint(1, 15)

        record = {
            'order_id': f'ORD-{1000 + i}',
            'date': (start_date + timedelta(days=random.randint(0, 364))
                     ).strftime('%Y-%m-%d'),
            'product': product,
            'category': category,
            'region': random.choice(REGIONS),
            'sales_rep': random.choice(SALES_REPS),
            'quantity': quantity,
            'unit_price': unit_price,
            'total': round(quantity * unit_price, 2),
        }
        records.append(record)

    df = pd.DataFrame(records)

    # Introduce data quality issues for cleaning demonstration
    # Add some NaN values
    nan_indices = random.sample(range(num_rows), 5)
    for idx in nan_indices[:3]:
        df.loc[idx, 'quantity'] = np.nan
    for idx in nan_indices[3:]:
        df.loc[idx, 'region'] = np.nan

    # Add duplicate rows
    df = pd.concat([df, df.iloc[[0, 5, 10]]], ignore_index=True)

    return df


def generate_customer_data() -> pd.DataFrame:
    """Generate customer data for merge demonstration."""
    return pd.DataFrame({
        'sales_rep': SALES_REPS,
        'territory': ['Northeast', 'Southeast', 'Midwest',
                       'Southwest', 'Northwest', 'Central'],
        'hire_date': ['2020-03-15', '2019-07-22', '2021-01-10',
                      '2018-11-05', '2022-06-18', '2020-09-01'],
        'quota': [150000, 180000, 120000, 200000, 140000, 160000],
    })


#  Step 2: Data Cleaning 

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the sales DataFrame: handle NaN, fix types, remove duplicates."""
    print("\n" + "=" * 60)
    print(" DATA CLEANING REPORT")
    print("=" * 60)

    print(f"\nOriginal shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    # Remove duplicate rows
    df = df.drop_duplicates()
    print(f"\nAfter removing duplicates: {df.shape}")

    # Fill missing quantities with median
    median_qty = df['quantity'].median()
    df['quantity'] = df['quantity'].fillna(median_qty)
    print(f"Filled missing quantities with median: {median_qty}")

    # Fill missing regions with 'Unknown'
    df['region'] = df['region'].fillna('Unknown')

    # Fix data types
    df['date'] = pd.to_datetime(df['date'])
    df['quantity'] = df['quantity'].astype(int)

    # Recalculate total after cleaning
    df['total'] = df['quantity'] * df['unit_price']
    df['total'] = df['total'].round(2)

    print(f"Final shape: {df.shape}")
    print(f"Remaining missing values: {df.isnull().sum().sum()}")

    return df


#  Step 3: Analysis Functions 

def monthly_sales_trends(df: pd.DataFrame) -> None:
    """Analyze and display monthly sales trends."""
    print("\n" + "=" * 60)
    print(" MONTHLY SALES TRENDS")
    print("=" * 60)

    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month').agg(
        revenue=('total', 'sum'),
        orders=('order_id', 'count'),
        avg_order=('total', 'mean')
    ).round(2)

    for month, row in monthly.iterrows():
        bar = '' * int(row['revenue'] / 5000)
        print(f"  {month} | ${row['revenue']:>12,.2f} | "
              f"{row['orders']:>3} orders | Avg: ${row['avg_order']:>8,.2f} "
              f"|{bar}")


def top_products_analysis(df: pd.DataFrame) -> None:
    """Analyze top-selling products by revenue and quantity."""
    print("\n" + "=" * 60)
    print(" TOP PRODUCTS BY REVENUE")
    print("=" * 60)

    product_stats = df.groupby('product').agg(
        total_revenue=('total', 'sum'),
        total_qty=('quantity', 'sum'),
        num_orders=('order_id', 'count'),
        avg_order_value=('total', 'mean')
    ).sort_values('total_revenue', ascending=False).round(2)

    for i, (product, row) in enumerate(product_stats.iterrows(), 1):
        medal = ['', '', ''][i - 1] if i <= 3 else f'  {i}.'
        print(f"  {medal} {product:<18} | Revenue: ${row['total_revenue']:>12,.2f} "
              f"| Qty: {row['total_qty']:>4} | Orders: {row['num_orders']:>3}")


def regional_comparison(df: pd.DataFrame) -> None:
    """Compare sales performance across regions."""
    print("\n" + "=" * 60)
    print(" REGIONAL COMPARISON")
    print("=" * 60)

    regional = df.groupby('region').agg(
        revenue=('total', 'sum'),
        orders=('order_id', 'count'),
        avg_order=('total', 'mean'),
        products_sold=('quantity', 'sum')
    ).sort_values('revenue', ascending=False).round(2)

    total_revenue = regional['revenue'].sum()

    for region, row in regional.iterrows():
        share = (row['revenue'] / total_revenue) * 100
        bar = '' * int(share / 2)
        print(f"  {region:<10} | ${row['revenue']:>12,.2f} "
              f"({share:>5.1f}%) | {row['orders']:>3} orders | "
              f"Avg: ${row['avg_order']:>8,.2f} |{bar}")


def sales_rep_performance(df: pd.DataFrame) -> None:
    """Evaluate individual sales representative performance."""
    print("\n" + "=" * 60)
    print(" SALES REP PERFORMANCE")
    print("=" * 60)

    rep_stats = df.groupby('sales_rep').agg(
        revenue=('total', 'sum'),
        orders=('order_id', 'count'),
        avg_deal=('total', 'mean'),
        products_sold=('quantity', 'sum')
    ).sort_values('revenue', ascending=False).round(2)

    for rep, row in rep_stats.iterrows():
        print(f"  {rep:<18} | Revenue: ${row['revenue']:>12,.2f} "
              f"| Orders: {row['orders']:>3} | Avg Deal: ${row['avg_deal']:>8,.2f}")


def category_breakdown(df: pd.DataFrame) -> None:
    """Break down sales by product category."""
    print("\n" + "=" * 60)
    print(" CATEGORY BREAKDOWN")
    print("=" * 60)

    category_stats = df.groupby('category').agg(
        revenue=('total', 'sum'),
        orders=('order_id', 'count'),
        unique_products=('product', 'nunique')
    ).sort_values('revenue', ascending=False).round(2)

    total = category_stats['revenue'].sum()

    for cat, row in category_stats.iterrows():
        pct = (row['revenue'] / total) * 100
        print(f"  {cat:<15} | ${row['revenue']:>12,.2f} ({pct:>5.1f}%) "
              f"| {row['orders']:>3} orders | {row['unique_products']} products")


#  Step 4: Merge Customer Data 

def merge_and_quota_analysis(sales_df: pd.DataFrame,
                             customer_df: pd.DataFrame) -> None:
    """Merge sales with customer data and analyze quota attainment."""
    print("\n" + "=" * 60)
    print(" MERGED DATA: QUOTA ATTAINMENT")
    print("=" * 60)

    # Aggregate sales per rep
    rep_revenue = sales_df.groupby('sales_rep').agg(
        total_revenue=('total', 'sum')
    ).reset_index()

    # Merge with customer data
    merged = pd.merge(rep_revenue, customer_df, on='sales_rep', how='left')
    merged['quota_pct'] = ((merged['total_revenue'] / merged['quota']) * 100
                           ).round(1)
    merged['status'] = merged['quota_pct'].apply(
        lambda x: ' On Track' if x >= 80 else ' At Risk' if x >= 50
        else ' Behind'
    )

    for _, row in merged.iterrows():
        print(f"  {row['sales_rep']:<18} | Territory: {row['territory']:<12} "
              f"| Revenue: ${row['total_revenue']:>10,.2f} "
              f"| Quota: ${row['quota']:>10,} "
              f"| {row['quota_pct']:>5.1f}% | {row['status']}")


#  Step 5: Executive Summary 

def executive_summary(df: pd.DataFrame) -> None:
    """Print executive summary dashboard."""
    print("\n" + "=" * 60)
    print(" EXECUTIVE SUMMARY")
    print("=" * 60)

    total_revenue = df['total'].sum()
    total_orders = len(df)
    avg_order = df['total'].mean()
    total_qty = df['quantity'].sum()
    unique_products = df['product'].nunique()
    unique_regions = df['region'].nunique()
    date_range = f"{df['date'].min().date()} to {df['date'].max().date()}"

    print(f"""
    Period:              {date_range}
    Total Revenue:       ${total_revenue:>12,.2f}
    Total Orders:        {total_orders:>12}
    Average Order Value: ${avg_order:>12,.2f}
    Total Units Sold:    {total_qty:>12}
    Unique Products:     {unique_products:>12}
    Active Regions:      {unique_regions:>12}
    """)

    # Top performer
    top_rep = df.groupby('sales_rep')['total'].sum().idxmax()
    top_rev = df.groupby('sales_rep')['total'].sum().max()
    print(f"     Top Performer:  {top_rep} (${top_rev:,.2f})")

    # Best product
    top_product = df.groupby('product')['total'].sum().idxmax()
    top_prod_rev = df.groupby('product')['total'].sum().max()
    print(f"     Best Product:   {top_product} (${top_prod_rev:,.2f})")

    # Best region
    top_region = df.groupby('region')['total'].sum().idxmax()
    top_reg_rev = df.groupby('region')['total'].sum().max()
    print(f"     Best Region:    {top_region} (${top_reg_rev:,.2f})")


#  Main Execution 

def main():
    """Run the complete sales analytics dashboard."""
    print("" + "" * 58 + "")
    print("" + " ENTERPRISE SALES ANALYTICS DASHBOARD ".center(58) + "")
    print("" + "" * 58 + "")

    # Generate data
    sales_df = generate_sales_data(60)
    customer_df = generate_customer_data()

    # Clean data
    sales_df = clean_data(sales_df)

    # Run all analyses
    executive_summary(sales_df)
    monthly_sales_trends(sales_df)
    top_products_analysis(sales_df)
    regional_comparison(sales_df)
    sales_rep_performance(sales_df)
    category_breakdown(sales_df)
    merge_and_quota_analysis(sales_df, customer_df)

    print("\n" + "=" * 60)
    print(" Dashboard generation complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
