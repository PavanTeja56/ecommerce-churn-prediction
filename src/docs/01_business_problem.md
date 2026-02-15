# Business Problem Statement

## 1. Business Context

The e-commerce industry operates in a highly competitive environment where customer retention is critical for sustained revenue growth. Studies show that acquiring a new customer can cost between 5 to 25 times more than retaining an existing one.

RetailCo Analytics, an e-commerce analytics company, is experiencing customer attrition where customers stop purchasing without explicit signals. This silent churn leads to revenue loss and inefficient marketing spend.

## 2. Problem Definition

The objective of this project is to predict customer churn.

**Churn Definition:**
A customer is considered churned if they do not make any purchase in the next 90 days.

This is framed as a binary classification problem:
- 1 → Churned customer
- 0 → Active customer

## 3. Stakeholders

- **Marketing Team:** Identify customers for retention campaigns
- **Sales Team:** Forecast revenue loss due to churn
- **Product Team:** Understand customer behavior patterns
- **Executive Team:** Measure ROI and business impact

## 4. Business Impact

- Reduce customer churn by 15–20%
- Increase customer lifetime value
- Improve marketing efficiency through targeted campaigns
- Reduce customer acquisition costs

## 5. Success Metrics

**Primary Metric**
- ROC-AUC Score ≥ 0.78

**Secondary Metrics**
- Precision ≥ 0.75
- Recall ≥ 0.70
- F1-Score ≥ 0.72
