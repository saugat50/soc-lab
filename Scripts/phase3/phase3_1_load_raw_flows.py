import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

RAW_DIR = "data/raw/cicids2017_raw/CSVs/"
OUTPUT_PATH = "data/processed/raw_flows_combined.parquet"

CHUNK_SIZE = 300_000


def normalize_dtypes(df):
    # Convert all numeric columns to float64 (except obvious IDs/ports)
    for col in df.columns:
        if col in ["src_port", "dst_port"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        elif col not in ["flow_id", "timestamp", "src_ip", "dst_ip", "protocol", "label"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")

    return df


def main():
    print("[*] Streaming raw CICIDS flows with stable schema...")

    files = [
        os.path.join(RAW_DIR, f)
        for f in os.listdir(RAW_DIR)
        if f.endswith(".csv")
    ]

    if not files:
        raise FileNotFoundError("No CSV files found!")

    os.makedirs("data/processed", exist_ok=True)

    writer = None
    total_rows = 0

    for file in files:
        print("\n[*] Processing:", file)

        for chunk in pd.read_csv(file, chunksize=CHUNK_SIZE):

            chunk = normalize_dtypes(chunk)

            table = pa.Table.from_pandas(chunk, preserve_index=False)

            if writer is None:
                writer = pq.ParquetWriter(OUTPUT_PATH, table.schema)

            writer.write_table(table)

            rows = len(chunk)
            total_rows += rows

            print(f"    Wrote {rows} rows (total: {total_rows})")

    if writer:
        writer.close()

    print("\n[✓] Finished loading all raw flows")
    print("[✓] Total rows:", total_rows)
    print("[✓] Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
