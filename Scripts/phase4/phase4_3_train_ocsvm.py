import pandas as pd
from sklearn.svm import OneClassSVM
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
import joblib
import os

BASE_DIR = "data/processed/baseline"
SPLIT_DIR = "data/processed/splits"
MODEL_DIR = "data/models"

os.makedirs(MODEL_DIR, exist_ok=True)


def train_and_test(prefix):

    print(f"\n===== One-Class SVM ({prefix}) =====")

    X_train = pd.read_parquet(
        f"{BASE_DIR}/{prefix}_baseline_features.parquet"
    )

    test_df = pd.read_parquet(
        f"{SPLIT_DIR}/{prefix}_test.parquet"
    )

    y_test = test_df["label"]
    X_test = test_df.drop(columns=["timestamp", "src_ip", "label"])

    # OCSVM model (RBF kernel works best generally)
    clf = OneClassSVM(
        kernel="rbf",
        gamma="scale",
        nu=0.01   # similar contamination assumption
    )

    print("[*] Training model...")
    clf.fit(X_train)

    model_path = f"{MODEL_DIR}/ocsvm_{prefix}.joblib"
    joblib.dump(clf, model_path)
    print("[✓] Saved model:", model_path)

    # OCSVM: higher negative = anomaly so invert sign
    scores = -clf.decision_function(X_test)

    roc = roc_auc_score(y_test, scores)

    precision, recall, _ = precision_recall_curve(y_test, scores)
    pr_auc = auc(recall, precision)

    print(f"[✓] ROC-AUC ({prefix}): {roc:.4f}")
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
