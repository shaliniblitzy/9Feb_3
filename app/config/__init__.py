"""
Environment-specific configuration module for the Flask application.
Environment-specific configuration module for the Flask application.
Environment-specific configuration module for the Flask application.
Environment-specific configuration module for the Flask application.
Environment-specific configuration module for the Flask application.
Environment-specific configuration module for the Flask application.
Environment-specific configuration module for the Flask application.
Environment-specific configuration module for the Flask application.

References Tech Spec §5.2.1 (Scaling Considerations) — this module provides
environment-specific configuration management for the Flask application factory.
It defines four configuration classes that inherit from a shared BaseConfig:

- BaseConfig: Shared defaults for all environments (SECRET_KEY, DEBUG, TESTING,
  JSON_SORT_KEYS, APP_NAME, APP_VERSION).
- DevelopmentConfig: Enables debug mode and verbose logging for local development.
- TestingConfig: Enables testing mode with a fixed SERVER_NAME for test client
  URL generation and verbose logging for test diagnostics.
- ProductionConfig: Hardened settings with mandatory SECRET_KEY from environment
  variables, disabled debug/testing flags, and WARNING-level logging.

The get_config() resolver function maps human-readable configuration profile
names ('development', 'testing', 'production', 'default') to the appropriate
configuration class. This module is the first thing loaded by the application
factory in app/__init__.py via create_app().
"""

import os


class BaseConfig:
    """Base configuration with shared defaults for all environments.

    All environment-specific configuration classes inherit from this base.
    Provides sensible defaults that can be overridden per environment.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False  # Preserve insertion order for consistent JSON output
    APP_NAME = '9Feb_3'
    APP_VERSION = '1.0.0'


class DevelopmentConfig(BaseConfig):
    """Development environment configuration.

    Enables debug mode for auto-reloading and interactive debugger.
    Sets verbose DEBUG-level logging for maximum visibility during
    local development.
    """

    DEBUG = True
    ENV = 'development'
    LOG_LEVEL = 'DEBUG'


class TestingConfig(BaseConfig):
    """Testing environment configuration.

    Enables both TESTING and DEBUG flags. Sets SERVER_NAME to 'localhost'
    to allow Flask's test client to generate URLs without an active
    request context. Uses DEBUG-level logging for test diagnostics.
    """

    TESTING = True
    DEBUG = True
    ENV = 'testing'
    LOG_LEVEL = 'DEBUG'
    SERVER_NAME = 'localhost'


class ProductionConfig(BaseConfig):
    """Production environment configuration.

    Hardened settings: debug and testing are explicitly disabled, logging
    is restricted to WARNING level to reduce noise. SECRET_KEY is read
    exclusively from the SECRET_KEY environment variable with no fallback
    default — unlike BaseConfig, which provides a development-only default.
    If the environment variable is not set, SECRET_KEY will be None, and
    Flask will reject any operation requiring a secure secret (session
    signing, CSRF tokens, etc.), preventing deployment with insecure defaults.
    """

    DEBUG = False
    TESTING = False
    ENV = 'production'
    LOG_LEVEL = 'WARNING'
    # Override BaseConfig.SECRET_KEY — no fallback default is provided.
    # The SECRET_KEY must come exclusively from the environment variable.
    # If not set, SECRET_KEY is None, which Flask treats as a configuration
    # error for any security-critical operation.
    SECRET_KEY = os.environ.get('SECRET_KEY')


# Configuration name-to-class mapping used by get_config() to resolve
# string-based configuration profile names to their corresponding classes.
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}


def get_config(config_name='default'):
    """Resolve a configuration profile name to its configuration class.

    Args:
        config_name: One of 'development', 'testing', 'production', or
            'default'. Defaults to 'default', which maps to DevelopmentConfig.

    Returns:
        The configuration class corresponding to the given profile name.

    Raises:
        KeyError: If config_name is not a recognized configuration profile.
            The error message lists all valid configuration names.
    """
    if config_name not in config:
        valid_names = ', '.join(sorted(config.keys()))
        raise KeyError(
            f"Invalid configuration name '{config_name}'. "
            f"Valid configuration names are: {valid_names}"
        )
    return config[config_name]
