# Climate-Adjusted Property Valuation API

This project provides a FastAPI backend for estimating a property value adjusted for local climate risks such as flood, heat, and cyclone exposure in Tamil Nadu.

## Project Structure

```text
.
├── README.md
├── main.py
├── pyproject.toml
├── TamilNadu-Climate-Property/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── climate_engine.py
│   │   ├── config.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── data/
│   │   ├── cyclone/
│   │   ├── flood/
│   │   └── heat/
│   ├── models/
│   ├── outputs/
│   ├── scripts/
│   └── tests/
│       └── test_api.py
└── .venv/
```

## Requirements

- Python 3.14
- GDAL command-line tools
- uv package manager

### Install GDAL on macOS

```bash
brew install gdal
```

### Install project dependencies

From the project root:

```bash
cd "/Users/harishrajap/Documents/TakeYouForward/climate-adjusted-property-valueation-tool"
uv sync
```

If `uv` is not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Run the API

From the app folder:

```bash
cd "/Users/harishrajap/Documents/TakeYouForward/climate-adjusted-property-valueation-tool/TamilNadu-Climate-Property"
uv run uvicorn app.main:app --reload
```

Open:

- Swagger docs: http://127.0.0.1:8000/docs
- API root: http://127.0.0.1:8000

## API Endpoint

### POST /predict

Request body:

```json
{
  "district": "Pudukkottai",
  "city": "Pudukkottai",
  "latitude": 10.3797,
  "longitude": 78.8208,
  "area_sqft": 1200,
  "market_rate_per_sqft": 2800
}
```

Example response:

```json
{
  "property": {
    "district": "Pudukkottai",
    "city": "Pudukkottai",
    "latitude": 10.3797,
    "longitude": 78.8208,
    "area_sqft": 1200,
    "market_rate_per_sqft": 2800
  },
  "valuation": {
    "base_value": 3360000.0,
    "risk_score": 0.24,
    "adjustment_percent": 4.8,
    "adjusted_value": 3196800.0
  },
  "risk_breakdown": {
    "flood_exposure": 1,
    "heat_risk": 0.32,
    "tmax_change": 2.1,
    "cyclone_intensity": 0.41,
    "nearest_cyclone_km": 62.4,
    "max_nearby_wind_knots": 58
  },
  "data_sources": {
    "heat": "district_mean",
    "cyclone": "historical_track_100km"
  },
  "data_completeness": 1.0,
  "available_factors": ["Flood", "Heat", "Cyclone"]
}
```

## Notes

- Flood exposure uses the raster data in the `data/flood` folder.
- Heat exposure uses the district/block risk dataset in `data/heat`.
- Cyclone exposure uses historical storm track data in `data/cyclone`.
- The valuation model is currently a rule-based climate risk adjustment service and is intended to be extended for production use.

## Testing

```bash
cd "/Users/harishrajap/Documents/TakeYouForward/climate-adjusted-property-valueation-tool/TamilNadu-Climate-Property"
uv run python -m unittest discover -s tests -v
```

This validates the health route and the prediction route.
# Climate-Adjusted-Property-Valuation
