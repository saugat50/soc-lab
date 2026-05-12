import pandas as pd
import os

SPLIT_DIR = "data/processed/splits"

OUT_DIR = "data/processed/baseline"
os.makedirs(OUT_DIR, exist_ok=True)


def prepare(prefix):

    train_path = f"{SPLIT_DIR}/{prefix}_train.parquet"

    print(f"\n[*] Loading {prefix} training split...")
    df = pd.read_parquet(train_path)

    print("[*] Total train rows:", len(df))

    # Keep mostly normal behavior for baseline
    baseline = df[df["label"] == 0]

    print("[*] Baseline (label=0) rows:", len(baseline))

    # Feature matrix (drop non-ML columns)
    X = baseline.drop(columns=["timestamp", "src_ip", "label"])

    out_path = f"{OUT_DIR}/{prefix}_baseline_features.parquet"
    X.to_parquet(out_path)

    print("[✓] Saved baseline features:", out_path)


def main():

    prepare("5min")
    prepare("30min")


if __name__ == "__main__":
    main()
