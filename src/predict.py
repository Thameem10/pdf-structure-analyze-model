import joblib
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models"

# 1. Load BOTH the model and the scaler
model = joblib.load(MODEL_PATH / "pdf_structure_analyze_model.pkl")

print("Model loaded successfully.")

# 2. Create New Sample Input
new_sample = pd.DataFrame(
    [[1, 1, 1, 0.14, 0.12, 0.06, 0.27, 0 , 0 , 0 , 0 ]],
    columns=[
        "font_size", "font_size_relative","is_bold","uppercase_ratio",
        "text_length","y_position","block_width","image_area","table_rows",
        "table_columns","image_aspect_ratio"
    ]
)

# 3. Fix Feature Order (Just in case)
expected_columns = model.feature_names_in_
new_sample = new_sample[expected_columns]

# 4. Make Prediction & Convert

predicted_label = model.predict(new_sample)


print(f"\nPredicted Label: ${predicted_label}")