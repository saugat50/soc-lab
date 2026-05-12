import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import roc_curve

MODEL_DIR = "data/models"
SPLIT_DIR = "data/processed/splits"


def tune(prefix):

    print(f"\n===== Threshold tuning ({prefix}) =====")

    # Load trained Isolation Forest
    model = joblib.load(f"{MODEL_DIR}/if_{prefix}.joblib")

    # Load test set
    df_test = pd.read_parquet(f"{SPLIT_DIR}/{prefix}_test.parquet")

    y = df_test["label"]
    X = df_test.drop(columns=["timestamp", "src_ip", "label"])

    # Anomaly scores (higher = more anomalous)
    scores = -model.decision_function(X)

    # ROC curve
    fpr, tpr, thresholds = roc_curve(y, scores)

    # SOC operational target
    target_fpr = 0.05   # 5% false positive rate

    idx = np.where(fpr <= target_fpr)[0]

    if len(idx) == 0:
        print("No threshold achieves FPR <= 5%")
        return

    best = idx[-1]

    print(f"Chosen threshold: {thresholds[best]:.6f}")
    print(f"False Positive Rate (FPR): {fpr[best]:.4f}")
    print(f"True Positive Rate (TPR / Recall): {tpr[best]:.4f}")


def main():

    tune("5min")
    tune("30min")


if __name__ == "__main__":
    main()
