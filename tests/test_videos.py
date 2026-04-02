"""
Module: test_videos.py

Unit tests for video-related API endpoints.

Endpoints Tested:
    - /api/videos/{{video_id}}
    - /api/videos/get_bulk
    - /api/videos/filter
    - /api/videos/metadata
    - /api/videos/add

Classes:
    TestGetVideo
        Tests for retrieving video details by ID.
    TestGetVideoBulk
        Tests for retrieving multiple videos by their IDs.
    TestGetFilteredVideos
        Tests for retrieving videos based on filter criteria.
"""


import requests


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestGetVideoBulk:
    """
    Tests for the GET /api/videos/get_bulk endpoint.

    Methods:
        test_get_videos_bulk
            Success: Test retrieving multiple videos by their IDs.
        test_missing_body
            Failure: A request without a body.
        test_missing_ids
            Failure: A request body that does not contain video IDs.
        test_invalid_ids
            Failure: A request body that contains invalid video IDs.
    """

    def test_get_videos_bulk(
        self,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving multiple videos by their IDs.

        Test:
            - Endpoint returns status code 200
            - Response contains a list of video details
        """

        url = f"{BASE_URL}{API_PREFIX}/videos/get_bulk"
        body = {
            "video_ids": [valid_video_id]
        }
        response = requests.post(
            url,
            json=body
        )
        assert response.status_code == 200

        # Validate response
        data = response.json().get('data', [])
        assert isinstance(data, list)

        # Validate structure
        if len(data) > 0:
            for index, item in enumerate(data):
                assert "id" in item, (
                    f"Video at index {index} is missing 'id'"
                )
                assert isinstance(item["id"], int), (
                    f"Video at index {index} has 'id' of type "
                    f"{item!r}, expected int"
                )

                assert "name" in item, (
                    f"Video at index {index} is missing 'name'"
                )
                assert isinstance(item["name"], str), (
                    f"Video at index {index} has 'name' of type "
                    f"{item!r}, expected str"
                )

                assert "description" in item, (
                    f"Video at index {index} is missing 'description'"
                )
                assert isinstance(item["description"], str), (
                    f"Video at index {index} has 'description' of type "
                    f"{item!r}, expected str"
                )

                assert "url" in item, (
                    f"Video at index {index} is missing 'url'"
                )

                assert "duration" in item, (
                    f"Video at index {index} is missing 'duration'"
                )
                assert isinstance(item["duration"], int), (
                    f"Video at index {index} has 'duration' of type "
                    f"{item!r}, expected int"
                )

                assert "date_added" in item, (
                    f"Video at index {index} is missing 'date_added'"
                )
                assert isinstance(item["date_added"], str), (
                    f"Video at index {index} has 'date_added' of type "
                    f"{item!r}, expected str"
                )

                assert "thumbnail" in item, (
                    f"Video at index {index} is missing 'thumbnail'"
                )
                assert isinstance(item["thumbnail"], str), (
                    f"Video at index {index} has 'thumbnail' of type "
                    f"{item!r}, expected str"
                )

                assert "url_1080" in item, (
                    f"Video at index {index} is missing 'url_1080'"
                )
                assert "url_720" in item, (
                    f"Video at index {index} is missing 'url_720'"
                )
                assert "url_480" in item, (
                    f"Video at index {index} is missing 'url_480'"
                )
                assert "url_360" in item, (
                    f"Video at index {index} is missing 'url_360'"
                )
                assert "url_240" in item, (
                    f"Video at index {index} is missing 'url_240'"
                )

    def test_missing_body(
        self
    ) -> None:
        """
        Test retrieving multiple videos without providing a request body.

        Test:
            - Endpoint returns status code 415 for missing body
        """

        url = f"{BASE_URL}{API_PREFIX}/videos/get_bulk"
        response = requests.post(url)

        assert response.status_code == 415

    def test_missing_ids(
        self
    ) -> None:
        """
        Test retrieving multiple videos with a
            request body that does not contain video IDs.

        Test:
            - Endpoint returns status code 400 for missing video IDs
        """

        url = f"{BASE_URL}{API_PREFIX}/videos/get_bulk"
        body = {}
        response = requests.post(
            url,
            json=body
        )

        assert response.status_code == 400

    def test_invalid_ids(
        self
    ) -> None:
        """
        Test retrieving multiple videos with a request body
            that contains invalid video IDs.

        Test:
            - Endpoint returns status code 400 for invalid video IDs
        """

        url = f"{BASE_URL}{API_PREFIX}/videos/get_bulk"
        body = {
            "video_ids": [1, "two", 3]
        }
        response = requests.post(
            url,
            json=body
        )

        assert response.status_code == 400


class TestGetFilteredVideos:
    """
    Tests for the POST /api/videos/filter endpoint.

    Methods:
        test_get_recent_videos
            Success: Test retrieving videos based on filter criteria.
        test_multiple_filters
            Success: Test retrieving videos based on multiple filter criteria.
        test_no_params
            Failure: Retrieving videos without providing any filter parameters.
        test_invalid_params
            Failure: Retrieving videos with invalid filter parameters.
    """

    def test_get_recent_videos(
        self,
    ) -> None:
        """
        Test retrieving videos based on filter criteria.

        Test:
            - Endpoint returns status code 200 for valid filters
            - Response contains a list of filtered video details
        """

        url = f"{BASE_URL}{API_PREFIX}/videos/filter"
        params = {
            "latest": 5
        }
        response = requests.get(
            url,
            params=params
        )
        assert response.status_code == 200

        # Validate response
        data = response.json().get('data', [])
        assert isinstance(data, list)
        assert len(data) > 0

    def test_multiple_filters(
        self,
    ) -> None:
        """
        Test retrieving videos based on multiple filter criteria.

        Test:
            - Endpoint returns status code 200 for valid filters
            - Response contains a list of filtered video details
            - Each video in the response contains expected fields
        """

        url = f"{BASE_URL}{API_PREFIX}/videos/filter"
        params = {
            "latest": 1,
            "cat": 1,
            "tag": 5,
            "speak": 1,
            "char": 1,
            "scrip": 2
        }
        response = requests.get(
            url,
            params=params
        )

        assert response.status_code == 200
        data = response.json().get('data', [])
        assert isinstance(data, list)

        for item in data:
            assert "id" in item
            assert "name" in item
            assert "description" in item
            assert "url" in item
            assert "duration" in item
            assert "date_added" in item
            assert "thumbnail" in item
            assert "url_1080" in item
            assert "url_720" in item
            assert "url_480" in item
            assert "url_360" in item
            assert "url_240" in item

    def test_no_params(
        self
    ) -> None:
        """
        Test retrieving videos without providing any filter parameters.

        Test:
            - Endpoint returns status code 400
            - Response contains a list of all video details
        """

        url = f"{BASE_URL}{API_PREFIX}/videos/filter"
        response = requests.get(url)

        assert response.status_code == 400

    def test_invalid_params(
        self
    ) -> None:
        """
        Test retrieving videos with invalid filter parameters.

        Test:
            - Endpoint returns status code 400 for invalid filter parameters
        """

        url = f"{BASE_URL}{API_PREFIX}/videos/filter"
        params = {
            "latest": "five",
            "cat": "one",
            "tag": "five",
            "speak": "one",
            "char": "one",
            "scrip": "two"
        }
        response = requests.get(
            url,
            params=params
        )

        assert response.status_code == 400


class TestVideoMetadata:
    """
    Tests for the GET and POST /api/videos/metadata endpoint.

    Methods:
        test_get_video_metadata
            Success: Test retrieving video metadata.
    """

    def test_get_video_metadata(
        self
    ) -> None:
        """
        Test retrieving video metadata.

        Test:
            - Endpoint returns status code 200
            - Response contains expected metadata fields
        """

        url = f"{BASE_URL}{API_PREFIX}/videos/metadata"
        params = {
            "video_name": "Can Love Conquer Hatred?",
            "tag_name": "av",
            "location_name": "Africa",
            "character_name": "Jesus",
            "speaker_name": "Stephen Lett"
        }
        response = requests.get(url, params=params)
        assert response.status_code == 200

        # Validate response
        data = response.json().get('data', {})
        assert "character_id" in data
        assert isinstance(data["character_id"], int)
        assert "location_id" in data
        assert isinstance(data["location_id"], int)
        assert "speaker_id" in data
        assert isinstance(data["speaker_id"], int)
        assert "video_id" in data
        assert isinstance(data["video_id"], int)
