# Database Management Classes

This document describes the usage of the database management classes found in `sql_db.py`. These classes provide a structured way to interact with the SQLite database for videos, categories, tags, speakers, Bible characters, and scriptures.
</br></br>


## Overview

Each manager class provides CRUD (Create, Read, Update, Delete) operations for its respective entity. The `DatabaseContext` class is a context manager that handles the database connection and is required by all manager classes.
</br></br>


### Main Classes

- **DatabaseContext**: Context manager for database connections.
- **VideoManager**: Manage videos (add, update, delete, get, search, filter).
- **CategoryManager**: Manage categories and their association with videos.
- **TagManager**: Manage tags and their association with videos.
- **SpeakerManager**: Manage speakers and their association with videos.
- **CharacterManager**: Manage Bible characters and their association with videos.
- **ScriptureManager**: Manage scriptures and their association with videos.
</br></br>


## Usage Pattern

1. Use `DatabaseContext` as a context manager.
2. Instantiate the desired manager class, passing the context as an argument.
3. Call the manager's methods to perform operations.
</br></br>


### Example: Adding a Category to a Video

```python
from sql_db import DatabaseContext, VideoManager, CategoryManager

with DatabaseContext("videos.db") as db:
    video_mgr = VideoManager(db)
    cat_mgr = CategoryManager(db)

    video_id = video_mgr.name_to_id("Sample Video")
    category_id = cat_mgr.add("Education")

    if video_id and category_id:
        cat_mgr.add_to_video(video_id, category_id)
```
</br></br>


### Example: Searching for Videos

```python
with DatabaseContext() as db:
    video_mgr = VideoManager(db)
    results = video_mgr.search("Moses")
    print(results)
```
</br></br>


## Method Summary

Most manager classes provide the following methods:

| Method            | Description                                      |
|-------------------|--------------------------------------------------|
| add               | Add a new item (returns item ID)                 |
| update            | Update an existing item (returns item ID)        |
| delete            | Delete an item (returns item ID)                 |
| get               | Get all or one item (returns list of dicts)      |
| name_to_id        | Resolve name to ID (returns int or None)         |
| get_from_video    | Get items associated with a video                |
| add_to_video      | Associate item with a video                      |
| remove_from_video | Remove association between item and a video      |
</br></br>


**Note:**  
- `ScriptureManager.name_to_id` requires book, chapter, and verse.
- `VideoManager` provides additional methods: `get_filter`, `search`.
</br></br>


## Filtering Videos

To filter videos by metadata (category, tag, speaker, character, scripture):

```python
with DatabaseContext() as db:
    video_mgr = VideoManager(db)
    # Example: filter by category IDs [1, 2]
    filtered = video_mgr.get_filter(category_id=[1, 2])
```
</br></br>


## Error Handling

- Methods return `None` or `False` on failure.
- Adding an existing item returns its ID (no error).
- Always check return values before proceeding.
</br></br>


## See Also

- [database.md](database.md) for table schemas and relationships.
</br></br>

