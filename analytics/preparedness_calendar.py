"""Basic seasonal preparedness calendar from historical monthly case counts."""
import argparse
import pandas as pd
from common import load_daily, ensure_parent

def make_calendar(df):
    x=df.copy(); x["month"]=x["date"].dt.month
    season=x.groupby(["disease","month"],as_index=False)["cases"].mean().rename(columns={"cases":"mean_monthly_daily_cases"})
    season["priority_rank"]=season.groupby("disease")["mean_monthly_daily_cases"].rank(method="dense",ascending=False).astype(int)
    season["preparedness_action"]=season["priority_rank"].map(lambda r: "High readiness: verify supplies, staffing and reporting" if r==1 else ("Prepare buffer stock and monitor weekly" if r<=3 else "Routine monitoring"))
    season["month_name"]=season["month"].map(lambda m: pd.Timestamp(2000,m,1).strftime("%B"))
    return season.sort_values(["disease","priority_rank","month"])

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--output",required=True)
    a=p.parse_args(); out=make_calendar(load_daily(a.input)); ensure_parent(a.output); out.to_csv(a.output,index=False)
    print(f"Wrote {len(out)} seasonal rows to {a.output}")
