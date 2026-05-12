import pandas as pd
import joblib
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

TEST_PATH = "data/processed/splits/5min_test.parquet"

MODEL_ORIG = "data/models/if_5min.joblib"
MODEL_RETRAINED = "data/models/if_5min_retrained.joblib"

# Tuned threshold from Phase 4.4
THRESHOLD = -0.162366

DROP_COLS = [
    "timestamp",
    "src_ip",
    "label",
    "is_anomaly"
]

def prepare_features(df):
    return df.drop(columns=[c for c in DROP_COLS if c in df.columns])

def evaluate(model, X, y_true, name):
    scores = model.decision_function(X)

    preds = (scores < THRESHOLD).astype(int)  # anomaly if below threshold

    precision = precision_score(y_true, preds)
    recall = recall_score(y_true, preds)
    f1 = f1_score(y_true, preds)
    roc = roc_auc_score(y_true, -scores)

    fp = ((preds == 1) & (y_true == 0)).sum()
    tn = ((preds == 0) & (y_true == 0)).sum()
    fpr = fp / (fp + tn)

    print(f"\n===== {name} =====")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-score  : {f1:.4f}")
    print(f"ROC-AUC   : {roc:.4f}")
    print(f"FPR       : {fpr:.4f}")

def main():
    print("[*] Loading test data...")
    df = pd.read_parquet(TEST_PATH)

    X = prepare_features(df)
    y = df["label"]

    print("[*] Feature columns used:")
    print(list(X.columns))

    model_orig = joblib.load(MODEL_ORIG)
    model_new = joblib.load(MODEL_RETRAINED)

    evaluate(model_orig, X, y, "Original Isolation Forest")
    evaluate(model_new, X, y, "Retrained Isolation Forest")

if __name__ == "__main__":
    main()
