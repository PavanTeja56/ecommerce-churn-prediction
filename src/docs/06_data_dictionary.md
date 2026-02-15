# Data Dictionary

**Dataset Name:** online_retail.csv  
**Source:** UCI Machine Learning Repository – Online Retail II

---

## Raw Dataset Columns

| Column Name   | Data Type | Description                                         | Example Values             | Missing % | Notes                                   |
|--------------|----------|-----------------------------------------------------|----------------------------|-----------|-----------------------------------------|
| Invoice      | String   | Invoice number; starts with 'C' if cancelled        | 489434, C489435            | 0%        | Used to identify transactions           |
| StockCode    | String   | Product code                                        | 85048, 79323P              | 0%        | Some non-standard product codes exist   |
| Description  | String   | Product description                                 | CHRISTMAS GLASS BALL       | 0.56%     | Cleaned by removing missing values      |
| Quantity     | Integer  | Quantity of product purchased                       | 12, 48                     | 0%        | Negative values indicate returns        |
| InvoiceDate  | DateTime | Date and time of transaction                        | 2009-12-01 07:45:00        | 0%        | Converted to datetime format            |
| Price        | Float    | Price per unit in GBP                               | 6.95, 1.25                 | 0%        | Must be positive                        |
| Customer ID  | Float    | Unique identifier for each customer                 | 13085                      | 20.54%    | Rows removed during cleaning            |
| Country      | String   | Country where customer is located                   | United Kingdom             | 0%        | Majority transactions from UK           |

---

## Notes

- Customer ID is converted to integer after removing missing values.
- Cancelled invoices and returned items are removed during cleaning.
- This dictionary reflects the raw dataset before cleaning operations.
