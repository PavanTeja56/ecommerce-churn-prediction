# 🛒 E-Commerce Customer Churn Prediction

Live App:  
👉 https://ecommerce-churn-prediction-c3izr8vhb5h8ikugbpbveh.streamlit.app/

---

## 📌 Project Overview

This project builds a complete end-to-end Machine Learning pipeline to predict customer churn in an e-commerce business using transactional data.

The system includes:

- Data acquisition & cleaning pipeline
- Feature engineering (RFM + behavioral + temporal features)
- Statistical analysis & EDA
- Model training & evaluation
- Hyperparameter tuning with cross-validation
- Production-ready inference pipeline
- Streamlit web application
- Docker containerization
- Cloud deployment

---

## 🎯 Business Problem

Customer churn significantly impacts revenue in e-commerce businesses.

Objective:
Predict customers likely to churn so that retention campaigns can be targeted effectively.

---

## 📊 Dataset

Source: UCI Machine Learning Repository  
Dataset: Online Retail II  

- Original Rows: 525,461
- Cleaned Rows: 342,273
- Final Customers Modeled: 3,059
- Churn Window: 3 months
- Observation Window: 8 months

---

## 🧠 Feature Engineering

Created 25+ customer-level features including:

### RFM Features
- Recency
- Frequency
- Monetary

### Behavioral Features
- Average Order Value
- Purchase Rate per Month
- Repeat Purchase Ratio
- Product Diversity Ratio

### Temporal Features
- Unique Active Months
- Monthly Purchase Variance
- Customer Lifetime Days

---

## 📈 Exploratory Data Analysis

- 15+ visualizations
- Statistical hypothesis testing
- Significant churn indicators identified:
  - Recency
  - Monetary
  - Frequency
  - Unique Products
  - Customer Lifetime

---

## 🤖 Models Trained

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- Neural Network (MLP)

### Final Selected Model:
Logistic Regression

### Final Performance (Test Set)

- Accuracy: ~0.69
- Precision: ~0.58
- Recall: ~0.58
- F1 Score: ~0.57
- ROC-AUC: ~0.748

---

## 🏗 Project Architecture

Raw Data
↓
Data Cleaning Pipeline
↓
Feature Engineering
↓
Model Training & Cross-Validation
↓
Model Selection
↓
Saved Model + Scaler
↓
Prediction API (predict.py)
↓
Streamlit App
↓
Docker Container
↓
Streamlit Cloud Deployment


---

## 🚀 Deployment

The application is deployed using:

- Streamlit
- Docker
- Streamlit Cloud

Access the live app here:

👉 https://ecommerce-churn-prediction-c3izr8vhb5h8ikugbpbveh.streamlit.app/

---

## 🧪 How to Run Locally

1. Clone repository
2. Install dependencies

```
pip install -r requirements.txt
```
3. Run Streamlit app
```
streamlit run streamlit_app.py
```

### Run with Docker
Buid image:
```
docker build -t churn-app
``` 
Run Container:
```
docker run -p 8501:8501 churn-app
```
Open:
http://localhost:8501

##Project Structure
ecommerce-churn-prediction/
│
├── src/
│   ├── 01_data_acquisition.py
│   ├── 02_data_cleaning.py
│   ├── 03_feature_engineering.py
│   ├── predict.py
│
├── notebooks/
│   ├── EDA & modeling notebooks
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── streamlit_app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── submission.json
└── README.md

##📚 Key Learnings

- Impact of churn window definition on class separability

- Importance of stratified cross-validation

- Building reproducible ML pipelines

- Deploying ML models in production

- Containerizing ML applications using Docker

Author 
Pavan Teja 
Data Science Project - 2026