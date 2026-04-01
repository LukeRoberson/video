"""
Module: web_dynamic.py

Defines a Flask blueprint for dynamic web routes.
    These are web pages that are based on an item, such as tag, speaker,
    bible chapter, or scripture.

Functions:
    - check_watch_status:
        Checks if videos in a list have been watched by the user.
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
    requests: For making API calls to fetch data for the pages.
    ThreadPoolExecutor: For concurrent API calls.

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
from concurrent.futures import ThreadPoolExecutor
import random
import os
import logging

# Custom imports
from app.theme import ThemeManager
import requests


logger = logging.getLogger(__name__)

# Configuration
SEARCH_API_BASE_URL = 'http://localhost:5010'
PIC_PATH = "/static/img/characters/"


def check_watch_status(
    video_list: list,
    profile_id: int
) -> None:
    """
    Check videos in a list to see if they have been watched by the user.
    If is has, mark them as watched by adding a 'watched' key with value True.
    This is used to display a watched badge on the video thumbnails.

    Args:
        video_list (list):
            A list of video IDs to check watched status for.
            These will contain video IDs and other metadata.
        profile_id (int):
            The ID of the user profile to check watched status against.

    Returns:
        None: The function modifies the video_list in place.
    """

    # Extract video IDs from the video list
    video_ids = [video['id'] for video in video_list]

    # API call to check status of multiple videos at once
    response = requests.post(
        url='http://localhost:5010/api/profile/mark_watched_bulk',
        params={
            'profile': profile_id
        },
        json={
            'video_ids': video_ids
        }
    )

    if response.status_code == 200:
        watched_data = response.json().get('data', {})
        for video in video_list:
            video['watched'] = watched_data.get(str(video['id']), False)
        logger.warning(video_list)

    else:
        logger.error(
            f"Failed to fetch watched status for videos: "
            f"{response.status_code}"
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

    Functions:
        - get_video_details:
            Fetches the details of a video from the API.
        - get_video_categories:
            Fetches the categories associated with a video from the API.
        - get_video_tags:
            Fetches the tags associated with a video from the API.
        - get_video_locations:
            Fetches the locations associated with a video from the API.
        - get_video_speakers:
            Fetches the speakers associated with a video from the API.
        - get_video_characters:
            Fetches the characters associated with a video from the API.
        - get_video_scriptures:
            Fetches the scriptures associated with a video from the API.
        - get_watch_status:
            Checks if the video has been watched by the user from the API.
        - get_watch_time:
            Gets the current time for the video from the API.
        - get_similar_videos:
            Fetches a list of similar videos from the API.

    Args:
        video_id (int): The ID of the video to fetch details for.

    Returns:
        Response: A rendered HTML page with video details,
            tags, speakers, characters, scriptures, and similar videos.
        If the video is not found, a 404 error is returned.
    """

    def get_video_details() -> dict | None:
        """
        Fetch the details of a specific video from the API.

        Returns:
            dict: A dictionary containing video details if found,
            else None.
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
            video = None
        else:
            video = video[0]

        return video

    def get_video_categories() -> dict | None:
        """
        Fetch the categories associated with a specific video from the API.

        Returns:
            list: A list of categories if found,
            else None.
        """

        # API: Get categories for the video
        response = requests.get(
            f'http://localhost:5010/api/categories/video/{video_id}',
        )
        if response.status_code == 200:
            cat_list = response.json().get('data', {})
        else:
            cat_list = None

        return cat_list

    def get_video_tags() -> dict | None:
        """
        Fetch the tags associated with a specific video from the API.

        Returns:
            list: A list of tags if found,
            else None.
        """

        # API: Get tags for the video
        response = requests.get(
            f'http://localhost:5010/api/tags/video/{video_id}',
        )
        if response.status_code == 200:
            tags = response.json().get('data', {})
        else:
            tags = None

        return tags

    def get_video_locations() -> dict | None:
        """
        Fetch the locations associated with a specific video from the API.

        Returns:
            list: A list of locations if found,
            else None.
        """

        # API: Get locations for the video
        response = requests.get(
            f'http://localhost:5010/api/locations/video/{video_id}',
        )
        if response.status_code == 200:
            locations = response.json().get('data', {})
        else:
            locations = None

        return locations

    def get_video_speakers() -> dict | None:
        """
        Fetch the speakers associated with a specific video from the API.

        Returns:
            list: A list of speakers if found,
            else None.
        """

        # API: Get speakers for the video
        response = requests.get(
            f'http://localhost:5010/api/speakers/video/{video_id}',
        )
        if response.status_code == 200:
            speakers = response.json().get('data', {})
        else:
            speakers = None

        logging.warning(f"Speakers for video {video_id}: {speakers}")

        return speakers

    def get_video_characters() -> dict | None:
        """
        Fetch the characters associated with a specific video from the API.

        Returns:
            list: A list of characters if found,
            else None.
        """

        # API: Get characters for the video
        response = requests.get(
            f'http://localhost:5010/api/characters/video/{video_id}',
        )
        if response.status_code == 200:
            characters = response.json().get('data', {})
        else:
            characters = None

        return characters

    def get_video_scriptures() -> dict | None:
        """
        Fetch the scriptures associated with a specific video from the API.

        Returns:
            list: A list of scriptures if found,
            else None.
        """

        # API: Get scriptures for the video
        response = requests.get(
            f'http://localhost:5010/api/scriptures/video/{video_id}',
        )
        if response.status_code == 200:
            scriptures = response.json().get('data', {})
        else:
            scriptures = None

        return scriptures

    def get_watch_status() -> bool:
        """
        Check if the video has been watched by the user.

        Returns:
            bool: True if the video has been watched, else False.
        """

        response = requests.post(
            'http://localhost:5010/api/profile/mark_watched_bulk',
            params={
                'profile': profile_id
            },
            json={'video_ids': [video_id]}
        )

        if response.status_code == 200:
            data = response.json().get('data', {})
            return data.get(str(video_id), False)
        else:
            logger.error(
                f"Failed to fetch watched status for video {video_id}: "
                f"{response.status_code}"
            )
            return False

    def get_watch_time() -> int:
        """
        If the video is in progress, get the current time for the video.

        Returns:
            int: The current time in seconds if the video is in progress,
            else 0.
        """

        response = requests.get(
            'http://localhost:5010/api/profile/in_progress',
            params={
                'video_id': video_id,
                'profile': profile_id
            }
        )
        payload = response.json().get('data', [])

        if payload:
            return payload[0].get('current_time', 0)
        else:
            return 0

    def get_similar_videos() -> list | None:
        """
        Fetch a list of similar videos from the API.

        Returns:
            list: A list of similar videos if found,
            else None.
        """

        # API: Get a list of similar videos
        response = requests.get(
            f'http://localhost:5010/api/similarity/{video_id}',
        )
        if response.status_code == 200:
            similar_videos = response.json().get('data', [])
        else:
            similar_videos = None

        if similar_videos is None or len(similar_videos) == 0:
            return None

        # Pick three videos at random, and get their IDs
        sample = random.sample(similar_videos, min(3, len(similar_videos)))
        ids = [
            s['video_2_id'] if s['video_2_id'] != video_id else s['video_1_id']
            for s in sample
        ]

        # Get the details for the similar videos
        response = requests.post(
            'http://localhost:5010/api/videos/get_bulk',
            json={'video_ids': ids}
        )

        if response.status_code == 200:
            video_ids = response.json().get('data', [])
        else:
            logger.error(
                f"Failed to fetch details for similar videos: "
                f"{response.status_code}"
            )
            video_ids = []

        return video_ids

    # Manage profile ID or guest
    profile_id = session.get("active_profile", None)
    future_watch_status = None
    future_watch_time = None

    # Concurrent API calls
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_video_details = executor.submit(get_video_details)
        future_video_categories = executor.submit(get_video_categories)
        future_video_tags = executor.submit(get_video_tags)
        future_video_locations = executor.submit(get_video_locations)
        future_video_speakers = executor.submit(get_video_speakers)
        future_video_characters = executor.submit(get_video_characters)
        future_video_scriptures = executor.submit(get_video_scriptures)
        future_similar_videos = executor.submit(get_similar_videos)

        # Skip this for the guest profile
        if profile_id is not None and profile_id != "guest":
            future_watch_status = executor.submit(get_watch_status)
            future_watch_time = executor.submit(get_watch_time)

    # Get the results
    video = future_video_details.result()
    cat_list = future_video_categories.result()
    tags = future_video_tags.result()
    locations = future_video_locations.result()
    speakers = future_video_speakers.result()
    characters = future_video_characters.result()
    scriptures = future_video_scriptures.result()
    video_ids = future_similar_videos.result()

    # Get these results if the user is not a guest
    if future_watch_status is not None and future_watch_time is not None:
        watched = future_watch_status.result()
        current_time = future_watch_time.result()
    else:
        watched = False
        current_time = 0

    # Validate video details
    if video is None:
        return make_response(
            render_template(
                "errors/404.html",
                message="Video not found"
            ),
            404
        )

    # Check for webVTT file for chapters
    vtt_file = os.path.join(
        str(current_app.static_folder),
        'vtt',
        f'{video_id}.vtt'
    )
    has_chapters = os.path.exists(vtt_file)

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
            video_cache=theme.video_cache,
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

    Functions:
        - get_tag_details:
            Fetches the details of a specific tag from the API.
        - get_tag_videos:
            Fetches the videos associated with a tag from the API.

    Args:
        tag_id (int): The ID of the tag to fetch details for.

    Returns:
        Response: A rendered HTML page with tag details and associated videos.
        If the tag is not found, a 404 error is returned.
    """

    def get_tag_details() -> dict | None:
        """
        Fetch the details of a specific tag from the API.

        Returns:
            dict:
                A dictionary containing tag details if found,
                else None.
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
                tag = None
            else:
                tag = tag[0]

        else:
            tag = None

        return tag

    def get_tag_videos() -> list | None:
        """
        Fetch the videos associated with a specific tag from the API.

        Returns:
            list: A list of videos if found,
            else None.
        """

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
            videos = None

        return videos

    # Concurrent API calls
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_tag_details = executor.submit(get_tag_details)
        future_tag_videos = executor.submit(get_tag_videos)

    # Get the results
    tag = future_tag_details.result()
    videos = future_tag_videos.result()

    # Validate tag details
    if tag is None:
        return make_response(
            render_template(
                "errors/404.html",
                message="Tag not found in API"
            ),
            404
        )

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest" and videos is not None:
        check_watch_status(videos, active_profile)

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

    Functions:
        - get_location_details:
            Fetches the details of a specific location from the API.
        - get_location_videos:
            Fetches the videos associated with a location from the API.

    Args:
        location_id (int): The ID of the location to fetch details for.

    Returns:
        Response:
            A rendered HTML page with location details and associated videos.
        If the location is not found, a 404 error is returned.
    """

    def get_location_details() -> dict | None:
        """
        Fetch the details of a specific location from the API.

        Returns:
            dict:
                A dictionary containing location details if found,
                else None.
        """

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
                location = None
            else:
                location = location[0]

        else:
            location = None

        return location

    def get_location_videos() -> list | None:
        """
        Fetch the videos associated with a specific location from the API.

        Returns:
            list: A list of videos if found,
            else None.
        """

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
            videos = None

        return videos

    # Concurrent API calls
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_location_details = executor.submit(get_location_details)
        future_location_videos = executor.submit(get_location_videos)

    # Get the results
    location = future_location_details.result()
    videos = future_location_videos.result()

    # Validate location details
    if location is None:
        logger.debug("Module: web_dynamic.py, Function: location_details")
        logger.error(
            f"Problems with API call to get location with ID {location_id}"
        )

        return make_response(
            render_template(
                "errors/404.html",
                message="Location could not be found"
            ),
            404
        )

    # API: Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest" and videos is not None:
        check_watch_status(videos, active_profile)

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

    Functions:
        - get_speaker_details:
            Fetches the details of a specific speaker from the API.
        - get_speaker_videos:
            Fetches the videos associated with a speaker from the API.

    Args:
        speaker_id (int): The ID of the speaker to fetch details for.

    Returns:
        Response: A rendered HTML page with speaker details and their videos.
        If the speaker is not found, a 404 error is returned.
    """

    def get_speaker_details() -> dict | None:
        """
        Fetch the details of a specific speaker from the API.

        Returns:
            dict:
                A dictionary containing speaker details if found,
                else None.
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
                speaker = None
        else:
            speaker = None

        return speaker

    def get_speaker_videos() -> list | None:
        """
        Fetch the videos associated with a specific speaker from the API.

        Returns:
            list: A list of videos if found,
            else None.
        """

        # API: Fetch videos for the speaker
        response = requests.get(
            'http://localhost:5010/api/videos/filter',
            params={
                'speak': speaker_id
            },
        )
        if response.status_code == 200:
            videos = response.json().get('data', [])
        else:
            videos = None

        return videos

    # Concurrent API calls
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_speaker_details = executor.submit(get_speaker_details)
        future_speaker_videos = executor.submit(get_speaker_videos)

    # Get the results
    speaker = future_speaker_details.result()
    videos = future_speaker_videos.result()

    # Validate speaker details
    if speaker is None:
        return make_response(
            render_template(
                "errors/404.html",
                message="Speaker not found in API"
            ),
            404
        )

    # API: Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest" and videos is not None:
        check_watch_status(videos, active_profile)

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

    Functions:
        - get_char_details:
            Fetches the details of a specific character from the API.
        - get_char_videos:
            Fetches the videos associated with a character from the API.

    Args:
        character_id (int): The ID of the character to fetch details for.

    Returns:
        Response: A rendered HTML page with character details and their videos.
        If the character is not found, a 404 error is returned.
    """

    def get_char_details() -> dict | None:
        """
        Fetch the details of a specific character from the API.

        Returns:
            dict:
                A dictionary containing character details if found,
                else None.
        """

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
            character = None
        return character

    def get_char_videos() -> list | None:
        """
        Fetch the videos associated with a specific character from the API.

        Returns:
            list: A list of videos if found,
            else None.
        """

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
            videos = None

        return videos

    # Concurrent API calls
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_char_details = executor.submit(get_char_details)
        future_char_videos = executor.submit(get_char_videos)

    # Get the results
    character = future_char_details.result()
    videos = future_char_videos.result()

    # Validate character details
    if character is None:
        return make_response(
            render_template(
                "errors/404.html",
                message="Character not found in API"
            ),
            404
        )

    # Validate videos
    if videos is None:
        return make_response(
            render_template(
                "errors/404.html",
                message="No videos found for this character"
            ),
            404
        )

    # If the character has a profile picture, add the path to it
    if character.get('profile_pic'):
        character['profile_pic'] = f"{PIC_PATH}{character['profile_pic']}"

    # API call: Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest":
        check_watch_status(videos, active_profile)

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

    Functions:
        - get_scripture_details:
            Fetches the details of a specific scripture from the API.
        - get_scripture_videos:
            Fetches the videos associated with a scripture from the API.

    Args:
        scripture_id (int): The ID of the scripture to fetch details for.

    Returns:
        Response: A rendered HTML page with scripture details and their videos.
        If the scripture is not found, a 404 error is returned.
    """

    def get_scripture_details() -> dict | None:
        """
        Fetch the details of a specific scripture from the API.

        Returns:
            dict:
                A dictionary containing scripture details if found,
                else None.
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
            scripture = None

        return scripture

    def get_scripture_videos() -> list | None:
        """
        Fetch the videos associated with a specific scripture from the API.

        Returns:
            list: A list of videos if found,
            else None.
        """

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
            videos = None

        return videos

    # Concurrent API calls
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_scripture_details = executor.submit(get_scripture_details)
        future_scripture_videos = executor.submit(get_scripture_videos)

    # Get the results
    scripture = future_scripture_details.result()
    videos = future_scripture_videos.result()

    # Validate scripture details
    if scripture is None:
        return make_response(
            render_template(
                "errors/404.html",
                message="Scripture not found in API"
            ),
            404
        )

    # Build a name for the scripture
    scripture['name'] = (
        f"{scripture['book']} {scripture['chapter']}:{scripture['verse']}"
    )

    # Check watched status for the videos
    active_profile = session.get("active_profile", None)
    if active_profile and active_profile != "guest" and videos is not None:
        check_watch_status(videos, active_profile)

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

    Functions:
        - get_speakers: Fetches the list of speakers from the API.
        - get_characters: Fetches the list of characters from the API.
        - get_locations: Fetches the list of locations from the API.
        - get_tags: Fetches the list of tags from the API.

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

    def get_speakers() -> list:
        """
        Fetch the list of speakers from the API.

        Returns:
             list: A list of speakers if found, else an empty list.
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

        return speakers

    def get_characters() -> list:
        """
        Fetch the list of characters from the API.

        Returns:
             list: A list of characters if found, else an empty list.
        """

        # API: Get characters
        response = requests.get(
            'http://localhost:5010/api/characters',
        )

        if response.status_code == 200:
            characters = response.json().get('data', [])
        else:
            logger.error("Failed to fetch characters from API")
            characters = []

        return characters

    def get_locations() -> list:
        """
        Fetch the list of locations from the API.

        Returns:
             list: A list of locations if found, else an empty list.
        """

        # API: Get locations
        response = requests.get(
            'http://localhost:5010/api/locations',
        )

        if response.status_code == 200:
            locations = response.json().get('data', [])
        else:
            logger.error("Failed to fetch locations from API")
            locations = []

        return locations

    def get_tags() -> list:
        """
        Fetch the list of tags from the API.

        Returns:
             list: A list of tags if found, else an empty list.
        """

        # API: Get tags
        response = requests.get(
            'http://localhost:5010/api/tags',
        )

        if response.status_code == 200:
            tags = response.json().get('data', [])
        else:
            logger.error("Failed to fetch tags from API")
            tags = []

        return tags

    # Concurrently fetch metadata for filters to speed up page load
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_speakers = executor.submit(get_speakers)
        future_characters = executor.submit(get_characters)
        future_locations = executor.submit(get_locations)
        future_tags = executor.submit(get_tags)

    speakers = future_speakers.result()
    characters = future_characters.result()
    locations = future_locations.result()
    tags = future_tags.result()

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
