from flask import (
    Flask,
    Response,
    render_template,
    jsonify,
    make_response
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


def seconds_to_hhmmss(seconds):
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


# Register the filter with Flask
app = Flask(__name__)
app.jinja_env.filters['seconds_to_hhmmss'] = seconds_to_hhmmss


@app.route(
    "/",
    methods=["GET"],
)
def home():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    # Fetch categories from the database
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        categories = cat_mgr.get()

    return render_template(
        "home.html",
        categories=categories
    )


@app.route(
    "/about",
    methods=["GET"],
)
def about():
    """
    A simple about page.

    Returns:
        Response: A rendered HTML page with information about the application.
        This page is static and does not require any database interaction.
    """

    return render_template("about.html")


@app.route(
    "/videos/<int:category_id>",
    methods=["GET"],
)
def get_videos_by_category(
    category_id: int,
) -> Response:
    """
    Fetch videos by category ID and return them as JSON.
    This is used by the JavaScript on the home page to load videos dynamically.

    Args:
        category_id (int): The ID of the category to filter videos by.

    Returns:
        Response: A JSON response containing the list of videos
            in the specified category.
        If no videos are found, a 404 error is returned.
    """

    # Select all videos with the given category ID
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        videos = video_mgr.get_filter(
            category_id=category_id,
        )

    # If no videos are found, return a 404 error
    if not videos:
        return make_response(
            jsonify(
                {
                    "error": "No videos found for this category"
                }
            ),
            404
        )

    # Convert duration from seconds to HH:MM:SS format
    for video in videos:
        video['duration'] = seconds_to_hhmmss(video['duration'])

    return jsonify(videos)


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
