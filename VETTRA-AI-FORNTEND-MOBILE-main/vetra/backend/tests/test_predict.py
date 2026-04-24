import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_predict_endpoint_success():
    payload = {
        "animal_id": "COW-TEST",
        "milk_yield": 15.0,
        "feed_intake": "medium",
        "activity_level": "medium",
        "temperature": 39.0
    }
    response = client.post("/api/v1/predict/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "risk_level" in data
    assert "reasons" in data

def test_predict_endpoint_invalid_temp():
    payload = {
        "animal_id": "COW-TEST",
        "milk_yield": 15.0,
        "feed_intake": "medium",
        "activity_level": "medium",
        "temperature": 100.0 # Way out of range (35-42)
    }
    response = client.post("/api/v1/predict/", json=payload)
    assert response.status_code == 422 # Pydantic validation error
