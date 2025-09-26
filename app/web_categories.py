"""
Module: web_categories.py

Defines a Flask blueprint for category-related web routes.
    These are web pages that are based on a major category
    Each page contains carousels for subcategories

Functions:
    render_category_page(category_name, sub_category_list) -> Response:
        Dynamically renders a category page with subcategories.
        If the main category or any subcategory is not found,
        a 404 error page is returned.

Routes:
    /broadcasting
        Displays the JW Broadcasting category and its subcategories.
    /children
        Displays the Children category and its subcategories.
    /teens
        Displays the Teenagers category and its subcategories.
    /family
        Displays the Family category and its subcategories.
    /programs_events
        Displays the Programs and Events category and its subcategories.
    /our_activities
        Displays the Our Activities category and its subcategories.
    /meetings_ministry
        Displays the Our Meetings and Ministry category and its subcategories.
    /organization
        Displays the Our Organization category and its subcategories.
    /bible
        Displays the Bible category and its subcategories.
    /dramas
        Displays the Dramas category and its subcategories.
    /series
        Displays the Series category and its subcategories.
    /music
        Displays the Music category and its subcategories.
    /interviews
        Displays the Interviews and Experiences category and its subcategories.

Dependancies:
    Flask: To define the blueprint for web pages.
    logging: For logging debug information.

Custom Dependencies:
    DatabaseContext: Context manager for database operations.
    CategoryManager: Manages category-related database operations.
"""

# Standard library imports
from flask import (
    Blueprint,
    Response,
    render_template,
    make_response,
    session,
)
import logging

# Custom imports
from app.sql_db import (
    DatabaseContext,
    VideoManager,
    CategoryManager,
)
from app.local_db import (
    LocalDbContext,
    ProfileManager,
)


category_bp = Blueprint(
    'category_pages',
    __name__,
)


def render_category_page(
    category_name,
    sub_category_list
) -> Response:
    """
    Dynamically render a category page with subcategories.

    Args:
        category_name (str): The name of the main category.
        sub_category_list (list): A list of subcategory names.

    Returns:
        Response:
            A rendered HTML page with the main category and its subcategories.
        If the main category or any subcategory is not found,
            a 404 error page is returned.
    """

    logging.debug(
        f"Category: {category_name}. Subcategories: {sub_category_list}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(name=category_name)

        if not main_cat_id:
            logging.error(f"Category '{category_name}' not found.")
            return make_response(
                render_template("404.html", message="Category not found"), 404
            )

        main_cat = {"id": main_cat_id, "name": category_name}

    # Get the active profile from the session
    active_profile = session.get("active_profile", None)
    print(f"Active profile: {active_profile}")

    # Get a list of subcategory IDs
    watch_status = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        video_mgr = VideoManager(db)

        # Loop through each subcategory name
        for sub_cat in sub_category_list:
            entry = {}

            # Get the subcategory ID from the database
            entry['name'] = sub_cat
            sub_cat_id = cat_mgr.name_to_id(name=sub_cat)

            # Add it to the list if found
            if sub_cat_id is not None:
                video_list = video_mgr.get_filter(
                    category_id=[sub_cat_id],
                )

                entry['id'] = sub_cat_id
                entry['count'] = (
                    len(video_list) if video_list else 0
                )
                logging.debug(
                    f"Subcategory '{sub_cat}' (Videos: {video_list}) "
                )

                with LocalDbContext() as local_db:
                    profile_mgr = ProfileManager(local_db)

                    # Get the watch status for the active profile
                    if (
                        active_profile is not None and
                        active_profile != "guest" and
                        video_list is not None
                    ):
                        watch_count = 0
                        for video in video_list:
                            watched = profile_mgr.check_watched(
                                video_id=video['id'],
                                profile_id=active_profile,
                            )
                            if watched:
                                watch_count += 1

                        entry['watched'] = watch_count

                    else:
                        entry['watched'] = 0

                watch_status.append(entry)

    logging.debug(f"Main category ID: {main_cat_id}")
    logging.debug(f"Watch status: {watch_status}")

    return make_response(
        render_template(
            "category.html",
            category=main_cat,
            watch_status=watch_status,
            active_profile=active_profile,
        )
    )


@category_bp.route(
    "/broadcasting",
    methods=["GET"],
)
def broadcasting():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "JW Broadcasting",
        ["Monthly Programs", "Talks", "News and Announcements"]
    )


@category_bp.route(
    "/children",
    methods=["GET"],
)
def children():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Children",
        [
            "Video Lessons",
            "Songs",
            "Animated"
        ]
    )


@category_bp.route(
    "/teens",
    methods=["GET"],
)
def teens():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Teenagers",
        [
            "Spiritual Growth",
            "Social Life",
            "Goals",
            "Interviews and Experiences",
            "Dramas",
        ]
    )


@category_bp.route(
    "/family",
    methods=["GET"],
)
def family():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Family",
        [
            "Family Challenges",
            "Dating and Marriage",
            "Family Worship",
            "Dramas",
        ]
    )


@category_bp.route(
    "/programs_events",
    methods=["GET"],
)
def programs_events():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Programs and Events",
        [
            "Morning Worship",
            "Special Programs",
            "Gilead Graduations",
            "Annual Meetings",
            "2025 Pure Worship Convention",
            "2024 “Declare the Good News!” Convention",
            "2023 “Exercise Patience”! Convention",
            "2022 “Pursue Peace”! Convention",
            "2021 Powerful by Faith! Convention",
            "2020 “Always Rejoice”! Convention",
            "2019 “Love Never Fails”! Convention",
            "2018 “Be Courageous”! Convention",
            "2017 Don’t Give Up! Convention",
            "2016 Remain Loyal to Jehovah! Convention",
            "2015 Imitate Jesus! Convention",
            "2014 Keep Seeking First God’s Kingdom! Convention",
        ]
    )


@category_bp.route(
    "/our_activities",
    methods=["GET"],
)
def our_activities():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Our Activities",
        [
            "Translation",
            "Audio and Video Production",
            "Publishing and Distribution",
            "Construction",
            "Relief Work",
            "Theocratic Schools and Training",
            "Special Events",
        ]
    )


@category_bp.route(
    "/meetings_ministry",
    methods=["GET"],
)
def meetings_ministry():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Our Meetings and Ministry",
        [
            "Tools for the Ministry",
            "Essential Bible Teachings",
            "Improving Our Skills",
            "Preaching Methods",
            "Expanding Our Ministry",
            "Meetings, Assemblies, and Conventions",
        ]
    )


@category_bp.route(
    "/organization",
    methods=["GET"],
)
def organization():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Our Organization",
        [
            "Reports From Around the World",
            "Bethel",
            "Organized to Accomplish Our Ministry",
            "History",
            "Legal Developments",
            "Bloodless Medicine",
        ]
    )


@category_bp.route(
    "/bible",
    methods=["GET"],
)
def bible():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "The Bible",
        [
            "Books of the Bible",
            "Bible Teachings",
            "Bible Accounts",
            "People, Places, and Things",
            "Bible Translations",
            "Apply Bible Principles",
            "Creation",
        ]
    )


@category_bp.route(
    "/dramas",
    methods=["GET"],
)
def dramas():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Dramas",
        [
            "The Good News According to Jesus",
            "Bible Times",
            "Modern Day",
            "Extra Features",
            "Animated",
        ]
    )


@category_bp.route(
    "/series",
    methods=["GET"],
)
def series():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Series",
        [
            "Apply Yourself to Reading and Teaching",
            "Become Jehovah's Friend—Songs",
            "Become Jehovah's Friend—Video Lessons",
            "Essential Bible Teachings",
            "For a Happy Marriage",
            "Imitate Their Faith",
            "Introduction to Bible Books",
            "Iron Sharpens Iron",
            "Learn From Jehovah's Friends",
            "Learn From Them",
            "Lessons From The Watchtower",
            "Love People—Make Disciples",
            "My Teen Life",
            "Neeta and Jade",
            "Organizational Accomplishments",
            "Our History in Motion",
            "Reasons for Faith",
            "The Bible Changes Lives",
            "The Good News According to Jesus",
            "Truth Transforms Lives",
            "Viewpoints on the Origin of Life",
            "Was It Designed?",
            "What Your Peers Say",
            "Where Are They Now?",
            "Whiteboard Animations",
        ]
    )


@category_bp.route(
    "/music",
    methods=["GET"],
)
def music():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Music",
        [
            "Original Songs",
            "Children’s Songs",
            "Convention Music Presentations",
            "Making Music",
            "Sing to Jehovah",
        ]
    )


@category_bp.route(
    "/interviews",
    methods=["GET"],
)
def interviews():
    """
    Render the home page with categories and their items.

    Returns:
        Response: A rendered HTML page with categories and their items.
        This page is dynamic and fetches data from the database.
    """

    return render_category_page(
        "Interviews and Experiences",
        [
            "Truth Transforms Lives",
            "Blessings of Sacred Service",
            "Enduring Trials",
            "Young People",
            "Science",
            "From Our Archives",
        ]
    )
