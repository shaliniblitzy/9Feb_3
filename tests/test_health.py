"""
Unit tests for the health check blueprint endpoints.

Tests the /health (liveness) and /ready (readiness) probe endpoints defined
in app/routes/health.py per Tech Spec §5.2.6 (Infrastructure). These endpoints
are critical for container orchestration platforms to determine service health.

Test coverage:
- GET /health returns 200 with JSON containing status="healthy" and service="9Feb_3"
- GET /ready returns 200 with JSON containing status="ready" and service="9Feb_3"
- DELETE /health returns 405 Method Not Allowed as structured JSON
"""

import pytest

from app import create_app


@pytest.fixture
def app():
    """Create a Flask application instance configured for testing."""
    application = create_app('testing')
    return application


@pytest.fixture
def client(app):
    """Create a Flask test client for making HTTP requests."""
    return app.test_client()


def test_health_endpoint_returns_200(client):
    """GET /health returns HTTP 200 status code."""
    response = client.get('/health')
    assert response.status_code == 200


def test_health_endpoint_returns_json(client):
    """GET /health returns Content-Type: application/json."""
    response = client.get('/health')
    assert response.content_type == 'application/json'


def test_health_endpoint_contains_status(client):
    """GET /health response JSON has 'status' key with value 'healthy'."""
    response = client.get('/health')
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_health_endpoint_contains_service(client):
    """GET /health response JSON has 'service' key with value '9Feb_3'."""
    response = client.get('/health')
    data = response.get_json()
    assert data['service'] == '9Feb_3'


def test_ready_endpoint_returns_200(client):
    """GET /ready returns HTTP 200 status code."""
    response = client.get('/ready')
    assert response.status_code == 200


def test_ready_endpoint_returns_json(client):
    """GET /ready returns Content-Type: application/json."""
    response = client.get('/ready')
    assert response.content_type == 'application/json'


def test_ready_endpoint_contains_status(client):
    """GET /ready response JSON has 'status' key with value 'ready'."""
    response = client.get('/ready')
    data = response.get_json()
    assert data['status'] == 'ready'


def test_ready_endpoint_contains_service(client):
    """GET /ready response JSON has 'service' key with value '9Feb_3'."""
    response = client.get('/ready')
    data = response.get_json()
    assert data['service'] == '9Feb_3'


def test_health_endpoint_method_not_allowed(client):
    """DELETE /health returns 405 Method Not Allowed with structured JSON."""
    response = client.delete('/health')
    assert response.status_code == 405
    data = response.get_json()
    assert data['error'] == 'Method Not Allowed'
