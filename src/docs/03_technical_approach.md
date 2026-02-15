# Technical Approach

## Problem Framing

Customer churn prediction is framed as a **classification problem** rather than regression because the business decision is binary: churned or active.

## Feature Engineering Strategy

Transactional data will be aggregated at the customer level. Features will include:
- RFM (Recency, Frequency, Monetary)
- Behavioral patterns
- Temporal activity features
- Product diversity metrics

## Modeling Strategy

Multiple algorithms will be evaluated to capture different data patterns:
- Logistic Regression (baseline)
- Decision Tree
- Random Forest
- Gradient Boosting / XGBoost
- Neural Network

## Deployment Strategy

The final model will be deployed using:
- Streamlit for web interface
- Docker for reproducible evaluation
- Joblib for model persistence
