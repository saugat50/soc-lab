import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import os

INPUT_PATH = "data/processed/unified_all_events.parquet"
OUTPUT_5M = "data/processed/features_5min.parquet"
OUTPUT_30M = "data/processed/features_30min.parquet"

BATCH_SIZE = 300_000


def aggregate_window(df, window):

    df = df.set_index("timestamp")

    results = []

    grouped = df.groupby("src_ip")

    for src_ip, g in grouped:

        # Resample by window
        resampled = g.resample(window)

        agg = resampled.agg(
            flow_count=("event_type", lambda x: (x == "flow").sum()),
            total_bytes=("bytes", "sum"),
            mean_bytes=("bytes", "mean"),
            total_packets=("packets", "sum"),
            mean_duration=("duration", "mean"),
            unique_dst_ips=("dst_ip", pd.Series.nunique),
            auth_events=("event_type", lambda x: (x == "auth").sum()),
            failed_auths=("auth_result", lambda x: (x == "failure").sum()),
            successful_auths=("auth_result", lambda x: (x == "success").sum()),
            label=("label", "max")
        )

        agg["src_ip"] = src_ip

        results.append(agg.reset_index())

    if results:
        return pd.concat(results, ignore_index=True)
    else:
        return pd.DataFrame()


def stream_aggregate(window, output_path):

    print(f"\n[*] Aggregating {window} windows...")

    parquet_file = pq.ParquetFile(INPUT_PATH)

    writer = None
    total_rows = 0

    for batch in parquet_file.iter_batches(batch_size=BATCH_SIZE):

        df = batch.to_pandas()

        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

        agg_df = aggregate_window(df, window)

        if len(agg_df) == 0:
            continue

        table = pa.Table.from_pandas(agg_df, preserve_index=False)

        if writer is None:
            os.makedirs("data/processed", exist_ok=True)
            writer = pq.ParquetWriter(output_path, table.schema)

        writer.write_table(table)

        rows = len(agg_df)
        total_rows += rows

        print(f"    Wrote {rows} rows (total: {total_rows})")

        del df
        del agg_df

    if writer:
        writer.close()

    print(f"[✓] Finished {window} aggregation")
    print(f"[✓] Total rows: {total_rows}")
    print(f"[✓] Saved to: {output_path}")


def main():

    stream_aggregate("5min", OUTPUT_5M)
    stream_aggregate("30min", OUTPUT_30M)


if __name__ == "__main__":
    main()
