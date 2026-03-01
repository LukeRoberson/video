# Testing

This is still in progress



Pytest

Test files are in /tests, start with test_* so they are discovered automatically.

Separate file for each API section (category, video, tag, etc) for testing valid/invalid responses.

test_performance.py for testing the response times of the endpoints.




conftest.py contains fixtures. pytest automatically detects this, so no imports are used.

pytest.ini in the root of the project



To do:
    Test response data better
    Eg, make sure the fields are all in place
    Consolidate error handling tests into one class?




Running tests

pytest                           # Run all tests
pytest -v                        # Verbose output
pytest -k "CategoryName"         # Run specific tests
pytest --cov                     # Check code coverage
