"""Frontend integration tests."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_plan_trip_endpoint():
    """Test travel planning endpoint."""
    request_data = {"query": "I want to relax at a beach"}
    response = client.post("/api/plan-trip", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "recommended_destination" in data
    assert "travel_style" in data
    assert "explanation" in data
    assert "weather_summary" in data
