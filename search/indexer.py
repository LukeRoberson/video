"""
Elasticsearch indexer for video content and transcripts.

This module handles creating the Elasticsearch index, mapping configuration,
    and indexing video data from the database along with VTT transcripts.

NOTE: Indexes are the containers for documents in Elasticsearch.
    Documents are the individual records stored in an index.
    Here, we create an index for Videos, where each document represents a video
    along with its metadata.

Indexes:
    Videos:
        - Fields: video_id, title, description, tags, speaker,
            bible_character, location, scriptures, transcript,
            transcript_chunks.

Classes:
    - ElasticsearchIndexer:
        Handles indexing operations for video content in Elasticsearch.

Third-party Dependencies:
    elasticsearch:
        - exceptions: Exception classes for handling Elasticsearch errors.

    elasticsearch.helpers:
        - bulk: Helper function for bulk indexing operations.

Local Dependencies:
    search:
        - elastic_client: Wrapper for connection management.
        - vtt_parser: VTTParser for parsing VTT subtitle files.

    app.sql_db:
        - DatabaseContext: Context manager for database connections.
        - VideoManager: Manager for accessing video records in the database.
"""

# Standard library imports
import json
import logging
import os
from typing import (
    List,
    Dict,
    Optional,
    Generator,
    Any
)

# Third-party imports
from elasticsearch import exceptions
from elasticsearch.helpers import bulk

# Local imports
from search.elastic_client import ElasticsearchClient
from search.vtt_parser import VTTParser
from app.sql_db import (
    DatabaseContext,
    VideoManager,
    TagManager,
    SpeakerManager,
    CharacterManager,
    LocationManager,
    ScriptureManager
)


logger = logging.getLogger(__name__)

MAPPINGS_FILE = 'mappings.json'


class ElasticsearchIndexer:
    """
    Handles indexing operations for video content in Elasticsearch.

    Uses DatabaseContext and VideoManager from app.sql_db.

    Attributes:
        INDEX_NAME (str):
            Name of the Elasticsearch index for videos.
        es_client (ElasticsearchClient): Elasticsearch client wrapper instance.
        vtt_directory (str): Directory containing VTT subtitle files.

    Methods:
        __init__:
            Initialize the indexer with Elasticsearch client and VTT directory.
        create_index:
            Create the Elasticsearch index with configured mappings.
        delete_index:
            Delete the Elasticsearch index.
        index_video:
            Index a single video with its transcript.
        bulk_index_videos:
            Index multiple videos in batches.
        reindex_all:
            Reindex all videos from the database.
    """

    INDEX_NAME = "videos"

    def __init__(
        self,
        vtt_directory: Optional[str] = None
    ) -> None:
        """
        Initialize the indexer.

        Args:
            vtt_directory (Optional[str]): Path to directory containing
                VTT files. Defaults to environment variable VTT_DIRECTORY
                or './vtt'.

        Returns:
            None
        """

        # Initialize Elasticsearch client
        self.es_client = ElasticsearchClient()

        # Set VTT directory, where transcript files are stored
        self.vtt_directory = vtt_directory or os.getenv(
            'VTT_DIRECTORY',
            './vtt'
        )

    def create_index(
        self
    ) -> bool:
        """
        Create the Elasticsearch 'Video' index with configured mappings.
            This will contain a document for each video.

        Args:
            None

        Returns:
            bool: True if index created successfully, False otherwise.

        Exceptions:
            - exceptions.RequestError:
                Raised if there is an error in the index creation request.
        """

        # Get Elasticsearch client
        client = self.es_client.get_client()
        if not client:
            logger.error("Elasticsearch not available, cannot create index")
            return False

        # Create the index with mappings from config file
        try:
            # Check if index already exists
            if client.indices.exists(index=self.INDEX_NAME):
                logger.info(f"Index '{self.INDEX_NAME}' already exists")
                return True

            # Load mappings from config file
            config_path = os.path.join(
                os.path.dirname(__file__),
                MAPPINGS_FILE
            )

            with open(config_path, 'r') as f:
                mappings = json.load(f)

            # Create index
            client.indices.create(
                index=self.INDEX_NAME,
                body=mappings
            )

            logger.info(f"Successfully created index '{self.INDEX_NAME}'")
            return True

        # Handle cases where the search is invalid
        except exceptions.RequestError as e:
            logger.error(f"Error creating index: {e}")
            return False

        # Handle any other exceptions
        except Exception as e:
            logger.error(f"Unexpected error creating index: {e}")
            return False

    def delete_index(
        self
    ) -> bool:
        """
        Delete the Elasticsearch index.

        Args:
            None

        Returns:
            bool: True if index deleted successfully, False otherwise.
        """

        # Get Elasticsearch client
        client = self.es_client.get_client()
        if not client:
            return False

        # Delete the index
        try:
            if client.indices.exists(index=self.INDEX_NAME):
                client.indices.delete(index=self.INDEX_NAME)
                logger.info(f"Successfully deleted index '{self.INDEX_NAME}'")

            return True

        except Exception as e:
            logger.error(f"Error deleting index: {e}")
            return False

    def index_video(
        self,
        video_data: Dict
    ) -> bool:
        """
        Index a single video with its transcript.
            This creates a document in the Elasticsearch index.

        Args:
            video_data (Dict): Video data from database containing
                video_id, name, description, etc.

        Returns:
            bool: True if indexed successfully, False otherwise.
        """

        # Get Elasticsearch client
        client = self.es_client.get_client()
        if not client:
            return False

        try:
            # Get the video ID
            video_id = video_data.get('id')
            if not video_id:
                logger.error("Video data missing ID field")
                return False

            # Parse transcript if available
            vtt_path = VTTParser.get_vtt_path_for_video(
                video_id,
                self.vtt_directory
            )
            vtt_data = VTTParser.parse_vtt_file(vtt_path)

            # Fetch related data using managers
            with DatabaseContext() as db:
                tag_mgr = TagManager(db)
                speaker_mgr = SpeakerManager(db)
                char_mgr = CharacterManager(db)
                loc_mgr = LocationManager(db)
                scripture_mgr = ScriptureManager(db)

                tags = tag_mgr.get_from_video(video_id)
                speakers = speaker_mgr.get_from_video(video_id)
                characters = char_mgr.get_from_video(video_id)
                locations = loc_mgr.get_from_video(video_id)
                scriptures = scripture_mgr.get_from_video(video_id)

            # Prepare document for indexing
            #   Map database field 'name' to ES field 'title'
            document = {
                'video_id': video_id,
                'title': video_data.get('name', ''),
                'description': video_data.get('description', ''),

                'tags': ', '.join(
                    [tag['name'] for tag in tags]
                ) if tags else '',

                'speaker': ', '.join(
                    [spk['name'] for spk in speakers]
                ) if speakers else '',

                'bible_character': ', '.join(
                    [char['name'] for char in characters]
                ) if characters else '',

                'location': ', '.join(
                    [loc['name'] for loc in locations]
                ) if locations else '',

                # Construct scripture reference from book, chapter, verse, text
                'scriptures': ', '.join(
                    [
                        f"{scr.get('book', '')} "
                        f"{scr.get('chapter', '')}:{scr.get('verse', '')} "
                        f"- {scr.get('verse_text', '')}"
                        for scr in scriptures
                    ]
                ) if scriptures else '',
            }

            # Add transcript data if available
            if vtt_data:
                document['transcript'] = vtt_data['transcript']
                document['transcript_chunks'] = vtt_data['transcript_chunks']

            else:
                document['transcript'] = ''
                document['transcript_chunks'] = []

            # Index the document
            client.index(
                index=self.INDEX_NAME,
                id=video_id,
                body=document
            )

            logger.debug(f"Successfully indexed video {video_id}")
            return True

        except Exception as e:
            logger.error(f"Error indexing video: {e}")
            return False

    def bulk_index_videos(
        self,
        videos: List[Dict],
        batch_size: int = 100
    ) -> Dict[str, int]:
        """
        Index multiple videos in batches.

        Args:
            videos (List[Dict[str, any]]): List of video data dictionaries.
            batch_size (int): Number of videos to index per batch.

        Returns:
            Dict[str, int]: Statistics with 'success' and 'failed' counts.

        Functions:
            generate_actions:
                Generator function to yield indexing actions for bulk API.
        """

        # Get Elasticsearch client
        client = self.es_client.get_client()
        if not client:
            return {'success': 0, 'failed': len(videos)}

        stats = {'success': 0, 'failed': 0}

        def generate_actions() -> Generator[Dict[str, Any], None, None]:
            """
            Generator for bulk indexing actions.

            Args:
                None

            Yields:
                Generator[Dict[str, Any], None, None]:
                    Action dictionary for each video to be indexed.
            """

            # Loop through videos and prepare documents
            for video in videos:
                video_id = video.get('id')
                if not video_id:
                    stats['failed'] += 1
                    continue

                # Parse VTT file
                vtt_path = VTTParser.get_vtt_path_for_video(
                    video_id,
                    self.vtt_directory
                )
                vtt_data = VTTParser.parse_vtt_file(vtt_path)

                # Fetch related data using managers
                with DatabaseContext() as db:
                    tag_mgr = TagManager(db)
                    speaker_mgr = SpeakerManager(db)
                    char_mgr = CharacterManager(db)
                    loc_mgr = LocationManager(db)
                    scripture_mgr = ScriptureManager(db)

                    tags = tag_mgr.get_from_video(video_id)
                    speakers = speaker_mgr.get_from_video(video_id)
                    characters = char_mgr.get_from_video(video_id)
                    locations = loc_mgr.get_from_video(video_id)
                    scriptures = scripture_mgr.get_from_video(video_id)

                document = {
                    'video_id': video_id,
                    'title': video.get('name', ''),
                    'description': video.get('description', ''),

                    'tags': ', '.join(
                        [tag['name'] for tag in tags]
                    ) if tags else '',

                    'speaker': ', '.join(
                        [spk['name'] for spk in speakers]
                    ) if speakers else '',

                    'bible_character': ', '.join(
                        [char['name'] for char in characters]
                    ) if characters else '',

                    'location': ', '.join(
                        [loc['name'] for loc in locations]
                    ) if locations else '',

                    # Construct scripture reference from
                    #   book, chapter, verse, text
                    'scriptures': ', '.join(
                        [
                            f"{scr.get('book', '')} "
                            f"{scr.get('chapter', '')}:{scr.get('verse', '')} "
                            f"- {scr.get('verse_text', '')}"
                            for scr in scriptures
                        ]
                    ) if scriptures else '',

                    'transcript': vtt_data['transcript'] if vtt_data else '',
                    'transcript_chunks': (
                        vtt_data['transcript_chunks'] if vtt_data else []
                    )
                }

                yield {
                    '_index': self.INDEX_NAME,
                    '_id': video_id,
                    '_source': document
                }

        try:
            # bulk() returns (success_count, failed_items_list)
            success_count, failed_items = bulk(
                client,
                generate_actions(),
                chunk_size=batch_size,
                raise_on_error=False,
                stats_only=False
            )

            # Success count
            stats['success'] = success_count

            # failed_items is a list of failed documents, or could be an int
            if isinstance(failed_items, int):
                stats['failed'] = failed_items
            else:
                stats['failed'] = len(failed_items) if failed_items else 0

            logger.info(
                f"Bulk indexing complete: {stats['success']} successful, "
                f"{stats['failed']} failed"
            )

        except Exception as e:
            logger.error(f"Error during bulk indexing: {e}")
            stats['failed'] = len(videos)
            stats['success'] = 0

        return stats

    def reindex_all(
        self
    ) -> Dict[str, int]:
        """
        Reindex all videos from the database.

        Uses DatabaseContext and VideoManager from app.sql_db.

        Args:
            None

        Returns:
            Dict[str, int]: Statistics with 'success' and 'failed' counts.
        """

        # Delete existing index and create new one
        self.delete_index()
        if not self.create_index():
            return {'success': 0, 'failed': 0}

        # Fetch all videos using VideoManager
        with DatabaseContext() as db:
            video_mgr = VideoManager(db)
            videos = video_mgr.get()

        if not videos:
            logger.warning("No videos found to reindex")
            return {'success': 0, 'failed': 0}

        logger.info(f"Reindexing {len(videos)} videos...")

        # Bulk index videos and return stats
        return self.bulk_index_videos(videos)
