"""
Module: main.py

This module initializes the Flask application and sets up the main routes.
It includes the home page and video details page, along with necessary imports

Blueprints:
    - web_bp:
        Main web routes for the application.
    - category_bp:
        Web routes for category-related pages.
    - dynamic_bp:
        Web routes for dynamic pages based on items like tags, speakers,
        characters, and scriptures.
    - api_bp:
        API endpoints for fetching video data from the browser.

Dependencies:
    - Flask: For creating the web application.
    - logging: For logging application events.

Custom Dependencies:
    - DatabaseContext: Context manager for database connections.
    - VideoManager: Manages video-related database operations.
    - CategoryManager: Manages category-related database operations
    - TagManager: Manages tag-related database operations.
    - SpeakerManager: Manages speaker-related database operations.
    - CharacterManager: Manages character-related database operations.
    - ScriptureManager: Manages scripture-related database operations.
"""

# Standard library imports
import logging
from flask import Flask

# Custom imports
from web import web_bp
from web_categories import category_bp
from web_dynamic import dynamic_bp
from api import (
    api_bp,
    seconds_to_hhmmss
)


# Define the custom filter
def nl2br(value):
    return value.replace('\n', '<br>')


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


# Create a secret key for the Flask application
SECRET_KEY = "gU0BTfsKgCJNpNipm5PeyhapfYCGCVB2"


# Register the filter with Flask
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
app.secret_key = SECRET_KEY
app.register_blueprint(category_bp)
app.register_blueprint(dynamic_bp)
app.register_blueprint(api_bp)
app.register_blueprint(web_bp)
app.jinja_env.filters['seconds_to_hhmmss'] = seconds_to_hhmmss
app.jinja_env.filters['nl2br'] = nl2br


if __name__ == "__main__":
    app.run(debug=True)
