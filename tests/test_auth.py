import pytest

from app.core.dev_auth import DevelopmentAuthenticator


def test_valid_employee_token():

    auth = DevelopmentAuthenticator()

    identity = auth.authenticate(
        "employee-token"
    )

    assert identity.user_id == "employee-001"
    assert identity.role == "employee"
    assert identity.department == "HR"


def test_valid_manager_token():

    auth = DevelopmentAuthenticator()

    identity = auth.authenticate(
        "manager-token"
    )

    assert identity.user_id == "manager-001"
    assert identity.role == "manager"
    assert identity.department == "Finance"


def test_invalid_token():

    auth = DevelopmentAuthenticator()

    with pytest.raises(ValueError):
        auth.authenticate(
            "invalid-token"
        )