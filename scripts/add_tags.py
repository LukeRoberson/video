import sys
import os

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

# Now you can import modules from the parent folder
from sql_db import DatabaseManager

tags = [
    {"tag": "av", "video_name": "JW Broadcasting - October 2014"},
    {"tag": "bethel", "video_name": "JW Broadcasting - October 2014"},
    {"tag": "broacasting", "video_name": "JW Broadcasting - October 2014"},
    {"tag": "prayer", "video_name": "JW Broadcasting - October 2014"},
    {"tag": "youth", "video_name": "JW Broadcasting - October 2014"},

    {"tag": "youth", "video_name": "Act Wisely When Bullied"},
    {"tag": "prayer", "video_name": "Act Wisely When Bullied"},
    {"tag": "school", "video_name": "Act Wisely When Bullied"},

    {"tag": "youth", "video_name": "Young Ones - You Are Loved by Jehovah"},
]

for tag in tags:
    with DatabaseManager() as db:
        # Get the video ID from the name
        id = db.get_video_id_by_name(tag["video_name"])

        if id is not None:
            result = db.add_tag(
                video_id=id,
                tag=tag["tag"]
            )
            print(f"Added tag '{tag['tag']}' to video '{tag['video_name']}': {result}")

        else:
            print(f"Video '{tag['video_name']}' not found in the database. Skipping tag addition.")

with DatabaseManager() as db:
    tag_list = db.get_tags()
    print("Current tags in the database:", tag_list)
