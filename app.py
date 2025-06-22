from flask import (
    Flask,
    Response,
    render_template,
    jsonify,
    make_response
)

import logging

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


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
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


@app.route(
    "/api/categories/<int:category_id>/<int:subcategory_id>",
    methods=["GET"],
)
def category_filter(
    category_id: int,
    subcategory_id: int,
) -> Response:
    """
    Fetch videos with the given major category ID and subcategory ID.
    This is used to populate carousels with videos.

    Process:
        1. Select all videos with the given category ID and subcategory ID.
        2. If no videos are found, return a 404 error.
        3. Convert the duration from seconds to HH:MM:SS format.
        4. Return a JSON response with the list of videos.

    Args:
        category_id (int): The ID of the major category to filter videos by.
        subcategory_id (int): The ID of the subcategory to filter videos by.

    Returns:
        Response: A JSON response containing the list of videos
            in the specified category and subcategory.
        If no videos are found, an empty list is returned.
    """

    logging.info(
        f"Fetching videos for Category ID: {category_id}, "
        f"Subcategory ID: {subcategory_id}"
    )

    # Select all videos with the given category ID and subcategory ID
    cat_list = [category_id, subcategory_id]
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        videos = video_mgr.get_filter(
            category_id=cat_list,
        )

    if videos:
        logging.info(
            f"Found {len(videos)} videos for Category ID: {category_id}, "
            f"Subcategory ID: {subcategory_id}"
        )

    # If no videos are found, return a 404 error
    if not videos:
        videos = []

    # Convert duration from seconds to HH:MM:SS format
    for video in videos:
        video['duration'] = seconds_to_hhmmss(video['duration'])

    return jsonify(videos)


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
    cat_list = [category_id]
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        videos = video_mgr.get_filter(
            category_id=cat_list,
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
