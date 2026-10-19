"""Forecast baseline: seasonal-naive (value from 7 days earlier) plus 80% interval.
Use time-ordered evaluation; do not describe this baseline as a validated clinical forecast.
"""
import argparse
import numpy as np
from common import load_daily, ensure_parent

def forecast(df, horizon=28):
    rows=[]
    for (district,disease), g in df.groupby(["district","disease"]):
        g=g.sort_values("date").dropna(subset=["cases"])
        if g.empty: continue
        last=g["date"].max()
        hist=g.set_index("date")["cases"].asfreq("D").interpolate(limit_direction="both")
        residual=(hist-hist.shift(7)).dropna()
        sigma=float(residual.std()) if len(residual)>1 else float(hist.std() if len(hist)>1 else 0)
        sigma=0 if not np.isfinite(sigma) else sigma
        for h in range(1,horizon+1):
            target=last+pd.Timedelta(days=h)
            if len(hist)>=7:
                base=float(hist.iloc[-7+(h-1)%7])
            else:
                base=float(hist.iloc[-1])
            rows.append({"district":district,"disease":disease,"date":target,
                         "forecast":max(0,base),"lower_80":max(0,base-1.28*sigma),
                         "upper_80":max(0,base+1.28*sigma),"method":"seasonal_naive_7d"})
    return rows

import pandas as pd
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--output",required=True); p.add_argument("--horizon",type=int,default=28)
    a=p.parse_args(); rows=forecast(load_daily(a.input),a.horizon); ensure_parent(a.output); pd.DataFrame(rows).to_csv(a.output,index=False)
    print(f"Wrote {len(rows)} forecast rows to {a.output}")
