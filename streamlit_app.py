import streamlit as st
import pandas as pd
import os
from src.predict import predict_churn

st.set_page_config(
    page_title="E-Commerce Churn Prediction",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Single Prediction", "Batch Prediction", "Dashboard", "Documentation"]
)

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
if page == "Home":
    st.title("📊 E-Commerce Customer Churn Prediction")

    st.markdown("""
    This application predicts whether a customer is likely to churn.

    **Model Used:** Logistic Regression  
    **Features:** RFM + Behavioral + Temporal Features  
    **Deployment:** Streamlit  
    """)

    st.info("Use the sidebar to navigate through the application.")


# -------------------------------------------------
# SINGLE PREDICTION
# -------------------------------------------------
elif page == "Single Prediction":
    st.title("🔍 Single Customer Prediction")

    st.markdown("Enter customer feature values below:")

    uploaded = st.file_uploader(
        "Upload a single customer CSV (one row)",
        type=["csv"]
    )

    if uploaded is not None:
        input_df = pd.read_csv(uploaded)

        st.write("### Uploaded Data")
        st.dataframe(input_df)

        if st.button("Predict"):
            result = predict_churn(input_df)

            st.write("### Prediction Result")
            st.dataframe(result[["churn_probability", "churn_prediction"]])

            prob = result["churn_probability"].iloc[0]
            st.metric("Churn Probability", f"{prob:.2f}")


# -------------------------------------------------
# BATCH PREDICTION
# -------------------------------------------------
elif page == "Batch Prediction":
    st.title("📂 Batch Customer Prediction")

    uploaded_file = st.file_uploader(
        "Upload CSV file for batch prediction",
        type=["csv"]
    )

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)

        st.write("### Uploaded Data")
        st.dataframe(batch_df.head())

        if st.button("Run Batch Prediction"):
            results = predict_churn(batch_df)

            st.write("### Prediction Results")
            st.dataframe(results.head())

            st.download_button(
                label="Download Results CSV",
                data=results.to_csv(index=False),
                file_name="churn_predictions.csv",
                mime="text/csv"
            )


# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
elif page == "Dashboard":
    st.title("📈 Model Dashboard")

    dataset_path = os.path.join("data", "processed", "model_ready_dataset.csv")

    if os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)

        churn_rate = df["churn"].mean()

        col1, col2 = st.columns(2)

        col1.metric("Total Customers", len(df))
        col2.metric("Churn Rate", f"{churn_rate:.2%}")

        st.write("### Churn Distribution")
        st.bar_chart(df["churn"].value_counts())

    else:
        st.warning("Dataset not found.")


# -------------------------------------------------
# DOCUMENTATION
# -------------------------------------------------
elif page == "Documentation":
    st.title("📄 Project Documentation")

    st.markdown("""
    ### Model Details
    - Algorithm: Logistic Regression
    - Evaluation Metric: ROC-AUC
    - Cross-Validation: 5-Fold Stratified

    ### Features Used
    - Recency
    - Frequency
    - Monetary
    - Behavioral Features
    - Temporal Features

    ### Usage Instructions
    1. Upload customer CSV file.
    2. Click predict.
    3. Download results.

    ### Developed For
    E-Commerce Churn Prediction Project
    """)
