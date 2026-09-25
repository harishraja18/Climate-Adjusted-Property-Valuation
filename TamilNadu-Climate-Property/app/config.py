from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
FLOOD_RASTER = DATA_DIR / "flood" / "tamil_nadu_flood_mask_tn_2003_2020.tif"
HEAT_FILE = DATA_DIR / "heat" / "heat_risk_dataset.csv"
CYCLONE_FILE = DATA_DIR / "cyclone" / "tamil_nadu_cyclone_tracks_1980_2025.csv"
