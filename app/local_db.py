"""
Module: local_mgmt.py

Manages the local user details, such as profiles, watch history, etc.

Classes:
    - LocalDbContext:
        A context manager for handling SQLite database connections.
    - ProfileManager:
        Manages CRUD operations for user profiles in the local database.
    - ProfileManager:
        Manages CRUD operations for user profiles in the local database.

Dependencies:
    - sqlite3: For SQLite database operations.
    - traceback: For handling exceptions and tracebacks.
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

            # Profiles table
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

            # Watch history table
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

            # In progress table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS in_progress_videos (
                    profile_id INTEGER NOT NULL,
                    video_id INTEGER NOT NULL,
                    current_time INTEGER NOT NULL DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (profile_id, video_id),
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

    Args:
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


class ProgressManager:
    """
    Manages CRUD operations for in-progress videos in the local database.
    Works alongside LocalDbContext for database operations.

    Args:
        db (LocalDbContext): The database context for operations.
    """

    def __init__(
        self,
        db: LocalDbContext
    ) -> None:
        """
        Initializes the ProgressManager with the database context.

        Args:
            db (LocalDbContext): The database context for operations.
        """

        self.db = db

    def create(
        self,
        profile_id: int,
        video_id: int,
        current_time: int,
    ) -> bool:
        """
        Adds a video to the in-progress list for a specific profile.

        Args:
            profile_id (int): The ID of the profile.
            video_id (int): The ID of the video.
            current_time (int): The current playback time of the video.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """

        try:
            with self.db.conn:
                cursor = self.db.cursor
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO in_progress_videos (
                        profile_id,
                        video_id,
                        current_time
                    )
                    VALUES (?, ?, ?)
                    """,
                    (profile_id, video_id, current_time)
                )
            self.db.conn.commit()

        except Exception as e:
            logging.error(
                f"[ProgressManager.create] Error adding profile: {e}"
            )
            self.db.conn.rollback()
            return False

        return True

    def read(
        self,
        profile_id: int,
        video_id: int | None = None,
    ) -> list[dict] | None:
        """
        Gets one or more videos from the in-progress list for a profile.

        Args:
            profile_id (int): The ID of the profile.
                Mandatory to retrieve in-progress videos.
            video_id (int | None): The ID of the video to retrieve.
                If None, retrieves all in-progress videos for the profile.

        Returns:
            list[dict] | None: A list of in-progress videos as dictionaries,
                or None if no in-progress videos are found.
        """

        if profile_id is None:
            logging.error(
                """
                [ProfileManager.read]
                Profile ID must be provided to retrieve in-progress videos.
                """
            )
            return None

        # Get all in-progress videos for the profile
        if video_id is None:
            try:
                with self.db.conn:
                    cursor = self.db.cursor
                    cursor.execute(
                        """
                        SELECT * FROM in_progress_videos
                        WHERE profile_id = ?
                        """,
                        (profile_id,)
                    )
                    videos = cursor.fetchall()
                    return [dict(videos) for videos in videos]

            except Exception as e:
                logging.error(
                    f"[ProfileManager.read] "
                    f"Error retrieving in progress videos: {e}"
                )
                return None

        # Get a specific in-progress video for the profile
        else:
            try:
                with self.db.conn:
                    cursor = self.db.cursor
                    cursor.execute(
                        """
                        SELECT * FROM in_progress_videos
                        WHERE profile_id = ? AND video_id = ?
                        """,
                        (profile_id, video_id,)
                    )
                    video = cursor.fetchone()
                    return [dict(video)] if video else None

            except Exception as e:
                logging.error(
                    f"[ProfileManager.read] Error retrieving video "
                    f"{video_id}: {e}"
                )
                return None

    def update(
        self,
        profile_id: int,
        video_id: int,
        current_time: int,
    ) -> bool:
        """
        Updates an in-progress entry.

        Args:
            profile_id (int): The ID of the profile.
            video_id (int): The ID of the video to update.
            current_time (int): The current playback time of the video.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """

        if profile_id is None or video_id is None or current_time is None:
            logging.error(
                """
                [ProfileManager.update] Profile and video IDs,
                and a current time, must be provided for update.
                """
            )
            return None

        # Check the entry exists before updating
        try:
            result = self.read(profile_id, video_id)
            if not result:
                logging.error(
                    f"[ProfileManager.update] No in-progress entry found "
                    f"for video {video_id} on profile {profile_id}."
                )
                return False

        except Exception as e:
            logging.error(
                f"[ProfileManager.update] Error checking in-progress entry "
                f"for video {video_id} on profile {profile_id}: {e}"
            )
            return False

        # Update the in-progress entry
        try:
            with self.db.conn:
                cursor = self.db.cursor
                cursor.execute(
                    """
                    UPDATE in_progress_videos
                    SET current_time = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE profile_id = ? AND video_id = ?
                    """,
                    (current_time, profile_id, video_id)
                )

        except Exception as e:
            logging.error(
                f"[ProfileManager.update] Error updating progress on video "
                f"{video_id} for profile {profile_id}: {e}"
            )
            return False

        return True

    def delete(
        self,
        profile_id: int,
        video_id: int,
    ) -> int | None:
        """
        Delete an in-progress entry.

        Args:
            profile_id (int): The ID of the profile.
            video_id (int): The ID of the video to delete.

        Returns:
            int | None: The ID of the deleted in-progress entry,
        """

        if profile_id is None or video_id is None:
            logging.error(
                """
                [ProfileManager.delete] Profile and video IDs must be
                provided for deletion.
                """
            )
            return None

        try:
            with self.db.conn:
                cursor = self.db.cursor
                cursor.execute(
                    """
                    DELETE FROM in_progress_videos
                    WHERE profile_id = ? AND video_id = ?
                    """,
                    (profile_id, video_id)
                )
                self.db.conn.commit()
                return cursor.rowcount > 0

        except Exception as e:
            logging.error(
                f"[ProfileManager.update] Error deleting in progress entry "
                f" for video {video_id} on profile {profile_id}: {e}"
            )
            self.db.conn.rollback()
            return None
