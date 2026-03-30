"""
Module: profile_api.py

API endpoints that the browser will use to fetch additional information
    Specifically, for user profiles and their management.

Blueprints:
    api_profile

Endpoints:
    GET /api/profile
        Retrieves a list of all user profiles.
    GET /api/profile/<profile_id>
        Retrieves a specific user profile by ID.
    POST /api/profile/create
        Creates a new user profile with the provided name and image.
    DELETE /api/profile/delete/<profile_id>
        Deletes a user profile by ID.
    POST /api/profile/update/<profile_id>
        Updates a user profile's name and/or image by ID.

    POST /api/profile/set_active
        Sets the active profile for the session.
    GET /api/profile/get_active
        Retrieves the active profile for the session.

    GET /api/profile/watch_history
        Retrieves the watch history for the active profile.
    POST /api/profile/clear_history/<profile_id>
        Clears the watch history for a user profile by ID.
    GET/POST/UPDATE/DELETE /api/profile/in_progress
        Manages in-progress video tracking for user profiles.

    GET /api/profile/mark_watched
        Checks if a video is marked as watched for the active profile.
    POST /api/profile/mark_watched_bulk
        Checks watched status for multiple videos for the active profile.
    POST /api/profile/mark_watched
        Marks a video as watched for the active profile.
    POST /api/profile/mark_unwatched
        Marks a video as unwatched for the active profile.

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
from api.sql_db import (
    DatabaseContext,
    VideoManager,
)


logger = logging.getLogger(__name__)

# Blueprint for user profile API endpoints
profile_bp = Blueprint(
    'api_profile',
    __name__,
)


@profile_bp.route(
    '/api/profile',
    methods=['GET'],
)
def get_profile_list() -> Response:
    """
    Get all user profiles.

    Args:
        None

    Returns:
        Response: A JSON response with the list of user profiles.
    """

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile_list = profile_mgr.read()

    return api_success(
        profile_list
    )


@profile_bp.route(
    '/api/profile/<int:profile_id>',
    methods=['GET'],
)
def get_profile(profile_id: int) -> Response:
    """
    Get a user profile by ID.

    Args:
        profile_id (int): The ID of the profile to retrieve.

    Returns:
        Response: A JSON response with the user profile data.
    """

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile = profile_mgr.read(profile_id)

    if not profile:
        logger.debug("Module: api_profile.py, Function: get_profile")
        logger.error(f"Profile with ID {profile_id} not found.")
        return api_error(f"Profile with ID {profile_id} not found", 404)

    return api_success(
        data=profile[0]
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
    "/api/profile/watch_history",
    methods=["GET"]
)
def get_watch_history() -> Response:
    """
    Get the watch history for the active profile.

    Returns:
        Response: JSON; The watch history for the active profile.
    """

    # Get the active profile from the parameter
    active_profile = request.args.get(
        "profile",
        None
    )

    # If no active profile is set, return empty response
    if active_profile is None or active_profile == "guest":
        return api_success(
            message="No watch history for guest profile"
        )

    # Check the profile exists in the database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile = profile_mgr.read(profile_id=int(active_profile))

    if not profile:
        logging.error(f"Profile with ID {active_profile} not found.")
        return api_error(f"Profile with ID {active_profile} not found", 404)

    # Retrieve the watch history for the active profile
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        watch_history = profile_mgr.read_watch_history(
            profile_id=int(active_profile)
        )

    # Remove the 'id' field from each item in watch_history
    if isinstance(watch_history, list):
        for item in watch_history:
            item.pop('id', None)

    return api_success(
        data=watch_history,
        message="Retrieved watch history successfully"
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
    "/api/profile/in_progress",
    methods=["GET", "POST", "DELETE"]
)
def in_progress_videos() -> Response:
    """
    Manage in-progress videos for the active profile.

    Handles CRUD operations:
        - GET: Retrieve in-progress videos for the active profile.
            Optional 'video_id' parameter to filter by specific video.
        - POST: Add a video to the in-progress list.
        - DELETE: Remove a video from the in-progress list.

    Parameters:
        profile (int): The ID of the profile to manage in-progress videos for.
        video_id (int, optional): The ID of the video to filter by (for GET)

    Expects JSON for POST requests:
        {
            "video_id": <int>,
            "current_time": <int>
        }

    Expects JSON for DELETE requests:
        {
            "video_id": <int>
        }

    Returns:
        Response: A JSON response indicating success or failure.
            Includes in-progress videos for a GET request.
    """

    method_used = request.method

    # Get the active profile from the parameter
    active_profile = request.args.get(
        "profile",
        None,
        type=int
    )

    # Check that the active profile parameter is provided
    if not active_profile:
        logger.debug("Module: api_profile.py, Function: in_progress_videos")
        logger.warning("No active_profile parameter provided")

        return api_error(
            error="Missing 'profile' parameter in request",
            status=400
        )

    # Check that the profile exists in the database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile = profile_mgr.read(active_profile)

    if not profile:
        return api_error(
            error="Profile not found",
            status=404
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
                data=in_progress_videos or [],
                message="Retrieved in-progress videos successfully",
                status=200
            )

    # Add a video to the in-progress list
    elif method_used == "POST":
        data = request.get_json()
        if not data:
            return api_error(
                error="No data provided",
                status=400
            )

        video_id = data.get("video_id", None)
        position = data.get("current_time", None)

        # Check that video_id and position are provided
        if video_id is None or position is None:
            logger.debug(
                "Module: api_profile.py, Function: in_progress_videos (POST)"
            )
            logger.warning(
                "Missing 'video_id' or 'current_time' in request data"
            )

            return api_error(
                error="Missing 'video_id' or 'current_time' in request data",
                status=400
            )

        # Check that the video_id and position are of the correct type
        if not isinstance(video_id, int) or not isinstance(position, int):
            logger.debug(
                "Module: api_profile.py, Function: in_progress_videos (POST)"
            )
            logger.warning(
                """
                Invalid data types for 'video_id' or 'current_time'."
                Must be integers.
                """
            )

            return api_error(
                error="Invalid data types. Must be integers",
                status=400
            )

        # Check that the video exists in the database
        with DatabaseContext() as db:
            video_mgr = VideoManager(db)
            video = video_mgr.get(video_id)

            if video is None:
                logger.debug(
                    """
                    Module: api_profile.py, Function: in_progress_videos (POST)
                    """
                )
                logger.warning(f"Video with ID {video_id} not found")

                return api_error(
                    error=f"Video with ID {video_id} not found",
                    status=404
                )

        # Add the video to the in-progress list for the profile
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
            ),
            status=201
        )

    # Remove a video from the in-progress list
    elif method_used == "DELETE":
        data = request.get_json()

        # Handle missing JSON body
        if not data:
            logger.debug(
                "Module: api_profile.py, Function: in_progress_videos (DELETE)"
            )
            logger.warning("No data provided for deleting in-progress video")

            return api_error(
                error="No data provided",
                status=400
            )

        # Get the video ID
        video_id = data.get("video_id", None)

        # Check that the video_id is provided
        if video_id is None:
            logger.debug(
                "Module: api_profile.py, Function: in_progress_videos (DELETE)"
            )
            logger.warning("Missing 'video_id' in request data for deletion")

            return api_error(
                error="Missing 'video_id' in request data",
                status=400
            )

        # Check that the video_id is of the correct type
        if not isinstance(video_id, int):
            logger.debug(
                "Module: api_profile.py, Function: in_progress_videos (DELETE)"
            )
            logger.warning("Invalid data type for 'video_id'. Must be integer")

            return api_error(
                error="Invalid data type for 'video_id'. Must be integer",
                status=400
            )

        with LocalDbContext() as db:
            progress_mgr = ProgressManager(db)

            result = progress_mgr.delete(
                profile_id=active_profile,
                video_id=int(video_id)
            )

            if not result:
                logger.debug(
                    "Module: api_profile.py, Function: in_progress_videos"
                )
                logger.warning(
                    f"Failed to remove in-progress video {video_id}"
                )

                return api_error(
                    error=f"Failed to remove in-progress video {video_id}",
                    status=500
                )

            return api_success(
                message="Removed in-progress videos successfully"
            )

    else:
        return api_error(
            error="Method not allowed",
            status=405
        )


@profile_bp.route(
    "/api/profile/mark_watched",
    methods=["GET"]
)
def get_watched() -> Response:
    """
    Check if a specific video is marked as watched for the active profile.

    Request Args:
        video_id (int):
            The ID of the video to check watched status for.
        profile (int):
            The ID of the profile to check watched status for.

    Returns:
        Response: A JSON response with the watched status of the video.
    """

    # Get the active profile from the parameter
    active_profile = request.args.get("profile", None)

    # If no active profile is set, return empty response
    if active_profile is None or active_profile == "guest":
        return api_success(
            message="No in progress videos for guest profile"
        )

    # Check the profile exists in the database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile = profile_mgr.read(profile_id=int(active_profile))

    if not profile:
        logging.error(f"Profile with ID {active_profile} not found.")
        return api_error(f"Profile with ID {active_profile} not found", 404)

    # Get the video ID from the request arguments
    video = request.args.get("video_id", None)
    if not video:
        return api_error(error="Missing 'video_id' in request data")
    video = int(video)

    # Check the video exists in the database
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        video_id = video_mgr.get(video)

        # Error if the video ID is not found in the database
        if video_id is None or len(video_id) == 0:
            logging.error(f"Video with ID {video} not found.")
            return api_error(f"Video with ID {video} not found", 404)

    # Check that the video is in the watch history for the active profile
    with LocalDbContext() as local_db:
        profile_mgr = ProfileManager(local_db)

        watched = profile_mgr.check_watched(
            profile_id=int(active_profile),
            video_id=video
        )

    return api_success(
        data={
            "video_id": video,
            "watched": watched
        }
    )


@profile_bp.route(
    "/api/profile/mark_watched_bulk",
    methods=["POST"]
)
def check_watched_bulk() -> Response:
    """
    Check watched status for multiple videos at once.

    Expects JSON:
        {
            "video_ids": [<int>, <int>, ...]
        }

    Returns:
        Response: A JSON response with watched status for each video.
            Example: {"1": true, "2": false, "3": true}
    """

    # Check the active profile from the parameter
    active_profile = request.args.get("profile", None)

    # Handle the guest profile
    if active_profile is None or active_profile == "guest":
        return api_success(message="No watched videos for guest profile")

    # Check the profile exists in the database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile = profile_mgr.read(profile_id=int(active_profile))

    if not profile:
        logging.error(f"Profile with ID {active_profile} not found.")
        return api_error(f"Profile with ID {active_profile} not found", 404)

    # Get the body of the request and validate it
    data = request.get_json()
    if not data or "video_ids" not in data:
        return api_error(error="Missing 'video_ids' in request data")

    # Get the list of video IDs and validate it
    video_ids = data.get("video_ids", [])
    if not isinstance(video_ids, list):
        return api_error(error="'video_ids' must be a list")

    # Check the watched status for each video ID
    with LocalDbContext() as local_db:
        profile_mgr = ProfileManager(local_db)
        watched_status = {}

        for video_id in video_ids:
            watched = profile_mgr.check_watched(
                profile_id=int(active_profile),
                video_id=int(video_id)
            )
            watched_status[str(video_id)] = watched

    return api_success(
        data=watched_status,
        message="Successfully checked watched status"
    )


@profile_bp.route(
    "/api/profile/mark_watched",
    methods=["POST"]
)
def mark_watched() -> Response:
    """
    Mark a video as watched for the active profile.

    Expects the profile ID as a query parameter

    Expects JSON:
        {
            "video_id": <int>
        }

    Returns:
        Response: A JSON response indicating success or failure.
    """

    # Get the active profile from the parameter
    active_profile = request.args.get("profile", None)

    # Handle the guest profile
    if active_profile is None or active_profile == "guest":
        return api_success(message="No watched videos for guest profile")

    # Check the profile exists in the database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile = profile_mgr.read(profile_id=int(active_profile))

    if not profile:
        logging.error(f"Profile with ID {active_profile} not found.")
        return api_error(f"Profile with ID {active_profile} not found", 404)

    # Get the body of the request and validate it
    data = request.get_json()
    video_id = data.get("video_id", None)

    if not video_id:
        logger.debug("Module: api_profile.py, Function: mark_watched")
        logger.warning(
            "Missing 'video_id' in request data for marking watched"
        )
        return api_error(
            error="Missing 'video_id' in request data"
        )

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        progress_mgr = ProgressManager(db)

        # Mark the video as watched for the active profile
        result = profile_mgr.mark_watched(
            profile_id=int(active_profile),
            video_id=int(video_id)
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

    Request Args:
        profile (int):
            The ID of the profile to check watched status for.

    Expects JSON:
        {
            "video_id": <int>
        }

    Returns:
        Response: A JSON response indicating success or failure.
    """

    logging.debug("Received request to mark video as unwatched")

    # Get the active profile from the parameter
    active_profile = request.args.get("profile", None)

    if active_profile is None or active_profile == "guest":
        logging.debug("No active profile set, cannot mark video as unwatched")
        return api_error(
            error="No active profile set, cannot mark video as unwatched",
            status=400
        )

    # Check the profile exists in the database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile = profile_mgr.read(profile_id=int(active_profile))

    if not profile:
        logging.error(f"Profile with ID {active_profile} not found.")
        return api_error(
            error=f"Profile with ID {active_profile} not found",
            status=404
        )

    # Get the body of the request and validate it
    data = request.get_json()
    video_id = data.get("video_id", None)

    if not video_id:
        return api_error(
            error="Missing 'video_id' in request data",
            status=400
        )

    logging.info(
        f"Marking video {video_id} as unwatched "
        f"for profile {active_profile}"
    )

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        result = profile_mgr.mark_unwatched(
            profile_id=int(active_profile),
            video_id=video_id
        )

    if not result:
        return api_error(
            error=f"Failed to mark video {video_id} as unwatched",
            status=500
        )

    return api_success(message=f"Marked video {video_id} as unwatched")
