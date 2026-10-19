"""Simple transparent resource allocation heuristic with equity floor."""
import argparse
import pandas as pd
from common import load_daily, ensure_parent

def allocate(df, total_units=1000, min_share=0.01):
    latest=df.sort_values("date").groupby(["district","disease"],as_index=False).tail(1)
    need=latest.groupby("district",as_index=False)["cases"].sum()
    need["need_score"]=need["cases"].clip(lower=0)
    districts=len(need)
    if districts==0: return pd.DataFrame(columns=["district","need_score","allocated_units","population_baseline"])
    floor=min(int(total_units*min_share), total_units//districts)
    base=[floor]*districts
    remaining=total_units-sum(base)
    weights=need["need_score"].to_numpy(dtype=float)
    if weights.sum()<=0: weights[:]=1
    raw=remaining*weights/weights.sum()
    extras=raw.astype(int)
    for i in range(remaining-int(extras.sum())): extras[i % districts]+=1
    need["allocated_units"]=[base[i]+int(extras[i]) for i in range(districts)]
    need["population_baseline"]=round(total_units/districts, 2)
    need["allocation_method"]="case-weighted with equity floor"
    return need.sort_values("allocated_units",ascending=False)

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--output",required=True); p.add_argument("--units",type=int,default=1000)
    a=p.parse_args(); out=allocate(load_daily(a.input),a.units); ensure_parent(a.output); out.to_csv(a.output,index=False)
    print(f"Allocated {int(out['allocated_units'].sum()) if len(out) else 0} units across {len(out)} districts")
