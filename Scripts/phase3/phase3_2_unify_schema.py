import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import os

INPUT_PATH = "data/processed/raw_flows_combined.parquet"
OUTPUT_PATH = "data/processed/unified_flow_events.parquet"

BATCH_SIZE = 200_000


def process_batch(df):
    unified = pd.DataFrame()

    unified["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    unified["event_type"] = "flow"

    unified["src_ip"] = df["src_ip"]
    unified["dst_ip"] = df["dst_ip"]

    unified["src_port"] = df["src_port"]
    unified["dst_port"] = df["dst_port"]

    unified["protocol"] = df["protocol"]

    # Core SOC metrics
    unified["bytes"] = df["total_payload_bytes"]
    unified["packets"] = df["packets_count"]
    unified["duration"] = df["duration"]

    # Binary label
    unified["label"] = df["label"].apply(
        lambda x: 0 if str(x).lower() == "benign" else 1
    )

    return unified


def main():
    print("[*] Building unified SOC flow schema...")

    parquet_file = pq.ParquetFile(INPUT_PATH)

    writer = None
    total_rows = 0

    for batch in parquet_file.iter_batches(batch_size=BATCH_SIZE):
        df = batch.to_pandas()

        unified_df = process_batch(df)

        table = pa.Table.from_pandas(unified_df, preserve_index=False)

        if writer is None:
            os.makedirs("data/processed", exist_ok=True)
            writer = pq.ParquetWriter(OUTPUT_PATH, table.schema)

        writer.write_table(table)

        rows = len(unified_df)
        total_rows += rows

        print(f"    Processed {rows} rows (total: {total_rows})")

        del df
        del unified_df

    if writer:
        writer.close()

    print("\n[✓] Unified flow events created")
    print("[✓] Total rows:", total_rows)
    print("[✓] Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
