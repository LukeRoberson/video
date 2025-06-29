"""
Module: local_mgmt.py

Manages the local user details, such as profiles, watch history, etc.
"""

import sqlite3
import traceback
import logging
from datetime import datetime


DB_NAME = "local.db"


class LocalDbContext:
    """
    A context manager for handling SQLite database connections.
    This class can be used alonside other database operations classes.

    Args:
        db_path (str): The path to the SQLite database file.
    """

    def __init__(
        self,
        db_path: str = "local.db"
    ) -> None:
        """
        Initializes the DatabaseContext with a database path.
        """

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_db()

    def __enter__(
        self
    ) -> "LocalDbContext":
        """
        Start the context manager and return the instance.

        Args:
            None

        Returns:
            LocalDbContext: The instance of the DatabaseContext.
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

    def _create_db(
        self,
    ):
        """
        Creates the local database
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    image TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS watch_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id INTEGER NOT NULL,
                    video_id INTEGER NOT NULL,
                    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (profile_id) REFERENCES profiles(id)
                )
                """
            )
            conn.commit()
            logging.info("Database created or already exists.")


class ProfileManager:
    """
    Manages CRUD operations for user profiles in the local database.
    Works alongside LocalDbContext for database operations.

    Attributes:
        db_path (str): Path to the SQLite database file.
    """

    def __init__(
        self,
        db: LocalDbContext
    ) -> None:
        """
        Initializes the LocalManager with the path to the SQLite database.
        Creates the database if it does not exist.

        Args:
            db_path (str): Path to the SQLite database file.
        """

        self.db = db

    def create(
        self,
        name: str,
        image: str,
    ) -> int | None:
        """
        Adds a new profile to the database.

        Args:
            name (str): The name of the profile.
            image (str): The image associated with the profile.

        Returns:
            int: The ID of the newly created profile.
        """

        try:
            with self.db.conn:
                cursor = self.db.cursor
                cursor.execute(
                    "INSERT INTO profiles (name, image) VALUES (?, ?)",
                    (name, image)
                )
            profile_id = self.db.cursor.lastrowid
            self.db.conn.commit()

        except Exception as e:
            logging.error(f"Error adding profile: {e}")
            self.db.conn.rollback()
            return -1

        return profile_id

    def read(
        self,
        profile_id: int | None = None,
    ) -> list[dict] | None:
        """
        Retrieves a profile from the database by its ID.

        Args:
            profile_id (int | None): The ID of the profile to retrieve.
                If None, retrieves all profiles.

        Returns:
            list[dict] | None:
                A list of profiles (one or all) as dictionaries,
                or None if no profiles are found.
        """

        if profile_id is None:
            try:
                with self.db.conn:
                    cursor = self.db.cursor
                    cursor.execute("SELECT * FROM profiles")
                    profiles = cursor.fetchall()
                    return [dict(profile) for profile in profiles]

            except Exception as e:
                logging.error(f"Error retrieving profiles: {e}")
                return None

        else:
            try:
                with self.db.conn:
                    cursor = self.db.cursor
                    cursor.execute(
                        "SELECT * FROM profiles WHERE id = ?",
                        (profile_id,)
                    )
                    profile = cursor.fetchone()
                    return [dict(profile)] if profile else None

            except Exception as e:
                logging.error(f"Error retrieving profile {profile_id}: {e}")
                return None

    def update(
        self,
        profile_id: int | None = None,
        name: str | None = None,
    ) -> int | None:
        """
        Updates an existing profile in the database.
        Multiple fields can be updated, but at least one must be provided.
            If a field is None, it will not be updated.

        Args:
            profile_id (int | None): The ID of the profile to update.
            name (str | None): The new name for the profile.

        Returns:
            int | None: The ID of the updated profile, or None if not found.
        """

        if profile_id is None:
            logging.error("Profile ID must be provided for update.")
            return None

        try:
            with self.db.conn:
                cursor = self.db.cursor
                updates = []
                params = []

                if name is not None:
                    updates.append("name = ?")
                    params.append(name)

                if not updates:
                    logging.error("No fields to update.")
                    return None

                params.append(profile_id)
                update_query = (
                    f"UPDATE profiles SET {', '.join(updates)} WHERE id = ?"
                )
                cursor.execute(update_query, params)
                self.db.conn.commit()

        except Exception as e:
            logging.error(f"Error updating profile {profile_id}: {e}")
            self.db.conn.rollback()
            return None

        return profile_id

    def delete(
        self,
        profile_id: int | None = None,
    ) -> int | None:
        """
        Deletes a profile from the database.

        Args:
            profile_id (int | None): The ID of the profile to delete.

        Returns:
            int | None: The ID of the deleted profile, or None if not found.
        """

        if profile_id is None:
            logging.error("Profile ID must be provided for deletion.")
            return None

        try:
            with self.db.conn:
                cursor = self.db.cursor
                cursor.execute(
                    "DELETE FROM profiles WHERE id = ?",
                    (profile_id,)
                )
                self.db.conn.commit()

        except Exception as e:
            logging.error(f"Error deleting profile {profile_id}: {e}")
            self.db.conn.rollback()
            return None

        return profile_id

    def mark_watched(
        self,
        profile_id: int,
        video_id: int
    ) -> bool:
        """
        Marks a video as watched for a specific profile.

        Args:
            profile_id (int): The ID of the profile.
            video_id (int): The ID of the video to mark as watched.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """

        try:
            with self.db.conn:
                cursor = self.db.cursor
                cursor.execute(
                    """
                    INSERT INTO watch_history (
                        profile_id,
                        video_id,
                        watched_at
                    )
                    VALUES (
                        ?,
                        ?,
                        ?
                    )
                    """,
                    (
                        profile_id,
                        video_id,
                        datetime.now()
                    )
                )
                self.db.conn.commit()
                return True

        except Exception as e:
            logging.error(
                f"Error marking video {video_id} as watched for "
                f"profile {profile_id}: {e}"
            )
            self.db.conn.rollback()
            return False

    def mark_unwatched(
        self,
        profile_id: int,
        video_id: int
    ) -> bool:
        """
        Marks a video as unwatched for a specific profile.

        Args:
            profile_id (int): The ID of the profile.
            video_id (int): The ID of the video to mark as unwatched.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """

        try:
            with self.db.conn:
                cursor = self.db.cursor
                cursor.execute(
                    """
                    DELETE FROM watch_history
                    WHERE profile_id = ? AND video_id = ?
                    """,
                    (profile_id, video_id)
                )
                self.db.conn.commit()
                return True

        except Exception as e:
            logging.error(
                f"Error marking video {video_id} as unwatched for "
                f"profile {profile_id}: {e}"
            )
            self.db.conn.rollback()
            return False

    def check_watched(
        self,
        profile_id: int,
        video_id: int,
    ) -> bool:
        """
        Checks if a video has been watched by a specific profile.

        Args:
            profile_id (int): The ID of the profile.
            video_id (int): The ID of the video to check.

        Returns:
            bool: True if the video has been watched, False otherwise.
        """

        try:
            with self.db.conn:
                cursor = self.db.cursor
                cursor.execute(
                    """
                    SELECT 1 FROM watch_history
                    WHERE profile_id = ? AND video_id = ?
                    """,
                    (profile_id, video_id)
                )
                return cursor.fetchone() is not None

        except Exception as e:
            logging.error(
                f"Error checking if video {video_id} is watched for "
                f"profile {profile_id}: {e}"
            )
            return False
