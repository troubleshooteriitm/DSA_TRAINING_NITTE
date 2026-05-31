"""
Scikit-Learn Basics Practice
==============================
Examples: train_test_split, linear regression, decision tree, model evaluation.
"""

try:
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import (accuracy_score, mean_squared_error, r2_score,
                                 classification_report)
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("  Install packages: pip install numpy scikit-learn")

if HAS_SKLEARN:
    print("=" * 50)
    print("  SCIKIT-LEARN BASICS")
    print("=" * 50)

    # ============================================================
    # 1. LINEAR REGRESSION
    # ============================================================
    print("\n--- Linear Regression ---")
    np.random.seed(42)

    # Generate data: salary = 5000 * experience + 30000 + noise
    X = np.random.randint(1, 21, 100).reshape(-1, 1)
    y = 5000 * X.ravel() + 30000 + np.random.randn(100) * 5000

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"  Coefficient: {model.coef_[0]:,.2f}")
    print(f"  Intercept:   {model.intercept_:,.2f}")
    print(f"  MSE:  {mean_squared_error(y_test, y_pred):,.2f}")
    print(f"  RMSE: {mean_squared_error(y_test, y_pred)**0.5:,.2f}")
    print(f"  R²:   {r2_score(y_test, y_pred):.4f}")

    # Predict
    new_experience = np.array([[5], [10], [15]])
    predictions = model.predict(new_experience)
    for exp, pred in zip(new_experience.ravel(), predictions):
        print(f"  Experience {exp} yrs  Predicted salary: ₹{pred:,.0f}")

    # ============================================================
    # 2. DECISION TREE CLASSIFIER
    # ============================================================
    print("\n--- Decision Tree Classifier ---")

    # Generate: [study_hours, sleep_hours]  pass/fail
    np.random.seed(42)
    n = 200
    study = np.random.uniform(0, 10, n)
    sleep = np.random.uniform(4, 10, n)
    passed = ((study > 4) & (sleep > 5.5)).astype(int)
    # Add some noise
    noise_idx = np.random.choice(n, 20, replace=False)
    passed[noise_idx] = 1 - passed[noise_idx]

    X = np.column_stack([study, sleep])
    y = passed

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print(f"  Accuracy: {accuracy_score(y_test, y_pred):.2%}")
    print(f"\n  Classification Report:")
    report = classification_report(y_test, y_pred, target_names=["Fail", "Pass"])
    for line in report.split("\n"):
        print(f"    {line}")

    # Feature importance
    print(f"  Feature Importance:")
    for name, imp in zip(["Study Hours", "Sleep Hours"], clf.feature_importances_):
        print(f"    {name}: {imp:.4f}")

    # ============================================================
    # 3. LOGISTIC REGRESSION
    # ============================================================
    print("\n--- Logistic Regression ---")

    lr = LogisticRegression(random_state=42)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)

    print(f"  Accuracy: {accuracy_score(y_test, y_pred_lr):.2%}")

    # Compare models
    print(f"\n  Model Comparison:")
    print(f"    Decision Tree: {accuracy_score(y_test, y_pred):.2%}")
    print(f"    Logistic Reg:  {accuracy_score(y_test, y_pred_lr):.2%}")

    print("\n   All examples completed!")
