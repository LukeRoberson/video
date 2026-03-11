"""
Module: test_performance.py

Test the performance of key API endpoints
    to ensure they respond within acceptable time limits.

Classes:
    TestPerformance
        Consolidated performance tests for all API endpoints.

To do:
    - Test performance for adding a scripture (POST /api/scriptures)
    - Test performance for search reindexing (POST /api/search/reindex)
    - Test /api/videos/get_bulk (uses POST)
    - Test /api/videos/filter (uses GET with params)
    - Test /api/videos/metadata (uses GET with params)
"""


import requests
import pytest


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestPerformance:
    """
    Consolidated performance tests for all API endpoints.

    Uses parametrization to test multiple endpoints with the same logic.
    """

    # Define endpoint patterns:
    #   (endpoint_template, fixture_name, max_time_seconds, description)
    ENDPOINTS_NO_PARAMS = [
        (
            "/characters",
            3.0,
            "Retrieve all characters"
        ),
        (
            "/speakers",
            3.0,
            "Retrieve all speakers"
        ),
        (
            "/tags",
            3.0,
            "Retrieve all tags"
        ),
        (
            "/scriptures",
            3.0,
            "Retrieve all scriptures"
        ),
        (
            "/search/status",
            3.0,
            "Check search index status"
        ),
        (
            "/search?q=bible",
            3.0,
            "Search for 'bible'"
        ),
        (
            "/search/advanced?"
            "query=generosity&"
            "speakers=Stephen Lett&"
            "characters=David&"
            "locations=Samaria&"
            "tags=prayer",
            3.0,
            "Advanced search with multiple parameters"
        ),
    ]

    ENDPOINTS_SINGLE_ID = [
        (
            "/characters/{id}",
            "valid_character_id",
            2.1,
            "Character lookup"
        ),
        (
            "/speakers/{id}",
            "valid_speaker_id",
            2.1,
            "Speaker lookup"
        ),
        (
            "/tags/{id}",
            "valid_tag_id",
            2.1,
            "Tag lookup"
        ),
        (
            "/characters/video/{id}",
            "valid_video_id",
            3.0,
            "Retrieve characters for video"
        ),
        (
            "/speakers/video/{id}",
            "valid_video_id",
            3.0,
            "Retrieve speakers for video"
        ),
        (
            "/tags/video/{id}",
            "valid_video_id",
            3.0,
            "Retrieve tags for video"
        ),
        (
            "/similarity/{id}",
            "valid_video_id",
            3.0,
            "Similarity lookup"
        ),
        (
            "/scriptures/video/{id}",
            "valid_video_id",
            3.0,
            "Retrieve scriptures for video"
        ),
        (
            "/scriptures/{id}",
            "valid_scripture_id",
            3.0,
            "Scripture lookup by ID"
        ),
        (
            "/locations/{id}",
            "valid_location_id",
            3.0,
            "Location lookup by ID"
        ),
        (
            "/locations/video/{id}",
            "valid_video_id",
            3.0,
            "Retrieve locations for video"
        ),
        (
            "/videos/{id}",
            "valid_video_id",
            3.0,
            "Video lookup by ID"
        ),
    ]

    ENDPOINTS_SINGLE_NAME = [
        (
            "/categories/{name}",
            "valid_category_name",
            3.0,
            "Category name lookup"
        ),
    ]

    ENDPOINTS_DUAL_ID = [
        (
            "/categories/{id1}/{id2}",
            "valid_category_id",
            "valid_subcategory_id",
            5.0,
            "Video retrieval by category"
        ),
    ]

    @pytest.mark.parametrize(
        "endpoint,max_time,description",
        ENDPOINTS_NO_PARAMS
    )
    def test_response_time_no_params(
        self,
        endpoint: str,
        max_time: float,
        description: str
    ) -> None:
        """
        Test response time for endpoints without parameters.

        Arguments:
            endpoint: The API endpoint path.
            max_time: Maximum acceptable response time in seconds.
            description: Description of what the test does.
        """
        url = f"{BASE_URL}{API_PREFIX}{endpoint}"
        response = requests.get(url)

        assert response.status_code == 200, \
            f"Request failed with status {response.status_code}"
        assert response.elapsed.total_seconds() < max_time, \
            (
                f"{description}: Expected response < {max_time}s, got "
                f"{response.elapsed.total_seconds()}s"
            )

    @pytest.mark.parametrize(
        "endpoint_template,fixture_name,max_time,description",
        ENDPOINTS_SINGLE_ID
    )
    def test_response_time_single_id(
        self,
        endpoint_template: str,
        fixture_name: str,
        max_time: float,
        description: str,
        request: pytest.FixtureRequest
    ) -> None:
        """
        Test response time for endpoints with a single ID parameter.

        Arguments:
            endpoint_template: URL template with {id} placeholder.
            fixture_name: Name of fixture providing the ID.
            max_time: Maximum acceptable response time in seconds.
            description: Description of what the test does.
            request: pytest request object to access fixtures.
        """

        fixture_value = request.getfixturevalue(fixture_name)
        url = f"{BASE_URL}{API_PREFIX}{endpoint_template}".format(
            id=fixture_value
        )
        response = requests.get(url)

        assert response.status_code == 200, \
            f"Request failed with status {response.status_code}"

        assert response.elapsed.total_seconds() < max_time, \
            (
                f"{description}: Expected response < {max_time}s, got "
                f"{response.elapsed.total_seconds()}s"
            )

    @pytest.mark.parametrize(
        "endpoint_template,fixture_name,max_time,description",
        ENDPOINTS_SINGLE_NAME
    )
    def test_response_time_single_name(
        self,
        endpoint_template: str,
        fixture_name: str,
        max_time: float,
        description: str,
        request: pytest.FixtureRequest
    ) -> None:
        """
        Test response time for endpoints with a single name parameter.

        Arguments:
            endpoint_template: URL template with {name} placeholder.
            fixture_name: Name of fixture providing the name.
            max_time: Maximum acceptable response time in seconds.
            description: Description of what the test does.
            request: pytest request object to access fixtures.
        """
        fixture_value = request.getfixturevalue(fixture_name)
        url = f"{BASE_URL}{API_PREFIX}{endpoint_template}".format(
            name=fixture_value
        )
        response = requests.get(url)

        assert response.status_code == 200, \
            f"Request failed with status {response.status_code}"
        assert response.elapsed.total_seconds() < max_time, \
            (
                f"{description}: Expected response < {max_time}s, got "
                f"{response.elapsed.total_seconds()}s"
            )

    @pytest.mark.parametrize(
        "endpoint_template,fixture1,fixture2,max_time,description",
        ENDPOINTS_DUAL_ID
    )
    def test_response_time_dual_id(
        self,
        endpoint_template: str,
        fixture1: str,
        fixture2: str,
        max_time: float,
        description: str,
        request: pytest.FixtureRequest
    ) -> None:
        """
        Test response time for endpoints with two ID parameters.

        Arguments:
            endpoint_template: URL template with {id1} and {id2} placeholders.
            fixture1: Name of fixture for first ID.
            fixture2: Name of fixture for second ID.
            max_time: Maximum acceptable response time in seconds.
            description: Description of what the test does.
            request: pytest request object to access fixtures.
        """
        value1 = request.getfixturevalue(fixture1)
        value2 = request.getfixturevalue(fixture2)
        url = f"{BASE_URL}{API_PREFIX}{endpoint_template}".format(
            id1=value1,
            id2=value2
        )
        response = requests.get(url)

        assert response.status_code == 200, \
            f"Request failed with status {response.status_code}"
        assert response.elapsed.total_seconds() < max_time, \
            (
                f"{description}: Expected response < {max_time}s, got "
                f"{response.elapsed.total_seconds()}s"
            )
