import csv

INPUT_FILE = "data/property/tamil_nadu_properties_climate.csv"
OUTPUT_FILE = "data/property/tamil_nadu_climate_valuation.csv"

FLOOD_WEIGHT = 0.50
HEAT_WEIGHT = 0.30
CYCLONE_WEIGHT = 0.20
MAX_DISCOUNT = 0.20


def get_float(value):
    if value is None or value.strip() == "":
        return None
    return float(value)


rows = []

with open(INPUT_FILE, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        flood = get_float(row["flood_exposure"])
        heat = get_float(row["heat_risk"])
        cyclone = get_float(row["cyclone_intensity"])

        factors = []
        weighted_sum = 0
        available_weight = 0

        if flood is not None:
            weighted_sum += FLOOD_WEIGHT * flood
            available_weight += FLOOD_WEIGHT
            factors.append("Flood")

        if heat is not None:
            weighted_sum += HEAT_WEIGHT * heat
            available_weight += HEAT_WEIGHT
            factors.append("Heat")

        if cyclone is not None:
            weighted_sum += CYCLONE_WEIGHT * cyclone
            available_weight += CYCLONE_WEIGHT
            factors.append("Cyclone")

        if available_weight > 0:
            risk_score = weighted_sum / available_weight
        else:
            risk_score = 0

        adjustment_percent = MAX_DISCOUNT * risk_score
        base_value = float(row["base_value"])
        adjusted_value = base_value * (1 - adjustment_percent)

        row["risk_score"] = round(risk_score, 3)
        row["adjustment_percent"] = round(adjustment_percent * 100, 2)
        row["adjusted_value"] = round(adjusted_value, 2)
        row["available_factors"] = ", ".join(factors)
        row["data_completeness"] = round(
            available_weight / (
                FLOOD_WEIGHT + HEAT_WEIGHT + CYCLONE_WEIGHT
            ),
            3
        )

        rows.append(row)


with open(OUTPUT_FILE, "w", newline="") as f:
    fieldnames = rows[0].keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


print(f"Created: {OUTPUT_FILE}")
print()

for row in rows:
    print(
        row["property_id"],
        row["city"],
        "| Base =", row["base_value"],
        "| Risk =", row["risk_score"],
        "| Adjustment =", f'{row["adjustment_percent"]}%',
        "| Adjusted =", row["adjusted_value"],
        "| Factors =", row["available_factors"]
    )
