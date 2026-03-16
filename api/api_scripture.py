"""
Module: api_scripture.py

API endpoints related to scriptures.

Endpoints:
    GET /api/scriptures
        Get a list of all scriptures.
    GET /api/scriptures/<int:scripture_id>
        Get a scripture by its ID.
    POST /api/scriptures
        Add text to a scripture.

Blueprints:
    scripture_endpoint

Dependancies:
    flask
        Creating the API endpoints.
        Handling HTTP requests and responses.
    logging
        Logging errors and information for debugging and monitoring.
    re
        Parsing scripture references from the input.

Custom Modules:
    api.api.api_error
        Utility function for returning API error responses.
    api.api.api_success
        Utility function for returning API success responses.

    api.sql_db.DatabaseContext:
        A context manager for database connections.
    api.sql_db.ScriptureManager:
        A class for managing scripture records in the database.
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
import re

# Local imports
from api.api import (
    api_error,
    api_success,
)
from api.sql_db import (
    DatabaseContext,
    ScriptureManager,
    VideoManager,
)


logger = logging.getLogger(__name__)

# Create a blueprint for scripture-related endpoints
scripture_endpoint = Blueprint(
    'scripture_endpoint',
    __name__,
    url_prefix='/api/scriptures'
)


@scripture_endpoint.route(
    "",
    methods=["GET"],
)
def get_scriptures() -> Response:
    """
    Get a list of all scriptures.

    Optional query parameters:
        scr_id (int): Filter by scripture ID.

    Returns:
        Response: A JSON response containing a list of all scriptures.
    """

    scripture_id = request.args.get("scr_id", None, type=int)

    with DatabaseContext() as db:
        scripture_mgr = ScriptureManager(db)
        scriptures = (
            scripture_mgr.get(id=scripture_id) if scripture_id
            else scripture_mgr.get()
            or []
        )

    if scriptures is None:
        logger.debug("Module: api_scripture.py, Function: get_scriptures")
        logger.error("Failed to retrieve scriptures from the database.")

        return api_error(
            error="Failed to retrieve scriptures",
            status=500
        )

    if scriptures == []:
        logger.debug("Module: api_scripture.py, Function: get_scriptures")
        logger.debug("No scriptures found in the database.")

    return api_success(
        data=scriptures,
        message=f"Retrieved {len(scriptures)} scriptures",
        status=200
    )


@scripture_endpoint.route(
    "/video/<int:video_id>",
    methods=["GET"],
)
def get_video_scriptures(
    video_id: int
) -> Response:
    """
    Get the scriptures for a video by its ID.

    Args:
        video_id (int): The ID of the video to retrieve scriptures for.

    Returns:
        Response: A JSON response containing the list of scriptures,
            or an error message if the video is not found.
    """

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        scripture_mgr = ScriptureManager(db)

        # Check if the video exists
        video_list = video_mgr.get(id=video_id)
        if not video_list:
            logger.debug(
                "Module: api_scripture.py, Function: get_video_scriptures"
            )
            logger.error(
                f"Video with ID {video_id} not found in the database."
            )

            return api_error(
                f"Video with ID {video_id} not found",
                404
            )

        # Get the scriptures for the video
        scriptures = scripture_mgr.get_from_video(
            video_id=video_id
        )

        if scriptures is None:
            logger.debug(
                "Module: api_scripture.py, Function: get_video_scriptures"
            )
            logger.error(
                f"Failed to retrieve scriptures for video ID {video_id}"
                f" from the database."
            )

            return api_error(
                error=f"Failed to retrieve scriptures for video ID {video_id}",
                status=500
            )

        if scriptures == []:
            logger.debug(
                "Module: api_scripture.py, Function: get_video_scriptures"
            )
            logger.debug(
                f"No scriptures found for video ID {video_id} in the database."
            )

        return api_success(
            data=scriptures,
            message=f"Retrieved scriptures for video ID {video_id}",
            status=200
        )


@scripture_endpoint.route(
    "",
    methods=["POST"],
)
def add_scripture_text() -> Response:
    """
    Add text to a scripture.

    Expects JSON:
        {
            "scr_name": "<scripture name>",
            "scr_text": "<scripture text>"
        }

    Returns:
        Response: A JSON response indicating success or failure.
    """

    # Get the JSON data from the request
    data = request.get_json()
    if not data:
        logger.debug("Module: api_scripture.py, Function: add_scripture_text")
        logger.error("No data provided for adding scripture text.")

        return api_error(
            error="No data provided",
            status=400
        )

    scr_name = data.get("scr_name", None)
    scr_text = data.get("scr_text", None)

    if not scr_name or not scr_text:
        logger.debug("Module: api_scripture.py, Function: add_scripture_text")
        logger.error("Missing 'scr_name' or 'scr_text' in request data.")

        return api_error(
            error="Missing 'scr_name' or 'scr_text' in request data",
            status=400
        )

    # Get the book, chapter, and verse from the scripture name
    match = re.match(
        r"""
        (?P<book>          # Match the book name
            (?:\d\s*)?     # Match a number then whitespace
            \w[\w\s]*?     # Match word characters and spaces
        )
        \s+                # Match one or more spaces
        (?P<chapter>\d+)   # Match the chapter number (digits)
        :                  # Match the colon separator
        (?P<verse>\d+)     # Match the verse number (digits)
        """,
        scr_name,
        re.X               # Enable verbose mode
    )

    if match:
        book = match.group('book').strip()
        chapter = int(match.group('chapter'))
        verse = int(match.group('verse'))
    else:
        book = chapter = verse = None

    if book is None or chapter is None or verse is None:
        logger.debug("Module: api_scripture.py, Function: add_scripture_text")
        logger.error(
            f"Scripture reference '{scr_name}' is not valid. Skipping."
        )

        return api_error(
            f"Scripture reference '{scr_name}' is not valid. Skipping",
            400
        )

    # Get the scripture ID from the database
    with DatabaseContext() as db:
        scripture_mgr = ScriptureManager(db)

        # Check if the scripture already exists
        scr_id = scripture_mgr.name_to_id(
            book=book,
            chapter=chapter,
            verse=verse,
        )

    if scr_id is None:
        logger.debug("Module: api_scripture.py, Function: add_scripture_text")
        logger.error(
            f"Failed to add scripture text: {scr_name}"
        )

        return api_error(
            error=f"Failed to add scripture text: {scr_name}",
            status=500
        )

    # Add the scripture text to the database
    logger.debug(
        f"Adding scripture text for {book} {chapter}:{verse} "
        f"(ID: {scr_id}) with text: '{scr_text}'"
    )

    with DatabaseContext() as db:
        scripture_mgr = ScriptureManager(db)
        result = scripture_mgr.update(
            id=scr_id,
            text=scr_text,
        )

    if not result:
        logger.debug("Module: api_scripture.py, Function: add_scripture_text")
        logger.error(f"Failed to add scripture text for '{scr_name}'.")

        return api_error(
            error=f"Failed to add scripture text for '{scr_name}'",
            status=500
        )

    return api_success(
        message=f"Added scripture text for '{scr_name}'",
        status=200
    )
