"""
Module: fixtures.py

Fixtures for testing.
    Provides reusable fixtures for valid and invalid values.

Fixtures:
    valid_category_name
        Provides a valid category name for testing.
    invalid_category_name
        Provides an invalid category name for testing.
    valid_category_id
        Provides a valid category ID for testing.
    valid_subcategory_id
        Provides a valid subcategory ID for testing.
    invalid_category_id
        Provides an invalid category ID for testing.
    valid_video_id
        Provides a valid video ID for testing.
    invalid_video_id
        Provides an invalid video ID for testing.
    valid_character_id
        Provides a valid character ID for testing.
    invalid_character_id
        Provides an invalid character ID for testing.
    valid_speaker_id
        Provides a valid speaker ID for testing.
    invalid_speaker_id
        Provides an invalid speaker ID for testing.
    valid_tag_id
        Provides a valid tag ID for testing.
    invalid_tag_id
        Provides an invalid tag ID for testing.
    valid_scripture_name
        Provides a valid scripture name for testing.
    invalid_scripture_name
        Provides an invalid scripture name for testing.
    valid_scripture_id
        Provides a valid scripture ID for testing.
    invalid_scripture_id
        Provides an invalid scripture ID for testing.
    valid_location_id
        Provides a valid location ID for testing.
    invalid_location_id
        Provides an invalid location ID for testing.
    search_query
        Provides a search query for testing.
    page_number
        Provides a page number for testing pagination.
    per_page
        Provides the number of results per page for testing pagination.
    valid_speaker_name
        Provides a valid speaker name for testing.
    valid_character_name
        Provides a valid character name for testing.
    valid_location_name
        Provides a valid location name for testing.
    valid_tag_name
        Provides a valid tag name for testing.
"""


import pytest


@pytest.fixture
def valid_category_name() -> str:
    """
    Return a valid category name for testing.
    """

    return "Monthly Programs"


@pytest.fixture
def invalid_category_name() -> str:
    """
    Return an invalid category name for testing.
    """

    return "NonExistentCategory12345"


@pytest.fixture
def valid_category_id() -> int:
    """
    Return a valid category ID for testing.
    """

    return 1


@pytest.fixture
def valid_subcategory_id() -> int:
    """
    Return a valid subcategory ID for testing.
    """

    return 1340


@pytest.fixture
def invalid_category_id() -> int:
    """
    Return an invalid category ID for testing.
    """

    return 999999


@pytest.fixture
def valid_video_id() -> int:
    """
    Return a valid video ID for testing.
    """

    return 3011


@pytest.fixture
def invalid_video_id() -> int:
    """
    Return an invalid video ID for testing.
    """

    return 999999


@pytest.fixture
def valid_character_id() -> int:
    """
    Fixture to provide a valid character ID for testing.

    '1' is King David
    """

    return 1


@pytest.fixture
def invalid_character_id() -> int:
    """
    Fixture to provide an invalid character ID for testing.

    '9999' is assumed to be a non-existent character ID
    """

    return 9999


@pytest.fixture
def valid_speaker_id() -> int:
    """
    Fixture to provide a valid speaker ID for testing.

    '1' is assumed to be an existing speaker ID
    """

    return 1


@pytest.fixture
def invalid_speaker_id() -> int:
    """
    Fixture to provide an invalid speaker ID for testing.

    '9999' is assumed to be a non-existent speaker ID
    """

    return 9999


@pytest.fixture
def valid_tag_id() -> int:
    """
    Fixture to provide a valid tag ID for testing.

    '1' is assumed to be an existing tag ID
    """

    return 1


@pytest.fixture
def invalid_tag_id() -> int:
    """
    Fixture to provide an invalid tag ID for testing.

    '9999' is assumed to be a non-existent tag ID
    """

    return 9999


@pytest.fixture
def valid_scripture_name() -> str:
    """
    Fixture to provide a valid scripture name for testing.
    """

    return "John 1:1"


@pytest.fixture
def invalid_scripture_name() -> str:
    """
    Fixture to provide an invalid scripture name for testing.
    """

    return "John 9999:9999"


@pytest.fixture
def valid_scripture_id() -> int:
    """
    Fixture to provide a valid scripture ID for testing.
    """

    return 2


@pytest.fixture
def invalid_scripture_id() -> int:
    """
    Fixture to provide an invalid scripture ID for testing.
    """

    return 9999


@pytest.fixture
def valid_location_id() -> int:
    """
    Fixture to provide a valid location ID for testing.
    """

    return 1


@pytest.fixture
def invalid_location_id() -> int:
    """
    Fixture to provide an invalid location ID for testing.
    """

    return 9999


@pytest.fixture
def search_query() -> str:
    """
    Fixture to provide a search query for testing.
    """

    return "bible"


@pytest.fixture
def page_number() -> int:
    """
    Fixture to provide a page number for testing pagination.
    """

    return 1


@pytest.fixture
def per_page() -> int:
    """
    Fixture to provide the number of results per page for testing pagination.
    """

    return 10


@pytest.fixture
def valid_speaker_name() -> str:
    """
    Fixture to provide a valid speaker name for testing.
    """

    return "Stephen Lett"


@pytest.fixture
def valid_character_name() -> str:
    """
    Fixture to provide a valid character name for testing.
    """

    return "David"


@pytest.fixture
def valid_location_name() -> str:
    """
    Fixture to provide a valid location name for testing.
    """

    return "Samaria"


@pytest.fixture
def valid_tag_name() -> str:
    """
    Fixture to provide a valid tag name for testing.
    """

    return "prayer"
