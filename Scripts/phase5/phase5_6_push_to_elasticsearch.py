import json
import requests
from requests.exceptions import RequestException

ES = "http://localhost:9200"
INDEX = "soc-alerts"
FILE = "data/processed/triaged_alerts/triaged_alerts_5min.json"


def push(doc):
    try:
        r = requests.post(
            f"{ES}/{INDEX}/_doc",
            headers={"Content-Type": "application/json"},
            json=doc,
            timeout=3   # IMPORTANT
        )

        if r.status_code in (200, 201):
            return True
        else:
            print("[X] Failed:", r.status_code, r.text)
            return False

    except RequestException as e:
        print("[X] Connection error:", e)
        return False


def main():

    with open(FILE) as f:
        alerts = json.load(f)

    print(f"[*] Sending {len(alerts)} alerts to Elasticsearch...")

    sent = 0

    for i, a in enumerate(alerts, 1):

        doc = {
            "timestamp": a["timestamp"].replace(" ", "T"),
            "entity": a["entity"],
            "window": a["window"],
            "anomaly_score": float(a["anomaly_score"]),
            "severity": a["severity"],
            "model": a["model"],

            "flow_count": int(a["context"]["flow_count"]),
            "total_bytes": float(a["context"]["total_bytes"]),
            "auth_events": int(a["context"]["auth_events"]),
            "failed_auths": int(a["context"]["failed_auths"]),
            "unique_dst_ips": int(a["context"]["unique_dst_ips"])
        }

        if push(doc):
            sent += 1

        if i % 500 == 0:
            print(f"   → Sent {i}/{len(alerts)}")

    print(f"[✓] Indexed {sent}/{len(alerts)} alerts")


if __name__ == "__main__":
    main()
