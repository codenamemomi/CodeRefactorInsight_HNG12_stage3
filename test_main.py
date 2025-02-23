import pytest
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_tick_endpoint():
    # Mock the payload and test the /tick endpoint
    response = client.post("/tick", json={"channel_id": "test_channel", "return_url": "http://test.url", "settings": []})
    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}

def test_process_task():
    # Mock the necessary functions and test the background task
    # This will require mocking fetch_github_commits and run_pylint
    pass

def test_integration_json():
    # Test the /integration.json endpoint
    response = client.get("/integration.json")
    assert response.status_code == 200
    assert "app_name" in response.json()["data"]["descriptions"]
