import pandas as pd
import joblib
import os

MODEL_DIR = "data/models"
SPLIT_DIR = "data/processed/splits"
OUT_DIR = "data/processed/alerts"

os.makedirs(OUT_DIR, exist_ok=True)

# Thresholds from Phase 4.4
THRESHOLD_5M = -0.162366
THRESHOLD_30M = -0.177436


def score(prefix, threshold):

    print(f"\n[*] Scoring {prefix} windows...")

    model = joblib.load(f"{MODEL_DIR}/if_{prefix}.joblib")

    df = pd.read_parquet(f"{SPLIT_DIR}/{prefix}_test.parquet")

    X = df.drop(columns=["timestamp", "src_ip", "label"])

    scores = -model.decision_function(X)

    df = df.copy()
    df["anomaly_score"] = scores
    df["is_anomaly"] = scores >= threshold

    anomalies = df[df["is_anomaly"]]

    out_path = f"{OUT_DIR}/alerts_{prefix}.parquet"
    anomalies.to_parquet(out_path)

    print("[✓] Total windows:", len(df))
    print("[✓] Anomalies detected:", len(anomalies))
    print("[✓] Saved:", out_path)


def main():

    score("5min", THRESHOLD_5M)
    score("30min", THRESHOLD_30M)


if __name__ == "__main__":
    main()
