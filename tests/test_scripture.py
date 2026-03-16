"""
Module: test_scripture.py

Unit tests for scripture-related API endpoints.

Endpoints Tested:
    - GET /api/scriptures
    - GET /api/scriptures/<int:scripture_id>
    - GET /api/scriptures/video/<int:video_id>
    - POST /api/scriptures

Classes:
    TestScriptureList
        Tests for retrieving the list of all scriptures.
    TestGetScripture
        Tests for retrieving scripture details by ID.
    TestAddScriptureText
        Tests for adding text to a scripture.
"""

import requests


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestScriptureList:
    """
    Tests for the GET /api/scriptures endpoint.

    Methods:
        test_get_all_scriptures
            Test retrieving the list of all scriptures.
        test_get_valid_scripture
            Test retrieving a single scripture by ID.
        test_get_invalid_scripture
            Test retrieving a scripture with an invalid ID.
    """

    def test_get_all_scriptures(
        self
    ) -> None:
        """
        Test retrieving the list of all scriptures.

        Test:
            - Endpoint returns status code 200
            - Response is a list
            - Response is structured correctly
            - Each field has the expected type
        """

        url = f"{BASE_URL}{API_PREFIX}/scriptures"
        response = requests.get(url)
        assert response.status_code == 200

        # Verify that the response contains a list of scriptures
        data = response.json().get("data", [])
        assert isinstance(data, list)

        # Verify the structure and types of fields in each scripture
        if len(data) > 0:
            # Verify that each scripture in the list has the expected fields
            assert all(
                (
                    "id" in scripture and
                    isinstance(scripture["id"], int)
                ) and
                (
                    "book" in scripture and
                    isinstance(scripture["book"], str)
                ) and
                (
                    "chapter" in scripture and
                    isinstance(scripture["chapter"], int)
                ) and
                (
                    "verse" in scripture and
                    isinstance(scripture["verse"], int)
                ) and
                (
                    "verse_text" in scripture
                )
                for scripture in data
            )

    def test_get_valid_scripture(
        self,
        valid_scripture_id: int,
    ) -> None:
        """
        Test retrieving a single scripture by ID.

        Test:
            - Endpoint returns status code 200 for valid ID
            - Response contains the correct scripture details
        """

        url = f"{BASE_URL}{API_PREFIX}/scriptures"
        params = {"scr_id": valid_scripture_id}
        response = requests.get(
            url,
            params=params
        )
        assert response.status_code == 200

        # Verify that the response contains a list with one scripture
        data = response.json().get("data", [])
        assert isinstance(data, list)
        assert len(data) == 1

        # Validate the contents of the scripture
        scripture = data[0]
        assert "id" in scripture and scripture["id"] == valid_scripture_id
        assert "book" in scripture and isinstance(scripture["book"], str)
        assert "chapter" in scripture and isinstance(scripture["chapter"], int)
        assert "verse" in scripture and isinstance(scripture["verse"], int)
        assert (
            "verse_text" in scripture and
            isinstance(scripture["verse_text"], str)
        )

    def test_get_invalid_scripture(
        self,
        invalid_scripture_id: int,
    ) -> None:
        """
        Test retrieving a scripture with an invalid ID.

        Test:
            - Endpoint returns status code 200
            - Response contains an empty list
        """

        url = f"{BASE_URL}{API_PREFIX}/scriptures"
        params = {"scr_id": invalid_scripture_id}
        response = requests.get(
            url,
            params=params
        )
        assert response.status_code == 200

        # Verify that the response contains an empty list
        data = response.json().get("data", [])
        assert isinstance(data, list)
        assert len(data) == 0


class TestVideoScriptures:
    """
    Tests for the GET /api/scriptures/video/<int:video_id> endpoint.

    Methods:
        test_get_video_scriptures_by_video_id
            Test retrieving scriptures associated with a video by its ID.
        test_get_video_scriptures_by_invalid_video_id
            Test retrieving scriptures with an invalid video ID.
    """

    def test_get_video_scriptures_by_video_id(
        self,
        valid_video_id: int,
    ) -> None:
        """
        Test retrieving scriptures associated with a video by its ID.

        Test:
            - Endpoint returns status code 200 for valid video ID
            - Response is a list
            - Response is structured correctly
            - Each field has the expected type
        """

        # Test with a valid video ID (assuming 1 is valid)
        valid_url = f"{BASE_URL}{API_PREFIX}/scriptures/video/{valid_video_id}"
        response = requests.get(valid_url)
        assert response.status_code == 200

        # Validate response structure
        data = response.json().get("data", [])
        assert isinstance(data, list)

        # Validate the contents of the response
        if len(data) > 0:
            assert all(
                (
                    "id" in scripture and
                    isinstance(scripture["id"], int)
                ) and
                (
                    "book" in scripture and
                    isinstance(scripture["book"], str)
                ) and
                (
                    "chapter" in scripture and
                    isinstance(scripture["chapter"], int)
                ) and
                (
                    "verse" in scripture and
                    isinstance(scripture["verse"], int)
                ) and
                (
                    "verse_text" in scripture
                )
                for scripture in data
            )

    def test_get_video_scriptures_by_invalid_video_id(
        self,
        invalid_video_id: int,
    ) -> None:
        """
        Test retrieving scriptures with an invalid video ID.

        Test:
            - Endpoint returns status code 404 for invalid video ID
        """

        # Test with an invalid video ID (assuming -1 is invalid)
        invalid_url = (
            f"{BASE_URL}{API_PREFIX}/scriptures/video/{invalid_video_id}"
        )
        invalid_response = requests.get(invalid_url)

        assert invalid_response.status_code == 404


class TestAddScriptureText:
    """
    Tests for the POST /api/scriptures endpoint.

    Methods:
        test_add_scripture_text
            Test adding text to a scripture.
        test_add_scripture_text_with_invalid_scripture_id
            Test adding text to a scripture with an invalid scripture ID.
    """

    def test_add_scripture_text(
        self,
        valid_scripture_name: str,
    ) -> None:
        """
        Test adding text to a scripture.

        Test:
            - Endpoint returns status code 200 for valid input
            - Response contains the updated scripture details
        """

        url = f"{BASE_URL}{API_PREFIX}/scriptures"
        payload = {
            "scr_name": valid_scripture_name,
            "scr_text": "Text used while testing the API.",
        }
        response = requests.post(
            url,
            json=payload
        )

        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_add_scripture_text_with_invalid_scripture_id(
        self,
        invalid_scripture_name: str,
    ) -> None:
        """
        Test adding text to a scripture with an invalid scripture name.

        Test:
            - Endpoint returns status code 400 for invalid scripture name
        """

        url = f"{BASE_URL}{API_PREFIX}/scriptures"
        payload = {
            "scripture_id": invalid_scripture_name,
            "text": "Text used while testing the API.",
        }
        response = requests.post(url, json=payload)

        assert response.status_code == 400
