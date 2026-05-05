"""
Module: api_video.py

API endpoints related to videos.

Endpoints:
    POST /api/videos/get_bulk
        Get multiple videos by their IDs.
    GET /api/videos/filter
        Filter videos based on query parameters.
    GET /api/videos/metadata
        Get metadata for a video.
    POST /api/videos/metadata
        Add metadata to a video, or update existing metadata.
    GET /api/videos/csv
        Read a CSV file of videos.
    POST /api/videos/add
        Add a video to the database.

Blueprints:
    video_endpoint
        Blueprint for video-related API endpoints.

Dependancies:
    flask
        Creating the API endpoints.
        Handling HTTP requests and responses.
    logging
        Logging errors and other information.
    datetime
        Handling date formatting for video metadata.
    re
        Parsing scripture references in video metadata.
    os
        Handling file paths for CSV files.
    pandas
        Loading and converting CSV files for video data.

Custom Modules:
    api.api.api_error
        Utility function for returning API error responses.
    api.api.api_success
        Utility function for returning API success responses.

    api.sql_db.DatabaseContext
        Context manager for database connections.
    api.sql_db.VideoManager
        Manager for video-related database operations.
    api.sql_db.TagManager
        Manager for tag-related database operations.
    api.sql_db.LocationManager
        Manager for location-related database operations.
    api.sql_db.SpeakerManager
        Manager for speaker-related database operations.
    api.sql_db.CharacterManager
        Manager for character-related database operations.
    api.sql_db.ScriptureManager
        Manager for scripture-related database operations.
    api.sql_db.CategoryManager
        Manager for category-related database operations.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
    request,
)
import logging
from datetime import datetime
import re
import os
import pandas as pd
import json

# Custom imports
from api.api import (
    api_error,
    api_success
)
from api.sql_db import (
    DatabaseContext,
    VideoManager,
    TagManager,
    LocationManager,
    SpeakerManager,
    CharacterManager,
    ScriptureManager,
    CategoryManager,
)


logger = logging.getLogger(__name__)

# Handle script and CSV directory paths
local_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = os.path.normpath(os.path.join(local_dir, "../scripts/csv"))
MISSING_VIDEOS_CSV = os.path.join(
    csv_folder,
    "missing_videos.csv",
)


# Create a blueprint for video-related endpoints
video_endpoint = Blueprint(
    'video_endpoint',
    __name__,
    url_prefix='/api/videos',
)


@video_endpoint.route(
    "/get_bulk",
    methods=["POST"],
)
def get_videos_bulk() -> Response:
    """
    Get multiple videos by their IDs.

    Expects a JSON body with a list of video IDs:
        {
            "video_ids": [1, 2, 3]
        }

    Args:
        None

    Returns:
        Response: A JSON response containing a list of video details for the
            requested video IDs. If any video ID is not found, it will be
            skipped and not included in the response.
    """

    # Get the list of video IDs from the request body
    data = request.get_json()
    if not data or "video_ids" not in data:
        logger.debug("Module: api_video.py, Function: get_videos_bulk")
        logger.error("Missing 'video_ids' in request data.")

        return api_error(
            error="Missing 'video_ids' in request data",
            status=400
        )

    # Validate that 'video_ids' is a list of integers
    video_ids = data["video_ids"]
    if (
        not isinstance(video_ids, list)
        or not all(isinstance(vid, int) for vid in video_ids)
    ):
        logger.debug("Module: api_video.py, Function: get_videos_bulk")
        logger.error("'video_ids' must be a list of integers.")

        return api_error(
            error="'video_ids' must be a list of integers",
            status=400
        )

    # Fetch video details for each ID
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        videos = []

        for video in video_ids:
            video_list = video_mgr.get(video)

            if not video_list:
                logger.debug("Module: api_video.py, Function: get_videos_bulk")
                logger.warning(
                    f"Video with ID {video} not found in database. Skipping."
                )

            else:
                # Add the video details to the response list if found
                if video_list:
                    videos.append(video_list[0])

                # Skip any video IDs that are not found, but log a warning
                else:
                    logger.debug(
                        "Module: api_video.py, Function: get_videos_bulk"
                    )
                    logger.warning(
                        f"Video with ID {video} not found. Skipping."
                    )

    return api_success(
        data=videos,
        message=f"Videos retrieved successfully for IDs: {video_ids}",
        status=200
    )


@video_endpoint.route(
    "/filter",
    methods=["GET"],
)
def filter_videos() -> Response:
    """
    Get a list of videos based on filter criteria provided as query parameters.

    Query parameters can include:
        - category_id: Filter by category ID.
        - tag_id: Filter by tag ID.
        - location_id: Filter by location ID.
        - speaker_id: Filter by speaker ID.
        - character_id: Filter by character ID.
        - scripture_id: Filter by scripture ID.
        - latest: Return only this many of the latest videos.

    Returns:
        Response: A JSON response containing the list of videos that match
            the filter criteria.
        If no videos are found, an empty list is returned.
    """

    # Get the query parameters (as strings or None)
    category_id = request.args.get("cat", None)
    tag_id = request.args.get("tag", None)
    location_id = request.args.get("loc", None)
    speaker_id = request.args.get("speak", None)
    character_id = request.args.get("char", None)
    scripture_id = request.args.get("scrip", None)
    latest = request.args.get("latest", None)

    # Validate that at least one filter was provided
    if all(
        value is None
        for value in [
            category_id,
            tag_id,
            location_id,
            speaker_id,
            character_id,
            scripture_id,
            latest,
        ]
    ):
        logger.debug("Module: api_video.py, Function: filter_videos")
        logger.error(
            "At least one filter query parameter is required."
        )
        return api_error(
            "At least one filter query parameter is required",
            400
        )

    # Confirm that any give parameters are valid integers
    for param_name, param_value in [
        ("category_id", category_id),
        ("tag_id", tag_id),
        ("location_id", location_id),
        ("speaker_id", speaker_id),
        ("character_id", character_id),
        ("scripture_id", scripture_id),
        ("latest", latest),
    ]:
        if param_value is not None:
            # If the parameter is a comma-separated list, validate each value
            if "," in param_value:
                values = param_value.split(",")
                if not all(value.strip().isdigit() for value in values):
                    logger.debug(
                        "Module: api_video.py, Function: filter_videos"
                    )
                    logger.error(
                        f"Invalid value for {param_name}: {param_value}. "
                        "All values must be integers."
                    )
                    return api_error(
                        error=f"Invalid value for {param_name}: {param_value}."
                        " All values must be integers.",
                        status=400
                    )

            # If it's a single value, validate it
            elif not param_value.isdigit():
                logger.debug("Module: api_video.py, Function: filter_videos")
                logger.error(
                    f"Invalid value for {param_name}: {param_value}. "
                    "Must be an integer."
                )
                return api_error(
                    error=f"Invalid value for {param_name}: {param_value}. "
                    "Must be an integer.",
                    status=400
                )

    # Convert category ID's to a list (if provided)
    if category_id:
        category_id = [int(cid) for cid in category_id.split(",")]

    # Fetch videos based on the provided filters
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)

        # Fetch a filtered list of videos
        videos = video_mgr.get_filter(
            category_id=category_id if category_id else None,
            tag_id=int(tag_id) if tag_id else None,
            location_id=int(location_id) if location_id else None,
            speaker_id=int(speaker_id) if speaker_id else None,
            character_id=int(character_id) if character_id else None,
            scripture_id=int(scripture_id) if scripture_id else None,
            latest=int(latest) if latest else 0,
        )

    return api_success(
        data=videos,
        message="Videos retrieved successfully",
        status=200
    )


@video_endpoint.route(
    "/metadata",
    methods=["GET", "POST"]
)
def add_video_metadata() -> Response:
    """
    Add or update metadata on a video (POST)
    Resolve metadata names to IDs (GET)

    GET:
        Map video names to IDs
        Map Tags to IDs
        Map Locations to IDs
        Map Speakers to IDs
        Map Characters to IDs

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
            },
            message="Metadata resolved successfully",
            status=200
        )

    elif request.method == "POST":
        # Get the JSON data from the request
        data = request.get_json()
        if not data:
            logging.error("No data provided for adding video metadata.")
            return api_error(
                "No data provided",
                400
            )

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
            return api_error(
                "Missing 'video_name' in request data",
                400
            )

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
                    return api_error(
                        "Failed to update video URL",
                        500
                    )

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
                        logging.warning(f"Creating new tag: {tag}")
                        tag_id = tag_mgr.add(
                            name=tag,
                        )

                    # Add the tag to the video
                    if tag_id is None:
                        logging.error(f"Failed to create tag: {tag}")
                        return api_error(
                            f"Failed to create tag: {tag}",
                            500
                        )

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
                        return api_error(
                            "Failed to add video tags",
                            500
                        )

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
                        logging.warning(f"Creating new location: {location}")
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
                        return api_error(
                            "Failed to add video locations",
                            500
                        )

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
                        logging.warning(f"Creating new speaker: {speaker}")
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
                        return api_error(
                            "Failed to add video speakers",
                            500
                        )

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
                        logging.warning(f"Creating new character: {character}")
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
                        return api_error(
                            "Failed to add video characters",
                            500
                        )

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
                        logging.warning(f"Creating new scripture: {scripture}")
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
                        return api_error(
                            "Failed to add video scriptures",
                            500
                        )

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
                        return api_error(
                            "Failed to add video categories",
                            500
                        )

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
                    return api_error(
                        "Failed to update video date added",
                        500
                    )

        # Return a success response
        return api_success(
            message="Video metadata added successfully",
            status=200
        )

    else:
        logging.error("Unsupported request method.")
        return api_error(
            "Unsupported request method",
            405
        )


@video_endpoint.route(
    "/csv",
    methods=["GET"]
)
def get_videos_csv() -> Response:
    """
    Get a CSV file of videos athat are missing from the database.

    Returns:
        Response: A CSV file containing video data.
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
        return api_error(
            "Failed to load CSV file",
            500
        )

    # Convert the DataFrame to JSON format
    data = json.loads(df.to_json(orient='records'))
    logging.debug(f"Missing videos:\n{data}")

    return api_success(
        data=data,
        message="Missing videos retrieved successfully",
        status=200
    )


@video_endpoint.route(
    "/add",
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
        return api_error(
            "No data provided",
            400
        )

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
    today = datetime.now().strftime("%Y-%m-%d")

    if not video_name:
        logging.error("Missing 'video_name' in request data.")
        return api_error(
            "Missing 'video_name' in request data",
            400
        )

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
            return api_error(
                f"Main category '{main_cat_name}' not found",
                404
            )

        if sub_cat_id is None:
            logging.error(f"Subcategory '{sub_cat_name}' not found.")
            return api_error(
                f"Subcategory '{sub_cat_name}' not found",
                404
            )

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
                return api_error(
                    "Invalid duration format",
                    400
                )

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
            return api_error(
                f"Failed to add video '{video_name}'",
                500
            )

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
