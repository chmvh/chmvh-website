import pytest


@pytest.fixture(scope="module")
def contact_info():
    return {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "message": "Test message content.",
    }
