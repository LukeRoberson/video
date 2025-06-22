"""
Module: web_categories.py

Defines a Flask blueprint for category-related web routes.
    These are web pages that are based on a major category
    Each page contains carousels for subcategories

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
    render_template,
    make_response
)
import logging

# Custom imports
from sql_db import (
    DatabaseContext,
    CategoryManager,
)


category_bp = Blueprint(
    'category_pages',
    __name__,
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

    # Fetch categories from the database
    CATEGORY = "JW Broadcasting"
    SUB_CATEGORY_LIST = [
        "Monthly Programs",
        "Talks",
        "News and Announcements",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Children"
    SUB_CATEGORY_LIST = [
        "Video Lessons",
        "Songs",
        "Dramas",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Teenagers"
    SUB_CATEGORY_LIST = [
        "Spiritual Growth",
        "Social Life",
        "Goals",
        "Interviews and Experiences",
        "Dramas",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Family"
    SUB_CATEGORY_LIST = [
        "Family Challenges",
        "Dating and Marriage",
        "Family Worship",
        "Dramas",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Programs and Events"
    SUB_CATEGORY_LIST = [
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
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Our Activities"
    SUB_CATEGORY_LIST = [
        "Translation",
        "Audio and Video Production",
        "Publishing and Distribution",
        "Construction",
        "Relief Work",
        "Theocratic Schools and Training",
        "Special Events",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Our Meetings and Ministry"
    SUB_CATEGORY_LIST = [
        "Tools for the Ministry",
        "Essential Bible Teachings",
        "Improving Our Skills",
        "Preaching Methods",
        "Expanding Our Ministry",
        "Meetings, Assemblies, and Conventions",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Our Organization"
    SUB_CATEGORY_LIST = [
        "Reports From Around the World",
        "Bethel",
        "Organized to Accomplish Our Ministry",
        "History",
        "Legal Developments",
        "Bloodless Medicine",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "The Bible"
    SUB_CATEGORY_LIST = [
        "Books of the Bible",
        "Bible Teachings",
        "Bible Accounts",
        "People, Places, and Things",
        "Bible Translations",
        "Apply Bible Principles",
        "Creation",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Dramas"
    SUB_CATEGORY_LIST = [
        "The Good News According to Jesus",
        "Bible Times",
        "Modern Day",
        "Extra Features",
        "Animated",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Series"
    SUB_CATEGORY_LIST = [
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
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Music"
    SUB_CATEGORY_LIST = [
        "Original Songs",
        "Children’s Songs",
        "Convention Music Presentations",
        "Making Music",
        "Sing to Jehovah",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
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

    # Fetch categories from the database
    CATEGORY = "Interviews and Experiences"
    SUB_CATEGORY_LIST = [
        "Truth Transforms Lives",
        "Blessings of Sacred Service",
        "Enduring Trials",
        "Young People",
        "Science",
        "From Our Archives",
    ]
    logging.debug(
        f"Category: {CATEGORY}. Subcategories: {SUB_CATEGORY_LIST}"
    )

    # Get an ID for the main category
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)
        main_cat_id = cat_mgr.name_to_id(
            name=CATEGORY
        )

        if not main_cat_id:
            logging.error(f"Category '{CATEGORY}' not found.")
            return make_response(
                render_template(
                    "404.html",
                    message="Category not found"
                ),
                404
            )

    main_cat = {
        "id": main_cat_id,
        "name": CATEGORY,
    }
    logging.debug(f"Main Category ID: {main_cat}")

    # Convert subcategories to IDs
    sub_cat_ids = []
    with DatabaseContext() as db:
        cat_mgr = CategoryManager(db)

        # Loop through each subcategory and get its ID
        for sub_cat in SUB_CATEGORY_LIST:
            sub_cat_id = cat_mgr.name_to_id(
                name=sub_cat,
            )
            if sub_cat_id:
                entry = {
                    "id": sub_cat_id,
                    "name": sub_cat,
                }
                sub_cat_ids.append(entry)
            else:
                logging.error(f"Subcategory '{sub_cat}' not found.")

    # Render the template with the main category and subcategories
    logging.debug(f"Main Category: {main_cat}")
    logging.debug(f"Subcategories: {sub_cat_ids}")
    return render_template(
        "category.html",
        category=main_cat,
        sub_categories=sub_cat_ids,
    )
