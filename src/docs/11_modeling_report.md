# Modeling Report

## Models Compared

1. Logistic Regression
2. Decision Tree
3. Random Forest
4. Gradient Boosting
5. Neural Network

---

## Best Model: Logistic Regression

### Performance (Threshold = 0.4)

- ROC-AUC: 0.7267
- Recall (Churn): 0.71
- Precision (Churn): 0.53
- F1 Score: 0.61
- Accuracy: 0.66

---

## Why Logistic Regression Won

- Highest ROC-AUC
- Stable generalization
- Better recall after threshold tuning
- Interpretable coefficients

---

## Business Decision

Threshold lowered to 0.4 to improve churn detection.

This increases recall while maintaining acceptable precision.

---

## Key Predictive Features

- UniqueActiveMonths
- UniqueProducts
- PurchaseRatePerMonth
- CustomerLifetimeDays
- MonthlyPurchaseVariance

---

## Conclusion

The final churn model balances predictive performance and business impact.

It is suitable for deployment in customer retention strategies.
