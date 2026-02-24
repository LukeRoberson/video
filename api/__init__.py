"""
Flask Application Initialization

This module initializes the Flask application, configures logging,
    registers blueprints, and initializes the search service.

Usage:
    From the base directory of the project, run the application using:
        python -m api.main

Blueprints Registered:
    - admin_bp: API endpoints for admin functionalities.
    - video_bp: API endpoints for video functionalities.
    - profile_bp: API endpoints for user profile functionalities.
    - search_bp: API endpoints for search functionalities.

Classes:
    - ColouredFormatter:
        Custom logging formatter that adds color codes to log messages
        based on their severity level.

Dependencies:
    - Flask: Web framework.
    - logging: Application logging.
    - flask_cors: For handling Cross-Origin Resource Sharing (CORS).
    - SearchService: Service for handling search functionalities.

Custom Imports:
    - api.api: Blueprints for admin and video API endpoints.
    - api.profile: Blueprint for user profile API endpoints.
    - api.api_search: Blueprint for search API endpoints.
"""

# Standard library imports
import logging
from flask import Flask
from flask_cors import CORS

# Custom imports
from api.api import (
    admin_bp,
    video_bp
)
from api.profile import profile_bp
from api.api_search import search_bp
from api.search import SearchService


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


def create_app(
    key: str,
    template_folder: str = 'templates',
    static_folder: str = 'static',
) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        key (str): Secret key for the Flask application.
        template_folder (str): Path to the templates folder.
        static_folder (str): Path to the static files folder.

    Returns:
        Flask: The configured Flask application instance.
    """

    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder,
    )

    # Allow requests from the frontend on localhost:5000
    #   Credentials are needed for session management (session cookies)
    CORS(
        app,
        origins=['http://localhost:5000'],
        supports_credentials=True
    )

    # Set the secret key for the Flask application
    app.secret_key = key

    # Register blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(search_bp)

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
