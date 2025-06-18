import pytest
from data.user_credentials import valid_user, invalid_user

@pytest.fixture(scope="function")
def test_data():
    """Fixture to provide test data including user credentials"""
    return {
        "valid_user": valid_user,
        "invalid_user": invalid_user
    }
