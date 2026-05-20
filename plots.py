import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from config import *

def generate_plots(df_catalog, eda_results):

	# KPI DASHBOARD

	fig = plt.figure(figsize=(16, 4.5))

	# dark dashboard theme
	fig.patch.set_facecolor(dark)

	# card data
	dashboard_cards = [

		(
			'Unique Products\nin Catalogue',
			f"{eda_results['total_products']:,}",
			# hardcoded date for now
			# TODO: derive from dataset automatically
			'scraped Aug 21-30',
			'#1A2535'
		),

		(
			'Top-Rated Products\n(rating ≥ 4.5)',
			f"{eda_results['top_rated_pct']:.1f}%",
			f"{int(eda_results['total_products'] * eda_results['top_rated_pct']/100):,} "
			f"out of {eda_results['total_products']:,}",
			'#1A3025'
		),

		(
			'Products Average\nRating',
			f"{eda_results['avg_rating']:.2f} / 5.0",
			'across all categories',
			'#2A1A10'
		),

		(
			'Products with\nActive Discount',
			f"{eda_results['pct_discounted']:.1f}%",
			f"avg {eda_results['avg_disc_when_on']:.1f}% off when discounted",
			'#1A2535'
		),

		(
			'Top Price Increase ↑\nProduct',
			eda_results['largest_price_increase_value'],
			eda_results['largest_price_increase_product_title'],
			'#2A1A1A'
		),

		(
			'Top Price Decrease ↓\nProduct',
			eda_results['largest_price_decrease_value'],
			eda_results['largest_price_decrease_product_title'],
			'#1A2A1A'
		)
	]

	card_colors = [
		orange,
		green,
		orange,
		orange,
		red,
		green
	]

	# render cards

	for idx, ((title, value, subtitle, bg_color), value_color) in enumerate(
		zip(dashboard_cards, card_colors)
	):

		ax = fig.add_subplot(2, 6, idx + 1)

		ax.set_facecolor(bg_color)

		# main value
		ax.text(
			0.5,
			0.72,
			value,
			transform=ax.transAxes,
			fontsize=16,
			fontweight='bold',
			color=value_color,
			ha='center',
			va='center'
		)

		# title
		ax.text(
			0.5,
			0.45,
			title,
			transform=ax.transAxes,
			fontsize=11,
			color='#DDDDDD',
			ha='center',
			va='center',
			linespacing=1.4
		)

		# subtitle / supporting detail
		ax.text(
			0.5,
			0.18,
			subtitle,
			transform=ax.transAxes,
			fontsize=9,
			color='#888888',
			ha='center',
			va='center'
		)

		# remove axis junk
		ax.set_xticks([])
		ax.set_yticks([])

		# border styling
		for spine in ax.spines.values():
			spine.set_edgecolor('#2A3A4A')
			spine.set_linewidth(1.2)

	# bottom insight strip

	insight_ax = fig.add_subplot(2, 1, 2)

	insight_ax.set_facecolor('#0D1B2A')

	insight_text = (
		f"KEY INSIGHTS:\n\n"
		f"· {eda_results['value_for_money']:.0f}% of products priced below "
		f"median (${eda_results['median_price']:.0f}) still achieve a 4.5+ "
		f"rating — strong value-for-money signal in this catalogue.\n"
		f"· Best Seller rate: only "
		f"{df_catalog['product_is_best_seller'].mean() * 100:.1f}% "
		f"({df_catalog['product_is_best_seller'].sum()} products) "
		f"— badge is highly selective."
	)

	insight_ax.text(
		0.02,
		0.8,
		insight_text,
		transform=insight_ax.transAxes,
		fontsize=12,
		color='#EAEAEA',
		ha='left',
		va='top',
		multialignment='left',
		linespacing=1.5
	)

	insight_ax.set_xticks([])
	insight_ax.set_yticks([])

	for spine in insight_ax.spines.values():
		spine.set_edgecolor('#1A3A5A')

	fig.suptitle(
		'AMAZON PRODUCT SALES DATASET  |  BUSINESS INTELLIGENCE OVERVIEW',
		fontsize=12,
		fontweight='bold',
		color='white',
		y=1.01
	)

	plt.tight_layout(pad=0.6, h_pad=0.4)
	plt.savefig(f'{output_path}/kpi_dashboard.png', bbox_inches='tight', facecolor=fig.get_facecolor())
	plt.close()

	# CHART 1 — RATING DISTRIBUTION

	fig, axes = plt.subplots(
		1,
		2,
		figsize=(13, 5)
	)

	ratings = df_catalog['product_rating'].dropna()

	# histogram
	axes[0].hist(
		ratings,
		bins=30,
		color=orange,
		edgecolor='white',
		linewidth=0.4
	)

	# mean marker
	axes[0].axvline(
		ratings.mean(),
		color=blue,
		linestyle='--',
		linewidth=1.8,
		label=f'Mean: {ratings.mean():.2f}'
	)

	# median marker
	axes[0].axvline(
		ratings.median(),
		color=red,
		linestyle=':',
		linewidth=1.5,
		label=f'Median: {ratings.median():.2f}'
	)

	axes[0].set_xlabel('Rating', fontsize=11)
	axes[0].set_ylabel('Number of Products', fontsize=11)

	axes[0].set_title(
		'Rating Distribution',
		fontsize=12,
		fontweight='bold'
	)

	axes[0].legend(fontsize=9)

	# bucketed view

	rating_buckets = pd.cut(
		ratings,
		bins=[0, 2, 3, 4, 4.5, 5],
		labels=['<2★', '2-3★', '3-4★', '4-4.5★', '4.5-5★']
	)

	bucket_counts = (
		rating_buckets
		.value_counts()
		.sort_index()
	)

	bucket_colors = [
		'#D32F2F',
		'#F57C00',
		'#FBC02D',
		'#388E3C',
		'#1B5E20'
	]

	bars = axes[1].bar(
		bucket_counts.index,
		bucket_counts.values,
		color=bucket_colors,
		edgecolor='white'
	)

	axes[1].bar_label(
		bars,
		fmt='%d',
		padding=3,
		fontsize=9,
		fontweight='bold'
	)

	axes[1].set_xlabel('Rating Bucket', fontsize=11)
	axes[1].set_ylabel('Number of Products', fontsize=11)

	axes[1].set_title(
		'Products by Rating Bucket',
		fontsize=12,
		fontweight='bold'
	)

	fig.suptitle(
		'Customer Rating Analysis',
		fontsize=14,
		fontweight='bold',
		y=1.02
	)

	plt.tight_layout()

	plt.savefig(
		f'{output_path}/rating_analysis.png',
		bbox_inches='tight'
	)

	plt.close()

	# CHART 2 — TOP CATEGORIES

	fig, axes = plt.subplots(
		1,
		2,
		figsize=(15, 6)
	)

	# top categories by product count
	category_counts = (
		df_catalog['product_category']
		.value_counts()
		.head(12)
		.sort_values()
	)

	count_colors = [
		orange if i == len(category_counts) - 1
		else '#CCCCCC'
		for i in range(len(category_counts))
	]

	bars = axes[0].barh(
		category_counts.index,
		category_counts.values,
		color=count_colors,
		edgecolor='white'
	)

	axes[0].bar_label(
		bars,
		fmt='%d',
		padding=4,
		fontsize=8.5,
		fontweight='bold'
	)

	axes[0].set_xlabel(
		'Number of Products',
		fontsize=11
	)

	axes[0].set_title(
		'Top 12 Categories by Product Count',
		fontsize=12,
		fontweight='bold'
	)

	# category average ratings

	category_rating = (
		df_catalog
		.groupby('product_category')['product_rating']
		.mean()
		.dropna()
		.sort_values(ascending=False)
		.head(12)
	)

	rating_colors = [
		orange if i == 0 else blue
		for i in range(len(category_rating))
	]

	bars2 = axes[1].barh(
		category_rating.index[::-1],
		category_rating.values[::-1],
		color=rating_colors[::-1],
		edgecolor='white'
	)

	axes[1].bar_label(
		bars2,
		fmt='%.2f',
		padding=4,
		fontsize=8.5,
		fontweight='bold'
	)

	axes[1].set_xlim(0, 5.5)

	avg_rating = df_catalog['product_rating'].mean()

	axes[1].axvline(
		avg_rating,
		color='red',
		linestyle='--',
		linewidth=1.2,
		label=f"Avg: {avg_rating:.2f}"
	)

	axes[1].set_xlabel(
		'Average Rating',
		fontsize=11
	)

	axes[1].set_title(
		'Top 12 Categories by Avg Rating',
		fontsize=12,
		fontweight='bold'
	)

	axes[1].legend(fontsize=9)

	fig.suptitle(
		'Category Analysis',
		fontsize=14,
		fontweight='bold',
		y=1.02
	)

	plt.tight_layout()
	plt.savefig(f'{output_path}/category_analysis.png', bbox_inches='tight')
	plt.close()

	# CHART 3 — PRICE SEGMENT ANALYSIS

	fig, axes = plt.subplots(
		1,
		3,
		figsize=(16, 5)
	)

	# keep configured order only if segment exists in data
	segment_order = [
		seg for seg in SEGMENT_ORDER
		if seg in df_catalog['product_price_segment'].values
	]

	# metrics by segment

	segment_counts = (
		df_catalog['product_price_segment']
		.value_counts()
		.reindex(segment_order)
	)

	segment_rating = (
		df_catalog
		.groupby(
			'product_price_segment',
			observed=True
		)['product_rating']
		.mean()
		.reindex(segment_order)
	)

	segment_discount = (
		df_catalog
		.groupby(
			'product_price_segment',
			observed=True
		)['discount_percentage']
		.mean()
		.reindex(segment_order)
	)

	# render charts


	chart_data = [
		(
			segment_counts,
			'Product Count',
			'{:,.0f}',
			orange
		),

		(
			segment_rating,
			'Avg Rating',
			'{:.2f}',
			blue
		),

		(
			segment_discount,
			'Avg Discount (%)',
			'{:.1f}%',
			'#232F3E'
		)
	]

	for ax, (series, title, fmt, color_used) in zip(
		axes,
		chart_data
	):

		bars = ax.bar(
			range(len(series)),
			series.values,
			color=color_used,
			edgecolor='white'
		)

		# value labels above bars
		for bar, val in zip(bars, series.values):

			if np.isnan(val):
				continue

			ax.text(
				bar.get_x() + (bar.get_width() / 2),
				bar.get_height() + (max(series.dropna()) * 0.01),
				fmt.format(val),
				ha='center',
				fontsize=8,
				fontweight='bold'
			)

		ax.set_xticks(range(len(series)))

		# shorter labels so they don't collide too much
		ax.set_xticklabels(
			[s.split(' ')[0] for s in segment_order],
			fontsize=8,
			rotation=15
		)

		ax.set_title(
			title,
			fontsize=12,
			fontweight='bold'
		)

	fig.suptitle(
		'Price Segment Analysis',
		fontsize=14,
		fontweight='bold',
		y=1.02
	)

	plt.tight_layout()
	plt.savefig(f'{output_path}/price_segment_analysis.png', bbox_inches='tight')
	plt.close()

	# CHART 4 — BEST SELLER VS NON-BEST SELLER

	fig, axes = plt.subplots(
		1,
		3,
		figsize=(14, 5)
	)

	best_sellers = df_catalog[
		df_catalog['product_is_best_seller'] == 1
	]

	regular_products = df_catalog[
		df_catalog['product_is_best_seller'] == 0
	]

	# metric config
	comparison_metrics = [

		(
			'product_rating',
			'Avg Rating',
			'.2f'
		),

		(
			'product_reviews_count',
			'Avg Reviews',
			',.0f'
		),

		(
			'discount_percentage',
			'Avg Discount (%)',
			'.1f'
		)
	]

	for ax, (column_name, chart_title, value_fmt) in zip(
		axes,
		comparison_metrics
	):

		values = [
			regular_products[column_name].mean(),
			best_sellers[column_name].mean()
		]

		bars = ax.bar(
			['Non-Best Seller', 'Best Seller'],
			values,
			color=[grey, orange],
			edgecolor='white',
			width=0.5
		)

		# labels on top
		for bar, val in zip(bars, values):

			ax.text(
				bar.get_x() + (bar.get_width() / 2),
				bar.get_height() + (max(values) * 0.01),
				f'{val:{value_fmt}}',
				ha='center',
				fontsize=10,
				fontweight='bold'
			)

		ax.set_title(
			chart_title,
			fontsize=12,
			fontweight='bold'
		)

	fig.suptitle(
		'Best Seller vs Non-Best Seller',
		fontsize=14,
		fontweight='bold',
		y=1.02
	)

	plt.tight_layout()
	plt.savefig(f'{output_path}/best_seller_analysis.png', bbox_inches='tight')
	plt.close()

	# CHART 5 — QUALITY VS DEMAND

	# preparing clean sample first
	scatter_sample = df_catalog[
		(
			df_catalog['product_rating'].notna()
		) &
		(
			df_catalog['product_reviews_count'].notna()
		)
	].copy()

	# log scale helps compress huge review count differences
	scatter_sample['reviews_log'] = np.log10(
		scatter_sample['product_reviews_count'].astype(float) + 1
	)

	fig, ax = plt.subplots(
		figsize=(13, 7)
	)

	# density hexbin plot
	# honestly works much better than scatter for big datasets
	hb = ax.hexbin(
		scatter_sample['reviews_log'],
		scatter_sample['product_rating'],

		gridsize=30,

		# yellow -> orange -> red
		cmap='YlOrRd',

		# ignore tiny sparse bins
		mincnt=2
	)

	# colorbar

	cbar = plt.colorbar(
		hb,
		ax=ax
	)

	cbar.set_label(
		'Number of Products',
		fontsize=10
	)

	# reference lines

	ax.axhline(
		eda_results['avg_rating'],
		color=green,
		linestyle='--',
		linewidth=1.2,
		alpha=0.7,
		label=f"Avg rating ({eda_results['avg_rating']:.2f})"
	)

	ax.axvline(
		np.log10(10000),
		color=orange,
		linestyle='--',
		linewidth=1.2,
		alpha=0.7,
		label='10K reviews threshold'
	)

	# quadrant labels

	ax.text(
		0.78,
		0.97,

		'HIGH DEMAND\nHIGH QUALITY',

		transform=ax.transAxes,

		fontsize=8.5,
		color='white',
		fontweight='bold',

		va='top',
		ha='center',

		bbox=dict(
			boxstyle='round,pad=0.3',
			facecolor='#1A3025',
			alpha=0.8
		)
	)

	ax.text(
		0.78,
		0.22,

		'HIGH DEMAND\nLOWER QUALITY',

		transform=ax.transAxes,

		fontsize=8.5,
		color='white',
		fontweight='bold',

		va='bottom',
		ha='center',

		bbox=dict(
			boxstyle='round,pad=0.3',
			facecolor='#2A1A1A',
			alpha=0.8
		)
	)

	ax.text(
		0.13,
		0.97,

		'LOW DEMAND\nHIGH QUALITY',

		transform=ax.transAxes,

		fontsize=8.5,
		color='white',
		fontweight='bold',

		va='top',
		ha='center',

		bbox=dict(
			boxstyle='round,pad=0.3',
			facecolor='#1A2535',
			alpha=0.8
		)
	)

	# axis formatting

	ax.set_xticks([1, 2, 3, 4, 5])

	ax.set_xticklabels(
		['10', '100', '1K', '10K', '100K'],
		fontsize=10
	)

	ax.set_xlim(left=1)

	ax.set_ylim(0.8, 5.4)

	ax.set_xlabel(
		'Number of Reviews (log scale)',
		fontsize=12
	)

	ax.set_ylabel(
		'Product Rating',
		fontsize=12
	)

	ax.set_title(
		'Product Quality vs Market Demand — Density View\n'
		'Color intensity = number of products  |  X axis is logarithmic',

		fontsize=13,
		fontweight='bold',
		pad=12
	)

	ax.legend(
		fontsize=9,
		loc='lower right',
		framealpha=0.85
	)

	# keeps hexagons visually balanced
	ax.set_aspect('equal')

	plt.tight_layout()
	plt.savefig(f'{output_path}/quality_vs_demand.png', bbox_inches='tight')
	plt.close()

	# CHART 6 — DISCOUNT BY CATEGORY

	fig, ax = plt.subplots(
		figsize=(11, 6)
	)

	category_discount = (
		df_catalog
		.groupby('product_category')['discount_percentage']
		.mean()
		.sort_values(ascending=True)
		.tail(10)
	)

	discount_colors = [
		orange if i == 9 else '#CCCCCC'
		for i in range(len(category_discount))
	]

	bars = ax.barh(
		category_discount.index,
		category_discount.values,
		color=discount_colors,
		edgecolor='white'
	)

	ax.bar_label(
		bars,
		fmt='%.1f%%',
		padding=4,
		fontsize=9,
		fontweight='bold'
	)

	overall_discount_avg = (
		df_catalog['discount_percentage']
		.mean()
	)

	ax.axvline(
		overall_discount_avg,
		color='red',
		linestyle='--',
		linewidth=1.2,
		label=f"Avg {overall_discount_avg:.1f}%"
	)

	ax.set_xlabel(
		'Average Discount (%)',
		fontsize=11
	)

	ax.set_title(
		'Top 10 Categories by Avg Discount',
		fontsize=14,
		fontweight='bold',
		pad=12
	)

	ax.legend(fontsize=9)

	plt.tight_layout()
	plt.savefig(f'{output_path}/discount_by_category.png', bbox_inches='tight')
	plt.close()

	# CHART 7 — MOST REVIEWED PRODUCTS

	fig, ax = plt.subplots(
		figsize=(12, 7)
	)

	top_reviewed = (

		df_catalog[
			df_catalog['product_reviews_count'].notna()
		]

		.nlargest(
			10,
			'product_reviews_count'
		)

		[[
			'title',
			'product_reviews_count',
			'product_rating',
			'product_discounted_price',
			'product_category'
		]]

		.copy()
	)

	# shorten gigantic amazon titles
	top_reviewed['short_title'] = top_reviewed['title'].apply(

		lambda txt:
		txt[:55] + '...'
		if len(str(txt)) > 55
		else txt
	)

	top_reviewed = top_reviewed.sort_values(
		'product_reviews_count',
		ascending=True
	)

	review_colors = [
		orange if i == 9 else '#CCCCCC'
		for i in range(len(top_reviewed))
	]

	bars = ax.barh(
		top_reviewed['short_title'],

		top_reviewed['product_reviews_count'].astype(float) / 1000,

		color=review_colors,

		edgecolor='white'
	)

	ax.bar_label(
		bars,
		fmt='%.0fK',
		padding=4,
		fontsize=8.5,
		fontweight='bold'
	)

	ax.set_xlabel(
		'Number of Reviews (Thousands)',
		fontsize=11
	)

	ax.set_title(
		'Top 10 Most Reviewed Products',
		fontsize=14,
		fontweight='bold',
		pad=12
	)

	# custom formatter because matplotlib defaults looked ugly
	ax.xaxis.set_major_formatter(

		mticker.FuncFormatter(
			lambda x, _: f'{x:.0f}K'
		)
	)

	plt.tight_layout()
	plt.savefig(f'{output_path}/top_reviewed_products.png', bbox_inches='tight')
	plt.close()