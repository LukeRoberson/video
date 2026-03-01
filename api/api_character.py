"""
Module: api_character.py

API endpoints related to characters.

Endpoints:
    GET /api/characters
        Get a list of all characters.
    GET /api/characters/<int:character_id>
        Get a character by its ID.
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
    make_response,
    jsonify,
)

# Local imports
from api.api import (
    api_error,
)
from api.sql_db import (
    DatabaseContext,
    CharacterManager,
    VideoManager,
)


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
    Get a list of all characters.

    Returns:
        Response: A JSON response containing a list of all characters.
    """

    with DatabaseContext() as db:
        character_mgr = CharacterManager(db)

        characters = character_mgr.get() or []

    # Sort characters alphabetically by name (case-insensitive)
    characters = sorted(
        characters, key=lambda char: char.get('name', '').lower()
    )

    return make_response(
        jsonify(
            characters,
        ),
        200
    )


@character_endpoint.route(
    "/<int:character_id>",
    methods=["GET"],
)
def get_character(
    character_id: int
) -> Response:
    """
    Get a character by its ID.

    Args:
        character_id (int): The ID of the character to retrieve.

    Returns:
        Response: A JSON response containing the character details if found,
            or an error message if not found.
    """

    with DatabaseContext() as db:
        character_mgr = CharacterManager(db)

        character_list = character_mgr.get(id=character_id)
        if not character_list:
            return api_error(
                f"Character with ID {character_id} not found",
                404
            )

    return make_response(
        jsonify(
            character_list[0],
        ),
        200
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
            return api_error(
                f"Video with ID {video_id} not found",
                404
            )

        # Get the characters for the video
        characters = character_mgr.get_from_video(
            video_id=video_id
        )

        return make_response(
            jsonify(
                characters,
            ),
            200
        )
