"""
Module: api_category.py

API endpoints related to categories.

Endpoints:
    GET /api/categories/<string:category_name>
        Get the ID of a category by its name.
    GET /api/categories/<int:category_id>/<int:subcategory_id>
        Fetch videos using the given major category ID and subcategory ID.
    GET /api/categories/video/<int:video_id>
        Get the categories for a video by its ID.

Blueprints:
    category_endpoint
        Blueprint for category-related API endpoints.

Dependancies:
    flask
        Creating the API endpoints.
        Handling HTTP requests and responses.
    logging
        Logging errors and other information.

Custom Modules:
    api.api.api_error
        Utility function for returning API error responses.
    api.api.seconds_to_hhmmss
        Utility function for converting seconds to HH:MM:SS format.

    api.sql_db.DatabaseContext
        Context manager for database connections.
    api.sql_db.CategoryManager
        Manager for category-related database operations.
    api.sql_db.VideoManager
        Manager for video-related database operations.

    api.local_db.LocalDbContext
        Context manager for local database connections.
    api.local_db.ProfileManager
        Manager for profile-related local database operations.
"""

# Standard library imports
from flask import (
    Blueprint,
    Response,
    session,
)
import logging

# Custom imports
from api.api import (
    api_error,
    api_success,
    seconds_to_hhmmss,
)
from api.sql_db import (
    DatabaseContext,
    CategoryManager,
    VideoManager,
)
from api.local_db import (
    LocalDbContext,
    ProfileManager,
)


logger = logging.getLogger(__name__)

# Create a blueprint for category-related endpoints
category_endpoint = Blueprint(
    'category_endpoint',
    __name__,
    url_prefix='/api/categories',
)


@category_endpoint.route(
    "/<string:category_name>",
    methods=["GET"],
)
def get_category_id(
    category_name: str
) -> Response:
    """
    Get the ID of a category by its name.

    Args:
        category_name (str): The name of the category to look up.

    Returns:
        Response: A JSON response containing the category ID if found,
            or an error message if not found.
    """

    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        category_id = cat_mgr.name_to_id(name=category_name)

    if category_id is None:
        logger.debug("Module: api_category.py, Function: get_category_id")
        logger.error(f"Category '{category_name}' not found.")
        return api_error(
            f"Category '{category_name}' not found",
            404
        )

    return api_success(
        data={"category_id": category_id},
        message="Retrieved category successfully",
        status=200
    )


@category_endpoint.route(
    "/<int:category_id>/<int:subcategory_id>",
    methods=["GET"],
)
def category_filter(
    category_id: int,
    subcategory_id: int,
) -> Response:
    """
    Fetch videos in a category.

    Uses the given major category ID and subcategory ID.
    This is used to populate carousels with videos.

    Process:
        1. Select all videos with the given category ID and subcategory ID.
        2. If no videos are found, return a 404 error.
        3. Convert the duration from seconds to HH:MM:SS format.
        4. Return a JSON response with the list of videos.

    Args:
        category_id (int): The ID of the major category to filter videos by.
        subcategory_id (int): The ID of the subcategory to filter videos by.

    Returns:
        Response: A JSON response containing the list of videos
            in the specified category and subcategory.
        If no videos are found, an empty list is returned.
    """

    # Select all videos with the given category ID and subcategory ID
    cat_list = [category_id, subcategory_id]

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        videos = video_mgr.get_filter(
            category_id=cat_list,
        )

    # If no videos are found, just return an empty list
    if not videos:
        logger.debug("Module: api_category.py, Function: category_filter")
        logger.debug(
            f"No videos found for category_id={category_id}"
            f" and subcategory_id={subcategory_id}"
        )
        videos = []

    # Convert duration from seconds to HH:MM:SS format
    for video in videos:
        video['duration'] = seconds_to_hhmmss(video['duration'])

    # Get watch status for the active profile
    active_profile = session.get("active_profile", None)
    logger.info(f"Active profile: {active_profile}")

    if active_profile is not None and active_profile != "guest":
        with LocalDbContext() as db:
            profile_mgr = ProfileManager(db)

            for video in videos:
                watched = profile_mgr.check_watched(
                    video_id=video['id'],
                    profile_id=active_profile,
                )
                video['watched'] = watched

    # Sort videos by 'date_added' (newest first)
    videos.sort(
        key=lambda v: v.get('date_added', ''),
        reverse=True
    )

    return api_success(
        data={"videos": videos},
        message="Retrieved videos successfully",
        status=200
    )


@category_endpoint.route(
    "/video/<int:video_id>",
    methods=["GET"],
)
def get_video_categories(
    video_id: int
) -> Response:
    """
    Get the categories for a video by its ID.

    Args:
        video_id (int): The ID of the video to retrieve categories for.

    Returns:
        Response: A JSON response containing the list of categories,
            or an error message if the video is not found.
    """

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        category_mgr = CategoryManager(db)

        # Check if the video exists
        video_list = video_mgr.get(id=video_id)

        if not video_list:
            logger.debug(
                "Module: api_category.py, Function: get_video_categories"
            )
            logger.warning(f"Video with ID {video_id} not found.")

            return api_error(
                f"Video with ID {video_id} not found",
                404
            )

        # Get the categories for the video
        categories = category_mgr.get_from_video(
            video_id=video_id
        )
        if categories is None or categories == []:
            logger.debug(
                "Module: api_category.py, Function: get_video_categories"
            )
            logger.debug(f"No categories found for video ID {video_id}.")

        return api_success(
            data=categories,
            message="Retrieved categories successfully",
            status=200
        )
