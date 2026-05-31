"""
Customer Order Processing & Enterprise Metadata Dashboard
============================================================
Corporate Use Case: Process customer orders, group by customer,
calculate totals, find top products using Counter, defaultdict,
OrderedDict, and comprehensions.
"""

from collections import Counter, defaultdict, OrderedDict
from datetime import datetime


# ============================================================
# SAMPLE ORDER DATA
# ============================================================

ORDERS = [
    {"order_id": "ORD001", "customer": "TechCorp", "product": "Laptop", "category": "Electronics", "qty": 5, "unit_price": 75000, "date": "2025-01-15", "status": "delivered"},
    {"order_id": "ORD002", "customer": "DataSoft", "product": "Monitor", "category": "Electronics", "qty": 10, "unit_price": 25000, "date": "2025-01-18", "status": "delivered"},
    {"order_id": "ORD003", "customer": "TechCorp", "product": "Keyboard", "category": "Accessories", "qty": 20, "unit_price": 2500, "date": "2025-02-01", "status": "delivered"},
    {"order_id": "ORD004", "customer": "InfoSys", "product": "Laptop", "category": "Electronics", "qty": 15, "unit_price": 75000, "date": "2025-02-10", "status": "delivered"},
    {"order_id": "ORD005", "customer": "DataSoft", "product": "Mouse", "category": "Accessories", "qty": 50, "unit_price": 500, "date": "2025-02-15", "status": "delivered"},
    {"order_id": "ORD006", "customer": "TechCorp", "product": "Server", "category": "Infrastructure", "qty": 2, "unit_price": 250000, "date": "2025-03-01", "status": "processing"},
    {"order_id": "ORD007", "customer": "CloudNet", "product": "SSD", "category": "Storage", "qty": 30, "unit_price": 5000, "date": "2025-03-05", "status": "delivered"},
    {"order_id": "ORD008", "customer": "InfoSys", "product": "Monitor", "category": "Electronics", "qty": 8, "unit_price": 25000, "date": "2025-03-10", "status": "shipped"},
    {"order_id": "ORD009", "customer": "CloudNet", "product": "RAM Module", "category": "Components", "qty": 40, "unit_price": 3000, "date": "2025-03-15", "status": "delivered"},
    {"order_id": "ORD010", "customer": "DataSoft", "product": "Laptop", "category": "Electronics", "qty": 3, "unit_price": 75000, "date": "2025-03-20", "status": "delivered"},
    {"order_id": "ORD011", "customer": "TechCorp", "product": "Webcam", "category": "Accessories", "qty": 15, "unit_price": 3500, "date": "2025-04-01", "status": "delivered"},
    {"order_id": "ORD012", "customer": "InfoSys", "product": "Keyboard", "category": "Accessories", "qty": 25, "unit_price": 2500, "date": "2025-04-05", "status": "delivered"},
]


def calculate_order_totals(orders):
    """Add 'total' field to each order using list comprehension."""
    return [
        {**order, "total": order["qty"] * order["unit_price"]}
        for order in orders
    ]


def group_by_customer(orders):
    """Group orders by customer using defaultdict."""
    customer_orders = defaultdict(list)
    for order in orders:
        customer_orders[order["customer"]].append(order)
    return dict(customer_orders)


def customer_summary(grouped_orders):
    """Calculate per-customer summary using comprehensions."""
    summary = {}
    for customer, orders in grouped_orders.items():
        summary[customer] = {
            "total_orders": len(orders),
            "total_revenue": sum(o["total"] for o in orders),
            "avg_order_value": sum(o["total"] for o in orders) / len(orders),
            "products": list({o["product"] for o in orders}),
        }
    return OrderedDict(
        sorted(summary.items(), key=lambda x: x[1]["total_revenue"], reverse=True)
    )


def top_products(orders, n=5):
    """Find top products by quantity sold using Counter."""
    product_qty = Counter()
    for order in orders:
        product_qty[order["product"]] += order["qty"]
    return product_qty.most_common(n)


def category_breakdown(orders):
    """Revenue breakdown by category using defaultdict + comprehension."""
    cat_revenue = defaultdict(int)
    cat_count = defaultdict(int)
    for order in orders:
        cat_revenue[order["category"]] += order["total"]
        cat_count[order["category"]] += 1
    return {
        cat: {"revenue": cat_revenue[cat], "orders": cat_count[cat]}
        for cat in sorted(cat_revenue, key=cat_revenue.get, reverse=True)
    }


def monthly_trends(orders):
    """Monthly revenue trends using defaultdict."""
    monthly = defaultdict(int)
    for order in orders:
        month = order["date"][:7]  # YYYY-MM
        monthly[month] += order["total"]
    return OrderedDict(sorted(monthly.items()))


def status_distribution(orders):
    """Order status distribution using Counter."""
    return dict(Counter(o["status"] for o in orders))


# ============================================================
# DASHBOARD OUTPUT
# ============================================================

def print_dashboard(orders):
    """Print complete dashboard."""
    orders = calculate_order_totals(orders)
    total_revenue = sum(o["total"] for o in orders)

    print("=" * 70)
    print("   ENTERPRISE ORDER PROCESSING DASHBOARD")
    print("=" * 70)

    # Overview
    print(f"\n{''*70}")
    print("   OVERVIEW")
    print(f"{''*70}")
    print(f"  Total Orders:    {len(orders)}")
    print(f"  Total Revenue:   ₹{total_revenue:,.2f}")
    print(f"  Unique Customers: {len(set(o['customer'] for o in orders))}")
    print(f"  Unique Products:  {len(set(o['product'] for o in orders))}")

    # Customer Summary
    grouped = group_by_customer(orders)
    summary = customer_summary(grouped)
    print(f"\n{''*70}")
    print("   CUSTOMER SUMMARY (by revenue)")
    print(f"{''*70}")
    print(f"  {'Customer':<15} {'Orders':<8} {'Revenue':>15} {'Avg Order':>15}")
    print(f"  {''*53}")
    for customer, data in summary.items():
        print(f"  {customer:<15} {data['total_orders']:<8} "
              f"₹{data['total_revenue']:>13,.2f} ₹{data['avg_order_value']:>13,.2f}")

    # Top Products
    top = top_products(orders)
    print(f"\n{''*70}")
    print("   TOP PRODUCTS (by quantity)")
    print(f"{''*70}")
    for rank, (product, qty) in enumerate(top, 1):
        bar = "" * (qty // 2)
        print(f"  {rank}. {product:<15} {qty:>4} units  {bar}")

    # Category Breakdown
    categories = category_breakdown(orders)
    print(f"\n{''*70}")
    print("   CATEGORY BREAKDOWN")
    print(f"{''*70}")
    for cat, data in categories.items():
        pct = data["revenue"] / total_revenue * 100
        print(f"  {cat:<15} ₹{data['revenue']:>13,.2f}  ({pct:5.1f}%)  "
              f"[{data['orders']} orders]")

    # Monthly Trends
    trends = monthly_trends(orders)
    print(f"\n{''*70}")
    print("   MONTHLY REVENUE TRENDS")
    print(f"{''*70}")
    max_rev = max(trends.values())
    for month, revenue in trends.items():
        bar_len = int(revenue / max_rev * 30)
        bar = "" * bar_len
        print(f"  {month}  ₹{revenue:>13,.2f}  {bar}")

    # Status
    status = status_distribution(orders)
    print(f"\n{''*70}")
    print("   ORDER STATUS")
    print(f"{''*70}")
    for s, count in sorted(status.items(), key=lambda x: -x[1]):
        print(f"  {s:<12} {count} orders")

    print(f"\n{'='*70}")


if __name__ == "__main__":
    print_dashboard(ORDERS)
