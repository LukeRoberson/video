# Global Database

The global database stores information about videos and other metadata.

This is the database that any user would need access to. It's updated by an admin only, not a user.

Also see **local_database.md** which contains information on a database of local user information.
</br></br>


## Tables

### Table: *bible_characters*

**Purpose:**
_Stores Bible characters_

| Field Name  | Datatype | Constraints               | Description                    |
| ----------- | -------- | ------------------------- | ------------------------------ |
| id          | INTEGER  | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| name        | TEXT     | NOT NULL, UNIQUE          | Name of the character          |
| profile_pic | TEXT     |                           | Pic of the character           |
| date_range  | TEXT     |                           | Date range of theie life       |
| description | TEXT     |                           | A brief description of them    |


**Schema:**
```sql
CREATE TABLE bible_characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    profile_pic TEXT,
    date_range TEXT,
    description TEXT
);
```

</br></br>


### Table: *categories*

**Purpose:**
_Stores a list of categories that a video can belong to_

| Field Name | Datatype | Constraints               | Description                    |
| ---------- | -------- | ------------------------- | ------------------------------ |
| id         | INTEGER  | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| name       | TEXT     | NOT NULL, UNIQUE          | Name of the category           | 


**Schema:**
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
```

</br></br>


### Table: *scriptures*

**Purpose:**
_Stores scriptures (book, chapter, verse) that appear in videos. The combination of book/chapter/verse is unique_

| Field Name | Datatype | Constraints               | Description                    |
| ---------- | -------- | ------------------------- | ------------------------------ |
| id         | INTEGER  | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| book       | TEXT     | NOT NULL                  | Name of the book               | 
| chapter    | INTEGER  | NOT NULL                  | Chapter number                 | 
| verse      | INTEGER  | NOT NULL                  | Verse number                   |
| verse_text | TEXT     |                           | The verse text                 |


**Schema:**
```sql
CREATE TABLE scriptures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    verse_text TEXT,
    UNIQUE(book, chapter, verse)
);
```

</br></br>


### Table: *speakers*

**Purpose:**
_Stores the names of people who have appeared in videos_

| Field Name  | Datatype | Constraints               | Description                    |
| ----------- | -------- | ------------------------- | ------------------------------ |
| id          | INTEGER  | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| name        | TEXT     | NOT NULL, UNIQUE          | Person's name                  |
| profile_pic | TEXT     |                           | Picture of the speaker         |


**Schema:**
```sql
CREATE TABLE speakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    profile_pic TEXT
);
```

</br></br>


### Table: *tags*

**Purpose:**
_Stores a collection of tags that may be attached to a video_

| Field Name | Datatype | Constraints               | Description                    |
| ---------- | -------- | ------------------------- | ------------------------------ |
| id         | INTEGER  | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| name       | TEXT     | NOT NULL, UNIQUE          | Tag name                       | 


**Schema:**
```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
```

</br></br>


### Table: *location*

**Purpose:**
_Stores a collection of location tags that may be attached to a video_

| Field Name | Datatype | Constraints               | Description                    |
| ---------- | -------- | ------------------------- | ------------------------------ |
| id         | INTEGER  | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| name       | TEXT     | NOT NULL, UNIQUE          | Location name                  | 


**Schema:**
```sql
CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
```


### Table: *videos*

**Purpose:**
_A collection of videos and their details_

| Field Name  | Datatype  | Constraints               | Description                     |
| ----------- | --------- | ------------------------- | ------------------------------- |
| id          | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row  |
| name        | TEXT      | NOT NULL, UNIQUE          | Video name                      | 
| url_1080    | TEXT      |                           | URL for the video in 1080p      |
| url_720     | TEXT      |                           | URL for the video in 720p       |
| url_480     | TEXT      |                           | URL for the video in 480p       |
| url_360     | TEXT      |                           | URL for the video in 360p       |
| url_240     | TEXT      |                           | URL for the video in 240p       |
| description | TEXT      |                           | A description of the video      |
| thumbnail   | TEXT      |                           | URL for the video's thumbnail   |
| duration    | INTEGER   |                           | Video duration in seconds       |
| date_added  | TIMESTAMP |                           | The date the video was added    |
| url         | TEXT      |                           | URL to the video on the website |


**Schema:**
```sql
CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    url_1080 TEXT,
    url_720 TEXT,
    url_480 TEXT,
    url_360 TEXT,
    url_240 TEXT,
    description TEXT,
    thumbnail TEXT,
    duration INTEGER,
    date_added TIMESTAMP,
    url TEXT
);
```
</br></br>


### Table: *video_similarity*
_Pre-calculated similarity between videos_

See **similar_videos.md** for more information on how this works.

| Field Name  | Datatype  | Constraints                        | Description               |
| ----------- | --------- | ---------------------------------- | ------------------------- |
| video_1_id  | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | Video with the lowest ID  |
| video_2_id  | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | Video with the highest ID |
| score       | FLOAT     | NOT NULL                           | Similarity score          |

**Schema:**
```sql
CREATE TABLE "video_similarity" (
    video_1_id INTEGER NOT NULL,
    video_2_id INTEGER NOT NULL,
    score FLOAT NOT NULL,
    PRIMARY KEY (video_1_id, video_2_id),
    FOREIGN KEY (video_1_id) REFERENCES videos(id),
    FOREIGN KEY (video_2_id) REFERENCES videos(id),
    CHECK (video_1_id < video_2_id)
);

CREATE UNIQUE INDEX `sqlite_autoindex_video_similarity_1`
ON `video_similarity` (video_1_id, video_2_id);
```
</br></br>



## Relationship (Junction) Tables

### Table: *video_categories*

**Purpose:**
_Associates videos with categories (many-to-many relationship)._

| Field Name  | Datatype  | Constraints                        | References     |
| ----------- | --------- | ---------------------------------- | -------------- |
| video_id    | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | videos(id)     |
| category_id | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | categories(id) |


**Schema:**
```sql
CREATE TABLE video_categories (
    video_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (video_id, category_id),
    FOREIGN KEY (video_id) REFERENCES videos(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

</br></br>



### Table: *videos_bible_characters*

**Purpose:**
_Associates videos with Bible characters (many-to-many relationship)._

| Field Name   | Datatype  | Constraints                        | References           |
| ------------ | --------- | ---------------------------------- | -------------------- |
| video_id     | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | videos(id)           |
| character_id | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | bible_characters(id) |


**Schema:**
```sql
CREATE TABLE videos_bible_categories (
    video_id INTEGER NOT NULL,
    character_id INTEGER NOT NULL,
    PRIMARY KEY (video_id, character_id),
    FOREIGN KEY (video_id) REFERENCES videos(id),
    FOREIGN KEY (category_id) REFERENCES bible_characters(id)
);
```

</br></br>



### Table: *videos_scriptures*

**Purpose:**
_Associates videos with scriptures (many-to-many relationship)._

| Field Name   | Datatype  | Constraints                        | References     |
| ------------ | --------- | ---------------------------------- | -------------- |
| video_id     | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | videos(id)     |
| scripture_id | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | scriptures(id) |


**Schema:**
```sql
CREATE TABLE videos_scriptures (
    video_id INTEGER NOT NULL,
    scripture_id INTEGER NOT NULL,
    PRIMARY KEY (video_id, scripture_id),
    FOREIGN KEY (video_id) REFERENCES videos(id),
    FOREIGN KEY (scripture_id) REFERENCES scriptures(id)
);
```

</br></br>



### Table: *videos_speakers*

**Purpose:**
_Associates videos with speakers (many-to-many relationship)._

| Field Name | Datatype  | Constraints                        | References   |
| ---------- | --------- | ---------------------------------- | ------------ |
| video_id   | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | videos(id)   |
| speaker_id | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | speakers(id) |


**Schema:**
```sql
CREATE TABLE videos_speakers (
    video_id INTEGER NOT NULL,
    speaker_id INTEGER NOT NULL,
    PRIMARY KEY (video_id, speaker_id),
    FOREIGN KEY (video_id) REFERENCES videos(id),
    FOREIGN KEY (speaker_id) REFERENCES speakers(id)
);
```

</br></br>



### Table: *videos_tags*

**Purpose:**
_Associates videos with tags (many-to-many relationship)._

| Field Name | Datatype  | Constraints                        | References   |
| ---------- | --------- | ---------------------------------- | ------------ |
| video_id   | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | videos(id)   |
| tag_id     | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | tags(id)     |


**Schema:**
```sql
CREATE TABLE videos_tags (
    video_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (video_id, tag_id),
    FOREIGN KEY (video_id) REFERENCES videos(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);
```

</br></br>


### Table: *videos_locations*

**Purpose:**
_Associates videos with location (many-to-many relationship)._

| Field Name  | Datatype  | Constraints                        | References   |
| ----------- | --------- | ---------------------------------- | ------------ |
| video_id    | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | videos(id)   |
| location_id | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | tags(id)     |


**Schema:**
```sql
CREATE TABLE videos_locations (
    video_id INTEGER NOT NULL, 
    location_id INTEGER NOT NULL,
    PRIMARY KEY (video_id, location_id),
    FOREIGN KEY (video_id) REFERENCES videos(id),
    FOREIGN KEY (location_id) REFERENCES location(id)
)
```



# Database Manager

## Classes

There are several classes used in managing the database.
</br></br>


### Class: DatabaseContext

A context manager that connects to the database and sets up a cursor. It handles a clean disconnection at the end.

An instance of this class is used by other classes.

Example usage:
```
with DatabaseContext() as db:
    video_mgr = VideoManager(db)
    videos = video_mgr.get()

print(videos)
```
</br></br>


### Management Classes

There are classes for managing each of the main databases:
* VideoManager
* CategoryManager
* TagManager
* LocationManager
* SpeakerManager
* CharacterManager
* ScriptureManager
</br></br>

Each of these manage CRUD operations for the databases. They typically all have these methods (the VideoManager class is an exception):

| Method            | Purpose                          | Returns (on success) |
| ----------------- | -------------------------------- | -------------------- |
| add               | Add a new item                   | The item's ID        |
| update            | Update an existing item          | The item's ID        |
| get               | Get one or more items            | The item's ID        |
| get_from_video    | Get the item from a video        | A list of the item   |
| add_to_video      | Add an item to a video           | True                 |
| remove_from_video | Remove an item from a video      | True                 |
| name_to_id        | Convert an item's name to its ID | The item's ID        |

Here an _item_ refers to a category, tag, speaker, character, or scripture.

Classes use the ID of an object when making changes.

Most classes will take a name (string) as input. The exception is ScriptureManager, which takes a book (string), chapter (integer), and verse (int).

When adding an item, if the item already exists, there will be no error. The _add_ method will return the ID of that item, whether newly added, or it already existed.
</br></br>


### Class: VideoManager

The VideoManager class is slightly different, as:
1. It has a lot more fields to work with
2. It is not applied to other tables, in the same sense as a category is applied to a video.

The _add_ and _update_ methods take inputs for:
* id - On _update_ only. Mandatory
* name - Mandatory when adding a video
* description
* url - URL of the video' web page on jw.org
* url_1080 - URL of the video in 1080p
* url_720 - URL of the video in 720p
* url_480 - URL of the video in 480p
* url_360 - URL of the video in 360p
* url_240 - URL of the video in 240p
* thumbnail - URL of the video's thumbnail
* duration - Duration of the video (in seconds)
* date_added - The date the video was added to jw.org (in epoch format)

Not all fields need to be present. They can be ignored if the information is not available.

The _delete_ method only needs an ID of the video to delete.

The _get_ method will return all videos in the database, or one specific video if the optional ID is provided.

The _name_to_id_ method resolves a videos name (if found) to it's ID. The ID is needed to perform any video related operation.
</br></br>


**Filtering Results**

To filter results, use the _get_filter_ method. This allows us to pass:
* Category ID
* Tag ID
* Location ID
* Speaker ID
* Character ID
* Scripture ID

The Category ID is expected to be a list with one or more items, or 'None' if we don't want to filter based on category at all.

Other parameters accept only one item.

These are all optional. If none are passed, this is functionally the same as the _get_ method with no video ID. That is, it will return all videos.



### Workflows

This is how to add an item to a video (eg, add a category to a video). The same process applies for other metadata; Category is used below as an example.

1. Instantiate ContextManager, VideoManager, CategoryManager
2. Convert a video name to it's ID (if needed)
3. Add the category to the category database (it's ok if it already exists); Returns category ID
4. Add category to video, passing video ID and category ID

```python
video_name = "Test video"
category_name = "Test category"

with DatabaseContext() as db:
    video_mgr = VideoManager(db)
    cat_mgr = CategoryManager(db)

    video_id = video_mgr.name_to_id(video_name)
    category_id = cat_mgr.add(category_name)

    if video_id is not None and category_id is not None:
        cat_mgr.add_to_video(
            video_id = video_id,
            category_id = category_id
        )
```

