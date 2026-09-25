from pydantic import BaseModel, Field


class PropertyInput(BaseModel):
    district: str = Field(..., min_length=1, example="Pudukkottai")
    city: str = Field(..., min_length=1, example="Pudukkottai")
    latitude: float = Field(..., ge=-90, le=90, example=10.3797)
    longitude: float = Field(..., ge=-180, le=180, example=78.8208)
    area_sqft: float = Field(..., gt=0, example=1200)
    market_rate_per_sqft: float = Field(..., gt=0, example=2800)


class PropertyPredictionResponse(BaseModel):
    property: dict
    valuation: dict
    risk_breakdown: dict
    data_sources: dict
    data_completeness: float
    available_factors: list[str]
