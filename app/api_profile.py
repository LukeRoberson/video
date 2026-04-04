"""
Module: profile_api.py

API endpoints that the browser will use to fetch additional information
    Specifically, for user profiles and their management.

Routes:
    - /profile/pictures
        - get_profile_pictures: Retrieves available profile pictures.
    - /profile/set_active
        - set_active_profile: Sets the active profile for the session.
    - /profile/get_active
        - get_active_profile: Retrieves the active profile for the session.

Dependencies:
    - Flask: For creating the API endpoints.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
    session,
    request,
    current_app,
    jsonify,
    make_response,
)
import os
import requests


profile_api_bp = Blueprint(
    'profile_api',
    __name__,
)


def api_error(
    error,
    status=400
) -> Response:
    """
    Helper to return a standardized error response.

    Args:
        error (str): Error message to include in the response.
        status (int, optional): HTTP status code for the response.

    Returns:
        Response: A JSON response with an error status.
    """

    resp = {"success": False, "error": error}

    return make_response(jsonify(resp), status)


@profile_api_bp.route(
    '/profile/pictures'
)
def get_profile_pictures():
    """Get list of available profile pictures"""
    try:
        # Get list of profile picture files from your static directory
        static_folder = current_app.static_folder
        if not static_folder:
            return jsonify({'error': 'Static folder not configured'}), 500

        profile_pics_dir = os.path.join(static_folder, 'img', 'profiles')
        profile_pics = []

        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.lower().endswith((
                    '.png', '.jpg', '.jpeg', '.gif', '.webp'
                )):
                    profile_pics.append(filename)

        return jsonify({'profile_pics': sorted(profile_pics)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_api_bp.route(
    "/profile/set_active",
    methods=["POST"]
)
def set_active_profile() -> Response:
    """
    Set the active profile for the session.

    Expects JSON:
        {
            "profile_id": <int or "guest">
        }

    Returns:
        Response: A redirect to the home page after setting the active profile.
    """

    # Get the JSON data from the request
    data = request.get_json()
    if not data:
        return api_error("No data provided", 400)

    if "profile_id" not in data:
        return api_error("Missing 'profile_id' in request data", 400)

    # Set the active profile
    profile_id = data.get("profile_id", "guest")
    session["active_profile"] = profile_id

    # Set admin status
    profile_admin = data.get("profile_admin", None)
    session["profile_admin"] = True if profile_admin == '1' else False

    # Return a JSON response indicating success
    return jsonify(
        {
            "success": True,
            "active_profile": profile_id,
            "profile_admin": profile_admin
        }
    )


@profile_api_bp.route(
    "/profile/get_active",
    methods=["GET"]
)
def get_active_profile() -> Response:
    """
    Get the active profile for the session.

    Returns:
        Response: A JSON response with the active profile ID.
    """

    base_url = current_app.config['API_BASE_URL']

    # Retrieve the active profile from the session
    active_profile = session.get("active_profile", None)

    # If no active profile is set, return a default value
    if active_profile is None or active_profile == "guest":
        profile = {
            "id": None,
            "name": "Guest",
            "image": "guest.png"
        }

    # Get profile details from the API
    else:
        try:
            response = requests.get(
                f"{base_url}/api/profile/{active_profile}"
            )
            if response.status_code == 200:
                profile = response.json().get("data", {})
            else:
                profile = {
                    "id": None,
                    "name": "Guest",
                    "image": "guest.png"
                }
        except Exception:
            profile = {
                "id": None,
                "name": "Guest",
                "image": "guest.png"
            }

    if profile.get("id") is None:
        profile["id"] = "guest"
        profile["admin"] = False

    # Return a JSON response with the active profile ID
    return jsonify(
        {
            "success": True,
            "data": {
                "active_profile": profile
            }
        }
    )
