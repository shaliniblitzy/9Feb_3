"""
Core API blueprint module for the Flask application.
"""
Core API blueprint module for the Flask application.
References Tech Spec §5.2.1 (Request Processing Pipeline) — this module
provides the versioned REST API gateway endpoints. All API routes are prefixed
with /api/v1/ to support future API versioning without breaking existing
consumers.

Endpoints:
- GET /api/v1/status: Returns the application's operational status, service
  name, and version.
- POST /api/v1/echo: Accepts a JSON request body and echoes it back, serving
  as both a connectivity test and a demonstration of the JSON request/response
  processing pipeline with input validation.

The api_bp Blueprint is registered by the application factory in
app/__init__.py without a url_prefix, so endpoints are accessible at
/api/v1/status and /api/v1/echo directly.
"""

from flask import Blueprint, jsonify, request


# Blueprint instance for core API routes. Registered by the application
# factory in app/__init__.py without a url_prefix.
api_bp = Blueprint('api', __name__)


@api_bp.route('/api/v1/status', methods=['GET'])
def api_status():
    """Application operational status endpoint.

    Provides current operational status, the service name, and the API version.
    Used by monitoring dashboards and API consumers to verify service health
    and discover the deployed version.

    Returns:
        JSON response with HTTP 200:
        {"status": "operational", "service": "9Feb_3", "version": "1.0.0"}
    """
    return jsonify({
        'status': 'operational',
        'service': '9Feb_3',
        'version': '1.0.0'
    }), 200


@api_bp.route('/api/v1/echo', methods=['POST'])
def api_echo():
    """JSON echo endpoint for testing request/response handling.

    Accepts a JSON request body and returns it within an echo wrapper. Validates
    that the request contains valid JSON with proper Content-Type header.

    Request:
        Content-Type: application/json
        Body: Any valid JSON object

    Returns:
        On success (HTTP 200):
        {"echo": <request_body>, "status": "success"}

        On invalid content type (HTTP 400):
        {"error": "Invalid content type", "status": "error"}

        On missing/empty/malformed JSON body (HTTP 400):
        {"error": "Invalid or empty JSON body", "status": "error"}
    """
    # Validate that the request has a JSON content type
    if not request.is_json:
        return jsonify({
            'error': 'Invalid content type',
            'status': 'error'
        }), 400

    # Attempt to parse the JSON body; silent=True returns None on failure
    data = request.get_json(silent=True)

    # Validate that the parsed JSON is not None or empty
    if data is None:
        return jsonify({
            'error': 'Invalid or empty JSON body',
            'status': 'error'
        }), 400

    # Return the echoed data with a success status
    return jsonify({
        'echo': data,
        'status': 'success'
    }), 200
