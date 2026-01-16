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
    '/api/profile/create',
    methods=['POST'],
)
def create_profile() -> Response:
    """
    Create a new user profile.

    Expected JSON Body:
        {
            "name": "<Profile Name>",
            "image": "<image file name>",
        }

    Returns:
        Response: A JSON response indicating that the profile creation
            endpoint is not yet implemented.
    """

    # Get the JSON data and validate it
    data = request.get_json()
    if not data:
        logging.error("No data provided for profile creation.")
        return api_error('No data provided', 400)

    if 'name' not in data or 'image' not in data:
        logging.error("Missing required fields for profile creation.")
        return api_error('Missing required fields: name and image', 400)

    # Extract profile name and image from the data
    profile_name = data['name']
    profile_image = data['image']

    # Create a new profile in the local database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        id = profile_mgr.create(
            name=profile_name,
            image=profile_image,
        )

    # Handle errors
    if id is None:
        logging.error("Failed to create profile in the local database.")
        return api_error('Failed to create profile', 500)

    # Return the response with the created profile ID
    return api_success(message=f'Created profile with ID: {id}')


@profile_bp.route(
    "/api/profile/delete/<int:profile_id>",
    methods=["DELETE"],
)
def delete_profile(profile_id: int) -> Response:
    """
    Delete a user profile by ID.

    Args:
        profile_id (int): The ID of the profile to delete.

    Returns:
        Response: A JSON response indicating success or failure.
    """

    logging.info(f"Deleting profile with ID: {profile_id}")

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)

        # Check if the profile exists
        profile = profile_mgr.read(profile_id)
        if profile is None:
            logging.error(f"Profile with ID {profile_id} not found.")
            return api_error(f"Profile with ID {profile_id} not found", 404)

        # Delete the profile (should return the deleted profile ID)
        result = profile_mgr.delete(profile_id)
        if result != profile_id:
            logging.error(f"Failed to delete profile with ID {profile_id}.")
            return api_error(
                f"Failed to delete profile with ID {profile_id}",
                500
            )

        logging.info(f"Successfully deleted profile with ID {profile_id}.")
        return api_success(
            message=f"Profile with ID {profile_id} deleted successfully."
        )


@profile_bp.route(
    "/api/profile/update/<int:profile_id>",
    methods=["POST"],
)
def update_profile(profile_id: int) -> Response:
    """
    Update a user profile by ID.

    Expects JSON:
        {
            "name": "<new profile name>",
            "icon": "<new profile icon>"
        }

    Args:
        profile_id (int): The ID of the profile to update.

    Returns:
        Response: A JSON response indicating success or failure.
    """

    data = request.get_json()
    if not data:
        logging.error("No data provided for updating profile.")
        return api_error("No data provided", 400)

    name = data.get("name", None)
    icon = data.get("icon", None)

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)

        # Check if the profile exists
        profile = profile_mgr.read(profile_id)
        if profile is None:
            logging.error(f"Profile with ID {profile_id} not found.")
            return api_error(f"Profile with ID {profile_id} not found", 404)

        # Update the profile (should return the profile ID)
        result = profile_mgr.update(
            profile_id=profile_id,
            name=name,
            image=icon,
        )
        if result != profile_id:
            logging.error(f"Failed to update profile with ID {profile_id}.")
            return api_error(
                f"Failed to update profile with ID {profile_id}",
                500
            )

    logging.info(f"Successfully updated profile with ID {profile_id}.")

    return api_success(
        message=f"Profile with ID {profile_id} updated successfully."
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
    "/api/profile/clear_history/<int:profile_id>",
    methods=["POST"],
)
def clear_watch_history(profile_id: int) -> Response:
    """
    Clear the watch history for a user profile by ID.
        If there's a JSON body, clear only the specified video ID.
        Otherwise, clear the entire watch history.

    Expected JSON Body:
        {
            "video_id": <int>
        }

    Args:
        profile_id (int):
            The ID of the profile whose watch history is to be cleared.

    Returns:
        Response: A JSON response indicating success or failure.
    """

    logging.info(f"Clearing watch history for profile with ID: {profile_id}")

    data = request.get_json(silent=True) if request.is_json else None

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)

        # Check if the profile exists
        profile = profile_mgr.read(profile_id)
        if profile is None:
            logging.error(f"Profile with ID {profile_id} not found.")
            return api_error(f"Profile with ID {profile_id} not found", 404)

        # Clear an individual video from the watch history
        if data and "video_id" in data:
            result = profile_mgr.remove_history(
                profile_id=profile_id,
                video_id=data["video_id"],
            )
            if not result:
                logging.error(
                    f"Failed to clear watch history for profile {profile_id}."
                )
                return api_error(
                    f"Failed to clear watch history for profile {profile_id}",
                    500
                )

            logging.info(
                f"Cleared video {data["video_id"]} "
                f"from watch history of profile {profile_id}."
            )
            return api_success(
                message=f"Cleared video {data["video_id"]} "
                f"from watch history of profile {profile_id}."
            )

        # Clear the entire watch history
        else:
            result = profile_mgr.remove_history(
                profile_id=profile_id,
            )
            if not result:
                logging.error(
                    f"Failed to clear watch history for profile {profile_id}."
                )
                return api_error(
                    f"Failed to clear watch history for profile {profile_id}",
                    500
                )

        logging.info(f"Cleared watch history for profile {profile_id}.")
        return api_success(
            message=f"Cleared watch history for profile {profile_id}."
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
