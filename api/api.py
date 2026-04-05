"""
Module: api.py

Helper functions and shared resources for the API.

Functions:
    - api_success: Returns a standardized success response.
    - api_error: Returns a standardized error response.
    - seconds_to_hhmmss: Converts seconds to HH:MM:SS format.

Routes:
    - /health: A simple health check endpoint.

Dependencies:
    - Flask: For creating the API endpoints.
"""


# Standard library imports
from flask import (
    Response,
    Blueprint,
    jsonify,
    make_response,
)


def api_success(
    data=None,
    message=None,
    status=200
) -> Response:
    """
    Helper to return a standardized success response.

    Note: It's best to use this for simple success responses only.
        Custom responses should be used in more complex cases.

    Args:
        data (dict, optional): Data to include in the response.
        message (str, optional): Message to include in the response.
        status (int, optional): HTTP status code for the response.

    Returns:
        Response: A JSON response with a success status.
    """

    resp = {"success": True}

    if message:
        resp["message"] = message

    if data is not None:
        resp["data"] = data

    return make_response(jsonify(resp), status)


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


def seconds_to_hhmmss(
    seconds: int,
) -> str:
    """
    Convert seconds to HH:MM:SS format.
        Shows hours only if greater than zero.

    Args:
        seconds (int): Duration in seconds.

    Returns:
        str: Duration in HH:MM:SS or MM:SS format.
    """

    # Handle None or non-positive values
    if seconds is None or seconds <= 0:
        seconds = 1

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    # Format the output based on whether hours are present
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    return f"{minutes}:{seconds:02}"


health_endpoint = Blueprint(
    "health",
    __name__
)


@health_endpoint.route(
    "/api/health",
    methods=["GET"]
)
def health_check() -> Response:
    """
    Health check endpoint to verify the API is running.

    Returns:
        Response: A JSON response indicating the API is healthy.
    """

    return api_success(
        message="API is healthy",
        status=200
    )
