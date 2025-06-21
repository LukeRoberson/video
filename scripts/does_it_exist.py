"""
Check if a video exists in the database.
"""

import sys
import os
from colorama import Style, Fore
import csv

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

from sql_db import (  # noqa: E402
    DatabaseContext,
    VideoManager,
    CategoryManager,
)


CSV_FILE = "jw_videos.csv"


if __name__ == "__main__":
    video_list = []
    new_videos = []

    # Load video names from CSV file and extend video_list
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                video_list.append(row)

    with DatabaseContext() as db:
        video_mgr = VideoManager(db)
        category_mgr = CategoryManager(db)
        print(f"There are {len(video_list)} videos to check.")

        for item in video_list:
            # Check if the video exists
            major_category = item[0]
            sub_category = item[1]
            video_name = item[2]
            video_id = video_mgr.name_to_id(video_name)
            if video_id is None:
                print(
                    Fore.RED,
                    f"Video '{video_name}' does not exist.",
                    Style.RESET_ALL
                )
                new_videos.append(item)

            # If it does, check the category
            else:
                cat_list = category_mgr.get_from_video(video_id)
                if not cat_list:
                    print(
                        Fore.CYAN,
                        f"Video '{video_name}' has no categories.",
                        Style.RESET_ALL
                    )
                    continue

                # Check if the major category exists on the video
                if not any(cat['name'] == major_category for cat in cat_list):
                    print(
                        Fore.MAGENTA,
                        f"Video '{video_name}' does not have major category "
                        f"'{major_category}'.",
                        Style.RESET_ALL
                    )
                    cat_id = category_mgr.name_to_id(major_category)

                    if cat_id is not None:
                        category_mgr.add_to_video(
                            video_id=video_id,
                            category_id=cat_id
                        )

                # Check if the sub category exists on the video
                if not any(cat['name'] == sub_category for cat in cat_list):
                    print(
                        Fore.YELLOW,
                        f"Video '{video_name}' does not have sub category "
                        f"'{sub_category}'.",
                        Style.RESET_ALL
                    )

                    cat_id = category_mgr.name_to_id(sub_category)
                    if cat_id is not None:
                        category_mgr.add_to_video(
                            video_id=video_id,
                            category_id=cat_id
                        )

    if new_videos:
        print(
            Fore.YELLOW,
            f"\n{len(new_videos)} new videos found that do not exist in the "
            "database.",
            Style.RESET_ALL
        )

        with open(
            "new_videos.csv",
            "w",
            newline='',
            encoding='utf-8'
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(new_videos)

        print(
            Fore.GREEN,
            "Saved new videos to 'new_videos.csv'.",
            Style.RESET_ALL
        )
