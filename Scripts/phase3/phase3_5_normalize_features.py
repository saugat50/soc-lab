import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

INPUT_5M = "data/processed/features_5min.parquet"
INPUT_30M = "data/processed/features_30min.parquet"

OUT_5M = "data/processed/features_5min_scaled.parquet"
OUT_30M = "data/processed/features_30min_scaled.parquet"


def scale(df):

    df = df.fillna(0)

    labels = df["label"]
    meta = df[["timestamp", "src_ip"]]

    features = df.drop(columns=["timestamp", "src_ip", "label"])

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    scaled_df = pd.DataFrame(scaled, columns=features.columns)

    scaled_df["timestamp"] = meta["timestamp"].values
    scaled_df["src_ip"] = meta["src_ip"].values
    scaled_df["label"] = labels.values

    return scaled_df


def main():

    print("[*] Scaling 5-minute features...")
    df5 = pd.read_parquet(INPUT_5M)
    scaled5 = scale(df5)
    scaled5.to_parquet(OUT_5M)
    print("[✓] Saved:", OUT_5M)

    print("[*] Scaling 30-minute features...")
    df30 = pd.read_parquet(INPUT_30M)
    scaled30 = scale(df30)
    scaled30.to_parquet(OUT_30M)
    print("[✓] Saved:", OUT_30M)


if __name__ == "__main__":
    main()
