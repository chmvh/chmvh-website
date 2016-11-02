import pytest


@pytest.fixture
def api_rf():
    """
    Fixture that creates an `APIRequestFactory` for testing.

    Returns:
        APIRequestFactory:
            An `APIRequestFactory` instance.
    """
    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()
