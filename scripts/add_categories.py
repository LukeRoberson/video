import sys
import os

# Add parent folder to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from sql_db import (  # noqa: E402
    DatabaseContext,
    VideoManager,
    CategoryManager,
)


video_name = "JW Broadcasting - October 2014"
category_name = "Test category"

with DatabaseContext() as db:
    video_mgr = VideoManager(db)
    cat_mgr = CategoryManager(db)

    video_id = video_mgr.name_to_id(video_name)
    category_id = cat_mgr.add(category_name)

    if video_id is not None and category_id is not None:
        result = cat_mgr.add_to_video(
            video_id=video_id,
            category_id=category_id
        )

        if result:
            print(f"Video '{video_name}' added to category '{category_name}'.")
        else:
            print(
                f"Failed to add video '{video_name}' "
                f"to category '{category_name}'."
            )
