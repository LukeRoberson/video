"""
Module: test_characters.py

Unit tests for character-related API endpoints.

Endpoints tested:
    - GET /api/characters
    - GET /api/characters/{id}
    - GET /api/characters/video/{video_id}

Classes:
    TestAllCharacters
        Tests for retrieving all characters.
    TestCharacters
        Tests for retrieving character details by ID.
    TestVideoCharacters
        Tests for retrieving characters associated with a specific video ID.
"""

import requests

# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestAllCharacters:
    """
    Tests for /api/characters endpoint.

    Methods:
        test_get_all_characters
            Test retrieving all characters.
    """

    def test_get_all_characters(
        self
    ) -> None:
        """
        Test retrieving all characters.

        Arguments:
             None

        Test:
            - Endpoint returns status code 200
            - Response is a list
            - List is not empty
            - Each item in the list has the expected structure
        """

        url = f"{BASE_URL}{API_PREFIX}/characters"
        response = requests.get(url)
        assert response.status_code == 200

        # Validate response structure
        data = response.json().get("data", [])
        assert isinstance(data, list)
        assert len(data) > 0

        # Validate that each item in the list has the expected structure
        assert all(isinstance(item, dict) for item in data)
        assert all(
            "id" in item and
            "name" in item and
            "description" in item and
            "profile_pic" in item and
            "date_range" in item
            for item in data
        )


class TestCharacters:
    """
    Tests for /api/characters/{character_id} endpoint.

    Methods:
        test_get_character_by_id
            Test retrieving character details by ID.
        test_get_character_by_invalid_id
            Test retrieving character details with an invalid ID.
    """

    def test_get_character_by_id(
        self,
        valid_character_id: int
    ) -> None:
        """
        Test retrieving character details by ID.

        Arguments:
            valid_character_id: A valid character ID provided by fixture.

        Test:
            - Endpoint returns status code 200
            - Response contains correct character ID
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/{valid_character_id}"
        response = requests.get(url)
        assert response.status_code == 200

        # Validate response structure and content
        data = response.json().get("data", {})
        assert "date_range" in data
        assert isinstance(data["date_range"], str)
        assert "description" in data
        assert isinstance(data["description"], str)
        assert "id" in data
        assert isinstance(data["id"], int)
        assert "name" in data
        assert isinstance(data["name"], str)
        assert "profile_pic" in data
        assert isinstance(data["profile_pic"], str)

    def test_get_character_by_invalid_id(
        self,
        invalid_character_id: int
    ) -> None:
        """
        Test retrieving character details with an invalid ID.

        Arguments:
            invalid_character_id: An invalid character ID provided by fixture.

        Test:
            - Endpoint returns status code 404
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/{invalid_character_id}"
        response = requests.get(url)

        assert response.status_code == 404


class TestVideoCharacters:
    """
    Tests for /api/characters/video/{video_id} endpoint.

    Methods:
        test_get_characters_by_video_id
            Test retrieving characters associated with a specific video ID.
        test_get_characters_by_invalid_video_id
            Test retrieving characters with an invalid video ID.
    """

    def test_get_characters_by_video_id(
        self,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving characters associated with a specific video ID.

        Arguments:
            valid_video_id: A valid video ID provided by fixture.

        Test:
            - Endpoint returns status code 200
            - Response is a list
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/video/{valid_video_id}"
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json().get("data", [])

        assert isinstance(data, list)
        if len(data) > 0:
            assert all(isinstance(item, dict) for item in data)
            assert all(
                "id" in item and
                "name" in item and
                "description" in item and
                "profile_pic" in item and
                "date_range" in item
                for item in data
            )

    def test_get_characters_by_invalid_video_id(
        self,
        invalid_video_id: int
    ) -> None:
        """
        Test retrieving characters associated with an invalid video ID.

        Arguments:
            invalid_video_id: An invalid video ID provided by fixture.

        Test:
            - Endpoint returns status code 404
        """

        url = f"{BASE_URL}{API_PREFIX}/characters/video/{invalid_video_id}"
        response = requests.get(url)

        assert response.status_code == 404
