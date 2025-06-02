import pytest
import sys
import os

# Add the parent directory (app) to sys.path to allow direct import of main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now try to import the app
try:
    from main import app as flask_app
except ImportError as e:
    flask_app = None
    print(f"Error importing flask_app from main: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Current working directory: {os.getcwd()}")

@pytest.fixture
def client():
    if flask_app is None:
        pytest.fail("Flask app could not be imported. Check test setup and PYTHONPATH.")
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page basic response."""
    response = client.get('/')
    # Check for general success or graceful Redis not connected message
    assert response.status_code == 200 or response.status_code == 500 
    if response.status_code == 200:
        assert b"Hello from the Web App!" in response.data
    else: # 500
        assert b"Redis is not connected" in response.data or b"Could not connect to Redis" in response.data

def test_health_check(client):
    """Test the health check endpoint basic response."""
    response = client.get('/health')
    assert response.status_code == 200 or response.status_code == 503
    if response.status_code == 200:
        assert b"Web app is healthy and connected to Redis" in response.data
    else: # 503
        assert b"Redis is not configured/connected" in response.data or b"Redis connection failed" in response.data 