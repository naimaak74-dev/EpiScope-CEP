
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask

ROOT = Path(r"E:\episcope")
boundary_file = ROOT / "data" / "public" / "districts.geojson"
raster_file = ROOT / "data" / "public" / "population_2023.tif"
output_file = ROOT / "data" / "public" / "population_by_district.csv"

if not boundary_file.exists():
    raise FileNotFoundError(f"Missing boundary file: {boundary_file}")

if not raster_file.exists():
    raise FileNotFoundError(f"Missing population raster: {raster_file}")

districts = gpd.read_file(boundary_file)

if districts.empty or districts.crs is None:
    raise ValueError("District file is empty or has no CRS.")

print("District columns:", list(districts.columns))


candidates = [
    "adm2_en", "ADM2_EN",
    "adm2alt1en", "adm2alt2en",
    "ADM2_ENGLISH", "DISTRICT",
    "district", "District", "NAME_2",
    "DIST_NAME", "name_2", "NAME"
]

name_col = next(
    (col for col in candidates if col in districts.columns),
    None
)

if name_col is None:
    raise ValueError(
        "District name column not found. "
        "Send the printed column names."
    )

rows = []

with rasterio.open(raster_file) as src:
    if src.crs is None:
        raise ValueError("Population raster has no CRS.")

    districts = districts.to_crs(src.crs)

    for _, district in districts.iterrows():
        name = str(district[name_col])

        try:
            data, _ = mask(
                src,
                [district.geometry],
                crop=True,
                filled=False
            )

            values = data[0].compressed()
            values = values[np.isfinite(values)]

            if src.nodata is not None:
                values = values[values != src.nodata]

            total = float(values.sum()) if len(values) else 0.0

            rows.append({
                "district": name,
                "population_estimate_2023": round(total, 2)
            })

            print("Processed:", name)

        except ValueError as error:
            print("Could not process:", name, error)
            rows.append({
                "district": name,
                "population_estimate_2023": np.nan
            })

result = pd.DataFrame(rows)
result.to_csv(output_file, index=False)

print("\nSaved:", output_file)
print("District rows:", len(result))
print(result.head().to_string(index=False))
