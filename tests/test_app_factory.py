"""
Unit tests for the Flask application factory, configuration profiles,
blueprint registration, and centralized error handling.

Tests the create_app() function from app/__init__.py and the configuration
system from app/config/__init__.py per Tech Spec §5.2.1.

Test coverage:
- Factory creates valid Flask instances with all configuration profiles
- get_config() resolves correct classes and raises KeyError on invalid names
- Blueprints ('health', 'api') are registered on the application
- Root route '/' returns API metadata
- 404 and 405 errors return structured JSON responses
"""

import pytest
from flask import Flask

from app import create_app
from app.config import get_config, DevelopmentConfig, TestingConfig, ProductionConfig


def test_create_app_returns_flask_instance():
    """create_app() returns a Flask application instance."""
    app = create_app('testing')
    assert isinstance(app, Flask)


def test_create_app_default_config():
    """create_app() with no arguments uses default (DevelopmentConfig)."""
    app = create_app()
    assert app.config['DEBUG'] is True


def test_create_app_testing_config():
    """create_app('testing') correctly applies TestingConfig."""
    app = create_app('testing')
    assert app.config['TESTING'] is True


def test_create_app_development_config():
    """create_app('development') correctly applies DevelopmentConfig."""
    app = create_app('development')
    assert app.config['DEBUG'] is True


def test_create_app_production_config():
    """create_app('production') correctly applies ProductionConfig."""
    app = create_app('production')
    assert app.config['DEBUG'] is False
    assert app.config['TESTING'] is False


def test_get_config_returns_correct_class():
    """get_config() returns the correct configuration class for each profile."""
    assert get_config('testing') is TestingConfig
    assert get_config('development') is DevelopmentConfig
    assert get_config('production') is ProductionConfig


def test_get_config_invalid_name_raises_error():
    """get_config('nonexistent') raises KeyError with descriptive message."""
    with pytest.raises(KeyError) as exc_info:
        get_config('nonexistent')
    error_msg = str(exc_info.value)
    assert 'nonexistent' in error_msg
    # Verify the error message lists valid configuration names
    assert 'development' in error_msg
    assert 'testing' in error_msg
    assert 'production' in error_msg


def test_testing_config_properties():
    """TestingConfig has TESTING=True and DEBUG=True."""
    assert TestingConfig.TESTING is True
    assert TestingConfig.DEBUG is True


def test_blueprints_registered():
    """App has 'health' and 'api' blueprints registered."""
    app = create_app('testing')
    assert 'health' in app.blueprints
    assert 'api' in app.blueprints


def test_root_route_exists():
    """GET / returns 200 with JSON containing 'message' and 'version' keys."""
    app = create_app('testing')
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'version' in data


def test_404_returns_json():
    """GET /nonexistent returns 404 with structured JSON error response."""
    app = create_app('testing')
    client = app.test_client()
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Not Found'


def test_405_returns_json():
    """DELETE /health returns 405 with structured JSON error response."""
    app = create_app('testing')
    client = app.test_client()
    response = client.delete('/health')
    assert response.status_code == 405
    data = response.get_json()
    assert data['error'] == 'Method Not Allowed'
