import pandas as pd
import os

FLOW_PATH = "data/processed/unified_flow_events.parquet"

AUTH_NORMAL = "data/raw/auth/auth_normal.json"
AUTH_ATTACK = "data/raw/auth/auth_attacks.json"

OUTPUT_PATH = "data/processed/unified_all_events.parquet"


def load_auth():
    print("[*] Reading auth normal logs...")
    normal = pd.read_json(AUTH_NORMAL, lines=True)

    print("[*] Reading auth attack logs...")
    attack = pd.read_json(AUTH_ATTACK, lines=True)

    # Labels
    normal["label"] = 0
    attack["label"] = 1

    auth = pd.concat([normal, attack], ignore_index=True)

    auth_events = pd.DataFrame()

    # Force UTC-aware timestamps
    auth_events["timestamp"] = pd.to_datetime(
        auth["timestamp"], errors="coerce", utc=True
    )

    auth_events["event_type"] = "auth"

    auth_events["src_ip"] = auth["src_ip"]
    auth_events["dst_ip"] = auth["host"]

    auth_events["src_port"] = None
    auth_events["dst_port"] = None
    auth_events["protocol"] = auth["auth_type"]

    auth_events["bytes"] = None
    auth_events["packets"] = None
    auth_events["duration"] = None

    auth_events["user"] = auth["user"]
    auth_events["host"] = auth["host"]
    auth_events["auth_result"] = auth["status"]

    auth_events["label"] = auth["label"]

    return auth_events


def main():
    print("[*] Loading flow events...")
    flow_events = pd.read_parquet(FLOW_PATH)

    # Force flow timestamps to UTC-aware
    flow_events["timestamp"] = pd.to_datetime(
        flow_events["timestamp"], errors="coerce", utc=True
    )

    # Add missing SOC fields to flows
    flow_events["user"] = None
    flow_events["host"] = None
    flow_events["auth_result"] = None

    print("[*] Loading auth events...")
    auth_events = load_auth()

    print("[*] Flow rows:", len(flow_events))
    print("[*] Auth rows:", len(auth_events))

    print("[*] Merging multi-source events...")

    all_events = pd.concat([flow_events, auth_events], ignore_index=True)

    print("[*] Sorting by timestamp...")
    all_events = all_events.sort_values("timestamp")

    os.makedirs("data/processed", exist_ok=True)
    all_events.to_parquet(OUTPUT_PATH)

    print("\n[✓] Unified multi-source event table created")
    print("[✓] Total rows:", len(all_events))
    print("[✓] Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
