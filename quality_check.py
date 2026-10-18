
from pathlib import Path
import pandas as pd

ROOT = Path(r"E:\episcope")
SILVER = ROOT / "data" / "silver" / "clean_encounters.csv"
REPORT = ROOT / "reports" / "data_quality_report.csv"

REPORT.parent.mkdir(parents=True, exist_ok=True)

if not SILVER.exists():
    raise FileNotFoundError(
        f"File not found: {SILVER}. "
        "Run build_pipeline.py first."
    )

df = pd.read_csv(SILVER)

results = []

results.append({
    "check": "Total rows",
    "value": len(df),
    "status": "PASS" if len(df) > 0 else "FAIL"
})

for col in df.columns:
    missing = int(df[col].isna().sum())

    results.append({
        "check": f"Missing values in {col}",
        "value": missing,
        "status": "PASS" if missing == 0 else "CHECK"
    })

duplicates = int(df.duplicated().sum())

results.append({
    "check": "Duplicate rows",
    "value": duplicates,
    "status": "PASS" if duplicates == 0 else "CHECK"
})

report = pd.DataFrame(results)
report.to_csv(REPORT, index=False)

print("Data quality check completed.")
print("Report saved:", REPORT)
print(report.to_string(index=False))
