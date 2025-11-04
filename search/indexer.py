"""
Elasticsearch indexer for video content and transcripts.

This module handles creating the Elasticsearch index, mapping configuration,
and indexing video data from the database along with VTT transcripts.
"""

from typing import List, Dict, Optional
from search.elastic_client import ElasticsearchClient
from search.vtt_parser import VTTParser
from app.sql_db import DatabaseContext, VideoManager
from elasticsearch import exceptions
import json
import logging
import os

logger = logging.getLogger(__name__)


class ElasticsearchIndexer:
    """
    Handles indexing operations for video content in Elasticsearch.
    
    Uses existing DatabaseContext and VideoManager from app.sql_db.
    
    Attributes:
        INDEX_NAME (str): Name of the Elasticsearch index for videos.
        es_client (ElasticsearchClient): Elasticsearch client wrapper instance.
        vtt_directory (str): Directory containing VTT subtitle files.
    """
    
    INDEX_NAME = "videos"
    
    def __init__(self, vtt_directory: Optional[str] = None) -> None:
        """
        Initialize the indexer.
        
        Parameters:
            vtt_directory (Optional[str]): Path to directory containing
                VTT files. Defaults to environment variable VTT_DIRECTORY
                or './vtt'.
        """
        self.es_client = ElasticsearchClient()
        self.vtt_directory = vtt_directory or os.getenv(
            'VTT_DIRECTORY',
            './vtt'
        )
    
    def create_index(self) -> bool:
        """
        Create the Elasticsearch index with configured mappings.
        
        Returns:
            bool: True if index created successfully, False otherwise.
        """
        client = self.es_client.get_client()
        if not client:
            logger.error("Elasticsearch not available, cannot create index")
            return False
        
        try:
            # Check if index already exists
            if client.indices.exists(index=self.INDEX_NAME):
                logger.info(f"Index '{self.INDEX_NAME}' already exists")
                return True
            
            # Load mappings from config file
            config_path = os.path.join(
                os.path.dirname(__file__),
                'mappings.json'
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
            
        except exceptions.RequestError as e:
            logger.error(f"Error creating index: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating index: {e}")
            return False
    
    def delete_index(self) -> bool:
        """
        Delete the Elasticsearch index.
        
        Returns:
            bool: True if index deleted successfully, False otherwise.
        """
        client = self.es_client.get_client()
        if not client:
            return False
        
        try:
            if client.indices.exists(index=self.INDEX_NAME):
                client.indices.delete(index=self.INDEX_NAME)
                logger.info(f"Successfully deleted index '{self.INDEX_NAME}'")
            return True
        except Exception as e:
            logger.error(f"Error deleting index: {e}")
            return False
    
    def index_video(self, video_data: Dict[str, any]) -> bool:
        """
        Index a single video with its transcript.
        
        Parameters:
            video_data (Dict[str, any]): Video data from database containing
                video_id, name, description, etc.
        
        Returns:
            bool: True if indexed successfully, False otherwise.
        """
        client = self.es_client.get_client()
        if not client:
            return False
        
        try:
            video_id = video_data.get('id')
            if not video_id:
                logger.error("Video data missing ID field")
                return False
            
            # Parse VTT file if available
            vtt_path = VTTParser.get_vtt_path_for_video(
                video_id,
                self.vtt_directory
            )
            vtt_data = VTTParser.parse_vtt_file(vtt_path)
            
            # Prepare document for indexing
            # Map database field 'name' to ES field 'title'
            document = {
                'video_id': video_id,
                'title': video_data.get('name', ''),
                'description': video_data.get('description', ''),
                'tags': '',  # Will be populated from related tables
                'speaker': '',  # Will be populated from related tables
                'bible_character': '',  # Will be populated from related tables
                'location': '',  # Will be populated from related tables
                'scriptures': '',  # Will be populated from related tables
            }
            
            # TODO: Fetch related data (tags, speakers, etc.) using managers
            # This would require additional queries to junction tables
            
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
        videos: List[Dict[str, any]],
        batch_size: int = 100
    ) -> Dict[str, int]:
        """
        Index multiple videos in batches.
        
        Parameters:
            videos (List[Dict[str, any]]): List of video data dictionaries.
            batch_size (int): Number of videos to index per batch.
        
        Returns:
            Dict[str, int]: Statistics with 'success' and 'failed' counts.
        """
        client = self.es_client.get_client()
        if not client:
            return {'success': 0, 'failed': len(videos)}
        
        from elasticsearch.helpers import bulk
        
        stats = {'success': 0, 'failed': 0}
        
        def generate_actions():
            """Generator for bulk indexing actions."""
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
                
                document = {
                    'video_id': video_id,
                    'title': video.get('name', ''),
                    'description': video.get('description', ''),
                    'tags': '',
                    'speaker': '',
                    'bible_character': '',
                    'location': '',
                    'scriptures': '',
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
            
            stats['success'] = success_count
            # failed_items is a list of failed documents
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
    
    def reindex_all(self) -> Dict[str, int]:
        """
        Reindex all videos from the database.
        
        Uses DatabaseContext and VideoManager from app.sql_db.
        
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
            videos = video_mgr.get()  # Get all videos
        
        if not videos:
            logger.warning("No videos found to reindex")
            return {'success': 0, 'failed': 0}
        
        logger.info(f"Reindexing {len(videos)} videos...")
        
        return self.bulk_index_videos(videos)