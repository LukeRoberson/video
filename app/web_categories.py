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

import requests


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

    logging.info(
        f"Category: {category_name}. Subcategories: {sub_category_list}"
    )

    # Resolve main category name to ID
    response = requests.get(
        f'http://localhost:5010/api/categories/{category_name}'
    )
    data = response.json().get('data', {})
    main_id = data.get('category_id', None)

    if not main_id:
        logging.error(f"Category '{category_name}' not found.")
        return make_response(
            render_template("404.html", message="Category not found"), 404
        )

    main_cat = {"id": main_id, "name": category_name}

    # Get the active profile from the session
    active_profile = session.get("active_profile", None)

    # Get a list of subcategory IDs
    watch_status = []

    # Loop through each subcategory name
    for sub_cat in sub_category_list:
        entry = {}

        # Resolve the subcategory name to ID
        response = requests.get(
            f'http://localhost:5010/api/categories/{sub_cat}'
        )
        data = response.json().get('data', {})
        sub_cat_id = data.get('category_id', None)

        # Get the list of videos for the subcategory and count them
        entry['name'] = sub_cat
        if sub_cat_id is not None:
            # Get the list of videos for the subcategory
            response = requests.get(
                f'http://localhost:5010/api/categories/{main_id}/{sub_cat_id}'
            )
            data = response.json().get('data', {})
            video_list = data.get('videos', [])

            entry['id'] = sub_cat_id
            entry['count'] = (
                len(video_list) if video_list else 0
            )
            logging.debug(
                f"Subcategory '{sub_cat}' (Videos: {video_list}) "
            )

            # Get the watch status for the active profile
            if (
                active_profile is not None and
                active_profile != "guest" and
                video_list is not None
            ):
                watch_count = 0

                # Bulk API call
                response = requests.post(
                    'http://localhost:5010/api/profile/mark_watched_bulk',
                    params={'profile': active_profile},
                    json={
                        'video_ids': [video['id'] for video in video_list]
                    }
                )

                # Collect the watch status from the API response
                if response.status_code == 200:
                    data = response.json().get('data', {})
                    watch_count = sum(
                        1 for video_id in data if data[video_id]
                    )
                    entry['watched'] = watch_count

            else:
                entry['watched'] = 0

            watch_status.append(entry)

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
        category_name="JW Broadcasting",
        sub_category_list=[
            "Monthly Programs",
            "Talks",
            "News and Announcements"
        ]
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
        category_name="Children",
        sub_category_list=[
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
        category_name="Teenagers",
        sub_category_list=[
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
        category_name="Family",
        sub_category_list=[
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
        category_name="Programs and Events",
        sub_category_list=[
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
        category_name="Our Activities",
        sub_category_list=[
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
        category_name="Our Meetings and Ministry",
        sub_category_list=[
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
        category_name="Our Organization",
        sub_category_list=[
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
        category_name="The Bible",
        sub_category_list=[
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
        category_name="Dramas",
        sub_category_list=[
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
        category_name="Series",
        sub_category_list=[
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
        category_name="Music",
        sub_category_list=[
            "Original Songs",
            "Children’s Songs",
            "Convention Music Presentations",
            "Making Music",
            "Sing to Jehovah",
            "“Sing Out Joyfully”—Meetings",
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
        category_name="Interviews and Experiences",
        sub_category_list=[
            "Truth Transforms Lives",
            "Blessings of Sacred Service",
            "Enduring Trials",
            "Young People",
            "Science",
            "From Our Archives",
        ]
    )
