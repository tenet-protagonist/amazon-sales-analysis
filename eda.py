import numpy as np
import textwrap
import pandas as pd

def eda(df_catalog, df_timeline):

    # basic KPIs

    total_products = len(df_catalog)

    # products rated 4.5+
    high_rating_mask = df_catalog['product_rating'] >= 4.5

    top_rated_products_percentage = (high_rating_mask.mean() * 100)
    average_rating = df_catalog['product_rating'].mean()

    # products that actually have discounts
    discounted_products = df_catalog[df_catalog['discount_percentage'] > 0]

    average_discount = discounted_products['discount_percentage'].mean()
    discounted_products_percentage = (len(discounted_products) / total_products) * 100

    # price tracking over time

    # average product price per collection date
    # use mean
    grouped_prices = (
        df_timeline
        .groupby(['title', 'data_collected_at'])
        ['product_discounted_price']
        .mean()
        .reset_index()
    )

    # self join to compare old/new prices
    # not the most elegant solution
    joined_prices = grouped_prices.merge(
        grouped_prices,
        on='title',
        suffixes=('_from', '_to')
    )

    # keep only forward-moving
    joined_prices = joined_prices[joined_prices['data_collected_at_to'] > joined_prices['data_collected_at_from']]

    # calculate changes

    joined_prices['price_change'] = (
        joined_prices['product_discounted_price_to'] -
        joined_prices['product_discounted_price_from']
    ).round(2)

    joined_prices['price_change_percentage'] = (
        (
            joined_prices['price_change'] /
            joined_prices['product_discounted_price_from']
        ) * 100
    ).round(2)

    # biggest increase / decrease
    # TODO: maybe later track by category too
    biggest_price_jump = (
        joined_prices
        .nlargest(1, 'price_change')
        .iloc[0]
    )

    biggest_price_drop = (
        joined_prices
        .nsmallest(1, 'price_change')
        .iloc[0]
    )

    # title formatting

    # wrapping because some amazon titles are absolutely ridiculous lol
    biggest_jump_title = '\n'.join(
        textwrap.wrap(
            biggest_price_jump['title'],
            width=30
        )[:3]
    )

    biggest_drop_title = '\n'.join(
        textwrap.wrap(
            biggest_price_drop['title'],
            width=30
        )[:3]
    )

    # pretty labels for dashboard cards

    biggest_jump_value = (
        f"+${biggest_price_jump['price_change']:.0f} "
        f"(+{biggest_price_jump['price_change_percentage']:.0f}%)"
    )

    biggest_drop_value = (
        f"-${abs(biggest_price_drop['price_change']):.0f} "
        f"({biggest_price_drop['price_change_percentage']:.0f}%)"
    )

    # "value for money" metric

    median_price = df_catalog['product_discounted_price'].median()

    # cheap-ish + well rated
    value_mask = (
        (df_catalog['product_discounted_price'] <= median_price) &
        (df_catalog['product_rating'] >= 4.5)
    )

    top_rated_below_median_price = (
        value_mask.mean() * 100
    )

    # final output

    metrics = {
        'total_products': total_products,
        'top_rated_pct': top_rated_products_percentage,
        'avg_rating': average_rating,
        'avg_disc_when_on': average_discount,
        'pct_discounted': discounted_products_percentage,
        'largest_price_increase': biggest_price_jump,
        'largest_price_decrease': biggest_price_drop,
        'largest_price_increase_product_title': biggest_jump_title,
        'largest_price_increase_value': biggest_jump_value,
        'largest_price_decrease_product_title': biggest_drop_title,
        'largest_price_decrease_value': biggest_drop_value,
        'median_price': median_price,
        'value_for_money': top_rated_below_median_price
    }
    # maybe eventually convert this into a dataclass
    # leaving dict for now because it's flexible enough

    return metrics