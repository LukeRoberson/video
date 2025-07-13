"""
Flask Application Initialization

This module initializes the Flask application, configures logging,
    registers blueprints, and sets up custom Jinja filters.

Usage:
    From the base directory of the project, run the application using:
        python -m app.main

Blueprints Registered:
    - web_bp: Main web routes for the application.
    - category_bp: Routes for category-related pages.
    - dynamic_bp: Routes for dynamic pages
        (tags, speakers, characters, scriptures).
    - api_bp: API endpoints for video data.
    - error_bp: Custom error pages (e.g., 403 Forbidden).

Dependencies:
    - Flask: Web framework.
    - logging: Application logging.

Custom Filters:
    - nl2br: Converts newlines in a string to HTML line breaks.
    - seconds_to_hhmmss: Converts seconds to a formatted string (HH:MM:SS).

Custom Imports:
    - app.web_categories: Blueprint for category-related web routes.
    - app.web_dynamic: Blueprint for dynamic web routes.
    - app.api: Blueprint for API endpoints.
    - app.web: Main web blueprint.
    - app.api.seconds_to_hhmmss:
        Function to convert seconds to HH:MM:SS format.
"""

# Standard library imports
import logging
from flask import Flask

# Custom imports
from app.web_categories import category_bp
from app.web_dynamic import dynamic_bp
from app.web import web_bp
from app.web_errors import (
    error_bp,
    forbidden,
    not_found,
)
from app.api import (
    api_bp,
    seconds_to_hhmmss,
)
from app.api_profile import profile_api_bp


SECRET_KEY = "gU0BTfsKgCJNpNipm5PeyhapfYCGCVB2"
LOCAL_DB_PATH = "/local.db"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


# Define the custom filter
def nl2br(
    value
) -> str:
    """
    Convert newlines in a string to HTML line breaks.

    Args:
        value (str): The input string containing newlines.

    Returns:
        str: The input string with newlines replaced by `<br>` tags.
    """

    return value.replace('\n', '<br>')


def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static',
    )

    # Import and register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(profile_api_bp)
    app.register_blueprint(web_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(dynamic_bp)
    app.register_blueprint(error_bp)

    # Add jinja filters
    app.jinja_env.filters['seconds_to_hhmmss'] = seconds_to_hhmmss
    app.jinja_env.filters['nl2br'] = nl2br

    # Set the secret key for the Flask application
    app.secret_key = SECRET_KEY

    # Register the 4xx error handlers globally
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)

    return app
