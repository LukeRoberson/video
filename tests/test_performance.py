"""
Module: test_performance.py

Test the performance of key API endpoints
    to ensure they respond within acceptable time limits.

Classes:
    TestCategories
        Basic performance tests for category-related endpoints.
    TestCharacters
        Basic performance tests for character-related endpoints.
    TestSimilarity
        Basic performance tests for similarity-related endpoints.
"""


import requests


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestCategories:
    """
    Basic performance tests.

    Methods:
        test_response_time_category_lookup
            Test that category lookup responds within acceptable time.
        test_response_time_video_retrieval
            Test that video retrieval responds within acceptable time.
    """

    def test_response_time_category_lookup(
        self,
        valid_category_name: str
    ) -> None:
        """
        Test that category lookup responds within acceptable time.

        Arguments:
            valid_category_name: A valid category name provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/category/{valid_category_name}"
        response = requests.get(url)

        # Should respond within 2 seconds
        assert response.elapsed.total_seconds() < 2.1

    def test_response_time_video_retrieval(
        self,
        valid_category_id: int,
        valid_subcategory_id: int
    ) -> None:
        """
        Test that video retrieval responds within acceptable time.

        Arguments:
            valid_category_id: A valid category ID provided by fixture.
            valid_subcategory_id: A valid subcategory ID provided by fixture.
        """

        url = (
            f"{BASE_URL}{API_PREFIX}/categories/{valid_category_id}/"
            f"{valid_subcategory_id}"
        )
        response = requests.get(url)

        # Should respond within 5 seconds (may return multiple videos)
        assert response.elapsed.total_seconds() < 5.0


class TestCharacters:
    """
    Basic performance tests for character-related endpoints.

    Methods:
        test_response_time_all_characters
            Test retrieving all characters response time.
        test_response_time_character_lookup
            Test character lookup response time.
        test_response_time_video_characters
            Test retrieving characters for a video response time.
    """

    def test_response_time_all_characters(
        self
    ) -> None:
        """
        Test retrieving all characters response time.
        """

        url = f"{BASE_URL}{API_PREFIX}/characters"
        response = requests.get(url)

        # Should respond within 2 seconds
        assert response.elapsed.total_seconds() < 2.1

    def test_response_time_character_lookup(
        self,
        valid_character_id: int
    ) -> None:
        """
        Test character lookup response time.

        Arguments:
            valid_character_id: A valid character ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/{valid_character_id}"
        response = requests.get(url)

        # Should respond within 2 seconds
        assert response.elapsed.total_seconds() < 2.1

    def test_response_time_video_characters(
        self,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving characters for a video response time.

        Arguments:
            valid_video_id: A valid video ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/video/{valid_video_id}"
        response = requests.get(url)

        # Should respond within 3 seconds (may return multiple characters)
        assert response.elapsed.total_seconds() < 3.0


class TestSimilarity:
    """
    Basic performance tests for similarity-related endpoints.

    Methods:
        test_response_time_similarity_lookup
            Test similarity lookup response time.
    """

    def test_response_time_similarity_lookup(
        self,
        valid_video_id: int
    ) -> None:
        """
        Test similarity lookup response time.

        Arguments:
            valid_video_id: A valid video ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/similarity/{valid_video_id}"
        response = requests.get(url)

        # Should respond within 3 seconds (may return multiple similar videos)
        assert response.elapsed.total_seconds() < 3.0
