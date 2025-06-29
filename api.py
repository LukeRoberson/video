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
    - re: For regular expression operations.

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
import re
from datetime import datetime

# Custom imports
from sql_db import (
    DatabaseContext,
    VideoManager,
    TagManager,
    SpeakerManager,
    CharacterManager,
    ScriptureManager,
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
            return make_response(
                jsonify(
                    {
                        "error": "Missing 'video_name' in request data"
                    }
                ),
                400
            )

        # Ensure at least one metadata field is provided
        if all(
            field is None
            for field in [
                description, url, tag_name, speaker_name,
                character_name, scripture_name, date_added
            ]
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

                return make_response(
                    jsonify(
                        {
                            "error": "Invalid date format for 'date_added'. "
                                     "Expected ISO format."
                        }
                    ),
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
                return make_response(
                    jsonify(
                        {
                            "error": f"Video '{video_name}' not found"
                        }
                    ),
                    404
                )
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
                    return make_response(
                        jsonify(
                            {
                                "error": "Failed to update video description"
                            }
                        ),
                        500
                    )
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
                    return make_response(
                        jsonify(
                            {
                                "error": "Failed to update video URL"
                            }
                        ),
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
                        logging.info(f"Creating new tag: {tag}")
                        tag_id = tag_mgr.add(
                            name=tag,
                        )

                    # Add the tag to the video
                    if tag_id is None:
                        logging.error(f"Failed to create tag: {tag}")
                        return make_response(
                            jsonify(
                                {
                                    "error": f"Failed to create tag: {tag}"
                                }
                            ),
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
                        return make_response(
                            jsonify(
                                {
                                    "error": "Failed to add video tags"
                                }
                            ),
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
                        logging.info(f"Creating new speaker: {speaker}")
                        speaker_id = speaker_mgr.add(
                            name=speaker,
                        )

                    # Add the speaker to the video
                    if speaker_id is None:
                        logging.error(f"Failed to create speaker: {speaker}")
                        return make_response(
                            jsonify(
                                {
                                    "error": f"Failed to create speaker: "
                                    f"{speaker}"
                                }
                            ),
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
                        return make_response(
                            jsonify(
                                {
                                    "error": "Failed to add video speakers"
                                }
                            ),
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
                        logging.info(f"Creating new character: {character}")
                        character_id = character_mgr.add(
                            name=character,
                        )

                    # Add the character to the video
                    if character_id is None:
                        logging.error(
                            f"Failed to create character: {character}"
                        )
                        return make_response(
                            jsonify(
                                {
                                    "error": f"Failed to create character: "
                                    f"{character}"
                                }
                            ),
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
                        return make_response(
                            jsonify(
                                {
                                    "error": "Failed to add video characters"
                                }
                            ),
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
                        return make_response(
                            jsonify(
                                {
                                    "error": f"Scripture reference "
                                    f"'{scripture}' is not valid. Skipping"
                                }
                            ),
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
                        return make_response(
                            jsonify(
                                {
                                    "error": f"Failed to create "
                                    f"scripture: {scripture}"
                                }
                            ),
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
                        return make_response(
                            jsonify(
                                {
                                    "error": "Failed to add video scriptures"
                                }
                            ),
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
                    return make_response(
                        jsonify(
                            {
                                "error": "Failed to update video date added"
                            }
                        ),
                        500
                    )

                logging.info(f"Updated video ({result}) date added.")

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
        return jsonify([])

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
    return make_response(
        jsonify(
            videos
        ),
        200
    )
