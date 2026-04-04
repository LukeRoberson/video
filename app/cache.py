"""
Module: cache.py

Define caching mechanisms for the web application.
    These are used to store and retrieve frequently accessed data
    to improve performance and reduce load on the server.

Classes:
    - AppCache:
        A simple in-memory cache for storing frequently accessed data,
        such as category IDs.

Dependencies:
    - requests: For making HTTP requests to the API endpoints.
    - logging: For logging errors and debug information.
"""

import requests
import logging
from flask import current_app


logger = logging.getLogger(__name__)


class AppCache:
    """
    A simple in-memory cache for storing frequently accessed data.

    Attributes:
        category_ids (list[dict[int, str]]):
            Cached list of category IDs and names.

    Methods:
        get_category_ids:
            Retrieve cached category IDs or fetch from API if not cached.
        cache_category_id:
            Fetch category IDs from the API and cache them.
    """

    def __init__(self):
        """
        Initialize the cache with empty data.
        """

        self.category_ids = {}

    def cache_category_id(
        self
    ) -> None:
        """
        Get all category IDs from the database.
        These rarely change (if ever), so we can cache them for performance.

        Args:
            None

        Returns:
            None
        """

        base_url = current_app.config['API_BASE_URL']

        # Get all categories from the API
        response = requests.get(f'{base_url}/api/categories')

        # Cache the category IDs if the request was successful
        if response.status_code == 200:
            self.category_ids = response.json().get('data', {})

        # Log an error if the request failed
        else:
            logger.debug("Module: cache.py, Function: get_category_id")
            logger.error(
                f"Failed to fetch category IDs. Status code: "
                f"{response.status_code}"
            )
            self.category_ids = {}

    def get_category_ids(
        self
    ) -> dict:
        """
        Return cached category IDs.
            Checks if the cache is empty and fetches from API if necessary.

        Args:
            None

        Returns:
            dict: Cached category IDs and names
        """

        # Check if the cache is empty and fetch from API if necessary
        if not self.category_ids or len(self.category_ids) == 0:
            logger.warning("Category ID cache is empty. Fetching from API...")
            self.cache_category_id()

        # Log an error if the cache is still empty after attempting to fetch
        if len(self.category_ids) == 0:
            logger.debug("Module: cache.py, Function: get_category_ids")
            logger.error(
                "Failed to fetch category IDs from API. Cache is empty."
            )

        return self.category_ids


# Cache category IDs at startup
app_cache = AppCache()
