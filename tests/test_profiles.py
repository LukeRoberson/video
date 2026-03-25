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


class TestInProgressVideos:
    """
    Tests for the /api/profile/in_progress endpoint.

    Methods:
        test_get_in_progress_videos
            Test retrieving in_progress videos for a profile.
    """

    def test_get_in_progress_videos(
        self,
        valid_profile_id: int
    ) -> None:
        """
        Test retrieving in-progress videos for a profile.

        Test:
            - Endpoint returns status code 200
            - Response contains expected fields
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/in_progress"
        parameters = {
            "profile": valid_profile_id
        }
        response = requests.get(
            url,
            params=parameters
        )
        assert response.status_code == 200

        # Validate response structure
        data = response.json().get("data", [])
        assert isinstance(data, list)

        # Validate fields in each video item
        assert all(
            (
                "video_id" in video and
                isinstance(video["video_id"], int)
            ) and
            (
                "profile_id" in video and
                isinstance(video["profile_id"], int)
            ) and
            (
                "current_time" in video and
                isinstance(video["current_time"], int)
            ) and
            (
                "updated_at" in video and
                isinstance(video["updated_at"], str)
            )
            for video in data
        )

    def test_get_in_progress_videos_invalid_profile(
        self,
        invalid_profile_id: int
    ) -> None:
        """
        Test retrieving in-progress videos for an invalid profile.

        Test:
            - Endpoint returns status code 404 for invalid profile ID
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/in_progress"
        parameters = {
            "profile": invalid_profile_id
        }
        response = requests.get(
            url,
            params=parameters
        )

        assert response.status_code == 404

    def test_get_in_progress_videos_no_profile(
        self
    ) -> None:
        """
        Test retrieving in-progress videos without providing a profile ID.

        Test:
            - Endpoint returns status code 400 for missing profile parameter
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/in_progress"
        response = requests.get(url)

        assert response.status_code == 400

    def test_add_in_progress_video(
        self,
        valid_profile_id: int,
        valid_video_id: int
    ) -> None:
        """
        Test adding an in-progress video for a profile.

        Test:
            - Endpoint returns status code 201 for successful addition
            - Response contains expected message
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/in_progress"
        parameters = {
            "profile": valid_profile_id
        }
        payload = {
            "video_id": valid_video_id,
            "current_time": 120  # Example current time in seconds
        }
        response = requests.post(
            url,
            params=parameters,
            json=payload
        )
        assert response.status_code == 201

        # Validate response message
        data = response.json()
        assert 'message' in data
        assert 'success' in data
        assert data['success'] is True

    def test_add_in_progress_video_missing_fields(
        self,
        valid_profile_id: int
    ) -> None:
        """
        Test adding an in-progress video with missing fields.

        Test:
            - Endpoint returns status code 400 for missing required fields
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/in_progress"
        parameters = {
            "profile": valid_profile_id
        }
        payload = {
            # Missing 'video_id' and 'current_time'
        }
        response = requests.post(
            url,
            params=parameters,
            json=payload
        )
        assert response.status_code == 400

    def test_add_in_progress_video_invalid_data_types(
        self,
        valid_profile_id: int
    ) -> None:
        """
        Test adding an in-progress video with invalid data types.

        Test:
            - Endpoint returns status code 400 for invalid data types
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/in_progress"
        parameters = {
            "profile": valid_profile_id
        }
        payload = {
            "video_id": "invalid_video_id",  # Should be an integer
            "current_time": "invalid_current_time"  # Should be an integer
        }
        response = requests.post(
            url,
            params=parameters,
            json=payload
        )
        assert response.status_code == 400


class TestWatchHistory:
    """
    Tests for the /api/profile/watch_history endpoint.

    Methods:
        test_get_watch_history
            Test retrieving watch history for a profile.
        test_get_watch_history_no_profile
            Test retrieving watch history without providing a profile ID.
        test_get_watch_history_invalid_profile
            Test retrieving watch history with an invalid profile ID.
    """

    def test_get_watch_history(
        self,
        valid_profile_id: int
    ) -> None:
        """
        Test retrieving watch history for a profile.

        Test:
            - Endpoint returns status code 200
            - Response contains expected fields
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/watch_history"
        parameters = {
            "profile": valid_profile_id
        }
        response = requests.get(
            url,
            params=parameters
        )
        assert response.status_code == 200

        # Validate response structure
        data = response.json().get("data", [])
        assert isinstance(data, list)

        # Validate fields in each watch history item
        if len(data) > 0:
            for index, item in enumerate(data):
                assert "video_id" in item, (
                    f"Missing 'video_id' in item at index {index}"
                )
                assert isinstance(item["video_id"], int), (
                    f"video_id[{index}] is not an integer: "
                    f"{item.get('video_id')!r}; full item: {item!r}"
                )

                assert "profile_id" in item, (
                    f"Missing 'profile_id' in item at index {index}"
                )
                assert isinstance(item["profile_id"], int), (
                    f"profile_id[{index}] is not an integer: "
                    f"{item.get('profile_id')!r}; full item: {item!r}"
                )

                assert "watched_at" in item, (
                    f"Missing 'watched_at' in item at index {index}"
                )
                assert isinstance(item["watched_at"], str), (
                    f"watched_at[{index}] is not a string: "
                    f"{item.get('watched_at')!r}; full item: {item!r}"
                )

                assert "current_time" in item, (
                    f"Missing 'current_time' in item at index {index}"
                )
                assert isinstance(item["current_time"], int), (
                    f"current_time[{index}] is not an integer: "
                    f"{item.get('current_time')!r}; full item: {item!r}"
                )

    def test_get_watch_history_no_profile(
        self
    ) -> None:
        """
        Test retrieving watch history without providing a profile ID.
        This means we're using a guest profile, which is valid.

        Test:
            - Endpoint returns status code 200 when no profile ID is provided
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/watch_history"
        response = requests.get(url)
        assert response.status_code == 200
        data = response.json()

        # Should still report a success response
        assert 'success' in data
        assert data['success'] is True

        # Should reference the guest profile in the message
        assert 'message' in data
        assert "guest profile" in data['message']

    def test_get_watch_history_invalid_profile(
        self,
        invalid_profile_id: int
    ) -> None:
        """
        Test retrieving watch history with an invalid profile ID.

        Test:
            - Endpoint returns status code 404 for invalid profile ID
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/watch_history"
        parameters = {
            "profile": invalid_profile_id
        }
        response = requests.get(
            url,
            params=parameters
        )
        assert response.status_code == 404, (
            f"Expected status code 404 for invalid profile ID, "
            f"but got {response.status_code}. "
            f"Response content: {response.text}"
        )


class TestWatchStatus:
    """
    Tests for the /api/profile/mark_watched endpoint.

    Methods:
        test_get_watch_status
            Test retrieving watch status for a profile and video.
    """

    def test_get_watch_status(
        self,
        valid_profile_id: int,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving watch status for a profile and video.

        Test:
            - Endpoint returns status code 200
            - Response contains expected fields
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/mark_watched"
        parameters = {
            "profile": valid_profile_id,
            "video_id": valid_video_id
        }
        response = requests.get(
            url,
            params=parameters
        )
        assert response.status_code == 200, (
            f"Expected status code 200, but got {response.status_code}. "
            f"Response content: {response.text}"
        )

        # Validate response structure
        data = response.json().get("data", {})
        assert isinstance(data, dict), (
            f"Expected 'data' to be dict, got {type(data)}"
        )

        # Validate expected fields in the response
        assert "video_id" in data, "Missing 'video_id' in response data"
        assert isinstance(data["video_id"], int), (
            f"Expected 'video_id' to be int, got {type(data['video_id'])}"
        )

        assert "watched" in data, "Missing 'watched' in response data"
        assert isinstance(data["watched"], bool), (
            f"Expected 'watched' to be bool, got {type(data['watched'])}"
        )

    def test_get_watch_status_no_profile(
        self,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving watch status without providing a profile ID.

        Test:
            - Endpoint returns status code 200 for missing profile parameter
                (Guest profile is valid and should return a response)
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/mark_watched"
        parameters = {
            "video_id": valid_video_id
        }
        response = requests.get(
            url,
            params=parameters
        )
        assert response.status_code == 200, (
            f"Expected status code 200 for missing profile parameter, "
            f"but got {response.status_code}. "
            f"Response content: {response.text}"
        )

    def test_get_watch_status_invalid_profile(
        self,
        invalid_profile_id: int,
        valid_video_id: int
    ) -> None:
        """
        Test retrieving watch status with an invalid profile ID.

        Test:
            - Endpoint returns status code 404 for invalid profile ID
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/mark_watched"
        parameters = {
            "profile": invalid_profile_id,
            "video_id": valid_video_id
        }
        response = requests.get(
            url,
            params=parameters
        )
        assert response.status_code == 404, (
            f"Expected status code 404 for invalid profile ID, "
            f"but got {response.status_code}. "
            f"Response content: {response.text}"
        )

    def test_get_watch_status_invalid_video(
        self,
        valid_profile_id: int,
        invalid_video_id: int
    ) -> None:
        """
        Test retrieving watch status with an invalid video ID.

        Test:
            - Endpoint returns status code 404 for invalid video ID
        """

        url = f"{BASE_URL}{API_PREFIX}/profile/mark_watched"
        parameters = {
            "profile": valid_profile_id,
            "video_id": invalid_video_id
        }
        response = requests.get(
            url,
            params=parameters
        )
        assert response.status_code == 404, (
            f"Expected status code 404 for invalid video ID, "
            f"but got {response.status_code}. "
            f"Response content: {response.text}"
        )
