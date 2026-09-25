import csv
import subprocess

input_file = "data/property/tamil_nadu_properties_with_base_value.csv"
raster = "data/flood/tamil_nadu_flood_mask_tn_2003_2020.tif"
output_file = "data/property/tamil_nadu_properties_flood.csv"

rows = []

with open(input_file, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        lon = row["longitude"]
        lat = row["latitude"]

        result = subprocess.run(
            [
                "gdallocationinfo",
                "-wgs84",
                raster,
                lon,
                lat,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        value = 0

        for line in result.stdout.splitlines():
            if "Value:" in line:
                value = int(float(line.split(":")[1].strip()))
                break

        row["flood_exposure"] = value
        rows.append(row)

with open(output_file, "w", newline="") as f:
    fieldnames = rows[0].keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Created: {output_file}")
print(f"Properties processed: {len(rows)}")
print()
for row in rows:
    print(row["property_id"], row["city"], "flood_exposure =", row["flood_exposure"])
