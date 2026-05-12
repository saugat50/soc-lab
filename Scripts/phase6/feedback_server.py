from flask import Flask, request, jsonify
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

OUTPUT_PATH = "data/processed/feedback/analyst_feedback.csv"

os.makedirs("data/processed/feedback", exist_ok=True)

def append_feedback(record):
    df = pd.DataFrame([record])

    if os.path.exists(OUTPUT_PATH):
        df.to_csv(OUTPUT_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(OUTPUT_PATH, index=False)

@app.route("/feedback", methods=["POST"])
def receive_feedback():
    data = request.json

    record = {
        "timestamp": data.get("timestamp"),
        "entity": data.get("entity"),
        "severity": data.get("severity"),
        "anomaly_score": data.get("anomaly_score"),
        "analyst_label": data.get("analyst_label"),
        "logged_at": datetime.utcnow().isoformat()
    }

    append_feedback(record)

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
