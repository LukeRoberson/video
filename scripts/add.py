import sys
import os

# Add parent folder to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from sql_db import (  # noqa: E402
    DatabaseContext,
    CategoryManager,
)

categories = [
    "Convention Music Presentations",
]

with DatabaseContext() as db:
    category_mgr = CategoryManager(db)

    for item in categories:
        id = category_mgr.add(item)
