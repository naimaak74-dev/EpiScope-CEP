
"""Synthetic encounter generator for EpiScope-CEP.

Creates population-weighted background encounters and deliberately injects
synthetic cases into 30 known outbreak windows for testing the detector.

This is development/test data, not real epidemiological evidence.
"""

import argparse
import csv
import hashlib
import json
import random
from datetime import date, timedelta
from pathlib import Path

DISEASES = ["Dengue", "Diarrhoea", "ARI", "Malaria"]
START_DATE = date(2021, 1, 1)
END_DATE = date(2025, 12, 31)
DAYS = (END_DATE - START_DATE).days + 1

# Fraction of all encounters deliberately placed inside outbreak windows.
# This is an injection rate, not a real-world disease probability.
OUTBREAK_INJECTION_RATE = 0.05


def make_outbreaks(districts, count=30):
    """Create deterministic outbreak definitions across 2021-2025."""
    outbreaks = []

    for i in range(count):
        district = districts[(i * 7) % len(districts)]
        disease = DISEASES[i % len(DISEASES)]

        start_offset = int((i + 1) * (DAYS - 35) / (count + 1))
        start = START_DATE + timedelta(days=start_offset)
        duration = 14 + (i % 3) * 7
        end = min(start + timedelta(days=duration - 1), END_DATE)

        outbreaks.append({
            "outbreak_id": f"OB{i + 1:02d}",
            "district": district,
            "disease": disease,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "injection_rule": (
                "Injected encounters in the outbreak window; "
                "target disease selected with target_probability"
            ),
            "target_probability": 0.60,
        })

    return outbreaks


def load_districts(geojson_path, population_path):
    with open(geojson_path, encoding="utf-8") as f:
        geo = json.load(f)

    names = sorted({
        str(feature["properties"].get("adm2_en", "")).strip()
        for feature in geo.get("features", [])
        if str(feature["properties"].get("adm2_en", "")).strip()
    })

    if len(names) != 64:
        raise ValueError(
            f"Expected 64 district names in GeoJSON, found {len(names)}"
        )

    population = {}

    with open(population_path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = row["district"].strip()
            population[name] = max(
                1.0, float(row["population_estimate_2023"])
            )

    missing = sorted(set(names) - set(population))
    if missing:
        raise ValueError(f"Population estimates missing for: {missing}")

    weights = [population[name] for name in names]
    return names, weights


def write_ground_truth(path, outbreaks):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(outbreaks[0].keys()))
        writer.writeheader()
        writer.writerows(outbreaks)


def generate(
    output,
    rows,
    districts,
    weights,
    outbreaks,
    seed=4345,
    chunk=100000,
    salt="EpiScope-dev-salt-change-before-production",
):
    rng = random.Random(seed)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Parse event dates once.
    parsed_outbreaks = []
    for event in outbreaks:
        parsed_outbreaks.append({
            **event,
            "start": date.fromisoformat(event["start_date"]),
            "end": date.fromisoformat(event["end_date"]),
        })

    fieldnames = [
        "encounter_id",
        "patient_hash",
        "encounter_date",
        "district",
        "disease",
        "age",
        "sex",
        "facility_id",
        "batch_id",
        "synthetic",
        "ground_truth_outbreak",
    ]

    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(rows):
            ground_truth = "none"

            # Deliberately place some encounters inside known outbreak windows.
            if rng.random() < OUTBREAK_INJECTION_RATE:
                event = rng.choice(parsed_outbreaks)

                duration = (event["end"] - event["start"]).days
                encounter_day = event["start"] + timedelta(
                    days=rng.randrange(duration + 1)
                )
                district = event["district"]

                # Target disease occurs with the configured probability.
                if rng.random() < float(event["target_probability"]):
                    disease = event["disease"]
                    ground_truth = "planted_outbreak"
                else:
                    # Background disease during the same window.
                    alternatives = [
                        d for d in DISEASES if d != event["disease"]
                    ]
                    disease = rng.choice(alternatives)

            else:
                # Normal background encounters.
                encounter_day = START_DATE + timedelta(
                    days=rng.randrange(DAYS)
                )
                district = rng.choices(
                    districts, weights=weights, k=1
                )[0]
                disease = rng.choice(DISEASES)

                # Mild seasonal Dengue pattern in background data.
                if encounter_day.month in (6, 7, 8):
                    if rng.random() < 0.22:
                        disease = "Dengue"

            patient_id = (
                f"synthetic-patient-"
                f"{rng.randrange(max(1000, rows // 3 + 1))}"
            )
            patient_hash = hashlib.sha256(
                (salt + patient_id).encode("utf-8")
            ).hexdigest()

            writer.writerow({
                "encounter_id": f"syn-{i + 1:09d}",
                "patient_hash": patient_hash,
                "encounter_date": encounter_day.isoformat(),
                "district": district,
                "disease": disease,
                "age": rng.randint(0, 95),
                "sex": rng.choice(["F", "M", "X"]),
                "facility_id": f"FAC-{rng.randint(1, 250):04d}",
                "batch_id": f"batch-{encounter_day.isoformat()}",
                "synthetic": True,
                "ground_truth_outbreak": ground_truth,
            })

            if chunk and (i + 1) % chunk == 0:
                f.flush()

    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="data/bronze/synthetic_encounters.csv",
    )
    parser.add_argument(
        "--ground-truth",
        default="data/bronze/outbreak_ground_truth.csv",
    )
    parser.add_argument(
        "--geojson",
        default="data/public/districts.geojson",
    )
    parser.add_argument(
        "--population",
        default="data/public/population_by_district.csv",
    )
    parser.add_argument("--rows", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=4345)
    parser.add_argument("--chunk", type=int, default=100000)
    parser.add_argument(
        "--salt",
        default="EpiScope-dev-salt-change-before-production",
    )

    args = parser.parse_args()

    if args.rows < 1:
        parser.error("--rows must be positive")

    districts, weights = load_districts(
        args.geojson, args.population
    )
    outbreaks = make_outbreaks(districts, 30)

    write_ground_truth(args.ground_truth, outbreaks)

    count = generate(
        args.output,
        args.rows,
        districts,
        weights,
        outbreaks,
        args.seed,
        args.chunk,
        args.salt,
    )

    print(f"Generated {count:,} synthetic rows: {args.output}")
    print(f"Districts used: {len(districts)}")
    print(
        f"Ground-truth outbreak events: {len(outbreaks)}"
        f" -> {args.ground_truth}"
    )
    print(f"Outbreak injection rate: {OUTBREAK_INJECTION_RATE:.0%}")
    print(
        "WARNING: Synthetic development data only; "
        "not clinically validated."
    )


if __name__ == "__main__":
    main()
