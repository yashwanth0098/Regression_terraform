from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
import joblib
import pandas as pd
from pathlib import Path
app = FastAPI()
import uvicorn





BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model" / "model.pkl"
FEATURE_PATH = BASE_DIR / "model" / "feature_columns.pkl"


# Load model artifacts
# -------------------------
model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURE_PATH)


REQUEST_COUNT = Counter("prediction_requests_total", "Total predictions")
PREDICTION_TIME =  Histogram(
    "prediction_latency_seconds",
    "Time spent processing prediction requests"
)

# Expected feature columns (same as training)
FEATURE_COLUMNS = [
    "Id","MSSubClass","LotFrontage","LotArea","OverallQual","OverallCond",
    "YearBuilt","YearRemodAdd","MasVnrArea","BsmtFinSF1","BsmtFinSF2",
    "BsmtUnfSF","TotalBsmtSF","1stFlrSF","2ndFlrSF","LowQualFinSF",
    "GrLivArea","BsmtFullBath","BsmtHalfBath","FullBath","HalfBath",
    "BedroomAbvGr","KitchenAbvGr","TotRmsAbvGrd","Fireplaces",
    "GarageYrBlt","GarageCars","GarageArea","WoodDeckSF","OpenPorchSF",
    "EnclosedPorch","3SsnPorch","ScreenPorch","PoolArea","MiscVal",
    "MoSold","YrSold"
]

@app.get("/predict")
def predict():
    REQUEST_COUNT.inc()
    with PREDICTION_TIME.time():
        # Example input data (single house)
        sample_data = {
            "Id": 1,
            "MSSubClass": 60,
            "LotFrontage": 65,
            "LotArea": 12000,
            "OverallQual": 7,
            "OverallCond": 5,
            "YearBuilt": 2005,
            "YearRemodAdd": 2006,
            "MasVnrArea": 200,
            "BsmtFinSF1": 600,
            "BsmtFinSF2": 0,
            "BsmtUnfSF": 400,
            "TotalBsmtSF": 1000,
            "1stFlrSF": 1000,
            "2ndFlrSF": 800,
            "LowQualFinSF": 0,
            "GrLivArea": 1800,
            "BsmtFullBath": 1,
            "BsmtHalfBath": 0,
            "FullBath": 2,
            "HalfBath": 1,
            "BedroomAbvGr": 3,
            "KitchenAbvGr": 1,
            "TotRmsAbvGrd": 7,
            "Fireplaces": 1,
            "GarageYrBlt": 2005,
            "GarageCars": 2,
            "GarageArea": 480,
            "WoodDeckSF": 120,
            "OpenPorchSF": 40,
            "EnclosedPorch": 0,
            "3SsnPorch": 0,
            "ScreenPorch": 0,
            "PoolArea": 0,
            "MiscVal": 0,
            "MoSold": 6,
            "YrSold": 2010
        }
        
        # Convert to DataFrame and reorder columns to match the model's expected input
        sample_df = pd.DataFrame([sample_data])
        sample_df = sample_df[FEATURE_COLUMNS]
        
        # Predict the price
        price = model.predict(sample_df)[0]
        
        return {"prediction": price}

@app.get("/metrics")
def metrics():
    return generate_latest()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
