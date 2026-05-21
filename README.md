<p align="center">
<img src="https://img.shields.io/badge/Python-3.13-green?style=for-the-badge&logo=python&logoColor=yellow"/>
<img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge"/>
</p>

# 🛒 Amazon Product Sales Analysis & Visualization

Exploratory data analysis project built around an Amazon products sales dataset.

🎯 **Business Goal**: Identify which price segments, discount strategies, and listing types (sponsored/organic, best seller/standard) drive the highest customer satisfaction and purchase demand — and translate findings into actionable e-commerce recommendations.

The project focuses on:
- cleaning messy scraped marketplace data
- transforming raw product fields into usable metrics
- generating business-oriented KPIs
- visualizing pricing, ratings, reviews, discounts, and category trends

---

## 🧹 Data Cleaning / ETL
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

## 🔍 Exploratory Data Analysis

The EDA step calculates:
- total products
- average ratings
- percentage of discounted products
- top-rated product share
- largest price increases/decreases
- value-for-money indicators
- discount statistics

---

## 📈 Visualizations

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

## 📊 Key Business Insights

| Insight | Recommendation |
|---|---|
| 1. The **top 5** most reviewed products are all **commodities** (batteries, microSD cards, HDMI cables). Amazon-branded products hold 4 of the top 5 spots | Commodity and basics-tier products dominate demand volume. Competing in these sub-categories requires a price or review count advantage — both heavily held by Amazon Basics |
| 2. Luxury products carry only **2.7%** avg discount vs **9.8–10.3%** for Budget/Economy. Best sellers are discounted more (**11.4%** vs **6.5%**) | For premium segments, avoid deep discounting — it is not expected and may signal lower quality. Use targeted discounts selectively to accelerate review accumulation for best seller candidacy |
| 3. **31%** of products priced below the median (**$79**) still achieve a **4.5+** rating — quality is not exclusive to high price tiers | Highlight value-tier products in marketing. Budget and Economy segments have the highest avg ratings (4.54 and 4.52) — leverage this in positioning |
| 4. Best sellers average **34,562** reviews vs **5,253** for non-best sellers — a **6.6×** gap. Rating difference is minimal (**4.53** vs **4.44**). | Focus on review volume as the primary driver of the badge — not just rating. Prioritise review acquisition strategies over minor rating improvements |
| 5. Largest observed price swing: **+$699 (+35%)** for a conferencing device and **-$152 (-11%)** for a projector within the 10-day window | Monitor high-ticket Electronics and AV categories for dynamic pricing. Large intra-period swings suggest algorithmic repricing — track competitors' price changes to stay competitive |
| 6. Digital Frames is the top-rated category (**4.7★**) and also has the highest avg discount (**12%**) — a rare combination of quality and aggressive pricing | Digital Frames is a high-opportunity niche — strong customer satisfaction with room to reduce discounting without losing quality perception. Worth expanding catalogue depth |

---

## 🛠 Tech Stack

- **Python 3.13**
- **Pandas, Numpy** – data processing
- **Matplotlib** – data visualization

---

## 🚀 Running the Project

1. Clone the repository
```
git clone https://github.com/yourusername/amazon-sales-analysis.git
cd amazon-sales-analysis
```

2. Install dependencies
```
pip install pandas numpy matplotlib
```

3. Run the pipeline
```
python main.py
```

This will:<br>
&ensp;• Load the raw dataset<br>
&ensp;• Clean + transform the data<br>
&ensp;• Run exploratory analysis<br>
&ensp;• Generate visualizations<br>

---

## 💾 Dataset

This project uses the Amazon Products Sales Dataset 42K+ Items - 2025 created by Ikram Sherazi.

Dataset license: CC BY-NC 4.0  
https://creativecommons.org/licenses/by-nc/4.0/

Original dataset source:<br>
https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025/data?select=amazon_products_sales_data_uncleaned.csv

**Raw rows:** 42,675 (multi-day snapshots of the same products)<br>
**Unique products (catalog):** 8,808 (deduplicated by title, latest snapshot kept)<br>
**Fields used:** title, rating, number_of_reviews, bought_in_last_month, price_on_variant, current/discounted_price, listed_price, is_best_seller, is_sponsored, is_couponed, collected_at<br>

Dataset file:

```text
data/amazon_products_sales_data_uncleaned.csv
```

---

## 📝 Notes

A few implementation details:
- some transformations intentionally prioritize robustness over perfection
- price tracking is based on timestamp comparisons
- category normalization uses a JSON mapping file
- matplotlib was used directly instead of higher-level plotting libraries to keep chart customization flexible

---

## 📁 Project Structure

```text
.
├── main.py
├── config.py
├── processing.py
├── eda.py
├── plots.py
├── category_map.json
├── LICENSE.txt
├── LICENSE_DATASET.txt
├── README.md
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

## 👨‍💻 Author

**Name:** Vladyslav Herman<br>
**LinkedIn:** https://www.linkedin.com/in/vladislav-german-b1811b3ba/<br>
**Email:** german.vladislav25@gmail.com

---

## 📄 License
This project is open-source under the MIT License.
