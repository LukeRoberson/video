"""
Module: web_dynamic.py

Defines a Flask blueprint for dynamic web routes.
    These are web pages that are based on an item, such as tag, speaker,
    bible chapter, or scripture.

Routes:

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
)


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
        print("Video Details:", video)

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

    # Check if the video is marked as watched by the user
    with LocalDbContext() as local_db:
        profile_mgr = ProfileManager(local_db)
        watched = profile_mgr.check_watched(
            profile_id=session.get("active_profile", "guest"),
            video_id=video['id']
        )

    # Dummy data for similar videos
    print("Video Details:", video)
    similar_videos = [
        {
            "title": "Similar Video 1",
            "thumb": """
            https://assetsnffrgf-a.akamaihd.net/assets/m/502015535/univ/art/502015535_univ_lss_lg.jpg
            """
        },
        {
            "title": "Similar Video 2",
            "thumb": """
            https://assetsnffrgf-a.akamaihd.net/assets/m/jwb/univ/201801/art/jwb_univ_201801_lss_02_lg.jpg
            """
        },
        {
            "title": "Similar Video 3",
            "thumb": """
            https://assetsnffrgf-a.akamaihd.net/assets/m/mwbv/univ/202203/art/mwbv_univ_202203_lss_03_lg.jpg
            """
        },
    ]

    return make_response(
        render_template(
            "video_details.html",
            video=video,
            categories=cat_list,
            tags=tags,
            speakers=speakers,
            characters=characters,
            scriptures=scriptures,
            similar_videos=similar_videos,
            watched=watched,
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
        tag = tag_mgr.get(id=tag_id)
        if tag:
            tag = tag[0]
        else:
            return make_response(
                render_template(
                    "404.html",
                    message="Tag not found"
                ),
                404
            )

        # Fetch videos associated with the tag
        videos = video_mgr.get_filter(
            tag_id=tag_id
        )
        if not videos:
            return make_response(
                render_template(
                    "404.html",
                    message="No videos found for this tag"
                ),
                404
            )

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
        speaker = speaker_mgr.get(id=speaker_id)
        if speaker:
            speaker = speaker[0]
        else:
            return make_response(
                render_template(
                    "404.html",
                    message="Speaker not found"
                ),
                404
            )

        # Fetch videos associated with the speaker
        videos = video_mgr.get_filter(
            speaker_id=speaker_id
        )
        if not videos:
            return make_response(
                render_template(
                    "404.html",
                    message="No videos found for this speaker"
                ),
                404
            )

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
    videos = []

    with DatabaseContext() as db:
        character_mgr = CharacterManager(db)
        video_mgr = VideoManager(db)

        # Get character details
        character = character_mgr.get(id=character_id)
        if character:
            character = character[0]
            if character['profile_pic']:
                character['profile_pic'] = (
                    f"{PIC_PATH}{character['profile_pic']}"
                )
        else:
            return make_response(
                render_template(
                    "404.html",
                    message="Character not found"
                ),
                404
            )

        # Fetch videos associated with the character
        videos = video_mgr.get_filter(
            character_id=character_id
        )
        if not videos:
            return make_response(
                render_template(
                    "404.html",
                    message="No videos found for this character"
                ),
                404
            )

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
        scripture = scripture_mgr.get(id=scripture_id)
        if scripture:
            scripture = scripture[0]
        else:
            return make_response(
                render_template(
                    "404.html",
                    message="Scripture not found"
                ),
                404
            )

        # Fetch videos associated with the scripture
        videos = video_mgr.get_filter(
            scripture_id=scripture_id
        )
        if not videos:
            return make_response(
                render_template(
                    "404.html",
                    message="No videos found for this scripture"
                ),
                404
            )

        # Build a name for the scripture
        scripture['name'] = (
            f"{scripture['book']} {scripture['chapter']}:{scripture['verse']}"
        )

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
