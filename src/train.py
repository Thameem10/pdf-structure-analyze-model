import time
import joblib
import numpy as np
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, RandomizedSearchCV
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score
from utils import load_data, split_data


BASE_DIR = Path(__file__).resolve().parent.parent
PLOT_DIR  = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"
PLOT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------
# Load Processed Data using utils
# ---------------------------------------

df = load_data("pdf_featured_processed_dataset.csv")

X_train, X_test, y_train, y_test = split_data(df, target_column="label")

print("Training shape:", X_train.shape)
print("Testing shape:", X_test.shape)

# ---------------------------------------
# Model Definition (Random Forest)
# ---------------------------------------

model = RandomForestClassifier(random_state=42)

param_grid = {
    "n_estimators": [100],      
    "max_depth": [6, 8, 10],             # Pushing depth even lower
    "min_samples_split": [20, 30, 50],   # Forcing much larger groups before splitting
    "min_samples_leaf": [10, 15, 20]     # Forcing larger final prediction buckets
}

kfold = KFold(n_splits=3, shuffle=True, random_state=42)  # reduced from 5 to 3 folds

grid = RandomizedSearchCV(                                  # switched from GridSearchCV
    model,
    param_grid,
    n_iter=20,
    cv=kfold,
    scoring="f1_weighted",
    n_jobs=-1,
    verbose=1,
    random_state=42
)

# ---------------------------------------
# Train Model (with timing)
# ---------------------------------------

print("\nStarting hyperparameter search...")
start = time.time()

grid.fit(X_train, y_train)

search_time = time.time() - start
print(f"\nHyperparameter Search Time: {search_time:.2f} seconds")

print("Best Parameters:", grid.best_params_)
print("Best CV R2:", grid.best_score_)

# Retrain best model with 300 estimators for better accuracy
print("\nRetraining best model with 300 estimators...")
retrain_start = time.time()

best_params = grid.best_params_.copy()
best_params["n_estimators"] = 300

best_model = RandomForestClassifier(**best_params, random_state=42)
best_model.fit(X_train, y_train)

retrain_time = time.time() - retrain_start
total_time = search_time + retrain_time

print(f"Retraining Time:            {retrain_time:.2f} seconds")
print(f"Total Training Time:        {total_time:.2f} seconds")

print("\n---------------------------------------")
print("        FINAL TEST PERFORMANCE")
print("---------------------------------------")

# Predictions
y_pred = best_model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Detailed Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt="d",
            xticklabels=best_model.classes_,
            yticklabels=best_model.classes_)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.savefig(PLOT_DIR / "confusion_matrix.png", dpi=150)

print("\n---------------------------------------")
print("          MODEL DIAGNOSIS")
print("---------------------------------------")

# Compare Training vs Testing Accuracy (Overfitting Check)
y_train_pred = best_model.predict(X_train)

train_acc = accuracy_score(y_train, y_train_pred)
test_acc = accuracy

print(f"Training Accuracy: {train_acc:.4f}")
print(f"Testing Accuracy:  {test_acc:.4f}")

if (train_acc - test_acc) > 0.05:
    print("=> Diagnosis: Model might be OVERFITTING.")
elif train_acc < 0.60:
    print("=> Diagnosis: Model might be UNDERFITTING.")
else:
    print("=> Diagnosis: Model is generalizing well!")

# Cross Validation
print("\nRunning 5-Fold Cross-Validation on Training Data...")

cv_scores = cross_val_score(
    best_model,
    X_train,
    y_train,
    cv=5,
    scoring='f1_weighted',
    n_jobs=-1
)

print(f"CV F1 Scores for each fold: {np.round(cv_scores, 4)}")
print(f"Average CV F1: {cv_scores.mean():.4f}")
print(f"Score Variance (+/-): {cv_scores.std() * 2:.4f}")

if cv_scores.std() > 0.05:
    print("=> Diagnosis: High variance across folds.")
else:
    print("=> Diagnosis: Low variance. Model is stable.")
    
# ---------------------------------------
# Save Model
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models"
MODEL_PATH.mkdir(parents=True, exist_ok=True)

joblib.dump(best_model, MODEL_PATH / "pdf_structure_analyze_model.pkl")

print("\nModel saved successfully.")