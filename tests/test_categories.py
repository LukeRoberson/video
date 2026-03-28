"""
Module: test_categories.py

Unit tests for category-related API endpoints.

Endpoints Tested:
    - GET /api/categories/{{category_name}}
    - GET /api/categories/{{category_id}}/{{subcategory_id}}
    - GET /api/categories/video/{{video_id}}

Classes:
    TestCategoryNameResolution
        Tests for resolving category names to IDs.
    TestCategoryVideoRetrieval
        Tests for retrieving videos based on category and subcategory IDs.
    TestVideoCategories
        Tests for retrieving categories associated with a video.
"""

import pytest
import requests
from typing import Dict


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestCategoryNameResolution:
    """
    Tests for /api/categories/{{category_name}} endpoint.

    Methods:
        test_resolve_valid_category_name
            Test resolving a valid category name, returns 200,
              and correct structure.
        test_resolve_invalid_category_name
            Test resolving an invalid category name returns 404.
        test_resolve_multiple_categories
            Test resolving multiple known categories.
        test_category_name_with_spaces
            Test category names with spaces are handled correctly.
    """

    def test_get_all_categories(
        self
    ) -> None:
        """
        Test retrieving all categories returns 200 and correct structure.

        Tests:
            - GET /api/categories returns 200
            - Response contains a list of categories
            - Each category has 'id' (int) and 'name' (str)
        """

        url = f"{BASE_URL}{API_PREFIX}/categories"
        response = requests.get(url)

        # Check response
        assert response.status_code == 200
        data = response.json().get("data", [])
        assert len(data) > 0, "Expected at least one category in response"

        # Validate response structure
        for index, category in enumerate(data):
            assert "id" in category, (
                f"Missing 'id' in category at index {index}"
            )
            assert isinstance(category["id"], int), (
                f"'id' is not an integer in category at index {index}"
            )

            assert "name" in category, (
                f"Missing 'name' in category at index {index}"
            )
            assert isinstance(category["name"], str), (
                f"'name' is not a string in category at index {index}"
            )

    def test_resolve_category_list(
        self
    ) -> None:
        """
        Test POST request to resolve a list of category names.

        Tests:
            - POST /api/categories with a list of category names returns 200
        """

        url = f"{BASE_URL}{API_PREFIX}/categories"
        category_names = ["Monthly Programs", "JW Broadcasting"]
        response = requests.post(
            url,
            json=category_names
        )

        # Check response
        assert response.status_code == 200
        data = response.json().get("data", [])
        assert len(data) == 2, (
            "Expected 2 resolved categories in response"
        )

        # Validate response structure
        for index, category in enumerate(data):
            assert "id" in category, (
                f"Missing 'id' in category at index {index}"
            )
            assert isinstance(category["id"], int), (
                f"'id' is not an integer in category at index {index}"
            )

            assert "name" in category, (
                f"Missing 'name' in category at index {index}"
            )
            assert isinstance(category["name"], str), (
                f"'name' is not a string in category at index {index}"
            )

    def test_resolve_valid_category_name(
        self,
        valid_category_name: str
    ) -> None:
        """
        Test resolving a valid category name returns 200 and correct structure.

        Arguments:
            valid_category_name: A valid category name provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/{valid_category_name}"
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert "success" in data
        assert "data" in data

        # Validate values
        assert data["success"] is True
        assert isinstance(data["data"]["category_id"], int)
        assert data["data"]["category_id"] > 0

    def test_resolve_invalid_category_name(
        self,
        invalid_category_name: str
    ) -> None:
        """
        Test resolving an invalid category name returns 404.

        Arguments:
            invalid_category_name:
                An invalid category name provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/category/{invalid_category_name}"
        response = requests.get(url)

        assert response.status_code == 404

    @pytest.mark.parametrize(
        "category_name,expected_id", [
            ("Monthly Programs", 1),
            ("JW Broadcasting", 1340),
        ]
    )
    def test_resolve_multiple_categories(
        self,
        category_name: str,
        expected_id: int
    ) -> None:
        """
        Test resolving multiple known categories.

        Arguments:
            category_name: The name of the category to resolve.
            expected_id: The expected category ID for the given name.
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/{category_name}"
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()

        assert data["data"]["category_id"] == expected_id


class TestCategoryVideoRetrieval:
    """
    Tests for /api/categories/{{category_id}}/{{subcategory_id}} endpoint.

    Methods:
        test_get_videos_valid_categories
            Test retrieving videos with valid category and subcategory IDs.
        test_get_videos_invalid_category
            Test retrieving videos with invalid category ID.
        test_get_videos_invalid_subcategory
            Test retrieving videos with invalid subcategory ID.
        test_get_videos_both_invalid
            Test retrieving videos with both IDs invalid.
    """

    def test_get_videos_valid_categories(
        self,
        valid_category_id: int,
        valid_subcategory_id: int
    ) -> None:
        """
        Test retrieving videos with valid category and subcategory IDs.

        Arguments:
            valid_category_id: A valid category ID provided by fixture.
            valid_subcategory_id: A valid subcategory ID provided by fixture.
        """

        url = (
            f"{BASE_URL}{API_PREFIX}/categories/"
            f"{valid_category_id}/{valid_subcategory_id}"
        )
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()

        # Validate response is a list
        assert isinstance(data["data"]["videos"], list)

        # If list is not empty, validate structure
        if len(data["data"]["videos"]) > 0:
            video = data["data"]["videos"][0]
            self._validate_video_structure(video)

    def test_get_videos_invalid_category(
        self,
        invalid_category_id: pytest.FixtureRequest,
        valid_subcategory_id: pytest.FixtureRequest
    ) -> None:
        """
        Test retrieving videos with invalid category ID.

        Arguments:
            invalid_category_id: An invalid category ID provided by fixture.
            valid_subcategory_id: A valid subcategory ID provided by fixture.
        """

        url = (
            f"{BASE_URL}{API_PREFIX}/categories/{invalid_category_id}/"
            f"{valid_subcategory_id}"
        )
        response = requests.get(url)

        # Should return empty list or 404
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert response.json()["data"]["videos"] == []

    def test_get_videos_invalid_subcategory(
        self,
        valid_category_id: int,
        invalid_category_id: int
    ) -> None:
        """
        Test retrieving videos with invalid subcategory ID.

        Arguments:
            valid_category_id: A valid category ID provided by fixture.
            invalid_category_id: An invalid category ID provided by fixture.
        """

        url = (
            f"{BASE_URL}{API_PREFIX}/categories/{valid_category_id}/"
            f"{invalid_category_id}"
        )
        response = requests.get(url)

        # Should return empty list or 404
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert response.json()["data"]["videos"] == []

    def test_get_videos_both_invalid(
        self,
        invalid_category_id: int
    ) -> None:
        """
        Test retrieving videos with both IDs invalid.

        Arguments:
            invalid_category_id: An invalid category ID provided by fixture.
        """

        url = (
            f"{BASE_URL}{API_PREFIX}/categories/{invalid_category_id}/"
            f"{invalid_category_id}"
        )
        response = requests.get(url)

        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert response.json()["data"]["videos"] == []

    def _validate_video_structure(
        self,
        video: Dict
    ) -> None:
        """
        Helper method to validate video object structure.

        Arguments:
            video: A dictionary representing a video object.
        """

        required_fields = [
            "id", "name", "description", "duration", "date_added",
            "thumbnail", "url", "url_1080", "url_720", "url_480",
            "url_360", "url_240"
        ]

        for field in required_fields:
            assert field in video, f"Missing field: {field}"

        # Validate data types
        assert isinstance(video["id"], int)
        assert isinstance(video["name"], str)
        assert isinstance(video["description"], str)
        assert isinstance(video["duration"], str)
        assert isinstance(video["date_added"], str)
        assert isinstance(video["thumbnail"], str)
        assert isinstance(video["url"], str)

        # URL fields can be null or string
        for url_field in [
            "url_1080", "url_720", "url_480", "url_360", "url_240"
        ]:
            assert (
                video[url_field] is None or
                isinstance(video[url_field], str)
            )

        # Validate URL formats
        if video["thumbnail"]:
            assert video["thumbnail"].startswith("http")
        if video["url"]:
            assert video["url"].startswith("http")


class TestVideoCategories:
    """
    Tests for /api/categories/video/{{video_id}} endpoint.

    Methods:
        test_get_categories_valid_video
            Test retrieving categories for a valid video ID.
        test_get_categories_invalid_video
            Test retrieving categories for an invalid video ID.
        test_get_categories_validates_category_ids
            Test that returned category IDs are positive integers.
        test_video_belongs_to_multiple_categories
            Test that a video can belong to multiple categories.
    """

    def test_get_categories_valid_video(
        self,
        valid_video_id
    ) -> None:
        """
        Test retrieving categories for a valid video ID.

        Arguments:
            valid_video_id: A valid video ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/video/{valid_video_id}"
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json().get("data", [])

        # Validate response is a list
        assert isinstance(data, list)

        # Validate category structure
        if len(data) > 0:
            category = data[0]
            assert "id" in category
            assert "name" in category
            assert isinstance(category["id"], int)
            assert isinstance(category["name"], str)

    def test_get_categories_invalid_video(
        self,
        invalid_video_id
    ) -> None:
        """
        Test retrieving categories for an invalid video ID.

        Arguments:
            invalid_video_id: An invalid video ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/video/{invalid_video_id}"
        response = requests.get(url)

        assert response.status_code == 404

    def test_get_categories_validates_category_ids(
        self,
        valid_video_id
    ) -> None:
        """
        Test that returned category IDs are positive integers.

        Arguments:
            valid_video_id: A valid video ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/video/{valid_video_id}"
        response = requests.get(url)
        assert response.status_code == 200

        data = response.json().get("data", [])
        for category in data:
            assert category["id"] > 0

    def test_video_belongs_to_multiple_categories(
        self,
        valid_video_id
    ) -> None:
        """
        Test that a video can belong to multiple categories.

        Arguments:
            valid_video_id: A valid video ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/video/{valid_video_id}"
        response = requests.get(url)
        assert response.status_code == 200

        data = response.json().get("data", [])
        assert len(data) >= 1
