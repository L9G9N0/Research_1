import os
import glob
import pandas as pd
import numpy as np

RAW_DIR = "research_output/raw_data"
OUT_DIR = "research_output"

# 1. Load UNDP Data
undp_csv = os.path.join(RAW_DIR, "HDR25_Composite_indices_complete_time_series.csv")
df_undp = pd.read_csv(undp_csv, encoding='latin1', low_memory=False)

# Exclude aggregates
# Aggregates have iso3 starting with 'ZZ'
undp_countries = df_undp[~df_undp['iso3'].str.startswith('ZZ')].copy()
print(f"Total UNDP rows: {len(df_undp)}, Country rows: {len(undp_countries)}")

# Let's verify all UNDP country iso3 codes
undp_iso3 = set(undp_countries['iso3'].unique())

# 2. Load World Bank Data
# We will load metadata country for World Bank to know which are sovereign/economies vs regional aggregates
wb_meta_country = pd.read_csv(os.path.join(RAW_DIR, "wb_NY_GDP_PCAP_KD", "Metadata_Country_API_NY.GDP.PCAP.KD_DS2_en_csv_v2_4863.csv"))
wb_economies_meta = wb_meta_country[wb_meta_country['Region'].notna()]
wb_iso3 = set(wb_economies_meta['Country Code'].unique())
print(f"Total WB economies with region: {len(wb_iso3)}")

# Unmatched economies
undp_not_in_wb = undp_iso3 - wb_iso3
wb_not_in_undp = wb_iso3 - undp_iso3
print(f"UNDP ISO3 not in WB economies ({len(undp_not_in_wb)}): {sorted(list(undp_not_in_wb))}")
print(f"WB economies not in UNDP ({len(wb_not_in_undp)}): {sorted(list(wb_not_in_undp))}")

# Check country names for unmatched
for code in sorted(list(undp_not_in_wb)):
    cname = undp_countries[undp_countries['iso3'] == code]['country'].values[0]
    print(f"  UNDP only: {code} -> {cname}")

for code in sorted(list(wb_not_in_undp)):
    cname = wb_economies_meta[wb_economies_meta['Country Code'] == code]['TableName'].values[0]
    print(f"  WB only: {code} -> {cname}")

# Let's inspect year-by-year counts for UNDP indicators
undp_indicators = {
    'hdi': 'HDI',
    'le': 'Life Expectancy',
    'eys': 'Expected Years of Schooling',
    'mys': 'Mean Years of Schooling',
    'gnipc': 'GNI per capita (2021 PPP $)',
    'ihdi': 'IHDI',
    'loss': 'Overall Loss due to Inequality (%)',
    'phdi': 'PHDI',
    'diff_hdi_phdi': 'Planetary Pressures Adjustment / Diff'
}

year_counts_undp = {}
for y in range(2000, 2024):
    row = {'Year': y}
    for ind, name in undp_indicators.items():
        col = f"{ind}_{y}"
        if col in undp_countries.columns:
            row[name] = undp_countries[col].notna().sum()
        else:
            row[name] = 0
    year_counts_undp[y] = row

df_undp_years = pd.DataFrame(list(year_counts_undp.values()))
df_undp_years.to_csv(os.path.join(OUT_DIR, "undp_indicator_coverage_2000_2023.csv"), index=False)
print("\nUNDP Coverage Table (sample years):")
print(df_undp_years[df_undp_years['Year'].isin([2000, 2005, 2010, 2015, 2020, 2022, 2023])])

# 3. Load World Bank indicator datasets
def load_wb_indicator_series(folder_name):
    path = glob.glob(os.path.join(RAW_DIR, folder_name, "API_*.csv"))
    path = [p for p in path if "Metadata" not in p][0]
    df = pd.read_csv(path, skiprows=4)
    # keep only WB economies
    df = df[df['Country Code'].isin(wb_iso3)]
    return df

df_wb_gdp = load_wb_indicator_series("wb_NY_GDP_PCAP_KD")
df_wb_growth = load_wb_indicator_series("wb_NY_GDP_PCAP_KD_ZG")
df_wb_ppp = load_wb_indicator_series("wb_NY_GDP_PCAP_PP_KD")
df_wb_gini = load_wb_indicator_series("wb_SI_POV_GINI")
df_wb_le = load_wb_indicator_series("wb_SP_DYN_LE00_IN")

# Coverage counts for World Bank
wb_year_counts = []
for y in range(2000, 2025):
    y_str = str(y)
    wb_year_counts.append({
        'Year': y,
        'GDP_pc_KD': df_wb_gdp[y_str].notna().sum() if y_str in df_wb_gdp else 0,
        'GDP_growth': df_wb_growth[y_str].notna().sum() if y_str in df_wb_growth else 0,
        'GDP_pc_PPP': df_wb_ppp[y_str].notna().sum() if y_str in df_wb_ppp else 0,
        'Gini': df_wb_gini[y_str].notna().sum() if y_str in df_wb_gini else 0,
        'Life_Exp_WB': df_wb_le[y_str].notna().sum() if y_str in df_wb_le else 0
    })
df_wb_years = pd.DataFrame(wb_year_counts)
df_wb_years.to_csv(os.path.join(OUT_DIR, "world_bank_indicator_coverage_2000_2024.csv"), index=False)
print("\nWorld Bank Coverage Table (sample years):")
print(df_wb_years[df_wb_years['Year'].isin([2000, 2005, 2010, 2015, 2020, 2022, 2023, 2024])])

print("\nSaved coverage tables to CSV.")
