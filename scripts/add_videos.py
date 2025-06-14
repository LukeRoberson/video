import sys
import os
import csv
from colorama import Style, Fore

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

from sql_db import (  # noqa: E402
    DatabaseContext,
    VideoManager,
    CategoryManager,
)


VIDEO_CSV = 'video_details.csv'


def duration_to_seconds(
    duration: str
) -> int:
    """
    Convert a duration string (HH:MM:SS or MM:SS) into seconds.

    Args:
        duration (str): The duration string.

    Returns:
        int: The duration in seconds.
    """

    parts = duration.split(":")
    if len(parts) == 3:  # Format: HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:  # Format: MM:SS
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid duration format: {duration}")


# Generate video data from CSV
video_list = []
with open(VIDEO_CSV, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    video_list = [row for row in reader]

# Add videos to the database
for video in video_list:
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        cat_mgr = CategoryManager(db)

        # Create the video
        video_id = video_mgr.add(
            name=video['name'],
            url_1080=video['url_1080'],
            url_720=video['url_720'],
            url_480=video['url_480'],
            url_360=video['url_360'],
            url_240=video['url_240'],
            description=video['description'],
            thumbnail=video['thumbnail'],
            duration=duration_to_seconds(video['duration']),
        )

        # Check that the video was added successfully
        if video_id is None:
            print(
                Fore.RED,
                f"Video {video['name']} could not be added",
                Style.RESET_ALL
            )
            continue

        # Add the category to the database (it may already exist)
        category_id = cat_mgr.add(name=video['category_name'])

        # Check that the category was added successfully
        if category_id is None:
            print(
                Fore.RED,
                f"Category {video['category_name']} "
                f"does not exist and could not be added",
                Style.RESET_ALL
            )
            continue

        # Associate the video with the category
        result = cat_mgr.add_to_video(
            video_id=video_id,
            category_id=category_id,
        )

        if result is False:
            print(
                Fore.RED,
                f"Video {video['name']} could not be associated "
                f"with category {video['category_name']}",
                Style.RESET_ALL
            )
            continue

        else:
            print(
                Fore.GREEN,
                f"Video {video['name']} added successfully "
                f"with category {video['category_name']}",
                Style.RESET_ALL
            )
