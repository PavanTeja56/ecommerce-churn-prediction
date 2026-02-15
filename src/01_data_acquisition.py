import pandas as pd
import os
from datetime import datetime

RAW_DATA_PATH = "data/raw/online_retail.csv"

def download_dataset():
    """
    Download and save the Online Retail dataset
    """
    print("Starting dataset download...")

    os.makedirs("data/raw", exist_ok=True)

    # Try UCI first (manual download fallback if blocked)
    try:
        df = pd.read_excel(
            "data/raw/online_retail_II.xlsx",
            sheet_name=0
        )
        print("Loaded dataset from local Excel file.")
    except:
        raise FileNotFoundError(
            "Please download 'online_retail_II.xlsx' manually and place it in data/raw/"
        )

    df.to_csv(RAW_DATA_PATH, index=False, encoding="latin1")

    print(f"Dataset saved to {RAW_DATA_PATH}")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"Download completed at {datetime.now()}")

def load_raw_data():
    """
    Load raw dataset
    """
    df = pd.read_csv(RAW_DATA_PATH, encoding="latin1")
    return df

def generate_data_profile():
    """
    Generate basic data profile
    """
    df = load_raw_data()

    profile_path = "data/raw/data_profile.txt"
    with open(profile_path, "w") as f:
        f.write(f"Rows: {df.shape[0]}\n")
        f.write(f"Columns: {df.shape[1]}\n\n")
        f.write("Column Info:\n")
        f.write(str(df.dtypes))
        f.write("\n\nMemory Usage:\n")
        f.write(str(df.memory_usage(deep=True)))
        f.write("\n\nSample Data:\n")
        f.write(str(df.head()))

    print(f"Data profile saved to {profile_path}")

if __name__ == "__main__":
    download_dataset()
    generate_data_profile()
