import pandas as pd
from src.predict import predict_churn

# Load a few real customers from your processed dataset
df = pd.read_csv("data/processed/model_ready_dataset.csv")

# Take first 5 customers (excluding churn label)
sample_input = df.drop(columns=["churn"]).head(5)

# Run prediction
results = predict_churn(sample_input)

print(results[["churn_probability", "churn_prediction"]])
