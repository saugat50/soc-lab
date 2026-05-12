import json
import os

ENRICH_DIR = "data/processed/enriched_alerts"
OUT_DIR = "data/processed/triaged_alerts"

os.makedirs(OUT_DIR, exist_ok=True)


def assign_severity(alert):

    score = alert["anomaly_score"]
    enrich = alert["enrichment"]

    rep = enrich["ip_reputation"]
    criticality = enrich["asset_criticality"]
    mitre = enrich["mitre_techniques"]

    # HIGH severity
    if score > 0.15 and (
        rep == "malicious"
        or criticality == "high"
        or len(mitre) >= 2
    ):
        return "high"

    # MEDIUM severity
    if score > 0.1 or len(mitre) == 1:
        return "medium"

    # LOW severity
    return "low"


def triage(prefix):

    print(f"\n[*] Triaging {prefix} alerts...")

    with open(f"{ENRICH_DIR}/enriched_alerts_{prefix}.json") as f:
        alerts = json.load(f)

    for alert in alerts:
        alert["severity"] = assign_severity(alert)

    out_path = f"{OUT_DIR}/triaged_alerts_{prefix}.json"

    with open(out_path, "w") as f:
        json.dump(alerts, f, indent=2)

    print("[✓] Triaged alerts:", len(alerts))
    print("[✓] Saved:", out_path)


def main():

    triage("5min")
    triage("30min")


if __name__ == "__main__":
    main()
