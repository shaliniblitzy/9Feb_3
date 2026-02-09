"""
Centralized error handling module for the Flask application.

References Tech Spec §4.8 (Error Handling Flows) — this module ensures all
error responses are returned as structured JSON rather than the default HTML
error pages provided by Flask/Werkzeug. This is critical for API consumers
that parse JSON responses exclusively.

Two categories of errors are handled:
1. HTTPException (404 Not Found, 405 Method Not Allowed, etc.) — caught
   individually and formatted with the exception's name, code, and description.
2. Generic Exception (500 Internal Server Error) — catches all unhandled
   exceptions and returns a safe, structured JSON response without leaking
   internal implementation details in production.

Usage:
    Called during application factory initialization in app/__init__.py:
    register_error_handlers(app)
"""

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    """Register centralized JSON error handlers on the Flask application.

    Attaches error handlers for HTTPException and generic Exception to ensure
    all error responses are structured JSON with consistent format:
    {"error": "<name>", "status": <code>, "description": "<detail>"}

    Args:
        app: The Flask application instance to register handlers on.
    """

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc):
        """Handle all HTTP exceptions with structured JSON responses.

        Catches 404 Not Found, 405 Method Not Allowed, 400 Bad Request, and
        all other HTTPException subclasses. Returns a JSON object with the
        exception's name, numeric status code, and human-readable description.
        """
        response = jsonify({
            'error': exc.name,
            'status': exc.code,
            'description': exc.description
        })
        response.status_code = exc.code
        return response

    @app.errorhandler(Exception)
    def handle_generic_exception(exc):
        """Handle unhandled exceptions with a generic 500 JSON response.

        Catches all exceptions not covered by the HTTPException handler.
        Returns a safe JSON error response without exposing internal details
        such as stack traces or variable values.
        """
        response = jsonify({
            'error': 'Internal Server Error',
            'status': 500,
            'description': str(exc) if app.config.get('DEBUG') else
                'An unexpected error occurred'
        })
        response.status_code = 500
        return response
