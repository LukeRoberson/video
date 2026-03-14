"""
Module: api_tag.py

API endpoints related to tags.

Endpoints:
    GET /api/tags
        Get a list of all tags.
    GET /api/tags/<int:tag_id>
        Get a tag by its ID.
    GET /api/tags/video/<int:video_id>
        Get the tags for a video by its ID.

Blueprints:
    tag_endpoint

Dependancies:
    flask
        Creating the API endpoints.
        Handling HTTP requests and responses.

Custom Modules:
    api.api.api_error
        Utility function for returning API error responses.

    api.sql_db.DatabaseContext
        Context manager for database connections.
    api.sql_db.VideoManager
        Manager for video-related database operations.
    api.sql_db.TagManager
        Manager for tag-related database operations.
"""

# Standard library imports
from flask import (
    Blueprint,
    Response,
)
import logging

# Custom imports
from api.api import (
    api_error,
    api_success,
)
from api.sql_db import (
    DatabaseContext,
    VideoManager,
    TagManager,
)


logger = logging.getLogger(__name__)

# Create a blueprint for tag-related endpoints
tag_endpoint = Blueprint(
    'tag_endpoint',
    __name__
)


@tag_endpoint.route(
    "/api/tags",
    methods=["GET"],
)
def get_tags() -> Response:
    """
    Get a list of all tags.

    Returns:
        Response: A JSON response containing a list of all tags.
    """

    with DatabaseContext() as db:
        tag_mgr = TagManager(db)
        video_mgr = VideoManager(db)

        # Get all tags
        tags = tag_mgr.get() or []

        if not tags:
            logger.debug("Module: api_tag.py, Function: get_tags")
            logger.error("Error retrieving tags from database")

            return api_error(
                error="Error retrieving tags from database",
                status=500
            )

        if tags == []:
            logger.debug("Module: api_tag.py, Function: get_tags")
            logger.debug("No tags found in database")

        else:
            # Get the video count for each tag
            for tag in tags:
                videos = video_mgr.get_filter(tag_id=tag['id'])
                tag['video_count'] = len(videos) if videos else 0

            # Sort tags alphabetically by name (case-insensitive)
            tags = sorted(
                tags, key=lambda tag: tag.get('name', '').lower()
            )

    return api_success(
        data=tags,
        message="Tags retrieved successfully",
        status=200
    )


@tag_endpoint.route(
    "/api/tags/<int:tag_id>",
    methods=["GET"],
)
def get_tag(
    tag_id: int
) -> Response:
    """
    Get a tag by its ID.

    Args:
        tag_id (int): The ID of the tag to retrieve.

    Returns:
        Response: A JSON response containing the tag details if found,
            or an error message if not found.
    """

    with DatabaseContext() as db:
        tag_mgr = TagManager(db)

        tag_list = tag_mgr.get(id=tag_id)
        if not tag_list:
            logger.debug("Module: api_tag.py, Function: get_tag")
            logger.error(f"Tag with ID {tag_id} not found in database")

            return api_error(
                error=f"Tag with ID {tag_id} not found",
                status=404
            )

    return api_success(
        data=tag_list[0],
        message="Tag retrieved successfully",
        status=200
    )


@tag_endpoint.route(
    "/api/tags/video/<int:video_id>",
    methods=["GET"],
)
def get_video_tags(
    video_id: int
) -> Response:
    """
    Get the tags for a video by its ID.

    Args:
        video_id (int): The ID of the video to retrieve tags for.

    Returns:
        Response: A JSON response containing the list of tags,
            or an error message if the video is not found.
    """

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        tag_mgr = TagManager(db)

        # Check if the video exists
        video_list = video_mgr.get(id=video_id)
        if not video_list:
            logger.debug("Module: api_tag.py, Function: get_video_tags")
            logger.error(f"Video with ID {video_id} not found in database")

            return api_error(
                error=f"Video with ID {video_id} not found",
                status=404
            )

        # Get the tags for the video
        tags = tag_mgr.get_from_video(
            video_id=video_id
        )

        if tags is None:
            logger.debug("Module: api_tag.py, Function: get_video_tags")
            logger.error(f"Error retrieving tags for video with ID {video_id}")

            return api_error(
                error=f"Error retrieving tags for video with ID {video_id}",
                status=500
            )

        if tags == []:
            logger.debug("Module: api_tag.py, Function: get_video_tags")
            logger.debug(f"No tags found for video with ID {video_id}")

    return api_success(
        data=tags,
        message="Tags retrieved successfully",
        status=200
    )
