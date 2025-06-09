import sys
import os
import csv

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

# Now you can import modules from the parent folder
from sql_db import DatabaseManager


VIDEO_CSV = 'scripts/video_list.csv'


def duration_to_seconds(duration: str) -> int:
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


# Create Video table
with DatabaseManager() as db:
    print("Creating video table")
    result = db.create_video_table()
    print(f"Result: {result}")

# Create metadata tables
with DatabaseManager() as db:
    # Create a database
    print("Creating metadata tables")
    result = db.create_meta_tables()
    print(f"Result: {result}")
    result = db.create_join_tables()
    print(f"Result: {result}")

# Generate video data from CSV
video_list = []
with open(VIDEO_CSV, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    video_list = [row for row in reader]

# Add videos to the database
for video in video_list:
    with DatabaseManager() as db:
        result = db.add_video(
            name=video['name'],
            url_1080=video['url_1080'],
            url_720=video['url_720'],
            url_480=video['url_480'],
            url_360=video['url_360'],
            url_240=video['url_240'],
            category_name=video['category_name'],
            description=video['description'],
            thumbnail=video['thumbnail'],
            duration=duration_to_seconds(video['duration']),
        )

        # Print the result, unless it was a duplicate
        if 'UNIQUE' not in result[1]:
            print(f"Adding video: {video['name']}")
            print(f"Result: {result}")

# Fetch and print all videos
with DatabaseManager() as db:
    videos = db.get_videos()
    print("Videos:")
    for video in videos:
        print(
            f"- {video['name']} (ID: {video['id']}, Category:"
            f"{video['category_id']})"
        )
