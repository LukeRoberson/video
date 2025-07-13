"""
Module: web_dynamic.py

Defines a Flask blueprint for dynamic web routes.
    These are web pages that are based on an item, such as tag, speaker,
    bible chapter, or scripture.

Functions:
    - get_one_video: Fetches a single video or item from the database by ID.
    - get_videos_by_filter: Fetches videos based on filter criteria.
    - set_watched_status: Sets the watched status for each video in a list.

Routes:
    - /video/<int:video_id>:
        Displays details of a specific video.
    - /tag/<int:tag_id>:
        Displays details of a specific tag and associated videos.
    - /speaker/<int:speaker_id>:
        Displays details of a specific speaker and associated videos.
    - /character/<int:character_id>:
        Displays details of a specific character and associated videos.
    - /scripture/<int:scripture_id>:
        Displays details of a specific scripture and associated videos.
    - /search:
        Displays search results for videos based on a query string.

Dependancies:
    Flask: To define the blueprint for web pages.
    logging: For logging debug information.

Custom Dependencies:
    DatabaseContext: Context manager for database operations.
    CategoryManager: Manages category-related database operations.
    LocalDbContext: Context manager for local database operations.
    ProfileManager: Manages user profile-related database operations.
"""

# Standard library imports
from flask import (
    Blueprint,
    Response,
    render_template,
    make_response,
    request,
    session,
)
from typing import Union
import random

# Custom imports
from app.sql_db import (
    DatabaseContext,
    VideoManager,
    CategoryManager,
    TagManager,
    SpeakerManager,
    CharacterManager,
    ScriptureManager,
    SimilarityManager,
)
from app.local_db import (
    LocalDbContext,
    ProfileManager,
    ProgressManager,
)


# Setup type variables for manager types
ManagerType = Union[
    VideoManager,
    TagManager,
    SpeakerManager,
    CharacterManager,
    ScriptureManager,
]


def get_one_video(
    manager: ManagerType,
    id: int,
    item_name: str = "Item",
) -> Response | dict:
    """
    Fetch a single item from the database by its ID.

    Args:
        manager (ManagerType):
            The manager instance to use for fetching the item.
        id (int):
            The ID of the item to fetch.
        item_name (str):
            The name of the item for error messages.

    Returns:
        Response | dict: The item if found, or a 404 response if not found.
    """

    # User the manager to get the video by ID
    video = manager.get(id=id)

    # If the video is found, return the first item in the list
    if video:
        return video[0]

    # If the video is not found, return a 404 response
    else:
        return make_response(
            render_template(
                "404.html",
                message=f"{item_name} not found"
            ),
            404
        )


def get_videos_by_filter(
    video_mgr: VideoManager,
    filter_kwargs: dict,
    message: str,
) -> list | Response:
    """
    Fetch videos from the database based on filter criteria.

    Args:
        video_mgr (VideoManager):
            The video manager instance to use for fetching videos.
        filter_kwargs (dict):
            The filter criteria to apply when fetching videos.
        message (str):
            The message to display if no videos are found.

    Returns:
        list | Response: A list of videos if found, or a 404 response if no
    """

    # Get a list of videos based on the filter criteria
    videos = video_mgr.get_filter(**filter_kwargs)

    # If no videos are found, return a 404 response with the provided message
    if not videos:
        return make_response(
            render_template(
                "404.html",
                message=message
            ),
            404
        )

    # If videos are found, return the list of videos
    return videos


def set_watched_status(
    videos: list,
    profile_id: int,
    profile_mgr: ProfileManager,
) -> None:
    """
    Set the watched status for each video in the list for the current user.

    Args:
        videos (list):
            A list of video dictionaries to update with watched status.
        profile_id (int):
            The ID of the user profile to check watched status against.
        profile_mgr (ProfileManager):
            The profile manager instance to use for checking watched status.

    Returns:
        None: The function modifies the videos list in place.
    """

    # Loop through each video and check if it has been watched
    for video in videos:
        watched = profile_mgr.check_watched(
            video_id=video['id'],
            profile_id=profile_id,
        )

        # Set the 'watched' key to True
        video['watched'] = watched


dynamic_bp = Blueprint(
    'dynamic_pages',
    __name__,
)


@dynamic_bp.route(
    "/video/<int:video_id>",
    methods=["GET"],
)
def video_details(
    video_id: int,
) -> Response:
    """
    Render the details of a specific video along with similar videos.
    This is seen when a user clicks on a video from the home page.

    Args:
        video_id (int): The ID of the video to fetch details for.

    Returns:
        Response: A rendered HTML page with video details,
            tags, speakers, characters, scriptures, and similar videos.
        If the video is not found, a 404 error is returned.
    """

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        cat_mgr = CategoryManager(db)

        # Fetch the video details (returned as a list)
        video_list = video_mgr.get(video_id)
        if not video_list:
            return make_response(
                render_template(
                    "404.html",
                    message="Video not found"
                ),
                404
            )
        video = video_list[0]

        # Fetch the category name for the video
        cat_list = cat_mgr.get_from_video(
            video_id=video_id
        )

        # Fetch tags for the video
        tag_mgr = TagManager(db)
        tags = tag_mgr.get_from_video(
            video_id=video_id
        )
        # Fetch speakers for the video
        speaker_mgr = SpeakerManager(db)
        speakers = speaker_mgr.get_from_video(
            video_id=video_id
        )
        # Fetch characters for the video
        character_mgr = CharacterManager(db)
        characters = character_mgr.get_from_video(
            video_id=video_id
        )
        # Fetch scriptures for the video
        scripture_mgr = ScriptureManager(db)
        scriptures = scripture_mgr.get_from_video(
            video_id=video_id
        )

    # Check if the video is marked as watched by the user, or in progress
    current_time = 0
    with LocalDbContext() as local_db:
        profile_mgr = ProfileManager(local_db)
        progress_mgr = ProgressManager(local_db)

        watched = profile_mgr.check_watched(
            profile_id=session.get("active_profile", "guest"),
            video_id=video['id']
        )

        # If not watched, check if the video is in progress
        if not watched:
            in_progress = progress_mgr.read(
                profile_id=session.get("active_profile", "guest"),
                video_id=video['id']
            )

            current_time = in_progress[0]['current_time'] if in_progress else 0

    # Get similar videos
    with DatabaseContext() as db:
        similarity_mgr = SimilarityManager(db)
        similar_videos = similarity_mgr.get(
            video1_id=video_id,
        )

    if similar_videos:
        similar_videos = random.sample(
            similar_videos, min(3, len(similar_videos))
        )
    else:
        similar_videos = []

    video_ids = []
    for similar in similar_videos:
        if similar['video_2_id'] != video_id:
            id = similar['video_2_id']
        else:
            id = similar['video_1_id']

        with DatabaseContext() as db:
            video_mgr = VideoManager(db)
            video_details = video_mgr.get(id)
            if video_details:
                video_ids.append(video_details[0])
            else:
                print(f"Video with ID {id} not found in database.")

    return make_response(
        render_template(
            "video_details.html",
            video=video,
            categories=cat_list,
            tags=tags,
            speakers=speakers,
            characters=characters,
            scriptures=scriptures,
            similar_videos=video_ids,
            watched=watched,
            current_time=current_time,
        )
    )


@dynamic_bp.route(
    "/tag/<int:tag_id>",
    methods=["GET"],
)
def tag_details(
    tag_id: int,
) -> Response:
    """
    Render the details of a specific tag and the videos associated with it.

    Args:
        tag_id (int): The ID of the tag to fetch details for.

    Returns:
        Response: A rendered HTML page with tag details and associated videos.
        If the tag is not found, a 404 error is returned.
    """

    with DatabaseContext() as db:
        tag_mgr = TagManager(db)
        video_mgr = VideoManager(db)

        # Get the tag name from the tag ID
        tag = get_one_video(tag_mgr, tag_id, "Tag")
        if isinstance(tag, Response):
            return tag

        # Fetch videos associated with the tag
        videos = get_videos_by_filter(
            video_mgr, {"tag_id": tag_id}, "No videos found for this tag"
        )
        if isinstance(videos, Response):
            return videos

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        with LocalDbContext() as db:
            profile_mgr = ProfileManager(db)
            set_watched_status(videos, active_profile, profile_mgr)

    return make_response(
        render_template(
            "tag_details.html",
            tag=tag,
            videos=videos,
        )
    )


@dynamic_bp.route(
    "/speaker/<int:speaker_id>",
    methods=["GET"],
)
def speaker_details(
    speaker_id: int,
) -> Response:
    """
    Render the details of a specific speaker and the videos with them.

    Args:
        speaker_id (int): The ID of the speaker to fetch details for.

    Returns:
        Response: A rendered HTML page with speaker details and their videos.
        If the speaker is not found, a 404 error is returned.
    """

    with DatabaseContext() as db:
        speaker_mgr = SpeakerManager(db)
        video_mgr = VideoManager(db)

        # Get speaker details
        speaker = get_one_video(speaker_mgr, speaker_id, "Speaker")
        if isinstance(speaker, Response):
            return speaker

        # Fetch videos associated with the speaker
        videos = get_videos_by_filter(
            video_mgr,
            {"speaker_id": speaker_id},
            "No videos found for this speaker"
        )
        if isinstance(videos, Response):
            return videos

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        with LocalDbContext() as db:
            profile_mgr = ProfileManager(db)
            set_watched_status(videos, active_profile, profile_mgr)

    return make_response(
        render_template(
            "speaker_details.html",
            speaker=speaker,
            videos=videos,
        )
    )


@dynamic_bp.route(
    "/character/<int:character_id>",
    methods=["GET"],
)
def character_details(
    character_id: int,
) -> Response:
    """
    Render the details of a specific character and the videos their them.

    Args:
        character_id (int): The ID of the character to fetch details for.

    Returns:
        Response: A rendered HTML page with character details and their videos.
        If the character is not found, a 404 error is returned.
    """

    PIC_PATH = "/static/img/characters/"

    with DatabaseContext() as db:
        character_mgr = CharacterManager(db)
        video_mgr = VideoManager(db)

        # Get character details
        character = get_one_video(character_mgr, character_id, "Character")
        if isinstance(character, Response):
            return character
        if character.get('profile_pic'):
            character['profile_pic'] = f"{PIC_PATH}{character['profile_pic']}"

        # Fetch videos associated with the character
        videos = get_videos_by_filter(
            video_mgr,
            {"character_id": character_id},
            "No videos found for this character"
        )
        if isinstance(videos, Response):
            return videos

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        with LocalDbContext() as db:
            profile_mgr = ProfileManager(db)
            set_watched_status(videos, active_profile, profile_mgr)

    return make_response(
        render_template(
            "character_details.html",
            character=character,
            videos=videos,
        )
    )


@dynamic_bp.route(
    "/scripture/<int:scripture_id>",
    methods=["GET"],
)
def scripture_details(
    scripture_id: int,
) -> Response:
    """
    Render the details of a specific scripture and their videos.

    Args:
        scripture_id (int): The ID of the scripture to fetch details for.

    Returns:
        Response: A rendered HTML page with scripture details and their videos.
        If the scripture is not found, a 404 error is returned.
    """

    with DatabaseContext() as db:
        scripture_mgr = ScriptureManager(db)
        video_mgr = VideoManager(db)

        # Get scripture details
        scripture = get_one_video(scripture_mgr, scripture_id, "Scripture")
        if isinstance(scripture, Response):
            return scripture

        # Fetch videos associated with the scripture
        videos = get_videos_by_filter(
            video_mgr,
            {"scripture_id": scripture_id},
            "No videos found for this scripture"
        )
        if isinstance(videos, Response):
            return videos

        # Build a name for the scripture
        scripture['name'] = (
            f"{scripture['book']} {scripture['chapter']}:{scripture['verse']}"
        )

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        with LocalDbContext() as db:
            profile_mgr = ProfileManager(db)
            set_watched_status(videos, active_profile, profile_mgr)

    return make_response(
        render_template(
            "scripture_details.html",
            scripture=scripture,
            videos=videos,
        )
    )


@dynamic_bp.route(
    "/search",
    methods=["GET"],
)
def search_results() -> Response:
    """
    Render search results page for video searches.

    Query Parameters:
        q (str): The search query string.

    Returns:
        Response: A rendered HTML page with search results.
        If no query is provided, redirects to home page.
    """

    # Get the search query from the request
    query = request.args.get("q", "").strip()
    if not query:
        return make_response(
            render_template(
                "search_results.html",
                query="",
                videos=[],
                message="Please enter a search term."
            )
        )

    # Use the VideoManager to search for videos
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        videos = video_mgr.search(query=query)

    # If no videos found, return an empty list and a message
    if not videos:
        videos = []
        message = f"No videos found for '{query}'"

    # If videos are found, return them with a message
    else:
        message = f"Found {len(videos)} videos for '{query}'"

    # Check watched status for the videos
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

    return make_response(
        render_template(
            "search_results.html",
            query=query,
            videos=videos,
            message=message
        )
    )
