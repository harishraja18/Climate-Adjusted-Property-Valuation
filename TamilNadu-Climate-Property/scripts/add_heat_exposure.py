import csv

property_file = "data/property/tamil_nadu_properties_flood.csv"
heat_file = "data/heat/heat_risk_dataset.csv"
output_file = "data/property/tamil_nadu_properties_climate.csv"

heat = {}

with open(heat_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["district"].lower(), row["block"].lower())
        heat[key] = row

rows = []

with open(property_file, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        district = row["district"].lower()
        city = row["city"].lower()

        match = heat.get((district, city))

        if match:
            row["heat_risk"] = match["heat_risk"]
            row["tmax_change"] = match["tmax_change"]
        else:
            row["heat_risk"] = ""
            row["tmax_change"] = ""

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
    print(
        row["property_id"],
        row["city"],
        "heat_risk =",
        row["heat_risk"] if row["heat_risk"] else "N/A"
    )
