"""
Health check blueprint module for the Flask application.

References Tech Spec §5.2.6 (Infrastructure) — this module provides liveness
and readiness probe endpoints for container orchestration platforms such as
Kubernetes. The /health endpoint confirms the service process is running and
responsive (liveness), while the /ready endpoint confirms the service is
prepared to accept traffic (readiness).

Both endpoints return structured JSON responses with Content-Type:
application/json, following the REST API conventions established across the
application. These endpoints are public and require no authentication.

The health_bp Blueprint is registered by the application factory in
app/__init__.py without a url_prefix, so endpoints are accessible at
/health and /ready directly.
"""

from flask import Blueprint, jsonify


# Blueprint instance for health check routes. Registered by the application
# factory in app/__init__.py without a url_prefix.
health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Liveness probe endpoint.

    Indicates that the service process is running and responsive. Container
    orchestration platforms (e.g., Kubernetes) poll this endpoint to determine
    whether the container should be restarted.

    Returns:
        JSON response with HTTP 200:
        {"status": "healthy", "service": "9Feb_3"}
    """
    return jsonify({
        'status': 'healthy',
        'service': '9Feb_3'
    }), 200


@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness probe endpoint.

    Indicates that the service is ready to accept traffic. In future iterations,
    this endpoint will verify connectivity to downstream dependencies (database,
    cache, external APIs) before reporting readiness.

    Returns:
        JSON response with HTTP 200:
        {"status": "ready", "service": "9Feb_3"}
    """
    return jsonify({
        'status': 'ready',
        'service': '9Feb_3'
    }), 200
