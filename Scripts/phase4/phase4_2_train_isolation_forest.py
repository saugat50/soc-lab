import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
import joblib
import os

BASE_DIR = "data/processed/baseline"
SPLIT_DIR = "data/processed/splits"
MODEL_DIR = "data/models"

os.makedirs(MODEL_DIR, exist_ok=True)


def train_and_test(prefix):

    print(f"\n===== Isolation Forest ({prefix}) =====")

    # Load baseline training features
    X_train = pd.read_parquet(
        f"{BASE_DIR}/{prefix}_baseline_features.parquet"
    )

    # Load full test set (with labels)
    test_df = pd.read_parquet(
        f"{SPLIT_DIR}/{prefix}_test.parquet"
    )

    y_test = test_df["label"]
    X_test = test_df.drop(columns=["timestamp", "src_ip", "label"])

    # Model
    clf = IsolationForest(
        n_estimators=300,
        max_samples="auto",
        contamination=0.01,   # realistic SOC assumption
        random_state=42,
        n_jobs=-1
    )

    print("[*] Training model...")
    clf.fit(X_train)

    # Save model
    model_path = f"{MODEL_DIR}/if_{prefix}.joblib"
    joblib.dump(clf, model_path)
    print("[✓] Saved model:", model_path)

    # Score (higher = more normal, so invert)
    scores = -clf.decision_function(X_test)

    # ROC-AUC
    roc = roc_auc_score(y_test, scores)

    print(f"[✓] ROC-AUC ({prefix}): {roc:.4f}")

    # PR-AUC (better for imbalance)
    precision, recall, _ = precision_recall_curve(y_test, scores)
    pr_auc = auc(recall, precision)

    print(f"[✓] PR-AUC ({prefix}): {pr_auc:.4f}")

    return roc, pr_auc


def main():

    roc5, pr5 = train_and_test("5min")
    roc30, pr30 = train_and_test("30min")

    print("\n===== SUMMARY =====")
    print(f"5min  ROC-AUC: {roc5:.4f} | PR-AUC: {pr5:.4f}")
    print(f"30min ROC-AUC: {roc30:.4f} | PR-AUC: {pr30:.4f}")


if __name__ == "__main__":
    main()
