"""
Module: profile_api.py

API endpoints that the browser will use to fetch additional information
    Specifically, for user profiles and their management.

Routes:
    - /api/profile/in_progress
        - in_progress_videos: Manages in-progress videos for the profile.
    - /api/profile/pictures
        - get_profile_pictures: Retrieves available profile pictures.

Dependencies:
    - Flask: For creating the API endpoints.

Custom Dependencies:
    - LocalDbContext: Context manager for local database connections.
    - ProgressManager: Manages in-progress video tracking for user profiles.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
    request,
    session,
    current_app,
    jsonify,
)
import os

# Custom imports
from app.api import (
    api_error,
    api_success,
)
from app.local_db import (
    LocalDbContext,
    ProgressManager,
)


profile_api_bp = Blueprint(
    'profile_api',
    __name__,
)


@profile_api_bp.route(
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

    # Get the active profile from the session
    active_profile = session.get("active_profile", "guest")
    if active_profile is None or active_profile == "guest":
        return api_success(
            message="No in progress videos for guest profile"
        )

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


@profile_api_bp.route(
    '/api/profile/pictures'
)
def get_profile_pictures():
    """Get list of available profile pictures"""
    try:
        # Get list of profile picture files from your static directory
        static_folder = current_app.static_folder
        if not static_folder:
            return jsonify({'error': 'Static folder not configured'}), 500

        profile_pics_dir = os.path.join(static_folder, 'img', 'profiles')
        profile_pics = []

        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.lower().endswith((
                    '.png', '.jpg', '.jpeg', '.gif', '.webp'
                )):
                    profile_pics.append(filename)

        return jsonify({'profile_pics': sorted(profile_pics)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
