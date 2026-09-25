import json
from pathlib import Path
import csv

INPUT_DIR = Path("data/heat/imd")
OUTPUT_FILE = Path("data/heat/heat_dataset.csv")


def mean(values):
    return sum(values) / len(values)


rows = []

for district_dir in sorted(INPUT_DIR.iterdir()):

    if not district_dir.is_dir():
        continue

    district = district_dir.name

    for json_file in sorted(district_dir.glob("*.json")):

        data = json.loads(json_file.read_text())

        tmax = data["Tmax (1995-2024)"]
        tmin = data["Tmin (1995-2024)"]

        years = tmax["years"]

        tmax_early = [
            v for y, v in zip(years, tmax["values"])
            if 1995 <= y <= 1999
        ]

        tmax_recent = [
            v for y, v in zip(years, tmax["values"])
            if 2020 <= y <= 2024
        ]

        tmin_early = [
            v for y, v in zip(years, tmin["values"])
            if 1995 <= y <= 1999
        ]

        tmin_recent = [
            v for y, v in zip(years, tmin["values"])
            if 2020 <= y <= 2024
        ]

        tmax_early_mean = mean(tmax_early)
        tmax_recent_mean = mean(tmax_recent)

        tmin_early_mean = mean(tmin_early)
        tmin_recent_mean = mean(tmin_recent)

        rows.append({
            "district": district,
            "block": json_file.stem,
            "tmax_early_mean": round(tmax_early_mean, 3),
            "tmax_recent_mean": round(tmax_recent_mean, 3),
            "tmax_change": round(
                tmax_recent_mean - tmax_early_mean, 3
            ),
            "tmin_early_mean": round(tmin_early_mean, 3),
            "tmin_recent_mean": round(tmin_recent_mean, 3),
            "tmin_change": round(
                tmin_recent_mean - tmin_early_mean, 3
            ),
        })


OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "district",
            "block",
            "tmax_early_mean",
            "tmax_recent_mean",
            "tmax_change",
            "tmin_early_mean",
            "tmin_recent_mean",
            "tmin_change",
        ],
    )

    writer.writeheader()
    writer.writerows(rows)


print(f"Saved: {OUTPUT_FILE}")
print(f"Rows: {len(rows)}")
