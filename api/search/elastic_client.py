"""
Elasticsearch client wrapper with connection management and health checks.

This module provides a singleton Elasticsearch client that handles
    connection failures gracefully and provides health check functionality.

ElasticsearchClient is a wrapper class around the official Elasticsearch
    Python client. This class formats connection parameters, manages the
    client instance, and includes methods to check the health of the
    Elasticsearch service.
The actual Elasticsearch operations are performed using the official
    Elasticsearch Python client library.

NOTE: This module assumes Elasticsearch 8.x compatibility. Newer versions
    of the Elasticsearch Python client may have different parameters.

NOTE: This app assumes a single-node Elasticsearch setup without
    SSL or authentication.

Classes:
    - ElasticsearchClient:
        Client for connecting to Elasticsearch with health monitoring.

Third-party Dependencies:
    elasticsearch:
        - Elasticsearch: Main client class for connecting to Elasticsearch.
        - exceptions: Exception classes for handling Elasticsearch errors.
"""

# Standard library imports
from typing import Optional
import logging
import os
import time

# Third-party imports
from elasticsearch import (
    Elasticsearch,
    exceptions
)


logger = logging.getLogger(__name__)


# Suppress verbose Elasticsearch library logging
logging.getLogger('elastic_transport.transport').setLevel(logging.ERROR)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)


# Elasticsearch client configuration constants
CLIENT_TIMEOUT = 2
CLIENT_RETRIES = 1
CLIENT_RETRY_ON_TIMEOUT = False

# Cert verification - Can be off for local dev or protected containers
CLIENT_VERIFY_CERTS = False

# Sniffing options - Disabled for single-node setups
CLIENT_SNIFF_ON_START = False
CLIENT_SNIFF_ON_CONNECTION_FAIL = False


class ElasticsearchClient:
    """
    Singleton wrapper for Elasticsearch client with health monitoring.

    Attributes:
        _instance: Singleton instance of the client.
        _client: The actual Elasticsearch client instance.
        _is_available: Flag indicating if Elasticsearch is available.
        _last_check_time: Timestamp of last health check.
        _check_interval: Minimum seconds between health checks.

    Methods:
        __new__: Create or return the singleton instance.
        __init__: Initialize the Elasticsearch client.
        _check_health: Check if Elasticsearch is available and responding.
        is_available: Check if Elasticsearch service is currently available.
        get_client: Get the Elasticsearch client instance if available.
        force_reconnect: Force a reconnection attempt to Elasticsearch.
        close: Close the Elasticsearch client connection.
    """

    # An instance of the ElasticsearchClient
    _instance: Optional['ElasticsearchClient'] = None

    # The Elasticsearch client instance
    _client: Optional[Elasticsearch] = None

    # Flag indicating if Elasticsearch is available
    _is_available: bool = False

    # Timestamp of last health check
    _last_check_time: float = 0

    # Seconds between health checks
    _check_interval: int = 30

    def __new__(
        cls
    ) -> 'ElasticsearchClient':
        """
        Create or return the singleton instance.
            (singleton means only one instance of this class can exist)

        __new__ creates a new instance of a class.
            This is overridden to ensure only one instance of
            ElasticsearchClient exists.

        Args:
            None

        Returns:
            ElasticsearchClient: The instance.
        """

        if cls._instance is None:
            # Super() uses the parent class (python's 'object')
            #   to create a new instance
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self
    ) -> None:
        """
        Initialize the Elasticsearch client with environment configuration.
            This uses the Elasticsearch client from the official library.

        Reads configuration from environment variables:
            - ELASTICSEARCH_HOST: Hostname (default: localhost)
            - ELASTICSEARCH_PORT: Port number (default: 9200)

        Include a .env file or pass through environment variables in
            docker-compose or 'docker run' as needed

        Args:
            None

        Returns:
            None
        """

        # Only initialize once
        if self._client is None:
            # Connection parameters
            es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
            es_port = os.getenv('ELASTICSEARCH_PORT', '9200')
            es_url = f"http://{es_host}:{es_port}"

            logger.info(f"Initializing Elasticsearch client: {es_url}")

            try:
                # Create the client from the official library
                self._client = Elasticsearch(
                    hosts=[es_url],
                    request_timeout=CLIENT_TIMEOUT,
                    max_retries=CLIENT_RETRIES,
                    retry_on_timeout=CLIENT_RETRY_ON_TIMEOUT,
                    verify_certs=CLIENT_VERIFY_CERTS,
                    sniff_on_start=CLIENT_SNIFF_ON_START,
                    sniff_on_connection_fail=CLIENT_SNIFF_ON_CONNECTION_FAIL,
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

    def _check_health(
        self
    ) -> None:
        """
        Check if Elasticsearch is available and responding.

        Updates the _is_available flag based on cluster health.
        Uses time-based caching to avoid excessive health checks.

        Args:
            None

        Returns:
            None

        Exceptions:
            ConnectionError: If unable to connect to Elasticsearch.
            TransportError: For transport-related issues.
            AuthenticationException: If authentication fails.
        """

        # Skip check if we checked recently
        current_time = time.time()
        if (current_time - self._last_check_time) < self._check_interval:
            return
        self._last_check_time = current_time

        try:
            if self._client:
                # Get basic info to verify connection
                info = self._client.info()

                if info:
                    # Get cluster health
                    health = self._client.cluster.health()
                    status = health.get('status', 'red')

                    # Consider 'yellow' and 'green' as available
                    #   Yellow is normal for single-node clusters
                    self._is_available = status in ['yellow', 'green']

                    # Log detailed status
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

            # Client is None; cannot connect
            else:
                self._is_available = False
                logger.warning("Elasticsearch client is None")

        # Connection error (server down, wrong port, etc)
        except exceptions.ConnectionError as e:
            self._is_available = False
            logger.warning(
                f"Elasticsearch connection error: {e}. "
                "Service may not be running."
            )

        # Transport error (general communication issues)
        except exceptions.TransportError as e:
            self._is_available = False
            logger.warning(
                f"Elasticsearch transport error: {e}. "
                "Check network connectivity."
            )

        # Authentication error (wrong credentials)
        except exceptions.AuthenticationException as e:
            self._is_available = False
            logger.error(
                f"Elasticsearch authentication failed: {e}. "
                "Check credentials."
            )

        # Catch-all for unexpected errors
        except Exception as e:
            self._is_available = False
            logger.error(
                f"Unexpected error checking Elasticsearch health: {e}",
                exc_info=True
            )

    def is_available(
        self
    ) -> bool:
        """
        Check if Elasticsearch service is currently available.

        Performs a fresh health check if the check interval has elapsed.

        Args:
            None

        Returns:
            bool: True if Elasticsearch is available, False otherwise.
        """

        self._check_health()
        return self._is_available

    def get_client(
        self
    ) -> Optional[Elasticsearch]:
        """
        Get the Elasticsearch client instance if available.

        Performs a health check before returning the client.

        Args:
            None

        Returns:
            Optional[Elasticsearch]: Client instance or None if unavailable.
        """

        # Return the library client
        if self.is_available():
            return self._client

        return None

    def force_reconnect(
        self
    ) -> bool:
        """
        Force a reconnection attempt to Elasticsearch.

        Useful when Elasticsearch becomes available after being down.

        Args:
            None

        Returns:
            bool: True if reconnection successful, False otherwise.
        """

        logger.info("Forcing Elasticsearch reconnection...")

        # Reset last check time
        self._last_check_time = 0
        self._check_health()

        if self._is_available:
            logger.info("Elasticsearch reconnection successful")
        else:
            logger.warning("Elasticsearch reconnection failed")

        return self._is_available

    def close(
        self
    ) -> None:
        """
        Close the Elasticsearch client connection.

        Args:
            None

        Returns:
            None

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
