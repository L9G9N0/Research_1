import os
import glob
import pandas as pd

raw_dir = "research_output/raw_data"
indicators = [
    ("NY.GDP.PCAP.KD", "wb_NY_GDP_PCAP_KD"),
    ("NY.GDP.PCAP.KD.ZG", "wb_NY_GDP_PCAP_KD_ZG"),
    ("NY.GDP.PCAP.PP.KD", "wb_NY_GDP_PCAP_PP_KD"),
    ("SI.POV.GINI", "wb_SI_POV_GINI"),
    ("SP.DYN.LE00.IN", "wb_SP_DYN_LE00_IN")
]

for ind_code, folder in indicators:
    print(f"\n==================== {ind_code} ====================")
    folder_path = os.path.join(raw_dir, folder)
    
    # Read indicator metadata
    meta_ind_files = glob.glob(os.path.join(folder_path, "Metadata_Indicator_*.csv"))
    if meta_ind_files:
        df_meta = pd.read_csv(meta_ind_files[0])
        print("Indicator Metadata:")
        for col in df_meta.columns:
            val = df_meta[col].dropna().iloc[0] if len(df_meta[col].dropna()) > 0 else ""
            print(f"  {col}: {str(val)[:200]}")
            
    # Read Country metadata to see aggregates
    meta_country_files = glob.glob(os.path.join(folder_path, "Metadata_Country_*.csv"))
    if meta_country_files:
        df_country = pd.read_csv(meta_country_files[0])
        print(f"Country metadata total rows: {len(df_country)}")
        # In WB metadata, Region is null for aggregates (e.g. Arab World, East Asia & Pacific, etc.)
        aggregates = df_country[df_country['Region'].isna()]['Country Code'].tolist()
        countries = df_country[df_country['Region'].notna()]['Country Code'].tolist()
        print(f"  Number of actual economies (with Region): {len(countries)}")
        print(f"  Number of aggregates (no Region): {len(aggregates)}")
        
    # Read main data file
    data_files = [f for f in glob.glob(os.path.join(folder_path, "API_*.csv")) if "Metadata" not in f]
    if data_files:
        # World Bank CSVs have 4 header rows before data
        df_data = pd.read_csv(data_files[0], skiprows=4)
        print(f"Data columns: {df_data.columns[:10].tolist()} ... {df_data.columns[-10:].tolist()}")
        print(f"Total rows in data: {len(df_data)}")
        
        # Filter to actual economies
        df_econ = df_data[df_data['Country Code'].isin(countries)]
        print(f"Economies in data: {len(df_econ)}")
        
        # Count non-nulls for recent years
        years = [str(y) for y in range(2000, 2025) if str(y) in df_econ.columns]
        counts = df_econ[years].notna().sum()
        print("Non-null country counts per year (2000-2024):")
        for y, c in counts.items():
            print(f"  {y}: {c} / {len(df_econ)} ({c/len(df_econ)*100:.1f}%)")
