import json
import os

import mlflow
import numpy as np
import pandas as pd

from src.train import train


FEATURE_NAMES = [
    "age", "workclass", "education_num", "marital_status", "occupation",
    "relationship", "sex", "capital_gain", "capital_loss", "hours_per_week",
]


def _make_temp_data(tmp_path, monkeypatch):
    """Tao dataset nho co cung schema voi Adult cho cac unit test."""
    monkeypatch.chdir(tmp_path)
    mlflow.set_tracking_uri(f"sqlite:///{(tmp_path / 'mlflow.db').as_posix()}")
    rng = np.random.default_rng(0)
    n = 200
    X = rng.random((n, len(FEATURE_NAMES)))
    y = rng.integers(0, 2, size=n)

    df = pd.DataFrame(X, columns=FEATURE_NAMES)
    df["target"] = y

    train_path = str(tmp_path / "train.csv")
    eval_path = str(tmp_path / "holdout.csv")
    df.iloc[:160].to_csv(train_path, index=False)
    df.iloc[160:].to_csv(eval_path, index=False)
    return train_path, eval_path


def test_train_returns_float(tmp_path, monkeypatch):
    train_path, eval_path = _make_temp_data(tmp_path, monkeypatch)
    f1 = train(
        {"n_estimators": 10, "learning_rate": 0.1, "max_depth": 2},
        data_path=train_path,
        eval_path=eval_path,
    )

    assert isinstance(f1, float)
    assert 0.0 <= f1 <= 1.0


def test_report_file_created(tmp_path, monkeypatch):
    train_path, eval_path = _make_temp_data(tmp_path, monkeypatch)
    train(
        {"n_estimators": 10, "learning_rate": 0.1, "max_depth": 2},
        data_path=train_path,
        eval_path=eval_path,
    )

    assert os.path.exists("outputs/report.json")
    with open("outputs/report.json") as f:
        report = json.load(f)
    assert {
        "f1_score",
        "accuracy",
        "f1_score_default_0_5",
        "best_threshold",
        "positive_ratio",
        "data_drift_warning",
    } <= report.keys()
    assert 0.1 <= report["best_threshold"] <= 0.9
    assert os.path.exists("outputs/detail.txt")


def test_model_file_created(tmp_path, monkeypatch):
    train_path, eval_path = _make_temp_data(tmp_path, monkeypatch)
    train(
        {"n_estimators": 10, "learning_rate": 0.1, "max_depth": 2},
        data_path=train_path,
        eval_path=eval_path,
    )

    assert os.path.exists("models/model.joblib")
