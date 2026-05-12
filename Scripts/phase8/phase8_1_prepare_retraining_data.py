import pandas as pd
import os

FEEDBACK_PATH = "data/processed/feedback/analyst_feedback.csv"
ALERTS_5MIN = "data/processed/alerts/alerts_5min.parquet"
OUTPUT_PATH = "data/processed/retraining/retraining_dataset_5min.parquet"

def main():

    if not os.path.exists(FEEDBACK_PATH):
        raise FileNotFoundError("No analyst feedback found!")

    print("[*] Loading analyst feedback...")
    feedback = pd.read_csv(FEEDBACK_PATH)

    print("[*] Loading alert windows...")
    alerts = pd.read_parquet(ALERTS_5MIN)

    # Normalize timestamps (important!)
    alerts["timestamp"] = pd.to_datetime(alerts["timestamp"], utc=True)
    feedback["timestamp"] = pd.to_datetime(feedback["timestamp"], utc=True)

    # Use src_ip as entity
    alerts = alerts.rename(columns={"src_ip": "entity"})

    print("[*] Merging feedback with alerts...")

    merged = alerts.merge(
        feedback,
        on=["timestamp", "entity"],
        how="inner"
    )

    # Map analyst decisions
    merged["final_label"] = merged["analyst_label"].map({
        "true_positive": 1,
        "false_positive": 0
    })

    merged = merged.dropna(subset=["final_label"])

    print("[✓] Retraining samples:", len(merged))

    os.makedirs("data/processed/retraining", exist_ok=True)
    merged.to_parquet(OUTPUT_PATH)

    print("[✓] Saved retraining dataset:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
