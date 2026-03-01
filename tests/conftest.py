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
