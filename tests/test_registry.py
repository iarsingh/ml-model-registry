from fastapi.testclient import TestClient
from registry.main import app
from registry import registry

client = TestClient(app)


def setup_function():
    registry.CHAMPION = next(iter(registry.MODELS))


def test_promote():
    client.post("/models", json={"name": "churn-v2", "version": "2", "metrics": {"auc": 0.9}})
    payload = client.post("/promote", json={"name": "churn-v2"}).json()
    assert payload["champion"] == "churn-v2"
    assert payload["applied"] is False
    assert client.get("/champion").json()["champion"] == "churn-v2"
