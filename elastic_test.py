"""
Test script for search functionality.

This script tests both Elasticsearch and database fallback search
to ensure proper functionality and graceful degradation.
"""

import requests
import json
from typing import Dict, Any, Optional
import sys


def create_session_with_profile(
    base_url: str,
    profile: str = "guest"
) -> requests.Session:
    """
    Create a session and set the profile cookie.
    
    Parameters:
        base_url (str): Base URL of the application.
        profile (str): Profile name to use (default: 'guest').
    
    Returns:
        requests.Session: Session with profile cookie set.
    """
    session = requests.Session()
    
    # Set the profile by making a request to the profile selection endpoint
    # or directly set the cookie
    session.cookies.set('selected_profile', profile, domain='localhost')
    
    return session


def print_section(title: str) -> None:
    """
    Print a formatted section header.
    
    Parameters:
        title (str): The section title to print.
    """
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def test_search_status(
    session: requests.Session,
    base_url: str
) -> Dict[str, Any]:
    """
    Test the search status endpoint.
    
    Parameters:
        session (requests.Session): HTTP session with profile cookie.
        base_url (str): Base URL of the application.
    
    Returns:
        Dict[str, Any]: Status response data.
    """
    print_section("Testing Search Status")
    
    try:
        response = session.get(
            f"{base_url}/api/search/status",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        print(
            f"Elasticsearch Available: "
            f"{data['elasticsearch_available']}"
        )
        print(f"Index Exists: {data['index_exists']}")
        print(f"Fallback Active: {data['fallback_active']}")
        
        return data
        
    except requests.exceptions.JSONDecodeError as e:
        print(f"❌ Error: Received non-JSON response")
        print(f"Response content: {response.text[:200]}")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


def test_search_query(
    session: requests.Session,
    base_url: str,
    query: str,
    expected_method: Optional[str] = None
) -> None:
    """
    Test a search query.
    
    Parameters:
        session (requests.Session): HTTP session with profile cookie.
        base_url (str): Base URL of the application.
        query (str): Search query string.
        expected_method (Optional[str]): Expected search method 
            ('elasticsearch' or 'database').
    """
    print_section(f"Testing Search Query: '{query}'")
    
    try:
        response = session.get(
            f"{base_url}/api/search/",
            params={'q': query, 'per_page': 5},
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            print(response.text[:500])
            return
        
        data = response.json()
        
        print(f"Total Results: {data['total']}")
        print(f"Using Elasticsearch: {data['using_elasticsearch']}")
        print(f"Results Returned: {len(data['results'])}")
        
        if expected_method:
            method = (
                'elasticsearch'
                if data['using_elasticsearch']
                else 'database'
            )
            if method == expected_method:
                print(f"✓ Search method matches expected: {method}")
            else:
                print(
                    f"✗ Search method mismatch: "
                    f"expected {expected_method}, got {method}"
                )
        
        if data['results']:
            print("\nTop 3 Results:")
            for i, result in enumerate(data['results'][:3], 1):
                print(f"\n{i}. {result.get('title', 'N/A')}")
                print(f"   Video ID: {result.get('video_id', 'N/A')}")
                if 'score' in result:
                    print(f"   Score: {result['score']:.2f}")
                if 'highlights' in result:
                    print(
                        f"   Highlights: "
                        f"{list(result['highlights'].keys())}"
                    )
                    
    except requests.exceptions.JSONDecodeError as e:
        print(f"❌ Error: Received non-JSON response")
        print(f"Response content: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def test_fuzzy_search(
    session: requests.Session,
    base_url: str
) -> None:
    """
    Test fuzzy search with intentional misspellings.
    
    Parameters:
        session (requests.Session): HTTP session with profile cookie.
        base_url (str): Base URL of the application.
    """
    print_section("Testing Fuzzy Search (Misspellings)")
    
    test_queries = [
        ("sermin", "Should match 'sermon'"),
        ("Jonh", "Should match 'John'"),
        ("bibel", "Should match 'bible'"),
    ]
    
    for query, description in test_queries:
        print(f"\n{description}")
        print(f"Query: '{query}'")
        
        try:
            response = session.get(
                f"{base_url}/api/search/",
                params={'q': query, 'per_page': 3},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Found {data['total']} results")
                if data['results']:
                    print(
                        f"  Top result: "
                        f"{data['results'][0].get('title', 'N/A')}"
                    )
            else:
                print(f"✗ Error: {response.status_code}")
                
        except requests.exceptions.JSONDecodeError:
            print(f"✗ Error: Received non-JSON response")
        except Exception as e:
            print(f"✗ Error: {e}")


def test_filtered_search(
    session: requests.Session,
    base_url: str
) -> None:
    """
    Test search with filters.
    
    Parameters:
        session (requests.Session): HTTP session with profile cookie.
        base_url (str): Base URL of the application.
    """
    print_section("Testing Filtered Search")
    
    try:
        # Test with speaker filter
        response = session.get(
            f"{base_url}/api/search/",
            params={
                'q': 'sermon',
                'speaker': 'John Smith',
                'per_page': 5
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Search with speaker filter:")
            print(f"  Total Results: {data['total']}")
            print(f"  Filters Applied: {data['filters']}")
        else:
            print(f"✗ Error: {response.status_code}")
            
    except requests.exceptions.JSONDecodeError:
        print(f"✗ Error: Received non-JSON response")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_reindex(
    session: requests.Session,
    base_url: str
) -> None:
    """
    Test the reindex endpoint.
    
    Parameters:
        session (requests.Session): HTTP session with profile cookie.
        base_url (str): Base URL of the application.
    """
    print_section("Testing Reindex Endpoint")
    
    try:
        response = session.post(
            f"{base_url}/api/search/reindex",
            timeout=300  # 5 minute timeout for reindexing
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Reindexing completed successfully")
            print(f"  Success: {data.get('success', 0)}")
            print(f"  Failed: {data.get('failed', 0)}")
            print(f"  Total: {data.get('total', 0)}")
        elif response.status_code == 503:
            print(f"⚠ Elasticsearch not available")
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text[:500])
            
    except requests.exceptions.JSONDecodeError:
        print(f"✗ Error: Received non-JSON response")
        print(f"Response content: {response.text[:200]}")
    except requests.exceptions.Timeout:
        print(f"⚠ Reindexing timed out (may still be running)")
    except Exception as e:
        print(f"✗ Error: {e}")


def main() -> None:
    """
    Run all search tests.
    
    Executes a comprehensive test suite for the search functionality,
    including status checks, query tests, fuzzy matching, and reindexing.
    """
    base_url = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "http://localhost:5000"
    )
    
    print(f"Testing search functionality at: {base_url}")
    print("Using profile: guest")
    
    # Create session with profile cookie
    session = create_session_with_profile(base_url, "guest")
    
    try:
        # Check status
        status = test_search_status(session, base_url)
        
        # Determine expected search method
        expected_method = (
            'elasticsearch'
            if status['elasticsearch_available']
            else 'database'
        )
        
        # Test basic search
        test_search_query(session, base_url, "sermon", expected_method)
        
        # Test fuzzy search (only if Elasticsearch is available)
        if status['elasticsearch_available']:
            test_fuzzy_search(session, base_url)
        else:
            print(
                "\n⚠ Skipping fuzzy search tests "
                "(Elasticsearch not available)"
            )
        
        # Test filtered search
        test_filtered_search(session, base_url)
        
        # Test reindex endpoint
        print("\nDo you want to test reindexing? (y/N): ", end="")
        if input().lower() == 'y':
            test_reindex(session, base_url)
        
        print_section("Test Complete")
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to {base_url}")
        print("Make sure the application is running.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠ Tests interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()