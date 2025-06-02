import pytest
import sys
import os

# Add the parent directory (app) to sys.path to allow direct import of main
# This assumes tests are run from the 'app' directory or this path is adjusted accordingly.
# For Docker Compose execution, WORKDIR in Dockerfile and compose service definition is key.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now try to import the app
try:
    from main import app as flask_app # Renaming to avoid conflict with pytest 'app' fixture if used
except ImportError as e:
    # Provide a more informative error if main cannot be imported
    # This often happens if PYTHONPATH is not set up correctly for the test environment
    # or if the test runner is in a different relative location than expected.
    flask_app = None
    print(f"Error importing flask_app from main: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Current working directory: {os.getcwd()}")

@pytest.fixture
def client():
    if flask_app is None:
        pytest.fail("Flask app could not be imported. Check test setup and PYTHONPATH.")
    flask_app.config['TESTING'] = True
    # For tests, we don't want to actually connect to an external Redis by default
    # We'd typically mock it. For this lab, we'll assume Redis might not be available
    # during unit tests and check for graceful handling.
    flask_app.config['REDIS_HOST'] = 'nonexistent.redis.host.for.testing' # Force connection error for some tests
    with flask_app.test_client() as client:
        yield client

def test_home_page_no_redis(client):
    """Test the home page when Redis is not available or connection fails."""
    # Simulate Redis being unavailable. The app should handle this.
    # In a real unit test, we'd mock the redis client in main.py
    response = client.get('/')
    assert response.status_code == 500
    assert b"Redis is not connected" in response.data or b"Could not connect to Redis" in response.data

def test_health_check_no_redis(client):
    """Test the health check endpoint when Redis is not available."""
    response = client.get('/health')
    assert response.status_code == 503
    assert b"Redis is not configured/connected" in response.data or b"Redis connection failed" in response.data

# To test with a live Redis, you would need to:
# 1. Ensure Redis is running and accessible during the test execution.
# 2. Configure main.app to point to this Redis instance (e.g., via environment variables).
# 3. Modify the tests or add new ones that expect successful Redis interaction.
# For this lab, focusing on CI with Docker Compose, the main Redis interaction tests
# will be implicitly covered when the services are run together. 