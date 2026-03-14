"""
Module: main.py

This is the entry point for the Flask application (API).

How to use:
    From the base directory of the project, run the application using:
        `python -m api.main`

    Supported command-line arguments:
        --debug: Run the server in debug mode.
            Sets Flask to debug mode and the logging level to DEBUG.
        --logging-level: Set the logging level for the application.
            Choices: DEBUG, INFO, WARNING, ERROR, CRITICAL
            Setting debug mode will override this to DEBUG.
            Default is WARNING.

Classes:
    - ColouredFormatter:
        Custom logging formatter that adds color codes to log messages
        based on their severity level.

Dependencies:
    - api (the application factory in __init__.py)
    - Flask: Web framework.
    - logging: Application logging.
    - argparse: Command-line argument parsing.
"""


# Standard library imports
import argparse

# Custom imports
from api import create_app


# Variables
DEBUG = False
PORT = 5010
HOST = "0.0.0.0"
SECRET_KEY = "gU0BTfsKgCJNpNipm5PeyhapfYCGCVB2"
TEMPLATE_FOLDER = "templates"
STATICFOLDER = "static"


# Setup argument parsing
parser = argparse.ArgumentParser(
    description="Run the Flask API server."
)
parser.add_argument(
    "--debug",
    action="store_true",
    help="Run the server in debug mode."
)
parser.add_argument(
    "--logging-level",
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    default="INFO",
    help="Set the logging level for the application."
)
args = parser.parse_args()

# Set debug mode and logging level based on arguments
DEBUG = args.debug
if DEBUG:
    log_level = "DEBUG"
else:
    log_level = args.logging_level


# Register the filter with Flask
app = create_app(
    key=SECRET_KEY,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATICFOLDER,
    log_level=log_level
)


if __name__ == "__main__":
    app.run(
        host=HOST,
        debug=DEBUG,
        port=PORT,
    )
