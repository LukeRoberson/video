"""
Module: main.py

This module initializes the Flask application and sets up the main routes.
It includes the home page and video details page, along with necessary imports

Blueprints:
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
import os
import random
from flask import (
    Flask,
    Response,
    render_template,
    make_response
)

# Custom imports
from web_categories import category_bp
from web_dynamic import dynamic_bp
from api import (
    api_bp,
    seconds_to_hhmmss
)
from local_db import (
    LocalDbContext,
    ProfileManager,
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
app.jinja_env.filters['seconds_to_hhmmss'] = seconds_to_hhmmss
app.jinja_env.filters['nl2br'] = nl2br


# Define the static directory for profile images
profile_dir = os.path.join(
    'static',
    'img',
    'profiles'
)

# Define the static directory for banner images
banner_dir = os.path.join(
    'static',
    'img',
    'banner'
)


@app.route(
    "/",
    methods=["GET"],
)
def home():
    """
    A very simple home page that renders the main HTML template.

    Returns:
        Response: A rendered HTML 'welcome' page
    """

    banner_pics = [
        f for f in os.listdir(banner_dir)
        if (
            f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        )
    ]
    print("Banner Pictures:", banner_pics)

    return render_template(
        "home.html",
        banner_pics=banner_pics,
    )


@app.route(
    "/select_profile",
    methods=["GET"]
)
def select_profile() -> Response:
    """
    Render the profile selection page.

    Returns:
        Response: A rendered HTML page for selecting a profile.
    """

    # Get all profiles from the local database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile_list = profile_mgr.read()

    return make_response(
        render_template(
            'select_profile.html',
            profiles=profile_list,
        )
    )


@app.route(
    "/create_profile",
    methods=["GET"]
)
def create_profile() -> Response:
    """
    Render the profile creation page.

    Returns:
        Response: A rendered HTML page for creating a new profile.
    """

    profile_pics = [
        f for f in os.listdir(profile_dir)
        if (
            f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) and
            f.lower() != 'guest.png'
        )
    ]
    random.shuffle(profile_pics)

    return make_response(
        render_template(
            'create_profile.html',
            profile_pics=profile_pics
        )
    )


@app.route(
    "/admin",
    methods=["GET"],
)
def admin_dashboard() -> Response:
    """
    Render the admin dashboard.

    Returns:
        Response: A rendered HTML page with the admin dashboard.
    """

    return make_response(
        render_template(
            "admin.html"
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
