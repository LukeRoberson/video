import sys
import os

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

# Now you can import modules from the parent folder
from sql_db import DatabaseManager

scriptures = [
    {"book": "Psalm", "chapter": 18, "verse": 17, "video_name": "JW Broadcasting - October 2014"},
    {"book": "Matthew", "chapter": 19, "verse": 13, "video_name": "JW Broadcasting - October 2014"},
    {"book": "Matthew", "chapter": 19, "verse": 14, "video_name": "JW Broadcasting - October 2014"},
    {"book": "Matthew", "chapter": 21, "verse": 25, "video_name": "JW Broadcasting - October 2014"},
    {"book": "Luke", "chapter": 2, "verse": 24, "video_name": "JW Broadcasting - October 2014"},
    {"book": "Luke", "chapter": 2, "verse": 47, "video_name": "JW Broadcasting - October 2014"},
    {"book": "Luke", "chapter": 2, "verse": 51, "video_name": "JW Broadcasting - October 2014"},
    {"book": "Luke", "chapter": 2, "verse": 52, "video_name": "JW Broadcasting - October 2014"},

    {"book": "Matthew", "chapter": 19, "verse": 13, "video_name": "Young Ones - You Are Loved by Jehovah"},
    {"book": "Matthew", "chapter": 19, "verse": 14, "video_name": "Young Ones - You Are Loved by Jehovah"},
    {"book": "Matthew", "chapter": 21, "verse": 25, "video_name": "Young Ones - You Are Loved by Jehovah"},
    {"book": "Luke", "chapter": 2, "verse": 24, "video_name": "Young Ones - You Are Loved by Jehovah"},
    {"book": "Luke", "chapter": 2, "verse": 47, "video_name": "Young Ones - You Are Loved by Jehovah"},
    {"book": "Luke", "chapter": 2, "verse": 51, "video_name": "Young Ones - You Are Loved by Jehovah"},
    {"book": "Luke", "chapter": 2, "verse": 52, "video_name": "Young Ones - You Are Loved by Jehovah"},

    {"book": "Psalm", "chapter": 18, "verse": 17, "video_name": "Act Wisely When Bullied"},
]

for scripture in scriptures:
    with DatabaseManager() as db:
        # Get the video ID from the name
        id = db.get_video_id_by_name(scripture["video_name"])

        if id is not None:
            result = db.add_scripture(
                video_id=id,
                book=scripture["book"],
                chapter=scripture["chapter"],
                verse=scripture["verse"],
            )
            print(f"Added scripture '{scripture['book']} {scripture['chapter']}:{scripture['verse']}' to video '{scripture['video_name']}': {result}")

        else:
            print(f"Video '{scripture['video_name']}' not found in the database. Skipping character addition.")

with DatabaseManager() as db:
    list = db.get_scriptures()
    print("Current scriptures in the database:", list)
