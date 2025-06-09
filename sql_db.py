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
    - category_id (INTEGER): Foreign key referencing categories(id).
    - description (TEXT): Description of the video.
    - tags (TEXT): Comma-separated tags associated with the video.
    - thumbnail (TEXT): URL or path to the video's thumbnail.
    - duration (INTEGER): Duration of the video in seconds.
    - watched (BOOLEAN): Whether the video has been watched (default is 0).

A video may have more than one URL for different resolutions.
    They may not all be available

Dependencies:
    - sqlite3: For SQLite database operations.
"""


import sqlite3
import traceback


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

    def create_category_table(
        self
    ) -> tuple[str, str]:
        """
        Create the categories table: Stores video categories.

        Schema:
            - id (INTEGER): Primary key, auto-incremented.
            - name (TEXT): Unique name of the category.
            - main_area (TEXT): Field for additional categorization.

        Args:
            None

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        # Create categories table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    main_area TEXT NOT NULL
                );
            """)
            self.conn.commit()

        except sqlite3.OperationalError as e:
            self.conn.rollback()
            return (
                "error",
                f"An error occurred while creating the categories: {e}"
            )

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the categories "
                f"table: {e}"
            )

        return (
            "success",
            "Created categories table successfully."
        )

    def create_video_table(
        self
    ) -> tuple[str, str]:
        """
        Create tables for storing video details.
            This is the main table for storing video information.

        Videos table:
            id, name, url_1080, url_720, url_480, url_360, url_240,
            category_id, description, thumbnail, duration, date_added

        Args:
            None

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        # Create videos table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    url_1080 TEXT,
                    url_720 TEXT,
                    url_480 TEXT,
                    url_360 TEXT,
                    url_240 TEXT,
                    category_id INTEGER NOT NULL,
                    description TEXT,
                    thumbnail TEXT,
                    duration INTEGER,
                    date_added TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                );
            """)
            self.conn.commit()

        except sqlite3.OperationalError as e:
            self.conn.rollback()
            return (
                "error",
                f"An error occurred while creating the videos table."
                f"\n{e}"
            )

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the videos "
                f"table: {e}"
            )

        return (
            "success",
            "Created tables successfully."
        )

    def create_meta_tables(
        self
    ) -> tuple[str, str]:
        """
        Create several tables for storing metadata related to videos.
            - Tags table: Stores tags for videos.
            - Speakers table: Stores speaker names.
            - Scriptures table: Stores scripture references.
            - Bible characters table: Stores names of Bible characters.

        Speakers table:
            id, name

        Scriptures table:
            id, reference

        Bible characters table:
            id, name

        Args:
            None

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        # Create tags table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );
            """)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the tags "
                f"table: {e}"
            )

        # Create speakers table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS speakers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );
            """)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the videos "
                f"table: {e}"
            )

        # Create scriptures table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS scriptures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book TEXT NOT NULL,
                    chapter INTEGER NOT NULL,
                    verse INTEGER NOT NULL,
                    UNIQUE(book, chapter, verse)
                );
            """)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the videos "
                f"table: {e}"
            )

        # Create bible characters table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS bible_characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );
            """)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the videos "
                f"table: {e}"
            )

        return (
            "success",
            "Created tables successfully."
        )

    def create_join_tables(
        self
    ) -> tuple[str, str]:
        """
        Create tables for joining videos with metadata
            Links videos to tags, speakers, scriptures, and Bible characters.

        Videos_Speakers table:
            video_id, speaker_id

        Videos_Scriptures table:
            video_id, scripture_id

        Videos_Bible_Characters table:
            video_id, character_id

        Videos_Tags table:
            video_id, tag_id

        Args:
            None

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        # Create Video-Tags table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS videos_tags (
                    video_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES videos(id),
                    FOREIGN KEY (tag_id) REFERENCES tags(id),
                    PRIMARY KEY (video_id, tag_id)
                );
            """)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the videos "
                f"table: {e}"
            )

        # Create Video-Speakers table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS videos_speakers (
                    video_id INTEGER NOT NULL,
                    speaker_id INTEGER NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES videos(id),
                    FOREIGN KEY (speaker_id) REFERENCES speakers(id),
                    PRIMARY KEY (video_id, speaker_id)
                );
            """)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the videos "
                f"table: {e}"
            )

        # Create Video-Scriptures table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS videos_scriptures (
                    video_id INTEGER NOT NULL,
                    scripture_id INTEGER NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES videos(id),
                    FOREIGN KEY (scripture_id) REFERENCES scriptures(id),
                    PRIMARY KEY (video_id, scripture_id)
                );
            """)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the videos "
                f"table: {e}"
            )

        # Create Video-Bible_Characters table
        try:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS videos_bible_characters (
                    video_id INTEGER NOT NULL,
                    character_id INTEGER NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES videos(id),
                    FOREIGN KEY (character_id) REFERENCES bible_characters(id),
                    PRIMARY KEY (video_id, character_id)
                );
            """)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            return (
                "error",
                f"An unexpected error occurred while creating the videos "
                f"table: {e}"
            )

        return (
            "success",
            "Created tables successfully."
        )

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
                "referenced by one or more videos."
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

        # Get the category ID by name
        category_id = self._get_category_id_by_name(category_name)
        if category_id is None:
            return ("error", f"Category '{category_name}' does not exist.")

        # Insert the video into the videos table
        try:
            self.c.execute(
                """
                INSERT INTO videos (
                    name, url_1080, url_720, url_480, url_360, url_240,
                    category_id, description, thumbnail,
                    duration, date_added
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    url_1080, url_720, url_480, url_360, url_240,
                    category_id,
                    description,
                    thumbnail,
                    duration,
                    date_added,
                )
            )
            self.conn.commit()

        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            return (
                "error",
                f"An error occurred while adding the video: {e}"
            )

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
            if category_name is not None:
                category_id = self._get_category_id_by_name(category_name)

        # Get videos based on category_id
        if category_id is not None:
            try:
                query = self.c.execute(
                    "SELECT * FROM videos WHERE category_id = ?",
                    (category_id,)
                )

            except Exception as e:
                return (
                    "error",
                    f"An unexpected error occurred while retrieving videos "
                    f"for category '{category_name}': {e}"
                )

        # If no category_name is provided, get all videos
        else:
            try:
                query = self.c.execute("SELECT * FROM videos")

            except Exception as e:
                return (
                    "error",
                    f"An unexpected error occurred while retrieving "
                    f"all videos: {e}"
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
                "INSERT OR IGNORE INTO videos_tags (video_id, tag_id) VALUES (?, ?)",
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
            f"Added tag '{tag}' and linked it to video ID {video_id} successfully."
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
            video_id (int): The ID of the video to which the speaker will be added.

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
                "INSERT OR IGNORE INTO videos_speakers (video_id, speaker_id) VALUES (?, ?)",
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
            f"Added speaker '{speaker}' and linked them to video ID {video_id} successfully."
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
            list: A list of dicts, each containing the ID and name of a speaker.
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
            Links the character to a video in the videos_bible_characters table.

        Args:
            character (str): A character name to be added.
            video_id (int): The ID of the video to which the character will be added.

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
                "INSERT OR IGNORE INTO videos_bible_characters (video_id, character_id) VALUES (?, ?)",
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
            f"Added character '{character}' and linked them to video ID {video_id} successfully."
        )

    def get_characters_by_video_id(
        self,
        video_id: int,
    ) -> list[dict]:
        """
        Retrieve characters from the characters table for a video

        Args:
            video_id (int): The ID of the video for which to retrieve characters.

        Returns:
            list: A list of dicts, each containing the ID and name of a character.
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
            video_id (int): The ID of the video to which the scripture will be added.

        Returns:
            tuple: A tuple containing the status ("success" or "error")
                and a message.
        """

        try:
            self.c.execute(
                "INSERT OR IGNORE INTO scriptures (book, chapter, verse) VALUES (?, ?, ?)",
                (book, chapter, verse)
            )
            self.conn.commit()

            # Retrieve the scripture ID
            self.c.execute(
                "SELECT id FROM scriptures WHERE book = ? AND chapter = ? AND verse = ?",
                (book, chapter, verse)
            )
            scripture_id = self.c.fetchone()[0]

            # Insert into the videos_scriptures join table
            self.c.execute(
                "INSERT OR IGNORE INTO videos_scriptures (video_id, scripture_id) VALUES (?, ?)",
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
            f"Added scripture '{book} {chapter}:{verse}' and linked them to video ID {video_id} successfully."
        )

    def get_scriptures_by_video_id(
        self,
        video_id: int,
    ) -> list[dict]:
        """
        Retrieve scriptures from the scriptures table for a video.

        Args:
            video_id (int): The ID of the video for which to retrieve scriptures.

        Returns:
            list: A list of dicts, each containing the ID and details of a scripture.
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


if __name__ == "__main__":
    print("This is a a class file, and should not be run directly.")
