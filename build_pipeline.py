
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
BRONZE = ROOT / "data" / "bronze"
ENCOUNTERS = BRONZE / "encounters"
SILVER = ROOT / "data" / "silver"
GOLD = ROOT / "data" / "gold"

SILVER.mkdir(parents=True, exist_ok=True)
GOLD.mkdir(parents=True, exist_ok=True)

files = sorted(ENCOUNTERS.glob("encounters_part_*.csv"))

if not files:
    raise FileNotFoundError(
        f"No encounter CSV files found in {ENCOUNTERS}. "
        "Run generate_data.py first."
    )

frames = []

for file in files:
    print("Reading:", file.name)
    frames.append(pd.read_csv(file))

df = pd.concat(frames, ignore_index=True)

print("Total encounter rows:", len(df))
print("Columns:", list(df.columns))

# Remove duplicate rows
df = df.drop_duplicates()

# Clean text values
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype("string").str.strip()

# Save cleaned data
silver_file = SILVER / "clean_encounters.csv"
df.to_csv(silver_file, index=False)
print("Saved:", silver_file)

# Find date and disease columns
date_candidates = [
    "date", "encounter_date", "visit_date", "report_date"
]
disease_candidates = [
    "disease", "disease_name", "condition"
]

date_col = next(
    (c for c in date_candidates if c in df.columns), None
)
disease_col = next(
    (c for c in disease_candidates if c in df.columns), None
)

if date_col is None or disease_col is None:
    print("Gold summary not created.")
    print("Could not identify date/disease columns.")
    print("Please check the printed column names above.")
else:
    df[date_col] = pd.to_datetime(
        df[date_col], errors="coerce"
    )
    valid = df.dropna(subset=[date_col, disease_col]).copy()
    valid["date"] = valid[date_col].dt.strftime("%Y-%m-%d")

    summary = (
        valid.groupby(["date", disease_col])
        .size()
        .reset_index(name="case_count")
        .rename(columns={disease_col: "disease"})
    )

    gold_file = GOLD / "daily_disease_summary.csv"
    summary.to_csv(gold_file, index=False)

    print("Saved:", gold_file)
    print("Summary rows:", len(summary))

print("Pipeline finished.")
