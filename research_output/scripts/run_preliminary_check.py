import os
import glob
import pandas as pd
import numpy as np
from scipy import stats

RAW_DIR = "research_output/raw_data"
OUT_DIR = "research_output"
SCRIPTS_DIR = "research_output/scripts"

# 1. Load UNDP Data
df_undp = pd.read_csv(os.path.join(RAW_DIR, "HDR25_Composite_indices_complete_time_series.csv"), encoding='latin1', low_memory=False)
df_undp = df_undp[~df_undp['iso3'].str.startswith('ZZ')].copy()

# 2. Load World Bank GDP per capita (constant 2015 US$)
path_wb_gdp = [p for p in glob.glob(os.path.join(RAW_DIR, "wb_NY_GDP_PCAP_KD", "API_*.csv")) if "Metadata" not in p][0]
df_wb_gdp = pd.read_csv(path_wb_gdp, skiprows=4)

# Latest common year
target_year = 2023
y_str = str(target_year)

# Extract 2023 data for all countries
records = []
for idx, row in df_undp.iterrows():
    c_iso = row['iso3']
    c_name = row['country']
    
    # WB GDP pc
    wb_match = df_wb_gdp[df_wb_gdp['Country Code'] == c_iso]
    gdp_val = np.nan
    if len(wb_match) > 0 and y_str in wb_match.columns:
        val = wb_match[y_str].values[0]
        if pd.notna(val) and float(val) > 0:
            gdp_val = float(val)
            
    # UNDP variables for 2023
    le_val = row.get(f'le_{target_year}', np.nan)
    mys_val = row.get(f'mys_{target_year}', np.nan)
    eys_val = row.get(f'eys_{target_year}', np.nan)
    hdi_val = row.get(f'hdi_{target_year}', np.nan)
    ihdi_val = row.get(f'ihdi_{target_year}', np.nan)
    loss_val = row.get(f'loss_{target_year}', np.nan)
    phdi_val = row.get(f'phdi_{target_year}', np.nan)
    gnipc_val = row.get(f'gnipc_{target_year}', np.nan)
    
    records.append({
        'iso3': c_iso,
        'country': c_name,
        'gdp_pc': gdp_val,
        'ln_gdp_pc': np.log(gdp_val) if pd.notna(gdp_val) else np.nan,
        'le': float(le_val) if pd.notna(le_val) else np.nan,
        'mys': float(mys_val) if pd.notna(mys_val) else np.nan,
        'eys': float(eys_val) if pd.notna(eys_val) else np.nan,
        'hdi': float(hdi_val) if pd.notna(hdi_val) else np.nan,
        'ihdi': float(ihdi_val) if pd.notna(ihdi_val) else np.nan,
        'loss': float(loss_val) if pd.notna(loss_val) else np.nan,
        'phdi': float(phdi_val) if pd.notna(phdi_val) else np.nan,
        'gnipc': float(gnipc_val) if pd.notna(gnipc_val) else np.nan,
    })

df_all = pd.DataFrame(records)
df_all.to_csv(os.path.join(OUT_DIR, f"matched_country_data_{target_year}.csv"), index=False)
print(f"Total matched dataset size for {target_year}: {len(df_all)} countries")

# --- 1. Correlation Analysis ---
# Pearson and Spearman of ln(GDP pc) with outcomes
variables = [
    ('le', 'Life Expectancy at Birth'),
    ('mys', 'Mean Years of Schooling'),
    ('eys', 'Expected Years of Schooling'),
    ('hdi', 'Human Development Index (HDI)'),
    ('ihdi', 'Inequality-adjusted HDI (IHDI)'),
    ('phdi', 'Planetary pressures-adjusted HDI (PHDI)')
]

corr_results = []
for var_code, var_name in variables:
    sub = df_all[['ln_gdp_pc', var_code]].dropna()
    n_obs = len(sub)
    r_pearson, p_pearson = stats.pearsonr(sub['ln_gdp_pc'], sub[var_code])
    r_spearman, p_spearman = stats.spearmanr(sub['ln_gdp_pc'], sub[var_code])
    
    corr_results.append({
        'Variable Code': var_code,
        'Variable Name': var_name,
        'N': n_obs,
        'Pearson r': round(r_pearson, 4),
        'Pearson p-value': f"{p_pearson:.2e}",
        'Spearman rho': round(r_spearman, 4),
        'Spearman p-value': f"{p_spearman:.2e}"
    })

df_corr = pd.DataFrame(corr_results)
df_corr.to_csv(os.path.join(OUT_DIR, "preliminary_correlations_2023.csv"), index=False)
print("\n=== PRELIMINARY CORRELATION TABLE (2023) ===")
print(df_corr.to_string())

# --- 2. Rank Difference Analysis ---
# D = |Rank(GDP pc) - Rank(Y)|
# (Higher value = better rank, rank 1 = highest)
def compute_ranks_and_diffs(var_target):
    sub = df_all[['iso3', 'country', 'gdp_pc', var_target]].dropna().copy()
    # Rank descending (highest GDP pc is rank 1)
    sub['rank_gdp'] = sub['gdp_pc'].rank(ascending=False, method='min')
    sub[f'rank_{var_target}'] = sub[var_target].rank(ascending=False, method='min')
    sub['rank_diff'] = sub['rank_gdp'] - sub[f'rank_{var_target}']
    sub['abs_rank_diff'] = sub['rank_diff'].abs()
    
    mean_diff = sub['abs_rank_diff'].mean()
    median_diff = sub['abs_rank_diff'].median()
    pct_over_20 = (sub['abs_rank_diff'] > 20).mean() * 100
    n = len(sub)
    
    return sub, {
        'Target': var_target,
        'N': n,
        'Mean |Rank Diff|': round(mean_diff, 2),
        'Median |Rank Diff|': round(median_diff, 2),
        'Share |Rank Diff| > 20 (%)': round(pct_over_20, 2)
    }

sub_ihdi, stats_ihdi = compute_ranks_and_diffs('ihdi')
sub_phdi, stats_phdi = compute_ranks_and_diffs('phdi')

df_rank_summary = pd.DataFrame([stats_ihdi, stats_phdi])
df_rank_summary.to_csv(os.path.join(OUT_DIR, "preliminary_rank_diff_summary_2023.csv"), index=False)
print("\n=== RANK DIFFERENCE SUMMARY (2023) ===")
print(df_rank_summary.to_string())

# Top divergences for IHDI and PHDI
sub_ihdi.sort_values(by='abs_rank_diff', ascending=False, inplace=True)
sub_ihdi.to_csv(os.path.join(OUT_DIR, "rank_differences_gdp_vs_ihdi_2023.csv"), index=False)

sub_phdi.sort_values(by='abs_rank_diff', ascending=False, inplace=True)
sub_phdi.to_csv(os.path.join(OUT_DIR, "rank_differences_gdp_vs_phdi_2023.csv"), index=False)

# --- 3. Matched-Country Comparisons (+/-10% GDP pc with large gaps) ---
# Find pairs of countries whose GDP pc is within +/- 10% of each other,
# but who have huge gaps in life expectancy or inequality loss (%)
df_valid = df_all.dropna(subset=['gdp_pc', 'le', 'loss']).copy()
pairs = []

visited_pairs = set()
for i, r1 in df_valid.iterrows():
    for j, r2 in df_valid.iterrows():
        if i >= j:
            continue
        g1, g2 = r1['gdp_pc'], r2['gdp_pc']
        pct_diff = abs(g1 - g2) / min(g1, g2)
        if pct_diff <= 0.10: # within 10%
            le_gap = abs(r1['le'] - r2['le'])
            loss_gap = abs(r1['loss'] - r2['loss']) if pd.notna(r1['loss']) and pd.notna(r2['loss']) else 0
            pairs.append({
                'Country A': r1['country'],
                'ISO A': r1['iso3'],
                'GDPpc A': round(r1['gdp_pc'], 1),
                'LE A': round(r1['le'], 1),
                'Loss A (%)': round(r1['loss'], 1) if pd.notna(r1['loss']) else np.nan,
                'Country B': r2['country'],
                'ISO B': r2['iso3'],
                'GDPpc B': round(r2['gdp_pc'], 1),
                'LE B': round(r2['le'], 1),
                'Loss B (%)': round(r2['loss'], 1) if pd.notna(r2['loss']) else np.nan,
                'GDP Diff (%)': round(pct_diff * 100, 2),
                'LE Gap (Years)': round(le_gap, 1),
                'Loss Gap (% pts)': round(loss_gap, 1),
                'Combined Score': round(le_gap + loss_gap, 2)
            })

df_pairs = pd.DataFrame(pairs)
df_pairs.sort_values(by='Combined Score', ascending=False, inplace=True)

# Select 5 diverse, illustrative pairs across different income tiers
# Let's inspect top pairs
print("\n=== TOP CANDIDATE MATCHED PAIRS (within 10% GDP pc) ===")
print(df_pairs.head(15)[['Country A', 'GDPpc A', 'LE A', 'Loss A (%)', 'Country B', 'GDPpc B', 'LE B', 'Loss B (%)', 'LE Gap (Years)', 'Loss Gap (% pts)']].to_string())

# Save matched pairs to CSV
df_pairs.to_csv(os.path.join(OUT_DIR, "preliminary_matched_country_pairs_2023.csv"), index=False)
