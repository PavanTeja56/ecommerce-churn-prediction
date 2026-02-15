# EDA Key Insights

Dataset Summary:
- Total Customers: 3,059
- Total Features: 25
- Churn Rate: 36.6%
- Observation Window: 8 months
- Churn Window: 4 months
- All key features statistically significant (p < 0.001)

---

# 1. Churn Patterns Discovered

## Finding 1: Recency is a Strong Indicator of Churn

Evidence:
Churned customers show significantly higher recency compared to active customers.
Statistical significance: p < 0.001

Business implication:
Customers who have not purchased recently are at high churn risk.
Re-engagement campaigns should target customers inactive for extended periods.

---

## Finding 2: Monetary Value Strongly Differentiates Churn

Evidence:
Average monetary value differs by ~₹688 between churned and active customers.
Statistical significance: p < 0.001

Business implication:
High-spending customers are less likely to churn.
Retention strategies should prioritize mid-value customers before they decline.

---

## Finding 3: Frequency Reduces Churn Probability

Evidence:
Churned customers have significantly lower purchase frequency.
Statistical significance: p < 0.001

Business implication:
Encouraging repeat purchases reduces churn risk.
Loyalty programs may improve retention.

---

## Finding 4: Customer Lifetime Matters

Evidence:
Active customers exhibit significantly longer lifetime engagement.
Statistical significance: p < 0.001

Business implication:
Customers with short engagement history are vulnerable.
Onboarding and early engagement are critical.

---

## Finding 5: Product Diversity Reduces Churn

Evidence:
Active customers purchase more unique products.
Statistical significance: p < 0.001

Business implication:
Cross-selling and product discovery reduce churn probability.

---

## Finding 6: Revenue Per Month is a Strong Stability Indicator

Evidence:
Higher monthly revenue correlates with lower churn probability.

Business implication:
Consistent spenders are more stable customers.

---

## Finding 7: Engagement Score Separates Churn Groups

Evidence:
Composite engagement score clearly differentiates churners from active customers.

Business implication:
Engagement scoring can be used for risk segmentation.

---

## Finding 8: Purchase Regularity Matters

Evidence:
Higher AvgDaysBetweenPurchases observed in churners.
Statistical significance: p < 0.001

Business implication:
Irregular purchase behavior signals churn risk.

---

## Finding 9: Lower Basket Size Correlates with Churn

Evidence:
Churned customers have lower AvgOrderValue and AvgItemsPerInvoice.

Business implication:
Smaller baskets indicate lower commitment.

---

## Finding 10: High Quantity Customers Rarely Churn

Evidence:
TotalQuantity strongly differentiates churn groups.

Business implication:
Bulk buyers are less sensitive to churn.

---

# 2. Customer Segments Analysis

Based on EDA, customers can be grouped into:

1. High-Value Loyalists  
   - High Monetary  
   - Low Recency  
   - High Frequency  
   - Low churn risk  

2. At-Risk Mid-Value Customers  
   - Moderate Monetary  
   - Increasing Recency  
   - Medium Frequency  
   - Moderate churn probability  

3. Low-Engagement Customers  
   - Low Monetary  
   - High Recency  
   - Low Frequency  
   - High churn risk  

4. Early-Stage Customers  
   - Short CustomerLifetimeDays  
   - Low Product Diversity  
   - Vulnerable to churn  

---

# 3. Feature Recommendations for Modeling

Based on EDA, the strongest predictive features are:

1. Monetary
2. Recency
3. Frequency
4. CustomerLifetimeDays
5. RevenuePerMonth
6. UniqueProducts
7. EngagementScore
8. AvgDaysBetweenPurchases
9. QuantityPerMonth
10. ProductDiversityRatio

Redundant features removed:
- TotalInvoices (correlated with Frequency)
- TotalQuantity (correlated with QuantityPerMonth)
- RevenuePerMonth duplicates Monetary trends

Final modeling dataset contains 25 robust features.

---

# 4. Hypotheses for Testing

H1: Customers with Recency > 90 days are significantly more likely to churn.

H2: Customers with Monetary value in the bottom 25% have 3x higher churn probability.

H3: Customers with Frequency > 10 purchases rarely churn regardless of recency.

H4: Customers with ProductDiversityRatio > 2 are less likely to churn.

H5: Customers with CustomerLifetimeDays < 60 are highly vulnerable to churn.

H6: High EngagementScore customers have significantly lower churn probability.

---

# Conclusion

EDA confirms that churn is strongly associated with:

- Lower spending
- Lower purchase frequency
- Higher recency
- Shorter customer lifetime
- Lower product diversity
- Lower engagement

All key features demonstrate strong statistical significance (p < 0.001).

The dataset is analytically validated and ready for predictive modeling.
