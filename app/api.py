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
    - /api/videos/csv
        - get_videos_csv: Returns a CSV file of missing videos.
    - /api/videos/add
        - add_videos: Adds a new video with metadata to the database.
    - /api/search/videos
        - search_videos: Searches for videos by name or description.
    - /api/search/advanced
        - advanced_search: Performs an advanced search for videos.

Dependencies:
    - Flask: For creating the API endpoints.
    - logging: For logging API requests and responses.

Custom Dependencies:
    - DatabaseContext: Context manager for database connections.
    - VideoManager: Manages video-related database operations.
    - CategoryManager: Manages category-related database operations.
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
from datetime import datetime
import pandas as pd
import os

# Custom imports
from app.sql_db import (
    DatabaseContext,
    VideoManager,
    CategoryManager,
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
