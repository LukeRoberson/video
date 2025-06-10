from flask import Flask, render_template, jsonify

from sql_db import DatabaseManager


with DatabaseManager() as db:
    result = db.create_category_table()
    print(f"Category table created: {result}")
    result = db.create_video_table()
    print(f"Video table created: {result}")


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


@app.route("/")
def home():
    """
    Render the home page with categories and their items.
    """

    # Fetch categories from the database
    with DatabaseManager() as db:
        # 'id' - the category ID
        # 'name' - the category name
        categories = db.get_categories()

    return render_template(
        "home.html",
        categories=categories
    )


@app.route("/about")
def about():
    """
    A simple about page.
    """

    return render_template("about.html")


@app.route("/videos/<int:category_id>")
def get_videos_by_category(category_id):
    """
    Fetch videos by category ID and return them as JSON.
    This is used by the JavaScript on the home page to load videos dynamically.
    """

    with DatabaseManager() as db:
        videos = db.get_videos(
            category_id=category_id
        )

    for video in videos:
        # Convert duration from seconds to HH:MM:SS format
        video['duration'] = seconds_to_hhmmss(video['duration'])

    return jsonify(videos)


@app.route("/video/<int:video_id>")
def video_details(video_id):
    """
    Render the details of a specific video along with similar videos.
    This is seen when a user clicks on a video from the home page.
    """

    with DatabaseManager() as db:
        # Fetch video details from the database
        video = db.get_video_by_id(video_id)
        tags = db.get_tags_by_video_id(video_id)
        speakers = db.get_speakers_by_video_id(video_id)
        characters = db.get_characters_by_video_id(video_id)
        scriptures = db.get_scriptures_by_video_id(video_id)

        print(f"Tags for video {video_id}: {tags}")
        print(f"Speakers for video {video_id}: {speakers}")
        print(f"Characters for video {video_id}: {characters}")
        print(f"Scriptures for video {video_id}: {scriptures}")

        if not video:
            return render_template("404.html", message="Video not found"), 404

        # Get the category name for the video
        with DatabaseManager() as db:
            cat_name = db.get_category_name_by_id(video['category_id'])
            video['category_name'] = cat_name

        # Dummy data for similar videos
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

    return render_template(
        "video_details.html",
        video=video,
        tags=tags,
        speakers=speakers,
        characters=characters,
        scriptures=scriptures,
        similar_videos=similar_videos
    )


if __name__ == "__main__":
    app.run(debug=True)
