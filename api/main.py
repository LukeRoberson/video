"""
Module: main.py

This is the entry point for the Flask application (API).

How to use:
    From the base directory of the project, run the application using:
    `python -m api.main`

Classes:
    - ColouredFormatter:
        Custom logging formatter that adds color codes to log messages
        based on their severity level.

Dependencies:
    - api (the application factory in __init__.py)
    - Flask: Web framework.
    - logging: Application logging.
"""

# Custom imports
from api import create_app


# Variables
DEBUG = True
PORT = 5010
HOST = "0.0.0.0"
SECRET_KEY = "gU0BTfsKgCJNpNipm5PeyhapfYCGCVB2"
TEMPLATE_FOLDER = "templates"
STATICFOLDER = "static"


# Register the filter with Flask
app = create_app(
    key=SECRET_KEY,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATICFOLDER,
)


if __name__ == "__main__":
    app.run(
        host=HOST,
        debug=DEBUG,
        port=PORT,
    )
