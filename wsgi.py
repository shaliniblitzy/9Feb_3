"""
WSGI entry point for the Flask application.

References Tech Spec §5.2.1 (Transport Reception) — this module bridges the
WSGI server (Gunicorn, uWSGI, or any WSGI-compliant server) to the Flask
application factory. The FLASK_CONFIG environment variable controls which
configuration profile is loaded at deployment time.

Usage:
    gunicorn wsgi:app
    uwsgi --module wsgi:app
"""

import os

from app import create_app

# Read configuration profile from environment variable, defaulting to 'default'
config_name = os.environ.get('FLASK_CONFIG', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()

