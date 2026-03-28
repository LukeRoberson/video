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

        # Validate response structure
        data = response.json().get("data")
        assert isinstance(data, list)

        # Validate the structure in each entry, and their types
        if len(data) > 0:
            for index, video in enumerate(data):
                assert isinstance(video, dict), (
                    f"Entry at index {index} is not a dictionary"
                )
                assert "score" in video, (
                    f"Entry at index {index} is missing 'score'"
                )
                assert isinstance(video["score"], float), (
                    f"'score' in entry at index {index} is not a float"
                )
                assert "video_1_id" in video, (
                    f"Entry at index {index} is missing 'video_1_id'"
                )
                assert isinstance(video["video_1_id"], int), (
                    f"'video_1_id' in entry at index {index} is not an int"
                )
                assert "video_2_id" in video, (
                    f"Entry at index {index} is missing 'video_2_id'"
                )
                assert isinstance(video["video_2_id"], int), (
                    f"'video_2_id' in entry at index {index} is not an int"
                )

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
