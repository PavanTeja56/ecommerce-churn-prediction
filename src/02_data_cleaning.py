import pandas as pd
import numpy as np
import json
import os

class DataCleaner:
    def __init__(self, input_path):
        self.input_path = input_path
        self.df = pd.read_csv(input_path, encoding="latin1")

        # -----------------------------
        # STANDARDIZE COLUMN NAMES
        # -----------------------------
        self.df.rename(columns={
            "Invoice": "InvoiceNo",
            "Price": "UnitPrice",
            "Customer ID": "CustomerID"
        }, inplace=True)

        self.original_rows = len(self.df)

        self.stats = {
            "original_rows": self.original_rows,
            "rows_after_cleaning": None,
            "rows_removed": None,
            "retention_rate": None,
            "missing_values_before": {},
            "missing_values_after": {},
            "steps_applied": []
        }

    # -----------------------------
    # STEP 1: Missing CustomerID
    # -----------------------------
    def remove_missing_customer_ids(self):
        before = len(self.df)

        self.stats["missing_values_before"]["CustomerID"] = int(
            self.df["CustomerID"].isnull().sum()
        )

        self.df = self.df.dropna(subset=["CustomerID"])

        removed = before - len(self.df)
        self.stats["steps_applied"].append({
            "step": "remove_missing_customer_ids",
            "rows_removed": removed
        })

    # -----------------------------
    # STEP 2: Remove Cancelled Invoices
    # -----------------------------
    def remove_cancelled_invoices(self):
        before = len(self.df)

        self.df["InvoiceNo"] = self.df["InvoiceNo"].astype(str)
        self.df = self.df[~self.df["InvoiceNo"].str.startswith("C")]

        removed = before - len(self.df)
        self.stats["steps_applied"].append({
            "step": "remove_cancelled_invoices",
            "rows_removed": removed
        })

    # -----------------------------
    # STEP 3: Remove Negative Quantities
    # -----------------------------
    def remove_negative_quantities(self):
        before = len(self.df)

        self.df = self.df[self.df["Quantity"] > 0]

        removed = before - len(self.df)
        self.stats["steps_applied"].append({
            "step": "remove_negative_quantities",
            "rows_removed": removed
        })

    # -----------------------------
    # STEP 4: Remove Zero or Negative Prices
    # -----------------------------
    def remove_invalid_prices(self):
        before = len(self.df)

        self.df = self.df[self.df["UnitPrice"] > 0]

        removed = before - len(self.df)
        self.stats["steps_applied"].append({
            "step": "remove_invalid_prices",
            "rows_removed": removed
        })

    # -----------------------------
    # STEP 5: Remove Missing Descriptions
    # -----------------------------
    def remove_missing_descriptions(self):
        before = len(self.df)

        self.stats["missing_values_before"]["Description"] = int(
            self.df["Description"].isnull().sum()
        )

        self.df = self.df.dropna(subset=["Description"])

        removed = before - len(self.df)
        self.stats["steps_applied"].append({
            "step": "remove_missing_descriptions",
            "rows_removed": removed
        })

    # -----------------------------
    # STEP 6: Remove Outliers (IQR)
    # -----------------------------
    def remove_outliers(self):
        before = len(self.df)

        for col in ["Quantity", "UnitPrice"]:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            self.df = self.df[
                (self.df[col] >= lower) & (self.df[col] <= upper)
            ]

        removed = before - len(self.df)
        self.stats["steps_applied"].append({
            "step": "remove_outliers",
            "rows_removed": removed
        })

    # -----------------------------
    # STEP 7: Remove Duplicates
    # -----------------------------
    def remove_duplicates(self):
        before = len(self.df)

        self.df = self.df.drop_duplicates()

        removed = before - len(self.df)
        self.stats["steps_applied"].append({
            "step": "remove_duplicates",
            "rows_removed": removed
        })

    # -----------------------------
    # STEP 8: Add Derived Columns
    # -----------------------------
    def add_derived_columns(self):
        self.df["InvoiceDate"] = pd.to_datetime(self.df["InvoiceDate"])

        self.df["TotalPrice"] = (
            self.df["Quantity"] * self.df["UnitPrice"]
        )

        self.df["Year"] = self.df["InvoiceDate"].dt.year
        self.df["Month"] = self.df["InvoiceDate"].dt.month
        self.df["DayOfWeek"] = self.df["InvoiceDate"].dt.dayofweek
        self.df["Hour"] = self.df["InvoiceDate"].dt.hour

    # -----------------------------
    # STEP 9: Convert Data Types
    # -----------------------------
    def convert_data_types(self):
        self.df["CustomerID"] = self.df["CustomerID"].astype(int)

    # -----------------------------
    # Save Outputs
    # -----------------------------
    def save_outputs(self):
        os.makedirs("data/processed", exist_ok=True)

        self.stats["rows_after_cleaning"] = len(self.df)
        self.stats["rows_removed"] = self.original_rows - len(self.df)
        self.stats["retention_rate"] = round(
            (len(self.df) / self.original_rows) * 100, 2
        )

        self.stats["missing_values_after"] = self.df.isnull().sum().to_dict()

        self.df.to_csv(
            "data/processed/cleaned_transactions.csv",
            index=False
        )

        with open(
            "data/processed/cleaning_statistics.json",
            "w"
        ) as f:
            json.dump(self.stats, f, indent=4)

    # -----------------------------
    # Run Full Pipeline
    # -----------------------------
    def run_pipeline(self):
        self.remove_missing_customer_ids()
        self.remove_cancelled_invoices()
        self.remove_negative_quantities()
        self.remove_invalid_prices()
        self.remove_missing_descriptions()
        self.remove_outliers()
        self.remove_duplicates()
        self.add_derived_columns()
        self.convert_data_types()
        self.save_outputs()

        print("Data cleaning pipeline completed successfully!")
        print(f"Final dataset shape: {self.df.shape}")

        return self.df


if __name__ == "__main__":
    cleaner = DataCleaner("data/raw/online_retail.csv")
    cleaner.run_pipeline()
