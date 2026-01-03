import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "test_1.csv"
MODEL_PATH = BASE_DIR / "model" / "model.pkl"
OUTPUT_PATH = BASE_DIR / "data" / "predictions.csv"

# Load model
model = joblib.load(MODEL_PATH)

# Load evaluation data (NO SalePrice)
df = pd.read_csv(DATA_PATH)


df_processed = df.fillna(df.mean(numeric_only=True))

# Predict
preds = model.predict(df_processed)

# Append predictions to original dataframe
df["Predicted_SalePrice"] = preds

# Save full output
df.to_csv(OUTPUT_PATH, index=False)

print("Inference completed. Predictions saved with full feature data.")
