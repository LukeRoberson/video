import sys
import os
import csv
from colorama import Style, Fore
import re

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

from sql_db import (  # noqa: E402
    DatabaseContext,
    VideoManager,
    CategoryManager,
    TagManager,
    SpeakerManager,
    CharacterManager,
    ScriptureManager,
)


VIDEO_CSV = 'metadata.csv'

# Generate data from CSV
meta_list = []
with open(VIDEO_CSV, newline='', encoding='cp1252') as csvfile:
    reader = csv.DictReader(csvfile)
    meta_list = [row for row in reader]

for item in meta_list:
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        video_id = video_mgr.name_to_id(item['name'])
        if video_id is None:
            print(
                Fore.RED,
                f"Video '{item['name']}' not found. Skipping",
                Style.RESET_ALL
            )
            continue

        # Add a description
        if len(item['description']) > 0:
            description = item['description'].strip()
            video_mgr.update(
                id=video_id,
                description=description,
            )

        # Add a tag
        if len(item['tag']) > 0:
            tag_mgr = TagManager(db)

            tag = item['tag'].strip()
            tag_id = tag_mgr.add(name=tag)

            if tag_id is None:
                print(
                    Fore.RED,
                    f"Tag '{tag}' already exists. Skipping",
                    Style.RESET_ALL
                )
            else:
                result = tag_mgr.add_to_video(
                    video_id=video_id,
                    tag_id=tag_id,
                )
                if result is False:
                    print(
                        Fore.RED,
                        f"Video '{item['name']}' could not be associated "
                        f"with tag '{tag}'",
                        Style.RESET_ALL
                    )

        # Add a speaker
        if len(item['speaker']) > 0:
            speaker_mgr = SpeakerManager(db)

            speaker = item['speaker'].strip()
            speaker_id = speaker_mgr.add(name=speaker)

            if speaker_id is None:
                print(
                    Fore.RED,
                    f"Speaker '{speaker}' already exists. Skipping",
                    Style.RESET_ALL
                )
            else:
                result = speaker_mgr.add_to_video(
                    video_id=video_id,
                    speaker_id=speaker_id,
                )
                if result is False:
                    print(
                        Fore.RED,
                        f"Video '{item['name']}' could not be associated "
                        f"with speaker '{speaker}'",
                        Style.RESET_ALL
                    )

        # Add a character
        if len(item['character']) > 0:
            character_mgr = CharacterManager(db)

            character = item['character'].strip()
            character_id = character_mgr.add(name=character)
            if character_id is None:
                print(
                    Fore.RED,
                    f"Character '{character}' already exists. Skipping",
                    Style.RESET_ALL
                )
            else:
                result = character_mgr.add_to_video(
                    video_id=video_id,
                    character_id=character_id,
                )
                if result is False:
                    print(
                        Fore.RED,
                        f"Video '{item['name']}' could not be associated "
                        f"with character '{character}'",
                        Style.RESET_ALL
                    )

        # Add a scripture reference
        if len(item['scripture']) > 0:
            scripture_mgr = ScriptureManager(db)

            scripture = item['scripture'].strip()
            match = re.match(r'(?P<book>(?:\d\s*)?\w[\w\s]*?)\s+(?P<chapter>\d+):(?P<verse>\d+)', scripture)
            if match:
                book = match.group('book').strip()
                chapter = match.group('chapter')
                verse = match.group('verse')
            else:
                book = chapter = verse = None

            if book is None or chapter is None or verse is None:
                print(
                    Fore.RED,
                    f"Scripture reference '{scripture}' is not valid. "
                    "Skipping",
                    Style.RESET_ALL
                )
            else:
                scripture_id = scripture_mgr.add(
                    book=book,
                    chapter=chapter,
                    verse=verse,
                )
                if scripture_id is None:
                    print(
                        Fore.RED,
                        f"Scripture reference '{scripture}' could not be added",
                        Style.RESET_ALL
                    )
                else:
                    result = scripture_mgr.add_to_video(
                        video_id=video_id,
                        scripture_id=scripture_id,
                    )
                    if result is False:
                        print(
                            Fore.RED,
                            f"Video '{item['name']}' could not be associated "
                            f"with scripture reference '{scripture}'",
                            Style.RESET_ALL
                        )
