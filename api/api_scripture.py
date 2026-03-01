"""
Module: api_scripture.py

API endpoints related to scriptures.

Endpoints:
    GET /api/scriptures
        Get a list of all scriptures.
    GET /api/scriptures/video/<int:video_id>
        Get the scriptures for a video by its ID.
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
    make_response,
    jsonify,
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

    Returns:
        Response: A JSON response containing a list of all scriptures.
    """

    with DatabaseContext() as db:
        scripture_mgr = ScriptureManager(db)

        scriptures = scripture_mgr.get() or []

    return make_response(
        jsonify(
            scriptures,
        ),
        200
    )


@scripture_endpoint.route(
    "/<int:scripture_id>",
    methods=["GET"],
)
def get_scripture(
    scripture_id: int
) -> Response:
    """
    Get a scripture by its ID.

    Args:
        scripture_id (int): The ID of the scripture to retrieve.

    Returns:
        Response: A JSON response containing the scripture details if found,
            or an error message if not found.
    """

    with DatabaseContext() as db:
        scripture_mgr = ScriptureManager(db)

        scripture_list = scripture_mgr.get(id=scripture_id)
        if not scripture_list:
            return api_error(
                f"Scripture with ID {scripture_id} not found",
                404
            )

    return make_response(
        jsonify(
            scripture_list[0],
        ),
        200
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
            return api_error(
                f"Video with ID {video_id} not found",
                404
            )

        # Get the scriptures for the video
        scriptures = scripture_mgr.get_from_video(
            video_id=video_id
        )

        return make_response(
            jsonify(
                scriptures,
            ),
            200
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
        logging.error("No data provided for adding scripture text.")
        return api_error("No data provided", 400)

    scr_name = data.get("scr_name")
    scr_text = data.get("scr_text")

    if not scr_name or not scr_text:
        logging.error("Missing 'scr_name' or 'scr_text' in request data.")
        return api_error(
            "Missing 'scr_name' or 'scr_text' in request data",
            400
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
        logging.error(
            f"Failed to add scripture text: {scr_name}"
        )
        return api_error(f"Failed to add scripture text: {scr_name}", 500)

    # Add the scripture text to the database
    logging.info(
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
        logging.error(f"Failed to add scripture text for '{scr_name}'.")
        return api_error(f"Failed to add scripture text for '{scr_name}'", 500)

    logging.info(f"Successfully added scripture text for '{scr_name}'.")

    return api_success(
        message=f"Added scripture text for '{scr_name}'"
    )
