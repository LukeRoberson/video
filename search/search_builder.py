"""
Elasticsearch query builder for constructing search queries.

This module provides a builder pattern for creating Elasticsearch query DSL
structures with multi-match queries, filters, and highlighting.
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SearchQueryBuilder:
    """
    Builder for constructing Elasticsearch query DSL.
    
    Provides a fluent interface for building complex search queries with
    multi-match queries, filters, and result highlighting.
    
    Attributes:
        query: The query structure being built.
        filters: List of filter clauses to apply.
    """
    
    def __init__(self) -> None:
        """
        Initialize a new query builder.
        
        Sets up the base query structure with empty must and filter clauses.
        """
        self.query: Dict[str, Any] = {
            'query': {
                'bool': {
                    'must': [],
                    'filter': []
                }
            }
        }
        self.filters: List[Dict[str, Any]] = []
    
    def add_multi_match(
        self,
        query: str,
        fields: List[str],
        fuzziness: str = "AUTO"
    ) -> 'SearchQueryBuilder':
        """
        Add a multi-match query across multiple fields.
        
        Enables fuzzy matching to handle typos and similar terms.
        
        Parameters:
            query (str): The search query string.
            fields (List[str]): List of fields to search across.
                Fields can include boost values (e.g., "title^3").
            fuzziness (str): Fuzziness level for matching.
                "AUTO" automatically adjusts based on term length.
        
        Returns:
            SearchQueryBuilder: Self for method chaining.
        """
        multi_match = {
            'multi_match': {
                'query': query,
                'fields': fields,
                'fuzziness': fuzziness,
                'type': 'best_fields'
            }
        }
        self.query['query']['bool']['must'].append(multi_match)
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
        term_filter = {
            'term': {
                field: value
            }
        }
        self.query['query']['bool']['filter'].append(term_filter)
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
        match_filter = {
            'match': {
                field: value
            }
        }
        self.query['query']['bool']['filter'].append(match_filter)
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
        range_params = {}
        if gte is not None:
            range_params['gte'] = gte
        if lte is not None:
            range_params['lte'] = lte
        if gt is not None:
            range_params['gt'] = gt
        if lt is not None:
            range_params['lt'] = lt
        
        if range_params:
            range_filter = {
                'range': {
                    field: range_params
                }
            }
            self.query['query']['bool']['filter'].append(range_filter)
        
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
        highlight_fields = {}
        for field in fields:
            highlight_fields[field] = {
                'fragment_size': fragment_size,
                'number_of_fragments': number_of_fragments
            }
        
        self.query['highlight'] = {
            'fields': highlight_fields,
            'pre_tags': ['<em>'],
            'post_tags': ['</em>']
        }
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
        if 'sort' not in self.query:
            self.query['sort'] = []
        
        self.query['sort'].append({
            field: {
                'order': order
            }
        })
        return self
    
    def build(self) -> Dict[str, Any]:
        """
        Build and return the complete query structure.
        
        Finalizes the query construction and returns the complete
        Elasticsearch query DSL.
        
        Returns:
            Dict[str, Any]: Complete Elasticsearch query structure ready
                for execution.
        """
        # If no must clauses, add match_all
        if not self.query['query']['bool']['must']:
            self.query['query']['bool']['must'].append({
                'match_all': {}
            })
        
        # Remove empty filter array if no filters added
        if not self.query['query']['bool']['filter']:
            del self.query['query']['bool']['filter']
        
        logger.debug(f"Built query: {self.query}")
        return self.query