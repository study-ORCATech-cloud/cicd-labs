import pytest
import sys
import os

# Add the parent directory (api_service) to sys.path to allow direct import of app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app # Renamed to flask_app to avoid conflict

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Welcome to the API Service!"
    assert "service_id" in json_data

def test_data_endpoint(client):
    """Test the /data endpoint."""
    response = client.get('/data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["source"] == "API Service"
    assert isinstance(json_data["data"], list)
    assert len(json_data["data"]) == 2
    assert json_data["data"][0]["name"] == "Item 1"

def test_health_check_endpoint(client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert json_data["service"] == "API Service" 