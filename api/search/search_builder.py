"""
Elasticsearch query builder for constructing search queries.

This module provides a builder pattern for creating Elasticsearch query DSL
    structures with multi-match queries, filters, and highlighting.

The main point is to create a complex search query that Elasticsearch can
    execute.

Classes:
    - SearchQueryBuilder:
        Builder for constructing Elasticsearch query DSL.
"""


# Standard library imports
import logging
from typing import (
    Dict,
    List,
    Any,
    Optional
)


logger = logging.getLogger(__name__)

# Constants
FUZZINESS = "AUTO"


class SearchQueryBuilder:
    """
    Builder for constructing Elasticsearch query DSL.

    Provides a fluent interface for building complex search queries with
        multi-match queries, filters, and result highlighting.

    Attributes:
        query: The query structure being built.
        filters: List of filter clauses to apply.

    Methods:
        __init__:
            Initialize a new query builder.
        add_multi_match:
            Add a multi-match query across multiple fields.
        add_filter:
            Add a term filter for exact matching.
        add_match_filter:
            Add a match filter for text matching.
        add_range_filter:
            Add a range filter for numeric or date fields.
        add_highlight:
            Add result highlighting for matched terms.
        add_sort:
            Add sorting to the query results.
    """

    def __init__(
        self
    ) -> None:
        """
        Initialize a new query builder.

        Sets up the base query structure with empty 'must' and
            'filter' clauses.
        """

        # Initialize base query structure
        self.query: Dict[str, Any] = {
            'query': {
                'bool': {
                    'must': [],
                    'filter': []
                }
            }
        }

        # Initialize filters list
        self.filters: List[Dict[str, Any]] = []

    def add_multi_match(
        self,
        query: str,
        fields: List[str],
        fuzziness: str = FUZZINESS
    ) -> 'SearchQueryBuilder':
        """
        Add a multi-match query across multiple fields.

        Enables fuzzy matching to handle typos and similar terms.

        Parameters:
            query (str): The search query string.
            fields (List[str]): List of fields to search across.
                Fields can include boost values (e.g., "title^3").
                This boosts the relevance of matches in higher-weighted fields.
            fuzziness (str): Fuzziness level for matching.
                "AUTO" automatically adjusts based on term length.

        Returns:
            SearchQueryBuilder: Self for method chaining.
        """

        # Construct multi-match query clause
        multi_match = {
            'multi_match': {
                'query': query,
                'fields': fields,
                'fuzziness': fuzziness,
                'type': 'best_fields'
            }
        }

        self.query['query']['bool']['must'].append(multi_match)

        # Return self for method chaining
        return self

    def add_filter(
        self,
        field: str,
        value: Any
    ) -> 'SearchQueryBuilder':
        """
        Add a term filter for exact matching.

        Filters results to only include documents where the field
        matches the specified value exactly.

        Parameters:
            field (str): The field name to filter on.
            value (Any): The value that must match exactly.

        Returns:
            SearchQueryBuilder: Self for method chaining.
        """

        # Construct term filter clause
        term_filter = {
            'term': {
                field: value
            }
        }

        # Add to filter list
        self.query['query']['bool']['filter'].append(term_filter)

        # Return self for method chaining
        return self

    def add_match_filter(
        self,
        field: str,
        value: str
    ) -> 'SearchQueryBuilder':
        """
        Add a match filter for text matching.

        Uses full-text matching instead of exact term matching.
        Useful for filtering on analyzed text fields.

        Parameters:
            field (str): The field name to filter on.
            value (str): The value to match against.

        Returns:
            SearchQueryBuilder: Self for method chaining.
        """

        # Construct match filter clause
        match_filter = {
            'match': {
                field: value
            }
        }

        # Add to filter list
        self.query['query']['bool']['filter'].append(match_filter)

        # Return self for method chaining
        return self

    def add_range_filter(
        self,
        field: str,
        gte: Optional[Any] = None,
        lte: Optional[Any] = None,
        gt: Optional[Any] = None,
        lt: Optional[Any] = None
    ) -> 'SearchQueryBuilder':
        """
        Add a range filter for numeric or date fields.

        Filters results based on field values within a specified range.

        Parameters:
            field (str): The field name to filter on.
            gte (Optional[Any]): Greater than or equal to.
            lte (Optional[Any]): Less than or equal to.
            gt (Optional[Any]): Greater than.
            lt (Optional[Any]): Less than.

        Returns:
            SearchQueryBuilder: Self for method chaining.
        """

        # Construct range filter clause
        range_params = {}

        if gte is not None:
            range_params['gte'] = gte
        if lte is not None:
            range_params['lte'] = lte
        if gt is not None:
            range_params['gt'] = gt
        if lt is not None:
            range_params['lt'] = lt

        # Add range filter if any parameters were provided
        if range_params:
            range_filter = {
                'range': {
                    field: range_params
                }
            }

            # Add to filter list
            self.query['query']['bool']['filter'].append(range_filter)

        # Return self for method chaining
        return self

    def add_highlight(
        self,
        fields: List[str],
        fragment_size: int = 150,
        number_of_fragments: int = 3
    ) -> 'SearchQueryBuilder':
        """
        Add result highlighting for matched terms.

        Highlights matching terms in search results to show users where
            their query terms appear in the content.

        Parameters:
            fields (List[str]): List of fields to highlight.
            fragment_size (int): Maximum size of each highlighted fragment.
            number_of_fragments (int): Number of fragments to return
                per field.

        Returns:
            SearchQueryBuilder: Self for method chaining.
        """

        # Construct highlight fields configuration
        highlight_fields = {}
        for field in fields:
            highlight_fields[field] = {
                'fragment_size': fragment_size,
                'number_of_fragments': number_of_fragments
            }

        # Add highlight configuration to query
        self.query['highlight'] = {
            'fields': highlight_fields,
            'pre_tags': ['<em>'],
            'post_tags': ['</em>']
        }

        # Return self for method chaining
        return self

    def add_should_match_filters(
        self,
        field: str,
        values: List[str]
    ) -> 'SearchQueryBuilder':
        """
        Add multiple match filters with OR logic (should clause).

        Creates a bool query with should clauses for matching any of
        the provided values. Useful for filtering where any value
        should match (e.g., speaker1 OR speaker2).

        Parameters:
            field (str): The field name to filter on.
            values (List[str]): List of values to match against.

        Returns:
            SearchQueryBuilder: Self for method chaining.
        """

        if not values:
            logger.debug(f"No values provided for field '{field}', skipping")
            return self

        logger.debug(
            f"Adding should match filter for field '{field}' "
            f"with values: {values}"
        )

        # Create should clauses for each value
        should_clauses = [
            {'match': {field: value}}
            for value in values
        ]

        # Wrap in a bool query with minimum_should_match
        bool_filter = {
            'bool': {
                'should': should_clauses,
                'minimum_should_match': 1
            }
        }

        logger.debug(f"Created bool filter: {bool_filter}")

        # Add to filter list
        self.query['query']['bool']['filter'].append(bool_filter)

        # Return self for method chaining
        return self

    def add_sort(
        self,
        field: str,
        order: str = 'desc'
    ) -> 'SearchQueryBuilder':
        """
        Add sorting to the query results.

        Parameters:
            field (str): The field name to sort by.
            order (str): Sort order, either 'asc' or 'desc'.

        Returns:
            SearchQueryBuilder: Self for method chaining.
        """

        # Initialize sort array if not present
        if 'sort' not in self.query:
            self.query['sort'] = []

        # Add sort clause
        self.query['sort'].append({
            field: {
                'order': order
            }
        })

        # Return self for method chaining
        return self

    def build(
        self
    ) -> Dict[str, Any]:
        """
        Build and return the complete query structure.

        Finalizes the query construction and returns the complete
            Elasticsearch query DSL.

        Args:
            None

        Returns:
            Dict[str, Any]: Complete Elasticsearch query structure ready
                for execution.
        """

        # If no 'must' clauses, add match_all
        if not self.query['query']['bool']['must']:
            self.query['query']['bool']['must'].append({
                'match_all': {}
            })

        # Remove empty filter array if no filters added
        if not self.query['query']['bool']['filter']:
            del self.query['query']['bool']['filter']

        logger.debug(f"Built query: {self.query}")
        return self.query
