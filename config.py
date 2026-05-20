import os
import warnings
import matplotlib.pyplot as plt

# Ignore warnings
warnings.filterwarnings('ignore')

# Set paths for input and output files
base_path = os.path.dirname(os.path.abspath(__file__))
raw_dataset_path = os.path.join(base_path, 'data', 'amazon_products_sales_data_uncleaned.csv')
output_path = os.path.join(base_path, 'visualizations')
category_map_path = os.path.join(base_path, 'category_map.json')

os.makedirs(output_path, exist_ok=True)

# Set some colors
orange = '#FF9900'
dark = '#000000'
blue = '#146EB4'
grey = '#565959'
green = '#4CAF50'
red = '#F44336'

# Set plot params
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'figure.dpi': 150,
})

SEGMENT_ORDER = [
    'Budget (<$15)',
    'Economy ($15-$30)',
    'Mid-Range ($30-$85)',
    'Upper-Mid ($85-$224)',
    'Premium ($224-$600)',
    'Luxury ($600+)'
]