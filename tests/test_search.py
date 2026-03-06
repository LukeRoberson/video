"""
Module: test_search.py

Unit tests for search-related API endpoints.

Endpoints Tested:
    - GET /api/search
    - GET /api/search/status
    - GET /api/search/advanced
    - GET /api/search/reindex

Classes:
    TestSearch
        Tests for standard search operations.
    TestSearchStatus
        Tests for retrieving search status.
    TestAdvancedSearch
        Tests for advanced search functionality.
    TestSearchReindex
        Tests for triggering search index reindexing.
"""


import requests


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestSearch:
    """
    Tests for the GET /api/search endpoint.

    Methods:
        test_standard_search
            Test performing a standard search query.
    """

    def test_standard_search(
        self,
        search_query: str
    ) -> None:
        """
        Test performing a standard search query.

        Test:
            - Endpoint returns status code 200
            - Response contains expected search results
        """

        url = f"{BASE_URL}{API_PREFIX}/search"
        params = {"q": search_query}
        response = requests.get(url, params=params)

        assert response.status_code == 200
        assert "results" in response.json()

    def test_search_with_pages(
        self,
        search_query: str,
        page_number: int,
        per_page: int
    ) -> None:
        """
        Test performing a search query with pagination.

        Test:
            - Endpoint returns status code 200
            - Response contains expected search results for the specified page
        """

        url = f"{BASE_URL}{API_PREFIX}/search"
        params = {
            "q": search_query,
            "page": page_number,
            "per_page": per_page
        }
        response = requests.get(url, params=params)

        assert response.status_code == 200
        assert "results" in response.json()


class TestSearchStatus:
    """
    Tests for the GET /api/search/status endpoint.

    Methods:
        test_get_search_status
            Test retrieving the current status of the search index.
    """

    def test_get_search_status(self) -> None:
        """
        Test retrieving the current status of the search index.

        Test:
            - Endpoint returns status code 200
            - Response contains expected status information
        """

        url = f"{BASE_URL}{API_PREFIX}/search/status"
        response = requests.get(url)

        assert response.status_code == 200
        assert "elasticsearch_available" in response.json()


class TestAdvancedSearch:
    """
    Tests for the GET /api/search/advanced endpoint.

    Methods:
        test_advanced_search
            Test performing an advanced search query.
    """

    def test_advanced_search(
        self,
        search_query: str
    ) -> None:
        """
        Test performing an advanced search query.

        Test:
            - Endpoint returns status code 200
            - Response contains expected search results
        """

        url = f"{BASE_URL}{API_PREFIX}/search/advanced"
        params = {
            "query": search_query
        }
        response = requests.get(url, params=params)

        assert response.status_code == 200
        assert "results" in response.json()

    def test_advanced_search_with_filters(
        self,
        search_query: str,
        valid_speaker_name: str,
        valid_character_name: str,
        valid_location_name: str,
        valid_tag_name: str
    ) -> None:
        """
        Test performing an advanced search query with filters.

        Test:
            - Endpoint returns status code 200
            - Response contains expected search results based on filters
        """

        url = f"{BASE_URL}{API_PREFIX}/search/advanced"
        params = {
            "query": search_query,
            "speakers": valid_speaker_name,
            "characters": valid_character_name,
            "locations": valid_location_name,
            "tags": valid_tag_name
        }
        response = requests.get(url, params=params)

        assert response.status_code == 200
        assert "results" in response.json()


class TestSearchReindex:
    """
    Tests for the GET /api/search/reindex endpoint.

    Methods:
        test_trigger_reindex
            Test triggering a search index reindexing.
    """

    def test_trigger_reindex(self) -> None:
        """
        Test triggering a search index reindexing.

        Test:
            - Endpoint returns status code 200
            - Response indicates that reindexing has been triggered
        """

        url = f"{BASE_URL}{API_PREFIX}/search/reindex"
        response = requests.post(url)

        assert response.status_code == 200
        assert "message" in response.json()
