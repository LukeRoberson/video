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
    - /api/video/metadata
        - add_video_metadata: Adds or resolves metadata for a video.
    - /api/videos/csv
        - get_videos_csv: Returns a CSV file of missing videos.
    - /api/videos/add
        - add_videos: Adds a new video with metadata to the database.
    - /api/search/videos
        - search_videos: Searches for videos by name or description.
    - /api/search/advanced
        - advanced_search: Performs an advanced search for videos.
    - /api/scripture
        - add_scripture_text: Adds text to a scripture.
    - /api/categories/<int>/<int>
        - category_filter: Fetches videos by category and subcategory IDs.

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
    LocationManager,
    SpeakerManager,
    CharacterManager,
    ScriptureManager,
)
from app.local_db import (
    LocalDbContext,
    ProfileManager,
)


# Handle script and CSV directory paths
local_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = os.path.normpath(os.path.join(local_dir, "../scripts/csv"))
MISSING_VIDEOS_CSV = os.path.join(csv_folder, "missing_videos.csv")

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

    # Handle None or non-positive values
    if seconds is None or seconds <= 0:
        seconds = 1

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
        Map Locations to IDs
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
                "location_id": <int>,
                "speaker_id": <int>,
                "character_id": <int>,
                "scripture_id": <int>,
                "category_name": <string>,
                "date_added": <string>,
            }

    Returns:
        Response: A JSON response indicating success or failure.
        Includes metadata for a GET
    """

    if request.method == "GET":
        video_id = None
        tag_id = None
        location_id = None
        speaker_id = None
        character_id = None

        # Get the query parameters
        video_name = request.args.get("video_name", None)
        tag_name = request.args.get("tag_name", None)
        location_name = request.args.get("location_name", None)
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

            if location_name:
                loc_mgr = LocationManager(db)
                location_id = loc_mgr.name_to_id(
                    name=location_name,
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
                "location_id": location_id,
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
        location_name = data.get("location_name", None)
        speaker_name = data.get("speaker_name", None)
        character_name = data.get("character_name", None)
        scripture_name = data.get("scripture_name", None)
        category_name = data.get("category_name", None)
        date_added = data.get("date_added", None)

        # If they're empty strings, convert to None
        description = None if description == '' else description
        url = None if url == '' else url
        tag_name = None if tag_name == '' else tag_name
        location_name = None if location_name == '' else location_name
        speaker_name = None if speaker_name == '' else speaker_name
        character_name = None if character_name == '' else character_name
        category_name = None if category_name == '' else category_name
        scripture_name = None if scripture_name == '' else scripture_name

        # Ensure video_name is provided
        if video_name is None:
            logging.error("Missing 'video_name' in request data.")
            return api_error("Missing 'video_name' in request data", 400)

        # Ensure at least one metadata field is provided
        if all(
            field is None
            for field in [
                description, url, tag_name, location_name, speaker_name,
                character_name, scripture_name, date_added, category_name
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

        # Convert location_name to a list, splitting by commas if necessary
        if location_name is not None:
            if isinstance(location_name, str):
                location_name = (
                    [t.strip() for t in location_name.split(",")]
                    if "," in location_name
                    else [location_name.strip()]
                )
            else:
                location_name = [location_name]

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

        # Convert category_name to a list, splitting by commas if necessary
        if category_name is not None:
            if isinstance(category_name, str):
                category_name = (
                    [s.strip() for s in category_name.split(",")]
                    if "," in category_name
                    else [category_name.strip()]
                )
            else:
                category_name = [category_name]

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
            f"Location IDs: {location_name}, "
            f"Speaker IDs: {speaker_name}, "
            f"Character IDs: {character_name}, "
            f"Scripture IDs: {scripture_name}, "
            f"Category Name: {category_name}, "
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

            # Add locations if provided
            if location_name is not None:
                loc_mgr = LocationManager(db)

                # Go through each location name and resolve it to an ID
                for location in location_name:
                    # Get the location ID from the database
                    location_id = loc_mgr.name_to_id(
                        name=location,
                    )

                    # If the tag does not exist, create it
                    if location_id is None:
                        logging.info(f"Creating new location: {location}")
                        location_id = loc_mgr.add(
                            name=location,
                        )

                    # Add the location to the video
                    if location_id is None:
                        logging.error(f"Failed to create location: {location}")
                        return api_error(
                            f"Failed to create location: {location}",
                            500
                        )

                    logging.info(
                        f"Adding location '{location}' with ID {location_id} "
                        f"to video ID: {video_id}"
                    )

                    result = loc_mgr.add_to_video(
                        video_id=video_id,
                        location_id=location_id,
                    )

                    if not result:
                        logging.error(
                            f"Failed to add location {location} "
                            f"for video ID: {video_id}"
                        )
                        return api_error("Failed to add video locations", 500)

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

            # Add category if provided
            if category_name is not None:
                cat_mgr = CategoryManager(db)

                # Get the category ID from the database
                for category in category_name:
                    category_id = cat_mgr.name_to_id(
                        name=category,
                    )

                    # If the category does not exist, return an error
                    if category_id is None:
                        logging.error(f"Category {category} does not exist")
                        return api_error(
                            f"Category {category} does not exist",
                            500
                        )

                    # Add the category to the video
                    logging.info(
                        f"Adding category '{category}' with ID "
                        f"{category_id} to video ID: {video_id}"
                    )

                    result = cat_mgr.add_to_video(
                        video_id=video_id,
                        category_id=category_id,
                    )

                    if not result:
                        logging.error(
                            f"Failed to add category {category} for "
                            f"video ID: {video_id}"
                        )
                        return api_error("Failed to add video categories", 500)

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
    logging.debug(f"Missing videos:\n{df.to_dict(orient='records')}")
    return make_response(
        Response(
            df.to_json(orient='index'),
        ),
        200,
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
    today = datetime.now().strftime("%d-%m-%Y")

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
            duration=duration,
            date_added=today,
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
    "/api/search/advanced",
    methods=["GET"],
)
def advanced_search() -> Response:
    """
    Advanced search for videos with multiple filter criteria.

    Query Parameters:
        query (str, optional): Text search in title/description
        speaker_ids (list, optional): Speaker IDs to filter by
        character_ids (list, optional): Character IDs to filter by
        location_ids (list, optional): Location IDs to filter by
        tag_ids (list, optional): Tag IDs to filter by
        limit (int, optional): Maximum results. Defaults to 50.

    Returns:
        Response: JSON response with matching videos
    """

    # Get query parameters
    query = request.args.get("query", "").strip()
    speaker_ids = request.args.getlist("speaker_ids")
    character_ids = request.args.getlist("character_ids")
    location_ids = request.args.getlist("location_ids")
    tag_ids = request.args.getlist("tag_ids")
    limit = request.args.get("limit", 50, type=int)

    # Convert string IDs to integers
    try:
        speaker_ids = [int(id) for id in speaker_ids if id]
        character_ids = [int(id) for id in character_ids if id]
        location_ids = [int(id) for id in location_ids if id]
        tag_ids = [int(id) for id in tag_ids if id]
    except ValueError:
        return api_error("Invalid ID format", 400)

    # Build the search query
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)

        # Build filter kwargs for get_filter method
        filter_kwargs = {}

        if query:
            videos = video_mgr.search(query=query, limit=1000)
        else:
            videos = []

        if speaker_ids:
            filter_kwargs["speaker_id"] = speaker_ids
        if character_ids:
            filter_kwargs["character_id"] = character_ids
        if location_ids:
            filter_kwargs["location_id"] = location_ids
        if tag_ids:
            filter_kwargs["tag_id"] = tag_ids

        if filter_kwargs:
            if videos:
                # Apply additional filters to search results
                video_ids = [v['id'] for v in videos]
                filter_kwargs["video_id"] = video_ids

            filtered_videos = video_mgr.get_filter(**filter_kwargs)
            videos = filtered_videos if filtered_videos else videos
        elif not query:
            # No search query and no filters - return empty
            videos = []

    # Limit results
    videos = videos[:limit] if videos else []

    # Convert duration format
    for video in videos:
        if video.get('duration'):
            video['duration'] = seconds_to_hhmmss(video['duration'])

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
