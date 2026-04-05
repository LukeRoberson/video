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
    - api.profile: Blueprint for user profile API endpoints.
    - api.api_search: Blueprint for search API endpoints.
    - api.api_video: Blueprint for video-related API endpoints.
    - api.api_category: Blueprint for category-related API endpoints.
    - api.api_tag: Blueprint for tag-related API endpoints.
    - api.api_scripture: Blueprint for scripture-related API endpoints.
    - api.api_location: Blueprint for location-related API endpoints.
    - api.api_speaker: Blueprint for speaker-related API endpoints.
    - api.api_character: Blueprint for character-related API endpoints.
    - api.api_similarity: Blueprint for similarity-related API endpoints.
    - api.search: SearchService class for handling search functionalities.
"""

# Standard library imports
import logging
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# Custom imports
from api.api_profile import profile_bp
from api.api_search import search_bp
from api.api_video import video_endpoint
from api.api_category import category_endpoint
from api.api_tag import tag_endpoint
from api.api_scripture import scripture_endpoint
from api.api_location import location_endpoint
from api.api_speaker import speaker_endpoint
from api.api_character import character_endpoint
from api.api_similarity import similarity_endpoint
from api.search import SearchService


# CORS, for running locally with the frontend on localhost:5000
FRONTEND_ORIGIN = 'http://localhost:5000'

# Settings
APP_NAME = 'Videos API'
APP_VERSION = '1.0.0'


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
file_handler = logging.FileHandler('api.log', encoding='utf-8')
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
    log_level: str = 'WARNING',
) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        key (str): Secret key for the Flask application.
        template_folder (str): Path to the templates folder.
        static_folder (str): Path to the static files folder.
        log_level (str): Logging level for the application.

    Returns:
        Flask: The configured Flask application instance.
    """

    # Set the logging level
    match log_level:
        case "DEBUG":
            level = logging.DEBUG
        case "INFO":
            level = logging.INFO
        case "WARNING":
            level = logging.WARNING
        case "ERROR":
            level = logging.ERROR
        case "CRITICAL":
            level = logging.CRITICAL
        case _:
            level = logging.INFO
            logging.warning(
                f"Invalid logging level: '{log_level}'. Defaulting to INFO"
            )

    # Configure the root logger and all handlers to the specified level
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    for handler in root_logger.handlers:
        handler.setLevel(level)
    print(f"Logging level set to: {logging.getLevelName(root_logger.level)}")

    # Create the Flask application
    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder='static',
        static_url_path='/api/static'
    )

    # Allow requests from the frontend on localhost:5000
    #   Credentials are needed for session management (session cookies)
    CORS(
        app,
        origins=[FRONTEND_ORIGIN],
        supports_credentials=True
    )

    # Set the secret key for the Flask application
    app.secret_key = key

    # Register blueprints
    app.register_blueprint(profile_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(video_endpoint)
    app.register_blueprint(category_endpoint)
    app.register_blueprint(tag_endpoint)
    app.register_blueprint(scripture_endpoint)
    app.register_blueprint(location_endpoint)
    app.register_blueprint(speaker_endpoint)
    app.register_blueprint(character_endpoint)
    app.register_blueprint(similarity_endpoint)

    # Register Swagger UI for API documentation
    swagger_ui_blueprint = get_swaggerui_blueprint(
        '/api/docs',
        '/api/static/swagger.yaml',
        config={'app_name': APP_NAME}
    )
    app.register_blueprint(swagger_ui_blueprint)

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
