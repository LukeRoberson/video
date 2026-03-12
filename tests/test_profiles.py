"""
Module: test_profiles.py

Unit tests for profile-related API endpoints.

Endpoints Tested:
    - /api/profile
    - /api/profile/{id}

Classes:
    TestGetProfiles:
        Tests getting the entire list of profiles
    TestGetProfileById:
        Tests getting a single profile

To Do:
    Add test for other profile realted endpoints
        These are not included at this time,
        as these endpoints will be updated in the near future
"""

import requests


# Configuration
BASE_URL = "http://localhost:5010"
API_PREFIX = "/api"


class TestGetProfiles:
    """
    Tests for the GET /api/profile endpoint.

    Methods:
        test_get_all_profiles
            Test retrieving the list of all profiles.
    """

    def test_get_all_profiles(
        self
    ) -> None:
        """
        Test retrieving the list of all profiles.

        Test:
            - Endpoint returns status code 200
            - Response contains expected fields
        """

        url = f"{BASE_URL}{API_PREFIX}/profile"
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()
        for item in data['data']:
            assert 'id' in item
            assert 'name' in item
            assert 'image' in item
            assert 'admin' in item
            assert 'created_at' in item


class TestGetProfileById:
    """
    Tests for the GET /api/profile/{id} endpoint.

    Methods:
        test_get_profile_by_id
            Test retrieving a profile by its ID.
        test_invalid_profile_id
            Test retrieving a profile with an invalid ID.
    """

    def test_get_profile_by_id(
        self,
        valid_profile_id: int
    ) -> None:
        """
        Test retrieving a profile by its ID.

        Test:
            - Endpoint returns status code 200
            - Response contains expected fields
        """

        # Get the profile by ID
        url = f"{BASE_URL}{API_PREFIX}/profile/{valid_profile_id}"
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()
        assert 'id' in data['data']
        assert 'name' in data['data']
        assert 'image' in data['data']
        assert 'admin' in data['data']
        assert 'created_at' in data['data']

    def test_invalid_profile_id(
        self,
        invalid_profile_id: int
    ) -> None:
        """
        Test retrieving a profile with an invalid ID.

        Test:
            - Endpoint returns status code 404 for non-existent profile
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/{invalid_profile_id}"
        response = requests.get(url)

        assert response.status_code == 404
