import os
import glob
import pandas as pd
import numpy as np

RAW_DIR = "research_output/raw_data"
OUT_DIR = "research_output"

# Load UNDP
df_undp = pd.read_csv(os.path.join(RAW_DIR, "HDR25_Composite_indices_complete_time_series.csv"), encoding='latin1', low_memory=False)
df_undp = df_undp[~df_undp['iso3'].str.startswith('ZZ')].copy()

# Load World Bank Data
def load_wb(folder):
    path = [p for p in glob.glob(os.path.join(RAW_DIR, folder, "API_*.csv")) if "Metadata" not in p][0]
    return pd.read_csv(path, skiprows=4)

df_wb_gdp = load_wb("wb_NY_GDP_PCAP_KD")
df_wb_gini = load_wb("wb_SI_POV_GINI")
df_wb_le = load_wb("wb_SP_DYN_LE00_IN")

# Harmonize on the 195 UNDP countries
countries = sorted(df_undp['iso3'].unique())

# Helper to check availability for country and years
years_all = list(range(2000, 2024)) # 2000 to 2023 (24 years)
years_ihdi = list(range(2010, 2024)) # 2010 to 2023 (14 years)

def check_country_coverage(years_list):
    results = []
    for c in countries:
        c_undp = df_undp[df_undp['iso3'] == c].iloc[0]
        c_wb_gdp = df_wb_gdp[df_wb_gdp['Country Code'] == c]
        c_wb_gini = df_wb_gini[df_wb_gini['Country Code'] == c]
        c_wb_le = df_wb_le[df_wb_le['Country Code'] == c]
        
        has_wb_gdp_series = c_wb_gdp.iloc[0] if len(c_wb_gdp) > 0 else None
        has_wb_gini_series = c_wb_gini.iloc[0] if len(c_wb_gini) > 0 else None
        has_wb_le_series = c_wb_le.iloc[0] if len(c_wb_le) > 0 else None
        
        # Check presence per year
        gdp_years = []
        le_undp_years = []
        le_wb_years = []
        mys_years = []
        eys_years = []
        hdi_years = []
        ihdi_years = []
        phdi_years = []
        gini_years = []
        
        for y in years_list:
            y_str = str(y)
            # GDP pc
            if has_wb_gdp_series is not None and y_str in has_wb_gdp_series and pd.notna(has_wb_gdp_series[y_str]):
                gdp_years.append(y)
            # LE undp
            if f"le_{y}" in c_undp and pd.notna(c_undp[f"le_{y}"]):
                le_undp_years.append(y)
            # LE wb
            if has_wb_le_series is not None and y_str in has_wb_le_series and pd.notna(has_wb_le_series[y_str]):
                le_wb_years.append(y)
            # MYS & EYS
            if f"mys_{y}" in c_undp and pd.notna(c_undp[f"mys_{y}"]):
                mys_years.append(y)
            if f"eys_{y}" in c_undp and pd.notna(c_undp[f"eys_{y}"]):
                eys_years.append(y)
            # HDI
            if f"hdi_{y}" in c_undp and pd.notna(c_undp[f"hdi_{y}"]):
                hdi_years.append(y)
            # IHDI
            if f"ihdi_{y}" in c_undp and pd.notna(c_undp[f"ihdi_{y}"]):
                ihdi_years.append(y)
            # PHDI
            if f"phdi_{y}" in c_undp and pd.notna(c_undp[f"phdi_{y}"]):
                phdi_years.append(y)
            # GINI
            if has_wb_gini_series is not None and y_str in has_wb_gini_series and pd.notna(has_wb_gini_series[y_str]):
                gini_years.append(y)
                
        n_years = len(years_list)
        
        # Criteria flags
        has_gdp_all = (len(gdp_years) == n_years)
        has_gdp_any = (len(gdp_years) > 0)
        
        has_le_all = (len(le_undp_years) == n_years)
        has_le_any = (len(le_undp_years) > 0)
        
        has_school_all = (len(mys_years) == n_years) and (len(eys_years) == n_years)
        has_school_any = (len(mys_years) > 0) and (len(eys_years) > 0)
        
        has_hdi_all = (len(hdi_years) == n_years)
        has_hdi_any = (len(hdi_years) > 0)
        
        has_ihdi_all = (len(ihdi_years) == n_years)
        has_ihdi_any = (len(ihdi_years) > 0)
        
        has_phdi_all = (len(phdi_years) == n_years)
        has_phdi_any = (len(phdi_years) > 0)
        
        has_gini_3plus = (len(gini_years) >= 3)
        has_gini_any = (len(gini_years) > 0)
        
        # Combined sets:
        # (a) GDP pc + life expectancy + schooling
        set_a_all = has_gdp_all and has_le_all and has_school_all
        set_a_any = has_gdp_any and has_le_any and has_school_any
        
        # (b) same + HDI
        set_b_all = set_a_all and has_hdi_all
        set_b_any = set_a_any and has_hdi_any
        
        # (c) same + IHDI
        set_c_all = set_a_all and has_ihdi_all
        set_c_any = set_a_any and has_ihdi_any
        
        # (d) same + PHDI
        set_d_all = set_a_all and has_phdi_all
        set_d_any = set_a_any and has_phdi_any
        
        # (e) same + at least 3 Gini observations
        set_e_all = set_a_all and has_gini_3plus
        set_e_any = set_a_any and has_gini_3plus
        
        results.append({
            'iso3': c,
            'country': c_undp['country'],
            'gdp_obs': len(gdp_years),
            'le_obs': len(le_undp_years),
            'mys_obs': len(mys_years),
            'eys_obs': len(eys_years),
            'hdi_obs': len(hdi_years),
            'ihdi_obs': len(ihdi_years),
            'phdi_obs': len(phdi_years),
            'gini_obs': len(gini_years),
            'set_a_all': set_a_all, 'set_a_any': set_a_any,
            'set_b_all': set_b_all, 'set_b_any': set_b_any,
            'set_c_all': set_c_all, 'set_c_any': set_c_any,
            'set_d_all': set_d_all, 'set_d_any': set_d_any,
            'set_e_all': set_e_all, 'set_e_any': set_e_any,
        })
    return pd.DataFrame(results)

df_cov_2000_2023 = check_country_coverage(years_all)
df_cov_2000_2023.to_csv(os.path.join(OUT_DIR, "country_coverage_breakdown_2000_2023.csv"), index=False)

df_cov_2010_2023 = check_country_coverage(years_ihdi)
df_cov_2010_2023.to_csv(os.path.join(OUT_DIR, "country_coverage_breakdown_2010_2023.csv"), index=False)

def summarize_matrix(df_cov, period_label):
    summary = {
        'Period': period_label,
        'Total Countries Evaluated': len(df_cov),
        'Condition (a): GDPpc + LE + Schooling (Balanced)': df_cov['set_a_all'].sum(),
        'Condition (a): GDPpc + LE + Schooling (Any Obs)': df_cov['set_a_any'].sum(),
        'Condition (b): (a) + HDI (Balanced)': df_cov['set_b_all'].sum(),
        'Condition (b): (a) + HDI (Any Obs)': df_cov['set_b_any'].sum(),
        'Condition (c): (a) + IHDI (Balanced)': df_cov['set_c_all'].sum(),
        'Condition (c): (a) + IHDI (Any Obs)': df_cov['set_c_any'].sum(),
        'Condition (d): (a) + PHDI (Balanced)': df_cov['set_d_all'].sum(),
        'Condition (d): (a) + PHDI (Any Obs)': df_cov['set_d_any'].sum(),
        'Condition (e): (a) + >=3 Gini Obs (Balanced a)': df_cov['set_e_all'].sum(),
        'Condition (e): (a) + >=3 Gini Obs (Any Obs a)': df_cov['set_e_any'].sum(),
    }
    return summary

sum_2000_2023 = summarize_matrix(df_cov_2000_2023, "2000-2023 (24 years)")
sum_2010_2023 = summarize_matrix(df_cov_2010_2023, "2010-2023 (14 years)")

df_summary = pd.DataFrame([sum_2000_2023, sum_2010_2023])
df_summary.to_csv(os.path.join(OUT_DIR, "panel_coverage_matrix_summary.csv"), index=False)

print("\n=== COVERAGE MATRIX SUMMARY ===")
print(df_summary.to_string())

# Cross-check life expectancy: UNDP vs World Bank
# Compare SP.DYN.LE00.IN and UNDP le for year 2023
diffs = []
for c in countries:
    c_undp = df_undp[df_undp['iso3'] == c].iloc[0]
    c_wb = df_wb_le[df_wb_le['Country Code'] == c]
    if len(c_wb) > 0 and '2023' in c_wb.columns:
        wb_val = c_wb['2023'].values[0]
        undp_val = c_undp['le_2023'] if 'le_2023' in c_undp else np.nan
        if pd.notna(wb_val) and pd.notna(undp_val):
            diffs.append({'iso3': c, 'country': c_undp['country'], 'wb_le_2023': wb_val, 'undp_le_2023': undp_val, 'diff': abs(wb_val - undp_val)})

df_diffs = pd.DataFrame(diffs)
print(f"\nLife Expectancy Cross-Check (2023, {len(df_diffs)} matched countries):")
print(f"Max absolute difference: {df_diffs['diff'].max():.4f}")
print(f"Mean absolute difference: {df_diffs['diff'].mean():.4f}")
print(f"Number of countries with diff > 0.1 years: {(df_diffs['diff'] > 0.1).sum()}")
if (df_diffs['diff'] > 0.1).sum() > 0:
    print(df_diffs[df_diffs['diff'] > 0.1].head(10))
