"""
Module: web.py

Define flask routes for the web application.

Routes:
    - /admin: Render the admin dashboard.

Dependencies:
    - Flask: For creating the web application.
    - Blueprint: For organizing routes.
    - render_template: For rendering HTML templates.
    - make_response: For creating HTTP responses.
"""

# Standard library imports
from flask import (
    Blueprint,
    Response,
    render_template,
    make_response,
)
from local_db import (
    LocalDbContext,
    ProfileManager,
)
import random
import os


web_bp = Blueprint(
    'web_pages',
    __name__,
)

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


@web_bp.route(
    "/",
    methods=["GET"],
)
def home() -> Response:
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

    return make_response(
        render_template(
            "home.html",
            banner_pics=banner_pics,
        )
    )


@web_bp.route(
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


@web_bp.route(
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


@web_bp.route(
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
