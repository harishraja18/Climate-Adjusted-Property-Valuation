import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "heat"
    / "virudhunagar_seasonal_extremes.json"
)


def load_heat_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_heat_risk(scenario="rcP85", period="2090s"):
    data = load_heat_data()

    comparison = data["comparisonChartData"]["monthlyComparison"]

    hwdi_data = next(
        item for item in comparison
        if item["monthOrSeason"] == "HWDI"
    )

    hwfi_data = next(
        item for item in comparison
        if item["monthOrSeason"] == "HWFI"
    )

    hwdi = hwdi_data[scenario][period]
    hwfi = hwfi_data[scenario][period]

    # Prototype normalization based on the maximum
    # values present in the captured Virudhunagar dataset.
    hwdi_score = min(hwdi / 7, 1.0)
    hwfi_score = min(hwfi / 77, 1.0)

    # Prototype weights — not official valuation coefficients.
    heat_risk = (0.4 * hwdi_score) + (0.6 * hwfi_score)

    return {
        "scenario": scenario,
        "period": period,
        "hwdi": hwdi,
        "hwfi": hwfi,
        "hwdi_score": round(hwdi_score, 3),
        "hwfi_score": round(hwfi_score, 3),
        "heat_risk": round(heat_risk, 3),
    }


if __name__ == "__main__":
    result = calculate_heat_risk()
    print(json.dumps(result, indent=2))