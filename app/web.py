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
    inject_site_flags:
        Injects site flags based on the hostname into the template context.
    admin_required:
        Decorator to restrict access to admin-only routes.

Routes:
    - /admin: Render the admin dashboard.
    - /about: Render the about page.
    - /select_profile: Render the profile selection page.
    - /create_profile: Render the profile creation page.
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

Custom Dependencies:
    - DatabaseContext: For managing database connections.
    - VideoManager: For managing video data.
    - CharacterManager: For managing character data.
    - TagManager: For managing tag data.
    - SpeakerManager: For managing speaker data.
    - ScriptureManager: For managing scripture data.
    - LocalDbContext: For managing local database connections.
    - ProfileManager: For managing user profiles.
    - ProgressManager: For managing user progress in videos.
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
from typing import List, Dict, Any
from collections import defaultdict
from functools import wraps
from typing import Callable

# Custom imports
from app.sql_db import (
    DatabaseContext,
    VideoManager,
    CategoryManager,
    CharacterManager,
    TagManager,
    LocationManager,
    SpeakerManager,
    ScriptureManager,
)
from app.local_db import (
    LocalDbContext,
    ProfileManager,
    ProgressManager,
)


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
    if request.blueprint == 'profile_api':
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
            next_url = request.url or url_for('web_pages.home')
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


@web_bp.app_context_processor
def inject_site_flags() -> Dict[str, Any]:
    """
    Inject site flags based on the hostname.

    If the hostname is 'devel.networkdirection.net',
        it sets 'is_devel' to True and 'host_name' to the hostname.
        Otherwise, it sets 'is_devel' to False and 'host_name' to the hostname.

    Args:
        None

    Returns:
        Dict[str, Any]: A dictionary containing the site flags.
    """

    # Prefer X-Forwarded-Host when behind a proxy, fallback to Host
    raw_host = request.headers.get('X-Forwarded-Host') or request.host or ''
    host = raw_host.split(':')[0].lower()

    return {
        'is_devel': host == 'devel.networkdirection.net',
        'host_name': host,
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
    "/",
    methods=["GET"],
)
def home() -> Response:
    """
    A very simple home page that renders the main HTML template.

    Returns:
        Response: A rendered HTML 'welcome' page
    """

    banner_pics = [
        {
            "filename": "banner_1.jpg",
            "description": "Sermon on the Mount",
        },
        {
            "filename": "banner_2.jpg",
            "description": "Prayer",
        },
        {
            "filename": "banner_3.jpg",
            "description": "People of all Nations",
        },
        {
            "filename": "banner_4.jpg",
            "description": "Guidance",
        },
        {
            "filename": "banner_5.jpg",
            "description": "Prophets of Old",
        },
    ]

    # Get the session profile ID from the request context
    in_progress_videos = []
    profile_id = session.get('active_profile')

    # Get in progress videos
    if profile_id != 0 and profile_id is not None and profile_id != 'guest':
        profile_id = (
            int(profile_id) if isinstance(profile_id, str) else profile_id
        )
        with LocalDbContext() as db:
            progress_mgr = ProgressManager(db)

            in_progress_videos = progress_mgr.read(
                profile_id=profile_id,
            )

            # Make sure it's a list
            in_progress_videos = (
                [] if not in_progress_videos else in_progress_videos
            )

    # Get details for each in-progress video
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)

        for video in in_progress_videos:
            video_details = video_mgr.get(
                id=video['video_id']
            )
            if video_details:
                video['id'] = video_details[0].get('id')
                video['name'] = video_details[0].get('name')
                video['thumbnail'] = video_details[0].get('thumbnail')
                video['duration'] = video_details[0].get('duration')

        # Sort, so the most recently updated videos are first
        in_progress_videos.sort(
            key=lambda v: v.get('updated_at', ''),
            reverse=True
        )

    # Get latest Monthly Programs video
    monthly = None
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        cat_mgr = CategoryManager(db)

        # Get the category ID for 'Monthly Programs'
        monthly_cat = cat_mgr.name_to_id(name='Monthly Programs')

        if monthly_cat is not None:
            monthly = video_mgr.get_filter(
                category_id=[monthly_cat],
                latest=1,
            )

    # Get the latest News video
    news = None
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        cat_mgr = CategoryManager(db)

        # Get the category ID for 'News and Announcements'
        news_cat = cat_mgr.name_to_id(name='News and Announcements')

        if news_cat is not None:
            news = video_mgr.get_filter(
                category_id=[news_cat],
                latest=1,
            )

    latest_monthly = monthly[0] if monthly else None
    latest_news = news[0] if news else None

    # Get the latest videos in general
    latest = None
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)

        # Get the latest 9 videos
        latest = video_mgr.get_filter(
            latest=9,
        )

    return make_response(
        render_template(
            "home.html",
            banner_pics=banner_pics,
            in_progress_videos=in_progress_videos,
            latest_monthly=latest_monthly,
            latest_news=latest_news,
            latest_videos=latest,
        )
    )


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

    return make_response(
        render_template(
            "about.html"
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

    # Get all profiles from the local database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)
        profile_list = profile_mgr.read()
        print(f"{profile_list=}")

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

    Args:
        profile_id (int): The ID of the profile to edit.

    Returns:
        Response: A rendered HTML page for editing the specified profile.
    """

    # Get the profile details from the local database
    with LocalDbContext() as db:
        profile_mgr = ProfileManager(db)

        # Get the user's profile
        profile = profile_mgr.read(profile_id=profile_id)

        if not profile:
            return make_response(
                render_template(
                    "404.html",
                    message="Profile not found"
                ),
                404
            )

        profile = profile[0]

        # Get watch history
        history = profile_mgr.read_watch_history(profile_id=profile_id)

        # Sort from newest to oldest, stripping fractional seconds
        if history:
            # Strip fractional seconds from all timestamps
            for item in history:
                item['watched_at'] = item['watched_at'].split('.')[0]

            # Sort by cleaned timestamps
            history.sort(key=lambda x: x['watched_at'], reverse=True)

        # Count items in history
        history_count = len(history) if history else 0

    # Get video name and thumbnail for each history item
    if history:
        with DatabaseContext() as db:
            video_mgr = VideoManager(db)

            for item in history:
                video_details = video_mgr.get(id=item['video_id'])
                if video_details:
                    item['video_name'] = video_details[0].get('name')
                    item['video_thumbnail'] = video_details[0].get('thumbnail')
                    item['duration'] = video_details[0].get('duration')

                else:
                    item['video_name'] = 'Unknown Video'
                    item['video_thumbnail'] = 'default-thumbnail.jpg'
                    item['duration'] = 0

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

    with DatabaseContext() as db:
        character_mgr = CharacterManager(db)
        characters: List[Dict[str, Any]] = character_mgr.get() or []

    # Sort characters by name in a case-insensitive manner
    characters = sorted(
        characters, key=lambda character: character.get('name', '').lower()
    )

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

    with DatabaseContext() as db:
        tag_mgr = TagManager(db)
        tags: List[Dict[str, Any]] = tag_mgr.get() or []

    # Sort tags by name in a case-insensitive manner
    tags = sorted(tags, key=lambda tag: tag.get('name', '').lower())

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

    with DatabaseContext() as db:
        loc_mgr = LocationManager(db)
        locations: List[Dict[str, Any]] = loc_mgr.get() or []

    # Sort locations by name in a case-insensitive manner
    locations = sorted(
        locations,
        key=lambda location: location.get('name', '').lower()
    )

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

    with DatabaseContext() as db:
        speaker_mgr = SpeakerManager(db)
        video_mgr = VideoManager(db)
        speakers = speaker_mgr.get()

        if not speakers:
            speakers = []

        # Get the video count for each speaker
        for speaker in speakers:
            videos = video_mgr.get_filter(
                speaker_id=speaker['id']
            )
            if not videos:
                return make_response(
                    render_template(
                        "404.html",
                        message="No videos found for this speaker"
                    ),
                    404
                )
            speaker['video_count'] = len(videos)

    # Sort speakers by name in a case-insensitive manner
    speakers = sorted(speakers, key=lambda s: s.get('name', '').lower())

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

    with DatabaseContext() as db:
        scripture_mgr = ScriptureManager(db)
        scriptures: List[Dict[str, Any]] = scripture_mgr.get() or []

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
