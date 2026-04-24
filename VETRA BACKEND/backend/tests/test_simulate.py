import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_simulate_endpoint_success():
    payload = {
        "animal_id": "COW-SIM",
        "modified_inputs": {
            "animal_id": "COW-SIM",
            "milk_yield": 20.0,
            "feed_intake": "high",
            "activity_level": "high",
            "temperature": 38.5
        }
    }
    response = client.post("/api/v1/simulate/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "delta" in data
    assert "risk_level_after" in data
    assert "improved_factors" in data
