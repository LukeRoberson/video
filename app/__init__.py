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
    - profile_api_bp: API endpoints for user profile management.
    - search_bp: API endpoints for video search functionality.

Dependencies:
    - Flask: Web framework.
    - logging: Application logging.

Custom Filters:
    - nl2br: Converts newlines in a string to HTML line breaks.
    - seconds_to_hhmmss: Converts seconds to a formatted string (HH:MM:SS).

Custom Imports:
    - app.web_categories: Blueprint for category-related web routes.
    - app.web_dynamic: Blueprint for dynamic web routes.
    - app.web: Main web blueprint.
    - app.web_errors: Blueprint and handlers for error pages.
    - app.api: Blueprint for API endpoints.
    - app.api_profile: Blueprint for user profile API endpoints.
    - app.api_search: Blueprint for video search API endpoints.
    - search: Module providing the SearchService class.
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
from app.api_search import search_bp
from search import SearchService


SECRET_KEY = "gU0BTfsKgCJNpNipm5PeyhapfYCGCVB2"
LOCAL_DB_PATH = "/local.db"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


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
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """

    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static',
    )

    # Set the secret key for the Flask application
    app.secret_key = SECRET_KEY

    # Import and register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(profile_api_bp)
    app.register_blueprint(web_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(dynamic_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(search_bp)

    # Add jinja filters
    app.jinja_env.filters['seconds_to_hhmmss'] = seconds_to_hhmmss
    app.jinja_env.filters['nl2br'] = nl2br

    # Register the 4xx error handlers globally
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)

    # Initialize search service with app context
    with app.app_context():
        try:
            # SearchService uses DatabaseContext internally, no params needed
            search_service = SearchService()
            app.config['SEARCH_SERVICE'] = search_service
            logger.info("Search service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize search service: {e}")
            logger.warning(
                "Application will continue with database fallback only"
            )

    return app
