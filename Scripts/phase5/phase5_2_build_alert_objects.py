import pandas as pd
import os

ALERT_DIR = "data/processed/alerts"
FEATURE_DIR = "data/processed"
OUT_DIR = "data/processed/alert_objects"

os.makedirs(OUT_DIR, exist_ok=True)

RAW_FEATURES = [
    "flow_count",
    "auth_events",
    "failed_auths",
    "unique_dst_ips",
    "total_bytes"
]


def build(prefix):

    print(f"\n[*] Building RAW alert objects for {prefix}...")

    # Load anomaly windows (these contain SCALED features)
    alerts_df = pd.read_parquet(f"{ALERT_DIR}/alerts_{prefix}.parquet")

    # Remove scaled context columns if present
    for f in RAW_FEATURES:
        if f in alerts_df.columns:
            alerts_df = alerts_df.drop(columns=[f])

    # Load true RAW feature windows
    raw_df = pd.read_parquet(f"{FEATURE_DIR}/features_{prefix}.parquet")

    # Force timestamps same format
    alerts_df["timestamp"] = pd.to_datetime(alerts_df["timestamp"], utc=True)
    raw_df["timestamp"] = pd.to_datetime(raw_df["timestamp"], utc=True)

    # Merge to bring raw values
    merged = alerts_df.merge(
        raw_df[["timestamp", "src_ip"] + RAW_FEATURES],
        on=["timestamp", "src_ip"],
        how="left"
    )

    alert_objects = []

    for _, row in merged.iterrows():

        context = {}

        for f in RAW_FEATURES:
            context[f] = row[f]

        alert = {
            "timestamp": str(row["timestamp"]),
            "entity": row["src_ip"],
            "window": prefix,
            "anomaly_score": float(row["anomaly_score"]),
            "model": "IsolationForest",
            "context": context
        }

        alert_objects.append(alert)

    out_path = f"{OUT_DIR}/alert_objects_{prefix}.json"

    pd.DataFrame(alert_objects).to_json(
        out_path,
        orient="records",
        indent=2
    )

    print("[✓] Total alerts:", len(alert_objects))
    print("[✓] Saved:", out_path)


def main():

    build("5min")
    build("30min")


if __name__ == "__main__":
    main()
