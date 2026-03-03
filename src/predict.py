import joblib
import pandas as pd
import json
from pathlib import Path

# ---------------------------------------
# Paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
INPUT_JSON_PATH = BASE_DIR / "data" / "testing" / "demo_testing.json"

OUTPUT_DIR = BASE_DIR / "data" / "predictions"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSON_PATH = OUTPUT_DIR / "demo_testing_with_predictions.json"

# ---------------------------------------
# Load Model & Scaler
# ---------------------------------------

model = joblib.load(MODEL_DIR / "pdf_structure_analyze_model.pkl")
scaler = joblib.load(MODEL_DIR / "minmax_scaler.pkl")

print("Model and scaler loaded successfully.")

# ---------------------------------------
# Load JSON Input
# ---------------------------------------

with open(INPUT_JSON_PATH, "r") as f:
    data = json.load(f)

# Convert to list if single object
if isinstance(data, dict):
    data = [data]

df = pd.DataFrame(data)

# ---------------------------------------
# Ensure Correct Feature Order
# ---------------------------------------



expected_columns = list(scaler.feature_names_in_)

for col in expected_columns:
    if col not in df.columns:
        df[col] = 0

# Select only model-required columns (but keep original df untouched)
df_features = df[expected_columns]

# ---------------------------------------
# Apply Min-Max Scaling
# ---------------------------------------

scaled_values = scaler.transform(df_features)
df_scaled = pd.DataFrame(scaled_values, columns=expected_columns)

# ---------------------------------------
# Prediction
# ---------------------------------------

predictions = model.predict(df_scaled)

# ---------------------------------------
# Attach Prediction to Original JSON
# ---------------------------------------

for i in range(len(data)):
    data[i]["predicted_label"] = predictions[i]

# ---------------------------------------
# Save Updated JSON
# ---------------------------------------

with open(OUTPUT_JSON_PATH, "w") as f:
    json.dump(data, f, indent=4)

print(f"\nPredictions saved to: {OUTPUT_JSON_PATH}")