import importlib
import sys

import boto3
import joblib
from fastapi.testclient import TestClient


class FakeModel:
    def predict(self, rows):
        return [int(rows[0][2] >= 10)]


class FakeS3:
    def download_file(self, bucket, key, path):
        return None


def test_api_endpoints(monkeypatch, tmp_path):
    monkeypatch.setenv("ARTIFACT_BUCKET", "test-bucket")
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setattr(boto3, "client", lambda service: FakeS3())
    monkeypatch.setattr(joblib, "load", lambda path: FakeModel())
    sys.modules.pop("src.serve", None)
    serve = importlib.import_module("src.serve")
    client = TestClient(serve.app)

    assert client.get("/healthz").json() == {"status": "ok"}
    assert client.post("/score", json={"features": [60, 2, 5, 2, 4, 0, 1, 0, 0, 45]}).json()["prediction"] == 0
    assert client.post("/score", json={"features": [28, 2, 14, 2, 11, 0, 1, 0, 0, 45]}).json()["prediction"] == 1
    assert client.post("/score", json={"features": [1]}).status_code == 400