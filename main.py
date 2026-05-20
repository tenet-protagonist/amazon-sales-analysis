import pandas as pd
from config import raw_dataset_path
from processing import clean_dataset
from eda import eda
from plots import generate_plots

# STEP 1 - LOAD RAW DATA
df = pd.read_csv(raw_dataset_path)

# STEP 2 - DATA CLEANING & ETL
df_catalog, df_timeline = clean_dataset(df)

# STEP 3 - EXPLORATORY DATA ANALYSIS
eda_results = eda(df_catalog, df_timeline)

# STEP 4 - VISUALIZATIONS
generate_plots(
    df_catalog=df_catalog,
    eda_results=eda_results
)
