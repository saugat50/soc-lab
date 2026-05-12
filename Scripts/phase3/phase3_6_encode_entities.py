import pandas as pd
import os

INPUT_5M = "data/processed/features_5min_scaled.parquet"
INPUT_30M = "data/processed/features_30min_scaled.parquet"

OUT_5M = "data/processed/features_5min_encoded.parquet"
OUT_30M = "data/processed/features_30min_encoded.parquet"

MAP_PATH = "data/processed/entity_map.csv"


def encode(df, entity_map=None):

    if entity_map is None:
        unique_entities = df["src_ip"].unique()
        entity_map = {e: i for i, e in enumerate(unique_entities)}

    df["entity_id"] = df["src_ip"].map(entity_map)

    return df, entity_map


def main():

    print("[*] Encoding entities for 5-minute windows...")
    df5 = pd.read_parquet(INPUT_5M)
    df5_enc, entity_map = encode(df5)

    df5_enc.to_parquet(OUT_5M)

    print("[*] Encoding entities for 30-minute windows...")
    df30 = pd.read_parquet(INPUT_30M)
    df30_enc, _ = encode(df30, entity_map)

    df30_enc.to_parquet(OUT_30M)

    # Save mapping
    pd.DataFrame(
        list(entity_map.items()),
        columns=["src_ip", "entity_id"]
    ).to_csv(MAP_PATH, index=False)

    print("[✓] Saved encoded datasets + entity map")


if __name__ == "__main__":
    main()
