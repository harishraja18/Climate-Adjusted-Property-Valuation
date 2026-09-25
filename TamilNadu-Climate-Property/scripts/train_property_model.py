import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor


# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "data/processed/chennai_property_clean.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "property_valuation_xgb.joblib")

TARGET = "SALES_PRICE"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("PROPERTY VALUATION MODEL TRAINING")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

print(f"\nDataset shape: {df.shape}")

# Separate features and target
X = df.drop(columns=[TARGET])
y = df[TARGET]


# ============================================================
# FEATURE TYPES
# ============================================================

categorical_features = [
    "AREA",
    "SALE_COND",
    "PARK_FACIL",
    "BUILDTYPE",
    "UTILITY_AVAIL",
    "STREET",
    "MZZONE",
]

numeric_features = [
    "INT_SQFT",
    "DIST_MAINROAD",
    "N_BEDROOM",
    "N_BATHROOM",
    "N_ROOM",
    "QS_ROOMS",
    "QS_BATHROOM",
    "QS_BEDROOM",
    "QS_OVERALL",
    "COMMIS",
]


print("\nCategorical features:")
for feature in categorical_features:
    print(f"  - {feature}")

print("\nNumeric features:")
for feature in numeric_features:
    print(f"  - {feature}")


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)

print("\nTrain/Test split:")
print(f"  Training samples: {X_train.shape[0]}")
print(f"  Testing samples:  {X_test.shape[0]}")


# ============================================================
# PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False,
            ),
            categorical_features,
        ),
        (
            "numeric",
            "passthrough",
            numeric_features,
        ),
    ]
)


# ============================================================
# MODEL
# ============================================================

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1,
)


# ============================================================
# PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)


# ============================================================
# TRAIN
# ============================================================

print("\nTraining XGBoost regression model...")

pipeline.fit(X_train, y_train)

print("Training complete.")


# ============================================================
# PREDICTION
# ============================================================

y_pred = pipeline.predict(X_test)


# ============================================================
# EVALUATION
# ============================================================

mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"\nMAE  : ₹{mae:,.2f}")
print(f"RMSE : ₹{rmse:,.2f}")
print(f"R²   : {r2:.4f}")


# ============================================================
# SAMPLE PREDICTIONS
# ============================================================

results = X_test.copy()

results["actual_price"] = y_test
results["predicted_price"] = y_pred
results["error"] = results["predicted_price"] - results["actual_price"]

print("\n" + "=" * 60)
print("SAMPLE PREDICTIONS")
print("=" * 60)

print(
    results[
        [
            "AREA",
            "INT_SQFT",
            "N_BEDROOM",
            "N_BATHROOM",
            "actual_price",
            "predicted_price",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# SAVE MODEL
# ============================================================

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(pipeline, MODEL_PATH)

print("\n" + "=" * 60)
print("MODEL SAVED")
print("=" * 60)

print(f"\nModel path: {MODEL_PATH}")