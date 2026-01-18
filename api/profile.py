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
    ProgressManager,
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
    "/api/profile/mark_watched",
    methods=["GET"]
)
def get_watched() -> Response:
    """
    Get videos that are marked as watched for the active profile.

    Request Args:
        video_id (int):
            The ID of the video to check watched status for.
        profile (int):
            The ID of the profile to check watched status for.

    Returns:
        Response: A JSON response with the list of watched videos.
    """

    # Get the active profile from the parameter
    active_profile = request.args.get("profile", None)

    # If not provided, get from the session
    if not active_profile:
        logging.info(
            "No active_profile parameter provided, "
            "retrieving from session"
        )
        active_profile = session.get("active_profile", "guest")

    # If no active profile is set, return empty response
    if active_profile is None or active_profile == "guest":
        return api_success(
            message="No in progress videos for guest profile"
        )

    logging.info(f"Active profile for watched videos: {active_profile}")

    video = request.args.get("video_id", None)
    if not video:
        return api_error(error="Missing 'video_id' in request data")
    video = int(video)

    with LocalDbContext() as local_db:
        profile_mgr = ProfileManager(local_db)

        watched = profile_mgr.check_watched(
            profile_id=int(active_profile),
            video_id=video
        )

    return api_success(
        data={"video_id": video, "watched": watched}
    )


@profile_bp.route(
    "/api/profile/mark_watched",
    methods=["POST"]
)
def mark_watched() -> Response:
    """
    Mark a video as watched for the active profile.

    Expects JSON:
        {
            "video_id": <int>
        }

    Returns:
        Response: A JSON response indicating success or failure.
    """

    data = request.get_json()
    video_id = data.get("video_id", None)

    if not video_id:
        return api_error(error="Missing 'video_id' in request data")

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        progress_mgr = ProgressManager(db)

        # Mark the video as watched for the active profile
        result = profile_mgr.mark_watched(
            profile_id=session.get("active_profile", "guest"),
            video_id=video_id
        )

        if not result:
            return api_error(
                error=f"Failed to mark video {video_id} as watched",
                status=500
            )

        # Remove from in progress list if needed
        result = progress_mgr.delete(
            profile_id=session.get("active_profile", "guest"),
            video_id=video_id
        )

    return api_success(
        message=f"Marked video {video_id} as watched"
    )


@profile_bp.route(
    "/api/profile/mark_unwatched",
    methods=["POST"]
)
def mark_unwatched() -> Response:
    """
    Mark a video as unwatched for the active profile.

    Expects JSON:
        {
            "video_id": <int>
        }

    Returns:
        Response: A JSON response indicating success or failure.
    """

    logging.info("Received request to mark video as unwatched")

    data = request.get_json()
    video_id = data.get("video_id", None)

    if not video_id:
        return api_error(error="Missing 'video_id' in request data")

    logging.info(
        f"Marking video {video_id} as unwatched "
        f"for profile {session.get('active_profile', 'guest')}"
    )

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        result = profile_mgr.mark_unwatched(
            profile_id=session.get("active_profile", "guest"),
            video_id=video_id
        )

    if not result:
        return api_error(
            error=f"Failed to mark video {video_id} as unwatched",
            status=500
        )

    return api_success(message=f"Marked video {video_id} as unwatched")


@profile_bp.route(
    "/api/profile/in_progress",
    methods=["GET", "POST", "UPDATE", "DELETE"]
)
def in_progress_videos() -> Response:
    """
    Manage in-progress videos for the active profile.

    Handles CRUD operations:
        - GET: Retrieve in-progress videos for the active profile.
            Optional 'video_id' parameter to filter by specific video.
        - POST: Add a video to the in-progress list.
        - UPDATE: Update the playback position of an in-progress video.
        - DELETE: Remove a video from the in-progress list.

    Expects JSON for POST and UPDATE requests:
        {
            "video_id": <int>,
            "current_time": <int>
        }

    Returns:
        Response: A JSON response indicating success or failure.
            Includes in-progress videos for a GET request.
    """

    method_used = request.method

    # Get the active profile from the parameter
    active_profile = request.args.get("profile", None)

    # If not provided, get from the session
    if not active_profile:
        logging.info(
            "No active_profile parameter provided, "
            "retrieving from session"
        )
        active_profile = session.get("active_profile", "guest")

    # If no active profile is set, return empty response
    if active_profile is None or active_profile == "guest":
        return api_success(
            message="No in progress videos for guest profile"
        )

    logging.info(f"Active profile for in-progress videos: {active_profile}")

    # Ensure active_profile is an integer
    try:
        active_profile = int(active_profile)
    except ValueError:
        return api_error(
            error="Invalid profile ID"
        )

    # Get one or more in progress videos
    if method_used == "GET":
        video_id = request.args.get("video_id", None)

        with LocalDbContext() as db:
            progress_mgr = ProgressManager(db)

            # Retrieve all in-progress videos for the active profile
            if video_id is None:
                in_progress_videos = progress_mgr.read(
                    profile_id=active_profile
                )

            else:
                in_progress_videos = progress_mgr.read(
                    profile_id=active_profile,
                    video_id=int(video_id)
                )

            return api_success(
                data=in_progress_videos,
                message="Retrieved in-progress videos successfully"
            )

    # Add a video to the in-progress list
    elif method_used == "POST":
        data = request.get_json()
        if not data:
            return api_error("No data provided", 400)

        video_id = data.get("video_id")
        position = data.get("current_time")

        if not video_id or not isinstance(position, int):
            return api_error(
                """
                Invalid data types for 'video_id' or 'current_time'.
                Must be integers.
                """,
                400
            )

        with LocalDbContext() as db:
            progress_mgr = ProgressManager(db)
            result = progress_mgr.create(
                profile_id=active_profile,
                video_id=video_id,
                current_time=position
            )

        if not result:
            return api_error(
                f"Failed to add in-progress video {video_id}",
                500
            )

        return api_success(
            message=(
                f"Added in-progress video {video_id} at position {position}"
            )
        )

    # Update the playback position of an in-progress video
    elif method_used == "UPDATE":
        data = request.get_json()
        if not data:
            return api_error("No data provided", 400)

        video_id = data.get("video_id")
        position = data.get("current_time")

        if not isinstance(video_id, int) or not isinstance(position, int):
            return api_error(
                """
                Invalid data types for 'video_id' or 'current_time'.
                Must be integers.
                """,
                400
            )

        with LocalDbContext() as db:
            progress_mgr = ProgressManager(db)
            result = progress_mgr.update(
                profile_id=active_profile,
                video_id=video_id,
                current_time=position
            )

        if not result:
            return api_error(
                f"Failed to update in-progress video {video_id}",
                500
            )

        return api_success(
            message=(
                f"Updated in-progress video {video_id} at position {position}"
            )
        )

    # Remove a video from the in-progress list
    elif method_used == "DELETE":
        data = request.get_json()
        if not data:
            return api_error("No data provided", 400)

        video_id = data.get("video_id")

        if video_id is None:
            return api_error(
                "Missing 'video_id' in request data",
                400
            )

        with LocalDbContext() as db:
            progress_mgr = ProgressManager(db)

            result = progress_mgr.delete(
                profile_id=active_profile,
                video_id=int(video_id)
            )

            if not result:
                return api_error(
                    f"Failed to remove in-progress video {video_id}",
                    500
                )

            return api_success(
                message="Removed in-progress videos successfully"
            )

    # Handle unsupported methods
    else:
        return api_error(
            f"Method {method_used} not allowed for this endpoint",
            405
        )
