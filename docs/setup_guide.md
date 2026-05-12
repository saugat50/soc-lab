# Setup Guide

This document explains how to install and run the Semi-Autonomous SIEM–SOAR Framework.

---

# System Requirements

## Hardware
- Minimum 8 GB RAM recommended
- Multi-core processor preferred
- 20+ GB free storage

## Operating System
- Ubuntu 20.04+ (recommended)
- Windows 10/11
- macOS

---

# Software Requirements

| Component | Version |
|---|---|
| Python | 3.10+ |
| Docker | Latest |
| Elasticsearch | 7.17+ |
| Kibana | 7.17+ |
| Shuffle SOAR | Latest |

---

# Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/soc-lab.git

cd soc-lab
```

---

# Create Python Virtual Environment

## Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

## Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Docker Setup

Verify Docker installation:

```bash
docker --version
```

Verify Docker Compose:

```bash
docker compose version
```

---

# Elasticsearch Setup

Start Elasticsearch:

```bash
sudo systemctl start elasticsearch
```

Verify service:

```bash
curl http://localhost:9200
```

Expected response:

```json
{
  "name": "elasticsearch",
  "cluster_name": "elasticsearch"
}
```

---

# Kibana Setup

Start Kibana:

```bash
sudo systemctl start kibana
```

Open browser:

```text
http://localhost:5601
```

---

# Shuffle SOAR Setup

Run Shuffle containers:

```bash
docker compose up -d
```

Verify containers:

```bash
docker ps
```

---

# Detection Pipeline Execution

## Step 1 — Window Aggregation

```bash
python3 Scripts/phase3/phase3_4_window_aggregation.py
```

---

## Step 2 — Train Isolation Forest

```bash
python3 Scripts/phase4/phase4_2_train_isolation_forest.py
```

---

## Step 3 — Score Behavioral Windows

```bash
python3 Scripts/phase5/phase5_1_score_windows.py
```

---

## Step 4 — Build Alert Objects

```bash
python3 Scripts/phase5/phase5_2_build_alert_objects.py
```

---

## Step 5 — Apply Triage

```bash
python3 Scripts/phase5/phase5_4_triage.py
```

---

## Step 6 — Push Alerts to Elasticsearch

```bash
python3 Scripts/phase5/phase5_6_push_to_elasticsearch.py
```

---

# Human Feedback Channel

Start analyst feedback server:

```bash
python3 Scripts/phase6/feedback_server.py
```

---

# Evaluation Pipeline

Run evaluation:

```bash
python3 Scripts/phase7/phase7_1_evaluate_models.py
```

---

# Offline Retraining Pipeline

```bash
python3 Scripts/phase8/phase8_1_prepare_retraining_data.py

python3 Scripts/phase8/phase8_2_update_baseline.py

python3 Scripts/phase8/phase8_3_retrain_iforest.py
```

---

# Verify Elasticsearch Alerts

```bash
curl "http://localhost:9200/soc-alerts/_search?size=1&pretty"
```

---

# Common Issues

## Elasticsearch Not Starting

Check status:

```bash
systemctl status elasticsearch
```

---

## Kibana Unreachable

Verify Kibana process:

```bash
systemctl status kibana
```

---

## Python Dependency Errors

Upgrade pip:

```bash
pip install --upgrade pip
```

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

# Notes

- This project is a research prototype.
- Generated datasets and trained models are excluded from the repository.
- Users may regenerate outputs by running the pipeline scripts.