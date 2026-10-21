
import pandas as pd

d = pd.read_csv("data/bronze/synthetic_encounters.csv")
g = pd.read_csv("data/bronze/outbreak_ground_truth.csv")

d["encounter_date"] = pd.to_datetime(d["encounter_date"])
g["start_date"] = pd.to_datetime(g["start_date"])
g["end_date"] = pd.to_datetime(g["end_date"])

print("OUTBREAK_ID | DISTRICT | DISEASE | MARKED_ROWS")

counts = []

for _, e in g.iterrows():
    mask = (
        (d["district"] == e["district"])
        & (d["disease"] == e["disease"])
        & (d["encounter_date"] >= e["start_date"])
        & (d["encounter_date"] <= e["end_date"])
        & (d["ground_truth_outbreak"] == "planted_outbreak")
    )

    n = int(mask.sum())
    counts.append(n)

    print(
        f"{e['outbreak_id']} | {e['district']} | "
        f"{e['disease']} | {n}"
    )

print("\nEvents with marked rows:", sum(n > 0 for n in counts), "out of", len(g))
print("Events with zero marked rows:", sum(n == 0 for n in counts))
