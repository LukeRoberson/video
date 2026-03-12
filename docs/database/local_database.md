# Local Database

The local database stores information about user profiles.

This includes information such as watched videos, in progress videos, and profile details

This is local to the implementation, and is updated (indirectly) by the user.

Also see **global_database.md** which contains information about videos and their metadata.
</br></br>


# Tables

## Table: *profiles*

**Purpose**
_Stores information about user profiles, including name and profile picture._

| Field Name  | Datatype  | Constraints               | Description                    |
| ----------- | --------- | ------------------------- | ------------------------------ |
| id          | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row |
| name        | TEXT      | NOT NULL                  | The profile name               |
| image       | TEXT      | NOT NULL                  | The profile image filename     |
| created_at  | TIMESTAMP |                           | The date/time this was created |


**Schema:**

```sql
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

</br></br>


## Table: *watch_history*

**Purpose**
_Stores information about watch history. Specifically, which videos have been watched_

| Field Name  | Datatype  | Constraints               | Description                          |
| ----------- | --------- | ------------------------- | ------------------------------------ |
| id          | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique identifier for each row       |
| profile_id  | INTEGER   | FOREIGN KEY, NOT NULL     | References the user's profile ID     |
| video_id    | INTEGER   | NOT NULL                  | The video ID (matches the global DB) |
| watched_at  | TIMESTAMP |                           | The date/time this was watched       |


**Schema:**
```sql
CREATE TABLE watch_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    video_id INTEGER NOT NULL,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES profiles(id)
)
```

</br></br>


## Table: *in_progress_videos*
_Stores information about videos that are in progress, allowing resume, etc_

| Field Name   | Datatype  | Constraints                        | Description                           |
| ------------ | --------- | ---------------------------------- | ------------------------------------- |
| profile_id   | INTEGER   | PRIMARY KEY, FOREIGN KEY, NOT NULL | Link to the user's profile            |
| video_id     | INTEGER   | PRIMARY KEY, NOT NULL              | A video ID, as in the global DB       |
| current_time | INTEGER   | NOT NULL                           | The time, in seconds, the video up to |
| updated_at   | TIMESTAMP |                                    | When this entry was updated           |


**Schema:**
```sql
CREATE TABLE in_progress_videos (
    profile_id INTEGER NOT NULL,
    video_id INTEGER NOT NULL,
    current_time INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (profile_id, video_id),
    FOREIGN KEY (profile_id) REFERENCES profiles(id)
)
```
</br></br>



# Database Manager

The database is managed by classes in **local_db.py**. These are:
* LocalDbContext
* ProfileManager
* ProgressManager
</br></br>


## Class: LocalDbContext

A context manager that connects to the database and sets up a cursor. It handles a clean disconnection at the end.

An instance of this class is used by other classes.

Example usage:
```python
with LocalDbContext() as db:
    profile_mgr = ProfileManager(db)
    profiles = profile_mgr.read()

print(profiles)
```
</br></br>


When this class is used, it will try to create the **local.db** file, if it does not already exist. If it does exist, it will just open the database.

If it creates the database file, it will also create the tables listed above.
</br></br>


## Class: ProfileManager

This class manages everything related to profiles. This supports basic CRUD operations:
* Create - Make a new profile entry
* Read - Get one or more profiles entries
* Update - Update an entry
* Delete - Delete an entry
</br></br>


Additionally, there are methods to manage a list of videos that have been watched:
* mark_watched
* mark_unwatched
* check_watched
</br></br>


## Class: ProgressManager

This manages the list of videos that are in progress. This also supports basic CRUD operations:
* Create - Make a new entry (a video has been started, but not finished)
* Read - Get one or more entries from the database
* Update - Update an entry (eg, more of the video has been watched)
* Delete - Delete an entry (eg, the video has been finished)
