"""
Flask application factory module.

References Tech Spec §5.2.1 (Flask Backend API) — this module implements the
application factory pattern, which is the recommended approach for creating
testable, configurable Flask applications. The create_app() function serves
as the central orchestration point for the entire application:

1. Loads environment-specific configuration from app.config via get_config()
2. Registers the health_bp Blueprint for /health and /ready probe endpoints
3. Registers the api_bp Blueprint for /api/v1/* REST API gateway endpoints
4. Attaches centralized JSON error handlers via register_error_handlers()
5. Defines the root route '/' returning API metadata

The wsgi.py entry point and all test modules call create_app() to obtain
a configured Flask application instance.
"""

from flask import Flask, jsonify

from app.config import get_config
from app.routes.health import health_bp
from app.routes.api import api_bp
from app.middleware.error_handler import register_error_handlers


def create_app(config_name='default') -> Flask:
    """Create and configure a Flask application instance.

    Implements the application factory pattern: each call produces a fresh,
    independently configured Flask app. This enables running multiple app
    instances with different configurations (e.g., testing vs. production)
    within the same process.

    Args:
        config_name: Configuration profile name. One of 'development',
            'testing', 'production', or 'default'. Defaults to 'default',
            which maps to DevelopmentConfig.

    Returns:
        A fully configured Flask application instance with blueprints
        registered and error handlers attached.
    """
    app = Flask(__name__)

    # Load environment-specific configuration
    app.config.from_object(get_config(config_name))

    # Register blueprints without url_prefix so endpoints are at root level
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp)

    # Attach centralized JSON error handlers for HTTPException and Exception
    register_error_handlers(app)

    @app.route('/')
    def root():
        """Root route returning API metadata.

        Provides a discovery endpoint confirming the API is running and
        reporting its version.
        """
        return jsonify({
            'message': 'Flask API',
            'version': '1.0.0'
        })

    return app
