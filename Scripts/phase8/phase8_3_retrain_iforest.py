import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

BASELINE_PATH = "data/processed/retraining/updated_baseline_5min.parquet"
MODEL_PATH = "data/models/if_5min_retrained.joblib"

def main():

    print("[*] Loading updated baseline...")
    X = pd.read_parquet(BASELINE_PATH)

    print("[*] Retraining Isolation Forest...")

    model = IsolationForest(
        n_estimators=300,
        contamination=0.02,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X)

    os.makedirs("data/models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("[✓] Saved retrained model:", MODEL_PATH)

if __name__ == "__main__":
    main()
