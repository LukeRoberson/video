"""
Search module for video indexing and retrieval.

This module provides Elasticsearch-powered search functionality with
    database fallback support.

Exported Classes:
    - ElasticsearchClient:
        Client for connecting to Elasticsearch.
    - ElasticsearchIndexer:
        Indexer for adding and updating video data in Elasticsearch.
    - SearchService:
        Service for handling search queries with fallback to the database.
    - SearchQueryBuilder:
        Builder for constructing complex search queries.
"""

from search.elastic_client import ElasticsearchClient
from search.indexer import ElasticsearchIndexer
from search.search_service import SearchService
from search.search_builder import SearchQueryBuilder

__all__ = [
    'ElasticsearchClient',
    'ElasticsearchIndexer',
    'SearchService',
    'SearchQueryBuilder',
]
