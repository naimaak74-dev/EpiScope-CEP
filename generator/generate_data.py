from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(r"E:\episcope")
PUBLIC = ROOT / "data" / "public"
OUT = ROOT / "data" / "bronze" / "encounters"

POP_FILE = PUBLIC / "population_by_district.csv"

if not POP_FILE.exists():
    raise FileNotFoundError(f"Missing file: {POP_FILE}")

districts_df = pd.read_csv(POP_FILE)
districts_df = districts_df.dropna(subset=["district"])
districts_df["district"] = districts_df["district"].astype(str)
districts_df = districts_df.drop_duplicates("district")

districts = districts_df["district"].tolist()

if len(districts) == 0:
    raise ValueError("No districts found in population CSV.")

rng = np.random.default_rng(42)

# Start with a small test dataset.
# 0.01 scale factor = 250,000 encounters.
SCALE_FACTOR = 0.01
TOTAL_ENCOUNTERS = int(25_000_000 * SCALE_FACTOR)
FACILITY_COUNT = 600
CHUNK_SIZE = 50_000

OUT.mkdir(parents=True, exist_ok=True)

# Create facilities and assign each one a district.
facilities = pd.DataFrame({
    "facility_id": [
        f"FAC{i:04d}" for i in range(1, FACILITY_COUNT + 1)
    ],
    "district": rng.choice(districts, size=FACILITY_COUNT)
})

facilities.to_csv(
    ROOT / "data" / "bronze" / "facilities.csv",
    index=False
)

facility_ids = facilities["facility_id"].to_numpy()
facility_districts = facilities["district"].to_numpy()

# Build a list of facilities for each district.
district_facilities = {
    district: facilities.loc[
        facilities["district"] == district, "facility_id"
    ].to_numpy()
    for district in districts
}

# Every district must have at least one facility.
for district in districts:
    if len(district_facilities[district]) == 0:
        district_facilities[district] = np.array([
            facility_ids[0]
        ])

diseases = np.array([
    "Dengue",
    "Diarrhea",
    "Respiratory_Infection",
    "Malaria",
    "Typhoid"
])

disease_probabilities = [0.30, 0.25, 0.20, 0.10, 0.15]
sexes = np.array(["Female", "Male", "Other"])
symptoms = np.array([
    "Fever",
    "Diarrhea",
    "Cough",
    "Headache",
    "Fever_and_Headache"
])
outcomes = np.array([
    "Recovered",
    "Admitted",
    "Referred"
])

start_date = np.datetime64("2021-01-01")
end_date = np.datetime64("2026-01-01")
date_range = (end_date - start_date).astype(int)

# Remove previous generated encounter chunks.
for old_file in OUT.glob("encounters_part_*.csv"):
    old_file.unlink()

written = 0
part = 1

while written < TOTAL_ENCOUNTERS:
    size = min(CHUNK_SIZE, TOTAL_ENCOUNTERS - written)

    chosen_districts = rng.choice(districts, size=size)

    chosen_facilities = np.array([
        rng.choice(district_facilities[d])
        for d in chosen_districts
    ])

    random_days = rng.integers(0, date_range, size=size)
    dates = start_date + random_days.astype("timedelta64[D]")

    data = pd.DataFrame({
        "encounter_id": [
            f"ENC{i:09d}"
            for i in range(written + 1, written + size + 1)
        ],
        "encounter_date": pd.to_datetime(dates).strftime("%Y-%m-%d"),
        "district": chosen_districts,
        "facility_id": chosen_facilities,
        "disease": rng.choice(
            diseases, size=size, p=disease_probabilities
        ),
        "age": rng.integers(0, 101, size=size),
        "sex": rng.choice(sexes, size=size, p=[0.49, 0.49, 0.02]),
        "symptom": rng.choice(symptoms, size=size),
        "outcome": rng.choice(
            outcomes, size=size, p=[0.80, 0.15, 0.05]
        )
    })

    filename = OUT / f"encounters_part_{part:04d}.csv"
    data.to_csv(filename, index=False)

    written += size
    part += 1
    print(f"Generated {written:,} / {TOTAL_ENCOUNTERS:,} encounters")

print("\nSynthetic data generation completed.")
print("Facilities:", ROOT / "data" / "bronze" / "facilities.csv")
print("Encounter folder:", OUT)
print("Total encounters:", written)