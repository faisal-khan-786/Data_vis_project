# Brazilian E‑commerce Analysis (Olist) – Data Visualization Final Project

This repository contains my final project for **Data Visualization (Summer 2025)** at the **University of Europe, Potsdam**. I analyze the public **Brazilian E‑commerce Dataset by Olist** (~100k marketplace orders, 2016–2018) to surface patterns in growth, category revenue, logistics performance, payments behavior, customer reviews, and retention.

**Author:** Mohammed Faisal Khan  
**Instructor:** Prof. Dina Deifallah  
**Course:** Data Visualization (Summer 2025)  
**Repo:** https://github.com/faisal-khan-786/Data_vis_project  
**Live Dashboard:** https://datavisproject-bk4hpzyykgye9svljfrfhx.streamlit.app/  
**Contact:** Faisalkhan.mys@gmail.com

---

## Goals
- Load and join multiple Olist relational tables (orders, items, payments, reviews, etc.).
- Answer **10 business‑driven analytical questions**, each with a clear visualization.
- Translate findings into actionable insights (marketing focus, logistics, retention).
- Deliver reproducible analysis in a **Jupyter notebook** and a **slide deck**.
- Provide an **interactive Streamlit dashboard** for hands‑on data exploration (bonus).

---

## Dataset

Public Kaggle release from Olist, a Brazilian multi‑seller marketplace. **Data files are stored in this repo**

**Core CSVs used**

| File | Description |
|---|---|
| `olist_orders_dataset.csv` | Order IDs, statuses, timestamps. |
| `olist_order_items_dataset.csv` | Line items: price, freight, seller. |
| `olist_products_dataset.csv` | Product metadata + category (Portuguese). |
| `product_category_name_translation.csv` | Mapping to English category labels. |
| `olist_customers_dataset.csv` | Customer location & persistent `customer_unique_id`. |
| `olist_order_payments_dataset.csv` | Payment type, installments, amounts. |
| `olist_order_reviews_dataset.csv` | Review scores & text. |
| *(Optional)* Sellers & geolocation tables for advanced analysis. |

---

## Key Questions & Visuals

1. Monthly order volume – demand trend.  
2. Top revenue categories – where the money comes from.  
3. Payment method mix – credit vs boleto vs others.  
4. Delivery time by state – fulfillment performance.  
5. Delivery delay vs review score – CX impact.  
6. Repeat vs one‑time customers – retention gap.  
7. Installments vs order value – financing behavior.  
8. Top sellers by review score – quality leaders.  
9. Cancellation rate over time – order risk periods.  
10. Review word cloud – common customer sentiment terms.

---
## Acknowledgments

- **Dataset:** *Brazilian E‑Commerce Public Dataset by Olist* (Kaggle).
- **Course guidance:** Dina Deifallah, University of Europe, Potsdam.
