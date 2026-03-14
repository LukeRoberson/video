"""
Module: api_location.py

API endpoints related to locations.

Endpoints:
    GET /api/locations
        Get a list of all locations.
    GET /api/locations/<int:location_id>
        Get a location by its ID.
    GET /api/locations/video/<int:video_id>
        Get the locations for a video by its ID.

Blueprints:
    location_endpoint

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
    api.sql_db.LocationManager:
        A class for managing location records in the database.
    api.sql_db.VideoManager:
        A class for managing video records in the database.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
)

# Local imports
from api.api import (
    api_error,
    api_success,
)
from api.sql_db import (
    DatabaseContext,
    LocationManager,
    VideoManager,
)


# Create a blueprint for location-related endpoints
location_endpoint = Blueprint(
    'location_endpoint',
    __name__,
    url_prefix='/api/locations'
)


@location_endpoint.route(
    "",
    methods=["GET"],
)
def get_locations() -> Response:
    """
    Get a list of all locations.

    Returns:
        Response: A JSON response containing a list of all locations.
    """

    with DatabaseContext() as db:
        loc_mgr = LocationManager(db)

        locations = loc_mgr.get() or []

    # Sort locations alphabetically by name (case-insensitive)
    locations = sorted(
        locations, key=lambda loc: loc.get('name', '').lower()
    )

    return api_success(
        data=locations,
        message="Locations retrieved successfully",
        status=200
    )


@location_endpoint.route(
    "/<int:location_id>",
    methods=["GET"],
)
def get_location(
    location_id: int
) -> Response:
    """
    Get a location by its ID.

    Args:
        location_id (int): The ID of the location to retrieve.

    Returns:
        Response: A JSON response containing the location details if found,
            or an error message if not found.
    """

    with DatabaseContext() as db:
        loc_mgr = LocationManager(db)

        loc_list = loc_mgr.get(id=location_id)
        if not loc_list:
            return api_error(
                f"Location with ID {location_id} not found",
                404
            )

    return api_success(
        data=loc_list[0],
        message="Location retrieved successfully",
        status=200
    )


@location_endpoint.route(
    "/video/<int:video_id>",
    methods=["GET"],
)
def get_video_locations(
    video_id: int
) -> Response:
    """
    Get the locations for a video by its ID.

    Args:
        video_id (int): The ID of the video to retrieve locations for.

    Returns:
        Response: A JSON response containing the list of locations,
            or an error message if the video is not found.
    """

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        location_mgr = LocationManager(db)

        # Check if the video exists
        video_list = video_mgr.get(id=video_id)
        if not video_list:
            return api_error(
                f"Video with ID {video_id} not found",
                404
            )

        # Get the locations for the video
        locations = location_mgr.get_from_video(
            video_id=video_id
        )

        return api_success(
            data=locations,
            message="Locations retrieved successfully",
            status=200
        )
