import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load existing Telco Churn dataset
df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

# Let's use the 'Titanic' dataset to predict 'Survival' (0 = No, 1 = Yes)
# It is the most famous existing dataset for tabular classification.
df = df[['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare']].dropna()
df['Sex'] = LabelEncoder().fit_transform(df['Sex']) # Convert to numbers

X = df.drop('Survived', axis=1)
y = df['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Train XGBoost
model = xgb.XGBClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 3. Save
joblib.dump(model, "model.joblib")
print("✅ Success: Titanic Survival model trained using existing data.")