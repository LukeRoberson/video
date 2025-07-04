"""
Module: api.py

API endpoints that the browser will use to fetch additional information
    For example, the browser may use the API to find videos that belong
        to a specific category

Functions:
    - seconds_to_hhmmss: Converts seconds to HH:MM:SS format.
    - api_success: Returns a standardized success response.
    - api_error: Returns a standardized error response.

Routes:
    - /api/categories/<int>/<int>
        - category_filter: Fetches videos by category and subcategory IDs.
    - /api/profile/create
        - create_profile: Creates a new user profile.
    - /api/profile/set_active
        - set_active_profile: Sets the active profile for the session.
    - /api/profile/get_active
        - get_active_profile: Retrieves the active profile for the session.
    - /api/video/metadata
        - add_video_metadata: Adds or resolves metadata for a video.
    - /api/search/videos
        - search_videos: Searches for videos by name or description.
    - /api/scripture
        - add_scripture_text: Adds text to a scripture.
    - /api/mark_watched
        - mark_watched: Marks a video as watched for the active profile.
    - /api/videos/csv
        - get_videos_csv: Returns a CSV file of missing videos.

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
    session,
    jsonify,
    make_response,
)
import logging
import re
from datetime import datetime
import pandas as pd
import os

# Custom imports
from app.sql_db import (
    DatabaseContext,
    VideoManager,
    CategoryManager,
    TagManager,
    SpeakerManager,
    CharacterManager,
    ScriptureManager,
)
from app.local_db import (
    LocalDbContext,
    ProfileManager,
    ProgressManager,
)


MISSING_VIDEOS_CSV = "csv/missing_videos.csv"


api_bp = Blueprint(
    'api',
    __name__,
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


def api_success(
    data=None,
    message=None,
    status=200
) -> Response:
    """
    Helper to return a standardized success response.

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


@api_bp.route(
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
        return api_error("No data provided", 400)

    if "profile_id" not in data:
        logging.error("Missing 'profile_id' in request data.")
        return api_error("Missing 'profile_id' in request data", 400)

    # Set the active profile in the session
    profile_id = data.get("profile_id")
    session["active_profile"] = profile_id
    logging.info(f"Active profile set to: {profile_id}")

    # Return a JSON response indicating success
    return api_success(
        data={"active_profile": profile_id}
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

    # Return a JSON response with the active profile ID
    return api_success(
        data={"active_profile": profile}
    )


@api_bp.route(
    "/api/profile/mark_watched",
    methods=["POST"]
)
def mark_watched() -> Response:
    """
    Mark a video as watched for the active profile.

    Expects JSON:
        {
            "video_id": <int>
        }

    Returns:
        Response: A JSON response indicating success or failure.
    """

    data = request.get_json()
    video_id = data.get("video_id", None)

    if not video_id:
        return api_error(error="Missing 'video_id' in request data")

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        progress_mgr = ProgressManager(db)

        # Mark the video as watched for the active profile
        result = profile_mgr.mark_watched(
            profile_id=session.get("active_profile", "guest"),
            video_id=video_id
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


@api_bp.route(
    "/api/profile/mark_unwatched",
    methods=["POST"]
)
def mark_unwatched() -> Response:
    """
    Mark a video as unwatched for the active profile.

    Expects JSON:
        {
            "video_id": <int>
        }

    Returns:
        Response: A JSON response indicating success or failure.
    """

    data = request.get_json()
    video_id = data.get("video_id", None)

    if not video_id:
        return api_error(error="Missing 'video_id' in request data")

    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        result = profile_mgr.mark_unwatched(
            profile_id=session.get("active_profile", "guest"),
            video_id=video_id
        )

    if not result:
        return api_error(
            error=f"Failed to mark video {video_id} as unwatched",
            status=500
        )

    return api_success(message=f"Marked video {video_id} as unwatched")


@api_bp.route(
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


@api_bp.route(
    "/api/video/metadata",
    methods=["GET", "POST"]
)
def add_video_metadata() -> Response:
    """
    Add metadata to a video, or update existing metadata.

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
                "scripture_id": <int>,
                "date_added": <string>,
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

        return api_success(
            data={
                "video_id": video_id,
                "tag_id": tag_id,
                "speaker_id": speaker_id,
                "character_id": character_id
            }
        )

    elif request.method == "POST":
        # Get the JSON data from the request
        data = request.get_json()
        if not data:
            logging.error("No data provided for adding video metadata.")
            return api_error("No data provided", 400)

        print(f"Received data: {data}")

        # Validate and extract the data
        video_name = data.get("video_name", None)
        description = data.get("description", None)
        url = data.get("url", None)
        tag_name = data.get("tag_name", None)
        speaker_name = data.get("speaker_name", None)
        character_name = data.get("character_name", None)
        scripture_name = data.get("scripture_name", None)
        date_added = data.get("date_added", None)

        # If they're empty strings, convert to None
        description = None if description == '' else description
        url = None if url == '' else url
        tag_name = None if tag_name == '' else tag_name
        speaker_name = None if speaker_name == '' else speaker_name
        character_name = None if character_name == '' else character_name
        scripture_name = None if scripture_name == '' else scripture_name

        # Ensure video_name is provided
        if video_name is None:
            logging.error("Missing 'video_name' in request data.")
            return api_error("Missing 'video_name' in request data", 400)

        # Ensure at least one metadata field is provided
        if all(
            field is None
            for field in [
                description, url, tag_name, speaker_name,
                character_name, scripture_name, date_added
            ]
        ):
            logging.error("No metadata fields provided for video.")
            return api_error(
                "At least one metadata field must be provided",
                400
            )

        # Convert tag_name to a list, splitting by commas if necessary
        if tag_name is not None:
            if isinstance(tag_name, str):
                tag_name = (
                    [t.strip() for t in tag_name.split(",")]
                    if "," in tag_name
                    else [tag_name.strip()]
                )
            else:
                tag_name = [tag_name]

        # Convert character_name to a list, splitting by commas if necessary
        if character_name is not None:
            if isinstance(character_name, str):
                character_name = (
                    [c.strip() for c in character_name.split(",")]
                    if "," in character_name
                    else [character_name.strip()]
                )
            else:
                character_name = [character_name]

        # Convert speaker_name to a list, splitting by commas if necessary
        if speaker_name is not None:
            if isinstance(speaker_name, str):
                speaker_name = (
                    [s.strip() for s in speaker_name.split(",")]
                    if "," in speaker_name
                    else [speaker_name.strip()]
                )
            else:
                speaker_name = [speaker_name]

        # Convert scripture_name to a list, splitting by commas if necessary
        if scripture_name is not None:
            if isinstance(scripture_name, str):
                scripture_name = (
                    [s.strip() for s in scripture_name.split(",")]
                    if "," in scripture_name
                    else [scripture_name.strip()]
                )
            else:
                scripture_name = [scripture_name]

        # Convert date_added to ISO format if provided
        if date_added is not None:
            try:
                # Parse the ISO format date and reformat it
                dt = datetime.fromisoformat(date_added)
                date_added = dt.strftime("%Y-%m-%d %H:%M:%S")

            except Exception:
                logging.error(
                    f"Invalid date format for 'date_added': {date_added}"
                )
                return api_error(
                    "Invalid date format for 'date_added'. Expect ISO format.",
                    400
                )

        logging.info(
            f"Adding metadata for video ID: {video_name}, "
            f"Description: {description}, "
            f"URL: {url}, "
            f"Tag IDs: {tag_name}, "
            f"Speaker IDs: {speaker_name}, "
            f"Character IDs: {character_name}, "
            f"Scripture IDs: {scripture_name}, "
            f"Date Added: {date_added}"
        )

        # Add metadata to the video
        with DatabaseContext() as db:
            video_mgr = VideoManager(db)
            video_id = video_mgr.name_to_id(
                name=video_name,
            )

            if video_id is None:
                logging.error(f"Video '{video_name}' not found.")
                return api_error(f"Video '{video_name}' not found", 404)
            logging.info(f"Video name: {video_name}, ID: {video_id}")

            # Add description if provided
            if description is not None:
                result = video_mgr.update(
                    id=video_id,
                    description=description,
                )

                if not result:
                    logging.error(
                        f"Failed to update description for "
                        f"video ID: {video_id}"
                    )
                    return api_error("Failed to update video description", 500)
                logging.info(f"Updated video ({result}) description.")

            # Add URL if provided
            if url is not None:
                result = video_mgr.update(
                    id=video_id,
                    url=url,
                )

                if not result:
                    logging.error(
                        f"Failed to update URL for video ID: {video_id}"
                    )
                    return api_error("Failed to update video URL", 500)

            # Add tags if provided
            if tag_name is not None:
                tag_mgr = TagManager(db)

                # Go through each tag name and resolve it to an ID
                for tag in tag_name:
                    # Get the tag ID from the database
                    tag_id = tag_mgr.name_to_id(
                        name=tag,
                    )

                    # If the tag does not exist, create it
                    if tag_id is None:
                        logging.info(f"Creating new tag: {tag}")
                        tag_id = tag_mgr.add(
                            name=tag,
                        )

                    # Add the tag to the video
                    if tag_id is None:
                        logging.error(f"Failed to create tag: {tag}")
                        return api_error(f"Failed to create tag: {tag}", 500)

                    logging.info(
                        f"Adding tag '{tag}' with ID {tag_id} "
                        f"to video ID: {video_id}"
                    )

                    result = tag_mgr.add_to_video(
                        video_id=video_id,
                        tag_id=tag_id,
                    )

                    if not result:
                        logging.error(
                            f"Failed to add tag {tag} for video ID: {video_id}"
                        )
                        return api_error("Failed to add video tags", 500)

            # Add speakers if provided
            if speaker_name is not None:
                speaker_mgr = SpeakerManager(db)

                # Go through each speaker name and resolve it to an ID
                for speaker in speaker_name:
                    # Get the speaker ID from the database
                    speaker_id = speaker_mgr.name_to_id(
                        name=speaker,
                    )

                    # If the speaker does not exist, create it
                    if speaker_id is None:
                        logging.info(f"Creating new speaker: {speaker}")
                        speaker_id = speaker_mgr.add(
                            name=speaker,
                        )

                    # Add the speaker to the video
                    if speaker_id is None:
                        logging.error(f"Failed to create speaker: {speaker}")
                        return api_error(
                            f"Failed to create speaker: {speaker}",
                            500
                        )

                    logging.info(
                        f"Adding speaker '{speaker}' with ID {speaker_id} "
                        f"to video ID: {video_id}"
                    )

                    result = speaker_mgr.add_to_video(
                        video_id=video_id,
                        speaker_id=speaker_id,
                    )

                    if not result:
                        logging.error(
                            f"Failed to add speaker {speaker} for "
                            f"video ID: {video_id}"
                        )
                        return api_error("Failed to add video speakers", 500)

            # Add characters if provided
            if character_name is not None:
                character_mgr = CharacterManager(db)

                # Go through each character name and resolve it to an ID
                for character in character_name:
                    # Get the character ID from the database
                    character_id = character_mgr.name_to_id(
                        name=character,
                    )

                    # If the character does not exist, create it
                    if character_id is None:
                        logging.info(f"Creating new character: {character}")
                        character_id = character_mgr.add(
                            name=character,
                        )

                    # Add the character to the video
                    if character_id is None:
                        logging.error(
                            f"Failed to create character: {character}"
                        )
                        return api_error(
                            f"Failed to create character: {character}",
                            500
                        )

                    logging.info(
                        f"Adding character '{character}' with ID "
                        f"{character_id} to video ID: {video_id}"
                    )

                    result = character_mgr.add_to_video(
                        video_id=video_id,
                        character_id=character_id,
                    )

                    if not result:
                        logging.error(
                            f"Failed to add character {character} for "
                            f"video ID: {video_id}"
                        )
                        return api_error("Failed to add video characters", 500)

            # Add scripture if provided
            if scripture_name is not None:
                scripture_mgr = ScriptureManager(db)

                for scripture in scripture_name:
                    # Split name into book, chapter, and verse
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
                        scripture,
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
                            f"Scripture reference '{scripture}' is not valid.",
                            400
                        )

                    # Get the scripture ID from the database
                    scripture_id = scripture_mgr.name_to_id(
                        book=book,
                        chapter=chapter,
                        verse=verse,
                    )

                    # If the scripture does not exist, create it
                    if scripture_id is None:
                        logging.info(f"Creating new scripture: {scripture}")
                        scripture_id = scripture_mgr.add(
                            book=book,
                            chapter=chapter,
                            verse=verse,
                        )

                    if scripture_id is None:
                        logging.error(
                            f"Failed to create scripture: {scripture}"
                        )
                        return api_error(
                            f"Failed to create scripture: {scripture}",
                            500
                        )

                    # Add the scripture to the video
                    logging.info(
                        f"Adding scripture '{scripture}' "
                        f"(book: {book}, chapter: {chapter}, verse: {verse}) "
                        f"with ID {scripture_id} to video ID: {video_id}"
                    )

                    result = scripture_mgr.add_to_video(
                        video_id=video_id,
                        scripture_id=scripture_id,
                    )

                    if not result:
                        logging.error(
                            f"Failed to add scripture {scripture} "
                            f"for video ID: {video_id}"
                        )
                        return api_error("Failed to add video scriptures", 500)

            if date_added is not None:
                # Update the video's date added
                result = video_mgr.update(
                    id=video_id,
                    date_added=date_added,
                )

                if not result:
                    logging.error(
                        f"Failed to update date added for video ID: {video_id}"
                    )
                    return api_error("Failed to update video date added", 500)

        # Return a success response
        return api_success()

    else:
        logging.error("Unsupported request method.")
        return api_error("Unsupported request method", 405)


@api_bp.route(
    "/api/videos/csv",
    methods=["GET"]
)
def get_videos_csv() -> Response:
    """
    Get a CSV file of all videos in the database.

    Returns:
        Response: A CSV file containing all video data.
    """

    # Check the CSV exists
    if not os.path.exists(MISSING_VIDEOS_CSV):
        logging.error(f"CSV file not found: {MISSING_VIDEOS_CSV}")
        return api_error("CSV file not found", 404)

    # Load the CSV file into a DataFrame
    try:
        df = pd.read_csv(MISSING_VIDEOS_CSV)
    except Exception as e:
        logging.error(f"Failed to load CSV: {e}")
        return api_error("Failed to load CSV file", 500)

    # Convert the DataFrame to JSON format
    return api_success(
        data=df.to_dict(orient='records'),
        message="CSV data retrieved successfully"
    )


@api_bp.route(
    "/api/videos/add",
    methods=["POST"]
)
def add_videos() -> Response:
    """
    Add a video to the database.

    Browser will send a POST request with a JSON body containing:
        {
            "video_name": "<video name>",
            "video_url": "<video URL>",
            "main_cat_name": "<main category name>",
            "sub_cat_name": "<subcategory name>",
            "url_1080": "<1080p video URL>",
            "url_720": "<720p video URL>",
            "url_480": "<480p video URL>",
            "url_360": "<360p video URL>",
            "url_240": "<240p video URL>",
            "thumbnail": "<thumbnail image URL>",
            "duration": <video duration in HH:MM:SS>,
        }

    Returns:
        Response: A JSON response indicating success or failure.
    """

    data = request.get_json()
    if not data:
        logging.error("No data provided for adding video.")
        return api_error("No data provided", 400)

    # Get fields
    video_name = data.get("video_name", None)
    video_url = data.get("video_url", None)
    main_cat_name = data.get("main_cat_name", None)
    sub_cat_name = data.get("sub_cat_name", None)
    url_1080 = data.get("url_1080", None)
    url_720 = data.get("url_720", None)
    url_480 = data.get("url_480", None)
    url_360 = data.get("url_360", None)
    url_240 = data.get("url_240", None)
    thumbnail = data.get("thumbnail", None)
    duration = data.get("duration", None)

    if not video_name:
        logging.error("Missing 'video_name' in request data.")
        return api_error("Missing 'video_name' in request data", 400)

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        cat_mgr = CategoryManager(db)

        # Get category IDs
        main_cat_id = cat_mgr.name_to_id(
            name=main_cat_name
        )
        sub_cat_id = cat_mgr.name_to_id(
            name=sub_cat_name
        )

        if main_cat_id is None:
            logging.error(f"Main category '{main_cat_name}' not found.")
            return api_error(f"Main category '{main_cat_name}' not found", 404)
        if sub_cat_id is None:
            logging.error(f"Subcategory '{sub_cat_name}' not found.")
            return api_error(f"Subcategory '{sub_cat_name}' not found", 404)

        # Convert duration to seconds if provided
        if duration is not None:
            try:
                # Parse the duration string in HH:MM:SS format
                parts = duration.split(':')
                if len(parts) == 3:
                    hours, minutes, seconds = map(int, parts)
                    duration = hours * 3600 + minutes * 60 + seconds
                elif len(parts) == 2:
                    minutes, seconds = map(int, parts)
                    duration = minutes * 60 + seconds
                else:
                    duration = int(parts[0])  # Assume it's just seconds

            except ValueError:
                logging.error(f"Invalid duration format: {duration}")
                return api_error("Invalid duration format", 400)

        # Add the video to the database
        video_id = video_mgr.add(
            name=video_name,
            url=video_url,
            url_1080=url_1080,
            url_720=url_720,
            url_480=url_480,
            url_360=url_360,
            url_240=url_240,
            thumbnail=thumbnail,
            duration=duration
        )

        if video_id is None:
            logging.error(
                f"Failed to add video '{video_name}' to the database."
            )
            return api_error(f"Failed to add video '{video_name}'", 500)

        # Add the categories to the video
        main_result = cat_mgr.add_to_video(
            video_id=video_id,
            category_id=main_cat_id,
        )
        sub_result = cat_mgr.add_to_video(
            video_id=video_id,
            category_id=sub_cat_id,
        )

        cat_str = ""
        if not main_result:
            logging.error(
                f"Failed to add main category '{main_cat_name}' "
                f"to video ID: {video_id}"
            )
            cat_str += f"Main category '{main_cat_name}' not added. "
        if not sub_result:
            logging.error(
                f"Failed to add subcategory '{sub_cat_name}' "
                f"to video ID: {video_id}"
            )
            cat_str += f"Subcategory '{sub_cat_name}' not added. "

        if cat_str:
            return api_success(
                message="Video added, but some categories were not added.",
            )

    return api_success(
        message="video added"
    )


@api_bp.route(
    "/api/search/videos",
    methods=["GET"],
)
def search_videos() -> Response:
    """
    Search for videos by name or description.

    Query Parameters:
        q (str): The search query string.
        limit (int, optional):
            Maximum number of results to return. Defaults to 50.

    Returns:
        Response: A JSON response containing the list of matching videos.
        If no videos are found, an empty list is returned.
    """

    # Get query parameters
    query = request.args.get("q", "").strip()
    limit = request.args.get("limit", 50, type=int)

    if not query:
        logging.warning("Empty search query provided.")
        return api_success(data=[])

    # Use the search method to find videos
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        videos = video_mgr.search(
            query=query,
            limit=limit
        )

    # If videos are found, log the count
    if videos:
        logging.info(f"Found {len(videos)} videos for query: '{query}'")

        # Convert duration from seconds to HH:MM:SS format
        for video in videos:
            video['duration'] = seconds_to_hhmmss(video['duration'])

    # If no videos are found, log the event
    else:
        videos = []
        logging.info(f"No videos found for query: '{query}'")

    # Return the list of videos as a JSON response
    return api_success(data=videos)


@api_bp.route(
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


@api_bp.route(
    "/api/categories/<int:category_id>/<int:subcategory_id>",
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

    # Get watch status for the active profile
    active_profile = session.get("active_profile", None)
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
    videos.sort(key=lambda v: v.get('date_added', ''), reverse=True)

    return make_response(
        jsonify(
            videos,
        ),
        200
    )
