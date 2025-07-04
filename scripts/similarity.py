"""
Module: similarity.py

Calculate the similarities between two videos based on their metadata.

Classes:
    Similarity: A class to calculate the similarity between two videos.

Dependencies:
    logging: For logging information and errors.
    types: For type hinting in the class methods.
"""


# Standard library imports
import logging
import types
import os
import sys

# Add the parent directory of 'app' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Custom application imports
from app.sql_db import (    # noqa: E402
    DatabaseContext,
    VideoManager,
    CategoryManager,
    TagManager,
    SpeakerManager,
    ScriptureManager,
    CharacterManager,
)


COMMON_STOP_WORDS = [
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why", "how",
    "all", "any", "both", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "s", "t", "can", "will", "just", "don", "should", "now"
]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Similarity:
    """
    Class to calculate the similarity between two videos.

    Args:
        video1_id (int): The ID of the first video.
        video2_id (int): The ID of the second video.
    """

    def __init__(
        self,
        video1_id: int,
        video2_id: int,
    ) -> None:
        """
        Initialize the Similarity class with two videos.

        Args:
            video1_id (int): The ID of the first video.
            video2_id (int): The ID of the second video.

        Returns:
            None
        """

        self.video1 = {}
        self.video2 = {}
        self.video1['id'] = video1_id
        self.video2['id'] = video2_id

        self.category_similarity = None
        self.tag_similarity = None
        self.speaker_similarity = None
        self.scripture_similarity = None
        self.character_similarity = None
        self.text_similarity = None
        self.weighted_similarity = None

        self._collect_data()

    def __enter__(
        self
    ) -> "Similarity":
        """
        Enter the context of the Similarity class.

        Args:
            None

        Returns:
            Similarity: The instance of the Similarity class.
        """

        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        """
        Exit the context of the Similarity class.

        Args:
            exc_type (type | None): The type of the exception.
            exc_value (BaseException | None): The value of the exception.
            traceback (object | None): The traceback object.

        Returns:
            None
        """

        if exc_type is not None and exc_value is not None:
            # Ensure traceback is of the correct type
            tb = (
                traceback
                if isinstance(traceback, types.TracebackType)
                else None
            )

            logging.error(
                "An exception occurred in the Similarity context manager.",
                exc_info=(exc_type, exc_value, tb),
            )

        # Do not suppress exceptions; let them propagate
        return None

    def _collect_data(
        self,
    ) -> None:
        """
        Collect data for the two videos.

        1. Fetch video metadata from the database.
        2. Retrieve associated categories, tags, speakers, scriptures,
            and characters.
        3. Store the collected data in the video dictionaries.

        Args:
            None

        Returns:
            None

        Raises:
            ValueError: If one or both videos are not found in the database.
        """

        with DatabaseContext() as db:
            video_mgr = VideoManager(db)
            cat_mgr = CategoryManager(db)
            tag_mgr = TagManager(db)
            speaker_mgr = SpeakerManager(db)
            scripture_mgr = ScriptureManager(db)
            character_mgr = CharacterManager(db)

            for video in (self.video1, self.video2):
                # Get the video entry
                video_entry = video_mgr.get(video['id'])
                if not video_entry:
                    raise ValueError(
                        f"Video with ID {video['id']} "
                        f"not found in the database."
                    )

                # Convert list to single item if necessary
                video_entry = (
                    video_entry[0]
                    if isinstance(video_entry, list)
                    else video_entry
                )

                # Store the video metadata
                video['name'] = video_entry.get('name', '')
                video['description'] = video_entry.get('description', '')

                # Get categories
                categories = cat_mgr.get_from_video(
                    video_id=video['id']
                )
                if categories is not None:
                    categories = [
                        category['name']
                        for category in categories
                        if 'name' in category
                    ]
                    video['categories'] = categories

                # Get tags
                tags = tag_mgr.get_from_video(
                    video_id=video['id']
                )
                if tags is not None:
                    tags = [tag['name'] for tag in tags if 'name' in tag]
                    video['tags'] = tags
                else:
                    video['tags'] = []

                # Get speakers
                speakers = speaker_mgr.get_from_video(
                    video_id=video['id']
                )
                if speakers is not None:
                    speakers = [
                        speaker['name']
                        for speaker in speakers
                        if 'name' in speaker
                    ]
                    video['speakers'] = speakers
                else:
                    video['speakers'] = []

                # Get scriptures
                scriptures = scripture_mgr.get_from_video(
                    video_id=video['id']
                )
                if scriptures is not None:
                    scriptures = [
                        {
                            k: v for k,
                            v in scripture.items()
                            if k not in ('id', 'verse_text')
                        }
                        for scripture in scriptures
                    ]
                    video['scriptures'] = scriptures
                else:
                    video['scriptures'] = []

                # Get characters
                characters = character_mgr.get_from_video(
                    video_id=video['id']
                )
                if characters is not None:
                    characters = [
                        character['name']
                        for character in characters
                        if 'name' in character
                    ]
                    video['characters'] = characters
                else:
                    video['characters'] = []

    def _jaccard(
        self,
        list1: list,
        list2: list,
    ) -> float:
        """
        Use Jaccard similarity to compare two sets of data.

        Used with tags and characters.

        Args:
            list1 (list): The first list of data.
            list2 (list): The second list of data.

        Returns:
            float: The Jaccard similarity coefficient between the two lists.
        """

        if not list1 or not list2:
            return 0.0

        set1 = set(list1)
        set2 = set(list2)

        # Get intersection and union of the two sets
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        # Return the score
        return intersection / union if union else 0.0

    def _max_norm(
        self,
        list1: list,
        list2: list,
    ) -> float:
        """
        Max Normilization to compare two sets of data.

        Used with speakers.

        Args:
            list1 (list): The first list of data.
            list2 (list): The second list of data.

        Returns:
            float: The Max Normilization similarity coefficient
                between the two lists.
        """

        if not list1 or not list2:
            return 0.0

        set1 = set(list1)
        set2 = set(list2)

        # Get intersection and max cardinality of the two sets
        intersection = len(set1.intersection(set2))
        max_cardinality = max(len(set1), len(set2))

        # Return the score
        return intersection / max_cardinality if max_cardinality else 0.0

    def _overlap_coefficient(
        self,
        name1: str,
        name2: str,
        desc1: str = "",
        desc2: str = "",
    ) -> float:
        """
        Overlap Coefficient to compare two sets of data.

        Used with name and description.

        Args:
            name1 (str): The name of the first video.
            desc1 (str): The description of the first video.
            name2 (str): The name of the second video.
            desc2 (str): The description of the second video.

        Returns:
            float: The Overlap Coefficient similarity score
                between the two videos.
        """

        if not name1 or not name2:
            return 0.0

        # Combine text from name and description
        text1 = f"{name1} {desc1}".lower()
        text2 = f"{name2} {desc2}".lower()

        # Remove common stop words
        text1_words = set(
            word
            for word in text1.split()
            if word not in COMMON_STOP_WORDS
        )
        text2_words = set(
            word
            for word in text2.split()
            if word not in COMMON_STOP_WORDS
        )

        if not text1_words or not text2_words:
            return 0.0

        # Get intersection and minimum cardinality of the two sets
        intersection = len(text1_words.intersection(text2_words))
        min_cardinality = min(len(text1_words), len(text2_words))

        # Return the score
        return intersection / min_cardinality if min_cardinality else 0.0

    def _hierarchy(
        self,
        list1: list[dict],
        list2: list[dict],
    ) -> float:
        """
        Hierarchical similarity to compare two sets of data.

        Used with scriptures.

        Args:
            list1 (list[dict]): The first list of dictionaries.
            list2 (list[dict]): The second list of dictionaries.

        Returns:
            float: The Hierarchical similarity score between the two lists.
        """

        if not list1 or not list2:
            return 0.0

        total_score = 0.0
        max_score = len(list1) * len(list2)

        for item1 in list1:
            for item2 in list2:
                # Exact match
                if (
                    item1.get('book') == item2.get('book') and
                    item1.get('chapter') == item2.get('chapter') and
                    item1.get('verse') == item2.get('verse')
                ):
                    total_score += 1.0

                # Book and chapter match
                elif (
                    item1.get('book') == item2.get('book') and
                    item1.get('chapter') == item2.get('chapter')
                ):
                    total_score += 0.5

                # Book match
                elif item1.get('book') == item2.get('book'):
                    total_score += 0.2

        # Return the score normalized by the maximum possible score
        return total_score / max_score if max_score else 0.0

    def weighted(
        self,
    ) -> None:
        """
        Calculate the weighted similarity score between the two videos.

        The score is calculated as follows:
        - 30% for categories
        - 20% for tags
        - 20% for scriptures
        - 15% for name and description
        - 10% for characters
        - 5% for speakers

        Args:
            None

        Returns:
            None
        """

        self.category_similarity = self._jaccard(
            self.video1['categories'],
            self.video2['categories'],
        )
        self.tag_similarity = self._jaccard(
            self.video1['tags'],
            self.video2['tags'],
        )
        self.speaker_similarity = self._max_norm(
            self.video1['speakers'],
            self.video2['speakers'],
        )
        self.scripture_similarity = self._hierarchy(
            self.video1['scriptures'],
            self.video2['scriptures'],
        )
        self.character_similarity = self._jaccard(
            self.video1['characters'],
            self.video2['characters'],
        )
        self.text_similarity = self._overlap_coefficient(
            name1=self.video1['name'],
            desc1=self.video1['description'],
            name2=self.video2['name'],
            desc2=self.video2['description'],
        )

        # Calculate the weighted score
        self.weighted_similarity = (
            (self.category_similarity * 0.3) +
            (self.tag_similarity * 0.2) +
            (self.scripture_similarity * 0.2) +
            (self.text_similarity * 0.15) +
            (self.character_similarity * 0.1) +
            (self.speaker_similarity * 0.05)
        )


if __name__ == "__main__":
    # Example usage of the Similarity class
    video1_id = 1  # Replace with actual video ID
    video2_id = 2  # Replace with actual video ID

    with Similarity(video1_id, video2_id) as similarity:
        similarity.weighted()

        # Print the similarity scores
        print(f"Category similarity: {similarity.category_similarity}")
        print(f"Tag similarity: {similarity.tag_similarity}")
        print(f"Speaker similarity: {similarity.speaker_similarity}")
        print(f"Scripture similarity: {similarity.scripture_similarity}")
        print(f"Character similarity: {similarity.character_similarity}")
        print(f"Text similarity: {similarity.text_similarity}")
        print(f"Similarity score: {similarity.weighted_similarity}")
