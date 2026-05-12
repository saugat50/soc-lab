# Workflow Explanation

This document explains the end-to-end workflow of the Semi-Autonomous SIEM–SOAR Framework.

---

# Overview

The framework simulates a modern Security Operations Center (SOC) architecture integrating:

- Security telemetry ingestion
- Behavioral anomaly detection
- Alert triage
- SIEM visualization
- SOAR orchestration
- Human analyst feedback
- Offline retraining

The objective is to demonstrate how machine learning and security automation can support semi-autonomous SOC operations.

---

# End-to-End Workflow

```text
Security Logs
      ↓
Data Ingestion & Preprocessing
      ↓
Sliding Window Aggregation
      ↓
Isolation Forest Detection
      ↓
Alert Enrichment & Triage
      ↓
Elasticsearch + Kibana
      ↓
Shuffle SOAR
      ↓
Human Analyst Feedback
      ↓
Offline Retraining
```

---

# Phase 3 — Data Engineering & Preprocessing

## Objectives
- Normalize telemetry
- Prepare behavioral features
- Generate temporal windows

## Components

### Raw Log Ingestion
The system ingests:
- Network flow logs
- Authentication telemetry

### Schema Unification
Different log schemas are normalized into a unified structure.

### Sliding Window Aggregation
Behavioral features are generated using:
- 5-minute windows
- 30-minute windows

Features include:
- Flow count
- Total bytes
- Failed authentication attempts
- Unique destination IPs
- Session statistics

---

# Phase 4 — Machine Learning Detection

## Isolation Forest Training

The framework uses Isolation Forest for unsupervised anomaly detection.

### Training Process
- Baseline-only training
- Feature normalization
- Temporal train/test split

### Detection Goals
The model identifies:
- Unusual traffic behavior
- Authentication anomalies
- Suspicious entity activity

---

# Phase 5 — Alert Generation & Triage

## Anomaly Scoring

Behavioral windows are scored using the trained model.

Suspicious windows are converted into structured alert objects.

---

## Alert Object Generation

Alert objects contain:
- Timestamp
- Entity identifier
- Severity level
- Anomaly score
- Behavioral metrics

---

## Alert Enrichment

Additional contextual metadata is added:
- MITRE ATT&CK-style mapping
- IP classification
- Asset criticality

---

## Severity Triage

Alerts are classified into:
- Low
- Medium
- High severity

High-severity alerts may trigger SOAR workflows.

---

# SIEM Layer

## Elasticsearch Indexing

Alert objects are indexed into Elasticsearch.

Benefits:
- Searchability
- Centralized alert storage
- Historical investigation

---

## Kibana Visualization

Kibana dashboards provide:
- Alert monitoring
- Severity distribution
- Entity analysis
- Security investigations

---

# SOAR Layer

## Shuffle SOAR Integration

High-severity alerts are forwarded to Shuffle SOAR.

### Workflow Capabilities
- Alert notifications
- Webhook automation
- Case tracking
- Analyst approval workflows

The framework intentionally avoids destructive automated actions.

---

# Human-in-the-Loop Feedback

## Analyst Validation

Security analysts review generated alerts.

Feedback categories:
- True Positive (TP)
- False Positive (FP)

---

## Feedback Logging

Feedback data is stored for future retraining.

Benefits:
- Reduced false positives
- Adaptive detection improvement
- Better operational accuracy

---

# Offline Retraining Pipeline

## Retraining Objectives

The retraining pipeline updates the baseline model using analyst feedback.

### Workflow
1. Collect analyst labels
2. Prepare retraining dataset
3. Update baseline
4. Retrain Isolation Forest

---

# Security Research Perspective

This framework demonstrates:
- SIEM/SOAR integration
- Human-assisted anomaly detection
- Semi-autonomous SOC operations
- Practical security analytics pipelines

This project does not claim:
- Fully autonomous SOC operations
- Production-scale deployment
- Zero false positives