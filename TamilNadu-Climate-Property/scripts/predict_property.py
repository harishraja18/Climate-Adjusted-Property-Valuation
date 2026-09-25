import joblib
import pandas as pd


MODEL_PATH = "models/property_valuation_xgb.joblib"


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)

print("=" * 60)
print("PROPERTY VALUATION PREDICTION")
print("=" * 60)


# ============================================================
# PROPERTY INPUT
# ============================================================

property_data = {
    "AREA": "Velachery",
    "INT_SQFT": 1500,
    "DIST_MAINROAD": 50,
    "N_BEDROOM": 3,
    "N_BATHROOM": 2,
    "N_ROOM": 5,
    "SALE_COND": "AbNormal",
    "PARK_FACIL": "Yes",
    "BUILDTYPE": "House",
    "UTILITY_AVAIL": "AllPub",
    "STREET": "Paved",
    "MZZONE": "RH",
    "QS_ROOMS": 4.0,
    "QS_BATHROOM": 4.0,
    "QS_BEDROOM": 4.0,
    "QS_OVERALL": 4.0,
    "COMMIS": 0,
}


# Convert dictionary into DataFrame
input_df = pd.DataFrame([property_data])


# ============================================================
# PREDICT
# ============================================================

predicted_price = model.predict(input_df)[0]


# ============================================================
# OUTPUT
# ============================================================

print("\nProperty:")
print(f"  Area        : {property_data['AREA']}")
print(f"  Built Area  : {property_data['INT_SQFT']} sqft")
print(f"  Bedrooms    : {property_data['N_BEDROOM']}")
print(f"  Bathrooms   : {property_data['N_BATHROOM']}")

print("\nPredicted Market Price:")
print(f"  ₹{predicted_price:,.2f}")

print("\n" + "=" * 60)