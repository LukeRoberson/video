"""
Module: test_errors.py

Unit tests for error handling and edge cases in API endpoints.

Classes:
    TestInvalidMethods
        Tests for invalid HTTP methods on various endpoints.

To Do:
    - Test the /api/categories/<main_category>/<sub_category> endpoint
    - Test the /api/scriptures POST endpoint with invalid data
    - Test the /api/scriptures for invalid methods (POST and GET are fine)
    - Test the /api/search/reindex endpoint with invalid methods (POST is fine)
"""

import requests
import pytest

# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestInvalidMethods:
    """
    Tests for invalid HTTP methods on various endpoints.

    GET_ONLY endpoints are those that should only allow GET requests.
    """

    # Endpoints that should only allow GET
    GET_ONLY_ENDPOINTS_ID = [
        ("/speakers/{id}", "valid_speaker_id"),
        ("/speakers/video/{id}", "valid_video_id"),
        ("/characters/{id}", "valid_character_id"),
        ("/similarity/{id}", "valid_video_id"),
        ("/categories/{id}", "valid_category_id"),
        ("/tags/{id}", "valid_tag_id"),
        ("/tags/video/{id}", "valid_video_id"),
        ("/scriptures/{id}", "valid_scripture_id"),
        ("/scriptures/video/{id}", "valid_video_id"),
        ("/locations/{id}", "valid_location_id"),
        ("/locations/video/{id}", "valid_video_id"),
    ]
    GET_ONLY_ENDPOINTS = [
        "/speakers",
        "/characters",
        "/tags",
        "/locations",
        "/search",
        "/search/status",
        "/search/advanced",
    ]

    @pytest.mark.parametrize(
        "endpoint_template, fixture_name",
        GET_ONLY_ENDPOINTS_ID
    )
    def test_get_only_method(
        self,
        endpoint_template: str,
        fixture_name: str,
        request: pytest.FixtureRequest
    ) -> None:
        """
        Test that GET method is the only allowed method on certain endpoints.

        Arguments:
            endpoint_template:
                The endpoint URL template with a placeholder for parameter.
            fixture_name:
                The name of the fixture to provide the parameter value.
        """

        fixture_value = request.getfixturevalue(fixture_name)
        url = (
            f"{BASE_URL}{API_PREFIX}{endpoint_template}".format(
                id=fixture_value
            )
        )

        response = requests.post(url)
        assert response.status_code in [405, 501]

        response = requests.put(url)
        assert response.status_code in [405, 501]

        response = requests.delete(url)
        assert response.status_code in [405, 501]

    @pytest.mark.parametrize(
        "endpoint",
        GET_ONLY_ENDPOINTS
    )
    def test_get_only_method_simple(
        self,
        endpoint: str
    ) -> None:
        """
        Test that GET method is the only allowed method on certain endpoints.

        Arguments:
            endpoint: The endpoint URL path.
        """

        url = f"{BASE_URL}{API_PREFIX}{endpoint}"

        response = requests.post(url)
        assert response.status_code in [405, 501]

        response = requests.put(url)
        assert response.status_code in [405, 501]

        response = requests.delete(url)
        assert response.status_code in [405, 501]
