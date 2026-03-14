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

        # Validate the response
        data = response.json().get("data", {})
        assert "results" in data
        assert isinstance(data['results'], list)
        assert "query" in data
        assert isinstance(data['query'], str)
        assert "total" in data
        assert isinstance(data['total'], int)
        assert "using_elasticsearch" in data
        assert isinstance(data['using_elasticsearch'], bool)

        # Validate results structure and type
        if len(data['results']) > 0:
            assert all(
                ("highlights" in result) and
                ("speaker" in result) and
                ("tags" in result) and
                (
                    "bible_character" in result and
                    isinstance(result["bible_character"], str)
                ) and
                (
                    "chapter_markers" in result and
                    isinstance(result["chapter_markers"], str)
                ) and
                (
                    "description" in result and
                    isinstance(result["description"], str)
                ) and
                (
                    "duration" in result and
                    isinstance(result["duration"], int)
                ) and
                (
                    "id" in result and
                    isinstance(result["id"], int)
                ) and
                (
                    "location" in result and
                    isinstance(result["location"], str)
                ) and
                (
                    "name" in result and
                    isinstance(result["name"], str)
                ) and
                (
                    "score" in result and
                    isinstance(result["score"], float)
                ) and
                (
                    "scriptures" in result and
                    isinstance(result["scriptures"], str)
                ) and
                (
                    "thumbnail" in result and
                    isinstance(result["thumbnail"], str)
                ) and
                (
                    "title" in result and
                    isinstance(result["title"], str)
                ) and
                (
                    "video_id" in result and
                    isinstance(result["video_id"], int)
                )
                for result in data['results']
            )

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

        # Validate response
        data = response.json().get("data", {})
        assert "results" in data
        assert "page" in data
        assert "pages" in data
        assert "per_page" in data


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

        data = response.json().get("data", {})
        assert "elasticsearch_available" in data
        assert isinstance(data['elasticsearch_available'], bool)
        assert "fallback_active" in data
        assert isinstance(data['fallback_active'], bool)
        assert "index_exists" in data
        assert isinstance(data['index_exists'], bool)
        assert "timestamp" in data
        assert isinstance(data['timestamp'], str)


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

        # Validate response
        data = response.json().get("data", {})
        assert "results" in data
        assert isinstance(data['results'], list)
        assert "query" in data
        assert isinstance(data['query'], str)
        assert "total" in data
        assert isinstance(data['total'], int)
        assert "using_elasticsearch" in data
        assert isinstance(data['using_elasticsearch'], bool)
        assert "filters" in data
        assert isinstance(data['filters'], dict)

        # Validate results structure and type
        if len(data['results']) > 0:
            assert all(
                ("highlights" in result) and
                ("speaker" in result) and
                ("tags" in result) and
                (
                    "bible_character" in result and
                    isinstance(result["bible_character"], str)
                ) and
                (
                    "chapter_markers" in result and
                    isinstance(result["chapter_markers"], str)
                ) and
                (
                    "description" in result and
                    isinstance(result["description"], str)
                ) and
                (
                    "duration" in result and
                    isinstance(result["duration"], int)
                ) and
                (
                    "id" in result and
                    isinstance(result["id"], int)
                ) and
                (
                    "location" in result and
                    isinstance(result["location"], str)
                ) and
                (
                    "name" in result and
                    isinstance(result["name"], str)
                ) and
                (
                    "score" in result and
                    isinstance(result["score"], float)
                ) and
                (
                    "scriptures" in result and
                    isinstance(result["scriptures"], str)
                ) and
                (
                    "thumbnail" in result and
                    isinstance(result["thumbnail"], str)
                ) and
                (
                    "title" in result and
                    isinstance(result["title"], str)
                ) and
                (
                    "video_id" in result and
                    isinstance(result["video_id"], int)
                )
                for result in data['results']
            )

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

        # Validate response
        data = response.json().get("data", {})
        assert "results" in data
        assert isinstance(data['results'], list)
        assert "query" in data
        assert isinstance(data['query'], str)
        assert "total" in data
        assert isinstance(data['total'], int)
        assert "using_elasticsearch" in data
        assert isinstance(data['using_elasticsearch'], bool)
        assert "filters" in data
        assert isinstance(data['filters'], dict)

        # Validate filters
        filters = data['filters']
        assert "speakers" in filters
        assert isinstance(filters['speakers'], list)
        assert "characters" in filters
        assert isinstance(filters['characters'], list)
        assert "locations" in filters
        assert isinstance(filters['locations'], list)
        assert "tags" in filters
        assert isinstance(filters['tags'], list)


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

        # Validate response
        data = response.json().get("data", {})
        assert "failed" in data
        assert isinstance(data['failed'], int)
        assert "total" in data
        assert isinstance(data['total'], int)
        assert "success" in data
        assert isinstance(data['success'], int)
