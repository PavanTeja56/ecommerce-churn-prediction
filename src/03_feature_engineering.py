import pandas as pd
import numpy as np
import json
import os

class FeatureEngineer:
    def __init__(self, input_path):
        self.df = pd.read_csv(input_path)
        self.df["InvoiceDate"] = pd.to_datetime(self.df["InvoiceDate"])

        self.features = None

    def define_time_windows(self):
        self.max_date = self.df["InvoiceDate"].max()
        self.churn_window_start = self.max_date - pd.DateOffset(months=3)
        self.observation_window_end = self.churn_window_start

        print("Max Date:", self.max_date)
        print("Observation Window End:", self.observation_window_end)
        print("Churn Window Start:", self.churn_window_start)

    def split_data(self):
        self.observation_df = self.df[
            self.df["InvoiceDate"] < self.observation_window_end
        ]

        self.churn_df = self.df[
            self.df["InvoiceDate"] >= self.churn_window_start
        ]

        print("Observation shape:", self.observation_df.shape)
        print("Churn window shape:", self.churn_df.shape)

    def create_churn_label(self):
        customers_in_churn = self.churn_df["CustomerID"].unique()

        # Create base customer dataframe from observation window
        self.features = self.observation_df.groupby("CustomerID").agg({
            "InvoiceDate": "max"
        }).reset_index()

        # Churn label
        self.features["churn"] = np.where(
            self.features["CustomerID"].isin(customers_in_churn),
            0,
            1
        )

        print("Churn distribution:")
        print(self.features["churn"].value_counts(normalize=True))
        self.features = self.features.drop(columns=["InvoiceDate"])


    def create_rfm_features(self):
        print("\nCreating RFM features...")

        snapshot_date = self.observation_df["InvoiceDate"].max()

        rfm = self.observation_df.groupby("CustomerID").agg({
            "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
            "InvoiceNo": "nunique",
            "TotalPrice": "sum",
            "Quantity": "sum"
        }).reset_index()

        rfm.columns = [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary",
            "TotalQuantity"
        ]

        # Average Order Value
        avg_order_value = self.observation_df.groupby("CustomerID").agg({
            "TotalPrice": "sum",
            "InvoiceNo": "nunique"
        })

        avg_order_value["AvgOrderValue"] = (
            avg_order_value["TotalPrice"] / avg_order_value["InvoiceNo"]
        )

        avg_order_value = avg_order_value[["AvgOrderValue"]].reset_index()

        # Merge RFM features
        self.features = self.features.merge(rfm, on="CustomerID", how="left")
        self.features = self.features.merge(avg_order_value, on="CustomerID", how="left")

        print("RFM features created.")

    def create_behavioral_features(self):
        print("\nCreating Behavioral features...")

        # First and last purchase
        customer_dates = self.observation_df.groupby("CustomerID").agg({
            "InvoiceDate": ["min", "max"],
            "InvoiceNo": "nunique"
        })

        customer_dates.columns = [
            "FirstPurchaseDate",
            "LastPurchaseDate",
            "TotalInvoices"
        ]

        customer_dates = customer_dates.reset_index()

        # Customer lifetime
        customer_dates["CustomerLifetimeDays"] = (
            customer_dates["LastPurchaseDate"] -
            customer_dates["FirstPurchaseDate"]
        ).dt.days

        # Avoid division by zero
        customer_dates["AvgDaysBetweenPurchases"] = np.where(
            customer_dates["TotalInvoices"] > 1,
            customer_dates["CustomerLifetimeDays"] /
            (customer_dates["TotalInvoices"] - 1),
            0
        )

        # Purchase rate per month
        customer_dates["PurchaseRatePerMonth"] = (
            customer_dates["TotalInvoices"] /
            (customer_dates["CustomerLifetimeDays"] / 30 + 1)
        )

        # Merge into main feature table
        self.features = self.features.merge(
            customer_dates[[
                "CustomerID",
                "TotalInvoices",
                "CustomerLifetimeDays",
                "AvgDaysBetweenPurchases",
                "PurchaseRatePerMonth"
            ]],
            on="CustomerID",
            how="left"
        )

        print("Behavioral features created.")

    def create_temporal_features(self):
        print("\nCreating Temporal features...")

        df = self.observation_df.copy()

        # Weekend flag
        df["IsWeekend"] = df["DayOfWeek"].isin([5, 6]).astype(int)

        # Evening flag (5PM to 10PM)
        df["IsEvening"] = df["Hour"].between(17, 22).astype(int)

        temporal = df.groupby("CustomerID").agg({
            "IsWeekend": "mean",
            "IsEvening": "mean",
            "Month": "nunique",
            "DayOfWeek": "nunique"
        }).reset_index()

        temporal.columns = [
            "CustomerID",
            "WeekendPurchaseRatio",
            "EveningPurchaseRatio",
            "UniqueActiveMonths",
            "UniqueActiveDays"
        ]

        # Purchase variance across months
        month_counts = df.groupby(["CustomerID", "Month"])["InvoiceNo"].nunique().reset_index()

        month_var = month_counts.groupby("CustomerID")["InvoiceNo"].std().reset_index()
        month_var.columns = ["CustomerID", "MonthlyPurchaseVariance"]

        temporal = temporal.merge(month_var, on="CustomerID", how="left")

        # Fill NaN variance with 0
        temporal["MonthlyPurchaseVariance"] = temporal["MonthlyPurchaseVariance"].fillna(0)

        self.features = self.features.merge(temporal, on="CustomerID", how="left")

        print("Temporal features created.")

    def save_final_features(self):
        os.makedirs("data/processed", exist_ok=True)

        self.features.to_csv(
            "data/processed/customer_features.csv",
            index=False
        )

        print("Final customer features saved.")


    def create_product_features(self):
        print("\nCreating Product Diversity features...")

        df = self.observation_df.copy()

        # Unique products per customer
        product_stats = df.groupby("CustomerID").agg({
            "StockCode": "nunique",
            "Quantity": "sum",
            "InvoiceNo": "nunique"
        }).reset_index()

        product_stats.columns = [
            "CustomerID",
            "UniqueProducts",
            "TotalQuantityCheck",
            "TotalInvoicesCheck"
        ]

        # Product diversity ratio
        product_stats["ProductDiversityRatio"] = (
            product_stats["UniqueProducts"] /
            product_stats["TotalInvoicesCheck"]
        )

        # Avg items per invoice
        product_stats["AvgItemsPerInvoice"] = (
            product_stats["TotalQuantityCheck"] /
            product_stats["TotalInvoicesCheck"]
        )

        # Repeat purchase ratio
        product_counts = df.groupby(["CustomerID", "StockCode"]).size().reset_index(name="Count")

        repeat_stats = product_counts.groupby("CustomerID")["Count"].apply(
            lambda x: (x > 1).mean()
        ).reset_index()

        repeat_stats.columns = ["CustomerID", "RepeatPurchaseRatio"]

        product_stats = product_stats.merge(repeat_stats, on="CustomerID", how="left")

        # Top product concentration
        top_product = product_counts.groupby("CustomerID")["Count"].max().reset_index()
        total_products = product_counts.groupby("CustomerID")["Count"].sum().reset_index()

        top_product = top_product.merge(total_products, on="CustomerID")
        top_product["TopProductConcentration"] = (
            top_product["Count_x"] / top_product["Count_y"]
        )

        top_product = top_product[["CustomerID", "TopProductConcentration"]]

        product_stats = product_stats.merge(top_product, on="CustomerID", how="left")

        # Keep only final columns
        product_stats = product_stats[[
            "CustomerID",
            "UniqueProducts",
            "ProductDiversityRatio",
            "AvgItemsPerInvoice",
            "RepeatPurchaseRatio",
            "TopProductConcentration"
        ]]

        self.features = self.features.merge(product_stats, on="CustomerID", how="left")

        print("Product Diversity features created.")

    def create_engagement_features(self):
        print("\nCreating Engagement features...")

        df = self.observation_df.copy()

        # Total active months
        active_months = df.groupby("CustomerID")["Month"].nunique().reset_index()
        active_months.columns = ["CustomerID", "ActiveMonths"]

        revenue = df.groupby("CustomerID")["TotalPrice"].sum().reset_index()
        revenue.columns = ["CustomerID", "TotalRevenue"]

        quantity = df.groupby("CustomerID")["Quantity"].sum().reset_index()
        quantity.columns = ["CustomerID", "TotalQuantityCheck2"]

        invoices = df.groupby("CustomerID")["InvoiceNo"].nunique().reset_index()
        invoices.columns = ["CustomerID", "TotalInvoicesCheck2"]

        engagement = active_months.merge(revenue, on="CustomerID")
        engagement = engagement.merge(quantity, on="CustomerID")
        engagement = engagement.merge(invoices, on="CustomerID")

        engagement["RevenuePerMonth"] = (
            engagement["TotalRevenue"] / engagement["ActiveMonths"]
        )

        engagement["QuantityPerMonth"] = (
            engagement["TotalQuantityCheck2"] / engagement["ActiveMonths"]
        )

        engagement["InvoiceFrequencyScore"] = (
            engagement["TotalInvoicesCheck2"] / engagement["ActiveMonths"]
        )

        # Normalize Recency & Monetary (min-max)
        recency_min = self.features["Recency"].min()
        recency_max = self.features["Recency"].max()

        monetary_min = self.features["Monetary"].min()
        monetary_max = self.features["Monetary"].max()

        self.features["RecencyScore"] = (
            (self.features["Recency"] - recency_min) /
            (recency_max - recency_min + 1e-6)
        )

        self.features["MonetaryScore"] = (
            (self.features["Monetary"] - monetary_min) /
            (monetary_max - monetary_min + 1e-6)
        )

        engagement = engagement[[
            "CustomerID",
            "RevenuePerMonth",
            "QuantityPerMonth",
            "InvoiceFrequencyScore"
        ]]

        self.features = self.features.merge(engagement, on="CustomerID", how="left")

        # Composite engagement score
        self.features["EngagementScore"] = (
            self.features["Frequency"] *
            self.features["MonetaryScore"] *
            (1 - self.features["RecencyScore"])
        )

        print("Engagement features created.")
    
    def create_advanced_features(self):
        print("\nCreating Advanced Interaction Features...")

        df = self.features.copy()

        # -------------------
        # 1. RFM Quartile Scores (Robust Version)
        # -------------------

        df["R_Quartile"] = pd.qcut(
            df["Recency"],
            q=4,
            labels=False,
            duplicates="drop"
        )

        df["F_Quartile"] = pd.qcut(
            df["Frequency"],
            q=4,
            labels=False,
            duplicates="drop"
        )

        df["M_Quartile"] = pd.qcut(
            df["Monetary"],
            q=4,
            labels=False,
            duplicates="drop"
        )

        df["RFM_Score"] = (
            df["R_Quartile"] +
            df["F_Quartile"] +
            df["M_Quartile"]
        )


        # -------------------
        # 2. Interaction Features
        # -------------------
        df["Recency_Frequency"] = df["Recency"] * df["Frequency"]
        df["Monetary_Frequency"] = df["Monetary"] * df["Frequency"]
        df["Recency_Monetary"] = df["Recency"] * df["Monetary"]

        # -------------------
        # 3. Log Transformations
        # -------------------
        df["Log_Monetary"] = np.log1p(df["Monetary"])
        df["Log_Frequency"] = np.log1p(df["Frequency"])
        df["Log_Recency"] = np.log1p(df["Recency"])

        # -------------------
        # 4. Risk Flags
        # -------------------
        df["High_Recency_Flag"] = (df["Recency"] > df["Recency"].median()).astype(int)
        df["Low_Frequency_Flag"] = (df["Frequency"] < df["Frequency"].median()).astype(int)
        df["Low_Monetary_Flag"] = (df["Monetary"] < df["Monetary"].median()).astype(int)

        # -------------------
        # 5. Recency Buckets
        # -------------------
        df["Recency_Bucket"] = pd.cut(
            df["Recency"],
            bins=[-1,30,60,90,180,365],
            labels=False
        )

        self.features = df

        print("Advanced features created.")




    def run_pipeline(self):
        self.define_time_windows()
        self.split_data()
        self.create_churn_label()
        self.create_rfm_features()
        self.create_behavioral_features()
        self.create_temporal_features()
        self.create_product_features()
        self.create_engagement_features()
        self.create_advanced_features()
        self.save_final_features()



if __name__ == "__main__":

    engineer = FeatureEngineer(
        "data/processed/cleaned_transactions.csv"
    )
    engineer.run_pipeline()
