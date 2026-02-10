"""
Unit tests for the core API blueprint endpoints.

Tests the /api/v1/status (GET) and /api/v1/echo (POST) endpoints defined
in app/routes/api.py per Tech Spec §5.2.1 (Request Processing Pipeline).

Test coverage:
- GET /api/v1/status returns 200 with JSON containing status, service, version
- POST /api/v1/echo with valid JSON returns 200 with echoed data
- POST /api/v1/echo with non-JSON content type returns 400
- POST /api/v1/echo with empty body returns 400
- POST /api/v1/echo with malformed JSON returns 400
- POST /api/v1/status returns 405 Method Not Allowed
GET /api/v1/status returns 200 with JSON containing status, service, version
"""

import json

import pytest

from app import create_app


@pytest.fixture
def app():
    """Create a Flask application instance configured for testing."""
    application = create_app('testing')
    return application
GET /api/v1/status returns 200 with JSON containing status, service, version

@pytest.fixture
def client(app):
    """Create a Flask test client for making HTTP requests."""
    return app.test_client()


def test_status_endpoint_returns_200(client):
    """GET /api/v1/status returns HTTP 200 status code."""
    response = client.get('/api/v1/status')
    assert response.status_code == 200


def test_status_endpoint_returns_json(client):
    """GET /api/v1/status returns Content-Type: application/json."""
    response = client.get('/api/v1/status')
    assert response.content_type == 'application/json'


def test_status_endpoint_contains_status(client):
    """GET /api/v1/status response has 'status' key with value 'operational'."""
    response = client.get('/api/v1/status')
    data = response.get_json()
    assert data['status'] == 'operational'


def test_status_endpoint_contains_service(client):
    """GET /api/v1/status response has 'service' key with value '9Feb_3'."""
    response = client.get('/api/v1/status')
    data = response.get_json()
    assert data['service'] == '9Feb_3'


def test_status_endpoint_contains_version(client):
    """GET /api/v1/status response has 'version' key with value '1.0.0'."""
    response = client.get('/api/v1/status')
    data = response.get_json()
    assert data['version'] == '1.0.0'


def test_echo_endpoint_returns_200_with_valid_json(client):
    """POST /api/v1/echo with valid JSON returns HTTP 200."""
    response = client.post(
        '/api/v1/echo',
        data=json.dumps({'message': 'hello'}),
        content_type='application/json'
    )
    assert response.status_code == 200


def test_echo_endpoint_echoes_correct_data(client):
    """POST /api/v1/echo echoes the posted JSON data back."""
    payload = {'message': 'hello'}
    response = client.post(
        '/api/v1/echo',
        data=json.dumps(payload),
        content_type='application/json'
    )
    data = response.get_json()
    assert data['echo'] == payload
    assert data['status'] == 'success'


def test_echo_endpoint_returns_400_for_non_json(client):
    """POST /api/v1/echo with non-JSON content type returns HTTP 400."""
    response = client.post(
        '/api/v1/echo',
        data='plain text data',
        content_type='text/plain'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['status'] == 'error'


def test_echo_endpoint_returns_400_for_empty_body(client):
    """POST /api/v1/echo with empty JSON body returns HTTP 400."""
    response = client.post(
        '/api/v1/echo',
        data='',
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'


def test_echo_endpoint_returns_400_for_invalid_json(client):
    """POST /api/v1/echo with malformed JSON returns HTTP 400."""
    response = client.post(
        '/api/v1/echo',
        data='{invalid json',
        content_type='application/json'
    )
    assert response.status_code == 400


def test_status_endpoint_method_not_allowed(client):
    """POST /api/v1/status returns 405 (only GET is allowed)."""
    response = client.post('/api/v1/status')
    assert response.status_code == 405
