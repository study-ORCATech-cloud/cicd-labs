import pytest
import sys
import os

# Add the parent directory (app) to sys.path to allow direct import of main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock the API_KEY_FILE_PATH and DATA_FILE_PATH for testing
# to avoid actual file system operations in unit tests for these
os.environ['API_KEY_FILE'] = '/tmp/fake_api_key.txt'
os.environ['DATA_FILE'] = '/tmp/fake_app_counter.txt'

# Clean up any fake files that might exist from previous test runs
if os.path.exists(os.environ['API_KEY_FILE']):
    os.remove(os.environ['API_KEY_FILE'])
if os.path.exists(os.environ['DATA_FILE']):
    os.remove(os.environ['DATA_FILE'])


# Now try to import the app
try:
    from main import app as flask_app
    # Reset app counter file before each test suite run if it somehow got created
    if os.path.exists(os.environ['DATA_FILE']):
        os.remove(os.environ['DATA_FILE'])

except ImportError as e:
    flask_app = None
    print(f"Error importing flask_app from main: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Current working directory: {os.getcwd()}")


@pytest.fixture
def client():
    if flask_app is None:
        pytest.fail("Flask app could not be imported. Check test setup and PYTHONPATH.")
    
    # Reset app counter file before each test
    if os.path.exists(os.environ['DATA_FILE']):
        os.remove(os.environ['DATA_FILE'])

    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_page_new_visit(client):
    """Test the home page on a new visit."""
    response = client.get('/')
    # Check for general success or graceful Redis not connected message
    assert response.status_code == 200

    # API Key (will be default as file doesn't exist in test)
    assert b'API Key: "default_api_key_not_set"' in response.data
    
    # App counter (should be 1 on first visit)
    assert b'app endpoint has been visited 1 times' in response.data
    assert bytes(os.environ['DATA_FILE'], 'utf-8') in response.data

    # Redis status (depends on actual Redis connection, can be connected or not)
    if b"Redis is not connected" in response.data or b"Could not connect to Redis" in response.data:
        # This is okay if Redis isn't running for the test
        pass
    else:
        assert b"Redis counter" in response.data


def test_home_page_multiple_visits(client):
    """Test the home page counter increments across multiple visits."""
    response1 = client.get('/')
    assert response1.status_code == 200
    assert b'app endpoint has been visited 1 times' in response1.data

    response2 = client.get('/')
    assert response2.status_code == 200
    assert b'app endpoint has been visited 2 times' in response2.data
    
    response3 = client.get('/')
    assert response3.status_code == 200
    assert b'app endpoint has been visited 3 times' in response3.data
    
    # Check that the API key remains the default
    assert b'API Key: "default_api_key_not_set"' in response3.data


def test_health_check_no_api_key_file(client):
    """Test the health check endpoint when API key file is not present."""
    response = client.get('/health')
    assert response.status_code == 200
    assert b"API key file NOT found (using default)" in response.data
    
    # Check for Redis status message (either connected or not)
    assert b"Redis Status:" in response.data


def test_health_check_with_mock_api_key_file(client):
    """Test the health check endpoint when API key file IS present (mocked)."""
    # Create a mock API key file
    mock_api_key_path = os.environ['API_KEY_FILE']
    with open(mock_api_key_path, 'w') as f:
        f.write("test_key_from_file_123")
    
    response = client.get('/health')
    assert response.status_code == 200
    assert b"API key file found." in response.data
    
    # Clean up the mock file
    os.remove(mock_api_key_path)

    # Test home page to see if it picks up the key from the mocked file path
    # For this to work, the app needs to re-read the API_KEY_FILE_PATH env var
    # OR we need to ensure the test client doesn't cache the app instance too aggressively
    # For simplicity, this test focuses on /health; main app path might need app restart/reconfig for key change
    # However, the main.py reads the file on each request to '/', so it should work.
    
    # Create the mock API key file again for the home page test
    with open(mock_api_key_path, 'w') as f:
        f.write("test_key_from_file_for_home_page")

    home_response = client.get('/')
    assert home_response.status_code == 200
    assert b'API Key: "test_key_from_file_for_home_page"' in home_response.data

    # Clean up the mock file again
    os.remove(mock_api_key_path)


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