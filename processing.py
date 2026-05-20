import json
import re
import numpy as np
import pandas as pd

from config import SEGMENT_ORDER, category_map_path

# dataset cleaning / transformation

def clean_dataset(df_messy: pd.DataFrame):

    # keeping a copy because pandas mutation bugs are annoying
    raw_df = df_messy.copy()

    # 2.1 ratings
    # example: "4.7 out of 5 stars"
    cleaned_ratings = (
        raw_df['rating']
        .astype(str)
        .str.replace(' out of 5 stars', '', regex=False)
        .str.strip()
    )

    raw_df['product_rating'] = pd.to_numeric(
        cleaned_ratings,
        errors='coerce'
    )

    # 2.2 review counts
    reviews_cleaned = (
        raw_df['number_of_reviews']
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.strip()
    )

    raw_df['product_reviews_count'] = pd.to_numeric(
        reviews_cleaned,
        errors='coerce'
    ).astype('Int64')

    # 2.3 bought in last month

    # sample values:
    # "6K+ bought in past month"
    # "400+ bought in past month"

    bought_text = (
        raw_df['bought_in_last_month']
        .astype(str)
        .str.replace('+ bought in past month', '', regex=False)
        .str.replace('K', '000', regex=False)
        .str.strip()
    )

    # NOTE:
    # this "K" replacement isn't technically perfect
    # ex: 1.5K becomes 1.500
    # but current dataset doesn't seem to have decimals

    raw_df['product_bought_in_last_month'] = pd.to_numeric(
        bought_text,
        errors='coerce'
    ).astype('Int64')

    # 2.4 variant/base price
    variant_price_text = (
        raw_df['price_on_variant']
        .astype(str)
        .str.replace('basic variant price: $', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.strip()
    )

    raw_df['product_variant_price'] = pd.to_numeric(
        variant_price_text,
        errors='coerce'
    )

    # 2.5 discounted/current price

    # values usually look like:
    # "1,579.99$"
    # "8.99$"
    # or missing

    discounted_price_text = (
        raw_df['current/discounted_price']
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.replace('$', '', regex=False)
        .str.strip()
    )

    raw_df['product_discounted_price'] = pd.to_numeric(
        discounted_price_text,
        errors='coerce'
    )

    # fallback to variant price if discounted price missing
    # probably not ideal but better than NaNs everywhere later
    raw_df['product_discounted_price'] = (
        raw_df['product_discounted_price']
        .fillna(raw_df['product_variant_price'])
    )

    # 2.6 listed/original price
    listed_price_text = (
        raw_df['listed_price']
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.replace('$', '', regex=False)
        .str.strip()
    )

    raw_df['product_listed_price'] = pd.to_numeric(
        listed_price_text,
        errors='coerce'
    )

    # backup fill
    raw_df['product_listed_price'] = (
        raw_df['product_listed_price']
        .fillna(raw_df['product_discounted_price'])
    )

    # 2.7 best seller flag
    raw_df['product_is_best_seller'] = (

        raw_df['is_best_seller']
        .astype(str)
        .str.lower()
        .str.strip()

        == 'best seller'

    ).astype(int)

    # 2.8 sponsored flag
    raw_df['product_is_sponsored'] = (

        raw_df['is_sponsored']
        .astype(str)
        .str.lower()
        .str.strip()

        == 'sponsored'

    ).astype(int)

    # 2.9 coupon flag
    raw_df['product_has_coupon'] = (

        raw_df['is_couponed']
        .astype(str)
        .str.lower()
        .str.contains('save ', na=False)

    ).astype(int)

    # 2.10 collection timestamp
    raw_df['data_collected_at'] = pd.to_datetime(
        raw_df['collected_at'],
        errors='coerce'
    )

    # 2.11 discount percentage
    # avoid divide-by-zero weirdness
    raw_df['discount_percentage'] = np.where(
        raw_df['product_listed_price'] > 0,
        (1 - (raw_df['product_discounted_price'] / raw_df['product_listed_price'])) * 100,
        0
    )

    raw_df['discount_percentage'] = (
        raw_df['discount_percentage']
        .round(2)
        .fillna(0)
    )

    # 2.12 category mapping
    # default bucket
    raw_df['product_category'] = 'Other Electronics'

    # lowercase once instead of inside loops
    product_titles = (
        raw_df['title']
        .fillna('')
        .str.lower()
    )

    with open(category_map_path, 'r', encoding='utf-8') as file:
        category_json = json.load(file)

    # category assignment

    # this is intentionally simple right now
    # regex approach worked but became harder to debug later
    for category_name, keyword_list in category_json.items():

        # skip empty groups just in case
        if len(keyword_list) == 0:
            continue

        for keyword in keyword_list:

            # making keyword lowercase for safer matching
            keyword = str(keyword).lower()

            # NOTE:
            # using apply here is slower than vectorized methods,
            # but honestly easier to reason about during debugging
            category_mask = (
                product_titles.apply(lambda title_text: keyword in title_text)
            ) & (
                raw_df['product_category'] == 'Other Electronics'
            )

            raw_df.loc[category_mask, 'product_category'] = category_name

    # 2.13 price segmentation

    # rough ecommerce pricing buckets
    # these were picked manually after looking at distribution
    price_bins = [0, 15, 30, 85, 224, 600, np.inf]

    raw_df['product_price_segment'] = pd.cut(
        raw_df['product_discounted_price'],
        bins=price_bins,
        labels=SEGMENT_ORDER
    )

    raw_df['product_price_segment'] = (
        raw_df['product_price_segment']
        .astype('category')
    )

    # final cleaned dataframe

    selected_columns = (
        ['title', 'data_collected_at', 'discount_percentage'] +
        [col_name for col_name in raw_df.columns
         if col_name.startswith('product_') and col_name != 'product_variant_price']
    )

    df_clean = raw_df[selected_columns].copy()

    # column ordering

    # manually arranging because dashboard/export looked weird before
    # yeah this indexing looks ugly but it works
    new_column_order = df_clean.columns[
        [0, 4, 5, 6, 8, 7, 2, 9, 10, 11, 12, 13, 1, 3]
    ]

    df_clean = df_clean.reindex(
        columns=new_column_order
    )

    # outputs

    # latest unique products only
    df_catalog = (
        df_clean
        .sort_values('data_collected_at')
        .drop_duplicates(subset=['title'], keep='last')
    )

    # keep historical rows too
    df_timeline = df_clean.copy()

    return df_catalog, df_timeline

# might add validation checks later
# ex: assert no negative prices etc.