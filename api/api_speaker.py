"""
Module: api_speaker.py

API endpoints related to speakers.

Endpoints:
    GET /api/speakers
        Get a list of all speakers.
    GET /api/speakers/<int:speaker_id>
        Get a speaker by its ID.
    GET /api/speakers/video/<int:video_id>
        Get the speakers for a video by its ID.

Blueprints:
    speaker_endpoint

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
    api.sql_db.SpeakerManager:
        A class for managing speaker records in the database.
    api.sql_db.VideoManager:
        A class for managing video records in the database.
"""


# Standard library imports
from flask import (
    Blueprint,
    Response,
)
import logging

# Local imports
from api.api import (
    api_error,
    api_success,
)
from api.sql_db import (
    DatabaseContext,
    SpeakerManager,
    VideoManager,
)


logger = logging.getLogger(__name__)

# Create a blueprint for speaker-related endpoints
speaker_endpoint = Blueprint(
    'speaker_endpoint',
    __name__,
    url_prefix="/api/speakers"
)


@speaker_endpoint.route(
    "",
    methods=["GET"],
)
def get_speakers() -> Response:
    """
    Get a list of all speakers.

    Returns:
        Response: A JSON response containing a list of all speakers.
    """

    with DatabaseContext() as db:
        speaker_mgr = SpeakerManager(db)
        video_mgr = VideoManager(db)

        # Get a list of all speakers
        speakers = speaker_mgr.get() or []

        if not speakers:
            logger.debug("Module api_speaker: Function get_speakers")
            logger.error("Error occurred while getting speakers.")

            return api_error(
                error="Error occurred while getting speakers.",
                status=500
            )

        if speakers == []:
            logger.debug("Module api_speaker: Function get_speakers")
            logger.info("No speakers found in the database.")

        else:
            # Get the video count for each speaker
            for speaker in speakers:
                videos = video_mgr.get_filter(
                    speaker_id=speaker['id']
                )

                if not videos:
                    videos = []
                    logger.info(
                        f"No videos found for speaker ID {speaker['id']}"
                    )

                speaker['video_count'] = len(videos)

                # Sort speakers alphabetically by name (case-insensitive)
                speakers = sorted(
                    speakers, key=lambda spk: spk.get('name', '').lower()
                )

    return api_success(
        data=speakers,
        message="Speakers retrieved successfully",
        status=200
    )


@speaker_endpoint.route(
    "/<int:speaker_id>",
    methods=["GET"],
)
def get_speaker(
    speaker_id: int
) -> Response:
    """
    Get a speaker by its ID.

    Args:
        speaker_id (int): The ID of the speaker to retrieve.

    Returns:
        Response: A JSON response containing the speaker details if found,
            or an error message if not found.
    """

    with DatabaseContext() as db:
        speaker_mgr = SpeakerManager(db)
        speaker_list = speaker_mgr.get(id=speaker_id)

        # Will be None if there is no speaker with the given ID
        if not speaker_list:
            logger.debug("Module api_speaker: Function get_speaker")
            logger.info(f"Speaker with ID {speaker_id} not found")

            return api_error(
                error=f"Speaker with ID {speaker_id} not found",
                status=404
            )

    return api_success(
        data=speaker_list[0],
        message="Speaker retrieved successfully",
        status=200
    )


@speaker_endpoint.route(
    "/video/<int:video_id>",
    methods=["GET"],
)
def get_video_speakers(
    video_id: int
) -> Response:
    """
    Get the speakers for a video by its ID.

    Args:
        video_id (int): The ID of the video to retrieve speakers for.

    Returns:
        Response: A JSON response containing the list of speakers,
            or an error message if the video is not found.
    """

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        speaker_mgr = SpeakerManager(db)

        # Check if the video exists
        #   (will be None if there is no video with the given ID)
        video_list = video_mgr.get(id=video_id)
        if not video_list:
            logger.debug("Module api_speaker: Function get_video_speakers")
            logger.info(f"Video with ID {video_id} not found")

            return api_error(
                error=f"Video with ID {video_id} not found",
                status=404
            )

    # Get the speakers for the video
    speakers = speaker_mgr.get_from_video(
        video_id=video_id
    )

    # Log this, but it may not be an error
    if speakers is None:
        logger.debug("Module api_speaker: Function get_video_speakers")
        logger.info(f"No speakers found for video ID {video_id}")

    return api_success(
        data=speakers,
        message="Speakers for video retrieved successfully",
        status=200
    )
