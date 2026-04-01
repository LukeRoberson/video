"""
Module: web.py

Define flask routes for the web application.
    These are the web pages that users will interact with.
    Does not include API endpoints.
    Does not include dynamic pages (tags, speakers, characters, scriptures).

Functions:
    ensure_profile_selected:
        Ensures that a profile is selected before accessing any web pages.
    inject_admin_status:
        Injects the admin status into the template context (for jinja).
    admin_required:
        Decorator to restrict access to admin-only routes.
    inject_app_version:
        Inject the application version into all templates.

Routes:
    - /admin: Render the admin dashboard.
    - /about: Render the about page.
    - /select_profile: Render the profile selection page.
    - /create_profile: Render the profile creation page.
    - /edit_profile/<profile_id>:
        Render the profile editing page for the specified profile.
    - /character: Render the character details page.
    - /tag: Render the tag details page.
    - /speaker: Render the speaker details page.
    - /scripture: Render the scripture details page.

Flask Dependencies:
    - Blueprint: For organizing routes.
    - Response: For creating HTTP responses.
    - render_template: For rendering HTML templates.
    - make_response: For creating HTTP responses.
    - abort: For aborting requests with an error code.
    - session: For managing user sessions.

Dependencies:
    - random: For selecting similar videos randomly.
    - os: For building file paths.
    - functools: For creating decorators.
    - typing: For type hinting.
    - yaml: For parsing YAML files.
    - requests: For making HTTP requests.

Custom Imports:
    - app_cache: Instance of the AppCache class for caching category IDs.
"""

# Standard library imports
from flask import (
    Blueprint,
    Response,
    render_template,
    make_response,
    abort,
    redirect,
    url_for,
    session,
    request,
)

import random
import os
from typing import Dict, Any
from collections import defaultdict
from functools import wraps
from typing import Callable
import yaml
import requests
import logging
from concurrent.futures import ThreadPoolExecutor


logger = logging.getLogger(__name__)

web_bp = Blueprint(
    'web_pages',
    __name__,
)

# Define the static directory for profile images
profile_dir = os.path.join(
    'static',
    'img',
    'profiles'
)

# Define the static directory for banner images
banner_dir = os.path.join(
    'static',
    'img',
    'banner'
)


@web_bp.before_app_request
def ensure_profile_selected() -> None | Response:
    """
    Ensure that a profile is selected before accessing any web pages.

    This function checks if a profile is selected in the session.
    If no profile is selected, redirects user to the profile selection page.

    Args:
        None

    Returns:
        None | Response: Returns None if the profile is selected,
            otherwise returns a redirect response
            to the profile selection page.
    """

    # Allow static and profile API routes
    if request.endpoint in ('static',):
        return
    if request.blueprint == 'profile_bp':
        return

    # Allow the profile selection/creation pages
    if request.endpoint in (
        'web_pages.select_profile',
        'web_pages.create_profile',
    ):
        return

    # Only redirect on normal page loads that expect HTML
    if (
        request.method in ('GET', 'HEAD') and
        request.accept_mimetypes.accept_html
    ):
        # Get the active profile from the session
        active = session.get('active_profile', None)

        # If no profile yet, send them to selector
        if active is None:
            next_url = request.url or url_for('home.home')
            return make_response(
                redirect(
                    url_for(
                        'web_pages.select_profile',
                        next=next_url
                    )
                )
            )


@web_bp.app_context_processor
def inject_admin_status() -> Dict[str, Any]:
    """
    Injects the admin status into the template context.

    Checks if the selected user is an admin, which is stored in the session.

    Args:
        None

    Returns:
        Dict[str, Any]: A dictionary containing the admin status.
    """

    return {
        'is_admin': session.get('profile_admin', False)
    }


def admin_required(
    f: Callable[..., Response]
) -> Callable[..., Response]:
    """
    Decorator to restrict access to admin-only routes.

    Args:
        f (function): The route function to protect.

    Returns:
        function: The wrapped function.
    """

    @wraps(f)
    def decorated_function(
        *args,
        **kwargs
    ) -> Response:
        """
        Checks if the user has admin privileges.

        Looks for 'profile_admin' in the session to determine if the user
            (current porfile) is an admin.
        'profile_admin' is set to True if the user is an admin,
            otherwise it is False.

        Args:
            *args: Positional arguments for the route function.
            **kwargs: Keyword arguments for the route function.

        Returns:
            Response:
                The response from the route function if the user is an admin,
        """

        if not session.get('profile_admin', False):
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@web_bp.route(
    "/admin",
    methods=["GET"],
)
@admin_required
def admin_dashboard() -> Response:
    """
    Render the admin dashboard.

    Returns:
        Response: A rendered HTML page with the admin dashboard.
    """

    return make_response(
        render_template(
            "admin.html"
        )
    )


@web_bp.route(
    "/about",
    methods=["GET"],
)
def about() -> Response:
    """
    Render the about page.

    Returns:
        Response: A rendered HTML page with information about the application.
    """

    with open('changelog.yaml', 'r', encoding='utf-8') as f:
        try:
            changelog = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error loading changelog.yaml: {e}")
            changelog = []

    return make_response(
        render_template(
            "about.html",
            changes=changelog,
        )
    )


@web_bp.route(
    "/select_profile",
    methods=["GET"]
)
def select_profile() -> Response:
    """
    Render the profile selection page.

    Returns:
        Response: A rendered HTML page for selecting a profile.
    """

    # API: Get all profiles
    response = requests.get(
        url='http://localhost:5010/api/profile',
    )
    profile_list = response.json().get('data', [])

    return make_response(
        render_template(
            'select_profile.html',
            profiles=profile_list,
        )
    )


@web_bp.route(
    "/create_profile",
    methods=["GET"]
)
def create_profile() -> Response:
    """
    Render the profile creation page.

    Returns:
        Response: A rendered HTML page for creating a new profile.
    """

    profile_pics = [
        f for f in os.listdir(profile_dir)
        if (
            f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) and
            f.lower() != 'guest.png'
        )
    ]
    random.shuffle(profile_pics)

    return make_response(
        render_template(
            'create_profile.html',
            profile_pics=profile_pics
        )
    )


@web_bp.route(
    "/edit_profile/<int:profile_id>",
    methods=["GET"]
)
def edit_profile(profile_id: int) -> Response:
    """
    Render the profile editing page.

    Functions:
        get_profile: Get profile details from the API.
        get_watch_history: Get watch history for the profile from the API.

    Args:
        profile_id (int): The ID of the profile to edit.

    Returns:
        Response: A rendered HTML page for editing the specified profile.
    """

    def get_profile() -> Dict[str, Any]:
        """
        Get profile details from the API.

        Returns:
            Dict[str, Any]: A dictionary containing the profile details.
        """

        # API: Get profile details
        response = requests.get(
            url=f'http://localhost:5010/api/profile/{profile_id}',
        )
        profile = response.json().get('data', {})

        return profile

    def get_watch_history() -> list[Dict[str, Any]]:
        """
        Get watch history for the profile from the API.

        Returns:
            list[Dict[str, Any]]:
                A list of dictionaries containing watch history items.
        """

        # API: Get watch history for the profile
        response = requests.get(
            url='http://localhost:5010/api/profile/watch_history',
            params={'profile': profile_id}
        )
        history = response.json().get('data', [])

        return history

    # Run API calls concurrently to speed up page load time
    with ThreadPoolExecutor(max_workers=2) as executor:
        profile_future = executor.submit(get_profile)
        history_future = executor.submit(get_watch_history)

    profile = profile_future.result()
    history = history_future.result()

    logger.info(f"Watch history: {history}")

    # Sort from newest to oldest, stripping fractional seconds
    if history:
        # Strip fractional seconds from all timestamps
        for item in history:
            item['watched_at'] = item['watched_at'].split('.')[0]

        # Sort by cleaned timestamps
        history.sort(key=lambda x: x['watched_at'], reverse=True)

    # Count items in history
    history_count = len(history) if history else 0
    logger.info(f"Watch history count: {history_count}")

    # API: Get the video details for each history item
    if history:
        video_ids = [item['video_id'] for item in history]
        response = requests.post(
            url='http://localhost:5010/api/videos/get_bulk',
            json={'video_ids': video_ids}
        )
        data = response.json().get('data', [])

        # Merge the video details into the history items
        for item in history:
            for video in data:
                if video['id'] == item['video_id']:
                    item['video_name'] = video.get('name')
                    item['video_thumbnail'] = video.get('thumbnail')
                    item['duration'] = video.get('duration')
                    break

    else:
        history = []

    # Get available profile pictures
    profile_pics = []
    profile_pics_path = os.path.join('static', 'img', 'profiles')
    if os.path.exists(profile_pics_path):
        profile_pics = [
            f for f in os.listdir(profile_pics_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]

    return make_response(
        render_template(
            'edit_profile.html',
            profile=profile,
            watch_history=history,
            history_count=history_count,
            profile_pics=profile_pics,
        )
    )


@web_bp.route(
    "/character",
    methods=["GET"]
)
@web_bp.route(
    "/characters",
    methods=["GET"]
)
def characters() -> Response:
    """
    Render the character details page.

    Returns:
        Response: A rendered HTML page with character details.
    """

    # API: Get all characters
    response = requests.get(
        url='http://localhost:5010/api/characters',
    )
    characters = response.json().get('data', {})

    # Set default profile picture if not provided
    for character in characters:
        if not character.get('profile_pic'):
            character['profile_pic'] = 'profile-icon.jpg'

    return make_response(
        render_template(
            'character.html',
            characters=characters,
        )
    )


@web_bp.route(
    "/tag",
    methods=["GET"]
)
@web_bp.route(
    "/tags",
    methods=["GET"]
)
def tags() -> Response:
    """
    Render the tag details page.

    Returns:
        Response: A rendered HTML page with tag details.
    """

    # API: Get all tags
    response = requests.get(
        url='http://localhost:5010/api/tags',
    )
    tags = response.json().get('data', [])

    # Strip 'bcast_' prefix from tag names (special handling)
    tags = [
        tag
        for tag in tags
        if not tag.get('name', '').lower().startswith('bcast_')
    ]

    return make_response(
        render_template(
            'tag.html',
            tags=tags,
        )
    )


@web_bp.route(
    "/location",
    methods=["GET"]
)
@web_bp.route(
    "/location",
    methods=["GET"]
)
def location() -> Response:
    """
    Render the location details page.

    Returns:
        Response: A rendered HTML page with location details.
    """

    # API: Get all locations
    response = requests.get(
        url='http://localhost:5010/api/locations',
    )
    locations = response.json().get('data', [])

    return make_response(
        render_template(
            'location.html',
            locations=locations,
        )
    )


@web_bp.route(
    "/speaker",
    methods=["GET"]
)
@web_bp.route(
    "/speakers",
    methods=["GET"]
)
def speakers() -> Response:
    """
    Render the speaker details page.

    Returns:
        Response: A rendered HTML page with speaker details.
    """

    # API: Get a list of speakers
    response = requests.get(
        url='http://localhost:5010/api/speakers',
    )
    speakers = response.json().get('data', [])

    # Set default profile picture if not provided
    for speaker in speakers:
        if not speaker.get('profile_pic'):
            speaker['profile_pic'] = 'profile-icon.jpg'

    # Categorize speakers by video_count
    speakers_lt3 = [s for s in speakers if s['video_count'] < 3]
    speakers_3_10 = [s for s in speakers if 3 <= s['video_count'] <= 10]
    speakers_gt10 = [s for s in speakers if s['video_count'] > 10]

    return make_response(
        render_template(
            'speaker.html',
            frequent_speakers=speakers_gt10,
            moderate_speakers=speakers_3_10,
            occasional_speakers=speakers_lt3,
        )
    )


@web_bp.route(
    "/scripture",
    methods=["GET"]
)
@web_bp.route(
    "/scriptures",
    methods=["GET"]
)
def scriptures() -> Response:
    """
    Render the scripture details page.

    Returns:
        Response: A rendered HTML page with scripture details.
    """

    # API: Get all scriptures (unsorted)
    response = requests.get(
        url='http://localhost:5010/api/scriptures',
    )
    scriptures = response.json().get('data', [])

    # Group scriptures by book and then by chapter
    scriptures_by_book = defaultdict(lambda: defaultdict(list))
    for scripture in scriptures:
        book = scripture["book"]
        chapter = scripture["chapter"]
        scriptures_by_book[book][chapter].append(scripture)

    # Sort scriptures within each chapter by verse
    for book, chapters in scriptures_by_book.items():
        for chapter in chapters:
            scriptures_by_book[book][chapter] = sorted(
                scriptures_by_book[book][chapter],
                key=lambda s: int(s.get("verse", 0))
            )

    # Define the custom order of books
    custom_book_order = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
        "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
        "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
        "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
        "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
        "Zephaniah", "Haggai", "Zechariah", "Malachi",
        "Matthew", "Mark", "Luke", "John", "Acts",
        "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
        "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
        "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
        "James", "1 Peter", "2 Peter", "1 John", "2 John",
        "3 John", "Jude", "Revelation"
    ]

    # Sort the books in the custom order
    sorted_scriptures_by_book = {
        book: scriptures_by_book[book]
        for book in custom_book_order
        if book in scriptures_by_book
    }

    return make_response(
        render_template(
            'scripture.html',
            scriptures_by_book=sorted_scriptures_by_book,
        )
    )


@web_bp.route(
    '/.well-known/appspecific/com.chrome.devtools.json'
)
def devtools_discovery():
    """
    Suppress 404 errors for Chrome DevTools discovery requests.
    """
    return []
