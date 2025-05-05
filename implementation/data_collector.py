import pandas as pd
from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_path
import glob
import urllib.request
import os
import re
import urllib.request
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# --- 1) Load and clean AML Metrics CSV -------------------------------

aml_metrics_df = pd.read_csv('data/seed_data.csv')

# strip whitespace from all column names
aml_metrics_df.columns = [c.strip() for c in aml_metrics_df.columns]

# strip whitespace in 'Metric Name' cells
aml_metrics_df['Metric Name'] = aml_metrics_df['Metric Name'].astype(str).str.strip()

# --- 2) Basel report list ---------------------------------------------

basel_reports = [
    'data/basel_index_reports/2014_report_dc265c4f18.pdf',
    'data/basel_index_reports/2015_report_6bc9a34138.pdf',
    'data/basel_index_reports/2016_report_d825b0c4e5.pdf',
    'data/basel_index_reports/2017_report_cccbe78d59.pdf',
    'data/basel_index_reports/2018_report_ec77a5272c.pdf',
    'data/basel_index_reports/2019_report_dd7e1bf664.pdf',
    'data/basel_index_reports/2020_report_b7b51e0f7b.pdf',
    'data/basel_index_reports/2021_report_8a5d126c66.pdf',
    'data/basel_index_reports/2022_report_e8b51e07e.pdf',
    'data/basel_index_reports/2023_report_cc7b51e0f88.pdf',
    'data/basel_index_reports/2024_report_017b51e0f14.pdf'
]

valid_prefixes = {"DR", "El", "St"}
_country_word = r"[A-Z][a-z]+(?:['\.\-][A-Za-z]+)*"
score_pattern = re.compile(
    rf"(?:\d{{1,3}}\s+)?"
    rf"({_country_word}(?:\s+{_country_word}){{0,4}})\s+(\d+\.\d+)"
)

# create data/basel_index_reports if it doesn't already exist
os.makedirs("data/basel_index_reports", exist_ok=True)

def download_all_basel_assets(download_dir: str):
    # 1) ensure download directory exists
    os.makedirs(download_dir, exist_ok=True)

    # 2) fetch raw HTML with urllib
    url = "https://index.baselgovernance.org/downloads"
    resp = urllib.request.urlopen(url)
    html = resp.read()

    # 3) parse with bs4 and find all /api/assets/ links
    soup = BeautifulSoup(html, "html.parser")
    asset_links = {
        a["href"]
        for a in soup.find_all("a", href=True)
        if "/api/assets/" in a["href"]
    }

    if not asset_links:
        print("No asset links found.")
        return

    # 4) download each link
    for link in sorted(asset_links):
        full_url = urljoin(url, link)
        # extract UUID
        match = re.search(r"/api/assets/([0-9a-fA-F\-]+)$", link)
        if not match:
            print(f"⚠️ skipping unrecognized link {link}")
            continue
        uuid = match.group(1)
        filename = os.path.join(download_dir, f"{uuid}.pdf")

        print(f"↓ Downloading {uuid} …")
        r = requests.get(full_url, stream=True)
        r.raise_for_status()

        # if the server sends a Content-Disposition with a filename, use it
        cd = r.headers.get("content-disposition", "")
        m = re.search(r'filename="([^"]+)"', cd)
        if m:
            filename = os.path.join(download_dir, m.group(1))

        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*64):
                f.write(chunk)

    print("✅ All done!")



def clean_country_name(raw: str) -> str:
    # overrides
    if re.search(r"\bDR\s+Congo\b", raw, re.I):
        return "DR Congo"
    if re.search(r"\bMacao\b", raw, re.I):
        return "Macao SAR, China"
    if re.search(r"\bHong\s+Kong\b", raw, re.I):
        return "Hong Kong SAR, China"
    if re.search(r"\bVincent\s+And\s+The\s+Grenadines\b", raw, re.I):
        return "St. Vincent And The Grenadines"

    s = re.sub(r"Uni219[78][\s\\n]*\d+", "", raw)
    s = re.sub(r"\s+", " ", s).strip()
    m = re.search(rf"({_country_word}(?:\s+{_country_word})*)", s)
    if not m:
        return ""
    s = m.group(1)
    parts = s.split()
    if len(parts[0]) == 2 and parts[0] not in valid_prefixes:
        parts = parts[1:]
    cleaned = []
    for p in parts:
        cleaned.append(p if p in valid_prefixes else p.capitalize())
    return " ".join(cleaned)

def extract_basel_scores(text: str) -> dict:
    out = {}
    for raw, score in score_pattern.findall(text):
        name = clean_country_name(raw)
        if name:
            out[name] = score
    return out

def pdf_contains_text(path):
    with open(path,'rb') as f:
        text = ""
        for page in PdfReader(f).pages:
            text += page.extract_text() or ""
    return text

def ocr_from_images(images):
    return "".join(pytesseract.image_to_string(im) for im in images)

def contains_country_score_pattern(txt):
    return bool(re.search(r"\d{1,3}\s+" + _country_word + r"(?:\s+" + _country_word + r"){0,4}\s+\d+\.\d+", txt))

def extract_basel_data(paths):
    data = {}
    for pdf in paths:
        raw = pdf_contains_text(pdf)
        if raw and contains_country_score_pattern(raw):
            print("[TEXT]", pdf)
        else:
            print("[OCR ]", pdf)
            imgs = convert_from_path(pdf, dpi=300)
            raw = ocr_from_images(imgs)
        scores = extract_basel_scores(raw)
        year = re.search(r"(\d{4})", pdf).group(1)
        data[year] = scores
    return data

# --- 3) Join Basel into AML Metrics ----------------------------------

def add_basel_index_to_aml_metrics(df: pd.DataFrame, data: dict) -> pd.DataFrame:
    # make sure the Metric Value column is clean
    val_col = 'Metric Value'
    if val_col not in df.columns:
        # maybe it had spaces
        candidates = [c for c in df.columns if c.strip() == 'Metric Value']
        if candidates:
            val_col = candidates[0]
    # for each row whose Metric Name mentions FATF, update its Metric Value
    mask = df['Metric Name'].str.lower().str.contains('fatf')
    for idx in df[mask].index:
        country = df.at[idx, 'Country']
        year    = str(df.at[idx, 'Year'])
        new_v   = data.get(year, {}).get(country)
        if new_v is not None:
            df.at[idx, val_col] = new_v
    return df

def prune_basel_reports(dir_path: str):
    for fname in os.listdir(dir_path):
        # case‐insensitive match for either substring
        if not (("eport" in fname.lower()) or ("asel" in fname.lower())):
            full = os.path.join(dir_path, fname)
            try:
                os.remove(full)
                print(f"Removed {fname}")
            except Exception as e:
                print(f"Could not remove {fname}: {e}")

def download_all_basel_assets(download_dir: str):
    # 1) ensure download directory exists
    os.makedirs(download_dir, exist_ok=True)

    # 2) fetch raw HTML with urllib
    url = "https://index.baselgovernance.org/downloads"
    resp = urllib.request.urlopen(url)
    html = resp.read()

    # 3) parse with bs4 and find all /api/assets/ links
    soup = BeautifulSoup(html, "html.parser")
    asset_links = {
        a["href"]
        for a in soup.find_all("a", href=True)
        if "/api/assets/" in a["href"]
    }

    if not asset_links:
        print("No asset links found.")
        return

    # 4) download each link
    for link in sorted(asset_links):
        full_url = urljoin(url, link)
        # extract UUID
        match = re.search(r"/api/assets/([0-9a-fA-F\-]+)$", link)
        if not match:
            print(f"⚠️ skipping unrecognized link {link}")
            continue
        uuid = match.group(1)
        filename = os.path.join(download_dir, f"{uuid}.pdf")

        print(f"↓ Downloading {uuid} …")
        r = requests.get(full_url, stream=True)
        r.raise_for_status()

        # if the server sends a Content-Disposition with a filename, use it
        cd = r.headers.get("content-disposition", "")
        m = re.search(r'filename="([^"]+)"', cd)
        if m:
            filename = os.path.join(download_dir, m.group(1))

        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*64):
                f.write(chunk)

    print("✅ All done!")

def normalize_report_filenames(reports_dir: str, default_year: str = "2019") -> None:
    """
    Walk through reports_dir, find all .pdf files, extract a standalone 4-digit year
    (not part of a longer digit sequence) from each filename (defaulting to default_year
    if none), and rename them to <YEAR>_report.pdf, skipping any that would overwrite.
    """
    # regex that matches exactly 4 digits not preceded or followed by another digit
    year_re = re.compile(r"(?<!\d)(\d{4})(?!\d)")

    for fname in os.listdir(reports_dir):
        if not fname.lower().endswith(".pdf"):
            continue

        m = year_re.search(fname)
        year = m.group(1) if m else default_year

        src = os.path.join(reports_dir, fname)
        dst = os.path.join(reports_dir, f"{year}_report.pdf")

        if src == dst:
            continue

        if os.path.exists(dst):
            print(f"⚠️  {dst} already exists, skipping rename of {fname}")
        else:
            os.rename(src, dst)
            print(f"Renamed {fname} → {year}_report.pdf")

# run it

# ensure directory exists
reports_dir = "data/basel_index_reports"
os.makedirs(reports_dir, exist_ok=True)
# download reports
download_all_basel_assets(reports_dir)
prune_basel_reports(reports_dir)
normalize_report_filenames(reports_dir)

# find all PDF files whose names contain “report” or “asel” (so you only pick up the Basel reports)
pattern = os.path.join("data", "basel_index_reports", "*[rR]eport*.pdf")
basel_reports = glob.glob(pattern)

# if you want them in chronological order, sort by the 4-digit year in the filename:
basel_reports = sorted(
    basel_reports,
    key=lambda fn: int(os.path.basename(fn).split("_")[0])
)

print(basel_reports)

# TODO: Singapore 2017 is score 4.83 but 2.xx is extracted, thats wrong.
basel_data    = extract_basel_data(basel_reports)
updated_df    = add_basel_index_to_aml_metrics(aml_metrics_df, basel_data)
updated_df.to_csv('reports/20250505_report_data.csv', index=False)
