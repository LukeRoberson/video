"""
Module: main.py

This module initializes the Flask application and sets up the main routes.
It includes the home page and video details page, along with necessary imports

Blueprints:
    - category_bp:
        Web routes for category-related pages.
    - api_bp:
        API endpoints for fetching video data from the browser.

Dependencies:
    - Flask: For creating the web application.
    - logging: For logging application events.

Custom Dependencies:
    - DatabaseContext: Context manager for database connections.
    - VideoManager: Manages video-related database operations.
    - CategoryManager: Manages category-related database operations
    - TagManager: Manages tag-related database operations.
    - SpeakerManager: Manages speaker-related database operations.
    - CharacterManager: Manages character-related database operations.
    - ScriptureManager: Manages scripture-related database operations.
"""

# Standard library imports
import logging
import os
import random
from flask import (
    Flask,
    Response,
    session,
    request,
    jsonify,
    render_template,
    make_response
)

# Custom imports
from web_categories import category_bp
from api import (
    api_bp,
    seconds_to_hhmmss
)
from sql_db import (
    DatabaseContext,
    VideoManager,
    CategoryManager,
    TagManager,
    SpeakerManager,
    CharacterManager,
    ScriptureManager,
)
from local_db import (
    LocalDbContext,
    ProfileManager,
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


# Create a secret key for the Flask application
SECRET_KEY = "gU0BTfsKgCJNpNipm5PeyhapfYCGCVB2"


# Register the filter with Flask
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
app.secret_key = SECRET_KEY
app.register_blueprint(category_bp)
app.register_blueprint(api_bp)
app.jinja_env.filters['seconds_to_hhmmss'] = seconds_to_hhmmss


# Define the static directory for profile images
profile_dir = os.path.join(
    app.static_folder,
    'img',
    'profiles'
)


@app.route(
    "/",
    methods=["GET"],
)
def home():
    """
    A very simple home page that renders the main HTML template.

    Returns:
        Response: A rendered HTML 'welcome' page
    """

    return render_template(
        "home.html",
    )


@app.route(
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

    return make_response(
        render_template(
            'select_profile.html',
            profiles=profile_list,
        )
    )


@app.route(
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


@app.route(
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
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
