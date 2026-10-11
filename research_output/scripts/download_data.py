import os
import sys
import ssl
import time
import zipfile
import io
import urllib.request
import urllib.error

RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "raw_data"))
os.makedirs(RAW_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def download_file(url, target_path, max_retries=3):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        print(f"Already exists: {target_path} ({os.path.getsize(target_path)} bytes)")
        return True
    print(f"Downloading {url} to {target_path}...")
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=45, context=ctx) as resp, open(target_path, 'wb') as f:
                f.write(resp.read())
            print(f"Saved {target_path} ({os.path.getsize(target_path)} bytes)")
            return True
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {url}: {e}")
            time.sleep(2)
    return False

def download_and_extract_wb_zip(indicator, folder_prefix):
    url = f"https://api.worldbank.org/v2/en/indicator/{indicator}?downloadformat=csv"
    target_zip = os.path.join(RAW_DIR, f"{indicator}.zip")
    print(f"Fetching WB indicator {indicator} from {url}...")
    success = False
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
                content = resp.read()
                with open(target_zip, 'wb') as f:
                    f.write(content)
                print(f"Saved {target_zip} ({len(content)} bytes)")
                with zipfile.ZipFile(io.BytesIO(content)) as z:
                    extract_dir = os.path.join(RAW_DIR, folder_prefix)
                    os.makedirs(extract_dir, exist_ok=True)
                    z.extractall(extract_dir)
                    print(f"Extracted to {extract_dir}: {z.namelist()}")
                success = True
                break
        except Exception as e:
            print(f"Attempt {attempt+1} failed for WB {indicator}: {e}")
            time.sleep(2)
    return success

# 1. Download UNDP files
undp_urls = [
    ("https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv", "HDR25_Composite_indices_complete_time_series.csv"),
    ("https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Technical_Notes.pdf", "HDR25_Technical_Notes.pdf"),
    ("https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_metadata.xlsx", "HDR25_Composite_indices_metadata.xlsx"),
    ("https://hdr.undp.org/sites/default/files/2023-24_HDR/hdr2023-24_technical_notes.pdf", "hdr2023-24_technical_notes.pdf")
]

for url, filename in undp_urls:
    download_file(url, os.path.join(RAW_DIR, filename))

# 2. Download World Bank Indicators
wb_indicators = [
    ("NY.GDP.PCAP.KD", "wb_NY_GDP_PCAP_KD"),
    ("NY.GDP.PCAP.KD.ZG", "wb_NY_GDP_PCAP_KD_ZG"),
    ("NY.GDP.PCAP.PP.KD", "wb_NY_GDP_PCAP_PP_KD"),
    ("SI.POV.GINI", "wb_SI_POV_GINI"),
    ("SP.DYN.LE00.IN", "wb_SP_DYN_LE00_IN")
]

for ind, prefix in wb_indicators:
    download_and_extract_wb_zip(ind, prefix)

print("All downloads and extractions completed!")
