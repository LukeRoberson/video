"""
Module: test_locations.py

Unit tests for location-related API endpoints.

Endpoints Tested:
    - GET /api/locations
    - GET /api/locations/<int:location_id>
    - GET /api/locations/video/<int:video_id>

Classes:
    TestLocationList
        Tests for retrieving the list of all locations.
    TestGetLocation
        Tests for retrieving location details by ID.
    TestVideoLocations
        Tests for retrieving locations associated with a video.
"""


import requests


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestLocationList:
    """
    Tests for the GET /api/locations endpoint.

    Methods:
        test_get_all_locations
            Test retrieving the list of all locations.

    Test:
        - Endpoint returns status code 200
        - Response is a list
    """

    def test_get_all_locations(
        self
    ) -> None:
        """
        Test retrieving the list of all locations.

        Test:
            - Endpoint returns status code 200
            - Response is a list
        """

        url = f"{BASE_URL}{API_PREFIX}/locations"
        response = requests.get(url)
        assert response.status_code == 200

        # The response should contain a list of locations
        data = response.json().get("data", [])
        assert isinstance(data, list)

        # Validate the structure and type
        if len(data) > 0:
            assert all(
                ("id" in loc and isinstance(loc["id"], int)) and
                ("name" in loc and isinstance(loc["name"], str))
                for loc in data
            )


class TestGetLocation:
    """
    Tests for the GET /api/locations/<int:location_id> endpoint.

    Methods:
        test_get_location_by_id
            Test retrieving location details by ID.
        test_get_location_by_invalid_id
            Test retrieving location details with an invalid ID.
    """

    def test_get_location_by_id(
        self,
        valid_location_id: int
    ) -> None:
        """
        Test retrieving location details by ID.

        Test:
            - Endpoint returns status code 200 for valid ID
            - Response contains expected location details
        """

        # Assuming a location with ID 1 exists for testing
        url = f"{BASE_URL}{API_PREFIX}/locations/{valid_location_id}"
        response = requests.get(url)
        assert response.status_code == 200

        # Validate the response type
        data = response.json().get("data", {})
        assert isinstance(data, dict)

        # Validate the contents of the response
        assert "id" in data and isinstance(data["id"], int)
        assert "name" in data and isinstance(data["name"], str)

    def test_get_location_by_invalid_id(
        self,
        invalid_location_id: int
    ) -> None:
        """
        Test retrieving location details with an invalid ID.

        Test:
            - Endpoint returns status code 404 for invalid ID
            - Response contains error message
        """

        # Using an unlikely high ID to ensure it does not exist
        url = f"{BASE_URL}{API_PREFIX}/locations/{invalid_location_id}"
        response = requests.get(url)

        assert response.status_code == 404
        assert "error" in response.json()


class TestVideoLocations:
    """
    Tests for the GET /api/locations/video/<int:video_id> endpoint.

    Methods:
        test_get_video_locations_by_video_id
            Test retrieving locations for a video by its ID.
        test_get_video_locations_by_invalid_video_id
            Test retrieving locations with an invalid video ID.
    """

    def test_get_video_locations_by_video_id(
        self,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving locations for a video by its ID.

        Test:
            - Endpoint returns status code 200 for valid video ID
            - Response is a list of locations
        """

        url = f"{BASE_URL}{API_PREFIX}/locations/video/{valid_video_id}"
        response = requests.get(url)
        assert response.status_code == 200

        # Validate response
        data = response.json().get("data", [])
        assert isinstance(data, list)

        # Validate structure and type
        assert all(
            ("id" in loc and isinstance(loc["id"], int)) and
            ("name" in loc and isinstance(loc["name"], str))
            for loc in data
        )

    def test_get_video_locations_by_invalid_video_id(
        self,
        invalid_video_id: int
    ) -> None:
        """
        Test retrieving locations with an invalid video ID.

        Test:
            - Endpoint returns status code 404 for invalid video ID
            - Response contains error message
        """

        url = f"{BASE_URL}{API_PREFIX}/locations/video/{invalid_video_id}"
        response = requests.get(url)

        assert response.status_code == 404
        assert "error" in response.json()
