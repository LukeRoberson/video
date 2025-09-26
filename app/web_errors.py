"""
Module: web_errors.py

Define flask routes web error pages

"""

# Standard library imports
from flask import (
    Blueprint,
    Response,
    render_template,
    make_response,
)
import logging


error_bp = Blueprint(
    'error_pages',
    __name__,
)


@error_bp.errorhandler(403)
def forbidden(
    e: Exception
) -> Response:
    """
    Render a custom 403 Forbidden page.

    Args:
        e (Exception): The exception raised.

    Returns:
        Response: A rendered HTML page for 403 errors.
    """

    from flask import request
    logging.error(f"Forbidden access: {request.url} - {e}")

    return make_response(
        render_template("errors/403.html"),
        403
    )


@error_bp.errorhandler(404)
def not_found(
    e: Exception
) -> Response:
    """
    Render a custom 404 Not Found page.

    Args:
        e (Exception): The exception raised.

    Returns:
        Response: A rendered HTML page for 404 errors.
    """

    from flask import request
    logging.error(f"Page not found: {request.url} - {e}")

    return make_response(
        render_template("errors/404.html"),
        404
    )
