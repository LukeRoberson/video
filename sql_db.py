"""
Module: db.py

This module provides classes for managing a SQLite database

classes:
    DatabaseContext:
        A context manager for handling SQLite database connections.
    VideoManager:
        A class for managing video-related operations in the database.
    CategoryManager:
        A class for managing category-related operations in the database.
    TagManager:
        A class for managing tag-related operations in the database.
    SpeakerManager:
        A class for managing speaker-related operations in the database.
    CharacterManager:
        A class for managing character-related operations in the database.
    ScriptureManager:
        A class for managing scripture-related operations in the database.

A video may have more than one URL for different resolutions.
    They may not all be available

Dependencies:
    - sqlite3: For SQLite database operations.
"""


import sqlite3
import traceback


class DatabaseContext:
    """
    A context manager for handling SQLite database connections.
    This class can be used alonside other database operations classes.

    Args:
        db_path (str): The path to the SQLite database file.
    """

    def __init__(
        self,
        db_path: str = "videos.db"
    ) -> None:
        """
        Initializes the DatabaseContext with a database path.
        """

        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def __enter__(
        self
    ) -> "DatabaseContext":
        """
        Start the context manager and return the instance.

        Args:
            None

        Returns:
            DatabaseContext: The instance of the DatabaseContext.
        """

        return self

    def __exit__(
        self,
        exc_type: type,
        exc_val: Exception,
        exc_tb: traceback.TracebackException
    ) -> None:
        """
        Exit the context manager, handling any exceptions.

        Args:
            exc_type (type): The type of the exception raised.
            exc_val (Exception): The exception instance.
            exc_tb (traceback.TracebackException): The traceback object.

        Returns:
            None
        """

        # Commit or rollback
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

        # Close the connection
        self.conn.close()


class VideoManager:
    """
    A class for managing video-related operations in the database.
        - Add/Update/Delete videos
        - Get videos (all, by ID, other filters)
        - Resolve video name to ID

    Args:
        db (DatabaseContext):
            An instance of DatabaseContext for database operations.
            This uses a 'composition' approach to manage database interactions.
    """

    def __init__(
        self,
        db: DatabaseContext
    ) -> None:
        """
        Initializes the VideoManager with a DatabaseContext instance.
            This uses a 'composition' approach

        Args:
            db (DatabaseContext): An instance of DatabaseContext for
                database operations.

        Returns:
            None
        """

        self.db = db

    def add(
        self,
        name: str,
        description: str = "",
        url: str = "",
        url_1080: str = "",
        url_720: str = "",
        url_480: str = "",
        url_360: str = "",
        url_240: str = "",
        thumbnail: str = "",
        duration: int = 0,
        date_added: str = "",
    ) -> int | None:
        """
        Adds a new video to the database.
            Not all fields are required, but at least a name is needed.

        Args:
            name (str): The name of the video.
            description (str): A description of the video.
            url (str): The main URL for the video.
            url_1080 (str): URL for the video in 1080p.
            url_720 (str): URL for the video in 720p.
            url_480 (str): URL for the video in 480p.
            url_360 (str): URL for the video in 360p.
            url_240 (str): URL for the video in 240p.
            thumbnail (str): URL or path to the video's thumbnail.
            duration (int): Duration of the video in seconds.
            date_added (str): The date the video was added.

        Returns:
            int | None:
                The ID of the newly added video if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("VideoManager.add: Invalid video name provided.")
            return None

        # Add the entry
        try:
            self.db.cursor.execute(
                """
                INSERT INTO videos (
                    name, description, url, url_1080, url_720, url_480,
                    url_360, url_240, thumbnail, duration, date_added
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    description,
                    url,
                    url_1080,
                    url_720,
                    url_480,
                    url_360,
                    url_240,
                    thumbnail,
                    duration,
                    date_added
                )
            )
            video_id = self.db.cursor.lastrowid
            self.db.conn.commit()

        except Exception as e:
            print(
                f"VideoManager.add: "
                f"An error occurred while adding the video:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return video_id

    def update(
        self,
        id: int,
        name: str = "",
        description: str = "",
        url: str = "",
        url_1080: str = "",
        url_720: str = "",
        url_480: str = "",
        url_360: str = "",
        url_240: str = "",
        thumbnail: str = "",
        duration: int = 0,
        date_added: str = "",
    ) -> int | None:
        """
        Updates an existing video in the database.
            Video is identified by its ID, which is immutable.
            Any other value can be updated.
            If values are not provided, they will not be updated.

        Args:
            id (int): The ID of the video to update.
            name (str): The new name of the video.
            description (str): The new description of the video.
            url (str): The new main URL for the video.
            url_1080 (str): New URL for the video in 1080p.
            url_720 (str): New URL for the video in 720p.
            url_480 (str): New URL for the video in 480p.
            url_360 (str): New URL for the video in 360p.
            url_240 (str): New URL for the video in 240p.
            thumbnail (str): New URL or path to the video's thumbnail.
            duration (int): New duration of the video in seconds.
            date_added (str): New date the video was added.

        Returns:
            int | None:
                The ID of the updated video if successful.
                Or None if an error occurs.
        """

        # Build the update statement dynamically
        #   based on provided (non-empty) values
        fields = []
        values = []

        if name:
            fields.append("name = ?")
            values.append(name)
        if description:
            fields.append("description = ?")
            values.append(description)
        if url:
            fields.append("url = ?")
            values.append(url)
        if url_1080:
            fields.append("url_1080 = ?")
            values.append(url_1080)
        if url_720:
            fields.append("url_720 = ?")
            values.append(url_720)
        if url_480:
            fields.append("url_480 = ?")
            values.append(url_480)
        if url_360:
            fields.append("url_360 = ?")
            values.append(url_360)
        if url_240:
            fields.append("url_240 = ?")
            values.append(url_240)
        if thumbnail:
            fields.append("thumbnail = ?")
            values.append(thumbnail)
        if duration:
            fields.append("duration = ?")
            values.append(duration)
        if date_added:
            fields.append("date_added = ?")
            values.append(date_added)

        if not fields:
            print("VideoManager.update: No fields to update.")
            return None

        # Set up the query
        values.append(id)
        query = f"UPDATE videos SET {', '.join(fields)} WHERE id = ?"

        try:
            self.db.cursor.execute(query, tuple(values))

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(f"VideoManager.update: No video found with ID {id}.")
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"VideoManager.update: "
                f"An error occurred while updating the video:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def delete(
        self,
        id: int,
    ) -> int | None:
        """
        Deletes a video from the database.
            Uses the video's ID to identify it.

        Args:
            id (int): The ID of the video to delete.

        Returns:
            int | None:
                The ID of the deleted video if successful.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                "DELETE FROM videos WHERE id = ?",
                (id,)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(f"VideoManager.delete: No video found with ID {id}.")
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"VideoManager.update: "
                f"An error occurred while updating the video:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def get(
        self,
        id: int | None = None,
    ) -> list[dict] | None:
        """
        Retrieves videos from the database.
            - Get a single video by a given ID
            - Get all videos

        Args:
            id (int | None): The ID of the video to retrieve.
                If None, retrieves all videos. Defaults to None.

        Returns:
            list[dict] | None:
                A list of dictionaries containing video details if successful.
                Or a None if an error occurs.
        """

        # Fetch all videos
        if id is None:
            query = self.db.cursor.execute("SELECT * FROM videos")

        # Fetch a single video by ID
        else:
            query = self.db.cursor.execute(
                "SELECT * FROM videos WHERE id = ?",
                (id,)
            )

        # Convert to a list of dictionaries, even for a single video
        try:
            items = [dict(row) for row in query.fetchall()]

        except Exception:
            return None

        return items

    def get_filter(
        self,
        category_id: list[int] | None = None,
        tag_id: int | None = None,
        speaker_id: int | None = None,
        character_id: int | None = None,
        scripture_id: int | None = None,
        missing_date: bool = False
    ) -> list[dict] | None:
        """
        Retrieves a filtered list of videos from the database.
        Filtering can be based on:
            - Category ID

        Args:
            category_id (list[int] | None):
                A list of category ID's to filter by.
                Returns videos the have ALL of the categories.
                If None, retrieves all videos. Defaults to None.
            tag_id (int | None):
                The ID of the tag to filter by.
                If None, does not filter by tag. Defaults to None.
            speaker_id (int | None):
                The ID of the speaker to filter by.
                If None, does not filter by speaker. Defaults to None.
            character_id (int | None):
                The ID of the character to filter by.
                If None, does not filter by character. Defaults to None.
            scripture_id (int | None):
                The ID of the scripture to filter by.
                If None, does not filter by scripture. Defaults to None.
            missing_date (bool):
                Filters for videos that are missing a 'date_added' value.
                If False, does not filter by date. Defaults to False.

        Returns:
            list[dict] | None:
                A list of dictionaries containing video details if successful.
                Or a None if an error occurs.
        """

        # Setup the base query
        #   DISTINCT ensures no duplicate videos are returned
        #   The 'v' is an alias for the videos table
        query = "SELECT DISTINCT v.* FROM videos v"

        # Stores parts of the query, depending on the filters
        #   A JOIN combines rows from two or more tables
        #   A WHERE clause filters records
        #   The params will be used to pass values to the query
        joins = []
        wheres = []
        params = []

        # Dymanically build the query fields based on provided filters
        #   This creates a list of JOIN and WHERE statements
        if (
            category_id is not None and
            isinstance(category_id, list) and
            category_id
        ):
            joins.append("JOIN video_categories vc ON v.id = vc.video_id")
            wheres.append(
                f"vc.category_id IN ({','.join(['?'] * len(category_id))})"
            )
            params.extend(category_id)

        if tag_id is not None:
            joins.append("JOIN videos_tags vt ON v.id = vt.video_id")
            wheres.append("vt.tag_id = ?")
            params.append(tag_id)

        if speaker_id is not None:
            joins.append("JOIN videos_speakers vs ON v.id = vs.video_id")
            wheres.append("vs.speaker_id = ?")
            params.append(speaker_id)

        if character_id is not None:
            joins.append("JOIN videos_bible_characters vch ON v.id = vch.video_id")
            wheres.append("vch.character_id = ?")
            params.append(character_id)

        if scripture_id is not None:
            joins.append("JOIN videos_scriptures vscr ON v.id = vscr.video_id")
            wheres.append("vscr.scripture_id = ?")
            params.append(scripture_id)

        if missing_date:
            wheres.append("(v.date_added IS NULL OR v.date_added = '')")

        # Convert the list of JOIN and WHERE statements to strings
        if joins:
            query += " " + " ".join(joins)
        if wheres:
            query += " WHERE " + " AND ".join(wheres)

        # Add a GROUP BY clause if filtering by categories
        if (
            category_id is not None and
            isinstance(category_id, list) and
            category_id
        ):
            query += " GROUP BY v.id HAVING COUNT(DISTINCT vc.category_id) = ?"
            params.append(len(category_id))

        # Execute the query with the parameters
        cursor = self.db.cursor.execute(query, tuple(params))

        # Convert to a list of dictionaries and return
        return [dict(row) for row in cursor.fetchall()]

    def name_to_id(
        self,
        name: str
    ) -> int | None:
        """
        Resolve a video name to its ID.

        Args:
            name (str): The name of the video.

        Returns:
            int | None:
                The ID of the video if found
                None if the video does not exist.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("VideoManager.name_to_id: Invalid video name provided.")
            return None

        try:
            self.db.cursor.execute(
                "SELECT id FROM videos WHERE name = ?",
                (name,)
            )
            result = self.db.cursor.fetchone()

            # There should be only one result, or nothing
            return result[0] if result else None

        except Exception as e:
            print(f"VideoManager.name_to_id: An error occurred while "
                  f"resolving video name '{name}' to ID:\n{e}")
            return None


class CategoryManager:
    """
    A class for managing catrgory-related operations in the database.
        - Add/Update/Delete categories
        - Add/Update/Remove catefories to/from videos
        - Get categories (all, assigned to a video)
        - Resolve category name to ID

    Args:
        db (DatabaseContext):
            An instance of DatabaseContext for database operations.
            This uses a 'composition' approach to manage database interactions.
    """

    def __init__(
        self,
        db: DatabaseContext
    ) -> None:
        """
        Initializes the class with a DatabaseContext instance.
            This uses a 'composition' approach

        Args:
            db (DatabaseContext): An instance of DatabaseContext for
                database operations.

        Returns:
            None
        """

        self.db = db

    def add(
        self,
        name: str,
    ) -> int | None:
        """
        Adds a new category to the database.

        Args:
            name (str): The name of the category to be added.

        Returns:
            int | None:
                The ID of the newly added category if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("CategoryManager.add: Invalid category name provided.")
            return None

        # Add the entry
        try:
            # Will just ignore it if it already exists
            self.db.cursor.execute(
                "INSERT OR IGNORE INTO categories (name) VALUES (?)",
                (name,)
            )
            self.db.conn.commit()

            # Get the ID of the category,
            #   whether it was just added or already existed
            self.db.cursor.execute(
                "SELECT id FROM categories WHERE name = ?",
                (name,)
            )
            row = self.db.cursor.fetchone()
            category_id = row[0] if row else None

        except Exception as e:
            print(
                f"CategoryManager.add: "
                f"An error occurred while adding the category:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return category_id

    def update(
        self,
        id: int,
        name: str,
    ) -> int | None:
        """
        Updates an existing category in the database.
            Identified by its ID, which is immutable.

        Args:
            id (int): The ID of the category to update.
            name (str): The new name of the category.

        Returns:
            int | None:
                The ID of the updated category if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("VideoManager.add: Invalid video name provided.")
            return None

        # Update the entry
        try:
            self.db.cursor.execute(
                "UPDATE categories SET name = ? WHERE id = ?",
                (name, id)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(
                    f"CategoryManager.update: No category found with ID {id}."
                )
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"CategoryManager.update: "
                f"An error occurred while updating the category:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def delete(
        self,
        id: int,
    ) -> int | None:
        """
        Deletes a category from the database.
            Uses the category's ID to identify it.

        Args:
            id (int): The ID of the category to delete.

        Returns:
            int | None:
                The ID of the deleted category if successful.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                "DELETE FROM categories WHERE id = ?",
                (id,)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(
                    f"CategoryManager.delete: No category found with ID {id}."
                )
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"CategoryManager.update: "
                f"An error occurred while updating the category:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def get(
        self,
        id: int | None = None,
    ) -> list[dict] | None:
        """
        Retrieves categories from the database.
            - Get a single category by a given ID
            - Get all categories

        Args:
            id (int | None): The ID of the category to retrieve.
                If None, retrieves all categories. Defaults to None.

        Returns:
            list[dict] | None:
                A list of dictionaries containing category details.
                Or a None if an error occurs.
        """

        # Fetch all
        if id is None:
            query = self.db.cursor.execute("SELECT * FROM categories")

        # Fetch a single video by ID
        else:
            query = self.db.cursor.execute(
                "SELECT * FROM categories WHERE id = ?",
                (id,)
            )

        # Convert to a list of dictionaries, even for a single video
        try:
            items = [dict(row) for row in query.fetchall()]

        except Exception:
            return None

        return items

    def get_from_video(
        self,
        video_id: int,
    ) -> list[dict] | None:
        """
        Retrieves categories associated with a specific video.

        Args:
            video_id (int):
                The ID of the video for which to retrieve categories.

        Returns:
            list[dict] | None:
                A list of dictionaries containing category details.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                """
                SELECT c.* FROM categories c
                JOIN video_categories vc ON c.id = vc.category_id
                WHERE vc.video_id = ?
                """,
                (video_id,)
            )
            items = [dict(row) for row in self.db.cursor.fetchall()]

        except Exception as e:
            print(f"Error retrieving categories for video {video_id}: {e}")
            return None

        return items

    def add_to_video(
        self,
        video_id: int,
        category_id: int
    ) -> bool:
        """
        Adds a category to a video in the database.
            Uses the 'video_categories' junction table to associate
            a video with a category.

        Args:
            video_id (int): The ID of the video to which the category
                will be added.
            category_id (int): The ID of the category to add to the video.

        Returns:
            bool:
                True if the category was successfully added to the video.
                False if an error occurs or the association already exists.
        """

        # Verify video exists
        self.db.cursor.execute(
            "SELECT 1 FROM videos WHERE id = ?", (video_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"Video with ID {video_id} does not exist.")
            return False

        # Verify category exists
        self.db.cursor.execute(
            "SELECT 1 FROM categories WHERE id = ?", (category_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"Category with ID {category_id} does not exist.")
            return False

        try:
            self.db.cursor.execute(
                """
                INSERT OR IGNORE INTO video_categories (video_id, category_id)
                VALUES (?, ?)
                """, (video_id, category_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error linking category to video: {e}")
            return False

    def remove_from_video(
        self,
        video_id: int,
        category_id: int
    ) -> bool:
        """
        Removes a category from a video in the database.
            Uses the 'video_categories' junction table to disassociate

        Args:
            video_id (int): The ID of the video from which the
                category will be removed.
            category_id (int): The ID of the category to remove from the video.

        Returns:
            bool:
                True if the category was successfully removed from the video.
                False if an error occurs or the association does not exist.
        """

        try:
            self.db.cursor.execute(
                """
                DELETE FROM video_categories
                WHERE video_id = ?
                AND category_id = ?
                """,
                (video_id, category_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error unlinking category from video: {e}")
            return False

    def name_to_id(
        self,
        name: str
    ) -> int | None:
        """
        Resolve a category name to its ID.

        Args:
            name (str): The name of the category.

        Returns:
            int | None:
                The ID of the video if found
                None if the video does not exist.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print(
                "CategoryManager.name_to_id: Invalid category name provided."
            )
            return None

        try:
            self.db.cursor.execute(
                "SELECT id FROM categories WHERE name = ?",
                (name,)
            )
            result = self.db.cursor.fetchone()

            # There should be only one result, or nothing
            return result[0] if result else None

        except Exception as e:
            print(f"CategoryManager.name_to_id: An error occurred while "
                  f"resolving category name '{name}' to ID:\n{e}")
            return None


class TagManager:
    """
    A class for managing tag-related operations in the database.
        - Add/Update/Delete tags
        - Add/Update/Remove tags to/from videos
        - Get tags (all, assigned to a video)
        - Resolve tag name to ID

    Args:
        db (DatabaseContext):
            An instance of DatabaseContext for database operations.
            This uses a 'composition' approach to manage database interactions.
    """

    def __init__(
        self,
        db: DatabaseContext
    ) -> None:
        """
        Initializes the class with a DatabaseContext instance.
            This uses a 'composition' approach

        Args:
            db (DatabaseContext): An instance of DatabaseContext for
                database operations.

        Returns:
            None
        """

        self.db = db

    def add(
        self,
        name: str,
    ) -> int | None:
        """
        Adds a new tag to the database.

        Args:
            name (str): The name of the tag to be added.

        Returns:
            int | None:
                The ID of the newly added tag if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("TagManager.add: Invalid tag name provided.")
            return None

        # Add the entry
        try:
            # Will just ignore it if it already exists
            self.db.cursor.execute(
                "INSERT OR IGNORE INTO tags (name) VALUES (?)",
                (name,)
            )
            self.db.conn.commit()

            # Get the ID of the tag,
            #   whether it was just added or already existed
            self.db.cursor.execute(
                "SELECT id FROM tags WHERE name = ?",
                (name,)
            )
            row = self.db.cursor.fetchone()
            tag_id = row[0] if row else None

        except Exception as e:
            print(
                f"TagManager.add: "
                f"An error occurred while adding the tag:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return tag_id

    def update(
        self,
        id: int,
        name: str,
    ) -> int | None:
        """
        Updates an existing tag in the database.
            Identified by its ID, which is immutable.

        Args:
            id (int): The ID of the tag to update.
            name (str): The new name of the tag.

        Returns:
            int | None:
                The ID of the updated tag if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("TagManager.add: Invalid tag name provided.")
            return None

        # Update the entry
        try:
            self.db.cursor.execute(
                "UPDATE tags SET name = ? WHERE id = ?",
                (name, id)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(f"TagManager.update: No tag found with ID {id}.")
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"TagManager.update: "
                f"An error occurred while updating the tag:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def delete(
        self,
        id: int,
    ) -> int | None:
        """
        Deletes a tag from the database.
            Uses the tag's ID to identify it.

        Args:
            id (int): The ID of the tag to delete.

        Returns:
            int | None:
                The ID of the deleted tag if successful.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                "DELETE FROM tags WHERE id = ?",
                (id,)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(f"TagManager.delete: No tag found with ID {id}.")
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"TagManager.update: "
                f"An error occurred while updating the tag:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def get(
        self,
        id: int | None = None,
    ) -> list[dict] | None:
        """
        Retrieves tags from the database.
            - Get a single tag by a given ID
            - Get all tags

        Args:
            id (int | None): The ID of the tag to retrieve.
                If None, retrieves all tags. Defaults to None.

        Returns:
            list[dict] | None:
                A list of dictionaries containing tag details if successful.
                Or a None if an error occurs.
        """

        # Fetch all
        if id is None:
            query = self.db.cursor.execute("SELECT * FROM tags")

        # Fetch a single item by ID
        else:
            query = self.db.cursor.execute(
                "SELECT * FROM tags WHERE id = ?",
                (id,)
            )

        # Convert to a list of dictionaries, even for a single item
        try:
            items = [dict(row) for row in query.fetchall()]

        except Exception:
            return None

        return items

    def get_from_video(
        self,
        video_id: int,
    ) -> list[dict] | None:
        """
        Retrieves tags associated with a specific video.

        Args:
            video_id (int): The ID of the video for which to retrieve tags.

        Returns:
            list[dict] | None:
                A list of dictionaries containing tag details if successful.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                """
                SELECT t.* FROM tags t
                JOIN videos_tags vt ON t.id = vt.tag_id
                WHERE vt.video_id = ?
                """,
                (video_id,)
            )
            items = [dict(row) for row in self.db.cursor.fetchall()]

        except Exception as e:
            print(f"Error retrieving tags for video {video_id}: {e}")
            return None

        return items

    def add_to_video(
        self,
        video_id: int,
        tag_id: int
    ) -> bool:
        """
        Adds a category to a video in the database.
            Uses the 'videos_tags' junction table to associate
            a video with a tag.

        Args:
            video_id (int): The ID of the video to which the tag will be added.
            tag_id (int): The ID of the tag to add to the video.

        Returns:
            bool:
                True if the tag was successfully added to the video.
                False if an error occurs or the association already exists.
        """

        # Verify video exists
        self.db.cursor.execute(
            "SELECT 1 FROM videos WHERE id = ?", (video_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"Video with ID {video_id} does not exist.")
            return False

        # Verify tag exists
        self.db.cursor.execute(
            "SELECT 1 FROM tags WHERE id = ?", (tag_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"Tag with ID {tag_id} does not exist.")
            return False

        try:
            self.db.cursor.execute(
                """
                INSERT OR IGNORE INTO videos_tags (video_id, tag_id)
                VALUES (?, ?)
                """, (video_id, tag_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error linking tag to video: {e}")
            return False

    def remove_from_video(
        self,
        video_id: int,
        tag_id: int
    ) -> bool:
        """
        Removes a tag from a video in the database.
            Uses the 'videos_tags' junction table to disassociate

        Args:
            video_id (int): The ID of the video from which the
                tag will be removed.
            tag_id (int): The ID of the tag to remove from the video.

        Returns:
            bool:
                True if the tag was successfully removed from the video.
                False if an error occurs or the association does not exist.
        """

        try:
            self.db.cursor.execute(
                """
                DELETE FROM videos_tags
                WHERE video_id = ?
                AND tag_id = ?
                """,
                (video_id, tag_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error unlinking tag from video: {e}")
            return False

    def name_to_id(
        self,
        name: str
    ) -> int | None:
        """
        Resolve a tag name to its ID.

        Args:
            name (str): The name of the tag.

        Returns:
            int | None:
                The ID of the tag if found
                None if the tag does not exist.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print(
                "TagManager.name_to_id: Invalid tag name provided."
            )
            return None

        try:
            self.db.cursor.execute(
                "SELECT id FROM tags WHERE name = ?",
                (name,)
            )
            result = self.db.cursor.fetchone()

            # There should be only one result, or nothing
            return result[0] if result else None

        except Exception as e:
            print(f"TagManager.name_to_id: An error occurred while "
                  f"resolving tag name '{name}' to ID:\n{e}")
            return None


class SpeakerManager:
    """
    A class for managing speaker-related operations in the database.
        - Add/Update/Delete speaker
        - Add/Update/Remove speaker to/from videos
        - Get speaker (all, assigned to a video)
        - Resolve tag name to ID

    Args:
        db (DatabaseContext):
            An instance of DatabaseContext for database operations.
            This uses a 'composition' approach to manage database interactions.
    """

    def __init__(
        self,
        db: DatabaseContext
    ) -> None:
        """
        Initializes the class with a DatabaseContext instance.
            This uses a 'composition' approach

        Args:
            db (DatabaseContext): An instance of DatabaseContext for
                database operations.

        Returns:
            None
        """

        self.db = db

    def add(
        self,
        name: str,
    ) -> int | None:
        """
        Adds a new speaker to the database.

        Args:
            name (str): The name of the speaker to be added.

        Returns:
            int | None:
                The ID of the newly added speaker if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("SpeakerManager.add: Invalid speaker name provided.")
            return None

        # Add the entry
        try:
            # Will just ignore it if it already exists
            self.db.cursor.execute(
                "INSERT OR IGNORE INTO speakers (name) VALUES (?)",
                (name,)
            )
            self.db.conn.commit()

            # Get the ID of the speaker,
            #   whether it was just added or already existed
            self.db.cursor.execute(
                "SELECT id FROM speakers WHERE name = ?",
                (name,)
            )
            row = self.db.cursor.fetchone()
            speaker_id = row[0] if row else None

        except Exception as e:
            print(
                f"SpeakerManager.add: "
                f"An error occurred while adding the speaker:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return speaker_id

    def update(
        self,
        id: int,
        name: str,
    ) -> int | None:
        """
        Updates an existing speaker in the database.
            Identified by its ID, which is immutable.

        Args:
            id (int): The ID of the speaker to update.
            name (str): The new name of the speaker.

        Returns:
            int | None:
                The ID of the updated speaker if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("SpeakerManager.add: Invalid speaker name provided.")
            return None

        # Update the entry
        try:
            self.db.cursor.execute(
                "UPDATE speakers SET name = ? WHERE id = ?",
                (name, id)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(f"SpeakerManager.update: No speaker found with ID {id}.")
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"SpeakerManager.update: "
                f"An error occurred while updating the speaker:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def delete(
        self,
        id: int,
    ) -> int | None:
        """
        Deletes a speaker from the database.
            Uses the speaker's ID to identify it.

        Args:
            id (int): The ID of the speaker to delete.

        Returns:
            int | None:
                The ID of the deleted speaker if successful.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                "DELETE FROM speakers WHERE id = ?",
                (id,)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(f"SpeakerManager.delete: No speaker found with ID {id}.")
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"SpeakerManager.update: "
                f"An error occurred while updating the speaker:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def get(
        self,
        id: int | None = None,
    ) -> list[dict] | None:
        """
        Retrieves speakers from the database.
            - Get a single speaker by a given ID
            - Get all speakers

        Args:
            id (int | None): The ID of the tag to retrieve.
                If None, retrieves all speakers. Defaults to None.

        Returns:
            list[dict] | None:
                A list of dictionaries containing speaker details.
                Or a None if an error occurs.
        """

        # Fetch all
        if id is None:
            query = self.db.cursor.execute("SELECT * FROM speakers")

        # Fetch a single item by ID
        else:
            query = self.db.cursor.execute(
                "SELECT * FROM speakers WHERE id = ?",
                (id,)
            )

        # Convert to a list of dictionaries, even for a single item
        try:
            items = [dict(row) for row in query.fetchall()]

        except Exception:
            return None

        return items

    def get_from_video(
        self,
        video_id: int,
    ) -> list[dict] | None:
        """
        Retrieves speakers associated with a specific video.

        Args:
            video_id (int): The ID of the video for which to retrieve speakers.

        Returns:
            list[dict] | None:
                A list of dictionaries containing speaker details.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                """
                SELECT s.* FROM speakers s
                JOIN videos_speakers vs ON s.id = vs.speaker_id
                WHERE vs.video_id = ?
                """,
                (video_id,)
            )
            items = [dict(row) for row in self.db.cursor.fetchall()]

        except Exception as e:
            print(f"Error retrieving speakers for video {video_id}: {e}")
            return None

        return items

    def add_to_video(
        self,
        video_id: int,
        speaker_id: int
    ) -> bool:
        """
        Adds a category to a video in the database.
            Uses the 'videos_speakers' junction table to associate
            a video with a speaker.

        Args:
            video_id (int): The ID of the video to which the speaker is added.
            speaker_id (int): The ID of the speaker to add to the video.

        Returns:
            bool:
                True if the speaker was successfully added to the video.
                False if an error occurs or the association already exists.
        """

        # Verify video exists
        self.db.cursor.execute(
            "SELECT 1 FROM videos WHERE id = ?", (video_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"Video with ID {video_id} does not exist.")
            return False

        # Verify speaker exists
        self.db.cursor.execute(
            "SELECT 1 FROM speakers WHERE id = ?", (speaker_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"Speaker with ID {speaker_id} does not exist.")
            return False

        try:
            self.db.cursor.execute(
                """
                INSERT OR IGNORE INTO videos_speakers (video_id, speaker_id)
                VALUES (?, ?)
                """, (video_id, speaker_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error linking speaker to video: {e}")
            return False

    def remove_from_video(
        self,
        video_id: int,
        speaker_id: int
    ) -> bool:
        """
        Removes a speaker from a speaker in the database.
            Uses the 'videos_speakers' junction table to disassociate

        Args:
            video_id (int): The ID of the video from which
                the speaker will be removed.
            speaker_id (int): The ID of the speaker to remove from the video.

        Returns:
            bool:
                True if the speaker was successfully removed from the video.
                False if an error occurs or the association does not exist.
        """

        try:
            self.db.cursor.execute(
                """
                DELETE FROM videos_speakers
                WHERE video_id = ?
                AND speaker_id = ?
                """,
                (video_id, speaker_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error unlinking speaker from video: {e}")
            return False

    def name_to_id(
        self,
        name: str
    ) -> int | None:
        """
        Resolve a speaker name to its ID.

        Args:
            name (str): The name of the speaker.

        Returns:
            int | None:
                The ID of the speaker if found
                None if the speaker does not exist.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print(
                "SpeakerManager.name_to_id: Invalid speaker name provided."
            )
            return None

        try:
            self.db.cursor.execute(
                "SELECT id FROM speakers WHERE name = ?",
                (name,)
            )
            result = self.db.cursor.fetchone()

            # There should be only one result, or nothing
            return result[0] if result else None

        except Exception as e:
            print(f"SpeakerManager.name_to_id: An error occurred while "
                  f"resolving speaker name '{name}' to ID:\n{e}")
            return None


class CharacterManager:
    """
    A class for managing character-related operations in the database.
        - Add/Update/Delete character
        - Add/Update/Remove character to/from videos
        - Get character (all, assigned to a video)
        - Resolve tag name to ID

    Args:
        db (DatabaseContext):
            An instance of DatabaseContext for database operations.
            This uses a 'composition' approach to manage database interactions.
    """

    def __init__(
        self,
        db: DatabaseContext
    ) -> None:
        """
        Initializes the class with a DatabaseContext instance.
            This uses a 'composition' approach

        Args:
            db (DatabaseContext): An instance of DatabaseContext for
                database operations.

        Returns:
            None
        """

        self.db = db

    def add(
        self,
        name: str,
    ) -> int | None:
        """
        Adds a new character to the database.

        Args:
            name (str): The name of the character to be added.

        Returns:
            int | None:
                The ID of the newly added character if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("CharacterManager.add: Invalid character name provided.")
            return None

        # Add the entry
        try:
            # Will just ignore it if it already exists
            self.db.cursor.execute(
                "INSERT OR IGNORE INTO bible_characters (name) VALUES (?)",
                (name,)
            )
            self.db.conn.commit()

            # Get the ID of the character,
            #   whether it was just added or already existed
            self.db.cursor.execute(
                "SELECT id FROM bible_characters WHERE name = ?",
                (name,)
            )
            row = self.db.cursor.fetchone()
            character_id = row[0] if row else None

        except Exception as e:
            print(
                f"CharacterManager.add: "
                f"An error occurred while adding the character:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return character_id

    def update(
        self,
        id: int,
        name: str,
    ) -> int | None:
        """
        Updates an existing character in the database.
            Identified by its ID, which is immutable.

        Args:
            id (int): The ID of the character to update.
            name (str): The new name of the character.

        Returns:
            int | None:
                The ID of the updated character if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print("CharacterManager.add: Invalid character name provided.")
            return None

        # Update the entry
        try:
            self.db.cursor.execute(
                "UPDATE bible_characters SET name = ? WHERE id = ?",
                (name, id)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(
                    f"CharacterManager.update: "
                    f"No character found with ID {id}."
                )
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"CharacterManager.update: "
                f"An error occurred while updating the character:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def delete(
        self,
        id: int,
    ) -> int | None:
        """
        Deletes a character from the database.
            Uses the character's ID to identify it.

        Args:
            id (int): The ID of the character to delete.

        Returns:
            int | None:
                The ID of the deleted character if successful.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                "DELETE FROM bible_characters WHERE id = ?",
                (id,)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(
                    f"CharacterManager.delete: "
                    f"No character found with ID {id}."
                )
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"CharacterManager.update: "
                f"An error occurred while updating the character:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def get(
        self,
        id: int | None = None,
    ) -> list[dict] | None:
        """
        Retrieves characters from the database.
            - Get a single character by a given ID
            - Get all characters

        Args:
            id (int | None): The ID of the character to retrieve.
                If None, retrieves all characters. Defaults to None.

        Returns:
            list[dict] | None:
                A list of dictionaries containing character details.
                Or a None if an error occurs.
        """

        # Fetch all
        if id is None:
            query = self.db.cursor.execute("SELECT * FROM bible_characters")

        # Fetch a single item by ID
        else:
            query = self.db.cursor.execute(
                "SELECT * FROM bible_characters WHERE id = ?",
                (id,)
            )

        # Convert to a list of dictionaries, even for a single item
        try:
            items = [dict(row) for row in query.fetchall()]

        except Exception:
            return None

        return items

    def get_from_video(
        self,
        video_id: int,
    ) -> list[dict] | None:
        """
        Retrieves characters associated with a specific video.

        Args:
            video_id (int): The ID of the video for which to
                retrieve characters.

        Returns:
            list[dict] | None:
                A list of dictionaries containing character details.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                """
                SELECT c.* FROM bible_characters c
                JOIN videos_bible_characters vc ON c.id = vc.character_id
                WHERE vc.video_id = ?
                """,
                (video_id,)
            )
            items = [dict(row) for row in self.db.cursor.fetchall()]

        except Exception as e:
            print(f"Error retrieving characters for video {video_id}: {e}")
            return None

        return items

    def add_to_video(
        self,
        video_id: int,
        character_id: int
    ) -> bool:
        """
        Adds a category to a video in the database.
            Uses the 'videos_bible_characters' junction table to associate
            a video with a character.

        Args:
            video_id (int): The ID of the video to which the character
                will be added.
            character_id (int): The ID of the character to add to the video.

        Returns:
            bool:
                True if the character was successfully added to the video.
                False if an error occurs or the association already exists.
        """

        # Verify video exists
        self.db.cursor.execute(
            "SELECT 1 FROM videos WHERE id = ?", (video_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"Video with ID {video_id} does not exist.")
            return False

        # Verify character exists
        self.db.cursor.execute(
            "SELECT 1 FROM bible_characters WHERE id = ?", (character_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"character with ID {character_id} does not exist.")
            return False

        try:
            self.db.cursor.execute(
                """
                INSERT OR
                IGNORE INTO videos_bible_characters (video_id, character_id)
                VALUES (?, ?)
                """, (video_id, character_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error linking a character to video: {e}")
            return False

    def remove_from_video(
        self,
        video_id: int,
        character_id: int
    ) -> bool:
        """
        Removes a character from a video in the database.
            Uses the 'videos_characters' junction table to disassociate

        Args:
            video_id (int): The ID of the video from which the
                character will be removed.
            character_id (int): The ID of the character to remove
                from the video.

        Returns:
            bool:
                True if the character was successfully removed from the video.
                False if an error occurs or the association does not exist.
        """

        try:
            self.db.cursor.execute(
                """
                DELETE FROM videos_bible_characters
                WHERE video_id = ?
                AND character_id = ?
                """,
                (video_id, character_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error unlinking character from video: {e}")
            return False

    def name_to_id(
        self,
        name: str
    ) -> int | None:
        """
        Resolve a character name to its ID.

        Args:
            name (str): The name of the character.

        Returns:
            int | None:
                The ID of the character if found
                None if the character does not exist.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(name, str) or not name.strip():
            print(
                "CharacterManager.name_to_id: Invalid character name provided."
            )
            return None

        try:
            self.db.cursor.execute(
                "SELECT id FROM bible_characters WHERE name = ?",
                (name,)
            )
            result = self.db.cursor.fetchone()

            # There should be only one result, or nothing
            return result[0] if result else None

        except Exception as e:
            print(f"CharacterManager.name_to_id: An error occurred while "
                  f"resolving character name '{name}' to ID:\n{e}")
            return None


class ScriptureManager:
    """
    A class for managing scripture-related operations in the database.
        - Add/Update/Delete scripture
        - Add/Update/Remove scripture to/from videos
        - Get scripture (all, assigned to a video)
        - Resolve tag name to ID

    Args:
        db (DatabaseContext):
            An instance of DatabaseContext for database operations.
            This uses a 'composition' approach to manage database interactions.
    """

    def __init__(
        self,
        db: DatabaseContext
    ) -> None:
        """
        Initializes the class with a DatabaseContext instance.
            This uses a 'composition' approach

        Args:
            db (DatabaseContext): An instance of DatabaseContext for
                database operations.

        Returns:
            None
        """

        self.db = db

    def add(
        self,
        book: str,
        chapter: int,
        verse: int,
    ) -> int | None:
        """
        Adds a new scripture to the database.

        Args:
            book (str): The name of the book to be added.
            chapter (int): The chapter number of the scripture.
            verse (int): The verse number of the scripture.

        Returns:
            int | None:
                The ID of the newly added scripture if successful.
                Or None if an error occurs.
        """

        # Check that 'name' is a valid non-empty string
        if not isinstance(book, str) or not book.strip():
            print("ScriptureManager.add: Invalid book name provided.")
            return None

        # Add the entry
        try:
            # Will just ignore it if it already exists
            self.db.cursor.execute(
                """
                INSERT OR IGNORE INTO scriptures (book, chapter, verse)
                VALUES (?, ?, ?)
                """,
                (book, chapter, verse)
            )
            self.db.conn.commit()

            # Get the ID of the scripture,
            #   whether it was just added or already existed
            self.db.cursor.execute(
                """
                SELECT id FROM scriptures
                WHERE book = ? AND chapter = ? AND verse = ?
                """,
                (book, chapter, verse)
            )
            row = self.db.cursor.fetchone()
            scripture_id = row[0] if row else None

        except Exception as e:
            print(
                f"ScriptureManager.add: "
                f"An error occurred while adding the scripture:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return scripture_id

    def update(
        self,
        id: int,
        book: str = "",
        chapter: int = 0,
        verse: int = 0,
    ) -> int | None:
        """
        Updates an existing scripture in the database.
            Identified by its ID, which is immutable.
            Any of the fields can be updated, but at least one
                must be provided.

        Args:
            id (int): The ID of the scripture to update.
            book (str): The new book of the scripture.
            chapter (int): The new chapter number of the scripture.
            verse (int): The new verse number of the scripture.

        Returns:
            int | None:
                The ID of the updated scripture if successful.
                Or None if an error occurs.
        """

        # Build the update statement dynamically
        #   based on provided (non-empty) values
        fields = []
        values = []

        if book:
            fields.append("book = ?")
            values.append(book)
        if chapter:
            fields.append("chapter = ?")
            values.append(chapter)
        if verse:
            fields.append("verse = ?")
            values.append(verse)

        if not fields:
            print("ScriptureManager.update: No fields to update.")
            return None

        # Set up the query
        values.append(id)
        query = f"UPDATE scriptures SET {', '.join(fields)} WHERE id = ?"

        try:
            self.db.cursor.execute(query, tuple(values))

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(
                    f"ScriptureManager.update: "
                    f"No scripture found with ID {id}."
                )
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"ScriptureManager.update: "
                f"An error occurred while updating the scripture:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def delete(
        self,
        id: int,
    ) -> int | None:
        """
        Deletes a scripture from the database.
            Uses the scripture's ID to identify it.

        Args:
            id (int): The ID of the scripture to delete.

        Returns:
            int | None:
                The ID of the deleted scripture if successful.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                "DELETE FROM scriptures WHERE id = ?",
                (id,)
            )

            # Check if any rows were affected
            if self.db.cursor.rowcount == 0:
                print(
                    f"ScriptureManager.delete: "
                    f"No scripture found with ID {id}."
                )
                self.db.conn.rollback()
                return None

            # If good, commit the changes
            self.db.conn.commit()

        except Exception as e:
            print(
                f"ScriptureManager.update: "
                f"An error occurred while updating the scripture:\n{e}"
            )
            self.db.conn.rollback()
            return None

        return id

    def get(
        self,
        id: int | None = None,
    ) -> list[dict] | None:
        """
        Retrieves scriptures from the database.
            - Get a single scripture by a given ID
            - Get all scriptures

        Args:
            id (int | None): The ID of the scripture to retrieve.
                If None, retrieves all scriptures. Defaults to None.

        Returns:
            list[dict] | None:
                A list of dictionaries containing scripture details.
                Or a None if an error occurs.
        """

        # Fetch all
        if id is None:
            query = self.db.cursor.execute("SELECT * FROM scriptures")

        # Fetch a single item by ID
        else:
            query = self.db.cursor.execute(
                "SELECT * FROM scriptures WHERE id = ?",
                (id,)
            )

        # Convert to a list of dictionaries, even for a single item
        try:
            items = [dict(row) for row in query.fetchall()]

        except Exception:
            return None

        return items

    def get_from_video(
        self,
        video_id: int,
    ) -> list[dict] | None:
        """
        Retrieves scriptures associated with a specific video.

        Args:
            video_id (int): The ID of the video for which to
                retrieve scriptures.

        Returns:
            list[dict] | None:
                A list of dictionaries containing scripture details.
                Or None if an error occurs.
        """

        try:
            self.db.cursor.execute(
                """
                SELECT s.* FROM scriptures s
                JOIN videos_scriptures vs ON s.id = vs.scripture_id
                WHERE vs.video_id = ?
                """,
                (video_id,)
            )
            items = [dict(row) for row in self.db.cursor.fetchall()]

        except Exception as e:
            print(f"Error retrieving scriptures for video {video_id}: {e}")
            return None

        return items

    def add_to_video(
        self,
        video_id: int,
        scripture_id: int
    ) -> bool:
        """
        Adds a category to a video in the database.
            Uses the 'videos_scriptures' junction table to associate
            a video with a scripture.

        Args:
            video_id (int): The ID of the video to which the scripture
                will be added.
            scripture_id (int): The ID of the scripture to add to the video.

        Returns:
            bool:
                True if the scripture was successfully added to the video.
                False if an error occurs or the association already exists.
        """

        # Verify video exists
        self.db.cursor.execute(
            "SELECT 1 FROM videos WHERE id = ?", (video_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"Video with ID {video_id} does not exist.")
            return False

        # Verify scripture exists
        self.db.cursor.execute(
            "SELECT 1 FROM scriptures WHERE id = ?", (scripture_id,)
        )
        if not self.db.cursor.fetchone():
            print(f"Scripture with ID {scripture_id} does not exist.")
            return False

        try:
            self.db.cursor.execute(
                """
                INSERT OR
                IGNORE INTO videos_scriptures (video_id, scripture_id)
                VALUES (?, ?)
                """, (video_id, scripture_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error linking a scripture to video: {e}")
            return False

    def remove_from_video(
        self,
        video_id: int,
        scripture_id: int
    ) -> bool:
        """
        Removes a scripture from a video in the database.
            Uses the 'videos_scriptures' junction table to disassociate

        Args:
            video_id (int): The ID of the video from which the scripture
                will be removed.
            scripture_id (int): The ID of the scripture to remove
                from the video.

        Returns:
            bool:
                True if the scripture was successfully removed from the video.
                False if an error occurs or the association does not exist.
        """

        try:
            self.db.cursor.execute(
                """
                DELETE FROM videos_scriptures
                WHERE video_id = ?
                AND scripture_id = ?
                """,
                (video_id, scripture_id)
            )
            self.db.conn.commit()
            return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error unlinking scripture from video: {e}")
            return False

    def name_to_id(
        self,
        book: str,
        chapter: int,
        verse: int
    ) -> int | None:
        """
        Resolve a full scripture to its ID.
            This is a little different from the other managers,
            as there are three parts, not just a name

        Args:
            book (str): The name of the book.
            chapter (int): The chapter number.
            verse (int): The verse number.

        Returns:
            int | None:
                The ID of the tag if found
                None if the tag does not exist.
        """

        # Check that 'book' is a valid non-empty string
        if not isinstance(book, str) or not book.strip():
            print(
                "ScriptureManager.name_to_id: Invalid book name provided."
            )
            return None

        try:
            self.db.cursor.execute(
                """
                SELECT id FROM scriptures
                WHERE book = ? AND chapter = ? AND verse = ?
                """, (book, chapter, verse)
            )
            result = self.db.cursor.fetchone()

            # There should be only one result, or nothing
            return result[0] if result else None

        except Exception as e:
            print(f"ScriptureManager.name_to_id: An error occurred while "
                  f"resolving scripture '{book} {chapter}:{verse}' "
                  f"to ID:\n{e}")
            return None


if __name__ == "__main__":
    print("This is a a class file, and should not be run directly.")
