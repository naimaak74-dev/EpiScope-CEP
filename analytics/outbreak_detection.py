"""Transparent baseline detector: trailing 7-day mean + 2 standard deviations.
This is a teaching baseline, not a clinically validated alerting system.
"""
import argparse
from common import load_daily, ensure_parent

def detect(df):
    df = df.sort_values("date").copy()
    grp = df.groupby(["district","disease"], dropna=False)["cases"]
    df["baseline_mean"] = grp.transform(lambda s: s.shift(1).rolling(7, min_periods=3).mean())
    df["baseline_std"] = grp.transform(lambda s: s.shift(1).rolling(7, min_periods=3).std().fillna(0))
    df["threshold"] = df["baseline_mean"] + 2 * df["baseline_std"]
    df["alert"] = (df["baseline_mean"].notna()) & (df["cases"] > df["threshold"])
    df["alert_reason"] = df["alert"].map({True:"cases exceed trailing baseline + 2 SD", False:""})
    return df

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input", required=True); p.add_argument("--output", required=True)
    a=p.parse_args()
    out=detect(load_daily(a.input)); ensure_parent(a.output); out.to_csv(a.output,index=False)
    print(f"Wrote {len(out)} rows to {a.output}; alerts={int(out['alert'].sum())}")
