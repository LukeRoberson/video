"""
Module: api.py

API endpoints that the browser will use to fetch additional information
    For example, the browser may use the API to find videos that belong
        to a specific category

Functions:
    - seconds_to_hhmmss: Converts seconds to HH:MM:SS format.

Routes:
    - /api/categories/<int>/<int>
        - category_filter: Fetches videos by category and subcategory IDs.
    - /api/profile/create
        - create_profile: Creates a new user profile.

Dependencies:
    - Flask: For creating the API endpoints.
    - logging: For logging API requests and responses.

Custom Dependencies:
    - DatabaseContext: Context manager for database connections.
    - VideoManager: Manages video-related database operations.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
    request,
    session,
    jsonify,
    make_response,
)
import logging

# Custom imports
from sql_db import (
    DatabaseContext,
    VideoManager,
    TagManager,
    SpeakerManager,
    CharacterManager,
)
from local_db import (
    LocalDbContext,
    ProfileManager,
)


def seconds_to_hhmmss(
    seconds: int,
) -> str:
    """
    Convert seconds to HH:MM:SS format.
        Shows hours only if greater than zero.

    Args:
        seconds (int): Duration in seconds.

    Returns:
        str: Duration in HH:MM:SS or MM:SS format.
    """

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    # Format the output based on whether hours are present
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    return f"{minutes}:{seconds:02}"


api_bp = Blueprint(
    'api',
    __name__,
)


@api_bp.route(
    "/api/categories/<int:category_id>/<int:subcategory_id>",
    methods=["GET"],
)
def category_filter(
    category_id: int,
    subcategory_id: int,
) -> Response:
    """
    Fetch videos with the given major category ID and subcategory ID.
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

    logging.info(
        f"Fetching videos for Category ID: {category_id}, "
        f"Subcategory ID: {subcategory_id}"
    )

    # Select all videos with the given category ID and subcategory ID
    cat_list = [category_id, subcategory_id]
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        videos = video_mgr.get_filter(
            category_id=cat_list,
        )

    if videos:
        logging.info(
            f"Found {len(videos)} videos for Category ID: {category_id}, "
            f"Subcategory ID: {subcategory_id}"
        )

    # If no videos are found, return a 404 error
    if not videos:
        videos = []

    # Convert duration from seconds to HH:MM:SS format
    for video in videos:
        video['duration'] = seconds_to_hhmmss(video['duration'])

    return jsonify(videos)


@api_bp.route(
    '/api/profile/create',
    methods=['POST'],
)
def create_profile() -> Response:
    """
    Endpoint to create a new user profile.
    This is a placeholder for future implementation.

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
        return make_response(
            jsonify(
                {
                    'error': 'No data provided'
                }
            ),
            400
        )

    if 'name' not in data or 'image' not in data:
        logging.error("Missing required fields for profile creation.")
        return make_response(
            jsonify(
                {
                    'error': 'Missing required fields: name and image'
                }
            ),
            400
        )

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
        return make_response(
            jsonify(
                {
                    'error': 'Failed to create profile'
                }
            ),
            500
        )

    # Return the response with the created profile ID
    return make_response(
        jsonify(
            {
                'message': f'Created profile with ID: {id}',
            }
        ),
        200
    )


@api_bp.route(
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
    data = request.get_json()
    if not data:
        logging.error("No data provided for setting active profile.")
        return make_response(
            jsonify(
                {
                    "error": "No data provided"
                }
            ),
            400
        )

    if "profile_id" not in data:
        logging.error("Missing 'profile_id' in request data.")
        return make_response(
            jsonify(
                {
                    "error": "Missing 'profile_id' in request data"
                }
            ),
            400
        )

    # Set the active profile in the session
    profile_id = data.get("profile_id")
    session["active_profile"] = profile_id
    logging.info(f"Active profile set to: {profile_id}")

    # Return a JSON response indicating success
    return make_response(
        jsonify(
            {
                "success": True,
                "active_profile": profile_id
            }
        ),
        200
    )


@api_bp.route(
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

    logging.info(f"Active profile retrieved: {active_profile}")
    logging.info(f"Profile details: {profile}")

    # Return a JSON response with the active profile ID
    return make_response(
        jsonify(
            {
                "active_profile": profile
            }
        ),
        200
    )


@api_bp.route(
    "/api/video/metadata",
    methods=["GET", "POST"]
)
def add_video_metadata() -> Response:
    """
    Add metadata to a video, or resolves existing metadata.

    GET:
        Map video names to IDs
        Map Tags to IDs
        Map Speakers to IDs
        Map Characters to IDs
        Map Scriptures to IDs

    POST:
        Add metadata to a video.
        Expects JSON:
            {
                "video_id": <int>,
                "url": <string>,
                "tag_id": <int>,
                "speaker_id": <int>,
                "character_id": <int>,
                "scripture_id": <int>
            }

    Returns:
        Response: A JSON response indicating success or failure.
        Includes metadata for a GET
    """

    if request.method == "GET":
        video_id = None
        tag_id = None
        speaker_id = None
        character_id = None

        # Get the query parameters
        video_name = request.args.get("video_name", None)
        tag_name = request.args.get("tag_name", None)
        speaker_name = request.args.get("speaker_name", None)
        character_name = request.args.get("character_name", None)

        with DatabaseContext() as db:
            if video_name:
                video_mgr = VideoManager(db)
                video_id = video_mgr.name_to_id(
                    name=video_name,
                )

            if tag_name:
                tag_mgr = TagManager(db)
                tag_id = tag_mgr.name_to_id(
                    name=tag_name,
                )

            if speaker_name:
                speaker_mgr = SpeakerManager(db)
                speaker_id = speaker_mgr.name_to_id(
                    name=speaker_name,
                )

            if character_name:
                character_mgr = CharacterManager(db)
                character_id = character_mgr.name_to_id(
                    name=character_name,
                )

        return make_response(
            jsonify(
                {
                    "video_id": video_id,
                    "tag_id": tag_id,
                    "speaker_id": speaker_id,
                    "character_id": character_id
                }
            ),
            200
        )

    elif request.method == "POST":
        # Get the JSON data from the request
        data = request.get_json()
        if not data:
            logging.error("No data provided for adding video metadata.")
            return make_response(
                jsonify(
                    {
                        "error": "No data provided"
                    }
                ),
                400
            )

        # Validate and extract the data
        video_id = data.get("video_id", None)
        url = data.get("url", None)
        tag_id = data.get("tag_id", None)
        speaker_id = data.get("speaker_id", None)
        character_id = data.get("character_id", None)
        scripture_id = data.get("scripture_id", None)

        if video_id is None:
            logging.error("Missing 'video_id' in request data.")
            return make_response(
                jsonify(
                    {
                        "error": "Missing 'video_id' in request data"
                    }
                ),
                400
            )

        # Ensure at least one metadata field is provided
        if all(
            field is None
            for field in [url, tag_id, speaker_id, character_id, scripture_id]
        ):
            logging.error("No metadata fields provided for video.")
            return make_response(
                jsonify(
                    {
                        "error": "At least one metadata field must be provided"
                    }
                ),
                400
            )

        # Convert tag_id to a list, splitting by commas if necessary
        if tag_id is not None:
            if isinstance(tag_id, str):
                tag_id = (
                    [t.strip() for t in tag_id.split(",")]
                    if "," in tag_id
                    else [tag_id.strip()]
                )
            else:
                tag_id = [tag_id]

        # Convert character_id to a list, splitting by commas if necessary
        if character_id is not None:
            if isinstance(character_id, str):
                character_id = (
                    [c.strip() for c in character_id.split(",")]
                    if "," in character_id
                    else [character_id.strip()]
                )
            else:
                character_id = [character_id]

        # Convert speaker_id to a list, splitting by commas if necessary
        if speaker_id is not None:
            if isinstance(speaker_id, str):
                speaker_id = (
                    [s.strip() for s in speaker_id.split(",")]
                    if "," in speaker_id
                    else [speaker_id.strip()]
                )
            else:
                speaker_id = [speaker_id]

        logging.info(
            f"Adding metadata for video ID: {video_id}, "
            f"URL: {url}, "
            f"Tag IDs: {tag_id}, "
            f"Speaker IDs: {speaker_id}, "
            f"Character IDs: {character_id}, "
        )

        # Return a success response
        return make_response(
            jsonify(
                {
                    "success": True
                }
            ),
            200
        )

    else:
        logging.error("Unsupported request method.")
        return make_response(
            jsonify(
                {
                    "error": "Unsupported request method"
                }
            ),
            405
        )
