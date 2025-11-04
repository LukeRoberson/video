"""
Flask routes for video search functionality.

This module provides REST API endpoints for searching videos
using either Elasticsearch or database fallback.
"""

from flask import Blueprint, request, jsonify, current_app
from search import SearchService
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

search_bp = Blueprint('search', __name__, url_prefix='/api/search')


def get_search_service() -> SearchService:
    """
    Get or create SearchService instance from application context.
    
    Returns:
        SearchService: Configured search service instance.
    """
    if 'SEARCH_SERVICE' not in current_app.config:
        current_app.config['SEARCH_SERVICE'] = SearchService()
    return current_app.config['SEARCH_SERVICE']


@search_bp.route('/', methods=['GET'])
def search_videos():
    """
    Search for videos using query parameters.
    
    Query Parameters:
        q (str): Search query string (required)
        page (int): Page number for pagination (default: 1)
        per_page (int): Results per page (default: 20, max: 100)
        speaker (str): Filter by speaker name (optional)
        tags (str): Comma-separated list of tags to filter (optional)
    
    Returns:
        JSON response containing:
            - results: List of matching videos
            - total: Total count of matching videos
            - page: Current page number
            - per_page: Number of results per page
            - pages: Total number of pages
            - using_elasticsearch: Boolean indicating search method used
            - query: The search query string
            - filters: Applied filters
    
    Status Codes:
        200: Success
        400: Bad request (missing or invalid parameters)
        500: Internal server error
    """
    try:
        # Get query parameters
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Query parameter "q" is required'
            }), 400
        
        # Pagination parameters
        try:
            page = max(1, int(request.args.get('page', 1)))
            per_page = min(
                100,
                max(1, int(request.args.get('per_page', 20)))
            )
        except ValueError:
            return jsonify({
                'error': 'Invalid pagination parameters'
            }), 400
        
        # Filter parameters
        filters = {}
        
        if request.args.get('speaker'):
            filters['speaker'] = request.args.get('speaker')
        
        if request.args.get('tags'):
            filters['tags'] = [
                tag.strip() 
                for tag in request.args.get('tags').split(',')
            ]
        
        # Perform search
        search_service = get_search_service()
        (results, total), using_es = search_service.search(
            query=query,
            page=page,
            per_page=per_page,
            filters=filters if filters else None
        )
        
        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page
        
        # Log search results with method indicator
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
        
        return jsonify({
            'results': results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': total_pages,
            'using_elasticsearch': using_es,
            'query': query,
            'filters': filters
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error processing search request: {e}",
            exc_info=True
        )
        return jsonify({
            'error': 'An error occurred while processing your search'
        }), 500


@search_bp.route('/reindex', methods=['POST'])
def reindex_all_videos():
    """
    Reindex all videos in Elasticsearch.
    
    This endpoint should be protected in production
    (e.g., require admin auth).
    
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
        from search import ElasticsearchIndexer, ElasticsearchClient
        
        # Check if Elasticsearch is available
        es_client = ElasticsearchClient()
        if not es_client.is_available():
            return jsonify({
                'error': 'Elasticsearch is not available'
            }), 503
        
        # Perform reindexing
        indexer = ElasticsearchIndexer()
        
        logger.info("Starting full reindex of all videos...")
        stats = indexer.reindex_all()
        
        # Validate stats dictionary
        success_count = int(stats.get('success', 0))
        failed_count = int(stats.get('failed', 0))
        total_count = success_count + failed_count
        
        logger.info(
            f"Reindexing complete: {success_count} successful, "
            f"{failed_count} failed"
        )
        
        return jsonify({
            'success': success_count,
            'failed': failed_count,
            'total': total_count,
            'message': 'Reindexing completed'
        }), 200
        
    except Exception as e:
        logger.error(f"Error during reindexing: {e}", exc_info=True)
        return jsonify({
            'error': 'An error occurred during reindexing'
        }), 500


@search_bp.route('/status', methods=['GET'])
def search_status():
    """
    Check the status of the search service.
    
    Returns:
        JSON response containing:
            - elasticsearch_available: Boolean indicating ES availability
            - index_exists: Boolean indicating if videos index exists
            - fallback_active: Boolean indicating if using database fallback
            - timestamp: ISO timestamp of the status check
    
    Status Codes:
        200: Success
    """
    try:
        from search import ElasticsearchClient
        
        es_client = ElasticsearchClient()
        es_available = es_client.is_available()
        
        index_exists = False
        if es_available:
            client = es_client.get_client()
            if client:
                from search.indexer import ElasticsearchIndexer
                # Convert HeadApiResponse to boolean
                try:
                    response = client.indices.exists(
                        index=ElasticsearchIndexer.INDEX_NAME
                    )
                    # In ES 8.x, this returns a response object
                    # Check if it has a boolean conversion or status
                    index_exists = bool(response)
                except Exception as idx_error:
                    logger.warning(
                        f"Could not check index existence: {idx_error}"
                    )
                    index_exists = False
        
        return jsonify({
            'elasticsearch_available': bool(es_available),
            'index_exists': bool(index_exists),
            'fallback_active': not bool(es_available),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error checking search status: {e}", exc_info=True)
        return jsonify({
            'elasticsearch_available': False,
            'index_exists': False,
            'fallback_active': True,
            'error': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200


# Add this new route for advanced search

@search_bp.route('/advanced', methods=['GET'])
def advanced_search():
    """
    Handle advanced search with multiple filters.
    
    Query Parameters:
        query (str): Text search query (optional)
        speakers (list): Speaker IDs to filter by
        characters (list): Character IDs to filter by
        locations (list): Location IDs to filter by
        tags (list): Tag IDs to filter by
        page (int): Page number (default: 1)
        per_page (int): Results per page (default: 20)
    
    Returns:
        JSON response with filtered search results.
    """
    try:
        query = request.args.get('query', '').strip()
        
        # Get pagination parameters
        try:
            page = max(1, int(request.args.get('page', 1)))
            per_page = min(
                100,
                max(1, int(request.args.get('per_page', 20)))
            )
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
        
        # Perform search with filters
        search_service = get_search_service()
        
        # If no text query but filters exist, use match_all with filters
        if not query and filters:
            query = "*"  # Match all, rely on filters
        
        (results, total), using_es = search_service.search(
            query=query if query else "*",
            page=page,
            per_page=per_page,
            filters=filters if filters else None
        )
        
        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page
        
        # Log operation
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
        
        return jsonify({
            'results': results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': total_pages,
            'using_elasticsearch': using_es,
            'query': query,
            'filters': filters
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error in advanced search: {e}",
            exc_info=True
        )
        return jsonify({
            'error': 'An error occurred during advanced search'
        }), 500
