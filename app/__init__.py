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

Classes:
    - ColouredFormatter:
        Custom logging formatter that adds color codes to log messages
        based on their severity level.

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


class ColouredFormatter(
    logging.Formatter
):
    """
    Custom formatter that adds color codes to log messages based on level.

    Attributes:
        COLORS (dict): Mapping of log levels to ANSI color codes
        RESET (str): ANSI reset code

    Methods:
        format:
            Format log record with appropriate color
    """

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m'  # Magenta
    }
    RESET = '\033[0m'

    def format(
        self,
        record: logging.LogRecord
    ) -> str:
        """
        Format log record with appropriate color.

        Args:
            record (logging.LogRecord): The log record to format

        Returns:
            str: Formatted log message with color codes
        """

        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


# Configure logging
level = logging.INFO

# Create formatters
file_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
console_formatter = ColouredFormatter(
    '%(levelname)s - %(message)s'
)

# Create handlers
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(console_formatter)

# Configure root logger
logging.basicConfig(
    level=level,
    handlers=[
        file_handler,
        stream_handler
    ]
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
