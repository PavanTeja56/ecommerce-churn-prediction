# Data Cleaning Strategy

This document outlines the strategy used to clean the raw e-commerce transaction data prior to feature engineering and modeling.

---

## 1. Missing Values Strategy

### Customer ID (Missing: 20.54%)

**Decision:** DROP rows with missing Customer ID

**Reasoning:**
Customer-level churn prediction requires a valid Customer ID to aggregate transactions. Rows without Customer ID cannot be associated with any customer and therefore provide no value for churn modeling.

**Impact:**
- Rows removed: 107,927
- Remaining data retains identifiable customer behavior.

---

### Description (Missing: ~0.56%)

**Decision:** DROP rows with missing Description

**Reasoning:**
Product descriptions are required for product-level analysis and feature engineering. Missing descriptions represent a very small percentage of the data and can be safely removed without significant data loss.

**Impact:**
- Minimal row reduction
- Improves data consistency

---

## 2. Handling Cancellations

**Issue:**
Invoices starting with the letter `'C'` represent cancelled transactions.

**Chosen Strategy:** REMOVE cancelled invoices

**Reasoning:**
Cancelled invoices do not represent completed purchases and would distort monetary and frequency-based features if included.

**Impact:**
- Cancelled invoices removed: ~10,206
- Revenue and purchase counts become accurate

---

## 3. Negative Quantities

**Issue:**
Negative quantities indicate product returns.

**Strategy:** REMOVE rows with negative quantities

**Reasoning:**
Returned items should not be counted as successful purchases. Including them would negatively affect revenue, frequency, and recency calculations.

**Impact:**
- Negative quantity rows removed: ~12,326
- Ensures all remaining transactions represent actual sales

---

## 4. Outlier Handling

### Quantity Outliers
- **Detection Method:** Interquartile Range (IQR)
- **Action:** Remove extreme outliers beyond IQR bounds

### Price Outliers
- **Strategy:** Remove zero or negative prices and extreme price outliers

**Reasoning:**
Outliers can heavily skew statistical measures and negatively impact model performance.

---

## 5. Data Type Conversions

- **InvoiceDate:** Converted to datetime format
- **Customer ID:** Converted to integer after handling missing values
- **Price & Quantity:** Ensured numeric types

---

## 6. Duplicate Handling

**Strategy:** Remove exact duplicate rows

**Reasoning:**
Duplicate records artificially inflate transaction counts and revenue.

**Impact:**
- Duplicate rows removed: ~6,865

---

## Summary

This cleaning strategy ensures:
- No missing customer identifiers
- Only valid, completed transactions
- Reduced noise and outliers
- High-quality input for feature engineering and modeling
