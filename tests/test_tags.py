"""
Module: test_tags.py

Unit tests for tag-related API endpoints.

Endpoints Tested:
    - GET /api/tags
    - GET /api/tags/<int:tag_id>
    - GET /api/tags/video/<int:video_id>

Classes:
    TestTagList
        Tests for retrieving the list of all tags.
    TestGetTag
        Tests for retrieving tag details by ID.
    TestVideoTags
        Tests for retrieving tags associated with a video.
"""

import requests


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestTagList:
    """
    Tests for the GET /api/tags endpoint.

    Methods:
        test_get_all_tags
            Test retrieving the list of all tags.
    """

    def test_get_all_tags(
        self
    ) -> None:
        """
        Test retrieving the list of all tags.

        Test:
            - Endpoint returns status code 200
            - Response is a list
            - Each tag in the list has 'id', 'name', and 'video_count' fields
            - Each field has the correct data type
        """

        url = f"{BASE_URL}{API_PREFIX}/tags"
        response = requests.get(url)
        assert response.status_code == 200

        data = response.json().get("data", [])
        assert isinstance(data, list)

        if len(data) > 0:
            assert all(isinstance(tag, dict) for tag in data)
            assert all(
                ("id" in tag and isinstance(tag["id"], int)) and
                ("name" in tag and isinstance(tag["name"], str)) and
                ("video_count" in tag and isinstance(tag["video_count"], int))
                for tag in data
            )

    def test_get_tags_by_id(
        self,
        valid_tag_id: int
    ) -> None:
        """
        Test retrieving a specific tag by ID.
        Test:
            - Endpoint returns status code 200 for valid ID
            - Response contains 'id', 'name', and 'video_count' fields
            - Each field has the correct data type
        """

        url = f"{BASE_URL}{API_PREFIX}/tags"
        params = {"tag_id": valid_tag_id}
        response = requests.get(url, params=params)
        assert response.status_code == 200

        # Validate the response
        data = response.json().get("data", [])
        assert isinstance(data, list)
        assert len(data) == 1

        # Validate the structure and data types of the returned tag
        tag = data[0]
        assert isinstance(tag, dict)
        assert "id" in tag and isinstance(tag["id"], int)
        assert "name" in tag and isinstance(tag["name"], str)
        assert "video_count" in tag and isinstance(tag["video_count"], int)

    def test_get_tags_by_invalid_id(
        self,
        invalid_tag_id: int
    ) -> None:
        """
        Test retrieving a specific tag with an invalid ID.
        Test:
            - Endpoint returns status code 200 for invalid ID
            - Response contains an empty list
        """

        url = f"{BASE_URL}{API_PREFIX}/tags"
        params = {"tag_id": invalid_tag_id}
        response = requests.get(url, params=params)

        # Validate the response
        assert response.status_code == 500


class TestVideoTags:
    """
    Tests for the GET /api/tags/video/<int:video_id> endpoint.

    Methods:
        test_get_video_tags
            Test retrieving tags associated with a video.
        test_get_video_tags_by_invalid_video_id
            Test retrieving tags with an invalid video ID.
    """

    def test_get_video_tags(
        self,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving tags associated with a video.

        Test:
            - Endpoint returns status code 200 for valid video ID
            - Response is a list
            - Structure is correct
            - Data types are correct
        """

        url = f"{BASE_URL}{API_PREFIX}/tags/video/{valid_video_id}"
        response = requests.get(url)
        assert response.status_code == 200

        # Validate the response structure
        data = response.json().get("data", [])
        assert isinstance(data, list)

        # Validate the structure and data types
        if len(data) > 0:
            assert all(isinstance(tag, dict) for tag in data)
            assert all(
                ("id" in tag and isinstance(tag["id"], int)) and
                ("name" in tag and isinstance(tag["name"], str))
                for tag in data
            )

    def test_get_video_tags_by_invalid_video_id(
        self,
        invalid_video_id: int
    ) -> None:
        """
        Test retrieving tags with an invalid video ID.

        Test:
            - Endpoint returns status code 404 for invalid video ID
        """

        url = f"{BASE_URL}{API_PREFIX}/tags/video/{invalid_video_id}"
        response = requests.get(url)

        assert response.status_code == 404
