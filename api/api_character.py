"""
Module: api_character.py

API endpoints related to characters.

Endpoints:
    GET /api/characters
        Get a list of one or all characters.
    GET /api/characters/video/<int:video_id>
        Get the characters for a video by its ID.

Blueprints:
    character_endpoint

Dependancies:
    flask
        Creating the API endpoints.
        Handling HTTP requests and responses.
    logging
        Logging errors and information for debugging and monitoring.

Custom Modules:
    api.api.api_error
        Utility function for returning API error responses.

    api.sql_db.DatabaseContext:
        A context manager for database connections.
    api.sql_db.CharacterManager:
        A class for managing character records in the database.
    api.sql_db.VideoManager:
        A class for managing video records in the database.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
    request,
)
import logging

# Local imports
from api.api import (
    api_error,
    api_success,
)
from api.sql_db import (
    DatabaseContext,
    CharacterManager,
    VideoManager,
)


logger = logging.getLogger(__name__)

# Create a blueprint for character-related endpoints
character_endpoint = Blueprint(
    'character_endpoint',
    __name__,
    url_prefix='/api/characters'
)


@character_endpoint.route(
    "",
    methods=["GET"],
)
def get_characters() -> Response:
    """
    Get a list of one or all characters.

    Optional Query Parameters:
        char_id (int): Get a character by their ID.

    Returns:
        Response: A JSON response containing a list of characters.
    """

    char_id = request.args.get("char_id", type=int)

    with DatabaseContext() as db:
        character_mgr = CharacterManager(db)
        characters = (
            character_mgr.get(id=char_id) if char_id
            else character_mgr.get()
            or []
        )

    # Handle errors
    if characters is None:
        logger.debug("Module: api_character.py, Function: get_characters")
        logger.warning("Error retrieving characters from the database.")
        return api_error(
            error="Error retrieving characters from the database",
            status=500
        )

    # Handle empty results
    elif characters == []:
        logger.debug("Module: api_character.py, Function: get_characters")
        logger.debug("No characters found in the database.")

    else:
        # Sort characters alphabetically by name (case-insensitive)
        characters = sorted(
            characters,
            key=lambda char: char.get('name', '').lower()
        )

    return api_success(
        data=characters,
        message=f"Retrieved {len(characters)} characters",
        status=200
    )


@character_endpoint.route(
    "/video/<int:video_id>",
    methods=["GET"],
)
def get_video_characters(
    video_id: int
) -> Response:
    """
    Get the characters for a video by its ID.

    Args:
        video_id (int): The ID of the video to retrieve characters for.

    Returns:
        Response: A JSON response containing the list of characters,
            or an error message if the video is not found.
    """

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        character_mgr = CharacterManager(db)

        # Check if the video exists
        video_list = video_mgr.get(id=video_id)
        if not video_list:
            logger.debug(
                "Module: api_character.py, Function: get_video_characters"
            )
            logger.warning(f"Video with ID {video_id} not found.")
            return api_error(
                f"Video with ID {video_id} not found",
                404
            )

        # Get the characters for the video
        characters = character_mgr.get_from_video(
            video_id=video_id
        )

        if characters is None:
            logger.debug(
                "Module: api_character.py, Function: get_video_characters"
            )
            logger.warning(f"No characters found for video ID {video_id}.")

            return api_error(
                error="Error retrieving characters for video ID",
                status=500
            )

    return api_success(
        data=characters,
        message=f"Retrieved characters for video ID {video_id}",
        status=200
    )
