import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import os

# Load data
df = pd.read_csv("backend/Zomato2_cleaned.csv")

# Preprocessing (same as in Final_RP.py)
zomato = df.copy()
zomato['avg_cost_for_two'] = np.log1p(zomato['avg_cost_for_two'])

label_cols = ['City','Cuisines','country','price_label']
le = LabelEncoder()
for col in label_cols:
    zomato[col] = le.fit_transform(zomato[col])

X = zomato.drop(columns=['restaurant_id','restaurant_name','Locality','Rating', 'Votes', 'is_rated'], axis=1)
y = zomato['Rating']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def check_overfitting(model, name):
    model.fit(X_train, y_train)
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    
    train_r2 = r2_score(y_train, train_preds)
    test_r2 = r2_score(y_test, test_preds)
    
    print(f"--- {name} ---")
    print(f"Train R2: {train_r2:.4f}")
    print(f"Test R2 : {test_r2:.4f}")
    print(f"Difference: {train_r2 - test_r2:.4f}")
    if (train_r2 - test_r2) > 0.1:
        print("Status: POTENTIAL OVERFITTING")
    else:
        print("Status: HEALTHY")
    print()

# Check the models used in Final_RP.py
check_overfitting(RandomForestRegressor(n_estimators=100, max_depth=10), "Random Forest (Default)")
check_overfitting(GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, max_depth=5), "Gradient Boosting (Current Best)")
