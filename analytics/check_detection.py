import pandas as pd

encounters = pd.read_csv("data/bronze/synthetic_encounters.csv")
alerts = pd.read_csv("data/lakehouse_test/outbreak_alerts.csv")

encounters["encounter_date"] = pd.to_datetime(encounters["encounter_date"])
alerts["date"] = pd.to_datetime(alerts["date"])

marked = encounters[
    encounters["ground_truth_outbreak"] == "planted_outbreak"
]

check = marked.merge(
    alerts[["date", "district", "disease", "alert"]],
    left_on=["encounter_date", "district", "disease"],
    right_on=["date", "district", "disease"],
    how="left"
)

print("Total planted rows:", len(marked))
print("Planted rows matching alert dates:", int(check["alert"].eq(True).sum()))
print("Planted rows without matching alert dates:", int((~check["alert"].eq(True)).sum()))