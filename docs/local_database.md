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


# Database Manager

The database is managed by classes in **local_db.py**. These are:
* LocalDbContext
* ProfileManager
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

