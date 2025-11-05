"""
Flask routes for video search functionality.

This module provides REST API endpoints for searching videos
using either Elasticsearch or database fallback.

Functions:
    get_search_service
        Get or create SearchService instance from application context.

Blueprint:
    /api/search

Endpoints:
    GET /           - Search videos with query parameters
    POST /reindex   - Reindex all videos in Elasticsearch
    GET /status     - Check search service status
    GET /advanced   - Advanced search with multiple filters

External Dependencies:
    Flask
        Blueprint - for route grouping
        request - to access request data
        current_app - to access app context
        jsonify - to create JSON responses
        make_response - to create custom responses

Local Dependencies:
    search
        SearchService - Main search service handling search logic
        ElasticsearchClient - Client for interacting with Elasticsearch
        ElasticsearchIndexer - Indexer for managing Elasticsearch indices
"""

# Standard Library Imports
import logging
from datetime import (
    datetime,
    timezone
)

# Third-Party Imports
from flask import (
    Blueprint,
    request,
    current_app,
    jsonify,
    make_response
)

# Local Application Imports
from search import (
    SearchService,
    ElasticsearchClient,
    ElasticsearchIndexer
)


logger = logging.getLogger(__name__)

search_bp = Blueprint(
    'search',
    __name__,
    url_prefix='/api/search'
)


def get_search_service() -> SearchService:
    """
    Get or create SearchService instance from application context.

    Args:
        None

    Returns:
        SearchService: Configured search service instance.
    """

    # Create SearchService if not already in app config
    if 'SEARCH_SERVICE' not in current_app.config:
        current_app.config['SEARCH_SERVICE'] = SearchService()

    return current_app.config['SEARCH_SERVICE']


@search_bp.route(
    '/',
    methods=['GET']
)
def search_videos():
    """
    Search for videos using a simple search string.

    Args:
        None

    Query Parameters:
        q (str): Search query string (required)
        page (int): Page number for pagination (default: 1)
        per_page (int): Results per page (default: 20, max: 100)

    Status Codes:
        200: Success
        400: Bad request (missing or invalid parameters)
        500: Internal server error

    Returns:
        JSON response containing:
            - results: List of matching videos
            - total: Total count of matching videos
            - page: Current page number
            - per_page: Number of results per page
            - pages: Total number of pages
            - using_elasticsearch: Boolean indicating search method used
            - query: The search query string
    """

    logger.info("API: Processing standard search request...")
    try:
        # Get query parameters
        query = request.args.get('q', '').strip()

        if not query:
            return make_response(
                jsonify(
                    {
                        'error': 'Query parameter "q" is required'
                    }
                ),
                400
            )

        # Pagination parameters
        try:
            # Set the page number with defaults and limits
            page = max(
                1,
                int(request.args.get('page', 1))
            )

            # Set the results per page with defaults and limits
            per_page = min(
                100,
                max(1, int(request.args.get('per_page', 20)))
            )

        # Handle invalid pagination parameters
        except ValueError:
            return make_response(
                jsonify(
                    {
                        'error': 'Invalid pagination parameters'
                    }
                ),
                400
            )

        # Get the search service object
        search_service = get_search_service()

        # Perform search
        #   Returns tuple: (results list, total count)
        #   and boolean indicating if ES was used
        (results, total), using_es = search_service.search(
            query=query,
            page=page,
            per_page=per_page,
        )

        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page

        # Log search results and indicate method used (terminal only)
        if using_es:
            logger.info(
                f"✓ Elasticsearch search for '{query}': "
                f"{total} results found, "
                f"returned page {page}/{total_pages}"
            )

        else:
            logger.warning(
                f"⚠ Database fallback search for '{query}': "
                f"{total} results found, "
                f"returned page {page}/{total_pages}"
            )

        # Return JSON response
        return make_response(
            jsonify(
                {
                    'results': results,
                    'total': total,
                    'page': page,
                    'per_page': per_page,
                    'pages': total_pages,
                    'using_elasticsearch': using_es,
                    'query': query,
                }
            ),
            200
        )

    # Handle unexpected errors
    except Exception as e:
        logger.error(
            f"Error processing search request: {e}",
            exc_info=True
        )

        return make_response(
            jsonify(
                {
                    'error': 'An error occurred while processing your search'
                }
            ),
            500
        )


@search_bp.route(
    '/advanced',
    methods=['GET']
)
def advanced_search():
    """
    Handle advanced search with multiple filters.

    Args:
        None

    Query Parameters:
        query (str): Text search query (optional)
        speakers (list): Speaker IDs to filter by
        characters (list): Character IDs to filter by
        locations (list): Location IDs to filter by
        tags (list): Tag IDs to filter by
        page (int): Page number (default: 1)
        per_page (int): Results per page (default: 20)

    Status Codes:
        200: Success
        500: Internal server error

    Returns:
        JSON response containing:
            - results: List of matching videos
            - total: Total count of matching videos
            - page: Current page number
            - per_page: Number of results per page
            - pages: Total number of pages
            - using_elasticsearch: Boolean indicating search method used
            - query: The search query string
    """

    logger.info("API: Processing advanced search request...")
    try:
        # Get text query parameter
        query = request.args.get('query', '').strip()

        # Get pagination parameters
        try:
            # Set page and per_page with defaults and limits
            page = max(
                1,
                int(request.args.get('page', 1))
            )

            per_page = min(
                100,
                max(1, int(request.args.get('per_page', 20)))
            )

        # Fall back to defaults on invalid input
        except ValueError:
            page = 1
            per_page = 20

        # Build filters from request parameters
        filters = {}

        # Get list parameters
        if request.args.get('speakers'):
            filters['speakers'] = request.args.getlist('speakers')

        if request.args.get('characters'):
            filters['characters'] = request.args.getlist('characters')

        if request.args.get('locations'):
            filters['locations'] = request.args.getlist('locations')

        if request.args.get('tags'):
            filters['tags'] = request.args.getlist('tags')

        # Get the search service object
        search_service = get_search_service()

        # If no text query but filters exist, match all results then filter
        if not query and filters:
            query = "*"

        # Perform search with filters
        #   Returns tuple: (results list, total count)
        #   and boolean indicating if ES was used
        (results, total), using_es = search_service.search(
            query=query if query else "*",
            page=page,
            per_page=per_page,
            filters=filters if filters else None
        )

        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page

        # Log results to terminal
        if using_es:
            logger.info(
                f"✓ Advanced Elasticsearch search: "
                f"{total} results with filters {filters}"
            )

        else:
            logger.warning(
                f"⚠ Advanced database search: "
                f"{total} results with filters {filters}"
            )

        # Return JSON response
        return make_response(
            jsonify(
                {
                    'results': results,
                    'total': total,
                    'page': page,
                    'per_page': per_page,
                    'pages': total_pages,
                    'using_elasticsearch': using_es,
                    'query': query,
                    'filters': filters
                }
            ),
            200
        )

    except Exception as e:
        logger.error(
            f"Error in advanced search: {e}",
            exc_info=True
        )

        return make_response(
            jsonify(
                {
                    'error': 'An error occurred during advanced search'
                }
            ),
            500
        )


@search_bp.route(
    '/reindex',
    methods=['POST']
)
def reindex_all_videos():
    """
    Reindex all videos in Elasticsearch.

    Args:
        None

    Returns:
        JSON response containing:
            - success: Number of videos successfully indexed
            - failed: Number of videos that failed to index
            - total: Total number of videos processed

    Status Codes:
        200: Reindexing completed (check response for individual failures)
        503: Elasticsearch not available
        500: Internal server error
    """

    try:
        # Create Elasticsearch client
        es_client = ElasticsearchClient()

        # Check if Elasticsearch is available
        if not es_client.is_available():
            return make_response(
                jsonify(
                    {
                        'error': 'Elasticsearch is not available'
                    }
                ), 503
            )

        # Create indexer
        indexer = ElasticsearchIndexer()

        # Perform reindexing
        logger.info("Starting full reindex of all videos...")
        stats = indexer.reindex_all()

        # Dictionary of stats
        success_count = int(stats.get('success', 0))
        failed_count = int(stats.get('failed', 0))
        total_count = success_count + failed_count

        logger.info(
            f"Reindexing complete: {success_count} successful, "
            f"{failed_count} failed"
        )

        # Return reindexing stats
        return make_response(
            jsonify(
                {
                    'success': success_count,
                    'failed': failed_count,
                    'total': total_count,
                    'message': 'Reindexing completed'
                }
            ),
            200
        )

    except Exception as e:
        logger.error(
            f"Error during reindexing: {e}",
            exc_info=True
        )

        return make_response(
            jsonify(
                {
                    'error': 'An error occurred during reindexing'
                }
            ),
            500
        )


@search_bp.route(
    '/status',
    methods=['GET']
)
def search_status():
    """
    Check the status of the search service.

    Args:
        None

    Returns:
        JSON response containing:
            - elasticsearch_available: Boolean indicating ES availability
            - index_exists: Boolean indicating if videos index exists
            - fallback_active: Boolean indicating if using database fallback
            - timestamp: ISO timestamp of the status check

    Status Codes:
        200: Success
    """

    # Default values
    index_exists = False

    try:
        # Create Elasticsearch client and check status
        es_client = ElasticsearchClient()
        es_available = es_client.is_available()

        # If ES is available, check if index exists
        if es_available:
            # Get ES client
            client = es_client.get_client()

            # Check if index exists
            if client:
                # Convert HeadApiResponse to boolean
                try:
                    # Check if index exists
                    response = client.indices.exists(
                        index=ElasticsearchIndexer.INDEX_NAME
                    )

                    # In ES 8.x, this returns a response object
                    # It may need to be converted to boolean
                    # NOTE: Future ES versions may change this behavior
                    index_exists = bool(response)

                except Exception as idx_error:
                    logger.warning(
                        f"Could not check index existence: {idx_error}"
                    )
                    index_exists = False

        # Return status response
        return make_response(
            jsonify(
                {
                    'elasticsearch_available': bool(es_available),
                    'index_exists': bool(index_exists),
                    'fallback_active': not bool(es_available),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            ),
            200
        )

    # If there was an error, this means ES is not available
    except Exception as e:
        logger.error(f"Error checking search status: {e}", exc_info=True)

        return make_response(
            jsonify(
                {
                    'elasticsearch_available': False,
                    'index_exists': False,
                    'fallback_active': True,
                    'error': str(e),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            ),
            200
        )
