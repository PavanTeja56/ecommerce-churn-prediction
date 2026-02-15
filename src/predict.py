import joblib
import pandas as pd
import os

# Load artifacts
# Load artifacts from data/processed
MODEL_PATH = os.path.join("models", "final_churn_model.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")
FEATURE_PATH = os.path.join("models", "feature_columns.pkl")


model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_columns = joblib.load(FEATURE_PATH)


def preprocess_input(df: pd.DataFrame):
    """
    Ensures correct feature order and scaling.
    """
    df = df.copy()
    df = df[feature_columns]  # enforce column order
    df_scaled = scaler.transform(df)
    return df_scaled


def predict_churn(df: pd.DataFrame):
    """
    Returns churn probability and label.
    """
    df_processed = preprocess_input(df)

    probabilities = model.predict_proba(df_processed)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    result = df.copy()
    result["churn_probability"] = probabilities
    result["churn_prediction"] = predictions

    return result
