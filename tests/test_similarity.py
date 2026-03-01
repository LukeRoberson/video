"""
Module: test_similarity.py

Unit tests for similarity-related API endpoints.

Endpoints tested:
    - GET /api/similarity/{video_id}

Classes:
    TestSimilarity
        Tests for retrieving similar videos for a given video ID.
"""

import requests

# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestSimilarity:
    """
    Tests for /api/similarity/{video_id} endpoint.

    Methods:
        test_get_similarity
            Test retrieving similar videos for a given video ID.
        test_get_similarity_invalid_video_id
            Test retrieving similar videos with an invalid video ID.
    """

    def test_get_similarity(
        self,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving similar videos for a given video ID.

        Arguments:
            valid_video_id (int): A valid video ID to test with.

        Test:
            - Endpoint returns status code 200
            - Response is a list
        """

        url = f"{BASE_URL}{API_PREFIX}/similarity/{valid_video_id}"
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_similarity_invalid_video_id(
        self,
        invalid_video_id: int
    ) -> None:
        """
        Test retrieving similar videos with an invalid video ID.

        Arguments:
            invalid_video_id (int): An invalid video ID to test with.

        Test:
            - Endpoint returns status code 404
        """

        url = f"{BASE_URL}{API_PREFIX}/similarity/{invalid_video_id}"
        response = requests.get(url)

        assert response.status_code == 404
