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
    # Point to a test-specific Redis or mock for unit tests if Redis interactions were complex.
    # For this lab, we assume a real Redis might be available via Docker Compose for integration-style tests,
    # or tests are designed to handle its absence.
    # flask_app.config['REDIS_HOST'] = os.environ.get('REDIS_HOST_TEST', 'localhost') # Example for test-specific Redis
    with flask_app.test_client() as client:
        yield client

def test_home_page_dev_mode(client):
    """Test the home page indicates dev mode."""
    response = client.get('/')
    # Check for general success or graceful Redis not connected message for basic test
    assert response.status_code == 200 or response.status_code == 500
    assert b"(Dev Mode)" in response.data

def test_health_check_dev_mode(client):
    """Test the health check endpoint indicates dev mode."""
    response = client.get('/health')
    assert response.status_code == 200 or response.status_code == 503
    assert b"(Dev Mode)" in response.data

# Note: If your app absolutely requires Redis to be up for most tests,
# you'd make sure your test environment (e.g., a separate docker-compose.test.yml or instructions)
# guarantees a Redis service is available and configured for the tests.
# These tests are simple and will pass if Flask is running and dev mode text is present. 