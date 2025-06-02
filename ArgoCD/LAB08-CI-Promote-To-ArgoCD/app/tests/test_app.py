import pytest
import json
import sys
import os

# Add the parent directory to sys.path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Test the main hello endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'version' in data
    assert 'environment' in data
    assert 'timestamp' in data
    assert data['message'] == 'Hello from CI/CD GitOps Demo!'

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

def test_version_endpoint(client):
    """Test the version endpoint"""
    response = client.get('/version')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'version' in data
    assert 'build_date' in data
    assert 'git_commit' in data

def test_app_version_env_var(client, monkeypatch):
    """Test that APP_VERSION environment variable is used"""
    monkeypatch.setenv('APP_VERSION', 'v2.0.0')
    monkeypatch.setenv('ENVIRONMENT', 'test')
    
    response = client.get('/')
    data = json.loads(response.data)
    assert data['version'] == 'v2.0.0'
    assert data['environment'] == 'test' 