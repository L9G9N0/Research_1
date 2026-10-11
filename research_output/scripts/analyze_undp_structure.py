import pandas as pd
import numpy as np

csv_path = "research_output/raw_data/HDR25_Composite_indices_complete_time_series.csv"
df = pd.read_csv(csv_path, encoding='latin1', low_memory=False)

# Inspect region, hdicode, etc. to see how aggregates are identified
print("Sample rows:")
print(df[['iso3', 'country', 'hdicode', 'region']].head(20))
print("\nUnique regions:", df['region'].unique())
print("Unique hdicodes:", df['hdicode'].unique())

# Identify non-country rows / aggregates
# In UNDP HDR, country rows typically have valid 3-letter ISO codes that are ISO3 country codes.
# Let's inspect rows where region is NaN or hdicode is NaN or iso3 starts with ZZ or similar
print("\nRows where region is NaN:")
print(df[df['region'].isna()][['iso3', 'country', 'hdicode', 'region']])

# Let's check how many total entities
print(f"\nTotal rows in CSV: {len(df)}")
