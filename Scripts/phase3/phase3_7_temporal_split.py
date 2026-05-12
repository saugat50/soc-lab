import pandas as pd
import os

INPUT_5M = "data/processed/features_5min_encoded.parquet"
INPUT_30M = "data/processed/features_30min_encoded.parquet"

OUT_DIR = "data/processed/splits"
os.makedirs(OUT_DIR, exist_ok=True)


def temporal_split(df, train_ratio=0.7):

    df = df.sort_values("timestamp")

    split_point = int(len(df) * train_ratio)

    train = df.iloc[:split_point]
    test = df.iloc[split_point:]

    return train, test


def process(input_path, prefix):

    df = pd.read_parquet(input_path)

    train, test = temporal_split(df)

    train.to_parquet(f"{OUT_DIR}/{prefix}_train.parquet")
    test.to_parquet(f"{OUT_DIR}/{prefix}_test.parquet")

    print(f"[✓] {prefix} train:", len(train))
    print(f"[✓] {prefix} test:", len(test))


def main():

    print("[*] Splitting 5-minute windows...")
    process(INPUT_5M, "5min")

    print("\n[*] Splitting 30-minute windows...")
    process(INPUT_30M, "30min")


if __name__ == "__main__":
    main()
