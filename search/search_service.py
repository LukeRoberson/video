"""
Search service providing unified interface to Elasticsearch and database search.

This module coordinates search operations, providing Elasticsearch-powered
search with automatic fallback to database search when Elasticsearch is
unavailable.
"""

from typing import Dict, List, Optional, Tuple, Any
from search.elastic_client import ElasticsearchClient
from search.search_builder import SearchQueryBuilder
import logging

logger = logging.getLogger(__name__)


class SearchService:
    """
    Unified search service with Elasticsearch and database fallback.
    
    Attributes:
        INDEX_NAME: Name of the Elasticsearch index for videos.
        es_client: Elasticsearch client instance.
    """
    
    INDEX_NAME = "videos"
    
    def __init__(self) -> None:
        """
        Initialize the search service.
        
        Sets up Elasticsearch client and prepares for search operations.
        """
        self.es_client = ElasticsearchClient()
        logger.info("Search service initialized")
    
    def search(
        self,
        query: str,
        page: int = 1,
        per_page: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[Tuple[List[Dict[str, Any]], int], bool]:
        """
        Search for videos using Elasticsearch or database fallback.
        
        Parameters:
            query (str): Search query string.
            page (int): Page number for pagination (1-indexed).
            per_page (int): Number of results per page.
            filters (Optional[Dict[str, Any]]): Additional filter criteria.
        
        Returns:
            Tuple containing:
                - Tuple of (List of search results, Total count)
                - Boolean indicating if Elasticsearch was used
        """
        if self.es_client.is_available():
            try:
                logger.info(
                    f"🔍 Using Elasticsearch for query: '{query}'"
                )
                results = self._elasticsearch_search(
                    query, page, per_page, filters
                )
                logger.info(
                    f"✓ Elasticsearch returned {results[1]} results "
                    f"for query: '{query}'"
                )
                return results, True
            except Exception as e:
                logger.error(
                    f"Elasticsearch search failed: {e}. "
                    "Falling back to database.",
                    exc_info=True
                )
        
        logger.warning(
            f"⚠ Using database fallback for query: '{query}' "
            "(Elasticsearch unavailable)"
        )
        results = self._database_search(query, page, per_page, filters)
        logger.warning(
            f"⚠ Database fallback returned {results[1]} results "
            f"for query: '{query}'"
        )
        return results, False
    
    def _elasticsearch_search(
        self,
        query: str,
        page: int = 1,
        per_page: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Perform search using Elasticsearch.
        
        Parameters:
            query (str): Search query string.
            page (int): Page number for pagination (1-indexed).
            per_page (int): Number of results per page.
            filters (Optional[Dict[str, Any]]): Additional filter criteria.
        
        Returns:
            Tuple of (List of search results, Total count).
        """
        client = self.es_client.get_client()
        if not client:
            raise RuntimeError("Elasticsearch client not available")
        
        # Build the search query
        search_query = self._build_search_query(query, filters)
        
        logger.debug(f"Elasticsearch query: {search_query}")
        
        # Calculate offset
        from_offset = (page - 1) * per_page
        
        try:
            # Execute search
            response = client.search(
                index=self.INDEX_NAME,
                body=search_query,
                from_=from_offset,
                size=per_page
            )
            
            logger.debug(
                f"ES Response: {response['hits']['total']} total hits"
            )
            
            # Extract results
            hits = response['hits']['hits']
            total = response['hits']['total']['value']
            
            logger.info(
                f"Elasticsearch found {total} documents, "
                f"returning {len(hits)} results"
            )
            
            # Format results and enrich with database data
            results = []
            for hit in hits:
                source = hit['_source']
                video_id = source.get('video_id')
                
                logger.debug(
                    f"Processing video_id: {video_id} "
                    f"(score: {hit['_score']})"
                )
                
                # Get full video data from database
                video_data = self._get_video_from_db(video_id)
                
                if video_data:
                    # Merge ES data with DB data
                    result = {
                        'id': video_id,
                        'video_id': video_id,
                        'name': video_data.get('name'),
                        'title': source.get('title'),
                        'description': video_data.get('description', ''),
                        'thumbnail': video_data.get('thumbnail'),
                        'speaker': video_data.get('speaker', ''),
                        'tags': video_data.get('tags', ''),
                        'duration': video_data.get('duration'),
                        'watched': video_data.get('watched', False),
                        'score': hit['_score'],
                    }
                    
                    # Add highlights if available
                    if 'highlight' in hit:
                        result['highlights'] = hit['highlight']
                    
                    results.append(result)
                    logger.debug(
                        f"Added video: {result['name']} "
                        f"(thumbnail: {result['thumbnail']})"
                    )
                else:
                    logger.warning(
                        f"Video {video_id} found in ES but not in database"
                    )
            
            return results, total
            
        except Exception as e:
            logger.error(
                f"Elasticsearch search error: {e}",
                exc_info=True
            )
            raise
    
    def _get_video_from_db(
        self,
        video_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch complete video data from database.
        
        Parameters:
            video_id (str): The video ID to fetch.
        
        Returns:
            Optional[Dict[str, Any]]: Video data dictionary or None if not 
                found.
        """
        try:
            from app.sql_db import DatabaseContext, VideoManager
            
            with DatabaseContext() as db:
                video_mgr = VideoManager(db)
                
                # Get all videos and find the one with matching ID
                all_videos = video_mgr.get() or []
                
                for video in all_videos:
                    if str(video.get('id')) == str(video_id):
                        logger.debug(
                            f"Found video in DB: {video.get('name')} "
                            f"(id: {video_id})"
                        )
                        return {
                            'id': video.get('id'),
                            'name': video.get('name'),
                            'description': video.get('description'),
                            'thumbnail': video.get('thumbnail'),
                            'speaker': video.get('speaker'),
                            'tags': video.get('tags'),
                            'duration': video.get('duration'),
                            'watched': video.get('watched', False),
                        }
                
                logger.warning(
                    f"Video {video_id} not found in database"
                )
        except Exception as e:
            logger.error(
                f"Error fetching video {video_id} from database: {e}",
                exc_info=True
            )
        
        return None
    
    def _database_search(
        self,
        query: str,
        page: int = 1,
        per_page: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Perform search using database as fallback.
        
        Parameters:
            query (str): Search query string.
            page (int): Page number for pagination (1-indexed).
            per_page (int): Number of results per page.
            filters (Optional[Dict[str, Any]]): Additional filter criteria.
        
        Returns:
            Tuple of (List of search results, Total count).
        """
        from app.sql_db import DatabaseContext, VideoManager
        
        with DatabaseContext() as db:
            video_mgr = VideoManager(db)
            
            # Get all videos and filter in memory (basic fallback)
            all_videos = video_mgr.get() or []
            
            logger.debug(
                f"Database has {len(all_videos)} total videos"
            )
            
            # Filter by query
            query_lower = query.lower()
            filtered = [
                v for v in all_videos
                if (query_lower in v.get('name', '').lower() or
                    query_lower in v.get('description', '').lower())
            ]
            
            logger.debug(
                f"After filtering by query '{query}': "
                f"{len(filtered)} videos"
            )
            
            # Apply additional filters if provided
            if filters:
                if 'speaker' in filters:
                    speaker = filters['speaker'].lower()
                    filtered = [
                        v for v in filtered
                        if speaker in v.get('speaker', '').lower()
                    ]
                
                if 'tags' in filters:
                    tag_filters = [t.lower() for t in filters['tags']]
                    filtered = [
                        v for v in filtered
                        if any(
                            tag in v.get('tags', '').lower()
                            for tag in tag_filters
                        )
                    ]
            
            # Calculate pagination
            total = len(filtered)
            start = (page - 1) * per_page
            end = start + per_page
            
            # Return paginated results
            results = filtered[start:end]
            
            # Normalize field names for consistency
            normalized_results = []
            for video in results:
                normalized_results.append({
                    'id': video.get('id'),
                    'video_id': video.get('id'),
                    'name': video.get('name'),
                    'title': video.get('name'),
                    'description': video.get('description', ''),
                    'thumbnail': video.get('thumbnail'),
                    'speaker': video.get('speaker', ''),
                    'tags': video.get('tags', ''),
                    'duration': video.get('duration'),
                    'watched': video.get('watched', False),
                })
            
            return normalized_results, total
    
    def _build_search_query(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build Elasticsearch query with filters.
        
        Parameters:
            query (str): Search query string.
            filters (Optional[Dict[str, Any]]): Additional filter criteria.
        
        Returns:
            Dict[str, Any]: Elasticsearch query DSL.
        """
        builder = SearchQueryBuilder()
        
        # Add main query
        if query and query != "*":
            builder.add_multi_match(
                query,
                [
                    "title^3",
                    "description^2",
                    "transcript",
                    "speaker",
                    "tags"
                ]
            )
        
        # Add filters
        if filters:
            if 'speaker' in filters:
                builder.add_filter('speaker', filters['speaker'])
            
            if 'tags' in filters:
                for tag in filters['tags']:
                    builder.add_filter('tags', tag)
        
        # Add highlighting
        builder.add_highlight(['title', 'description', 'transcript'])
        
        query_dsl = builder.build()
        logger.debug(f"Built query DSL: {query_dsl}")
        
        return query_dsl