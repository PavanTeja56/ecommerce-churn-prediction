# Churn Definition

## Time Window Design

The dataset spans from December 2009 to December 2010.

The data was divided into:

- **Observation Window:** First 9 months
- **Churn Window:** Last 4 months

This prevents data leakage and ensures proper temporal separation.

---

## Churn Logic

A customer is labeled as:

- **Churned (1):**
  Purchased in the observation window but made no purchase in the churn window.

- **Active (0):**
  Made at least one purchase in the churn window.

---

## Final Churn Distribution

Approximately 42% churn rate.

This is considered balanced and suitable for binary classification modeling.
