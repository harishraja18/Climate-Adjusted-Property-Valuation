import csv
from math import radians, sin, cos, sqrt, atan2

PROPERTY_FILE = "data/property/tamil_nadu_properties_climate.csv"
CYCLONE_FILE = "data/cyclone/tamil_nadu_cyclone_tracks_1980_2025.csv"
OUTPUT_FILE = "data/property/tamil_nadu_properties_climate.csv"

RADIUS_KM = 100
MIN_WIND = 20
MAX_WIND = 90
EARTH_RADIUS_KM = 6371


def distance_km(lat1, lon1, lat2, lon2):
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    return EARTH_RADIUS_KM * 2 * atan2(sqrt(a), sqrt(1 - a))


tracks = []

with open(CYCLONE_FILE, newline="") as f:
    for row in csv.DictReader(f):
        if not row["wmo_wind_knots"].strip():
            continue

        tracks.append({
            "name": row["name"],
            "season": row["season"],
            "lat": float(row["lat"]),
            "lon": float(row["lon"]),
            "wind": float(row["wmo_wind_knots"]),
        })


rows = []

with open(PROPERTY_FILE, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        property_lat = float(row["latitude"])
        property_lon = float(row["longitude"])

        nearby = []

        for track in tracks:
            distance = distance_km(
                property_lat,
                property_lon,
                track["lat"],
                track["lon"],
            )

            if distance <= RADIUS_KM:
                nearby.append((track, distance))

        if nearby:
            strongest_track, strongest_distance = max(
                nearby,
                key=lambda x: x[0]["wind"]
            )

            wind = strongest_track["wind"]

            cyclone_intensity = (
                (wind - MIN_WIND) / (MAX_WIND - MIN_WIND)
            )

            cyclone_intensity = max(0, min(1, cyclone_intensity))

            row["cyclone_intensity"] = round(cyclone_intensity, 3)
            row["nearest_cyclone_km"] = round(
                min(distance for _, distance in nearby), 1
            )
            row["max_nearby_wind_knots"] = wind
            row["cyclone_source"] = "historical_track_100km"

        else:
            row["cyclone_intensity"] = 0
            row["nearest_cyclone_km"] = ""
            row["max_nearby_wind_knots"] = ""
            row["cyclone_source"] = "no_valid_track_within_100km"

        rows.append(row)


with open(OUTPUT_FILE, "w", newline="") as f:
    fieldnames = rows[0].keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


print(f"Updated: {OUTPUT_FILE}")
print()

for row in rows:
    print(
        row["property_id"],
        row["city"],
        "cyclone_intensity =",
        row["cyclone_intensity"],
        "| max wind =",
        row["max_nearby_wind_knots"] or "N/A",
        "kt"
    )
