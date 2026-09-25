from fastapi import FastAPI

from app.climate_engine import calculate_property_valuation
from app.schemas import PropertyInput

app = FastAPI(
    title="Tamil Nadu Climate-Adjusted Property Valuation API",
    description=(
        "Backend API for climate-adjusted property valuation using flood, heat, "
        "and cyclone exposure data for Tamil Nadu."
    ),
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Tamil Nadu Climate-Adjusted Property Valuation API",
        "status": "running",
        "service": "property_valuation",
    }


@app.post("/predict")
def predict_property(property: PropertyInput):
    result = calculate_property_valuation(
        district=property.district,
        city=property.city,
        latitude=property.latitude,
        longitude=property.longitude,
        area_sqft=property.area_sqft,
        market_rate_per_sqft=property.market_rate_per_sqft,
    )

    return {
        "property": {
            "district": property.district,
            "city": property.city,
            "latitude": property.latitude,
            "longitude": property.longitude,
            "area_sqft": property.area_sqft,
            "market_rate_per_sqft": property.market_rate_per_sqft,
        },
        "valuation": {
            "base_value": result["base_value"],
            "risk_score": result["risk"]["risk_score"],
            "adjustment_percent": result["risk"]["adjustment_percent"],
            "adjusted_value": result["adjusted_value"],
        },
        "risk_breakdown": {
            "flood_exposure": result["flood_exposure"],
            "heat_risk": result["heat"]["heat_risk"],
            "tmax_change": result["heat"]["tmax_change"],
            "cyclone_intensity": result["cyclone"]["cyclone_intensity"],
            "nearest_cyclone_km": result["cyclone"]["nearest_cyclone_km"],
            "max_nearby_wind_knots": result["cyclone"]["max_nearby_wind_knots"],
        },
        "data_sources": {
            "heat": result["heat"]["heat_source"],
            "cyclone": result["cyclone"]["cyclone_source"],
        },
        "data_completeness": result["risk"]["data_completeness"],
        "available_factors": result["risk"]["available_factors"],
    }