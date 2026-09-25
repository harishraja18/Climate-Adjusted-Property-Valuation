from app.climate_engine import calculate_property_valuation


result = calculate_property_valuation(
    district="Pudukkottai",
    city="Pudukkottai",
    latitude=10.3797,
    longitude=78.8208,
    area_sqft=1200,
    market_rate_per_sqft=2800,
)


print("=" * 60)
print("CLIMATE PROPERTY VALUATION TEST")
print("=" * 60)

print("\nBase Value:")
print(f"₹{result['base_value']:,.2f}")

print("\nFlood:")
print(result["flood_exposure"])

print("\nHeat:")
print(result["heat"])

print("\nCyclone:")
print(result["cyclone"])

print("\nClimate Risk:")
print(result["risk"])

print("\nAdjusted Value:")
print(f"₹{result['adjusted_value']:,.2f}")

print("=" * 60)