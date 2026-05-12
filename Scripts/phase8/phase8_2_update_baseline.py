import pandas as pd
import os

OLD_BASELINE = "data/processed/baseline/5min_baseline_features.parquet"
RETRAIN_DATA = "data/processed/retraining/retraining_dataset_5min.parquet"
NEW_BASELINE = "data/processed/retraining/updated_baseline_5min.parquet"

def main():

    print("[*] Loading old baseline...")
    baseline = pd.read_parquet(OLD_BASELINE)

    print("[*] Loading retraining corrections...")
    retrain = pd.read_parquet(RETRAIN_DATA)

    # Keep only analyst-confirmed normal
    corrected_normals = retrain[retrain["final_label"] == 0]

    feature_cols = baseline.columns

    corrected_normals = corrected_normals[feature_cols]

    updated = pd.concat([baseline, corrected_normals], ignore_index=True)

    print("[✓] Old baseline:", len(baseline))
    print("[✓] Added normals:", len(corrected_normals))
    print("[✓] New baseline:", len(updated))

    os.makedirs("data/processed/retraining", exist_ok=True)
    updated.to_parquet(NEW_BASELINE)

    print("[✓] Saved updated baseline:", NEW_BASELINE)

if __name__ == "__main__":
    main()
