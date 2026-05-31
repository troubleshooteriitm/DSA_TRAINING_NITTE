# Day 11 -- Matplotlib, Data Science & Scikit-Learn

##  Topics Covered
- Data Visualization (Line/Bar/Pie Charts)
- Machine Learning Basics (Classification, Regression)
- Train-Test Split, Model Evaluation, Feature Engineering

> **Required:** `pip install matplotlib scikit-learn pandas numpy`

---

## 1. Matplotlib Basics

```python
import matplotlib.pyplot as plt

# LINE CHART
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
sales = [12000, 15000, 13500, 17000, 16500, 19000]

plt.figure(figsize=(10, 5))
plt.plot(months, sales, marker='o', color='#2563eb', linewidth=2)
plt.title("Monthly Sales Trend", fontsize=14, fontweight='bold')
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.grid(True, alpha=0.3)
plt.show()

# BAR CHART
departments = ['Engineering', 'Sales', 'HR', 'Finance']
headcount = [50, 30, 15, 20]

plt.bar(departments, headcount, color=['#3b82f6', '#10b981', '#f59e0b', '#ef4444'])
plt.title("Department Headcount")
plt.ylabel("Employees")
plt.show()

# PIE CHART
plt.pie(headcount, labels=departments, autopct='%1.1f%%', startangle=90)
plt.title("Department Distribution")
plt.show()
```

---

## 2. Subplots

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: Line
axes[0].plot(months, sales, 'b-o')
axes[0].set_title("Sales Trend")

# Plot 2: Bar
axes[1].bar(departments, headcount, color='skyblue')
axes[1].set_title("Headcount")

# Plot 3: Pie
axes[2].pie(headcount, labels=departments, autopct='%1.0f%%')
axes[2].set_title("Distribution")

plt.tight_layout()
plt.show()
```

---

## 3. Machine Learning Basics

### Supervised vs Unsupervised Learning

| Aspect | Supervised | Unsupervised |
|--------|-----------|-------------|
| Labels | Has labels (y) | No labels |
| Goal | Predict output | Find patterns |
| Examples | Classification, Regression | Clustering, Dimensionality Reduction |
| Algorithms | Linear Regression, Decision Tree, SVM | K-Means, PCA, DBSCAN |

### Classification vs Regression

| Type | Output | Example |
|------|--------|---------|
| Classification | Discrete (categories) | Spam/Not Spam, Churn/No Churn |
| Regression | Continuous (numbers) | House Price, Temperature |

---

## 4. Train-Test Split

```python
from sklearn.model_selection import train_test_split
import numpy as np

X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([2, 4, 5, 4, 5, 7, 8, 9, 10, 11])

# Split: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training set: {len(X_train)} samples")
print(f"Test set:     {len(X_test)} samples")
```

---

## 5. Linear Regression

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"MSE: {mse:.4f}")
print(f"R² Score: {r2:.4f}")
print(f"Coefficient: {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
```

---

## 6. Classification (Decision Tree)

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Sample: [age, salary]  [will_buy: 0/1]
X = [[25, 30000], [30, 50000], [35, 60000], [40, 80000],
     [22, 25000], [28, 45000], [45, 90000], [50, 100000]]
y = [0, 0, 1, 1, 0, 0, 1, 1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
```

---

## 7. Model Evaluation Metrics

### Classification Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| **Accuracy** | (TP+TN) / Total | Balanced classes |
| **Precision** | TP / (TP+FP) | Minimize false positives |
| **Recall** | TP / (TP+FN) | Minimize false negatives |
| **F1 Score** | 2x(PxR)/(P+R) | Balance P and R |

### Regression Metrics

| Metric | Description |
|--------|-------------|
| **MSE** | Mean Squared Error -- penalizes large errors |
| **RMSE** | Root MSE -- same unit as target |
| **MAE** | Mean Absolute Error -- robust to outliers |
| **R²** | Coefficient of determination (0-1, higher=better) |

### Confusion Matrix

```
                 Predicted
              Positive  Negative
Actual  Pos    TP       FN    
        Neg    FP       TN    
```

---

## 8. Feature Engineering

```python
import pandas as pd

# Common techniques:
# 1. Handling missing values
df['col'] = df['col'].fillna(df['col'].median())

# 2. Encoding categorical variables
df['dept_code'] = df['department'].map({'Engineering': 0, 'Sales': 1, 'HR': 2})

# 3. Feature scaling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Creating new features
df['experience'] = 2025 - df['join_year']
df['salary_per_year'] = df['salary'] / df['experience']
```

---

##  Interview Tips
- **Bias-Variance Tradeoff**: Underfitting (high bias) vs overfitting (high variance)
- **Cross-Validation**: K-fold CV gives more reliable evaluation than single split
- **Feature Scaling**: Required for SVM, KNN, Neural Networks; not needed for Decision Trees
- **When to use what**:
  - Small data, interpretable  Decision Tree
  - Linear relationship  Linear/Logistic Regression
  - Complex patterns  Random Forest, Gradient Boosting

##  Practice Problems
| Problem | Platform | Difficulty |
|---------|----------|------------|
| Binary Search | LeetCode 704 | Easy |
| Merge Sorted Array | LeetCode 88 | Easy |
| Statistics & ML Basics | HackerRank | Easy |
