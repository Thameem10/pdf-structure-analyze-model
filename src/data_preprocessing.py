from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

BASE_DIR = Path().resolve().parent
DATA_PATH = BASE_DIR / "data" / "labelled" / "features_labeled.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load Data

df = pd.read_csv(DATA_PATH)

if "Id" in df.columns:
    df = df.drop(columns=["Id"])

print("Initial Shape:", df.shape)
print("Sample view:")
print(df.head)

# Drop Noise Columns

drop_cols = ["page_number", "content", "type", "contains_numbering"]
df = df.drop(columns=[col for col in drop_cols if col in df.columns])
print("Shape after dropping noise cols:", df.shape)
print("Sample view:")
print(df.head)

# Fill numeric NaN with median

num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
for col in num_cols:
    df[col] = df[col].fillna(0)

# ---------------------------------------
# Min-Max Scaling
# ---------------------------------------

scaler = MinMaxScaler()

df[num_cols] = scaler.fit_transform(df[num_cols])

print("\nAfter Scaling:")
print(df.head())

# Save

OUTPUT_PATH = PROCESSED_DIR / "pdf_featured_processed_dataset.csv"
df.to_csv(OUTPUT_PATH, index=False)

print(f"\n✔ Saved to: {OUTPUT_PATH}")
print(f"   Final Shape: {df.shape}")
