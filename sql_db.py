"""
Module: db.py

This module provides a DatabaseManager class for managing a SQLite database

classes:
    DatabaseManager: A context manager for handling SQLite database operations.

Tables:
    - categories: Stores video categories.
    - videos: Stores video details including name, filename, category,
        description, tags, thumbnail, duration, watched status.

Categories Schema:
    - id (INTEGER): Primary key, auto-incremented.
    - name (TEXT): Unique name of the category.
    - main_area (TEXT): Field for additional categorization.

Videos Schema:
    - id (INTEGER): Primary key, auto-incremented.
    - name (TEXT): Unique name of the video.
    - url_1080 (TEXT): URL for the video in 1080p.
    - url_720 (TEXT): URL for the video in 720p.
    - url_480 (TEXT): URL for the video in 480p.
    - url_360 (TEXT): URL for the video in 360p.
    - url_240 (TEXT): URL for the video in 240p.
    - description (TEXT): Description of the video.
    - thumbnail (TEXT): URL or path to the video's thumbnail.
    - duration (INTEGER): Duration of the video in seconds.
    - url (TEXT): Main URL for the video.

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
            description (str): A description of the video. Defaults to "".
            url (str): The main URL for the video. Defaults to "".
            url_1080 (str): URL for the video in 1080p. Defaults to "".
            url_720 (str): URL for the video in 720p. Defaults to "".
            url_480 (str): URL for the video in 480p. Defaults to "".
            url_360 (str): URL for the video in 360p. Defaults to "".
            url_240 (str): URL for the video in 240p. Defaults to "".
            thumbnail (str): URL or path to the video's thumbnail. Defaults to "".
            duration (int): Duration of the video in seconds. Defaults to 0.
            date_added (str): The date the video was added. Defaults to "".

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
            self.db.cursor.execute(
                "INSERT INTO categories (name) VALUES (?)",
                (name,)
            )
            category_id = self.db.cursor.lastrowid
            self.db.conn.commit()

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
                print(f"CategoryManager.update: No category found with ID {id}.")
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
                print(f"CategoryManager.delete: No category found with ID {id}.")
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
            video_id (int): The ID of the video to which the category will be added.
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
            video_id (int): The ID of the video from which the category will be removed.
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
            self.db.cursor.execute(
                "INSERT INTO tags (name) VALUES (?)",
                (name,)
            )
            tag_id = self.db.cursor.lastrowid
            self.db.conn.commit()

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
            "SELECT 1 FROM categories WHERE id = ?", (tag_id,)
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
            video_id (int): The ID of the video from which the tag will be removed.
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
            self.db.cursor.execute(
                "INSERT INTO speakers (name) VALUES (?)",
                (name,)
            )
            speaker_id = self.db.cursor.lastrowid
            self.db.conn.commit()

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
            "SELECT 1 FROM categories WHERE id = ?", (speaker_id,)
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
            video_id (int): The ID of the video from which the speaker will be removed.
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
            self.db.cursor.execute(
                "INSERT INTO bible_characters (name) VALUES (?)",
                (name,)
            )
            character_id = self.db.cursor.lastrowid
            self.db.conn.commit()

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
            video_id (int): The ID of the video to which the character will be added.
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
            "SELECT 1 FROM categories WHERE id = ?", (character_id,)
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
            self.db.cursor.execute(
                """
                INSERT INTO scriptures (book, chapter, verse)
                VALUES (?, ?, ?)
                """,
                (book, chapter, verse)
            )
            scripture_id = self.db.cursor.lastrowid
            self.db.conn.commit()

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
                print(f"ScriptureManager.update: No scripture found with ID {id}.")
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
                print(f"ScriptureManager.delete: No scripture found with ID {id}.")
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
            "SELECT 1 FROM categories WHERE id = ?", (scripture_id,)
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


class DatabaseManager:
    """
    A context manager for handling SQLite database operations.
    """

    def __init__(
        self,
        db_path: str = "videos.db"
    ) -> None:
        """
        Initializes the DatabaseManager with a database path.

        Args:
            db_path (str): The path to the SQLite database file.
                Defaults to "videos.db".

        Returns:
            None
        """

        # Set the database path and connect to the database
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def __enter__(
        self
    ) -> "DatabaseManager":
        """
        Start the context manager and return the instance.

        Args:
            None

        Returns:
            DatabaseManager: The instance of the DatabaseManager.
        """

        return self

    def __exit__(
        self,
        exc_type: type,
        exc_value: Exception,
        traceback: traceback.TracebackException
    ) -> None:
        """
        Exit the context manager, handling any exceptions.

        Args:
            exc_type (type): The type of the exception raised.
            exc_value (Exception): The exception instance.
            traceback (traceback.TracebackException): The traceback object.

        Returns:
            None
        """

        # Commit any changes and close the connection
        self.conn.commit()
        self.conn.close()

    def _get_category_id_by_name(
        self,
        name: str
    ) -> int | None:
        """
        Retrieve the ID of a category by its name.

        Args:
            name (str): The name of the category.

        Returns:
            int | None: The ID of the category if found, otherwise None.
        """

        self.c.execute(
            "SELECT id FROM categories WHERE name = ?",
            (name,)
        )
        result = self.c.fetchone()

        return result[0] if result else None

    def get_video_id_by_name(
        self,
        name: str
    ) -> int | None:
        """
        Retrieve the ID of a video by its name.

        Args:
            name (str): The name of the video.

        Returns:
            int | None: The ID of the video if found, otherwise None.
        """

        self.c.execute(
            "SELECT id FROM videos WHERE name = ?",
            (name,)
        )
        result = self.c.fetchone()

        return result[0] if result else None

    def get_category_name_by_id(
        self,
        category_id: int
    ) -> str | None:
        """
        Retrieve the name of a category by its ID.

        Args:
            category_id (int): The ID of the category.

        Returns:
            str | None: The name of the category if found, otherwise None.
        """

        self.c.execute(
            "SELECT name FROM categories WHERE id = ?",
            (category_id,)
        )
        result = self.c.fetchone()

        return result[0] if result else None

    def add_category(
        self,
        name: str,
        main_area: str,
    ) -> tuple[str, str]:
        """
        Add a new category to the categories table.

        Args:
            name (str): The name of the category to be added.

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        # Write the SQL command to insert a new category
        try:
            self.c.execute(
                "INSERT INTO categories (name, main_area) VALUES (?, ?)",
                (name, main_area)
            )
            self.conn.commit()

        # Handle integrity errors, such as duplicate category names
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            return (
                "error",
                f"Category '{name}' already exists.\n{e}"
            )

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while adding the category.\n{e}"
            )

        return (
            "success",
            "Added category successfully."
        )

    def delete_category(
        self,
        category_id: int
    ) -> tuple[str, str]:
        """
        Delete a category from the categories table by its ID.

        Args:
            category_id (int): The ID of the category to be deleted.

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        try:
            self.c.execute(
                "DELETE FROM categories WHERE id = ?",
                (category_id,)
            )
            self.conn.commit()

        except sqlite3.IntegrityError:
            self.conn.rollback()
            return (
                "error",
                f"Cannot delete category with ID {category_id} because it is "
                "referenced by one or more linked videos."
            )

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while deleting the category."
                f"\n{e}"
            )

        return (
            "success",
            f"Deleted category with ID {category_id} successfully."
        )

    def get_categories(
        self
    ) -> list[dict]:
        """
        Retrieve all categories from the categories table.

        Args:
            None

        Returns:
            list: A list of dicts, each containing the ID and name
                of a category.
        """

        self.c.execute("SELECT * FROM categories")
        rows = self.c.fetchall()

        # Convert each row to a dictionary for easier access
        return [dict(row) for row in rows]

    def add_video(
        self,
        name: str,
        url: str = "",
        url_1080: str = "",
        url_720: str = "",
        url_480: str = "",
        url_360: str = "",
        url_240: str = "",
        category_name: str = None,
        description: str = "",
        thumbnail: str = "",
        duration: int = 0,
        date_added: str = None,
    ) -> tuple[str, str]:
        """
        Add a new video to the videos table.

        Args:
            name (str): The name of the video.
            url (str): The main URL for the video.
            url_1080 (str, optional): URL for the video in 1080p.
            url_720 (str, optional): URL for the video in 720p.
            url_480 (str, optional): URL for the video in 480p.
            url_360 (str, optional): URL for the video in 360p.
            url_240 (str, optional): URL for the video in 240p.
            category (int): The category the video belongs to.
            description (str, optional): A description of the video.
                Defaults to an empty string.
            thumbnail (str, optional): URL or path to the video's thumbnail.
                Defaults to an empty string.
            duration (int, optional): Duration of the video in seconds.
                Defaults to 0.
            date_added (str, optional): The date the video was added.

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        # Insert the video into the videos table
        try:
            self.c.execute(
                """
                INSERT INTO videos (
                    name, url, url_1080, url_720, url_480, url_360, url_240,
                    description, thumbnail, duration, date_added
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    url,
                    url_1080, url_720, url_480, url_360, url_240,
                    description,
                    thumbnail,
                    duration,
                    date_added,
                )
            )
            video_id = self.c.lastrowid

            # Link to category if provided
            if category_name:
                category_id = self._get_category_id_by_name(category_name)
                if category_id is None:
                    self.conn.rollback()
                    return (
                        "error",
                        f"Category '{category_name}' does not exist."
                    )

                self.c.execute(
                    """
                    INSERT OR IGNOREINTO video_categories (
                        video_id,
                        category_id
                    ) VALUES (?, ?)
                    """,
                    (video_id, category_id)
                )

            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while adding the video: {e}"
            )

        return (
            "success",
            "Added video successfully."
        )

    def delete_video(
        self,
        *,
        video_id: int = None,
        video_name: str = None
    ) -> None:
        """
        Delete a video from the videos table by its ID or name.

        Args:
            video_id (int, optional): The ID of the video to be deleted.
                Defaults to None.
            video_name (str, optional): The name of the video to be deleted.
                Defaults to None.

        Returns:
            None: If the video is successfully deleted.
        """

        # Check at least one of video_id or video_name is provided
        if video_id is None and video_name is None:
            return (
                "error",
                "Either video_id or video_name must be provided"
            )

        # If we have a name but no ID, get the ID from the name
        elif video_id is None and video_name is not None:
            # Get the video ID by name
            if video_id is None:
                return (
                    "error",
                    f"Video '{video_name}' does not exist."
                )

        # Now we can safely delete the video by ID
        try:
            self.c.execute("DELETE FROM videos WHERE id = ?", (video_id,))

            # Check how many rows were affected
            if self.c.rowcount == 0:
                return (
                    "error",
                    f"Video with ID {video_id} does not exist."
                )

            self.conn.commit()

        except sqlite3.IntegrityError:
            self.conn.rollback()
            return (
                "error",
                f"Cannot delete video with ID {video_id} because it is "
                "referenced by one or more categories."
            )

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while deleting the video."
                f"\n{e}"
            )

        return (
            "success",
            f"Deleted video with ID {video_id} successfully."
        )

    def get_videos(
        self,
        *,
        category_id: int = None,
        category_name: str = None,
    ) -> list[dict] | tuple[str, str]:
        """
        Retrieve all videos from the videos table, optionally filtered
            by category.

        Either category_id or category_name can be provided to filter
            videos by a specific category.
        If neither is provided, all videos are retrieved.
        If both are provided, category_id takes precedence.

        Args:
            category_id (int, optional): The ID of the category to filter
                videos by. If None, retrieves all videos. Defaults to None.
            category_name (str, optional): The name of the category to filter
                videos by. If None, retrieves all videos. Defaults to None.

        Returns:
            list: A list of dicts, each containing the details of a video.
        """

        # Convert category_name to category_id if ID is not provided
        if category_id is None and category_name is not None:
            category_id = self._get_category_id_by_name(category_name)

        # Get videos based on category_id
        try:
            if category_id is not None:
                query = self.c.execute(
                    """
                    SELECT v.*
                    FROM videos v
                    JOIN video_categories vc ON v.id = vc.video_id
                    WHERE vc.category_id = ?
                    """,
                    (category_id,)
                )
            else:
                query = self.c.execute("SELECT * FROM videos")
        except Exception as e:
            return (
                "error",
                f"An unexpected error occurred while retrieving videos: {e}"
            )

        # Fetch all videos, converting each row to a dict
        try:
            videos = [dict(row) for row in query.fetchall()]

        except Exception as e:
            return (
                "error",
                f"An unexpected error occurred while fetching videos: {e}"
            )

        return videos

    def get_video_by_id(
        self,
        video_id: int
    ) -> dict | None:
        """
        Retrieve video details by its ID.

        Args:
            video_id (int): The ID of the video.

        Returns:
            dict | None: A dictionary containing video details if found,
                otherwise None.
        """

        self.c.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
        row = self.c.fetchone()

        # Convert the 'tags' key from a comma-separated string to a list
        video = dict(row) if row else None

        return video

    def add_tag(
        self,
        tag: str,
        video_id: int,
    ) -> tuple[str, str]:
        """
        Adds a tag:
            Tag definition in the tags table.
            Links the tag to a video in the videos_tags table.

        Args:
            tag (str): A tag name to be added.
            video_id (int): The ID of the video to which the tags
                will be added.

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        try:
            self.c.execute(
                "INSERT OR IGNORE INTO tags (name) VALUES (?)",
                (tag,)
            )
            self.conn.commit()

            # Retrieve the tag ID
            self.c.execute(
                "SELECT id FROM tags WHERE name = ?",
                (tag,)
            )
            tag_id = self.c.fetchone()[0]

            # Insert into the videos_tags join table
            self.c.execute(
                """
                INSERT OR IGNORE INTO videos_tags (video_id, tag_id)
                VALUES (?, ?)
                """,
                (video_id, tag_id)
            )
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while adding the tag "
                f"'{tag}'.\n{e}"
            )

        return (
            "success",
            f"Added tag '{tag}' and linked it to video ID {video_id}."
        )

    def get_tags_by_video_id(
        self,
        video_id: int,
    ) -> list[dict]:
        """
        Retrieve tags from the tags table for a video.

        Args:
            video_id (int): The ID of the video for which to retrieve tags.

        Returns:
            list: A list of dicts, each containing the ID and name of a tag.
        """

        self.c.execute("""
            SELECT t.id, t.name
            FROM tags t
            JOIN videos_tags vt ON t.id = vt.tag_id
            WHERE vt.video_id = ?
        """, (video_id,))
        rows = self.c.fetchall()

        # Convert each row to a dictionary for easier access
        return [dict(row) for row in rows]

    def add_speaker(
        self,
        speaker: str,
        video_id: int,
    ) -> tuple[str, str]:
        """
        Adds a speaker:
            Add definition in the speakers table.
            Links the speaker to a video in the videos_speakers table.

        Args:
            speaker (str): A speaker name to be added.
            video_id (int): The ID of the video to which the speaker
                will be added.

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        try:
            self.c.execute(
                "INSERT OR IGNORE INTO speakers (name) VALUES (?)",
                (speaker,)
            )
            self.conn.commit()

            # Retrieve the speakers ID
            self.c.execute(
                "SELECT id FROM speakers WHERE name = ?",
                (speaker,)
            )
            tag_id = self.c.fetchone()[0]

            # Insert into the videos_tags join table
            self.c.execute(
                """
                INSERT OR IGNORE INTO videos_speakers (video_id, speaker_id)
                VALUES (?, ?)
                """,
                (video_id, tag_id)
            )
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while adding the speaker "
                f"'{speaker}'.\n{e}"
            )

        return (
            "success",
            f"Added speaker '{speaker}' and linked them to video {video_id}."
        )

    def get_speakers_by_video_id(
        self,
        video_id: int,
    ) -> list[dict]:
        """
        Retrieve speakers from the speakers table for a video

        Args:
            video_id (int): The ID of the video for which to retrieve speakers.

        Returns:
            list: A list of dicts, each containing the ID and
                name of a speaker.
        """

        self.c.execute("""
            SELECT t.id, t.name
            FROM speakers t
            JOIN videos_speakers vt ON t.id = vt.speaker_id
            WHERE vt.video_id = ?
        """, (video_id,))
        rows = self.c.fetchall()

        # Convert each row to a dictionary for easier access
        return [dict(row) for row in rows]

    def add_character(
        self,
        character: str,
        video_id: int,
    ) -> tuple[str, str]:
        """
        Adds a character:
            Add definition in the characters table.
            Links the character to a video in the
                videos_bible_characters table.

        Args:
            character (str): A character name to be added.
            video_id (int): The ID of the video to which the character
                will be added.

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        try:
            self.c.execute(
                "INSERT OR IGNORE INTO bible_characters (name) VALUES (?)",
                (character,)
            )
            self.conn.commit()

            # Retrieve the character ID
            self.c.execute(
                "SELECT id FROM bible_characters WHERE name = ?",
                (character,)
            )
            character_id = self.c.fetchone()[0]

            # Insert into the videos_bible_characters join table
            self.c.execute(
                """
                INSERT OR IGNORE INTO videos_bible_characters (
                    video_id,
                    character_id
                )
                VALUES (?, ?)
                """,
                (video_id, character_id)
            )
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while adding the character "
                f"'{character}'.\n{e}"
            )

        return (
            "success",
            f"Added character '{character}' and linked them "
            f"to video ID {video_id}."
        )

    def get_characters_by_video_id(
        self,
        video_id: int,
    ) -> list[dict]:
        """
        Retrieve characters from the characters table for a video

        Args:
            video_id (int): The ID of the video for which to
                retrieve characters.

        Returns:
            list: A list of dicts, each containing the ID and
                name of a character.
        """

        self.c.execute("""
            SELECT t.id, t.name
            FROM bible_characters t
            JOIN videos_bible_characters vt ON t.id = vt.character_id
            WHERE vt.video_id = ?
        """, (video_id,))
        rows = self.c.fetchall()

        # Convert each row to a dictionary for easier access
        return [dict(row) for row in rows]

    def add_scripture_by_video_id(
        self,
        book: str,
        chapter: int,
        verse: int,
        video_id: int,
    ) -> tuple[str, str]:
        """
        Adds a scripture:
            Add definition in the scriptures table.
            Links the scripture to a video in the videos_scriptures table.

        Args:
            book (str): The bible book name.
            chapter (int): The chapter number.
            verse (int): The verse number.
            video_id (int): The ID of the video to which the scripture
                will be added.

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        try:
            self.c.execute(
                """
                INSERT OR IGNORE INTO scriptures (book, chapter, verse)
                VALUES (?, ?, ?)
                """,
                (book, chapter, verse)
            )
            self.conn.commit()

            # Retrieve the scripture ID
            self.c.execute(
                """
                SELECT id
                FROM scriptures
                WHERE book = ? AND chapter = ? AND verse = ?
                """,
                (book, chapter, verse)
            )
            scripture_id = self.c.fetchone()[0]

            # Insert into the videos_scriptures join table
            self.c.execute(
                """
                INSERT OR IGNORE INTO videos_scriptures (
                    video_id,
                    scripture_id
                )
                VALUES (?, ?)
                """,
                (video_id, scripture_id)
            )
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while adding the scripture "
                f"'{book} {chapter}:{verse}'.\n{e}"
            )

        return (
            "success",
            f"Added scripture '{book} {chapter}:{verse}' and linked "
            f"them to video {video_id}."
        )

    def get_scriptures_by_video_id(
        self,
        video_id: int,
    ) -> list[dict]:
        """
        Retrieve scriptures from the scriptures table for a video.

        Args:
            video_id (int): The ID of the video for which to
                retrieve scriptures.

        Returns:
            list: A list of dicts, each containing the ID and
                details of a scripture.
        """

        self.c.execute("""
            SELECT t.id, t.book, t.chapter, t.verse
            FROM scriptures t
            JOIN videos_scriptures vt ON t.id = vt.scripture_id
            WHERE vt.video_id = ?
        """, (video_id,))
        rows = self.c.fetchall()

        # Convert each row to a dictionary for easier access
        return [dict(row) for row in rows]

    def add_category_to_video(
        self,
        video_id: int,
        category_id: int
    ) -> tuple[str, str]:
        """
        Link a category to a video in the video_categories table.

        Args:
            video_id (int): The ID of the video to which the category
                will be linked.
            category_id (int): The

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        try:
            self.c.execute(
                """
                INSERT OR IGNORE INTO video_categories (
                    video_id,
                    category_id
                ) VALUES (?, ?)
                """,
                (video_id, category_id)
            )
            self.conn.commit()
            return ("success", "Category linked to video.")

        except Exception as e:
            self.conn.rollback()
            return ("error", f"Failed to link category: {e}")

    def remove_category_from_video(
        self,
        video_id: int,
        category_id: int
    ) -> tuple[str, str]:
        """
        Unlink a category from a video in the video_categories table.

        Args:
            video_id (int): The ID of the video from which the category
                will be unlinked.
            category_id (int): The

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        try:
            self.c.execute(
                """
                DELETE FROM video_categories
                WHERE video_id = ?
                AND category_id = ?
                """,
                (video_id, category_id)
            )
            self.conn.commit()
            return ("success", "Category unlinked from video.")

        except Exception as e:
            self.conn.rollback()
            return ("error", f"Failed to unlink category: {e}")

    def get_categories_by_video_id(
        self,
        video_id: int
    ) -> list[dict]:
        """
        Retrieve categories linked to a video by its ID.

        Args:
            video_id (int): The ID of the video for which to
                retrieve categories.

        Returns:
            list: A list of dicts, each containing the ID and name
                of a category.
        """

        self.c.execute("""
            SELECT c.id, c.name
            FROM categories c
            JOIN video_categories vc ON c.id = vc.category_id
            WHERE vc.video_id = ?
        """, (video_id,))

        return [dict(row) for row in self.c.fetchall()]


if __name__ == "__main__":
    print("This is a a class file, and should not be run directly.")
