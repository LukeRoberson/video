"""
Module: profile_api.py

API endpoints that the browser will use to fetch additional information
    Specifically, for user profiles and their management.

Blueprints:
    - api_profile: Blueprint for user profile API endpoints.
        For example, managing user profiles and their related data.

Routes:
    - /api/profile/create
        - create_profile: Creates a new user profile.
    - /api/profile/set_active
        - set_active_profile: Sets the profile for the session.
    - /api/profile/get_active
        - get_active_profile: Retrieves the profile for the session.
    - /api/profile/mark_watched
        - mark_watched: Marks a video as watched for the acve profile.
    - /api/profile/mark_unwatched
        - mark_unwatched: Marks a video as unwatched for the profile.
    - /api/profile/in_progress
        - in_progress_videos: Manages in-progress videos for the profile.
    - /api/profile/delete/<int:profile_id>
        - delete_profile: Deletes a user profile by ID.
    - /api/profile/update/<int:profile_id>
        - update_profile: Updates a user profile by ID.

Dependencies:
    - Flask: For creating the API endpoints.

Custom Dependencies:
    - LocalDbContext: Context manager for local database connections.
    - ProfileManager: Manages user profile-related operations in the local db.
    - ProgressManager: Manages in-progress video tracking for user profiles.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
    request,
    session,
)
import logging

# Custom imports
from api.api import (
    api_error,
    api_success,
)
from api.local_db import (
    LocalDbContext,
    ProfileManager,
)


# Blueprint for user profile API endpoints
profile_bp = Blueprint(
    'api_profile',
    __name__,
)


@profile_bp.route(
    "/api/profile/set_active",
    methods=["POST"]
)
def set_active_profile() -> Response:
    """
    Set the active profile for the session.

    Expects JSON:
        {
            "profile_id": <int or "guest">
        }

    Returns:
        Response: A redirect to the home page after setting the active profile.
    """

    # Get the JSON data from the request
    logging.info("Setting active profile from request data")
    data = request.get_json()
    if not data:
        logging.error("No data provided for setting active profile.")
        return api_error("No data provided", 400)

    if "profile_id" not in data:
        logging.error("Missing 'profile_id' in request data.")
        return api_error("Missing 'profile_id' in request data", 400)

    # Set the active profile
    profile_id = data.get("profile_id", "guest")
    session["active_profile"] = profile_id
    logging.info(f"Active profile set to: {profile_id}")

    # Set admin status
    profile_admin = data.get("profile_admin", None)
    session["profile_admin"] = True if profile_admin == '1' else False
    if session["profile_admin"]:
        logging.info(f"Profile {profile_id} is an admin")

    # Return a JSON response indicating success
    return api_success(
        data={"active_profile": profile_id}
    )


@profile_bp.route(
    "/api/profile/get_active",
    methods=["GET"]
)
def get_active_profile() -> Response:
    """
    Get the active profile for the session.

    Returns:
        Response: A JSON response with the active profile ID.
    """

    # Retrieve the active profile from the session
    active_profile = session.get("active_profile", None)

    # If no active profile is set, return a default value
    if active_profile is None or active_profile == "guest":
        logging.info("No active profile set, returning guest profile.")
        profile = {
            "id": None,
            "name": "Guest",
            "image": "guest.png"
        }

    else:
        with LocalDbContext() as db:
            profile_mgr = ProfileManager(db)
            profile = profile_mgr.read(
                profile_id=active_profile
            )

            profile = profile[0] if profile else {
                "id": None,
                "name": "Guest",
                "image": "guest.png"
            }

    logging.info(f"Active profile returned: {profile}")

    # Return a JSON response with the active profile ID
    return api_success(
        data={"active_profile": profile}
    )
