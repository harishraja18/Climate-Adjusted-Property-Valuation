import csv
import subprocess
from math import atan2, cos, radians, sin, sqrt

from app.config import CYCLONE_FILE, FLOOD_RASTER, HEAT_FILE


# ============================================================
# EXISTING VALUATION PARAMETERS
# ============================================================

FLOOD_WEIGHT = 0.50
HEAT_WEIGHT = 0.30
CYCLONE_WEIGHT = 0.20

MAX_DISCOUNT = 0.20

CYCLONE_RADIUS_KM = 100
CYCLONE_MIN_WIND = 20
CYCLONE_MAX_WIND = 90
EARTH_RADIUS_KM = 6371


# ============================================================
# LOAD HEAT DATA
# ============================================================

def load_heat_data():

    heat = {}

    with open(HEAT_FILE, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            key = (
                row["district"].strip().lower(),
                row["block"].strip().lower(),
            )

            heat[key] = row

    return heat


# ============================================================
# LOAD CYCLONE DATA
# ============================================================

def load_cyclone_tracks():

    tracks = []

    with open(CYCLONE_FILE, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if not row["wmo_wind_knots"].strip():
                continue

            tracks.append(
                {
                    "name": row["name"],
                    "season": row["season"],
                    "lat": float(row["lat"]),
                    "lon": float(row["lon"]),
                    "wind": float(row["wmo_wind_knots"]),
                }
            )

    return tracks


# ============================================================
# FLOOD EXPOSURE
# ============================================================

def calculate_flood_exposure(latitude, longitude):

    result = subprocess.run(
        [
            "gdallocationinfo",
            "-wgs84",
            str(FLOOD_RASTER),
            str(longitude),
            str(latitude),
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

    return value


# ============================================================
# HEAT EXPOSURE
# ============================================================

def calculate_heat_exposure(district, city):

    heat_data = load_heat_data()

    key = (
        district.strip().lower(),
        city.strip().lower(),
    )

    match = heat_data.get(key)

    if not match:

        return {
            "heat_risk": None,
            "tmax_change": None,
            "heat_source": "unavailable",
        }

    return {
        "heat_risk": float(match["heat_risk"]),
        "tmax_change": float(match["tmax_change"]),
        "heat_source": "district_mean",
    }


# ============================================================
# HAVERSINE DISTANCE
# ============================================================

def distance_km(lat1, lon1, lat2, lon2):

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    return (
        EARTH_RADIUS_KM
        * 2
        * atan2(sqrt(a), sqrt(1 - a))
    )


# ============================================================
# CYCLONE EXPOSURE
# ============================================================

def calculate_cyclone_exposure(latitude, longitude):

    tracks = load_cyclone_tracks()

    nearby = []

    for track in tracks:

        distance = distance_km(
            latitude,
            longitude,
            track["lat"],
            track["lon"],
        )

        if distance <= CYCLONE_RADIUS_KM:

            nearby.append(
                (
                    track,
                    distance,
                )
            )

    if not nearby:

        return {
            "cyclone_intensity": 0,
            "nearest_cyclone_km": None,
            "max_nearby_wind_knots": None,
            "cyclone_source": "no_valid_track_within_100km",
        }

    strongest_track, _ = max(
        nearby,
        key=lambda item: item[0]["wind"],
    )

    wind = strongest_track["wind"]

    cyclone_intensity = (
        (wind - CYCLONE_MIN_WIND)
        / (CYCLONE_MAX_WIND - CYCLONE_MIN_WIND)
    )

    cyclone_intensity = max(
        0,
        min(1, cyclone_intensity),
    )

    return {
        "cyclone_intensity": round(
            cyclone_intensity,
            3,
        ),
        "nearest_cyclone_km": round(
            min(distance for _, distance in nearby),
            1,
        ),
        "max_nearby_wind_knots": wind,
        "cyclone_source": "historical_track_100km",
    }


# ============================================================
# CLIMATE RISK
# ============================================================

def calculate_climate_risk(
    flood_exposure,
    heat_risk,
    cyclone_intensity,
):

    factors = []

    weighted_sum = 0
    available_weight = 0

    if flood_exposure is not None:

        weighted_sum += (
            FLOOD_WEIGHT
            * flood_exposure
        )

        available_weight += FLOOD_WEIGHT

        factors.append("Flood")

    if heat_risk is not None:

        weighted_sum += (
            HEAT_WEIGHT
            * heat_risk
        )

        available_weight += HEAT_WEIGHT

        factors.append("Heat")

    if cyclone_intensity is not None:

        weighted_sum += (
            CYCLONE_WEIGHT
            * cyclone_intensity
        )

        available_weight += CYCLONE_WEIGHT

        factors.append("Cyclone")

    if available_weight > 0:

        risk_score = (
            weighted_sum
            / available_weight
        )

    else:

        risk_score = 0

    adjustment = (
        MAX_DISCOUNT
        * risk_score
    )

    data_completeness = (
        available_weight
        / (
            FLOOD_WEIGHT
            + HEAT_WEIGHT
            + CYCLONE_WEIGHT
        )
    )

    return {
        "risk_score": round(
            risk_score,
            3,
        ),
        "adjustment_percent": round(
            adjustment * 100,
            2,
        ),
        "available_factors": factors,
        "data_completeness": round(
            data_completeness,
            3,
        ),
    }


# ============================================================
# COMPLETE PROPERTY VALUATION
# ============================================================

def calculate_property_valuation(
    district,
    city,
    latitude,
    longitude,
    area_sqft,
    market_rate_per_sqft,
):

    # --------------------------------------------------------
    # BASE VALUE
    # --------------------------------------------------------

    base_value = (
        area_sqft
        * market_rate_per_sqft
    )

    # --------------------------------------------------------
    # CLIMATE FACTORS
    # --------------------------------------------------------

    flood = calculate_flood_exposure(
        latitude,
        longitude,
    )

    heat = calculate_heat_exposure(
        district,
        city,
    )

    cyclone = calculate_cyclone_exposure(
        latitude,
        longitude,
    )

    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    risk = calculate_climate_risk(
        flood_exposure=flood,
        heat_risk=heat["heat_risk"],
        cyclone_intensity=cyclone["cyclone_intensity"],
    )

    # --------------------------------------------------------
    # FINAL VALUE
    # --------------------------------------------------------

    adjustment = (
        risk["adjustment_percent"]
        / 100
    )

    adjusted_value = (
        base_value
        * (1 - adjustment)
    )

    return {

        "base_value": round(
            base_value,
            2,
        ),

        "flood_exposure": flood,

        "heat": heat,

        "cyclone": cyclone,

        "risk": risk,

        "adjusted_value": round(
            adjusted_value,
            2,
        ),
    }