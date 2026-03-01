"""
Module: test_errors.py

Unit tests for error handling and edge cases in API endpoints.

Classes:
    TestCategoryErrorHandling
        Tests for error handling for category-related endpoints.
"""

import requests

# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestCategoryErrorHandling:
    """
    Tests for error handling for category-related endpoints.

    Methods:
        test_invalid_http_methods_category_name
            Test that invalid HTTP methods are rejected for
                category name endpoint.
        test_malformed_category_id
            Test that non-numeric category IDs are rejected.
        test_negative_category_id
            Test that negative category IDs are rejected.
        test_response_content_type
            Test that API returns JSON content type for category name endpoint.
    """

    def test_invalid_http_methods_category_name(
        self,
        valid_category_name: str
    ) -> None:
        """
        Test that invalid HTTP methods are rejected.

        Arguments:
            valid_category_name: A valid category name provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/{valid_category_name}"

        response = requests.post(url)
        assert response.status_code in [405, 501]

        response = requests.put(url)
        assert response.status_code in [405, 501]

        response = requests.delete(url)
        assert response.status_code in [405, 501]

    def test_malformed_category_id(
        self
    ) -> None:
        """
        Test with non-numeric category ID.

        Arguments:
            None
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/abc/123"
        response = requests.get(url)

        assert response.status_code in [400, 404]

    def test_negative_category_id(
        self
    ) -> None:
        """
        Test with negative category ID.

        Arguments:
            None
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/-1/-1"
        response = requests.get(url)

        assert response.status_code in [400, 404]

    def test_response_content_type(
        self,
        valid_category_name: str
    ) -> None:
        """
        Test that API returns JSON content type.

        Arguments:
            valid_category_name: A valid category name provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/categories/{valid_category_name}"
        response = requests.get(url)

        assert "application/json" in response.headers.get("Content-Type", "")


class TestCharacterErrorHandling:
    """
    Tests for error handling for character-related endpoints.

    Methods:
        test_invalid_http_methods_character_id
            Test that invalid HTTP methods are rejected for
                character ID endpoint.
        test_malformed_character_id
            Test that non-numeric character IDs are rejected.
        test_negative_character_id
            Test that negative character IDs are rejected.
        test_response_content_type_character_id
            Test that API returns JSON content type for character ID endpoint.
    """

    def test_invalid_http_methods_character_id(
        self,
        valid_character_id: int
    ) -> None:
        """
        Test that invalid HTTP methods are rejected.

        Arguments:
            valid_character_id: A valid character ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/{valid_character_id}"

        response = requests.post(url)
        assert response.status_code in [405, 501]

        response = requests.put(url)
        assert response.status_code in [405, 501]

        response = requests.delete(url)
        assert response.status_code in [405, 501]

    def test_malformed_character_id(
        self
    ) -> None:
        """
        Test with non-numeric character ID.

        Arguments:
            None
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/abc"
        response = requests.get(url)

        assert response.status_code in [400, 404]

    def test_negative_character_id(
        self
    ) -> None:
        """
        Test with negative character ID.

        Arguments:
            None
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/-1"
        response = requests.get(url)

        assert response.status_code in [400, 404]

    def test_response_content_type_character_id(
        self,
        valid_character_id: int
    ) -> None:
        """
        Test that API returns JSON content type.

        Arguments:
            valid_character_id: A valid character ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/{valid_character_id}"
        response = requests.get(url)

        assert "application/json" in response.headers.get("Content-Type", "")


class TestSimilarityErrorHandling:
    """
    Tests for error handling for similarity-related endpoints.

    Methods:
        test_invalid_http_methods_similarity
            Test that invalid HTTP methods are rejected for
                similarity endpoint.
        test_malformed_similarity_parameters
            Test that malformed parameters are rejected.
        test_response_content_type_similarity
            Test that API returns JSON content type for similarity endpoint.
    """

    def test_invalid_http_methods_similarity(
        self,
        valid_video_id: str
    ) -> None:
        """
        Test that invalid HTTP methods are rejected.

        Arguments:
            valid_video_id: A valid video ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/similarity/{valid_video_id}"

        response = requests.post(url)
        assert response.status_code in [405, 501]

        response = requests.put(url)
        assert response.status_code in [405, 501]

        response = requests.delete(url)
        assert response.status_code in [405, 501]

    def test_malformed_similarity_parameters(
        self,
        valid_video_id: str
    ) -> None:
        """
        Test that malformed parameters are rejected.

        Arguments:
            valid_video_id: A valid video ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/similarity/{valid_video_id}/abc/def"
        response = requests.get(url)

        assert response.status_code in [400, 404]

    def test_response_content_type_similarity(
        self,
        valid_video_id: str
    ) -> None:
        """
        Test that API returns JSON content type.

        Arguments:
            valid_video_id: A valid video ID provided by fixture.
        """

        url = f"{BASE_URL}{API_PREFIX}/similarity/{valid_video_id}"
        response = requests.get(url)

        assert "application/json" in response.headers.get("Content-Type", "")
