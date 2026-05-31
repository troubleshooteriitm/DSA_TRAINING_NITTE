"""
Excel Report Automation -- Migrating from VBA to Python
=======================================================

Corporate Use Case: Replacing VBA Macros with Python for Excel Reporting

Context:
    Many enterprises rely on VBA (Visual Basic for Applications) macros embedded
    inside Excel workbooks to generate recurring reports -- sales summaries,
    monthly breakdowns, top performers, etc. While VBA works, it has significant
    drawbacks that Python can address.

VBA vs Python -- Why Migrate?

| Aspect              | VBA (Legacy)                | Python (Modern)           |
||||
| Portability         | Tied to MS Office           | Runs anywhere             |
| Version Control     | Embedded in .xlsm files     | Plain .py files (Git)     |
| Testing             | Manual / fragile            | unittest, pytest          |
| Readability         | Verbose, dated syntax       | Clean, expressive syntax  |
| Libraries           | Limited to Office objects   | 400,000+ on PyPI          |
| Automation          | Requires Excel open         | Runs headless (cron/CI)   |
| Scalability         | Struggles with large data   | Handles millions of rows  |
| Collaboration       | One macro, one workbook     | Shared repos, code review |
| Scheduling          | Task Scheduler + Excel      | cron, Airflow, CI/CD      |
| Error Handling      | On Error GoTo...            | try/except, logging       |


This Script Demonstrates:
    1. Reading sales data from an embedded CSV (simulating an Excel export)
    2. Computing total sales per region
    3. Calculating the average sale amount
    4. Identifying the top 3 performers by total revenue
    5. Breaking down sales by month
    6. Writing the summary report to a new CSV file

Dependencies:
    - Python 3.6+ (uses f-strings)
    - Standard library ONLY: csv, io, os, collections
    - NO external packages required (no openpyxl, pandas, etc.)

Usage:
    python excel_report_automation.py

    The script prints a formatted report to the console and writes
    a summary CSV file to the same directory.
"""

import csv
import os
from collections import defaultdict
from io import StringIO

# 
# 1. EMBEDDED SAMPLE DATA (simulates reading an exported Excel file)
# 
RAW_CSV_DATA = """\
Date,Region,Salesperson,Product,Quantity,Unit_Price,Total_Sale
2025-01-05,North,Alice Johnson,Widget A,50,29.99,1499.50
2025-01-12,South,Bob Smith,Widget B,30,49.99,1499.70
2025-01-18,East,Carol Davis,Widget A,45,29.99,1349.55
2025-01-25,West,David Lee,Widget C,20,99.99,1999.80
2025-02-03,North,Alice Johnson,Widget B,60,49.99,2999.40
2025-02-10,South,Eve Martinez,Widget A,35,29.99,1049.65
2025-02-17,East,Carol Davis,Widget C,25,99.99,2499.75
2025-02-22,West,Frank Wilson,Widget B,40,49.99,1999.60
2025-03-01,North,Alice Johnson,Widget C,15,99.99,1499.85
2025-03-08,South,Bob Smith,Widget A,55,29.99,1649.45
2025-03-15,East,Carol Davis,Widget B,70,49.99,3499.30
2025-03-21,West,David Lee,Widget A,25,29.99,749.75
2025-04-02,North,Eve Martinez,Widget B,45,49.99,2249.55
2025-04-09,South,Bob Smith,Widget C,10,99.99,999.90
2025-04-16,East,Frank Wilson,Widget A,80,29.99,2399.20
2025-04-23,West,David Lee,Widget B,35,49.99,1749.65
2025-05-01,North,Alice Johnson,Widget A,90,29.99,2699.10
2025-05-07,South,Eve Martinez,Widget C,20,99.99,1999.80
2025-05-14,East,Carol Davis,Widget B,55,49.99,2749.45
2025-05-20,West,Frank Wilson,Widget C,30,99.99,2999.70
"""


def read_sales_data(csv_string: str) -> list[dict]:
    """
    Parse the embedded CSV string into a list of dictionaries.

    Each dictionary represents one sales record with keys matching
    the CSV header: Date, Region, Salesperson, Product, Quantity,
    Unit_Price, Total_Sale.

    Args:
        csv_string: A string containing CSV-formatted sales data.

    Returns:
        A list of dictionaries, one per row.
    """
    reader = csv.DictReader(StringIO(csv_string))
    records = []
    for row in reader:
        # Convert numeric fields from strings to appropriate types
        row["Quantity"] = int(row["Quantity"])
        row["Unit_Price"] = float(row["Unit_Price"])
        row["Total_Sale"] = float(row["Total_Sale"])
        records.append(row)
    return records


def total_sales_per_region(records: list[dict]) -> dict[str, float]:
    """
    Calculate the total sales revenue for each region.

    Args:
        records: List of sales record dictionaries.

    Returns:
        A dictionary mapping region names to total revenue.
    """
    region_totals = defaultdict(float)
    for record in records:
        region_totals[record["Region"]] += record["Total_Sale"]
    return dict(sorted(region_totals.items(), key=lambda x: x[1], reverse=True))


def average_sale_amount(records: list[dict]) -> float:
    """
    Calculate the average sale amount across all transactions.

    Args:
        records: List of sales record dictionaries.

    Returns:
        The average sale amount as a float.
    """
    if not records:
        return 0.0
    total = sum(record["Total_Sale"] for record in records)
    return total / len(records)


def top_performers(records: list[dict], n: int = 3) -> list[tuple[str, float]]:
    """
    Identify the top N salespersons by total revenue.

    Args:
        records: List of sales record dictionaries.
        n: Number of top performers to return (default: 3).

    Returns:
        A list of (salesperson_name, total_revenue) tuples,
        sorted by revenue descending.
    """
    person_totals = defaultdict(float)
    for record in records:
        person_totals[record["Salesperson"]] += record["Total_Sale"]
    sorted_performers = sorted(
        person_totals.items(), key=lambda x: x[1], reverse=True
    )
    return sorted_performers[:n]


def monthly_breakdown(records: list[dict]) -> dict[str, dict[str, float]]:
    """
    Break down sales by month, showing total revenue and transaction count.

    Args:
        records: List of sales record dictionaries.

    Returns:
        A dictionary mapping month strings (e.g., '2025-01') to
        sub-dictionaries with 'total_revenue' and 'transaction_count'.
    """
    monthly = defaultdict(lambda: {"total_revenue": 0.0, "transaction_count": 0})
    for record in records:
        # Extract YYYY-MM from the date string
        month_key = record["Date"][:7]
        monthly[month_key]["total_revenue"] += record["Total_Sale"]
        monthly[month_key]["transaction_count"] += 1
    return dict(sorted(monthly.items()))


def print_report(records: list[dict]) -> None:
    """
    Print a formatted summary report to the console.

    Args:
        records: List of sales record dictionaries.
    """
    separator = "" * 60

    print()
    print(separator)
    print("    SALES SUMMARY REPORT")
    print(f"    Data Period: {records[0]['Date']} to {records[-1]['Date']}")
    print(f"    Total Transactions: {len(records)}")
    print(separator)

    #  Total Sales per Region 
    print("\n    TOTAL SALES PER REGION")
    print("  " + "" * 40)
    region_data = total_sales_per_region(records)
    grand_total = sum(region_data.values())
    for region, total in region_data.items():
        bar = "" * int(total / grand_total * 30)
        pct = total / grand_total * 100
        print(f"  {region:<8} ${total:>10,.2f}  ({pct:5.1f}%)  {bar}")
    print(f"  {'TOTAL':<8} ${grand_total:>10,.2f}")

    #  Average Sale Amount 
    avg = average_sale_amount(records)
    print(f"\n    AVERAGE SALE AMOUNT: ${avg:,.2f}")

    #  Top 3 Performers 
    print("\n    TOP 3 PERFORMERS BY REVENUE")
    print("  " + "" * 40)
    top = top_performers(records, n=3)
    medals = ["", "", ""]
    for i, (name, revenue) in enumerate(top):
        print(f"  {medals[i]} {name:<20} ${revenue:>10,.2f}")

    #  Monthly Breakdown 
    print("\n    MONTHLY BREAKDOWN")
    print("  " + "" * 50)
    print(f"  {'Month':<10} {'Revenue':>12} {'Transactions':>15}")
    print("  " + "" * 50)
    monthly_data = monthly_breakdown(records)
    for month, data in monthly_data.items():
        print(
            f"  {month:<10} ${data['total_revenue']:>10,.2f} "
            f"{data['transaction_count']:>12}"
        )
    print()
    print(separator)
    print()


def write_summary_csv(records: list[dict], output_dir: str) -> str:
    """
    Write the summary report data to a CSV file.

    Uses os.path for cross-platform path handling so the script
    works on Windows, macOS, and Linux.

    Args:
        records: List of sales record dictionaries.
        output_dir: Directory where the output file will be created.

    Returns:
        The absolute path to the created CSV file.
    """
    output_path = os.path.join(output_dir, "sales_summary_report.csv")

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        #  Section 1: Region Summary 
        writer.writerow(["=== TOTAL SALES PER REGION ==="])
        writer.writerow(["Region", "Total Revenue ($)", "Percentage (%)"])
        region_data = total_sales_per_region(records)
        grand_total = sum(region_data.values())
        for region, total in region_data.items():
            pct = total / grand_total * 100
            writer.writerow([region, f"{total:.2f}", f"{pct:.1f}"])
        writer.writerow(["GRAND TOTAL", f"{grand_total:.2f}", "100.0"])
        writer.writerow([])

        #  Section 2: Average Sale 
        avg = average_sale_amount(records)
        writer.writerow(["=== AVERAGE SALE AMOUNT ==="])
        writer.writerow(["Metric", "Value ($)"])
        writer.writerow(["Average Sale", f"{avg:.2f}"])
        writer.writerow(["Total Transactions", len(records)])
        writer.writerow([])

        #  Section 3: Top Performers 
        writer.writerow(["=== TOP 3 PERFORMERS ==="])
        writer.writerow(["Rank", "Salesperson", "Total Revenue ($)"])
        top = top_performers(records, n=3)
        for rank, (name, revenue) in enumerate(top, start=1):
            writer.writerow([rank, name, f"{revenue:.2f}"])
        writer.writerow([])

        #  Section 4: Monthly Breakdown 
        writer.writerow(["=== MONTHLY BREAKDOWN ==="])
        writer.writerow(["Month", "Total Revenue ($)", "Transactions"])
        monthly_data = monthly_breakdown(records)
        for month, data in monthly_data.items():
            writer.writerow([
                month,
                f"{data['total_revenue']:.2f}",
                data["transaction_count"],
            ])

    return output_path


# 
# MAIN EXECUTION
# 
if __name__ == "__main__":
    # Step 1: Read and parse the embedded sales data
    sales_records = read_sales_data(RAW_CSV_DATA)
    print(f" Loaded {len(sales_records)} sales records from embedded CSV data.")

    # Step 2: Print formatted report to console
    print_report(sales_records)

    # Step 3: Write summary to CSV in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = write_summary_csv(sales_records, script_dir)
    print(f" Summary report written to: {output_file}")
    print()
    print(
        " TIP: In a real migration, you would schedule this script via "
        "cron (Linux/macOS) or Task Scheduler (Windows) to replace the "
        "VBA macro that runs inside Excel."
    )
