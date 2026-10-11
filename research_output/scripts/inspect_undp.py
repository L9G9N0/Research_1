import os
import pandas as pd
import numpy as np

csv_path = "research_output/raw_data/HDR25_Composite_indices_complete_time_series.csv"
df = pd.read_csv(csv_path, encoding='latin1', low_memory=False)

print("Columns in UNDP dataset:")
print(df.columns.tolist()[:30])
print(f"Total rows: {len(df)}, Total columns: {len(df.columns)}")

# Check ISO3 column name and country column name
# Let's inspect unique iso3 codes and country names
iso_col = [c for c in df.columns if 'iso' in c.lower()][0]
country_col = [c for c in df.columns if 'country' in c.lower()][0]
print(f"ISO col: {iso_col}, Country col: {country_col}")

# List all indicator prefixes
# In UNDP HDR time series, columns are typically named like hdi_1990, hdi_2022, le_1990, etc.
prefixes = sorted(list(set([c.rsplit('_', 1)[0] for c in df.columns if '_' in c])))
print("\nIndicator prefixes found:")
for p in prefixes:
    cols = [c for c in df.columns if c.startswith(p + '_')]
    years = [int(c.split('_')[-1]) for c in cols if c.split('_')[-1].isdigit()]
    if years:
        print(f"{p}: years {min(years)} to {max(years)} (total {len(years)} years)")
