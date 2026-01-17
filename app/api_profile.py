"""
Module: profile_api.py

API endpoints that the browser will use to fetch additional information
    Specifically, for user profiles and their management.

Routes:
    - /api/profile/pictures
        - get_profile_pictures: Retrieves available profile pictures.

Dependencies:
    - Flask: For creating the API endpoints.
"""


# Standard library imports
from flask import (
    Blueprint,
    current_app,
    jsonify,
)
import os


profile_api_bp = Blueprint(
    'profile_api',
    __name__,
)


@profile_api_bp.route(
    '/api/profile/pictures'
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
