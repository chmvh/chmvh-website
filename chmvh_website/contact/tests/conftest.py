import pytest


@pytest.fixture(scope="module")
def contact_info():
    return {
        "g-recaptcha-response": "Sample captcha response",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "message": "Test message content.",
    }
