import json
import os
import ipaddress

ALERT_OBJ_DIR = "data/processed/alert_objects"
OUT_DIR = "data/processed/enriched_alerts"

os.makedirs(OUT_DIR, exist_ok=True)

# Simulated malicious IPs (demo)
MALICIOUS_IPS = {
    "192.168.10.50",
    "10.0.0.99"
}

# Simulated asset importance
CRITICAL_ASSETS = {
    "192.168.10.1": "high",
    "192.168.10.2": "high"
}


def get_reputation(ip):

    if ip in MALICIOUS_IPS:
        return "malicious"

    try:
        if ipaddress.ip_address(ip).is_private:
            return "internal"
    except:
        pass

    return "unknown"


def map_mitre(context):

    techniques = []

    if context["failed_auths"] > 5:
        techniques.append("Brute Force")

    if context["unique_dst_ips"] > 10:
        techniques.append("Lateral Movement")

    if context["total_bytes"] > 1e6:
        techniques.append("Data Exfiltration")

    return techniques


def enrich(prefix):

    print(f"\n[*] Enriching {prefix} alerts...")

    with open(f"{ALERT_OBJ_DIR}/alert_objects_{prefix}.json") as f:
        alerts = json.load(f)

    enriched = []

    for alert in alerts:

        ip = alert["entity"]
        ctx = alert["context"]

        alert["enrichment"] = {
            "ip_reputation": get_reputation(ip),
            "asset_criticality": CRITICAL_ASSETS.get(ip, "normal"),
            "mitre_techniques": map_mitre(ctx)
        }

        enriched.append(alert)

    out_path = f"{OUT_DIR}/enriched_alerts_{prefix}.json"

    with open(out_path, "w") as f:
        json.dump(enriched, f, indent=2)

    print("[✓] Enriched alerts:", len(enriched))
    print("[✓] Saved:", out_path)


def main():

    enrich("5min")
    enrich("30min")


if __name__ == "__main__":
    main()
