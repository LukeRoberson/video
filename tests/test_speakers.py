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
    TestGetSpeaker
        Tests for retrieving speaker details by ID.
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
        assert isinstance(response.json(), list)


class TestGetSpeaker:
    """
    Tests for the GET /api/speakers/<int:speaker_id> endpoint.

    Methods:
        test_get_speaker_by_id
            Test retrieving speaker details by ID.
        test_get_speaker_by_invalid_id
            Test retrieving speaker details with an invalid ID.
    """

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
        url = f"{BASE_URL}{API_PREFIX}/speakers/{valid_speaker_id}"
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data.get("id") == valid_speaker_id

    def test_get_speaker_by_invalid_id(
        self,
        invalid_speaker_id: int
    ) -> None:
        """
        Test retrieving speaker details with an invalid ID.

        Test:
            - Endpoint returns status code 404 for invalid ID
        """

        # Test with an invalid speaker ID (assuming ID 9999 does not exist)
        url = f"{BASE_URL}{API_PREFIX}/speakers/{invalid_speaker_id}"
        response = requests.get(url)

        assert response.status_code == 404


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
        data = response.json()
        assert isinstance(data, list)

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
