"""
Search module for video indexing and retrieval.

This module provides Elasticsearch-powered search functionality with
database fallback support.
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
