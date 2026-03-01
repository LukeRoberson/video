"""
Module: api_similarity.py

API endpoints related to video similarity.

Endpoints:
    GET /api/similarity/<int:video_id>
        Get a list of similar videos for a given video ID.

Blueprints:
    similarity_endpoint

Dependancies:
    flask
        Creating the API endpoints.
        Handling HTTP requests and responses.
    logging
        Logging errors and information for debugging and monitoring.

Custom Modules:
    api.api.api_error
        Utility function for returning API error responses.

    api.sql_db.DatabaseContext:
        A context manager for database connections.
    api.sql_db.SimilarityManager:
        A class for managing video similarity records in the database.
    api.sql_db.VideoManager:
        A class for managing video records in the database.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
    make_response,
    jsonify,
)

# Local imports
from api.api import (
    api_error,
)
from api.sql_db import (
    DatabaseContext,
    SimilarityManager,
    VideoManager,
)


# Create a blueprint for similarity-related endpoints
similarity_endpoint = Blueprint(
    'similarity_endpoint',
    __name__,
    url_prefix="/api/similarity"
)


@similarity_endpoint.route(
    "/<int:video_id>",
    methods=["GET"],
)
def get_similar_videos(
    video_id: int
) -> Response:
    """
    Get a list of similar videos for a given video ID.

    Args:
        video_id (int): The ID of the video to find similar videos for.

    Returns:
        Response: A JSON response containing a list of similar videos,
            or an error message if the video is not found.
    """

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        similarity_mgr = SimilarityManager(db)

        # Check if the video exists
        video_list = video_mgr.get(id=video_id)
        if not video_list:
            return api_error(
                f"Video with ID {video_id} not found",
                404
            )

        # Get similar videos for the video
        similar_videos = similarity_mgr.get(
            video1_id=video_id,
        )

        return make_response(
            jsonify(
                similar_videos,
            ),
            200
        )
