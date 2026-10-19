"""Chunked synthetic encounter generator for development/testing.
Use --rows to control scale. It does NOT generate 25 million rows by default.
"""
import argparse, csv, random
from datetime import date, timedelta
from pathlib import Path

DISTRICTS=["Dhaka","Chattogram","Cumilla","Noakhali","Sylhet","Rajshahi","Khulna","Barishal","Rangpur","Mymensingh"]
DISEASES=["Dengue","Diarrhoea","ARI","Malaria"]
def generate(out, rows, seed=4345, chunk=100000):
    rng=random.Random(seed); out=Path(out); out.parent.mkdir(parents=True,exist_ok=True)
    start=date(2021,1,1)
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["encounter_id","patient_hash","encounter_date","district","disease","age","sex","facility_id","batch_id","synthetic"])
        for i in range(rows):
            day=start+timedelta(days=rng.randrange(1826))
            disease=rng.choice(DISEASES); district=rng.choice(DISTRICTS)
            # Several deterministic high-incidence periods are planted for detector demonstrations.
            if day.month in (6,7,8) and disease=="Dengue" and rng.random()<0.22:
                disease="Dengue"
            w.writerow([f"syn-{i:09d}",f"h{rng.getrandbits(128):032x}",day.isoformat(),district,disease,
                        rng.randint(0,95),rng.choice(["F","M","X"]),f"FAC-{rng.randint(1,250):04d}",
                        f"batch-{day.isoformat()}",True])
            if chunk and (i+1)%chunk==0: f.flush()
    return rows
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--output",default="data/bronze/synthetic_encounters.csv"); p.add_argument("--rows",type=int,default=100000); p.add_argument("--seed",type=int,default=4345)
    a=p.parse_args()
    if a.rows<1: raise SystemExit("--rows must be positive")
    print(f"Generated {generate(a.output,a.rows,a.seed)} synthetic rows at {a.output}")
