# Database

## Tables

### Table: *bible_characters*

**Purpose:**
_Stores Bible characters_

| Field Name | Datatype | Constraints               | Description                    |
| ---------- | -------- | ------------------------- | ------------------------------ |
| id         | INTEGER  | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| name       | TEXT     | NOT NULL, UNIQUE          | Name of the character          |


**Schema:**
```sql
CREATE TABLE bible_characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
```


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


### Table: *scriptures*

**Purpose:**
_Stores scriptures (book, chapter, verse) that appear in videos. The combination of book/chapter/verse is unique_

| Field Name | Datatype | Constraints               | Description                    |
| ---------- | -------- | ------------------------- | ------------------------------ |
| id         | INTEGER  | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| book       | TEXT     | NOT NULL                  | Name of the book               | 
| chapter    | INTEGER  | NOT NULL                  | Chapter number                 | 
| verse      | INTEGER  | NOT NULL                  | Verse number                   | 


**Schema:**
```sql
CREATE TABLE scriptures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    UNIQUE(book, chapter, verse)
);
```


### Table: *speakers*

**Purpose:**
_Stores the names of people who have appeared in videos_

| Field Name | Datatype | Constraints               | Description                    |
| ---------- | -------- | ------------------------- | ------------------------------ |
| id         | INTEGER  | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| name       | TEXT     | NOT NULL, UNIQUE          | Person's name                  | 


**Schema:**
```sql
CREATE TABLE speakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
```


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


# Database Manager

This is several classes to manage the database.


Parent class:
* context manager
* commit and close DB


Videos:
* Add a new video                                   [DONE]
* Update a video (by it's ID)                       [DONE]
* Delete a video (by it's ID)                       [DONE]
* Resolve a video name to an ID                     [DONE]
* Get all videos                                    [DONE]
* Get a video by it's ID                            [DONE]
* Get a filtered list of videos (category, etc)


Categories:
* Add a new category                                [DONE]
* Update a category (by ID)                         [DONE]
* Delete a category (by ID)                         [DONE]
* Add a category to a video
* Get categories (all/id)                           [DONE]
* Update the category on a video
* Remove a category from a video
* Resolve a category to an ID                       [DONE]


Tags:
* Add a new tag                                     [DONE]
* Update a tag                                      [DONE]
* Delete a tag                                      [DONE]
* Add a tag to a video
* Get tags (all/id)                                 [DONE]
* Update a tag on a video
* Remove a tag from a video
* Resolve a tag name to an ID                       [DONE]


Speaker:
* Add a new speaker                                 [DONE]
* Update a speaker                                  [DONE]
* Delete a speaker                                  [DONE]
* Add a speaker to a video
* Get speakers (all/id)                             [DONE]
* Update a speaker on a video
* Remove a speaker from a video
* Resolve a speaker name to an ID                   [DONE]


Character:
* Add a new character                               [DONE]
* Update a character                                [DONE]
* Delete a character                                [DONE]
* Add a character to a video
* Get characters (all/id)                           [DONE]
* Update a character on a video
* Remove a character from a video
* Resolve a character name to an ID                 [DONE]


Scripture:
* Add a new scripture                               [DONE]
* Update a scripture                                [DONE]
* Delete a scripture                                [DONE]
* Add a scripture to a video
* Get categories (all/id)                           [DONE]
* Update a scripture on a video
* Remove a scripture from a video
* Resolve a scripture name to an ID                 [DONE]

