import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory (web_frontend_service) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    # Set a mock API URL for tests to avoid real network calls
    flask_app.config['API_SERVICE_URL'] = "http://mock-api-service:1234"
    # Alternative way if app re-reads os.environ directly:
    # with patch.dict(os.environ, {"API_SERVICE_URL": "http://mock-api-service:1234"}):
    #     with flask_app.test_client() as client:
    #         yield client
    with flask_app.test_client() as client:
        yield client

@patch('requests.get')
def test_home_page_api_success(mock_get, client):
    """Test the home page when API call is successful."""
    # Configure the mock API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Mock Item"}], "source": "Mock API"}
    mock_get.return_value = mock_response

    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Web Frontend Service!" in response.data
    assert b"Data from API Service" in response.data
    assert b"Mock Item" in response.data
    assert b"Successfully fetched data" in response.data
    mock_get.assert_called_once_with(f"{flask_app.config['API_SERVICE_URL']}/data", timeout=5)

@patch('requests.get')
def test_home_page_api_failure(mock_get, client):
    """Test the home page when API call fails."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response

    response = client.get('/')
    assert response.status_code == 200 # Page itself should load
    assert b"Error fetching data. API returned HTTP 500" in response.data
    mock_get.assert_called_once_with(f"{flask_app.config['API_SERVICE_URL']}/data", timeout=5)

@patch('requests.get')
def test_home_page_api_connection_error(mock_get, client):
    """Test the home page when API is unreachable."""
    mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")

    response = client.get('/')
    assert response.status_code == 200 # Page itself should load
    assert b"Error connecting to API service: Failed to connect" in response.data
    mock_get.assert_called_once_with(f"{flask_app.config['API_SERVICE_URL']}/data", timeout=5)

@patch('requests.get')
def test_health_check_dependencies_healthy(mock_get, client):
    """Test the /health endpoint when API dependency is healthy."""
    mock_api_health_response = MagicMock()
    mock_api_health_response.status_code = 200
    mock_get.return_value = mock_api_health_response

    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert json_data["service"] == "Web Frontend"
    assert json_data["dependencies"]["api_service"] == "healthy"
    mock_get.assert_called_once_with(f"{flask_app.config['API_SERVICE_URL']}/health", timeout=2)

@patch('requests.get')
def test_health_check_dependencies_unhealthy(mock_get, client):
    """Test the /health endpoint when API dependency is unhealthy."""
    mock_api_health_response = MagicMock()
    mock_api_health_response.status_code = 503
    mock_get.return_value = mock_api_health_response

    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["dependencies"]["api_service"] == "unhealthy (HTTP 503)"

@patch('requests.get')
def test_health_check_dependencies_unreachable(mock_get, client):
    """Test the /health endpoint when API dependency is unreachable."""
    mock_get.side_effect = requests.exceptions.RequestException("Cannot connect")

    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["dependencies"]["api_service"] == "unreachable" 