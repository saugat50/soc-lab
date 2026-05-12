import json
import time
import requests
from pathlib import Path

# =========================
# CONFIG
# =========================

# 👉 IMPORTANT: Use your VM IP, NOT localhost
SHUFFLE_WEBHOOK_URL = "http://192.168.29.149:3001/api/v1/hooks/webhook_f0afcfd3-243a-49c3-9c29-04c5e59924bd"

ALERT_FILE_5MIN = "data/processed/triaged_alerts/triaged_alerts_5min.json"

# Production-like tuning
SEND_ONLY_SEVERITY = ["medium", "high"]
MAX_ALERTS = 10            # demo cap (set None for unlimited)
DELAY_SECONDS = 1          # simulate real-time feed
TIMEOUT = 10               # request timeout
MAX_RETRIES = 3


# =========================
# HELPERS
# =========================

def load_alerts(path):
    print(f"[*] Loading alerts from {path}")
    with open(path, "r") as f:
        return json.load(f)


def should_send(alert):
    return alert.get("severity") in SEND_ONLY_SEVERITY


def send_with_retry(alert, idx):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.post(
                SHUFFLE_WEBHOOK_URL,
                json=alert,
                timeout=TIMEOUT
            )

            if r.status_code == 200:
                try:
                    resp = r.json()
                except Exception:
                    resp = r.text

                if isinstance(resp, dict) and resp.get("success") is True:
                    print(f"[✓] Alert {idx} sent successfully")
                    return True
                else:
                    print(f"[!] Alert {idx} response: {resp}")

            else:
                print(f"[X] Alert {idx} failed | Status: {r.status_code} | Response: {r.text}")

        except Exception as e:
            print(f"[X] Alert {idx} exception (attempt {attempt}): {e}")

        time.sleep(1)

    print(f"[X] Alert {idx} permanently failed after retries")
    return False


# =========================
# MAIN STREAMER
# =========================

def main():
    alerts = load_alerts(ALERT_FILE_5MIN)

    # Filter actionable alerts
    actionable = [a for a in alerts if should_send(a)]

    print(f"[*] Total alerts loaded: {len(alerts)}")
    print(f"[*] Actionable (medium/high): {len(actionable)}")

    if MAX_ALERTS:
        actionable = actionable[:MAX_ALERTS]
        print(f"[*] Limiting to {len(actionable)} alerts for demo")

    sent = 0
    failed = 0

    print("\n[*] Starting real-time alert stream...\n")

    for idx, alert in enumerate(actionable, start=1):
        ok = send_with_retry(alert, idx)

        if ok:
            sent += 1
        else:
            failed += 1

        time.sleep(DELAY_SECONDS)

    print("\n===== STREAM SUMMARY =====")
    print(f"Sent successfully: {sent}")
    print(f"Failed: {failed}")
    print("Finished cleanly.")


if __name__ == "__main__":
    main()
