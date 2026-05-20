# Amazon Product Sales Analysis & Visualization

Small exploratory data analysis project built around an Amazon products sales dataset.

The project focuses on:
- cleaning messy scraped marketplace data
- transforming raw product fields into usable metrics
- generating business-oriented KPIs
- visualizing pricing, ratings, reviews, discounts, and category trends

Most of the workflow is written in plain pandas + matplotlib without heavy frameworks.

---

## Project Structure

```text
.
├── main.py
├── config.py
├── processing.py
├── eda.py
├── plots.py
├── category_map.json
│
├── data/
│   └── amazon_products_sales_data_uncleaned.csv
│
└── visualizations/
    ├── best_seller_analysis.png
    ├── category_analysis.png
    ├── discount_by_category.png
    ├── kpi_dashboard.png
    ├── price_segment_analysis.png
	├── quality_vs_demand.png
	├── rating_analysis.png
    └── top_reviewed_products.png
```

---

# Features

## Data Cleaning / ETL
The processing pipeline handles:
- ratings extraction
- review count parsing
- price normalization
- discount calculations
- coupon flags
- sponsored/best-seller flags
- timeline formatting
- category mapping
- price segmentation

Raw scraped marketplace data tends to be messy, so most of the project work happens during transformation.

---

## Exploratory Data Analysis

The EDA step calculates:
- total products
- average ratings
- percentage of discounted products
- top-rated product share
- largest price increases/decreases
- value-for-money indicators
- discount statistics

---

## Visualizations

The project generates multiple charts automatically:

| Visualization | Description |
|---|---|
| KPI Dashboard | High-level business overview |
| Rating Analysis | Distribution of customer ratings |
| Category Analysis | Product/category breakdown |
| Best Seller Analysis | Best seller vs non-best seller comparison |
| Discount Analysis | Discount patterns by category |
| Price Segment Analysis | Metrics grouped by pricing tier |
| Quality vs Demand | Ratings vs review density |
| Top Reviewed Products | Most reviewed products |
| Timeline Trends | Rating/price changes over time |

Generated charts are saved inside:

```text
visualizations/
```

---

# Tech Stack

- Python
- pandas
- numpy
- matplotlib

---

# Installation

Clone the repository:

```bash
git clone <repo-url>
cd amazon-product-analysis
```

Install dependencies:

```bash
pip install pandas numpy matplotlib
```

---

# Running the Project

Run the main pipeline:

```bash
python main.py
```

This will:
1. Load the raw dataset
2. Clean + transform the data
3. Run exploratory analysis
4. Generate visualizations

---

# Dataset

This project uses the Amazon Products Sales Dataset 42K+ Items - 2025 created by Ikram Sherazi.

Dataset license: CC BY-NC 4.0  
https://creativecommons.org/licenses/by-nc/4.0/

Original dataset source:
https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025/data?select=amazon_products_sales_data_uncleaned.csv

Dataset file:

```text
data/amazon_products_sales_data_uncleaned.csv
```

---

# Example Workflow

```text
Raw CSV
   ↓
Data Cleaning / ETL
   ↓
Feature Engineering
   ↓
EDA Metrics
   ↓
Visualization Export
```

---

# Notes

A few implementation details:
- some transformations intentionally prioritize robustness over perfection
- price tracking is based on timestamp comparisons
- category normalization uses a JSON mapping file
- matplotlib was used directly instead of higher-level plotting libraries to keep chart customization flexible

---

# Sample Output

The project automatically exports charts similar to:
- KPI business dashboards
- rating distribution histograms
- pricing trend analysis
- category comparison charts
- review vs quality density plots

All outputs are saved into the `visualizations/` folder.

---

# Author

Name: Vladyslav Herman
LinkedIn: https://www.linkedin.com/in/vladislav-german-b1811b3ba/
Email: german.vladislav25@gmail.com
