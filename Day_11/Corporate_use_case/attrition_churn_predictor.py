"""
Predictive Employee Attrition & Customer Churn Analysis System
================================================================
Corporate Use Case: Build a simple ML model to predict employee attrition.
Uses scikit-learn for classification with synthetic data.
"""

import random
random.seed(42)

try:
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("  Install required packages: pip install numpy pandas scikit-learn")
    print("   Running in demo mode with basic Python only.\n")


def generate_employee_data(n=100):
    """Generate synthetic employee data."""
    random.seed(42)
    data = []
    for i in range(n):
        age = random.randint(22, 60)
        department = random.choice(["Engineering", "Sales", "HR", "Finance", "Support"])
        salary = random.randint(30000, 200000)
        years_at_company = random.randint(0, 20)
        satisfaction = round(random.uniform(1, 5), 1)
        overtime_hours = random.randint(0, 30)
        num_projects = random.randint(1, 8)
        last_promotion_years = random.randint(0, 10)

        # Attrition probability based on features
        attrition_score = 0
        if satisfaction < 2.5:
            attrition_score += 3
        if overtime_hours > 20:
            attrition_score += 2
        if salary < 60000:
            attrition_score += 2
        if years_at_company < 2:
            attrition_score += 1
        if last_promotion_years > 5:
            attrition_score += 2
        if num_projects > 6:
            attrition_score += 1

        left = 1 if attrition_score >= 5 or random.random() < 0.1 else 0

        data.append({
            "emp_id": f"E{1000 + i}",
            "age": age,
            "department": department,
            "salary": salary,
            "years_at_company": years_at_company,
            "satisfaction_score": satisfaction,
            "overtime_hours": overtime_hours,
            "num_projects": num_projects,
            "last_promotion_years": last_promotion_years,
            "left": left,
        })
    return data


def run_with_sklearn(data):
    """Full ML pipeline with scikit-learn."""
    df = pd.DataFrame(data)

    print(f"\n{''*60}")
    print("   DATASET OVERVIEW")
    print(f"{''*60}")
    print(f"  Total employees: {len(df)}")
    print(f"  Left (attrition): {df['left'].sum()} ({df['left'].mean()*100:.1f}%)")
    print(f"  Stayed: {(df['left']==0).sum()} ({(1-df['left'].mean())*100:.1f}%)")

    # Department-wise attrition
    print(f"\n  Department-wise Attrition:")
    dept_attrition = df.groupby("department")["left"].agg(["sum", "count", "mean"])
    dept_attrition.columns = ["left", "total", "rate"]
    for dept, row in dept_attrition.iterrows():
        print(f"    {dept:<15} {int(row['left'])}/{int(row['total'])} ({row['rate']*100:.1f}%)")

    # Feature engineering
    dept_map = {d: i for i, d in enumerate(df["department"].unique())}
    df["dept_code"] = df["department"].map(dept_map)

    features = ["age", "salary", "years_at_company", "satisfaction_score",
                 "overtime_hours", "num_projects", "last_promotion_years", "dept_code"]

    X = df[features].values
    y = df["left"].values

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print(f"\n{''*60}")
    print("   MODEL TRAINING")
    print(f"{''*60}")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")

    # Train Decision Tree
    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n  Accuracy: {accuracy:.2%}")
    print(f"\n  Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"    {'':>15} Predicted Stay  Predicted Leave")
    print(f"    {'Actual Stay':<15} {cm[0][0]:>13}  {cm[0][1]:>14}")
    print(f"    {'Actual Leave':<15} {cm[1][0]:>13}  {cm[1][1]:>14}")

    print(f"\n  Classification Report:")
    report = classification_report(y_test, y_pred, target_names=["Stayed", "Left"])
    for line in report.split("\n"):
        print(f"    {line}")

    # Feature importance
    print(f"\n{''*60}")
    print("   FEATURE IMPORTANCE")
    print(f"{''*60}")
    importances = sorted(zip(features, clf.feature_importances_),
                         key=lambda x: x[1], reverse=True)
    for feat, imp in importances:
        bar = "" * int(imp * 40)
        print(f"  {feat:<25} {imp:.4f} {bar}")

    # Predict new employees
    print(f"\n{''*60}")
    print("   ATTRITION RISK PREDICTION (New Employees)")
    print(f"{''*60}")

    new_employees = [
        {"name": "Ravi", "age": 25, "salary": 45000, "years": 1, "satisfaction": 2.0,
         "overtime": 25, "projects": 7, "promo_years": 0, "dept": "Support"},
        {"name": "Priya", "age": 35, "salary": 120000, "years": 8, "satisfaction": 4.5,
         "overtime": 5, "projects": 3, "promo_years": 1, "dept": "Engineering"},
        {"name": "Amit", "age": 42, "salary": 80000, "years": 12, "satisfaction": 2.8,
         "overtime": 15, "projects": 5, "promo_years": 7, "dept": "Finance"},
    ]

    for emp in new_employees:
        dept_code = dept_map.get(emp["dept"], 0)
        features_arr = np.array([[emp["age"], emp["salary"], emp["years"],
                                  emp["satisfaction"], emp["overtime"],
                                  emp["projects"], emp["promo_years"], dept_code]])
        pred = clf.predict(features_arr)[0]
        prob = clf.predict_proba(features_arr)[0]
        risk = " HIGH RISK" if pred == 1 else " LOW RISK"
        print(f"  {emp['name']:<10} ({emp['dept']:<12})  {risk} "
              f"(Stay: {prob[0]:.0%}, Leave: {prob[1]:.0%})")


def run_basic(data):
    """Basic analysis without sklearn."""
    left = [d for d in data if d["left"] == 1]
    stayed = [d for d in data if d["left"] == 0]

    print(f"\n  Total: {len(data)}, Left: {len(left)}, Stayed: {len(stayed)}")
    print(f"  Attrition rate: {len(left)/len(data)*100:.1f}%")

    # Averages
    print(f"\n  Avg satisfaction (left):   {sum(d['satisfaction_score'] for d in left)/len(left):.2f}")
    print(f"  Avg satisfaction (stayed): {sum(d['satisfaction_score'] for d in stayed)/len(stayed):.2f}")
    print(f"  Avg overtime (left):       {sum(d['overtime_hours'] for d in left)/len(left):.1f} hrs")
    print(f"  Avg overtime (stayed):     {sum(d['overtime_hours'] for d in stayed)/len(stayed):.1f} hrs")


if __name__ == "__main__":
    print("=" * 60)
    print("   EMPLOYEE ATTRITION & CHURN PREDICTION SYSTEM")
    print("=" * 60)

    data = generate_employee_data(100)

    if HAS_SKLEARN:
        run_with_sklearn(data)
    else:
        run_basic(data)

    print(f"\n{'='*60}")
