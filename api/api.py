"""
Module: api.py

API endpoints that the browser will use to fetch additional information
    For example, the browser may use the API to find videos that belong
        to a specific category

Functions:
    - api_success: Returns a standardized success response.
    - api_error: Returns a standardized error response.

Blueprints:
    - api_metadata: Blueprint for metadata-related API endpoints.

Routes:
    - /api/scripture
        - add_scripture_text: Adds text to a scripture.

Dependencies:
    - Flask: For creating the API endpoints.
    - logging: For logging API requests and responses.
    - re: For regular expression operations.

Custom Dependencies:
    - DatabaseContext: Context manager for database connections.
    - VideoManager: Manages video-related database operations.
    - TagManager: Manages tag-related database operations.
    - SpeakerManager: Manages speaker-related database operations.
    - CharacterManager: Manages character-related database operations.
    - ScriptureManager: Manages scripture-related database operations.
    - LocalDbContext: Context manager for local database connections.
    - ProfileManager: Manages user profile-related operations in the local db.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
    request,
    jsonify,
    make_response,
)
import logging
import re

# Custom imports
from api.sql_db import (
    DatabaseContext,
    ScriptureManager,
)


metadata_bp = Blueprint(
    'api_metadata',
    __name__,
)


def api_success(
    data=None,
    message=None,
    status=200
) -> Response:
    """
    Helper to return a standardized success response.

    Note: It's best to use this for simple success responses only.
        Custom responses should be used in more complex cases.

    Args:
        data (dict, optional): Data to include in the response.
        message (str, optional): Message to include in the response.
        status (int, optional): HTTP status code for the response.

    Returns:
        Response: A JSON response with a success status.
    """

    resp = {"success": True}

    if message:
        resp["message"] = message

    if data is not None:
        resp["data"] = data

    return make_response(jsonify(resp), status)


def api_error(
    error,
    status=400
) -> Response:
    """
    Helper to return a standardized error response.

    Args:
        error (str): Error message to include in the response.
        status (int, optional): HTTP status code for the response.

    Returns:
        Response: A JSON response with an error status.
    """

    resp = {"success": False, "error": error}

    return make_response(jsonify(resp), status)


@metadata_bp.route(
    "/api/scripture",
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
            f"Failed to create scripture: {scr_name}"
        )
        return api_error(f"Failed to create scripture: {scr_name}", 500)

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
