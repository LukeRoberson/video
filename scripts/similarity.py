"""
Module: similarity.py

Calculate the similarities between two videos based on their metadata.

Classes:
    Similarity: A class to calculate the similarity between two videos.
    SimScraper: A class to scrape and calculate similarity between videos.

Usage:
    Use the Similarity class to compare two videos by their IDs.
        Use the context manager, and provide two video IDs to compare.
        Will return a float between 0 and 1, where 1 is identical.

    Use the SimScraper class to compare multiple videos.
        No context manager is available.
        Initialize with a list of video IDs or leave empty to compare all.
        Call the run_comparison method to perform the comparisons.
        Each video in the list will be compared against every video in the DB.
        The top 10 similarities will be stored in the database.

Dependencies:
    - heapq
        For maintaining a min-heap of top similarity scores.
    - concurrent.futures
        For parallel execution of similarity calculations (multithreading).
"""


# Standard library imports
import logging
import types
import os
import sys
from tqdm import tqdm
from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Optional
)

# Special imports
import heapq
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

# Add the parent directory of 'app' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Custom application imports
from app.sql_db import (    # noqa: E402
    DatabaseContext,
    VideoManager,
    CategoryManager,
    TagManager,
    LocationManager,
    SpeakerManager,
    ScriptureManager,
    CharacterManager,
    SimilarityManager,
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

WEIGHTS = {
    "categories": 0.15,
    "tags": 0.15,
    "location": 0.1,
    "scriptures": 0.35,
    "text": 0.1,
    "characters": 0.1,
    "speakers": 0.05,
}

THREADS = 8


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Similarity:
    """
    Class to calculate the similarity between two videos.

    Args:
        video1_id (int): The ID of the first video.
        video2_id (int): The ID of the second video.

    Methods:
        __init__:
            Initialize the Similarity class with two videos.
        __enter__:
            Enter the context of the Similarity class.
        __exit__:
            Exit the context of the Similarity class.
        _collect_data_from_cache:
            Collect video data from the provided metadata cache.
        _collect_data:
            Collect data for the two videos (non-cached).
        _jaccard:
            Use Jaccard similarity to compare two sets of data.
        _max_norm:
            Max Normilization to compare two sets of data.
        _overlap_coefficient:
            Overlap Coefficient to compare two sets of data.
        _hierarchy:
            Hierarchical similarity to compare two sets of data.
        weighted:
            Calculate the weighted similarity score between the two videos.
    """

    def __init__(
        self,
        video1_id: int,
        video2_id: int,
        metadata_cache: Optional[Dict[int, Dict[str, Any]]] = None,
    ) -> None:
        """
        Initialize the Similarity class with two videos.

        Args:
            video1_id (int): The ID of the first video.
            video2_id (int): The ID of the second video.
            metadata_cache (dict, optional): Cached metadata for all videos.

        Returns:
            None
        """

        self.video1 = {}
        self.video2 = {}
        self.video1['id'] = video1_id
        self.video2['id'] = video2_id

        self.category_similarity = None
        self.tag_similarity = None
        self.location_similarity = None
        self.speaker_similarity = None
        self.scripture_similarity = None
        self.character_similarity = None
        self.text_similarity = None
        self.weighted_similarity = None

        # If a metadata cache is provided, use it
        if metadata_cache:
            self._collect_data_from_cache(metadata_cache)

        # Otherwise, collect data from the database
        else:
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

    def _collect_data_from_cache(
        self,
        metadata_cache: Dict[int, Dict[str, Any]]
    ) -> None:
        """
        Collect video data from the provided metadata cache.

        Args:
            metadata_cache (dict): Cached metadata for all videos.

        Returns:
            None

        Raises:
            ValueError: If one or both videos are not found in the cache.
        """

        # Loop through both videos and update their data from the cache
        for video in (
            self.video1,
            self.video2
        ):
            # Collect data from the cache
            data = metadata_cache.get(video['id'])

            if not data:
                raise ValueError(
                    f"Video with ID {video['id']} not found in cache."
                )

            video.update(data)

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
            location_mgr = LocationManager(db)
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

                # Get location
                location = location_mgr.get_from_video(
                    video_id=video['id']
                )
                if location is not None:
                    location = [
                        location['name']
                        for location in location
                        if 'name' in location
                    ]
                    video['location'] = location
                else:
                    video['location'] = []

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

        Use the values in WEIGHTS to calculate the final score.

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
        self.location_similarity = self._jaccard(
            self.video1['location'],
            self.video2['location'],
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
            (self.category_similarity * WEIGHTS["categories"]) +
            (self.tag_similarity * WEIGHTS["tags"]) +
            (self.scripture_similarity * WEIGHTS["scriptures"]) +
            (self.text_similarity * WEIGHTS["text"]) +
            (self.character_similarity * WEIGHTS["characters"]) +
            (self.speaker_similarity * WEIGHTS["speakers"]) +
            (self.location_similarity * WEIGHTS["location"])
        )


class SimScraper:
    """
    Class to scrape and calculate similarity between videos.

    Builds a cache of all video metadata in memory
        to avoid repeated DB queries.

    Args:
        video_list (list): A list of video IDs to compare.
            Assumes all videos in the DB if not provided.

    Methods:
        __init__:
            Initialize the SimScraper class.
        _full_list:
            Fetch all video IDs from the database.
        _cache_all_metadata:
            Cache all video metadata in memory.
        _calculate_similarity:
            Calculate similarity between two videos.
        run_comparison:
            Run the similarity comparison for all video pairs.
    """

    def __init__(
        self,
        video_list: list[int] = [],
    ) -> None:
        """
        Initialize the SimScraper class.

        Requires:
            1. A list of video ID's
            2. A second list of video ID's to compare against.

        Tracks which videos have been compared already to avoid
            asymmetric comparisons.

        Args:
            video_list (list): A list of video IDs to compare.
                Assumes all videos in the DB if not provided.

        Returns:
            None
        """

        # Initialize the video list
        self.video_list = video_list
        if not self.video_list:
            self.video_list = self._full_list()

        # Initialise comparison list
        self.comparison_list = self._full_list()

        # Store a list of ID's that are done
        self.done_list = []

        # Cache all metadata
        self.metadata_cache = self._cache_all_metadata()

    def _full_list(
        self,
    ) -> list[int]:
        """
        Fetch all video IDs from the database if no video list is provided.

        Args:
            None

        Returns:
            list[int]: A list of video IDs from the database.
        """

        with DatabaseContext() as db:
            video_mgr = VideoManager(db)
            video_list = video_mgr.get()

        # Convert to list of IDs
        if video_list:
            video_list = [video['id'] for video in video_list]

        else:
            logger.warning("No videos found in the database.")
            video_list = []

        return video_list

    def _cache_all_metadata(
        self
    ) -> Dict[int, Dict[str, Any]]:
        """
        Fetch and cache all video metadata and related entities in memory.
        Returns a dict keyed by video ID.

        Args:
            None

        Returns:
            dict: A dictionary containing metadata for all videos.
        """

        with DatabaseContext() as db:
            video_mgr = VideoManager(db)
            cat_mgr = CategoryManager(db)
            tag_mgr = TagManager(db)
            location_mgr = LocationManager(db)
            speaker_mgr = SpeakerManager(db)
            scripture_mgr = ScriptureManager(db)
            character_mgr = CharacterManager(db)

            # Get all videos
            video_list = video_mgr.get()
            if not video_list:
                logger.warning("No videos found in the database for caching.")
                return {}

            # Build a dict of videos keyed by ID
            #   This will be the cache
            videos = {
                v['id']: v
                for v in video_list
            }

            # Fetch and attach related metadata for each video
            for vid in videos:
                # Get categories
                videos[vid]['categories'] = [
                    c['name']
                    for c in cat_mgr.get_from_video(video_id=vid)
                    or []
                ]

                # Get tags
                videos[vid]['tags'] = [
                    t['name']
                    for t in tag_mgr.get_from_video(video_id=vid)
                    or []
                ]

                # Get location
                videos[vid]['location'] = [
                    loc['name']
                    for loc in location_mgr.get_from_video(video_id=vid)
                    or []
                ]

                # Get speakers
                videos[vid]['speakers'] = [
                    s['name']
                    for s in speaker_mgr.get_from_video(video_id=vid)
                    or []
                ]

                # Get scriptures
                videos[vid]['scriptures'] = [
                    # Ignore 'id' and 'verse_text' fields
                    {
                        k: v
                        for k, v in s.items()
                        if k not in ('id', 'verse_text')
                    }
                    for s in scripture_mgr.get_from_video(video_id=vid)
                    or []
                ]

                # Get characters
                videos[vid]['characters'] = [
                    c['name']
                    for c in character_mgr.get_from_video(video_id=vid)
                    or []
                ]

        return videos

    def _calculate_similarity(
        self,
        video1: int,
        video2: int
    ) -> float | None:
        """
        Helper method to calculate weighted similarity between two videos.

        Args:
            video1 (int): ID of the first video.
            video2 (int): ID of the second video.

        Returns:
            float | None:
                Weighted similarity score, or None if calculation fails.
        """

        try:
            # Calculate similarity, using cached metadata
            with Similarity(
                video1_id=video1,
                video2_id=video2,
                metadata_cache=self.metadata_cache,
            ) as similarity:
                similarity.weighted()
                return similarity.weighted_similarity

        except Exception as exc:
            logger.error(
                f"Error calculating similarity for {video1} "
                f"and {video2}: {exc}"
            )

            return None

    def run_comparison(
        self,
    ) -> None:
        """
        Run the similarity comparison for all video pairs.

        Compares each video in the list against every other video
            and stores the results in the comparison list.
        The list of all videos is obtained from __init__.

        A min-heap is used to efficiently track the top 10 similarities
            for each video during the comparison process.

        Each video is compared only once against each other video
            to avoid redundant calculations.

        ThreadPoolExecutor is used to parallelize the similarity
            calculations for efficiency.

        Args:
            None

        Returns:
            None
        """

        # Loop through video list
        for video in tqdm(
            self.video_list,
            desc="Total Progress",
            leave=True,
            colour="magenta",
        ):
            # Track videos which have been compared already
            self.done_list.append(video)

            # Store top 10 similarities for the current video
            top_10: List[Dict[str, Any]] = []

            # Min-heap to keep track of top 10 similarities
            heap: List[Tuple[float, Any, Dict[str, Any]]] = []

            # Prepare comparison targets for this video
            #   Exclude videos that are already done
            targets = [
                comparison
                for comparison in self.comparison_list
                if comparison not in self.done_list
            ]

            # Use ThreadPoolExecutor for parallel similarity calculation
            with ThreadPoolExecutor(
                max_workers=THREADS
            ) as executor:
                # Map futures to comparison IDs
                future_to_comparison = {
                    executor.submit(
                        self._calculate_similarity,
                        video,
                        comparison
                    ):
                        comparison
                        for comparison in targets
                }

                # Iterate over futures
                for future in as_completed(future_to_comparison):
                    # Get the comparison ID
                    comparison = future_to_comparison[future]

                    # Retrieve the similarity score
                    try:
                        score = future.result()

                    except Exception as exc:
                        logger.error(
                            f"Similarity calculation failed for {video} "
                            f"and {comparison}: {exc}"
                        )
                        continue

                    if score is None:
                        continue

                    # Use a min-heap to keep top 10 scores efficiently
                    # Add a tiebreaker (comparison ID) to avoid comparing dicts
                    item = {
                        'video1': video,
                        'video2': comparison,
                        'score': score
                    }
                    heap_entry = (
                        score,
                        comparison,
                        item
                    )

                    # If heap has less than 10 items, push new entry
                    if len(heap) < 10:
                        heapq.heappush(
                            heap,
                            heap_entry
                        )

                    # Check if this result is better than the smallest in heap
                    #   If it is, push to heap and pop the smallest
                    #   This means the heap always contains the top 10 scores
                    else:
                        # The first element of the heap is the smallest score
                        if score > heap[0][0]:
                            heapq.heappushpop(heap, heap_entry)

            # Extract top 10 from heap and sort descending
            top_10 = [
                entry[2]
                for entry in sorted(
                    heap,
                    key=lambda x: x[0],
                    reverse=True
                )
            ]

            # Write the top 10 similarities for the current video
            with DatabaseContext() as db:
                sim_mgr = SimilarityManager(db)

                for item in top_10:
                    sim_mgr.add(
                        video1_id=item['video1'],
                        video2_id=item['video2'],
                        score=item['score'],
                    )


if __name__ == "__main__":
    scraper = SimScraper()
    scraper.run_comparison()
