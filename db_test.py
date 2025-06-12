"""
Test the db management classes

Use DatabaseContext as a context manager, and use other managers within:
    with DatabaseContext() as db:
        mgr = VideoManager(db)

Standard Methods ('item' = video, category, etc.):
    Get item by ID
        mgr.get(id = 1)

    Get all items
        mgr.get()

    Get an item ID by name
        mgr.name_to_id("item name")

    Add an item
        id = mgr.add(
            name="Sample entry"
        )

    Update an item
        mgr.update(
            id=1288,
            name="a new name",
        )


Scripture-specific Methods:
    Resolve a scripture reference to an ID:
        script_mgr.name_to_id(
            book = "Matthew",
            chapter = 21,
            verse = 25
        )

    Add a scripture reference:
        id = script_mgr.add(
            book="Matthew",
            chapter=21,
            verse=25,
        )

Exceptions to the above:
    Add a video:
        id = video_mgr.add(
            name="Sample Video",
            description="This is a sample video.",
            url="",
            url_1080="",
            url_720="",
            url_480="",
            url_360="",
            url_240="",
            thumbnail="",
            duration=0,
            date_added="",
        )
"""


from sql_db import (
    DatabaseContext,
    VideoManager,
    CategoryManager,
    TagManager,
    SpeakerManager,
    CharacterManager,
    ScriptureManager,
)


# Connect to the database
with DatabaseContext() as db:
    video_mgr = VideoManager(db)
    cat_mgr = CategoryManager(db)
    tag_mgr = TagManager(db)
    spk_mgr = SpeakerManager(db)
    ch_mgr = CharacterManager(db)
    scrip_mgr = ScriptureManager(db)
