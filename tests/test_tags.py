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
        """

        url = f"{BASE_URL}{API_PREFIX}/tags"
        response = requests.get(url)

        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestGetTag:
    """
    Tests for the GET /api/tags/<int:tag_id> endpoint.

    Methods:
        test_get_tag_by_id
            Test retrieving tag details by ID.
        test_get_tag_by_invalid_id
            Test retrieving tag details with an invalid ID.
    """

    def test_get_tag_by_id(
        self,
        valid_tag_id: int
    ) -> None:
        """
        Test retrieving tag details by ID.

        Test:
            - Endpoint returns status code 200 for valid ID
        """

        # Test with a valid tag ID (assuming 1 is valid)
        valid_url = f"{BASE_URL}{API_PREFIX}/tags/{valid_tag_id}"
        valid_response = requests.get(valid_url)

        assert valid_response.status_code == 200
        assert isinstance(valid_response.json(), dict)

    def test_get_tag_by_invalid_id(
        self,
        invalid_tag_id: int
    ) -> None:
        """
        Test retrieving tag details with an invalid ID.

        Test:
            - Endpoint returns status code 404 for invalid ID
        """

        # Test with an invalid tag ID (assuming -1 is invalid)
        invalid_url = f"{BASE_URL}{API_PREFIX}/tags/{invalid_tag_id}"
        invalid_response = requests.get(invalid_url)

        assert invalid_response.status_code == 404


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
        """

        url = f"{BASE_URL}{API_PREFIX}/tags/video/{valid_video_id}"
        response = requests.get(url)

        assert response.status_code == 200
        assert isinstance(response.json(), list)

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
