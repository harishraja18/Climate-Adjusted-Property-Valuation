import pandas as pd
from pathlib import Path


RAW_PATH = Path("data/raw/chennai_house_price_prediction.csv")
OUTPUT_PATH = Path("data/processed/chennai_property_clean.csv")


def main():
    print("=" * 70)
    print("PROPERTY DATA PREPARATION")
    print("=" * 70)

    df = pd.read_csv(RAW_PATH)

    print(f"\nOriginal shape: {df.shape}")

    # Remove identifier
    df = df.drop(columns=["PRT_ID"])

    # Handle missing numeric values
    numeric_columns = [
        "N_BEDROOM",
        "N_BATHROOM",
        "QS_OVERALL",
    ]

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    # Normalize categorical text
    categorical_columns = [
        "AREA",
        "SALE_COND",
        "PARK_FACIL",
        "BUILDTYPE",
        "UTILITY_AVAIL",
        "STREET",
        "MZZONE",
    ]

    for column in categorical_columns:
        df[column] = df[column].astype(str).str.strip()

    # Make sure target is numeric
    df["SALES_PRICE"] = pd.to_numeric(
        df["SALES_PRICE"],
        errors="coerce",
    )

    # Remove rows where target is unavailable
    df = df.dropna(subset=["SALES_PRICE"])

    print(f"Cleaned shape: {df.shape}")

    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()