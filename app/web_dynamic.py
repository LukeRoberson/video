"""
Module: web_dynamic.py

Defines a Flask blueprint for dynamic web routes.
    These are web pages that are based on an item, such as tag, speaker,
    bible chapter, or scripture.

Functions:
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
import random
import os
import logging

# Custom imports
from app.theme import ThemeManager
import requests


logger = logging.getLogger(__name__)

# Configuration for search API
SEARCH_API_BASE_URL = 'http://localhost:5010'


def set_watched_status(
    videos: list,
    profile_id: int,
) -> None:
    """
    Check each video in the list to see if it has been watched by the user.
    If it has, mark it as watched by adding a 'watched' key with value True.
    This is used to display a watched badge on the video thumbnails.

    Args:
        videos (list):
            A list of video dictionaries to update with watched status.
        profile_id (int):
            The ID of the user profile to check watched status against.

    Returns:
        None: The function modifies the videos list in place.
    """

    # Loop through each video and check if it has been watched
    for video in videos:
        # API: Check if video is marked as watched
        response = requests.get(
            'http://localhost:5010/api/profile/mark_watched',
            params={
                'video_id': video['id'],
                'profile': profile_id
            },
        )

        # Set the 'watched' key to True or False
        video['watched'] = response.json()['data'].get('watched', False)


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

    # API: Fetch video details
    body = {
        'video_ids': [video_id]
    }
    response = requests.post(
        "http://localhost:5010/api/videos/get_bulk",
        json=body
    )
    video = response.json().get('data', [])

    if video is None or len(video) == 0:
        return make_response(
            render_template(
                "404.html",
                message="Video not found in API"
            ),
            404
        )

    video = video[0]

    # API: Get categories for the video
    response = requests.get(
        f'http://localhost:5010/api/categories/video/{video_id}',
    )
    cat_list = response.json().get('data', {})

    # API: Get tags for the video
    response = requests.get(
        f'http://localhost:5010/api/tags/video/{video_id}',
    )
    tags = response.json().get('data', {})

    # API: Get locations for the video
    response = requests.get(
        f'http://localhost:5010/api/locations/video/{video_id}',
    )
    locations = response.json().get('data', [])

    # API: Get speakers for the video
    response = requests.get(
        f'http://localhost:5010/api/speakers/video/{video_id}',
    )
    speakers = response.json().get('data', [])

    # API: Get characters for the video
    response = requests.get(
        f'http://localhost:5010/api/characters/video/{video_id}',
    )
    characters = response.json().get('data', {})

    # API: Get scriptures for the video
    response = requests.get(
        f'http://localhost:5010/api/scriptures/video/{video_id}',
    )
    scriptures = response.json().get('data', [])

    # API: Check if video is marked as watched
    response = requests.get(
        'http://localhost:5010/api/profile/mark_watched',
        params={
            'video_id': video_id,
            'profile': session.get("active_profile", "guest")
        }
    )
    watched = response.json()['data'].get('watched', False)

    # API: Check if video is in progress
    response = requests.get(
        'http://localhost:5010/api/profile/in_progress',
        params={
            'video_id': video_id,
            'profile': session.get("active_profile", "guest")
        }
    )
    payload = response.json().get('data', [])

    if payload:
        current_time = response.json()['data'][0].get('current_time', 0)
    else:
        current_time = 0

    # API: Get a list of similar videos
    response = requests.get(
        f'http://localhost:5010/api/similarity/{video_id}',
    )
    if response.status_code == 200:
        similar_videos = response.json().get('data', [])
    else:
        similar_videos = None

    # Randomly select up to 3 similar videos to display
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

        # Get details for the similar video
        body = {
            'video_ids': [id]
        }
        response = requests.post(
            "http://localhost:5010/api/videos/get_bulk",
            json=body
        )

        if response.status_code == 200:
            video_details = response.json().get('data', [])
            if len(video_details) > 0:
                video_ids.append(video_details[0])

        else:
            print(f"Video with ID {id} not found in API.")

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

    # API: Get tag details
    param = {
        'tag_id': tag_id
    }
    response = requests.get(
        'http://localhost:5010/api/tags',
        params=param
    )

    if response.status_code == 200:
        tag = response.json().get('data', {})
        if len(tag) == 0:
            return make_response(
                render_template(
                    "404.html",
                    message="Tag not found in API"
                ),
                404
            )
        tag = tag[0]

    else:
        return make_response(
            render_template(
                "404.html",
                message="Tag not found in API"
            ),
            404
        )

    # API: Fetch videos for the tag
    response = requests.get(
        'http://localhost:5010/api/videos/filter',
        params={
            'tag': tag_id
        },
    )
    if response.status_code == 200:
        videos = response.json().get('data', [])
    else:
        return make_response(
            render_template(
                "404.html",
                message="No videos found for this tag"
            ),
            404
        )

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        set_watched_status(videos, active_profile)

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

    # API: Get locations
    param = {
        'loc_id': location_id
    }
    response = requests.get(
        'http://localhost:5010/api/locations',
        params=param
    )

    if response.status_code == 200:
        location = response.json().get('data', [])
        if len(location) == 0:
            return make_response(
                render_template(
                    "404.html",
                    message="Location not found in API"
                ),
                404
            )
        location = location[0]

    else:
        logger.debug("Module: web_dynamic.py, Function: location_details")
        logger.error(
            f"Problems with API call to get location with ID {location_id}"
        )

        return make_response(
            render_template(
                "500.html",
                message="Problems with API call to get location"
            ),
            500
        )

    # Just the first item in the list since we are searching by ID
    if len(location) > 0:
        location = location[0]

    else:
        logger.debug("Module: web_dynamic.py, Function: location_details")
        logger.warning(f"Location with ID {location_id} not found in API")

        return make_response(
            render_template(
                "404.html",
                message="Location not found in API"
            ),
            404
        )

    # API: Fetch videos for the location
    response = requests.get(
        'http://localhost:5010/api/videos/filter',
        params={
            'loc': location_id
        },
    )
    if response.status_code == 200:
        videos = response.json().get('data', [])
    else:
        return make_response(
            render_template(
                "404.html",
                message="No videos found for this location"
            ),
            404
        )

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        set_watched_status(videos, active_profile)

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

    # API: Get speaker
    param = {
        'spk_id': speaker_id
    }
    response = requests.get(
        'http://localhost:5010/api/speakers',
        params=param
    )

    if response.status_code == 200:
        speaker = response.json().get('data', [])
        if len(speaker) > 0:
            speaker = speaker[0]
        else:
            return make_response(
                render_template(
                    "404.html",
                    message="Speaker not found in API"
                ),
                404
            )

    else:
        return make_response(
            render_template(
                "404.html",
                message="Speaker not found in API"
            ),
            404
        )

    # API: Fetch videos associated with the speaker
    response = requests.get(
        'http://localhost:5010/api/videos/filter',
        params={
            'speak': speaker_id
        },
    )
    if response.status_code == 200:
        videos = response.json().get('data', [])
    else:
        return make_response(
            render_template(
                "404.html",
                message="No videos found for this speaker"
            ),
            404
        )

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        set_watched_status(videos, active_profile)

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

    # API: Get character details
    param = {
        'char_id': character_id
    }
    response = requests.get(
        'http://localhost:5010/api/characters',
        params=param
    )
    if response.status_code == 200:
        character = response.json().get('data', [])[0]
    else:
        return make_response(
            render_template(
                "404.html",
                message="Character not found in API"
            ),
            404
        )

    # If the character has a profile picture, add the path to it
    if character.get('profile_pic'):
        character['profile_pic'] = f"{PIC_PATH}{character['profile_pic']}"

    # API: Fetch videos for the character
    response = requests.get(
        'http://localhost:5010/api/videos/filter',
        params={
            'char': character_id
        },
    )
    if response.status_code == 200:
        videos = response.json().get('data', [])
    else:
        return make_response(
            render_template(
                "404.html",
                message="No videos found for this character"
            ),
            404
        )

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        set_watched_status(videos, active_profile)

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

    # API: Get the scripture
    param = {
        'scr_id': scripture_id
    }
    response = requests.get(
        'http://localhost:5010/api/scriptures',
        params=param
    )

    # Get a single scripture from the list since we are searching by ID
    if response.status_code == 200:
        scripture = response.json().get('data', [])
        if len(scripture) > 0:
            scripture = scripture[0]

    else:
        return make_response(
            render_template(
                "404.html",
                message="Scripture not found in API"
            ),
            404
        )

    # Build a name for the scripture
    scripture['name'] = (
        f"{scripture['book']} {scripture['chapter']}:{scripture['verse']}"
    )

    # API: Fetch videos for the scripture
    response = requests.get(
        'http://localhost:5010/api/videos/filter',
        params={
            'scrip': scripture_id
        },
    )
    if response.status_code == 200:
        videos = response.json().get('data', [])
    else:
        return make_response(
            render_template(
                "404.html",
                message="No videos found for this scripture"
            ),
            404
        )

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        set_watched_status(videos, active_profile)

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
            # Make API call to search endpoint
            api_url = f'{SEARCH_API_BASE_URL}/api/search/advanced'
            params = {
                'query': query,
                'page': page,
                'per_page': per_page
            }

            # Add filters if they exist
            if filters:
                for filter_type, filter_values in filters.items():
                    params[filter_type] = filter_values

            logger.info(f"Calling search API: {api_url} with params: {params}")

            response = requests.get(api_url, params=params)

            if response.status_code == 200:
                data = response.json().get('data', {})
                videos = data.get('results', [])
                total = data.get('total', 0)
                pages = data.get('pages', 0)
                using_elasticsearch = data.get('using_elasticsearch', False)

            else:
                logger.warning(
                    f"Search API returned error: {response.status_code}"
                )

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
                    f"Elasticsearch search for '{query}': "
                    f"{total} results, page {page}/{pages}"
                )

            else:
                logger.warning(
                    f"Database fallback search for '{query}': "
                    f"{total} results, page {page}/{pages}"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling search API: {e}", exc_info=True)
            message = "Unable to connect to search service. Please try again."

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

    # API: Get speakers
    response = requests.get(
        'http://localhost:5010/api/speakers',
    )
    if response.status_code == 200:
        speakers = response.json().get('data', [])
    else:
        logger.error("Failed to fetch speakers from API")
        speakers = []

    # API: Get characters
    response = requests.get(
        'http://localhost:5010/api/characters',
    )
    if response.status_code == 200:
        characters = response.json().get('data', [])
    else:
        logger.error("Failed to fetch characters from API")
        characters = []

    # API: Get locations
    response = requests.get(
        'http://localhost:5010/api/locations',
    )
    if response.status_code == 200:
        locations = response.json().get('data', [])
    else:
        logger.error("Failed to fetch locations from API")
        locations = []

    # API: Get tags
    response = requests.get(
        'http://localhost:5010/api/tags',
    )
    if response.status_code == 200:
        tags = response.json().get('data', [])
    else:
        logger.error("Failed to fetch tags from API")
        tags = []

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
            # Make API call to advanced search endpoint
            api_url = f'{SEARCH_API_BASE_URL}/api/search/advanced'
            params = {
                'query': search_query,
                'page': page,
                'per_page': per_page
            }

            # Add filters if they exist
            if filters:
                for filter_type, filter_values in filters.items():
                    params[filter_type] = filter_values

            response = requests.get(api_url, params=params)

            if response.status_code == 200:
                data = response.json().get('data', {})
                videos = data.get('results', [])
                total = data.get('total', 0)
                pages = data.get('pages', 0)
                using_elasticsearch = data.get('using_elasticsearch', False)

            else:
                logger.error(f"Error during API call: {response.status_code}")
                videos = []
                total = 0
                pages = 0
                using_elasticsearch = False

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
                    f"Advanced Elasticsearch search: "
                    f"{total} results, page {page}/{pages}"
                )
            else:
                logger.warning(
                    f"Advanced database search: "
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
