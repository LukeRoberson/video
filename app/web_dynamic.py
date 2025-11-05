"""
Module: web_dynamic.py

Defines a Flask blueprint for dynamic web routes.
    These are web pages that are based on an item, such as tag, speaker,
    bible chapter, or scripture.

Functions:
    - get_one_video:
        Fetches a single video or item from the database by ID.
    - get_videos_by_filter:
        Fetches videos based on filter criteria.
    - set_watched_status:
        Sets the watched status for each video in a list.
    - get_search_service:
        Retrieves or creates a SearchService instance.

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
    app.sql_db:
        DatabaseContext: Context manager for database operations.
        VideoManager: Manages videos.
        CategoryManager: Manages categories.
        TagManager: Manages tags.
        LocationManager: Manages locations.
        SpeakerManager: Manages speakers.
        CharacterManager: Manages Bible characters.
        ScriptureManager: Manages scriptures.
        SimilarityManager: Manages video similarity.

    app.local_db:
        LocalDbContext: Context manager for local database operations.
        ProfileManager: Manages user profiles.
        ProgressManager: Manages video progress.

    app.theme:
        ThemeManager: Manages theme-related operations.

    search:
        SearchService: Provides search functionality.
"""

# Standard library imports
from flask import (
    Blueprint,
    Response,
    render_template,
    make_response,
    request,
    session,
    current_app
)
from typing import Union
import random
import os
import logging

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
    SimilarityManager,
)
from app.local_db import (
    LocalDbContext,
    ProfileManager,
    ProgressManager,
)
from app.theme import ThemeManager
from search import SearchService


logger = logging.getLogger(__name__)


# Setup type variables for manager types
ManagerType = Union[
    VideoManager,
    TagManager,
    LocationManager,
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


def get_search_service() -> SearchService:
    """
    Get or create SearchService instance from application context.

    Args:
        None

    Returns:
        SearchService: Configured search service instance.
    """

    if 'SEARCH_SERVICE' not in current_app.config:
        current_app.config['SEARCH_SERVICE'] = SearchService()

    return current_app.config['SEARCH_SERVICE']


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

        # Fetch locations for the video
        loc_mgr = LocationManager(db)
        locations = loc_mgr.get_from_video(
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
    # Check for webVTT file for chapters
    vtt_file = os.path.join(
        str(current_app.static_folder),
        'vtt',
        f'{video_id}.vtt'
    )
    has_chapters = os.path.exists(vtt_file)
    print(vtt_file)

    return make_response(
        render_template(
            "video_details.html",
            video=video,
            categories=cat_list,
            tags=tags,
            locations=locations,
            speakers=speakers,
            characters=characters,
            scriptures=scriptures,
            similar_videos=video_ids,
            watched=watched,
            current_time=current_time,
            has_chapters=has_chapters,
            chapters_url=(
                f"/static/vtt/{video_id}.vtt"
                if has_chapters
                else None
            ),
        )
    )


@dynamic_bp.route(
    "/theme/<string:theme_name>",
    methods=["GET"],
)
def theme(
    theme_name: str,
) -> Response:
    """
    Render a theme page based on the theme name.

    Args:
        theme_name (str): The name of the theme to display.
            This represents a YAML file in the themes directory.

    Returns:
        Response: A rendered HTML page with the specified theme.
    """

    # The path to the theme file
    themes_folder = os.path.join(str(current_app.static_folder), 'themes')
    theme_file = os.path.join(themes_folder, f"{theme_name}.yaml")

    theme = ThemeManager()
    result = theme.load_theme(theme_file)

    # Check for errors loading the theme
    if result[0] is False:
        logging.error(f"Error loading theme: {result[1]}")
        return make_response(
            render_template(
                "errors/500.html",
                message=result[1]
            ),
            500
        )

    return make_response(
        render_template(
            "theme.html",
            title=theme.main['title'],
            main_heading=theme.main['heading'],
            sections=theme.sections,
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
        print(f"Tag details for tag_id {tag_id}: {tag}")
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
    "/location/<int:location_id>",
    methods=["GET"],
)
def location_details(
    location_id: int,
) -> Response:
    """
    Details of a specific location and the videos associated with it.

    Args:
        location_id (int): The ID of the location to fetch details for.

    Returns:
        Response:
            A rendered HTML page with location details and associated videos.
        If the location is not found, a 404 error is returned.
    """

    with DatabaseContext() as db:
        loc_mgr = LocationManager(db)
        video_mgr = VideoManager(db)

        # Get the tag name from the tag ID
        location = get_one_video(loc_mgr, location_id, "Location")
        if isinstance(location, Response):
            return location

        # Fetch videos associated with the tag
        videos = get_videos_by_filter(
            video_mgr,
            {"location_id": location_id},
            "No videos found for this location"
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
            "location_details.html",
            location=location,
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

    Integrates Elasticsearch with database fallback for searching videos.
    Supports both simple and advanced search with filters.

    Query Parameters:
        q (str): The search query string.
        page (int): The page number for pagination (default is 1).
        speakers (list): Speaker IDs to filter by (advanced search).
        characters (list): Character IDs to filter by (advanced search).
        locations (list): Location IDs to filter by (advanced search).
        tags (list): Tag IDs to filter by (advanced search).

    Returns:
        Response: A rendered HTML page with search results.
        If no query is provided, redirects to home page.
    """

    # Get the search query from the request
    query = request.args.get("q", "").strip()

    # Get advanced search filters
    filters = {}
    if request.args.get('speakers'):
        filters['speakers'] = request.args.getlist('speakers')
    if request.args.get('characters'):
        filters['characters'] = request.args.getlist('characters')
    if request.args.get('locations'):
        filters['locations'] = request.args.getlist('locations')
    if request.args.get('tags'):
        filters['tags'] = request.args.getlist('tags')

    # If no query but filters exist, use wildcard search
    if not query and filters:
        query = "*"

    if not query:
        return make_response(
            render_template(
                "search_results.html",
                query="",
                videos=[],
                message="Please enter a search term."
            )
        )

    # Get pagination parameter
    try:
        page = max(1, int(request.args.get('page', 1)))

    # Default to page 1 on error
    except ValueError:
        page = 1

    # Results per page
    per_page = 20

    # Initialize default values
    videos = []
    total = 0
    pages = 0
    using_elasticsearch = False
    message = "Enter a search term to find videos."

    if query:
        try:
            # Use SearchService for unified search
            search_service = get_search_service()
            (results, total), using_elasticsearch = search_service.search(
                query=query,
                page=page,
                per_page=per_page,
                filters=filters if filters else None
            )

            # Calculate pagination
            pages = (total + per_page - 1) // per_page

            # Convert results to video format for template
            videos = results

            # Add a badge to show which search method was used (ES or DB)
            if total > 0:
                method = (
                    "Elasticsearch"
                    if using_elasticsearch
                    else "database"
                )

                # Build filter description for message
                filter_desc = ""
                if filters:
                    filter_parts = []
                    if 'speakers' in filters:
                        filter_parts.append(
                            f"{len(filters['speakers'])} speaker(s)"
                        )
                    if 'characters' in filters:
                        filter_parts.append(
                            f"{len(filters['characters'])} character(s)"
                        )
                    if 'locations' in filters:
                        filter_parts.append(
                            f"{len(filters['locations'])} location(s)"
                        )
                    if 'tags' in filters:
                        filter_parts.append(
                            f"{len(filters['tags'])} tag(s)"
                        )
                    if filter_parts:
                        filter_desc = (
                            f" with filters: {', '.join(filter_parts)}"
                        )
                message = (
                    f"Found {total} video{'s' if total != 1 else ''} "
                    f"matching '{query}'{filter_desc} (using {method})"
                )

            else:
                message = f"No videos found matching '{query}'"

            # Log search operation
            if using_elasticsearch:
                logger.info(
                    f"✓ Elasticsearch search for '{query}': "
                    f"{total} results, page {page}/{pages}"
                )

            else:
                logger.warning(
                    f"⚠ Database fallback search for '{query}': "
                    f"{total} results, page {page}/{pages}"
                )

        except Exception as e:
            logger.error(
                f"Error during search: {e}",
                exc_info=True
            )
            message = "An error occurred while searching. Please try again."
            videos = []
            total = 0

    return make_response(
        render_template(
            'search_results.html',
            query=query,
            videos=videos,
            total=total,
            page=page,
            pages=pages,
            message=message,
            using_elasticsearch=using_elasticsearch
        )
    )


@dynamic_bp.route(
    "/search/advanced",
    methods=["GET"],
)
def advanced_search() -> Response:
    """
    Display advanced search page with filters and results.

    Supports searching with text query and multiple filter types.

    Query Parameters:
        q (str): Text search query (optional).
        speakers (list): Speaker IDs to filter by (optional).
        characters (list): Character IDs to filter by (optional).
        locations (list): Location IDs to filter by (optional).
        tags (list): Tag IDs to filter by (optional).
        page (int): Page number for pagination (default is 1).

    Returns:
        Rendered advanced search template with metadata options and results.
    """

    with DatabaseContext() as db:
        # Get speakers
        speaker_mgr = SpeakerManager(db)
        speakers = speaker_mgr.get() or []
        speakers = sorted(
            speakers, key=lambda spkr: spkr.get('name', '').lower()
        )

        # Get characters
        character_mgr = CharacterManager(db)
        characters = character_mgr.get() or []
        characters = sorted(
            characters, key=lambda char: char.get('name', '').lower()
        )

        # Get locations
        loc_mgr = LocationManager(db)
        locations = loc_mgr.get() or []
        locations = sorted(
            locations, key=lambda location: location.get('name', '').lower()
        )

        # Get tags
        tag_mgr = TagManager(db)
        tags = tag_mgr.get() or []
        tags = sorted(
            tags, key=lambda tag: tag.get('name', '').lower()
        )

    # Check if a search was performed
    query = request.args.get("q", "").strip()

    # Log all request parameters for debugging
    logger.info(f"All request parameters: {dict(request.args)}")

    # Get advanced search filters (IDs from form)
    filter_ids = {}
    if request.args.get('speakers'):
        filter_ids['speakers'] = request.args.getlist('speakers')
    if request.args.get('characters'):
        filter_ids['characters'] = request.args.getlist('characters')
    if request.args.get('locations'):
        filter_ids['locations'] = request.args.getlist('locations')
    if request.args.get('tags'):
        filter_ids['tags'] = request.args.getlist('tags')

    # Log received filter IDs
    logger.info(f"Received filter IDs from form: {filter_ids}")
    if not filter_ids:
        logger.warning("No filter IDs received despite request parameters")

    # Convert filter IDs to names for Elasticsearch
    filters = {}
    if filter_ids:
        # Convert speaker IDs to names
        if 'speakers' in filter_ids:
            logger.debug(
                f"Available speakers: "
                f"{[(s['id'], s['name']) for s in speakers[:5]]}"
            )
            speaker_names = [
                s['name'] for s in speakers
                if str(s['id']) in filter_ids['speakers']
            ]
            logger.info(f"Converted speaker IDs to names: {speaker_names}")
            if speaker_names:
                filters['speakers'] = speaker_names

        # Convert character IDs to names
        if 'characters' in filter_ids:
            logger.debug(
                f"Available characters: "
                f"{[(c['id'], c['name']) for c in characters[:5]]}"
            )
            character_names = [
                c['name'] for c in characters
                if str(c['id']) in filter_ids['characters']
            ]
            logger.info(f"Converted character IDs to names: {character_names}")
            if character_names:
                filters['characters'] = character_names

        # Convert location IDs to names
        if 'locations' in filter_ids:
            logger.debug(
                f"Available locations: "
                f"{[(loc['id'], loc['name']) for loc in locations[:5]]}"
            )
            location_names = [
                loc['name'] for loc in locations
                if str(loc['id']) in filter_ids['locations']
            ]
            logger.info(f"Converted location IDs to names: {location_names}")
            if location_names:
                filters['locations'] = location_names

        # Convert tag IDs to names
        if 'tags' in filter_ids:
            logger.debug(
                f"Available tags: "
                f"{[(t['id'], t['name']) for t in tags[:5]]}"
            )
            tag_names = [
                t['name'] for t in tags
                if str(t['id']) in filter_ids['tags']
            ]
            logger.info(f"Converted tag IDs to names: {tag_names}")
            if tag_names:
                filters['tags'] = tag_names

    logger.info(f"Final filters being sent to search: {filters}")

    # Initialize default values for results
    videos = []
    total = 0
    pages = 0
    page = 1
    using_elasticsearch = False
    message = None

    # Perform search if query or filters exist
    if query or filters:
        # If no query text but filters exist, use wildcard search
        search_query = query if query else "*"

        # Log the filters being applied
        if filters:
            logger.info(f"Advanced search filters applied: {filters}")

        # Get pagination parameter
        try:
            page = max(1, int(request.args.get('page', 1)))
        except ValueError:
            page = 1

        # Results per page
        per_page = 20

        try:
            # Use SearchService for unified search
            search_service = get_search_service()
            (results, total), using_elasticsearch = search_service.search(
                query=search_query,
                page=page,
                per_page=per_page,
                filters=filters if filters else None
            )

            # Calculate pagination
            pages = (total + per_page - 1) // per_page

            # Convert results to video format for template
            videos = results

            # Build message
            if total > 0:
                method = (
                    "Elasticsearch"
                    if using_elasticsearch
                    else "database"
                )

                # Build filter description for message
                filter_desc = ""
                if filters:
                    filter_parts = []
                    if 'speakers' in filters:
                        filter_parts.append(
                            f"{len(filters['speakers'])} speaker(s)"
                        )
                    if 'characters' in filters:
                        filter_parts.append(
                            f"{len(filters['characters'])} character(s)"
                        )
                    if 'locations' in filters:
                        filter_parts.append(
                            f"{len(filters['locations'])} location(s)"
                        )
                    if 'tags' in filters:
                        filter_parts.append(
                            f"{len(filters['tags'])} tag(s)"
                        )
                    if filter_parts:
                        filter_desc = (
                            f" with filters: {', '.join(filter_parts)}"
                        )

                query_text = f"'{query}'" if query else "all videos"
                message = (
                    f"Found {total} video{'s' if total != 1 else ''} "
                    f"matching {query_text}{filter_desc} (using {method})"
                )
            else:
                query_text = f"'{query}'" if query else "your criteria"
                message = f"No videos found matching {query_text}"

            # Log search operation
            if using_elasticsearch:
                logger.info(
                    f"✓ Advanced Elasticsearch search: "
                    f"{total} results, page {page}/{pages}"
                )
            else:
                logger.warning(
                    f"⚠ Advanced database search: "
                    f"{total} results, page {page}/{pages}"
                )

        except Exception as e:
            logger.error(
                f"Error during advanced search: {e}",
                exc_info=True
            )
            message = "An error occurred while searching. Please try again."
            videos = []
            total = 0

    return make_response(
        render_template(
            "advanced_search.html",
            speakers=speakers,
            characters=characters,
            locations=locations,
            tags=tags,
            videos=videos,
            total=total,
            page=page,
            pages=pages,
            message=message,
            query=query,
            using_elasticsearch=using_elasticsearch,
        )
    )
