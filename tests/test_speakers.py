"""
Module: test_speakers.py

Unit tests for speaker-related API endpoints.

Endpoints Tested:
    - GET /api/speakers
    - GET /api/speakers/<int:speaker_id>
    - GET /api/speakers/video/<int:video_id>

Classes:
    TestSpeakerList
        Tests for retrieving the list of all speakers.
    TestVideoSpeakers
        Tests for retrieving speakers associated with a video.
"""


import requests


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestSpeakerList:
    """
    Tests for the GET /api/speakers endpoint.

    Methods:
        test_get_all_speakers
            Test retrieving the list of all speakers.
        test_get_speaker_by_id
            Test retrieving speaker details by ID.
        test_get_speaker_by_invalid_id
            Test retrieving speaker details with an invalid ID.
    """

    def test_get_all_speakers(
        self
    ) -> None:
        """
        Test retrieving the list of all speakers.

        Test:
            - Endpoint returns status code 200
            - Response is a list
        """

        url = f"{BASE_URL}{API_PREFIX}/speakers"
        response = requests.get(url)
        assert response.status_code == 200

        # Validate response
        data = response.json().get("data", [])
        assert isinstance(data, list)

        # Validate structure and types
        assert all(
            ("id" in speaker and isinstance(speaker["id"], int)) and
            ("name" in speaker and isinstance(speaker["name"], str)) and
            ("profile_pic" in speaker)
            for speaker in data
        )

    def test_get_speaker_by_id(
        self,
        valid_speaker_id: int
    ) -> None:
        """
        Test retrieving speaker details by ID.

        Test:
            - Endpoint returns status code 200 for valid ID
            - Endpoint returns a JSON object
            - Response contains expected speaker details
        """

        # Test with a valid speaker ID (assuming ID 1 exists)
        url = f"{BASE_URL}{API_PREFIX}/speakers"
        params = {"spk_id": valid_speaker_id}
        response = requests.get(url, params=params)
        assert response.status_code == 200

        # Validate the response
        data = response.json().get("data", [])
        assert isinstance(data, list)
        assert len(data) == 1

        # Validate the structure and type
        speaker = data[0]
        assert isinstance(speaker, dict)
        assert "id" in speaker and isinstance(speaker["id"], int)
        assert "name" in speaker and isinstance(speaker["name"], str)
        assert (
            "profile_pic" in speaker and
            isinstance(speaker["profile_pic"], str)
        )
        assert (
            "video_count" in speaker and
            isinstance(speaker["video_count"], int)
        )

    def test_get_speaker_by_invalid_id(
        self,
        invalid_speaker_id: int
    ) -> None:
        """
        Test retrieving speaker details with an invalid ID.

        Test:
            - Endpoint returns status code 500 for invalid ID
        """

        # Test with an invalid speaker ID (assuming ID 9999 does not exist)
        url = f"{BASE_URL}{API_PREFIX}/speakers"
        params = {"spk_id": invalid_speaker_id}
        response = requests.get(url, params=params)

        # Validate the response
        assert response.status_code == 500


class TestVideoSpeakers:
    """
    Tests for the GET /api/speakers/video/<int:video_id> endpoint.

    Methods:
        test_get_video_speakers_by_video_id
            Test retrieving speakers for a video by its ID.
        test_get_video_speakers_by_invalid_video_id
            Test retrieving speakers with an invalid video ID.
    """

    def test_get_video_speakers_by_video_id(
        self,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving speakers for a video by its ID.

        Test:
            - Endpoint returns status code 200 for valid video ID
            - Endpoint returns a list
        """

        url = f"{BASE_URL}{API_PREFIX}/speakers/video/{valid_video_id}"
        response = requests.get(url)
        assert response.status_code == 200

        # Validate the response
        data = response.json().get("data", [])
        assert isinstance(data, list)

        # Validate structure and types
        assert all(
            ("id" in speaker and isinstance(speaker["id"], int)) and
            ("name" in speaker and isinstance(speaker["name"], str)) and
            ("profile_pic" in speaker)
            for speaker in data
        )

    def test_get_video_speakers_by_invalid_video_id(
        self,
        invalid_video_id: int
    ) -> None:
        """
        Test retrieving speakers with an invalid video ID.

        Test:
            - Endpoint returns status code 404 for invalid video ID
        """

        url = f"{BASE_URL}{API_PREFIX}/speakers/video/{invalid_video_id}"
        response = requests.get(url)

        assert response.status_code == 404
