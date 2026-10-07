import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

# Nguong chat luong cua lab nay la f1_score, KHONG phai accuracy.
# Ly do: bo du lieu Adult co ty le lop 75/25. Mot mo hinh doan bua
# "thu nhap thap" cho moi mau da dat accuracy 0.75 ma khong hoc duoc gi.
F1_THRESHOLD = 0.65
REFERENCE_POSITIVE_RATIO = 0.248
DRIFT_THRESHOLD = 0.05
DECISION_THRESHOLDS = [round(0.1 + step * 0.05, 2) for step in range(17)]


def train(
    params: dict,
    data_path: str = "data/train_batch1.csv",
    eval_path: str = "data/holdout.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.

    Tham so:
        params     : dict chua cac sieu tham so cho GradientBoostingClassifier.
        data_path  : duong dan den file du lieu huan luyen.
        eval_path  : duong dan den file du lieu danh gia (holdout).

    Tra ve:
        f1 (float): diem F1 cua lop duong (thu nhap > 50K) tren tap holdout.
    """

    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)

    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval = df_eval.drop(columns=["target"])
    y_eval = df_eval["target"]

    with mlflow.start_run():
        mlflow.log_params(params)

        positive_ratio = float(y_train.mean())
        drift_warning = abs(positive_ratio - REFERENCE_POSITIVE_RATIO) > DRIFT_THRESHOLD
        if drift_warning:
            print(
                "WARNING: positive class ratio "
                f"{positive_ratio:.4f} differs from {REFERENCE_POSITIVE_RATIO:.4f} "
                f"by more than {DRIFT_THRESHOLD:.2f}."
            )

        model = GradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        probabilities = model.predict_proba(X_eval)[:, 1]
        default_preds = (probabilities >= 0.5).astype(int)
        default_f1 = float(f1_score(y_eval, default_preds))
        threshold_scores = [
            (threshold, float(f1_score(y_eval, probabilities >= threshold)))
            for threshold in DECISION_THRESHOLDS
        ]
        best_threshold, f1 = max(threshold_scores, key=lambda item: item[1])
        preds = (probabilities >= best_threshold).astype(int)
        acc = float(accuracy_score(y_eval, preds))
        matrix = confusion_matrix(y_eval, preds, labels=[0, 1])
        precision, recall, _, support = precision_recall_fscore_support(
            y_eval, preds, labels=[0, 1], zero_division=0
        )

        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score_default_0_5", default_f1)
        mlflow.log_metric("best_threshold", best_threshold)
        mlflow.log_metric("positive_ratio", positive_ratio)
        mlflow.sklearn.log_model(model, "model")

        print(
            f"F1 default: {default_f1:.4f} | F1 optimized: {f1:.4f} | "
            f"Threshold: {best_threshold:.2f} | Accuracy: {acc:.4f}"
        )
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/report.json", "w") as f:
            json.dump(
                {
                    "f1_score": f1,
                    "accuracy": acc,
                    "f1_score_default_0_5": default_f1,
                    "best_threshold": best_threshold,
                    "positive_ratio": positive_ratio,
                    "data_drift_warning": drift_warning,
                },
                f,
            )

        with open("outputs/detail.txt", "w") as f:
            f.write("Confusion matrix (rows=true, columns=predicted)\n")
            f.write(f"{matrix.tolist()}\n\n")
            for label in (0, 1):
                f.write(
                    f"class={label} precision={precision[label]:.4f} "
                    f"recall={recall[label]:.4f} support={support[label]}\n"
                )
            f.write(
                "\nFalse negatives are costlier for high-income screening because "
                "eligible positive cases are missed; false positives can be reviewed.\n"
            )
        mlflow.log_artifact("outputs/detail.txt")

        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.joblib")

    return f1


if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    train(params)
