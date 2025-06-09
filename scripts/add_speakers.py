import sys
import os

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

# Now you can import modules from the parent folder
from sql_db import DatabaseManager

speakers = [
    {"name": "Stephen Lett", "video_name": "JW Broadcasting - October 2014"},
    {"name": "Burt Mann", "video_name": "JW Broadcasting - October 2014"},
    {"name": "Theodore Jaracz", "video_name": "JW Broadcasting - October 2014"},
]

for speaker in speakers:
    with DatabaseManager() as db:
        # Get the video ID from the name
        id = db.get_video_id_by_name(speaker["video_name"])

        if id is not None:
            result = db.add_speaker(
                video_id=id,
                speaker=speaker["name"]
            )
            print(f"Added speaker '{speaker['name']}' to video '{speaker['video_name']}': {result}")

        else:
            print(f"Video '{speaker['video_name']}' not found in the database. Skipping speaker addition.")

with DatabaseManager() as db:
    speaker_list = db.get_speakers()
    print("Current speakers in the database:", speaker_list)
