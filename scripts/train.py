import pandas as pd
import json
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import os
from sklearn.ensemble import RandomForestRegressor

# CHANGE 1: Update directory to match Lab 6 requirements
os.makedirs('app/artifacts', exist_ok=True)

# 1. Load Dataset
data = pd.read_csv('data/winequality-red.csv', sep=';')

# 2. Pre-processing & Feature Selection
X = data.drop('quality', axis=1)
y = data['quality']

# --- EXPERIMENT 1 ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
# -----------------------------------------------

# 3. Train
model.fit(X_train, y_train)

# 4. Evaluate
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# CHANGE 2: Save to the app/artifacts directory
joblib.dump(model, 'app/artifacts/model.pkl')

metrics = {
    "mse": mse,
    "r2_score": r2
}

with open('app/artifacts/metrics.json', 'w') as f:
    json.dump(metrics, f)

# 6. Print to Standard Output
print(f"MSE: {mse}")
print(f"R2 Score: {r2}")
