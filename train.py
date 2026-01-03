import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load training data
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "train_1.csv"
MODEL_PATH = BASE_DIR / "model" / "model.pkl"
FEATURE_PATH = BASE_DIR / "model" / "feature_columns.pkl"
df = pd.read_csv(DATA_PATH)


X = df.drop("SalePrice", axis=1)
y = df["SalePrice"]

# Split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Validate
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
rmse = mse ** 0.5

# Save artifacts
joblib.dump(model, MODEL_PATH)
joblib.dump(X.columns.tolist(), FEATURE_PATH)

print(f"Model trained successfully | RMSE: {rmse:.2f}")