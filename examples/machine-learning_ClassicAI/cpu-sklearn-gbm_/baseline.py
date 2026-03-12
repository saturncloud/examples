import numpy as np
import pandas as pd
import matplotlib
import joblib  # <--- NEW: For saving the model
import os

# ---------------------------------------------------------
# 🔧 Headless Server Config
matplotlib.use('Agg') 
# ---------------------------------------------------------

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# Set style for plots
sns.set(style="whitegrid")

def run_baseline_comparison():
    print("🔄 Loading Iris Dataset...")
    data = load_iris()
    X = data.data
    y = data.target
    
    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    results = []

    print("\n--- 1. Baseline Models (Dummy Classifiers) ---")
    strategies = ['stratified', 'most_frequent', 'prior', 'uniform']
    for strategy in strategies:
        dummy = DummyClassifier(strategy=strategy, random_state=42)
        dummy.fit(X_train, y_train)
        score = dummy.score(X_test, y_test)
        results.append({'Model': f"Dummy ({strategy})", 'Accuracy': score, 'Type': 'Baseline'})
        print(f"   {strategy}: {score:.4f}")

    print("\n--- 2. Real Machine Learning Models ---")
    
    # SVM
    svm = SVC(gamma='scale', random_state=42)
    svm.fit(X_train, y_train)
    res_svm = svm.score(X_test, y_test)
    results.append({'Model': 'SVM', 'Accuracy': res_svm, 'Type': 'Real Model'})
    print(f"   SVM: {res_svm:.4f}")

    # Logistic Regression (We will save this one)
    log_reg = LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42)
    log_reg.fit(X_train, y_train)
    res_log = log_reg.score(X_test, y_test)
    results.append({'Model': 'Logistic Regression', 'Accuracy': res_log, 'Type': 'Real Model'})
    print(f"   Logistic Regression: {res_log:.4f}")

    # Decision Tree
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train, y_train)
    res_dt = dt.score(X_test, y_test)
    results.append({'Model': 'Decision Tree', 'Accuracy': res_dt, 'Type': 'Real Model'})
    print(f"   Decision Tree: {res_dt:.4f}")

    # --- 3. Save Artifacts ---
    print("\n💾 Saving Artifacts...")
    
    # Save the Plot
    df_results = pd.DataFrame(results)
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Accuracy", y="Model", hue="Type", data=df_results, palette="viridis")
    plt.title("Baseline vs. Real Model Performance")
    plt.axvline(x=0.33, color='r', linestyle='--', label="Random Guess")
    plt.tight_layout()
    plt.savefig("baseline_comparison.png")
    print("   ✅ Plot saved to 'baseline_comparison.png'")
    
    # Save the Model (For the API)
    joblib.dump(log_reg, "iris_model.pkl")
    print("   ✅ Model saved to 'iris_model.pkl'")

if __name__ == "__main__":
    run_baseline_comparison()