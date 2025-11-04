"""
Elasticsearch client wrapper with connection management and health checks.

This module provides a singleton Elasticsearch client that handles
connection failures gracefully and provides health check functionality.
"""

from typing import Optional
from elasticsearch import Elasticsearch, exceptions
import logging
import os
import time

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """
    Singleton wrapper for Elasticsearch client with health monitoring.
    
    Attributes:
        _instance: Singleton instance of the client.
        _client: The actual Elasticsearch client instance.
        _is_available: Flag indicating if Elasticsearch is available.
        _last_check_time: Timestamp of last health check.
        _check_interval: Minimum seconds between health checks.
    """
    
    _instance: Optional['ElasticsearchClient'] = None
    _client: Optional[Elasticsearch] = None
    _is_available: bool = False
    _last_check_time: float = 0
    _check_interval: int = 30  # Check health every 30 seconds max
    
    def __new__(cls) -> 'ElasticsearchClient':
        """
        Create or return the singleton instance.
        
        Returns:
            ElasticsearchClient: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """
        Initialize the Elasticsearch client with environment configuration.
        
        Reads configuration from environment variables:
        - ELASTICSEARCH_HOST: Hostname (default: localhost)
        - ELASTICSEARCH_PORT: Port number (default: 9200)
        """
        if self._client is None:
            es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
            es_port = os.getenv('ELASTICSEARCH_PORT', '9200')
            es_url = f"http://{es_host}:{es_port}"
            
            logger.info(f"Initializing Elasticsearch client: {es_url}")
            
            try:
                # Create client with ES 8.x compatible settings
                self._client = Elasticsearch(
                    hosts=[es_url],
                    request_timeout=10,
                    max_retries=3,
                    retry_on_timeout=True,
                    # Disable SSL verification for local development
                    verify_certs=False,
                    # Don't use sniffing in single-node setup
                    sniff_on_start=False,
                    sniff_on_connection_fail=False,
                )
                
                # Perform initial health check
                self._check_health()
                
                if self._is_available:
                    logger.info(
                        f"Elasticsearch client connected successfully "
                        f"to {es_url}"
                    )
                else:
                    logger.warning(
                        f"Elasticsearch client created but service "
                        f"not available at {es_url}"
                    )
                    
            except Exception as e:
                logger.error(
                    f"Failed to initialize Elasticsearch client: {e}. "
                    f"URL: {es_url}. Falling back to database search.",
                    exc_info=True
                )
                self._is_available = False
    
    def _check_health(self) -> None:
        """
        Check if Elasticsearch is available and responding.
        
        Updates the _is_available flag based on cluster health.
        Uses time-based caching to avoid excessive health checks.
        """
        current_time = time.time()
        
        # Skip check if we checked recently
        if (current_time - self._last_check_time) < self._check_interval:
            return
        
        self._last_check_time = current_time
        
        try:
            if self._client:
                # Use info() instead of ping() for ES 8.x compatibility
                info = self._client.info()
                
                if info:
                    # Get cluster health
                    health = self._client.cluster.health()
                    status = health.get('status', 'red')
                    
                    self._is_available = status in ['yellow', 'green']
                    
                    if self._is_available:
                        logger.debug(
                            f"Elasticsearch health check passed. "
                            f"Status: {status}, "
                            f"Version: {info.get('version', {}).get('number')}"
                        )
                    else:
                        logger.warning(
                            f"Elasticsearch cluster status is {status}"
                        )
                else:
                    self._is_available = False
                    logger.warning(
                        "Elasticsearch info() returned empty response"
                    )
            else:
                self._is_available = False
                logger.warning("Elasticsearch client is None")
                
        except exceptions.ConnectionError as e:
            self._is_available = False
            logger.warning(
                f"Elasticsearch connection error: {e}. "
                "Service may not be running."
            )
        except exceptions.TransportError as e:
            self._is_available = False
            logger.warning(
                f"Elasticsearch transport error: {e}. "
                "Check network connectivity."
            )
        except exceptions.AuthenticationException as e:
            self._is_available = False
            logger.error(
                f"Elasticsearch authentication failed: {e}. "
                "Check credentials."
            )
        except Exception as e:
            self._is_available = False
            logger.error(
                f"Unexpected error checking Elasticsearch health: {e}",
                exc_info=True
            )
    
    def is_available(self) -> bool:
        """
        Check if Elasticsearch service is currently available.
        
        Performs a fresh health check if the check interval has elapsed.
        
        Returns:
            bool: True if Elasticsearch is available, False otherwise.
        """
        self._check_health()
        return self._is_available
    
    def get_client(self) -> Optional[Elasticsearch]:
        """
        Get the Elasticsearch client instance if available.
        
        Performs a health check before returning the client.
        
        Returns:
            Optional[Elasticsearch]: Client instance or None if unavailable.
        """
        if self.is_available():
            return self._client
        return None
    
    def force_reconnect(self) -> bool:
        """
        Force a reconnection attempt to Elasticsearch.
        
        Useful when Elasticsearch becomes available after being down.
        
        Returns:
            bool: True if reconnection successful, False otherwise.
        """
        logger.info("Forcing Elasticsearch reconnection...")
        self._last_check_time = 0  # Reset check interval
        self._check_health()
        
        if self._is_available:
            logger.info("Elasticsearch reconnection successful")
        else:
            logger.warning("Elasticsearch reconnection failed")
        
        return self._is_available
    
    def close(self) -> None:
        """
        Close the Elasticsearch client connection.
        
        Cleans up resources and resets availability flags.
        """
        if self._client:
            try:
                self._client.close()
                logger.info("Elasticsearch client connection closed")
            except Exception as e:
                logger.error(
                    f"Error closing Elasticsearch client: {e}",
                    exc_info=True
                )
            finally:
                self._client = None
                self._is_available = False
                self._last_check_time = 0