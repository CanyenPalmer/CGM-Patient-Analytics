# CGM Patient Analytics

![GitHub last commit](https://img.shields.io/github/last-commit/CanyenPalmer/CGM-Patient-Analytics)
![GitHub repo size](https://img.shields.io/github/repo-size/CanyenPalmer/CGM-Patient-Analytics)
![Top language](https://img.shields.io/github/languages/top/CanyenPalmer/CGM-Patient-Analytics)
![Language count](https://img.shields.io/github/languages/count/CanyenPalmer/CGM-Patient-Analytics)

---

## Overview

This project analyzes CGM (Continuous Glucose Monitor) patient billing data to identify discrepancies between billed amounts, received payments, and outstanding patient responsibility.

The objective was to transform fragmented invoice data into a structured analytical system capable of uncovering revenue gaps and supporting financial decision-making.

**Key Outcome:**  
Identified over **$30,000 in unpaid patient responsibility** and provided visibility into billing inefficiencies across the revenue cycle.

---

## Problem

The organization lacked clear visibility into:
- What had been billed vs. what had been paid  
- Outstanding patient responsibility  
- Monthly trends in patient payments  

Data was exported from Brightree but remained unstructured, making it difficult to extract meaningful financial insights.

---

## Approach

Developed a Python-based data pipeline to process and restructure raw invoice data into a usable analytical format.

### Workflow:
- Extracted invoice data via Brightree ad-hoc reporting (~15,000 rows × 25 columns)  
- Cleaned and transformed data using Python (pandas)  
- Engineered a **Patient Responsibility** variable:  

```python
Patient_Responsibility = Invoice_Allow_Amount - Invoice_Detail_Payments
