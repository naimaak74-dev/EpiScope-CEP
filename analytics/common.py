from pathlib import Path
import pandas as pd

DATE_CANDIDATES = ["date", "report_date", "encounter_date", "visit_date", "ds", "day"]
COUNT_CANDIDATES = ["case_count", "cases", "encounters", "count", "total_cases", "n"]
DISEASE_CANDIDATES = ["disease", "disease_name", "condition", "diagnosis"]
DISTRICT_CANDIDATES = ["district", "district_name", "district_id", "admin2"]

def load_daily(path):
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"No rows found in {path}")
    lower = {str(c).lower(): c for c in df.columns}
    date_col = next((lower[c] for c in DATE_CANDIDATES if c in lower), None)
    count_col = next((lower[c] for c in COUNT_CANDIDATES if c in lower), None)
    disease_col = next((lower[c] for c in DISEASE_CANDIDATES if c in lower), None)
    district_col = next((lower[c] for c in DISTRICT_CANDIDATES if c in lower), None)
    if date_col is None or count_col is None:
        raise ValueError(f"Could not identify date/count columns. Found columns: {list(df.columns)}")
    df = df.rename(columns={date_col:"date", count_col:"cases"})
    if disease_col: df = df.rename(columns={disease_col:"disease"})
    else: df["disease"] = "All diseases"
    if district_col: df = df.rename(columns={district_col:"district"})
    else: df["district"] = "All districts"
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["cases"] = pd.to_numeric(df["cases"], errors="coerce")
    df = df.dropna(subset=["date","cases"])
    df["cases"] = df["cases"].clip(lower=0)
    if df.empty:
        raise ValueError("No usable rows after parsing dates and counts.")
    return df

def ensure_parent(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
