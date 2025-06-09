import sys
import os

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

# Now you can import modules from the parent folder
from sql_db import DatabaseManager

characters = [
    {"name": "David", "video_name": "JW Broadcasting - October 2014"},
    {"name": "Jonathan", "video_name": "JW Broadcasting - October 2014"},
    {"name": "Saul", "video_name": "JW Broadcasting - October 2014"},

    {"name": "David", "video_name": "Act Wisely When Bullied"},
    {"name": "Jonathan", "video_name": "Act Wisely When Bullied"},
    {"name": "Saul", "video_name": "Act Wisely When Bullied"},
]

for character in characters:
    with DatabaseManager() as db:
        # Get the video ID from the name
        id = db.get_video_id_by_name(character["video_name"])

        if id is not None:
            result = db.add_character(
                video_id=id,
                character=character["name"]
            )
            print(f"Added character '{character['name']}' to video '{character['video_name']}': {result}")

        else:
            print(f"Video '{character['video_name']}' not found in the database. Skipping character addition.")

with DatabaseManager() as db:
    character_list = db.get_characters()
    print("Current character in the database:", character_list)
