"""
Matplotlib Charts Practice
============================
Examples: line, bar, pie, scatter, histogram charts.
"""

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend for saving
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("  Install matplotlib: pip install matplotlib")
    print("   This script requires matplotlib to generate charts.")

if HAS_MPL:
    print("=" * 50)
    print("  MATPLOTLIB CHARTS PRACTICE")
    print("=" * 50)

    # ============================================================
    # 1. LINE CHART
    # ============================================================
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    revenue = [120, 135, 150, 145, 165, 180, 175, 190, 210, 205, 225, 250]
    expenses = [100, 110, 115, 120, 125, 130, 128, 135, 140, 138, 145, 155]

    plt.figure(figsize=(10, 5))
    plt.plot(months, revenue, 'o-', color='#2563eb', label='Revenue', linewidth=2)
    plt.plot(months, expenses, 's--', color='#ef4444', label='Expenses', linewidth=2)
    plt.fill_between(range(12), revenue, expenses, alpha=0.1, color='green')
    plt.title("Revenue vs Expenses (2025)", fontsize=14, fontweight='bold')
    plt.xlabel("Month")
    plt.ylabel("Amount (₹ Lakhs)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("line_chart.png", dpi=100)
    plt.close()
    print("   line_chart.png saved")

    # ============================================================
    # 2. BAR CHART
    # ============================================================
    departments = ['Engineering', 'Sales', 'HR', 'Finance', 'Support']
    headcount = [55, 30, 12, 18, 25]
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

    plt.figure(figsize=(8, 5))
    bars = plt.bar(departments, headcount, color=colors, edgecolor='white', linewidth=1.5)
    for bar, count in zip(bars, headcount):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 str(count), ha='center', fontweight='bold')
    plt.title("Department Headcount", fontsize=14, fontweight='bold')
    plt.ylabel("Employees")
    plt.tight_layout()
    plt.savefig("bar_chart.png", dpi=100)
    plt.close()
    print("   bar_chart.png saved")

    # ============================================================
    # 3. PIE CHART
    # ============================================================
    plt.figure(figsize=(8, 6))
    explode = (0.05, 0, 0, 0, 0)
    plt.pie(headcount, labels=departments, autopct='%1.1f%%', startangle=90,
            colors=colors, explode=explode, shadow=True)
    plt.title("Department Distribution", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig("pie_chart.png", dpi=100)
    plt.close()
    print("   pie_chart.png saved")

    # ============================================================
    # 4. SCATTER PLOT
    # ============================================================
    import random
    random.seed(42)
    experience = [random.randint(1, 20) for _ in range(50)]
    salary = [exp * 8000 + random.randint(-10000, 15000) for exp in experience]

    plt.figure(figsize=(8, 5))
    plt.scatter(experience, salary, c=experience, cmap='viridis', alpha=0.7, s=80, edgecolors='white')
    plt.colorbar(label='Years of Experience')
    plt.title("Experience vs Salary", fontsize=14, fontweight='bold')
    plt.xlabel("Years of Experience")
    plt.ylabel("Salary (₹)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("scatter_plot.png", dpi=100)
    plt.close()
    print("   scatter_plot.png saved")

    # ============================================================
    # 5. HISTOGRAM
    # ============================================================
    ages = [random.randint(22, 60) for _ in range(200)]

    plt.figure(figsize=(8, 5))
    plt.hist(ages, bins=15, color='#6366f1', edgecolor='white', alpha=0.8)
    plt.axvline(sum(ages)/len(ages), color='red', linestyle='--', label=f'Mean: {sum(ages)/len(ages):.0f}')
    plt.title("Employee Age Distribution", fontsize=14, fontweight='bold')
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig("histogram.png", dpi=100)
    plt.close()
    print("   histogram.png saved")

    print("\n  All charts saved as PNG files in the current directory.")
