# Data Cleaning Report

## Overview

This report summarizes the results of the data cleaning pipeline implemented in `src/02_data_cleaning.py`.

The objective was to transform the raw transaction dataset into a clean, analysis-ready dataset suitable for feature engineering and churn modeling.

---

## 1. Original Dataset

- Total Rows: 525,461
- Total Columns: 8

---

## 2. Cleaning Steps Applied

### 1. Removed Missing Customer IDs
- Rows Removed: 107,927

### 2. Removed Cancelled Invoices
- Rows Removed: 9,839

### 3. Removed Negative Quantities
- Rows Removed: 0

### 4. Removed Invalid Prices
- Rows Removed: 31

### 5. Removed Missing Descriptions
- Rows Removed: 0

### 6. Removed Outliers (IQR Method)
- Rows Removed: 59,051

### 7. Removed Duplicate Rows
- Rows Removed: 6,340

---

## 3. Final Dataset

- Final Rows: 342,273
- Total Columns After Feature Addition: 13
- Retention Rate: 65.14%

---

## 4. Derived Columns Added

The following features were added:

- TotalPrice
- Year
- Month
- DayOfWeek
- Hour

---

## 5. Data Validation

All validation checks passed successfully:

- No missing values
- All quantities are positive
- All prices are positive
- CustomerID is integer type
- Date range is valid

Validation report saved at:
`data/processed/validation_report.json`

---

## Conclusion

The dataset is now fully cleaned, standardized, and validated.  
It is ready for customer-level aggregation and feature engineering.
